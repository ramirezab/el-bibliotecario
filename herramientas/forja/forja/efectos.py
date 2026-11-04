"""Efectos de combate cuadro a cuadro en pixel art ("tinta que se vuelve luz", biblia de VFX).

Cada capa calcula un campo de energía 0..1 sobre el lienzo para la fase t (0..1) y lo convierte en
colores de su paleta (de oscuro a brillante) con tramado ordenado en los bordes. Las capas se
apilan en orden. Además de los cuadros, se exporta una máscara de brillo: los pixeles en los dos
tonos más altos de una paleta marcada como `emisiva`, para que el motor les ponga resplandor.

Capas: arco (tajo en media luna), trazo (caligrafía que se dibuja y se enciende), anillo, estrella,
particulas, gota (proyectil con estela) y disco (destello).
"""
import math

import numpy as np
import yaml

from . import color
from .render import BAYER4

PALETAS = {
    'tinta': ['#0e1030', '#1c2058', '#2b3170', '#4a52b8', '#8a93f0'],
    'oro': ['#7a4e12', '#a8741f', '#e8b04b', '#ffd98a', '#fff6dc'],
    'brasa': ['#5a0e10', '#a8231f', '#ff5a1f', '#ffb000', '#fff4d6'],
    'luna': ['#3a4466', '#5e6a8a', '#c9d6e8', '#eef3fa', '#ffffff'],
    'papel': ['#8a7a5a', '#d9c9a8', '#f2e8d5', '#fffaf0'],
    'savia': ['#3a2208', '#8c5a1e', '#f2a93b', '#ffd27a', '#fff1c9'],
    'podre': ['#120a12', '#3a1f3d', '#5b2a6e', '#9db83a', '#d4e05a'],
}


def _vent(t, a, b):
    return float(np.clip((t - a) / max(b - a, 1e-9), 0, 1))


def _sale(x):
    return 1 - (1 - x) ** 3


def _entra(x):
    return x ** 2


def _hash(X, Y, s=0):
    n = (X.astype(np.int64) * 73856093) ^ (Y.astype(np.int64) * 19349663) ^ (s * 83492791)
    n = (n ^ (n >> 13)) * 1274126177
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def _paleta(p):
    return PALETAS[p] if isinstance(p, str) else list(p)


def _bezier(ctrl, n=240):
    P = np.asarray(ctrl, float)
    u = np.linspace(0, 1, n)[:, None]
    if len(P) == 4:
        return ((1 - u) ** 3) * P[0] + 3 * ((1 - u) ** 2) * u * P[1] + 3 * (1 - u) * u * u * P[2] + u ** 3 * P[3]
    seg = np.linspace(0, len(P) - 1, n)
    i = np.minimum(np.floor(seg).astype(int), len(P) - 2)
    f = (seg - i)[:, None]
    return P[i] * (1 - f) + P[i + 1] * f


# ------------------------------------------------------------------ capas

def arco(c, t, X, Y):
    cx, cy = c['centro']
    R, g = c['radio'], c['grosor']
    a0, a1 = math.radians(c['desde']), math.radians(c['hasta'])
    s = _sale(_vent(t, *c.get('barrido', [0, 0.35])))
    f = 1 - _vent(t, *c.get('desvanecer', [0.45, 1.0]))
    if s <= 0 or f <= 0:
        return np.zeros(X.shape)
    cabeza = a0 + (a1 - a0) * s
    sentido = 1 if a1 >= a0 else -1
    cola = math.radians(c.get('cola', 150)) * (0.35 + 0.65 * s)
    dx, dy = X - cx, Y - cy
    r = np.hypot(dx, dy)
    ang = np.arctan2(dy, dx)
    atras = np.mod((cabeza - ang) * sentido, 2 * math.pi)
    u = atras / cola
    grosor = g * np.clip(1 - u, 0, 1) ** 0.7 * (0.35 + 0.65 * f)
    # Media luna: el borde exterior sigue el radio, el interior se come hacia adentro
    radio_medio = R - grosor * 0.35
    e = 1 - np.abs(r - radio_medio) / np.maximum(grosor / 2, 1e-6)
    e = np.clip(e, 0, 1) * (u <= 1) * (1 - 0.55 * np.clip(u, 0, 1)) * (0.4 + 0.6 * f)
    return e


def anillo(c, t, X, Y):
    k = _vent(t, *c.get('ventana', [0, 0.5]))
    if k <= 0 or k >= 1:
        return np.zeros(X.shape)
    cx, cy = c['centro']
    R = c.get('r0', 2) + (c['r1'] - c.get('r0', 2)) * _sale(k)
    g = c.get('grosor', 5) * (1 - k) + 1
    r = np.hypot(X - cx, Y - cy)
    return np.clip(1 - np.abs(r - R) / (g / 2), 0, 1) * (1 - k * 0.7)


def estrella(c, t, X, Y):
    k = _vent(t, *c.get('ventana', [0, 0.35]))
    if k <= 0 or k >= 1:
        return np.zeros(X.shape)
    cx, cy = c['centro']
    tam = c['radio'] * math.sin(math.pi * k) ** 0.6
    n = c.get('puntas', 4)
    rot = math.radians(c.get('giro', 0)) + k * math.radians(c.get('gira', 0))
    dx, dy = X - cx, Y - cy
    r = np.hypot(dx, dy)
    ang = np.arctan2(dy, dx) - rot
    punta = np.abs(np.cos(ang * n / 2)) ** c.get('agudeza', 18)
    limite = tam * (c.get('nucleo', 0.22) + (1 - c.get('nucleo', 0.22)) * punta)
    return np.clip(1 - r / np.maximum(limite, 1e-6), 0, 1)


def disco(c, t, X, Y):
    k = _vent(t, *c.get('ventana', [0, 0.2]))
    if k <= 0 or k >= 1:
        return np.zeros(X.shape)
    cx, cy = c['centro']
    R = c['radio'] * (0.6 + 0.4 * _sale(k))
    r = np.hypot(X - cx, Y - cy)
    return np.clip(1 - r / R, 0, 1) ** 0.7 * (1 - k)


def particulas(c, t, X, Y):
    H, W = X.shape
    E = np.zeros((H, W))
    rng = np.random.default_rng(c.get('semilla', 1))
    n = c.get('cantidad', 20)
    ox, oy = c['origen']
    disp = c.get('dispersion', 0)
    a_min, a_max = [math.radians(v) for v in c.get('angulo', [0, 360])]
    v_min, v_max = c.get('velocidad', [30, 80])
    t0, t1 = c.get('inicio', [0.0, 0.1])
    l_min, l_max = c.get('vida', [0.3, 0.6])
    grav = c.get('gravedad', 0)
    roce = c.get('roce', 1.5)
    for _ in range(n):
        ts = rng.uniform(t0, t1)
        vida = rng.uniform(l_min, l_max)
        ang = rng.uniform(a_min, a_max)
        vel = rng.uniform(v_min, v_max)
        px, py = ox + rng.uniform(-disp, disp), oy + rng.uniform(-disp, disp)
        if not ts <= t <= ts + vida:
            continue
        a = (t - ts) / vida
        dt = t - ts
        avance = (1 - math.exp(-roce * dt)) / roce if roce else dt
        x = px + math.cos(ang) * vel * avance
        y = py + math.sin(ang) * vel * avance + 0.5 * grav * dt * dt
        e = (1 - a) ** c.get('curva', 1.0)
        tam = 2 if e > c.get('umbral_grande', 0.65) else 1
        xi, yi = int(round(x)), int(round(y))
        for ddx in range(tam):
            for ddy in range(tam):
                if 0 <= xi + ddx < W and 0 <= yi + ddy < H:
                    E[yi + ddy, xi + ddx] = max(E[yi + ddy, xi + ddx], e)
        if c.get('estela'):
            dt2 = max(dt - c['estela'], 0)
            av2 = (1 - math.exp(-roce * dt2)) / roce if roce else dt2
            x2 = px + math.cos(ang) * vel * av2
            y2 = py + math.sin(ang) * vel * av2 + 0.5 * grav * dt2 * dt2
            for k in np.linspace(0, 1, 8):
                xx, yy = int(round(x2 + (x - x2) * k)), int(round(y2 + (y - y2) * k))
                if 0 <= xx < W and 0 <= yy < H:
                    E[yy, xx] = max(E[yy, xx], e * (0.35 + 0.5 * k))
    return E


def gota(c, t, X, Y):
    k = _vent(t, *c.get('ventana', [0, 0.6]))
    if k <= 0 or k >= 1:
        return np.zeros(X.shape)
    curva = _bezier(c['camino'], 120)
    i = int(_entra(k) * (len(curva) - 1)) if c.get('acelera', True) else int(k * (len(curva) - 1))
    E = np.zeros(X.shape)
    largo = c.get('estela', 30)
    for j in range(max(0, i - largo), i + 1):
        px, py = curva[j]
        u = (i - j) / max(largo, 1)
        rad = c.get('radio', 4) * (1 - u) ** 0.8
        r = np.hypot(X - px, Y - py)
        E = np.maximum(E, np.clip(1 - r / max(rad, 0.6), 0, 1) * (1 - 0.6 * u))
    return E


def trazo(c, t, X, Y):
    """Trazo caligráfico: se dibuja (tinta), se enciende de un extremo al otro (oro) y se deshace."""
    pts = _bezier(c['puntos'], 220)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    s = seg / seg[-1]
    p = _sale(_vent(t, *c.get('dibujo', [0, 0.35])))
    g = _vent(t, *c.get('ignicion', [0.35, 0.6]))
    v = _vent(t, *c.get('desvanecer', [0.65, 1.0]))
    gro = c.get('grosor', 6) * np.sin(np.pi * np.clip(s, 0.02, 0.98)) ** c.get('presion', 0.6)
    d = np.full(X.shape, 1e9)
    s_cerca = np.zeros(X.shape)
    w_cerca = np.ones(X.shape)
    for j in range(0, len(pts), 2):
        if s[j] > p:
            break
        dj = np.hypot(X - pts[j, 0], Y - pts[j, 1]) / max(gro[j] / 2, 0.5)
        m = dj < d
        d = np.where(m, dj, d)
        s_cerca = np.where(m, s[j], s_cerca)
        w_cerca = np.where(m, gro[j], w_cerca)
    e = np.clip(1 - d, 0, 1) * (1 - 0.6 * v)
    if v > 0:
        e = e * (_hash(X, Y, 5) > v)
    tinta = np.where(s_cerca >= g, e, 0)
    oro = np.where(s_cerca < g, np.clip(e + 0.25, 0, 1) * (e > 0), 0)
    frente = (np.abs(s_cerca - g) < 0.04) & (e > 0) & (g > 0) & (g < 1)
    oro = np.where(frente, 1.0, oro)
    return tinta, oro


CAPAS = {'arco': arco, 'anillo': anillo, 'estrella': estrella, 'disco': disco,
         'particulas': particulas, 'gota': gota}


def _pintar(rgba, brillo, E, pal, umbral, tramado, emisiva, X, Y, disolver_k=0.0, semilla=0):
    if disolver_k > 0:
        E = E * (_hash(X, Y, semilla) > disolver_k)
    cols = np.array([color.hex_a_rgb(c) for c in pal], np.uint8)
    n = len(cols)
    b = (BAYER4[Y % 4, X % 4] - 0.5) * tramado
    u = (E - umbral) / (1 - umbral)
    idx = np.floor(u * n + b).astype(int)
    m = (E > umbral) & (u * n + b >= 0)
    idx = np.clip(idx, 0, n - 1)
    rgba[m, :3] = cols[idx[m]]
    rgba[m, 3] = 255
    if emisiva:
        brillo[m & (idx >= n - 2)] = True
        brillo[m & (idx < n - 2)] = False
    else:
        brillo[m] = False


def renderizar_efecto(spec, t):
    W, H = spec['lienzo']
    Y, X = np.mgrid[0:H, 0:W]
    Xf, Yf = X + 0.5, Y + 0.5
    rgba = np.zeros((H, W, 4), np.uint8)
    brillo = np.zeros((H, W), bool)
    for c in spec['capas']:
        tipo = c['tipo']
        umbral, tramado = c.get('umbral', 0.08), c.get('tramado', 1.0)
        dk = _vent(t, *c['disolver']) if 'disolver' in c else 0.0
        if tipo == 'trazo':
            tinta, oro = trazo(c, t, Xf, Yf)
            _pintar(rgba, brillo, tinta, _paleta(c.get('paleta', 'tinta')), umbral, tramado, False, X, Y)
            _pintar(rgba, brillo, oro, _paleta(c.get('paleta_luz', 'oro')), umbral, tramado, True, X, Y)
        else:
            E = CAPAS[tipo](c, t, Xf, Yf)
            _pintar(rgba, brillo, E, _paleta(c.get('paleta', 'oro')), umbral, tramado, c.get('emisiva', True), X, Y,
                    dk, c.get('semilla', 0))
    if spec.get('contorno'):
        op = rgba[..., 3] > 0
        pd = np.pad(op, 1)
        borde = ~op & (pd[:-2, 1:-1] | pd[2:, 1:-1] | pd[1:-1, :-2] | pd[1:-1, 2:])
        rgba[borde, :3] = color.hex_a_rgb(spec['contorno']).astype(np.uint8)
        rgba[borde, 3] = 255
    return rgba, brillo


def cargar(ruta):
    with open(ruta, encoding='utf-8') as f:
        return yaml.safe_load(f)


def cuadros(spec):
    n = spec.get('cuadros', 10)
    salida = []
    for i in range(n):
        t = i / max(n - 1, 1)
        salida.append(renderizar_efecto(spec, t))
    return salida
