"""Pluma: dibujo a tinta y color plano a partir de un esqueleto 3D (estilo ilustrado, sin pixeles).

Cada pieza es una forma con volumen o una lámina plana pegada a un hueso. En cada cuadro las formas se
proyectan a la pantalla como curvas exactas y se pintan de atrás hacia adelante, como lo haría un
ilustrador:

1. contorno de tinta, más grueso del lado contrario a la luz, y uno más grueso alrededor de toda la silueta;
2. color plano;
3. lo que va pegado a la pieza (bolsillos, botones, ojos, boca, pecas), recortado a su forma;
4. sombra propia en media luna y sombras que proyectan las piezas de adelante, en una capa multiplicada;
5. luces, brillos y trazos interiores (pliegues, mechones).

Las calcas se pintan sobre la superficie de un elipsoide como si se proyectaran desde el frente, así que se
deforman y se esconden al girar la cabeza. Huesos, poses y animaciones funcionan igual que en el modelo de
volumen (`modelo.py`).
"""
import math

import numpy as np
import skia
import yaml

from . import color
from .modelo import Esqueleto, S, rot, tras, _sumar_poses, _mezclar_poses
from .fisica import Fisica, rejilla_campana, paño_abierto

REFLEJO = np.array([-1.0, 1, 1])
UNION, RESTA, CRUCE = (skia.PathOp.kUnion_PathOp, skia.PathOp.kDifference_PathOp,
                       skia.PathOp.kIntersect_PathOp)
FORMAS = ('elipsoide', 'tubo', 'casco', 'caja', 'cilindro', 'lamina', 'cinta', 'mechones', 'campana')


# ---------------------------------------------------------------------------- 2D
def _c4(hexa, a=1.0):
    r, g, b = color.hex_a_rgb(hexa) / 255
    return skia.Color4f(float(r), float(g), float(b), float(a))


def _pintura(hexa, a=1.0, blur=0.0, modo=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor4f(_c4(hexa, a))
    if blur > 0.05:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, float(blur)))
    if modo is not None:
        p.setBlendMode(modo)
    return p


def _camino(pts):
    p = skia.Path()
    if len(pts) >= 3:
        p.addPoly([skia.Point(float(x), float(y)) for x, y in pts], True)
    return p


def _mover(camino, d):
    q = skia.Path(camino)
    q.offset(float(d[0]), float(d[1]))
    return q


def _op_o_nada(a, b, op):
    """skia.Op con reintentos: la geometría casi coincidente a veces la hace fallar; corrida una fracción de
    pixel o simplificada, casi siempre funciona. Devuelve None si no hubo caso."""
    intentos = (lambda: (a, b), lambda: (a, _mover(b, (0.013, 0.007))), lambda: (_simplificar(a), _simplificar(b)),
                lambda: (a, _mover(b, (-0.011, 0.017))))
    for intento in intentos:
        x, y = intento()
        if x is None or y is None:
            continue
        try:
            r = skia.Op(x, y, op)
        except Exception:
            r = None
        if r is not None:
            return r
    return None


def _op(a, b, op):
    r = _op_o_nada(a, b, op)
    return r if r is not None else skia.Path(a if op == RESTA else skia.Path())


def _restar(base, agujeros):
    """Resta los agujeros; si la operación falla, arma el mismo camino con la regla par-impar."""
    for h in agujeros:
        r = _op_o_nada(base, h, RESTA)
        if r is None:
            r = skia.Path(base)
            r.addPath(h)
            r.setFillType(skia.PathFillType.kEvenOdd)
            r = _simplificar(r) or r
        base = r
    return base


def _union(caminos):
    caminos = [c for c in caminos if c is not None and not c.isEmpty()]
    if not caminos:
        return skia.Path()
    if len(caminos) == 1:
        return caminos[0]
    b = skia.OpBuilder()
    for c in caminos:
        b.add(c, UNION)
    try:
        r = b.resolve()
        if r is not None:
            return r
    except RuntimeError:
        pass
    # Si la unión de todo junto falla (geometría degenerada), se une de a una, saltando lo que no se pueda
    acc = skia.Path()
    for c in caminos:
        r = _op_o_nada(acc, c, UNION)
        if r is not None:
            acc = r
    return acc


def _simplificar(c):
    try:
        return skia.Simplify(c)
    except Exception:
        return None


def _contorno_de(camino, ancho):
    """El trazo de un camino convertido en relleno (para unirlo, moverlo o recortarlo)."""
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=float(ancho),
                   StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap)
    out = skia.Path()
    p.getFillPath(camino, out)
    return out


def _tinta(cv, camino, ancho, luz2, extra, pintura):
    """Contorno de tinta de ancho `ancho`, más grueso del lado contrario a la luz (hasta `ancho·(1+extra)`).

    El engrosamiento es la banda del borde que cae bajo la forma corrida hacia la sombra. Se recorta con el
    lienzo (no con una operación booleana) para que respete exactamente la forma, por compleja que sea; al
    limitarlo a una banda, las puntas finas no rellenan el hueco que las separa del resto."""
    cv.drawPath(_contorno_de(camino, ancho), pintura)
    if extra <= 0:
        return
    cv.save()
    cv.clipPath(_mover(camino, -luz2 * ancho * extra * 1.2), skia.ClipOp.kIntersect, True)
    cv.drawPath(_contorno_de(camino, ancho * (1 + 2 * extra)), pintura)
    cv.restore()


def _engordar(camino, r):
    return _union([camino, _contorno_de(camino, 2 * r)]) if r > 0 else camino


def _casco2d(pts):
    P = sorted(set(map(tuple, np.round(np.asarray(pts, float), 3))))
    if len(P) < 3:
        return np.array(P)

    def cruz(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    abajo, arriba = [], []
    for p in P:
        while len(abajo) >= 2 and cruz(abajo[-2], abajo[-1], p) <= 0:
            abajo.pop()
        abajo.append(p)
    for p in reversed(P):
        while len(arriba) >= 2 and cruz(arriba[-2], arriba[-1], p) <= 0:
            arriba.pop()
        arriba.append(p)
    return np.array(abajo[:-1] + arriba[:-1])


def _circulo(c, r, paso=1.2):
    if r <= 0.05:
        return np.asarray(c, float)[None]
    n = max(12, int(math.tau * r / paso))
    th = np.linspace(0, math.tau, n, endpoint=False)
    return np.asarray(c, float) + r * np.stack([np.cos(th), np.sin(th)], 1)


def _radio_ef(pts):
    """2·área/perímetro: el radio de un círculo, la mitad del ancho de una tira larga."""
    if len(pts) < 3:
        return 0.0
    x, y = pts[:, 0], pts[:, 1]
    a = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
    per = np.sum(np.hypot(*(np.roll(pts, -1, 0) - pts).T))
    return float(2 * a / max(per, 1e-6))


def _catmull(P, n=8, cerrado=False):
    """Curva suave que pasa por los puntos (de cualquier dimensión: x, y, z, radio...)."""
    P = np.asarray(P, float)
    if len(P) < 3 and not cerrado:
        t = np.linspace(0, 1, n * max(len(P) - 1, 1) + 1)[:, None]
        return P[0] + (P[-1] - P[0]) * t if len(P) > 1 else P
    E = np.vstack([P[-1:], P, P[:2]]) if cerrado else np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    t = np.linspace(0, 1, n, endpoint=False)[:, None]
    seg = []
    for i in range(len(E) - 3):
        p0, p1, p2, p3 = E[i:i + 4]
        seg.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out = np.vstack(seg)
    return out if cerrado else np.vstack([out, P[-1:]])


def _perfil(valores, n):
    v = np.atleast_1d(np.asarray(valores, float))
    if len(v) == 1:
        return np.full(n, v[0])
    return np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(v)), v)


def _tira2d(pts, anchos):
    """Polígono de un trazo de ancho variable (punta fina donde el ancho llega a 0)."""
    pts = np.asarray(pts, float)
    w = np.broadcast_to(np.asarray(anchos, float), (len(pts),))
    d = np.gradient(pts, axis=0)
    d /= np.maximum(np.hypot(d[:, 0], d[:, 1]), 1e-9)[:, None]
    n = np.stack([-d[:, 1], d[:, 0]], 1) * (w / 2)[:, None]
    return np.vstack([pts + n, (pts - n)[::-1]])


def _rect(w, h, r, n=7):
    r = min(r, w / 2, h / 2)
    if r <= 0:
        return np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]])
    pts = []
    for cx, cy, a0 in [(w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0),
                       (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180)]:
        for a in np.radians(np.linspace(a0, a0 + 90, n)):
            pts.append([cx + r * math.cos(a), cy + r * math.sin(a)])
    return np.array(pts)


def forma2d(d):
    """Una forma plana en unidades del modelo: lista de (puntos, +1 suma / -1 agujero).

    circulo: r · ovalo: [rx, ry] · rect: [ancho, alto] (+ radio) · contorno: [[x, y], ...] (suave: true) ·
    trazo: [[x, y], ...] con ancho o anchos (trazo de ancho variable). Todas aceptan centro, angulo y
    agujeros.
    """
    c = np.asarray(d.get('centro', [0, 0]), float)
    a = math.radians(d.get('angulo', 0))
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    if 'circulo' in d:
        pts = _circulo([0, 0], d['circulo'], paso=0.2)
    elif 'ovalo' in d:
        rx, ry = d['ovalo']
        th = np.linspace(0, math.tau, max(24, int(4 * (rx + ry))), endpoint=False)
        pts = np.stack([rx * np.cos(th), ry * np.sin(th)], 1)
    elif 'rect' in d:
        pts = _rect(*d['rect'], d.get('radio', 0))
    elif 'contorno' in d:
        pts = np.asarray(d['contorno'], float)
        if d.get('suave', True):
            pts = _catmull(pts, 10, cerrado=True)
    elif 'trazo' in d:
        P = np.asarray(d['trazo'], float)
        if d.get('suave', True) and len(P) > 2:
            P = _catmull(P, 10)
        elif len(P) == 2:
            P = _catmull(P, 12)
        pts = _tira2d(P, _perfil(d.get('anchos', d.get('ancho', 0.6)), len(P)))
    else:
        raise ValueError(f'Forma plana sin tipo: {d}')
    salida = [(pts @ R.T + c, 1)]
    for h in d.get('agujeros', []):
        salida += [(p, -1) for p, _ in forma2d(h)]
    return salida


def _elipse(c2, A):
    """Camino de la elipse {c + A·u : |u| = 1} (la sombra exacta de un elipsoide)."""
    w, Q = np.linalg.eigh(A @ A.T)
    ax = np.sqrt(np.maximum(w, 1e-9))
    p = skia.Path()
    p.addOval(skia.Rect.MakeLTRB(-ax[0], -ax[1], ax[0], ax[1]))
    m = skia.Matrix()
    m.setAll(Q[0, 0], Q[0, 1], c2[0], Q[1, 0], Q[1, 1], c2[1], 0, 0, 1)
    p.transform(m)
    return p, ax


def _unitarios(xy, r, giro=None):
    xy = np.atleast_2d(np.asarray(xy, float))
    ux, uy = xy[:, 0] / r[0], xy[:, 1] / r[1]
    s = ux ** 2 + uy ** 2
    k = np.where(s > 1, 1 / np.sqrt(np.maximum(s, 1e-12)), 1.0)
    ux, uy = ux * k, uy * k
    U = np.stack([ux, uy, np.sqrt(np.maximum(0, 1 - ux ** 2 - uy ** 2))], 1)
    if giro:
        G = (rot([0, giro[0], 0]) @ rot([-(giro[1] if len(giro) > 1 else 0), 0, 0]))[:3, :3]
        U = U @ G.T
    return U


def _contornos(camino):
    """Los contornos de un camino como listas de puntos."""
    V = skia.Path.Verb
    pts = [(q.fX, q.fY) for q in camino.getPoints()]
    salida, actual, i = [], [], 0
    for v in camino.getVerbs():
        if v == V.kMove_Verb:
            if len(actual) > 2:
                salida.append(np.array(actual))
            actual = [pts[i]]
            i += 1
        elif v == V.kLine_Verb:
            actual.append(pts[i])
            i += 1
        elif v in (V.kQuad_Verb, V.kConic_Verb):
            actual.append(pts[i + 1])
            i += 2
        elif v == V.kCubic_Verb:
            actual.append(pts[i + 2])
            i += 3
    if len(actual) > 2:
        salida.append(np.array(actual))
    return salida


def _densificar(pts, paso):
    out = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n = max(1, int(np.ceil(np.linalg.norm(b - a) / paso)))
        out.append(a + (b - a) * (np.arange(n)[:, None] / n))
    return np.vstack(out)


def _region_visible(a, n=128):
    """La parte del disco unidad (ux, uy) cuyo punto de la semiesfera delantera cumple U·a ≥ 0.

    El borde es medio círculo unidad (el contorno de la pieza vista de frente) y media gran circunferencia
    (el horizonte visto desde la cámara). Devuelve None si no se ve nada."""
    a = np.asarray(a, float) / np.linalg.norm(a)
    h = math.hypot(a[0], a[1])
    if h < 1e-6:
        return _circulo([0, 0], 1.0, paso=math.tau / n) if a[2] > 0 else None
    P = np.array([-a[1], a[0], 0.0]) / h
    Q = np.cross(a, P)
    if Q[2] < 0:
        Q = -Q
    th = np.linspace(0, math.pi, n)
    gran = np.outer(np.cos(th), P) + np.outer(np.sin(th), Q)
    f_ini = math.atan2(-P[1], -P[0])
    d = (math.atan2(a[1], a[0]) - f_ini + math.pi) % math.tau - math.pi
    f = f_ini + math.copysign(1.0, d) * np.linspace(0, math.pi, n)
    return np.vstack([gran[:, :2], np.stack([np.cos(f), np.sin(f)], 1)])


def sobre_elipsoide(xy, r, giro=None, alza=0.0):
    """Puntos (x, y) dibujados de frente → puntos sobre el elipsoide (marco local) y sus normales.

    Es como proyectar una calca con un proyector que mira la pieza desde su frente (+Z), o desde el
    ángulo `giro` = [giro horizontal, altura] en grados. Lo que cae fuera del óvalo se pega al borde.
    """
    xy = np.atleast_2d(np.asarray(xy, float))
    ux, uy = xy[:, 0] / r[0], xy[:, 1] / r[1]
    s = ux ** 2 + uy ** 2
    k = np.where(s > 1, 1 / np.sqrt(np.maximum(s, 1e-12)), 1.0)
    ux, uy = ux * k, uy * k
    U = np.stack([ux, uy, np.sqrt(np.maximum(0, 1 - ux ** 2 - uy ** 2))], 1)
    if giro:
        G = (rot([0, giro[0], 0]) @ rot([-(giro[1] if len(giro) > 1 else 0), 0, 0]))[:3, :3]
        U = U @ G.T
    P = U * r
    N = U / r
    N /= np.linalg.norm(N, axis=1, keepdims=True)
    return P + N * np.atleast_1d(alza)[:, None] if np.any(alza) else P, N


def _curva(u, tipo='suave'):
    """Cómo se reparte el movimiento entre dos claves."""
    if tipo == 'lineal':
        return u
    if tipo == 'entrada':
        return u ** 3
    if tipo == 'salida':
        return 1 - (1 - u) ** 3
    if tipo == 'sobrepaso':
        c = 1.70158
        return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
    return u * u * (3 - 2 * u)


def _arco(a, b, u):
    """Dirección intermedia entre a y b por el arco más corto (u de 0 a 1)."""
    a = np.asarray(a, float) / np.linalg.norm(a)
    b = np.asarray(b, float) / np.linalg.norm(b)
    w = math.acos(float(np.clip(a.dot(b), -1, 1)))
    if w < 1e-4:
        return a
    return (math.sin((1 - u) * w) * a + math.sin(u * w) * b) / math.sin(w)


def _euler(R):
    """Ángulos [x, y, z] en grados tales que rot(ángulos) = R (orden X, luego Y, luego Z)."""
    y = -math.asin(float(np.clip(R[2, 0], -1, 1)))
    x = math.atan2(R[2, 1], R[2, 2])
    z = math.atan2(R[1, 0], R[0, 0])
    return [math.degrees(x), math.degrees(y), math.degrees(z)]


# ---------------------------------------------------------------------------- materiales y modelo
class Material:
    def __init__(self, nombre, d, tinta):
        self.nombre = nombre
        self.color = d['color']
        rampa = color.rampa(self.color, 5, 2, d.get('dL', 0.12), d.get('giro', 14.0))
        self.sombra = d.get('sombra', rampa[1])
        self.hondo = d.get('hondo', rampa[0])
        self.luz = d.get('luz', rampa[3])
        self.opacidad = d.get('opacidad', 1.0)
        self.linea = d.get('linea', tinta)
        self.ancho_sombra = d.get('ancho_sombra', 0.36)
        self.suave = d.get('suave', 0.35)
        self.brillo = d.get('brillo', 0.0)
        self.ancho_luz = d.get('ancho_luz', 0.2)
        self.sin_sombra = d.get('sin_sombra', False)
        self.aura = d.get('aura')
        self.borde_suave = d.get('borde_suave')
        self.sin_grano = d.get('sin_grano', False)
        base, sb = color.hex_a_rgb(self.color), color.hex_a_rgb(self.sombra)
        self.multiplica = color.rgb_a_hex(np.clip(sb / np.maximum(base, 1) * 255, 0, 255))

    def tono(self, nombre):
        return {'hondo': self.hondo, 'sombra': self.sombra, 'luz': self.luz, 'color': self.color,
                'linea': self.linea}.get(nombre, nombre)


CLAVES_PIEZA = {'nombre', 'hueso', 'forma', 'pos', 'rot', 'material', 'grupo', 'capa', 'dentro_de', 'fuera_de',
                'debajo_de', 'encima_de',
                'sin_linea', 'grosor', 'proyecta', 'recibe', 'calcas', 'trazos', 'op', 'oculta', 'espejo', 'lados',
                'sin_silueta'}


class Dibujo(Esqueleto):
    def __init__(self, ruta_o_dict):
        if isinstance(ruta_o_dict, dict):
            d = ruta_o_dict
        else:
            with open(ruta_o_dict, encoding='utf-8') as f:
                d = yaml.safe_load(f)
        self.d = d
        self.nombre = d.get('nombre', 'dibujo')
        self.lienzo = tuple(d.get('lienzo', [512, 640]))
        self.origen = tuple(d.get('origen', [self.lienzo[0] / 2, self.lienzo[1] - 24]))
        self.escala = d.get('escala', 4.0)
        self.camara = {'yaw': 0.0, 'pitch': 0.0, **d.get('camara', {})}
        luz = np.asarray(d.get('luz', [-0.6, 0.75, 0.6]), float)
        self.luz = luz / np.linalg.norm(luz)
        self.luz_camara = d.get('luz_camara', True)
        self.tinta = d.get('tinta', '#0e1030')
        self.grosor = d.get('grosor', 0.55)
        self.grosor_silueta = d.get('grosor_silueta', 1.1)
        self.proyectada = d.get('sombra_proyectada', 1.6)
        self.degradado = d.get('degradado')
        self.contraluz = d.get('contraluz')
        self.peso_sombra = d.get('peso_sombra', 0.75)
        self.grano = d.get('grano', 0.0)
        self.linea_encima = d.get('linea_encima', False)
        self.materiales = {n: Material(n, md, self.tinta) for n, md in d.get('materiales', {}).items()}
        self._armar_huesos(d.get('huesos', [{'nombre': 'raiz'}]))
        self._resolver_apuntes()
        self.piezas = self._expandir(d.get('piezas', []))
        self.poses = d.get('poses', {})
        self.animaciones = d.get('animaciones', {})
        self.fisica = Fisica(self) if d.get('fisica') else None
        self._estados = {}

    def _rot_para(self, n, pose_total, hacia, frente):
        """Giro de pose (sumado a la base) que deja el eje +Y del hueso `n` apuntando a `hacia`."""
        h = self.huesos[n]
        W = self.matrices(pose_total, 0.0)
        Rp = W[h['padre']][:3, :3] if h.get('padre') else np.eye(3)
        y = np.asarray(hacia, float)
        y /= np.linalg.norm(y)
        ref = np.asarray(frente, float)
        z = ref - ref.dot(y) * y
        z /= np.linalg.norm(z)
        Rw = np.column_stack([np.cross(y, z), y, z])
        return np.array(_euler(rot(h.get('rot', [0, 0, 0]))[:3, :3].T @ Rp.T @ Rw))

    def _direccion(self, clave, n):
        """Hacia dónde apunta el hueso `n` en una clave: lo que diga su `apunta`, o su dirección base."""
        h = self.huesos[n]
        spec = (clave.get('apunta') or {}).get(n)
        if spec is None:
            return np.asarray(h['apunta'], float), np.asarray(h.get('frente', [0, 0, 1]), float)
        if isinstance(spec, dict):
            return np.asarray(spec['hacia'], float), np.asarray(spec.get('frente', h.get('frente', [0, 0, 1])), float)
        return np.asarray(spec, float), np.asarray(h.get('frente', [0, 0, 1]), float)

    def _tramo(self, claves, t):
        """Las dos claves que rodean la fase t y el avance entre ellas, ya pasado por la curva de la clave."""
        if t <= claves[0]['t']:
            return claves[0], claves[0], 0.0
        if t >= claves[-1]['t']:
            return claves[-1], claves[-1], 0.0
        for c0, c1 in zip(claves, claves[1:]):
            if c0['t'] <= t <= c1['t']:
                u = (t - c0['t']) / max(c1['t'] - c0['t'], 1e-9)
                return c0, c1, _curva(u, c1.get('curva', 'suave'))
        return claves[-1], claves[-1], 0.0

    def _mezcla(self, claves, t):
        c0, c1, u = self._tramo(claves, t)
        return _mezclar_poses(c0.get('pose') or {}, c1.get('pose') or {}, u, t)

    def pose_de(self, anim=None, cuadro=0):
        """La pose de un cuadro. Además de lo del esqueleto:

        - las claves aceptan `curva`: suave, lineal, entrada (arranca lento), salida (frena al final) o
          sobrepaso (se pasa un poco y vuelve), para que los golpes y los frenos se sientan;
        - `retraso: {hueso: fracción}` hace que ese hueso siga la animación un poco más tarde que el resto
          (capas, puntas y trapos que arrastran el movimiento);
        - los huesos con `apunta` en las claves siguen un arco: se interpola su dirección y el giro de la
          muñeca se resuelve en cada cuadro.
        """
        a = self.animaciones.get(anim) if anim else None
        if not a or 'claves' not in a:
            return super().pose_de(anim, cuadro)
        n_cuadros = a.get('cuadros', 1)
        bucle = a.get('bucle', True)
        t = cuadro / n_cuadros if bucle else cuadro / max(n_cuadros - 1, 1)
        claves = sorted(a['claves'], key=lambda k: k['t'])
        pose = self._mezcla(claves, t)
        for n, d in (a.get('retraso') or {}).items():
            tb = (t - d) % 1.0 if bucle else min(max(t - d, 0.0), 1.0)
            pose[n] = self._mezcla(claves, tb).get(n, {'rot': [0, 0, 0], 'pos': [0, 0, 0]})
        huesos = {n for k in claves for n in (k.get('apunta') or {})}
        if not huesos:
            return pose, t
        k0, k1, u = self._tramo(claves, t)
        base = self.d.get('pose_base', {})
        for n in huesos:
            (d0, f0), (d1, f1) = self._direccion(k0, n), self._direccion(k1, n)
            d = _arco(d0, d1, u)
            f = _arco(f0, f1, u)
            pose.pop(n, None)
            total = _sumar_poses(base, pose, t)
            total.pop(n, None)
            r = self._rot_para(n, total, d, f)
            r_base = np.asarray((_sumar_poses(base, {}, 0.0).get(n) or {}).get('rot', [0, 0, 0]), float)
            pose[n] = {'rot': [float(v) for v in r - r_base]}
        return pose, t

    def _resolver_apuntes(self):
        """Huesos con `apunta: [x, y, z]`: su eje +Y se orienta a esa dirección del mundo en la pose base
        (con `frente` como guía para su eje +Z). Así un báculo o un libro quedan donde deben aunque cambie el
        brazo que los sostiene; las animaciones giran encima de esa orientación."""
        base = self.d.get('pose_base', {})
        for n in self.orden:
            h = self.huesos[n]
            if 'apunta' not in h:
                continue
            if h['lado']:
                raise ValueError(f'Hueso "{n}": `apunta` no funciona en huesos con espejo.')
            W = self.matrices(_sumar_poses(base, {}, 0.0), 0.0)
            Rp = W[h['padre']][:3, :3] if h.get('padre') else np.eye(3)
            y = np.asarray(h['apunta'], float)
            y /= np.linalg.norm(y)
            ref = np.asarray(h.get('frente', [0, 0, 1]), float)
            z = ref - ref.dot(y) * y
            z /= np.linalg.norm(z)
            Rw = np.column_stack([np.cross(y, z), y, z])
            prot = np.asarray((base.get(n) or {}).get('rot', [0, 0, 0]) if isinstance(base.get(n), dict)
                              else (base.get(n) or [0, 0, 0]), float)
            Rl = Rp.T @ Rw @ rot(prot)[:3, :3].T
            h['rot'] = _euler(Rl)

    def _expandir(self, lista):
        nombres_espejados = set()
        for pz in lista:
            if pz.get('espejo') or pz.get('hueso', self.orden[0]) in self.espejados:
                nombres_espejados.add(pz.get('nombre'))
        salida = []
        for pz in lista:
            if pz.get('oculta'):
                continue
            nombre = pz.get('nombre', pz.get('forma'))
            if pz.get('forma') not in FORMAS:
                raise ValueError(f'Pieza "{nombre}": forma "{pz.get("forma")}" desconocida. Opciones: {", ".join(FORMAS)}')
            if pz.get('material') not in self.materiales:
                raise ValueError(f'Pieza "{nombre}": material "{pz.get("material")}" no definido.')
            hueso = pz.get('hueso', self.orden[0])
            lados = ('i', 'd') if nombre in nombres_espejados else (None,)
            base_pz = pz
            for lado in lados:
                # `lados: {d: {...}}` cambia algo solo de un lado (p. ej. el brazo del bastón fuera de la capa)
                pz = {**base_pz, **(base_pz.get('lados') or {}).get(lado, {})} if lado else base_pz
                hb = f'{hueso}.{lado}' if (lado and hueso in self.espejados) else hueso
                if hb not in self.huesos:
                    raise ValueError(f'Pieza "{nombre}": hueso "{hueso}" no existe.')
                L = tras(pz.get('pos', [0, 0, 0])) @ rot(pz.get('rot', [0, 0, 0]))
                if lado == 'd':
                    L = S @ L @ S
                suf = f'.{lado}' if lado else ''
                padre = pz.get('dentro_de')
                if padre and lado and padre in nombres_espejados:
                    padre += suf
                salida.append(dict(
                    nombre=nombre + suf, base=nombre, hueso=hb, local=L, lado=lado, forma=pz['forma'],
                    p={k: v for k, v in pz.items() if k not in CLAVES_PIEZA},
                    mat=self.materiales[pz['material']], grupo=pz.get('grupo', nombre) + suf,
                    capa=pz.get('capa', 0.0), dentro_de=padre, linea=not pz.get('sin_linea', False),
                    grosor=pz.get('grosor', 1.0), proyecta=pz.get('proyecta', True),
                    recibe=pz.get('recibe', True), calcas=pz.get('calcas', []), trazos=pz.get('trazos', []),
                    op=pz.get('op', 'union'), silueta=not pz.get('sin_silueta', False),
                    fuera_de=pz.get('fuera_de'), debajo_de=pz.get('debajo_de', []),
                    encima_de=pz.get('encima_de', [])))
        return salida

    def esqueleto_de(self, anim=None, cuadro=0, pose=None):
        """Las matrices de mundo de los huesos en un cuadro (sin la física de la ropa)."""
        if pose is None:
            pose, t = self.pose_de(anim, cuadro)
        else:
            t = 0.0
        return self.matrices(_sumar_poses(self.d.get('pose_base', {}), pose, t), t)

    def estado_fisica(self, anim=None, cuadro=0, pose=None):
        """Dónde está la ropa simulada en un cuadro. Cada animación se simula una vez, entera y en orden."""
        if self.fisica is None:
            return None
        if pose is not None:
            return self.fisica.simular([self.esqueleto_de(pose=pose)], 24, False)[0]
        clave = anim if anim in self.animaciones else (anim or '_reposo')
        if clave not in self._estados:
            if anim in self.animaciones:
                a = self.animaciones[anim]
                Ws = [self.esqueleto_de(anim, i) for i in range(a.get('cuadros', 1))]
                self._estados[clave] = self.fisica.simular(Ws, a.get('fps', 12), a.get('bucle', True))
            else:
                self._estados[clave] = self.fisica.simular([self.esqueleto_de(anim, 0)], 24, False)
        estados = self._estados[clave]
        return estados[min(cuadro, len(estados) - 1)]

    def hueso_lado(self, nombre, lado):
        if nombre in self.espejados:
            return f'{nombre}.{lado or "i"}'
        if nombre not in self.huesos:
            raise ValueError(f'Hueso "{nombre}" no existe.')
        return nombre

    def cara_de(self, anim=None, cuadro=0):
        """La expresión de la cara en un cuadro: `cara` de la animación, de sus claves o de sus tramos."""
        cara = self.d.get('cara', 'normal')
        if not anim or anim not in self.animaciones:
            return self.poses.get(anim, {}).get('_cara', cara) if anim in self.poses else cara
        a = self.animaciones[anim]
        n = a.get('cuadros', 1)
        t = cuadro / n if a.get('bucle', True) else cuadro / max(n - 1, 1)
        cara = a.get('cara', cara)
        for k in sorted(a.get('claves', []), key=lambda k: k['t']):
            if k['t'] <= t + 1e-9 and 'cara' in k:
                cara = k['cara']
        for tramo in a.get('caras', []):
            if tramo['desde'] <= t < tramo['hasta']:
                cara = tramo['cara']
        return cara


# ---------------------------------------------------------------------------- cámara
class Vista:
    def __init__(self, dib, yaw, pitch, zoom=1.0):
        self.V = (rot([pitch, 0, 0]) @ rot([0, yaw, 0]))[:3, :3]
        self.esc = dib.escala * zoom
        self.o = np.array(dib.origen, float) * zoom
        self.tam = (int(round(dib.lienzo[0] * zoom)), int(round(dib.lienzo[1] * zoom)))
        L = dib.luz if dib.luz_camara else self.V @ dib.luz
        l2 = np.array([L[0], -L[1]])
        m = float(np.hypot(*l2))
        self.luz2 = l2 / max(m, 1e-6)
        self.fuerza = float(np.clip(m, 0.4, 1.0))
        self.P2 = (np.array([[1.0, 0, 0], [0, -1.0, 0]]) @ self.V) * self.esc

    def pant(self, Pw):
        Pc = np.atleast_2d(Pw) @ self.V.T
        return np.stack([self.o[0] + self.esc * Pc[:, 0], self.o[1] - self.esc * Pc[:, 1]], 1)

    def prof(self, Pw):
        return (np.atleast_2d(Pw) @ self.V.T)[:, 2]

    def de_frente(self, Nw):
        return (np.atleast_2d(Nw) @ self.V.T)[:, 2]


# ---------------------------------------------------------------------------- proyección de piezas
class _Proyector:
    def __init__(self, dib, W, vista, cara):
        self.dib, self.W, self.v, self.cara = dib, W, vista, cara
        self.telas = {}

    def rejilla(self, pz):
        """Los puntos de una campana en su marco: los simulados si la tela tiene física, si no los de diseño."""
        G, radios, ang = rejilla_campana(pz['p'])
        tela = self.telas.get(pz['nombre'])
        if tela is None:
            return G, G, radios, ang
        M = self.matriz(pz)
        return (tela - M[:3, 3]) @ M[:3, :3], G, radios, ang

    def deformador(self, pz, G, G0):
        """Lleva puntos pegados a una tela (pliegues dibujados) con la deformación de la tela simulada."""
        if G is G0:
            return None
        M = self.matriz(pz)
        P0, D = G0.reshape(-1, 3), (G - G0).reshape(-1, 3)

        def f(Pw):
            L = (np.atleast_2d(Pw) - M[:3, 3]) @ M[:3, :3]
            d2 = ((L[:, None, :] - P0[None]) ** 2).sum(2)
            cerca = np.argsort(d2, 1)[:, :4]
            w = 1 / (np.take_along_axis(d2, cerca, 1) + 1.0)
            disp = (D[cerca] * w[..., None]).sum(1) / w.sum(1, keepdims=True)
            return (L + disp) @ M[:3, :3].T + M[:3, 3]
        return f

    def matriz(self, pz):
        return self.W[pz['hueso']] @ pz['local']

    def puntos(self, pz, specs):
        """[x, y, z, extra...] en el marco de la pieza, o [hueso, x, y, z, extra...] en el de otro hueso."""
        M0 = self.matriz(pz)
        P, X, R = [], [], []
        for s in specs:
            if isinstance(s[0], str):
                M = self.W[self.dib.hueso_lado(s[0], pz['lado'])]
                v = s[1:]
            else:
                M, v = M0, s
            p = np.asarray(v[:3], float)
            if pz['lado'] == 'd':
                p = p * REFLEJO
            P.append((M @ np.append(p, 1))[:3])
            X.append(list(v[3:]))
            R.append(M[:3, :3])
        return np.array(P), X, R

    def proyectar(self, pz):
        f = getattr(self, '_' + pz['forma'])
        miembros = f(pz)
        for m in miembros:
            m.setdefault('pieza', pz)
        return miembros

    def _dentro_de_campanas(self, nombres, Pw):
        """Dentro de alguna de las campanas (`fuera_de` acepta un nombre o una lista)."""
        nombres = [nombres] if isinstance(nombres, str) else nombres
        dentro = np.zeros(len(np.atleast_2d(Pw)), bool)
        for n in nombres:
            dentro |= self._dentro_de_campana(n, Pw)
        return dentro

    def _dentro_de_campana(self, nombre, Pw):
        """Qué puntos del mundo quedan dentro del volumen de la campana `nombre` (entre su ruedo y su aro de
        arriba, dentro de la elipse que forman los aros a esa altura)."""
        cap = next((q for q in self.dib.piezas if q['nombre'] == nombre and q['forma'] == 'campana'), None)
        if cap is None:
            raise ValueError(f'fuera_de: "{nombre}" no es una pieza con forma campana.')
        M = self.matriz(cap)
        L = (np.atleast_2d(Pw) - M[:3, 3]) @ M[:3, :3]
        G, _, _, ang = self.rejilla(cap)
        R, K, _ = G.shape
        # el perfil de la tela (de arriba abajo) en el ángulo de cada punto
        u = ((np.arctan2(L[:, 0], L[:, 2]) - ang[0]) / (math.tau / K)) % K
        k0 = np.floor(u).astype(int) % K
        f = (u - np.floor(u))[None, :, None]
        perfil = G[:, k0] * (1 - f) + G[:, (k0 + 1) % K] * f
        yr, rr = perfil[..., 1], np.hypot(perfil[..., 0], perfil[..., 2])
        q = np.hypot(L[:, 0], L[:, 2])
        dentro = (L[:, 1] >= yr[0]) & (L[:, 1] <= yr[0] + 4) & (q < rr[0])
        for j in range(R - 1):
            ya, yb = yr[j], yr[j + 1]
            entre = (L[:, 1] <= np.maximum(ya, yb)) & (L[:, 1] >= np.minimum(ya, yb))
            w = np.clip((L[:, 1] - ya) / np.where(np.abs(yb - ya) > 1e-6, yb - ya, 1.0), 0, 1)
            dentro |= entre & (q < rr[j] + (rr[j + 1] - rr[j]) * w)
        abertura = cap['p'].get('abertura', 0)
        if abertura:
            # lo que queda en la abertura de adelante se ve aunque esté dentro de la campana
            ang = np.degrees(np.arctan2(L[:, 0], L[:, 2]))
            dentro &= ~((np.abs(ang) < abertura / 2) & (L[:, 2] > 0))
        return dentro

    # -- formas
    def _elipsoide(self, pz):
        M = self.matriz(pz)
        r = np.broadcast_to(np.asarray(pz['p'].get('r', 5), float), (3,)).copy()
        c = M[:3, 3]
        A = self.v.P2 @ M[:3, :3] @ np.diag(r)
        c2 = self.v.pant(c)[0]
        camino, ejes = _elipse(c2, A)
        m = dict(camino=camino, prof=float(self.v.prof(c)[0]), r_ef=float(min(ejes)),
                 elipse=dict(c2=c2, A=A, M=M, r=r))
        m['calcas'] = self._calcas(pz, m)
        return [m]

    def _circulos(self, P, R):
        C = self.v.pant(P)
        return C, np.maximum(np.asarray(R, float), 0) * self.v.esc

    def _tubo_de(self, P, R, cerrado=False):
        C, Rp = self._circulos(P, R)
        if cerrado:
            C, Rp = np.vstack([C, C[:1]]), np.append(Rp, Rp[0])
        if len(C) == 1:
            return _camino(_circulo(C[0], Rp[0]))
        return _union([_camino(_casco2d(np.vstack([_circulo(C[i], Rp[i]), _circulo(C[i + 1], Rp[i + 1])])))
                       for i in range(len(C) - 1)])

    def _tubo(self, pz):
        p = pz['p']
        P, X, _ = self.puntos(pz, p['puntos'])
        if 'radios' in p:
            R = _perfil(p['radios'], len(P))
        else:
            R = np.array([x[0] if x else p.get('radio', 2.0) for x in X], float)
        cerrado = p.get('cerrado', False)
        if p.get('curva', True) and len(P) > 2:
            Q = _catmull(np.column_stack([P, R]), p.get('pasos', 6), cerrado)
            P, R = Q[:, :3], np.maximum(Q[:, 3], 0)
        if pz['fuera_de']:
            # solo se dibuja lo que asoma fuera de la capa
            Q = _catmull(np.column_stack([P, R]), 4) if len(P) > 1 else np.column_stack([P, R])
            P, R = Q[:, :3], Q[:, 3]
            fuera = ~self._dentro_de_campanas(pz['fuera_de'], P)
            if not fuera.any():
                return []
            i0 = max(int(np.argmax(fuera)) - 1, 0)
            P, R = P[i0:], R[i0:]
        camino = self._tubo_de(P, R, cerrado)
        m = dict(camino=camino, prof=float(np.mean(self.v.prof(P))), r_ef=float(np.mean(R) * self.v.esc))
        m['trazos'] = self._trazos(pz)
        return [m]

    def _esferas_y_discos(self, pz, esferas, discos):
        pts, profs = [], []
        if esferas:
            P, X, _ = self.puntos(pz, esferas)
            C, Rp = self._circulos(P, [x[0] if x else 0 for x in X])
            pts += [_circulo(c, r) for c, r in zip(C, Rp)]
            profs += list(self.v.prof(P))
        for dsc in discos or []:
            P, X, Rm = self.puntos(pz, [dsc[:-4] if isinstance(dsc[0], str) else dsc[:3]])
            r, n = dsc[-4], np.asarray(dsc[-3:], float)
            if pz['lado'] == 'd':
                n = n * REFLEJO
            n = Rm[0] @ n
            n /= np.linalg.norm(n)
            u = np.cross(n, [0, 1, 0] if abs(n[1]) < 0.9 else [1, 0, 0])
            u /= np.linalg.norm(u)
            w = np.cross(n, u)
            th = np.linspace(0, math.tau, 48, endpoint=False)[:, None]
            pts.append(self.v.pant(P[0] + r * (np.cos(th) * u + np.sin(th) * w)))
            profs.append(float(self.v.prof(P)[0]))
        H = _casco2d(np.vstack(pts))
        return dict(camino=_camino(H), prof=float(np.mean(profs)), r_ef=_radio_ef(H))

    def _casco(self, pz):
        p = pz['p']
        if pz['fuera_de'] and self._dentro_de_campanas(pz['fuera_de'], self.matriz(pz)[:3, 3])[0]:
            return []
        m = self._esferas_y_discos(pz, p.get('esferas'), p.get('discos'))
        m['trazos'] = self._trazos(pz)
        return [m]

    def _campana(self, pz):
        """Capa o falda acampanada: aros de arriba abajo ([y, rx, rz]); el último es el ruedo, que se ondula en
        `ondas` paños que cuelgan `caida` en su centro. Con `pliegues: true` dibuja un pliegue en cada entrada.

        `abertura` (grados) deja abierta la parte de adelante. Los paños de atrás se dibujan aparte, detrás del
        cuerpo (`capa_atras`) y con el material `reverso`: por la abertura se ve el forro, no la cara de afuera."""
        p = pz['p']
        G, G0, radios, ang = self.rejilla(pz)
        R, K, _ = G.shape
        n = K // 2
        M = self.matriz(pz)
        prof = float(self.v.prof(M[:3, 3])[0])
        miembros = []
        reverso = self.dib.materiales.get(p.get('reverso'))
        for i in range(n):
            if paño_abierto(p, ang, i):
                continue
            cols = [2 * i, 2 * i + 1, (2 * i + 2) % K]
            esf = [list(G[r, k]) + [radios[r, k]] for r in range(R) for k in cols]
            m = self._esferas_y_discos(pz, esf, None)
            m['prof'] = prof
            if p.get('abertura') or reverso:
                n_loc = G[-1, 2 * i + 1] * [1, 0, 1]
                n_loc = n_loc / max(np.linalg.norm(n_loc), 1e-9) * (REFLEJO if pz['lado'] == 'd' else 1)
                if float(self.v.de_frente(M[:3, :3] @ n_loc)[0]) < 0:
                    m['atras'] = True
                    if reverso:
                        m['mat'] = reverso
            miembros.append(m)
        rayas = self._arrugas(pz, G, G0, M) if G is not G0 else []
        if p.get('pliegues'):
            alto = p.get('alto_pliegue', 0.45)
            sub = int(p.get('subdividir', 1))
            for k in range(0, K, 2):
                ini, fin = G[-1, k], G[max(R - 1 - 2 * sub, 0), k]
                n_loc = ini * [1, 0, 1]
                n_loc = n_loc / max(np.linalg.norm(n_loc), 1e-9) * (REFLEJO if pz['lado'] == 'd' else 1)
                if float(self.v.de_frente(M[:3, :3] @ n_loc)[0]) < 0.15:
                    continue
                P3 = (ini + (fin - ini) * np.linspace(0, alto, 6)[:, None]) * [1.01, 1, 1.01]
                if pz['lado'] == 'd':
                    P3 = P3 * REFLEJO
                C = self.v.pant(P3 @ M[:3, :3].T + M[:3, 3])
                w = _perfil(p.get('ancho_pliegue', [0.7, 0.4, 0.0]), len(C)) * self.v.esc
                rayas.append(dict(camino=_camino(_tira2d(C, w)), tono='linea', opacidad=0.9))
        delante = [m for m in miembros if not m.get('atras')] or miembros
        delante[0]['trazos'] = rayas + self._trazos(pz, self.deformador(pz, G, G0))
        return miembros

    def _arrugas(self, pz, G, G0, M):
        """Arrugas donde la tela simulada quedó más corta que su diseño: si se aprieta de arriba abajo (un brazo
        que levanta el hombro) salen pliegues de lado a lado; si se aprieta de costado, pliegues verticales."""
        umbral = pz['p'].get('arrugas', 0.92)
        if not umbral:
            return []
        R, K, _ = G.shape
        salida = []

        def frente(P):
            n_loc = P * [1, 0, 1]
            n_loc = n_loc / max(np.linalg.norm(n_loc), 1e-9) * (REFLEJO if pz['lado'] == 'd' else 1)
            return float(self.v.de_frente(M[:3, :3] @ n_loc)[0])

        def trazo(P3, fuerza):
            P3 = P3 * [1.015, 1, 1.015]
            if pz['lado'] == 'd':
                P3 = P3 * REFLEJO
            C = self.v.pant(_catmull(P3 @ M[:3, :3].T + M[:3, 3], 6))
            ancho = min(1.0, 0.4 + 4 * fuerza) * self.v.esc
            salida.append(dict(camino=_camino(_tira2d(C, _perfil([0, ancho, ancho * 0.8, 0], len(C)))),
                               tono='linea', opacidad=min(1.0, 0.6 + 4 * fuerza)))

        for r in range(R - 1):
            for k in range(K):
                # apretada de arriba abajo: pliegue horizontal entre los aros r y r+1, alrededor de la columna k
                largo = np.linalg.norm(G[r + 1, k] - G[r, k])
                largo0 = np.linalg.norm(G0[r + 1, k] - G0[r, k])
                cociente = largo / max(largo0, 1e-6)
                if cociente < umbral:
                    medio = (G[r] + G[r + 1]) / 2
                    P3 = np.array([medio[(k - 1) % K], medio[k], medio[(k + 1) % K]])
                    if frente(P3[1]) > 0.1:
                        trazo(P3, umbral - cociente)
                # apretada de costado: pliegue vertical en la columna k
                if 0 < r:
                    ancho_ = np.linalg.norm(G[r, (k + 1) % K] - G[r, (k - 1) % K])
                    ancho0 = np.linalg.norm(G0[r, (k + 1) % K] - G0[r, (k - 1) % K])
                    cociente = ancho_ / max(ancho0, 1e-6)
                    if cociente < umbral:
                        P3 = np.array([G[r - 1, k] * 0.5 + G[r, k] * 0.5, G[r, k], G[r + 1, k] * 0.6 + G[r, k] * 0.4])
                        if frente(P3[1]) > 0.1:
                            trazo(P3, umbral - cociente)
        return salida

    def _caja(self, pz):
        w, h, d = (np.asarray(pz['p']['tam'], float) / 2)
        r = min(pz['p'].get('radio', 0.5), w, h, d)
        esf = [[sx * (w - r), sy * (h - r), sz * (d - r), r] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
        m = self._esferas_y_discos(pz, esf, None)
        m['trazos'] = self._trazos(pz)
        return [m]

    def _cilindro(self, pz):
        p = pz['p']
        a, b = np.asarray(p.get('a', [0, 0, 0]), float), np.asarray(p['b'], float)
        ra, rb = (p['r'], p['r']) if 'r' in p else (p['ra'], p['rb'])
        n = (b - a) / np.linalg.norm(b - a)
        m = self._esferas_y_discos(pz, None, [list(a) + [ra] + list(n), list(b) + [rb] + list(n)])
        m['trazos'] = self._trazos(pz)
        return [m]

    def _lamina(self, pz):
        M = self.matriz(pz)
        normal = M[:3, :3] @ np.array([0, 0, 1.0])
        frente = float(self.v.de_frente(normal)[0])
        if pz['p'].get('una_cara') and frente < 0.05:
            return []
        suma, resta, r_ef = [], [], 0.0
        for pts, signo in forma2d(pz['p']):
            P3 = np.column_stack([pts, np.zeros(len(pts))])
            if pz['lado'] == 'd':
                P3 = P3 * REFLEJO
            Q = self.v.pant(P3 @ M[:3, :3].T + M[:3, 3])
            (suma if signo > 0 else resta).append(_camino(Q))
            if signo > 0:
                r_ef = max(r_ef, _radio_ef(Q))
        camino = _restar(_union(suma), resta)
        m = dict(camino=camino, prof=float(self.v.prof(M[:3, 3])[0]), r_ef=r_ef, frente=frente)
        if frente < 0 and pz['p'].get('reverso'):
            m['mat'] = self.dib.materiales[pz['p']['reverso']]
        m['trazos'] = self._trazos(pz)
        return [m]

    def _cinta(self, pz):
        """Listón plano de ancho fijo que sigue una curva; muestra su revés cuando se tuerce."""
        p = pz['p']
        P, X, Rm = self.puntos(pz, p['puntos'])
        eje = np.asarray(p.get('normal', [0, 0, 1]), float)
        if pz['lado'] == 'd':
            eje = eje * REFLEJO
        N = np.array([R @ eje for R in Rm])
        W = _perfil(p.get('anchos', p.get('ancho', 4.0)), len(P))
        Q = _catmull(np.column_stack([P, N, W]), p.get('pasos', 6)) if len(P) > 2 else np.column_stack([P, N, W])
        P, N, W = Q[:, :3], Q[:, 3:6], Q[:, 6]
        N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)
        T = np.gradient(P, axis=0)
        T /= np.maximum(np.linalg.norm(T, axis=1, keepdims=True), 1e-9)
        B = np.cross(T, N)
        B /= np.maximum(np.linalg.norm(B, axis=1, keepdims=True), 1e-9)
        E1 = self.v.pant(P + B * (W / 2)[:, None])
        E2 = self.v.pant(P - B * (W / 2)[:, None])
        frente = self.v.de_frente(N)
        cuadros, reves = [], []
        for i in range(len(P) - 1):
            q = _camino(np.array([E1[i], E1[i + 1], E2[i + 1], E2[i]]))
            cuadros.append(q)
            if frente[i] + frente[i + 1] < 0:
                reves.append(q)
        if p.get('cola') == 'v':
            fin = self.v.pant(P[-1] - T[-1] * W[-1] * 0.7)[0]
            cuadros.append(_camino(np.array([E1[-1], E2[-1], fin])))
            muesca = _camino(np.array([E1[-1], fin, E2[-1], self.v.pant(P[-1] + T[-1] * W[-1])[0]]))
            camino = _op(_union(cuadros), muesca, RESTA)
        else:
            camino = _union(cuadros)
        m = dict(camino=camino, prof=float(np.mean(self.v.prof(P))), r_ef=float(np.mean(W) * self.v.esc / 2))
        if reves and p.get('reverso'):
            m['reves'] = (_op(_union(reves), camino, CRUCE), self.dib.materiales[p['reverso']])
        m['trazos'] = self._trazos(pz)
        return [m]

    def _mechones(self, pz):
        """Mechones de pelo: tubos afilados que nacen sobre un elipsoide (`sobre`) y lo siguen o salen de él."""
        p = pz['p']
        M = self.matriz(pz)
        r = np.asarray(p['sobre'], float)
        espejo = -1.0 if pz['lado'] == 'd' else 1.0
        miembros, rayas = [], []
        for mc in p['lista']:
            x, y = mc['en']
            giro = list(mc.get('giro', [0, 0]))
            giro[0] *= espejo
            largo = mc.get('largo', 8)
            if 'dir' in mc:
                B, N = sobre_elipsoide([[x * espejo, y]], r, giro)
                D = np.asarray(mc['dir'], float) * [espejo, 1, 1]
                D /= np.linalg.norm(D)
                dob = np.asarray(mc.get('doblez', [0, 0, 0]), float) * [espejo, 1, 1]
                N_raiz = N[0]
                B0 = B[0] - N[0] * 0.8
                ctrl = [B0, B0 + D * largo * 0.5 + dob * largo * 0.25, B0 + D * largo + dob * largo * 0.6]
                L = _catmull(np.array(ctrl), 6)
            else:
                ang0 = math.radians(mc.get('hacia', -90))
                curva = math.radians(mc.get('curva', 0))
                n = 9
                s = np.linspace(0, 1, n)
                ang = ang0 + curva * s
                paso = largo / (n - 1)
                xy = np.cumsum(np.stack([np.cos(ang), np.sin(ang)], 1) * paso, 0) - [math.cos(ang0) * paso,
                                                                                      math.sin(ang0) * paso]
                xy = xy + [x, y]
                xy[:, 0] *= espejo
                alza = _perfil(mc.get('alza', [0.4, 1.2]), n)
                L, Ns = sobre_elipsoide(xy, r, giro, alza)
                N_raiz = Ns[0]
            Pw = L @ M[:3, :3].T + M[:3, 3]
            ancho = mc.get('ancho', 2.5)
            R = _perfil(mc.get('perfil', [1.0, 0.9, 0.0]), len(Pw)) * ancho
            camino = self._tubo_de(Pw, R)
            # Un mechón que nace del lado oculto de la cabeza se dibuja detrás de ella
            atras = float(self.v.de_frente(M[:3, :3] @ N_raiz)[0]) < -0.02
            miembros.append(dict(camino=camino, prof=float(np.mean(self.v.prof(Pw))),
                                 r_ef=float(np.mean(R) * self.v.esc), atras=atras))
            if mc.get('raya', p.get('rayas', False)) and not atras:
                C = self.v.pant(Pw)
                k = len(C)
                seg = C[int(k * 0.15):int(k * 0.85)]
                if len(seg) > 2:
                    lado = np.asarray(mc.get('lado_raya', 0.25))
                    d = np.gradient(seg, axis=0)
                    d /= np.maximum(np.hypot(d[:, 0], d[:, 1]), 1e-9)[:, None]
                    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
                    seg = seg + nrm * (R[int(k * 0.15):int(k * 0.85)] * self.v.esc * lado)[:, None]
                    rayas.append(dict(camino=_camino(_tira2d(seg, _perfil([0.0, 1.0, 0.0], len(seg))
                                                                   * self.dib.grosor * self.v.esc * 0.8)),
                                      tono='hondo', opacidad=1.0))
        if miembros:
            miembros[0]['trazos'] = rayas + self._trazos(pz)
        return miembros

    # -- calcas sobre elipsoides y trazos interiores
    def _calcas(self, pz, m):
        e = m['elipse']
        # Dirección "hacia la cámara" en el espacio de la esfera unitaria: U·w > 0 es el lado visible
        w = (e['M'][:3, :3].T @ self.v.V.T @ np.array([0, 0, 1.0])) / e['r']
        w /= np.linalg.norm(w)
        salida = []
        for c in pz['calcas']:
            if 'caras' in c and self.cara not in c['caras']:
                continue
            if self.cara in c.get('sin_caras', []):
                continue
            lados = (1.0, -1.0) if c.get('espejo') else (1.0,)
            for sx in lados:
                if pz['lado'] == 'd':
                    sx = -sx
                giro = list(c.get('giro', [0, 0]))
                giro[0] *= sx
                G = (rot([0, giro[0], 0]) @ rot([-(giro[1] if len(giro) > 1 else 0), 0, 0]))[:3, :3]
                vis = _region_visible(G.T @ w)
                if vis is None:
                    continue
                K = 1000.0
                vis_c = _camino(vis * K)
                caminos = []
                for pts, signo in forma2d(c):
                    # La calca se recorta en su propio plano contra la parte visible y recién después se
                    # pega sobre la pieza: así el borde que queda en el horizonte coincide con la silueta.
                    norm = pts * [sx, 1] / e['r'][:2]
                    corte = _op(_camino(norm * K), vis_c, CRUCE)
                    for cont in _contornos(corte):
                        q = _densificar(cont / K, 0.02)
                        U0 = np.column_stack([q, np.sqrt(np.maximum(0, 1 - (q ** 2).sum(1)))])
                        Pw = ((U0 @ G.T) * e['r']) @ e['M'][:3, :3].T + e['M'][:3, 3]
                        caminos.append((_camino(self.v.pant(Pw)), signo))
                if not any(s_ > 0 for _, s_ in caminos):
                    continue
                camino = _restar(_union([q for q, s in caminos if s > 0]), [q for q, s in caminos if s < 0])
                camino = _op(camino, m['camino'], CRUCE)
                mat = self.dib.materiales.get(c.get('material'))
                salida.append(dict(camino=camino, op=c.get('op', 'pintar'),
                                   color=c.get('color', mat.color if mat else self.dib.tinta),
                                   opacidad=c.get('opacidad', 1.0), blur=c.get('blur', 0.0) * self.v.esc,
                                   brillo=c.get('brillo', False), linea=c.get('linea', False)))
        return salida

    def _trazos(self, pz, deformar=None):
        salida = []
        for t in pz['trazos']:
            P, X, Rm = self.puntos(pz, t['puntos'])
            if deformar is not None:
                P = deformar(P)
            if 'normal' in t:
                n = np.asarray(t['normal'], float) * (REFLEJO if pz['lado'] == 'd' else 1)
                fr = float(self.v.de_frente(Rm[0] @ n)[0])
                if fr < t.get('min_frente', 0.1):
                    continue
            if len(P) > 2 and t.get('suave', True):
                P = _catmull(P, 8)
            elif len(P) == 2:
                P = _catmull(P, 10)
            C = self.v.pant(P)
            w = _perfil(t.get('anchos', t.get('ancho', 0.5)), len(C)) * self.v.esc
            if 'guiones' in t:
                # costura: guiones de largo a con huecos de largo b (en unidades del modelo)
                a, b = (np.asarray(t['guiones'], float) * self.v.esc)
                C = _catmull(C, 4) if len(C) > 2 else C
                w = _perfil(w, len(C))
                s_ = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(C, axis=0).T))])
                dentro = (s_ % (a + b)) < a
                camino = skia.Path()
                i = 0
                while i < len(C):
                    if dentro[i]:
                        j = i
                        while j + 1 < len(C) and dentro[j + 1]:
                            j += 1
                        if j > i:
                            camino.addPath(_camino(_tira2d(C[i:j + 1], w[i:j + 1])))
                        i = j + 1
                    else:
                        i += 1
            else:
                camino = _camino(_tira2d(C, w))
            salida.append(dict(camino=camino, tono=t.get('tono', 'linea'), opacidad=t.get('opacidad', 1.0)))
        return salida


# ---------------------------------------------------------------------------- dibujo
class Cuadro:
    pass


def _armar(dib, yaw, pitch, anim, cuadro, pose, zoom, cara):
    yaw = dib.camara['yaw'] if yaw is None else yaw
    pitch = dib.camara['pitch'] if pitch is None else pitch
    W = dib.esqueleto_de(anim, cuadro, pose)
    estado = dib.estado_fisica(anim, cuadro, pose)
    telas = dib.fisica.aplicar(W, estado) if estado is not None else {}
    cara = cara or dib.cara_de(anim, cuadro)
    vista = Vista(dib, yaw, pitch, zoom)
    pr = _Proyector(dib, W, vista, cara)
    pr.telas = telas

    grupos, hijos = {}, []
    for pz in dib.piezas:
        ms = pr.proyectar(pz)
        for m in ms:
            for c in m.get('calcas', []):
                if c['op'] == 'resta':
                    # engordado apenas, para no dejar astillas de un pixel junto al borde de la silueta
                    m['camino'] = _op(m['camino'], _engordar(c['camino'], 1.5), RESTA)
        if pz['dentro_de']:
            hijos += ms
        elif ms:
            grupos.setdefault(pz['grupo'], []).extend(ms)

    def item(nombre, ms, prof=None):
        suma = [m['camino'] for m in ms if m['pieza']['op'] != 'resta']
        camino = _union(suma)
        for m in ms:
            if m['pieza']['op'] == 'resta':
                camino = _op(camino, m['camino'], RESTA)
        principal = max((m for m in ms if m['pieza']['op'] != 'resta'), key=lambda m: m['r_ef'], default=ms[0])
        pz = principal['pieza']
        return dict(nombre=nombre, camino=camino, prof=principal['prof'] + pz['capa'] if prof is None else prof,
                    mat=principal.get('mat', pz['mat']), miembros=[m for m in ms if m['pieza']['op'] != 'resta'],
                    linea=pz['linea'], grosor=pz['grosor'], proyecta=pz['proyecta'], recibe=pz['recibe'],
                    silueta=pz['silueta'], hijos=[], debajo_de=pz['debajo_de'], encima_de=pz['encima_de'],
                    calcas=[c for m in ms for c in m.get('calcas', []) if c['op'] != 'resta'],
                    trazos=[t for m in ms for t in m.get('trazos', [])],
                    reves=[m['reves'] for m in ms if 'reves' in m])

    items, por_pieza = [], {}
    for g, ms in grupos.items():
        delante = [m for m in ms if not m.get('atras')]
        atras = [m for m in ms if m.get('atras')]
        it = item(g, delante or atras)
        items.append(it)
        if delante and atras:
            principal = max(delante, key=lambda m: m['r_ef'])
            items.append(item(g + '_atras', atras, prof=principal['prof'] + atras[0]['pieza']['p'].get('capa_atras', -2.0)))
        for m in ms:
            por_pieza.setdefault(m['pieza']['nombre'], it)
    for h in hijos:
        padre = por_pieza.get(h['pieza']['dentro_de'])
        if padre is None:
            raise ValueError(f'Pieza "{h["pieza"]["nombre"]}": dentro_de "{h["pieza"]["dentro_de"]}" no existe o no se ve.')
        padre['hijos'].append(h)
    for it in items:
        it['hijos'].sort(key=lambda h: h['prof'] + h['pieza']['capa'])
    items.sort(key=lambda it: it['prof'])
    _ordenar_por_reglas(items)
    return items, vista, cara


def _ordenar_por_reglas(items):
    """Respeta `debajo_de` y `encima_de` de las piezas por encima de la profundidad (la parte de arriba de un
    brazo va siempre bajo el manto que la cubre, aunque el brazo esté adelante)."""
    for _ in range(4):
        cambio = False
        for it in list(items):
            for regla, arriba in (('debajo_de', False), ('encima_de', True)):
                for otro in it[regla]:
                    nombres = [x['nombre'] for x in items]
                    if otro not in nombres:
                        continue
                    i, j = nombres.index(it['nombre']), nombres.index(otro)
                    if (not arriba and i > j) or (arriba and i < j):
                        items.remove(it)
                        j = [x['nombre'] for x in items].index(otro)
                        items.insert(j + 1 if arriba else j, it)
                        cambio = True
        if not cambio:
            break


def _pintar_item(cv, it, cerca, vista, dib):
    P, m = it['camino'], it['mat']
    l2, f = vista.luz2, vista.fuerza
    w = dib.grosor * vista.esc * it['grosor']
    extra = dib.peso_sombra if m.opacidad >= 1 else 0
    if it['linea'] and not dib.linea_encima:
        _tinta(cv, P, w, l2, extra, _pintura(m.linea))
    cv.drawPath(P, _pintura(m.color, m.opacidad))
    cv.save()
    cv.clipPath(P, skia.ClipOp.kIntersect, True)
    for camino, mat in it['reves']:
        cv.drawPath(camino, _pintura(mat.color))
    for h in it['hijos']:
        hm = h.get('mat', h['pieza']['mat'])
        cv.drawPath(h['camino'], _pintura(hm.color, hm.opacidad))
        if h['pieza']['linea']:
            cv.drawPath(_contorno_de(h['camino'], w * (1.0 if dib.linea_encima else 0.7) * h['pieza']['grosor']),
                        _pintura(hm.linea))
        for t in h.get('trazos', []):
            cv.drawPath(t['camino'], _pintura(hm.tono(t['tono']), t['opacidad']))
    for c in it['calcas']:
        if not c['brillo']:
            cv.drawPath(c['camino'], _pintura(c['color'], c['opacidad'], c['blur']))
            if c['linea']:
                cv.drawPath(_contorno_de(c['camino'], w * 0.5), _pintura(dib.tinta, 0.8))
    if not m.sin_sombra:
        blur = m.suave * vista.esc * 0.5
        cv.saveLayer(None, skia.Paint(BlendMode=skia.BlendMode.kMultiply))
        ps = _pintura(m.multiplica, 1.0, blur)
        for mb in it['miembros']:
            # La media luna de cada parte se resta contra toda la forma corrida hacia la luz: un mechón que
            # descansa sobre el casquete solo se oscurece donde forma el borde de sombra del conjunto.
            d = m.ancho_sombra * mb['r_ef'] * f
            cv.drawPath(_op(_engordar(mb['camino'], blur * 3 + 1), _mover(P, l2 * d), RESTA), ps)
        if it['recibe'] and cerca is not None and not cerca.isEmpty():
            cv.drawPath(_mover(cerca, -l2 * dib.proyectada * vista.esc), ps)
        cv.restore()
        if m.borde_suave:
            ancho, fuerza = m.borde_suave
            pb = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=float(ancho * vista.esc * 2))
            pb.setColor4f(_c4(m.multiplica, fuerza))
            pb.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, float(ancho * vista.esc * 0.6)))
            pb.setBlendMode(skia.BlendMode.kMultiply)
            cv.drawPath(P, pb)
        if m.brillo > 0:
            pl = _pintura(m.luz, m.brillo, blur)
            for mb in it['miembros']:
                d = m.ancho_luz * mb['r_ef'] * f
                cv.drawPath(_op(mb['camino'], _mover(P, -l2 * d), RESTA), pl)
    for t in it['trazos']:
        cv.drawPath(t['camino'], _pintura(m.tono(t['tono']), t['opacidad']))
    for c in it['calcas']:
        if c['brillo']:
            cv.drawPath(c['camino'], _pintura(c['color'], c['opacidad'], c['blur']))
    cv.restore()
    if it['linea'] and dib.linea_encima:
        _tinta(cv, P, w, l2, extra, _pintura(m.linea))


def dibujar(dib, yaw=None, pitch=None, anim=None, cuadro=0, pose=None, zoom=1.0, cara=None, fondo=None):
    """Dibuja un cuadro. Devuelve un objeto con `rgba` (alto × ancho × 4, uint8) e información de las piezas."""
    items, vista, cara = _armar(dib, yaw, pitch, anim, cuadro, pose, zoom, cara)
    ancho, alto = vista.tam
    sup = skia.Surface(ancho, alto)
    cv = sup.getCanvas()
    cv.clear(_c4(fondo) if fondo else skia.Color4f(0, 0, 0, 0))
    l2 = vista.luz2

    silueta = _union([it['camino'] for it in items if it['silueta']])
    ws = dib.grosor_silueta * vista.esc
    if ws > 0:
        _tinta(cv, silueta, ws, l2, 0.5, _pintura(dib.tinta))

    cerca, acc = [None] * len(items), skia.Path()
    for i in reversed(range(len(items))):
        cerca[i] = acc
        if items[i]['proyecta']:
            acc = _union([acc, items[i]['camino']])
    for it, c in zip(items, cerca):
        _pintar_item(cv, it, c, vista, dib)

    if dib.degradado:
        b = silueta.getBounds()
        g = skia.GradientShader.MakeLinear([skia.Point(0, b.top()), skia.Point(0, b.bottom())],
                                           [_c4(dib.degradado[0]).toColor(), _c4(dib.degradado[1]).toColor()])
        p = skia.Paint(AntiAlias=True, Shader=g, BlendMode=skia.BlendMode.kMultiply)
        cv.save()
        cv.clipPath(silueta, skia.ClipOp.kIntersect, True)
        cv.drawRect(b.makeOutset(ws * 2, ws * 2), p)
        cv.restore()

    if dib.grano:
        rng = np.random.default_rng(11)
        g = rng.random((alto, ancho))
        g = (g + np.roll(g, 1, 0) + np.roll(g, 1, 1) + np.roll(np.roll(g, 1, 0), 1, 1)) / 4
        v = (255 * (1 - dib.grano * g)).astype(np.uint8)
        textura = skia.Image.fromarray(np.dstack([v, v, v, np.full_like(v, 255)]))
        zona = skia.Path()
        for it in items:
            zona = _op(zona, it['camino'], RESTA if it['mat'].sin_grano else UNION)
        cv.save()
        cv.clipPath(zona, skia.ClipOp.kIntersect, True)
        cv.drawImage(textura, 0, 0, skia.SamplingOptions(), skia.Paint(BlendMode=skia.BlendMode.kMultiply))
        cv.restore()

    if dib.contraluz:
        # luz de contorno: una línea clara del lado de la sombra, por dentro de la silueta
        col, ancho, alfa = dib.contraluz
        borde = _op(silueta, _mover(silueta, l2 * ancho * vista.esc), RESTA)
        cv.save()
        cv.clipPath(silueta, skia.ClipOp.kIntersect, True)
        cv.drawPath(_mover(borde, -l2 * ws * 0.35),
                    _pintura(col, alfa, ancho * vista.esc * 0.25, skia.BlendMode.kScreen))
        cv.restore()

    auras = [it for it in items if it['mat'].aura]
    for it in auras:
        col, radio, alfa = it['mat'].aura
        cv.drawPath(it['camino'], _pintura(col, alfa, radio * vista.esc, skia.BlendMode.kScreen))

    img = sup.makeImageSnapshot()
    r = Cuadro()
    r.rgba = img.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType)
    r.items, r.vista, r.cara, r.silueta = items, vista, cara, silueta
    return r


def que_hay(cuadro, x, y):
    """Las piezas que cubren el pixel (x, y), de la de adelante a la de atrás, con lo que tienen pegado."""
    salida = []
    for it in reversed(cuadro.items):
        if not it['camino'].contains(float(x), float(y)):
            continue
        partes = [m['pieza']['nombre'] for m in it['miembros'] if m['camino'].contains(float(x), float(y))]
        hijos = [h['pieza']['nombre'] for h in it['hijos'] if h['camino'].contains(float(x), float(y))]
        salida.append(dict(item=it['nombre'], prof=round(it['prof'], 1), partes=partes, hijos=hijos))
    return salida
