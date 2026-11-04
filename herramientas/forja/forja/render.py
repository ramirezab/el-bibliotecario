"""Render: traza rayos sobre la escena SDF y convierte el resultado en pixel art.

Pasos: trazado ortográfico a tamaño final, sin suavizado -> normales -> luz por pasos de rampa
(sombreado tipo cel, oclusión, sombras proyectadas, brillo especular, luz de borde) -> limpieza de
pixeles sueltos -> líneas interiores entre piezas -> contorno exterior -> calcas -> retoques a mano.
"""
import numpy as np

from . import color
from .modelo import rot
from .sdf import ruido3, smin, smax

BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
ZC = 2000.0
# Códigos del mapa de tipos de pixel
FONDO, RELLENO, CONTORNO, LINEA, CALCA, RETOQUE, BRILLO = range(7)


def _dist_pieza(p, P, corte):
    """Distancia a una pieza. Lejos de su esfera envolvente devuelve la cota inferior (más barata)."""
    cota = np.linalg.norm(P - p['centro'], axis=1) - p['radio']
    m = cota < corte
    if m.any():
        Pl = P[m] @ p['inv'][:3, :3].T + p['inv'][:3, 3]
        d = p['fdist'](Pl, p['params'])
        rug = p['params'].get('rugosidad')
        if rug:
            d = d + (ruido3(Pl, rug.get('escala', 3), rug.get('semilla', 0), rug.get('octavas', 2)) - 0.5) * 2 * rug['fuerza']
        cota[m] = d
    return cota


def dist_escena(piezas, grupos, P, corte=2.0):
    total = np.full(len(P), np.inf)
    for g in grupos:
        dg, k = None, g['suave']
        for i in g['piezas']:
            p = piezas[i]
            d = _dist_pieza(p, P, corte + k)
            if p['op'] == 'resta':
                if dg is not None:
                    dg = smax(dg, -d, k)
            else:
                dg = d if dg is None else smin(dg, d, k)
        if dg is not None:
            total = np.minimum(total, dg)
    return total


def _region(material, regiones, Pl, Nl=None):
    """Material final por punto según las regiones de la pieza (la última que aplica gana)."""
    mat = np.full(len(Pl), material)
    for r in regiones:
        tipo = r.get('tipo', 'caja')
        if tipo == 'caja':
            c, s = np.asarray(r.get('centro', [0, 0, 0]), float), np.asarray(r['tam'], float) / 2
            dentro = np.all(np.abs(Pl - c) <= s, axis=1)
        elif tipo == 'esfera':
            dentro = np.linalg.norm(Pl - np.asarray(r.get('centro', [0, 0, 0]), float), axis=1) <= r['r']
        elif tipo == 'franja':
            e = 'xyz'.index(r.get('eje', 'y'))
            dentro = (Pl[:, e] >= r.get('desde', -1e9)) & (Pl[:, e] <= r.get('hasta', 1e9))
        elif tipo == 'semiespacio':
            dentro = Pl @ np.asarray(r['normal'], float) > r.get('d', 0)
        elif tipo == 'cuadros':
            t = r.get('tam', 3)
            dentro = (np.floor(Pl[:, 0] / t) + np.floor(Pl[:, 1] / t) + np.floor(Pl[:, 2] / t)) % 2 == 0
        elif tipo == 'rayas':
            e = 'xyz'.index(r.get('eje', 'y'))
            dentro = np.mod(Pl[:, e] - r.get('fase', 0), r.get('periodo', 4)) < r.get('ancho', 1)
        elif tipo == 'ladrillos':
            # Juntas de un aparejo de ladrillo o de tejas: filas de `alto`, piezas de `ancho`, desfasadas.
            plano = r.get('plano', 'auto')
            if plano == 'auto' and Nl is not None:
                # En cada cara se usa el eje horizontal que corre a lo largo de ella
                u = np.where(np.abs(Nl[:, 0]) > np.abs(Nl[:, 2]), Pl[:, 2], Pl[:, 0]) - r.get('fase', [0, 0])[0]
                v = Pl[:, 1] - r.get('fase', [0, 0])[1]
            else:
                plano = 'xy' if plano == 'auto' else plano
                eu, ev = 'xyz'.index(plano[0]), 'xyz'.index(plano[1])
                u, v = Pl[:, eu] - r.get('fase', [0, 0])[0], Pl[:, ev] - r.get('fase', [0, 0])[1]
            fila = np.floor(v / r['alto'])
            junta = r.get('junta', 1.0)
            uu = u + (np.mod(fila, 2) * r['ancho'] / 2)
            dentro = (np.mod(v, r['alto']) < junta) | (np.mod(uu, r['ancho']) < junta * r.get('junta_v', 1.0))
        elif tipo == 'ruido':
            dentro = ruido3(Pl, r.get('escala', 4), r.get('semilla', 1), r.get('octavas', 2)) > r.get('umbral', 0.6)
        else:
            raise ValueError(f'Región de tipo desconocido: {tipo}')
        mat = np.where(dentro, r['_mat'], mat)
    return mat


def _vecinos(a, relleno):
    """Los 4 vecinos de cada celda (arriba, abajo, izquierda, derecha) con relleno en los bordes."""
    p = np.pad(a, 1, constant_values=relleno)
    return [p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]]


def _vecinos8(a, relleno):
    p = np.pad(a, 1, constant_values=relleno)
    H, W = a.shape
    return [p[1 + dy:1 + dy + H, 1 + dx:1 + dx + W] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx]


class Camara:
    """Ortográfica con giro e inclinación (combate) u oblicua (mundo cenital 3/4).

    En la oblicua el suelo se ve sin deformar (una baldosa cuadrada sigue cuadrada) y la altura se
    dibuja hacia arriba multiplicada por `alto`, como en los juegos de aldea con vista cenital.
    """

    def __init__(self, modelo, yaw, pitch):
        c = modelo.camara
        self.oblicua = c.get('proyeccion') == 'oblicua'
        if self.oblicua:
            self.h, self.g = c.get('alto', 0.8), c.get('fondo', 1.0)
            self.V = rot([0, yaw, 0])[:3, :3]
            d = np.array([0.0, self.g, self.h])
            self.dir_c = -d / np.linalg.norm(d)
            self.k = float(np.hypot(self.h, self.g))
        else:
            self.V = (rot([pitch, 0, 0]) @ rot([0, yaw, 0]))[:3, :3]
            self.dir_c = np.array([0, 0, -1.0])
            self.k = 1.0

    def origen(self, u, v):
        if self.oblicua:
            return np.stack([u, (v + self.g * ZC) / self.h, np.full(len(u), ZC)], 1)
        return np.stack([u, v, np.full(len(u), ZC)], 1)

    def proyectar(self, Pc):
        """Puntos en el marco de cámara -> coordenadas de pantalla (u, v) en unidades del modelo."""
        if self.oblicua:
            return Pc[:, 0], self.h * Pc[:, 1] - self.g * Pc[:, 2]
        return Pc[:, 0], Pc[:, 1]

    def prof(self, Pc):
        u, v = self.proyectar(Pc)
        return (Pc - self.origen(u, v)) @ self.dir_c


class Render:
    pass


def renderizar(modelo, yaw=None, pitch=None, anim=None, cuadro=0, pose=None, retocar=True):
    cam = modelo.camara
    yaw = cam['yaw'] if yaw is None else yaw
    pitch = cam['pitch'] if pitch is None else pitch
    t_fase = 0.0
    if pose is None:
        pose, t_fase = modelo.pose_de(anim, cuadro)
    piezas, grupos = modelo.escena(pose, t_fase)
    for g in grupos:
        g['piezas'].sort(key=lambda i: piezas[i]['op'] == 'resta')
    for p in piezas:
        for r in p['regiones']:
            r['_mat'] = modelo.lista_mat.index(r['material'])
    mats = [modelo.materiales[n] for n in modelo.lista_mat]

    W, H = modelo.lienzo
    ox, oy = modelo.origen
    esc = modelo.escala
    cam = Camara(modelo, yaw, pitch)
    V = cam.V
    ii, jj = np.meshgrid(np.arange(W), np.arange(H))
    uu = ((ii + 0.5 - ox) / esc).ravel()
    vv = ((oy - (jj + 0.5)) / esc).ravel()
    N = W * H
    Oc = cam.origen(uu, vv)
    O = Oc @ V
    D = cam.dir_c @ V

    # Rayos candidatos: los que cruzan alguna esfera envolvente
    t0 = np.full(N, np.inf)
    t1 = np.full(N, -np.inf)
    kmax = max([g['suave'] for g in grupos] + [0])
    for p in piezas:
        if p['op'] == 'resta':
            continue
        cc = V @ p['centro']
        pu, pv = cam.proyectar(cc[None])
        r = p['radio'] + 1 + kmax
        m = (np.abs(uu - pu[0]) < r) & (np.abs(vv - pv[0]) < r * cam.k)
        tc = (cc - Oc[m]) @ cam.dir_c
        t0[m] = np.minimum(t0[m], tc - r)
        t1[m] = np.maximum(t1[m], tc + r)
    idx = np.nonzero(np.isfinite(t0))[0]
    tt, tm = t0[idx].copy(), t1[idx]
    golpe = np.zeros(len(idx), bool)
    vivo = np.ones(len(idx), bool)
    for _ in range(220):
        a = np.nonzero(vivo)[0]
        if not len(a):
            break
        d = dist_escena(piezas, grupos, O[idx[a]] + D * tt[a, None])
        h = d < 0.02
        golpe[a[h]] = True
        vivo[a[h]] = False
        nh = a[~h]
        tt[nh] += np.maximum(d[~h] * 0.9, 0.01)
        vivo[nh[tt[nh] > tm[nh]]] = False
    hi = idx[golpe]
    th = tt[golpe]
    Ph = O[hi] + D * th[:, None]
    nh = len(hi)

    # Normales por diferencias centrales
    e = 0.08
    n = np.zeros((nh, 3))
    for k in range(3):
        dv = np.zeros(3)
        dv[k] = e
        n[:, k] = dist_escena(piezas, grupos, Ph + dv) - dist_escena(piezas, grupos, Ph - dv)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)

    # Pieza y material de cada pixel
    dist_p = np.stack([np.abs(_dist_pieza(p, Ph, 1e9)) for p in piezas], 0) if nh else np.zeros((0, 0))
    pid = np.argmin(dist_p, axis=0) if nh else np.zeros(0, int)
    mat = np.zeros(nh, int)
    textura = np.zeros(nh)
    for i, p in enumerate(piezas):
        m = pid == i
        if m.any():
            Pl = Ph[m] @ p['inv'][:3, :3].T + p['inv'][:3, 3]
            mat[m] = _region(p['material'], p['regiones'], Pl, n[m] @ p['inv'][:3, :3].T)
            for mi in np.unique(mat[m]):
                tx = mats[mi].textura
                if tx:
                    sel = mat[m] == mi
                    idx_m = np.nonzero(m)[0][sel]
                    textura[idx_m] = (ruido3(Pl[sel], tx.get('escala', 2.5), tx.get('semilla', 3), tx.get('octavas', 2))
                                      - 0.5) * 2 * tx.get('fuerza', 0.1)

    # Luz
    Lc = modelo.luz / np.linalg.norm(modelo.luz)
    Lm = Lc @ V
    val = 0.5 + 0.5 * (n @ Lm) + textura
    ao = np.zeros(nh)
    for k, hk in enumerate([0.8, 1.8, 3.5, 6.0]):
        ao += np.clip((hk - dist_escena(piezas, grupos, Ph + n * hk)) / hk, 0, 1) * (0.5 ** k)
    val -= 0.22 * np.clip(ao, 0, 1)
    sombra = np.zeros(nh, bool)
    if modelo.sombras and nh:
        st = np.full(nh, 0.0)
        base = Ph + n * 0.7
        viva = np.ones(nh, bool)
        for _ in range(70):
            a = np.nonzero(viva)[0]
            if not len(a):
                break
            d = dist_escena(piezas, grupos, base[a] + Lm * st[a, None])
            b = d < 0.05
            sombra[a[b]] = True
            viva[a[b]] = False
            st[a[~b]] += np.maximum(d[~b], 0.15)
            viva[a[st[a] > 90]] = False
        val = np.where(sombra, np.minimum(val, val * 0.6), val)
    nc = n @ V.T
    vista = -D
    Hm = (Lm + vista) / np.linalg.norm(Lm + vista)
    espec = np.clip(n @ Hm, 0, 1) ** 40
    ys, xs = np.divmod(hi, W)
    paso = np.zeros(nh, int)
    brillo = np.zeros(nh, bool)
    for mi, M in enumerate(mats):
        m = mat == mi
        if not m.any():
            continue
        v = val[m]
        if M.dither:
            v = v + (BAYER4[ys[m] % 4, xs[m] % 4] - 0.5) * 2 * M.dither
        s = np.searchsorted(M.umbrales, v) if not M.plano else np.full(m.sum(), min(2, len(M.colores) - 1))
        if M.brillo:
            b = espec[m] > 1 - M.brillo
            s = np.where(b, len(M.colores) - 1, s)
            brillo[np.nonzero(m)[0][b]] = True
        if modelo.borde_luz:
            frente = nc[m] @ -cam.dir_c
            borde = (1 - np.abs(frente) > 1 - modelo.borde_luz) & (nc[m, 0] * Lc[0] < 0) & (nc[m, 1] > -0.4)
            s = np.where(borde & ~sombra[m], np.minimum(s + 1, len(M.colores) - 1), s)
        paso[m] = np.clip(s, 0, len(M.colores) - 1)

    # Mapas en la cuadrícula del lienzo
    PID = np.full((H, W), -1)
    MAT = np.full((H, W), -1)
    PASO = np.full((H, W), -1)
    DEP = np.full((H, W), np.inf)
    BRI = np.zeros((H, W), bool)
    PID[ys, xs] = pid
    MAT[ys, xs] = mat
    PASO[ys, xs] = paso
    DEP[ys, xs] = th
    BRI[ys, xs] = brillo
    GID = np.full((H, W), -1)
    gidx = {}
    for gi, g in enumerate(grupos):
        for i in g['piezas']:
            gidx[i] = gi
    GID[ys, xs] = np.array([gidx[i] for i in pid]) if nh else []
    spr = PID >= 0

    # Limpieza: un paso de sombra aislado (sin vecino igual en 8 direcciones) toma el valor de sus
    # vecinos del mismo material; y en una escalera de 1 px (s-1, s, s+1) el del medio se une a un lado.
    for _ in range(3):
        vm, vp = _vecinos8(MAT, -2), _vecinos8(PASO, -2)
        iguales = sum((vm[k] == MAT) & (vp[k] == PASO) for k in range(8))
        mismos_mat = sum((vm[k] == MAT) for k in range(8))
        suelto = spr & ~BRI & (iguales == 0) & (mismos_mat >= 3)
        if not suelto.any():
            break
        votos = np.stack([np.where(vm[k] == MAT, vp[k], -9) for k in range(8)], 0)
        for y, x in zip(*np.nonzero(suelto)):
            vals = votos[:, y, x]
            vals = vals[vals >= 0]
            PASO[y, x] = np.bincount(vals).argmax()
    if modelo.d.get('sin_bandas', True):
        for _ in range(2):
            v4m, v4p = _vecinos(MAT, -2), _vecinos(PASO, -9)
            for a, b in ((0, 1), (2, 3)):
                mismo = (v4m[a] == MAT) & (v4m[b] == MAT) & spr & ~BRI
                esc = mismo & (np.abs(v4p[a] - v4p[b]) == 2) & (PASO * 2 == v4p[a] + v4p[b])
                if esc.any():
                    v8m, v8p = _vecinos8(MAT, -2), _vecinos8(PASO, -9)
                    cnt_a = sum((v8m[k] == MAT) & (v8p[k] == v4p[a]) for k in range(8))
                    cnt_b = sum((v8m[k] == MAT) & (v8p[k] == v4p[b]) for k in range(8))
                    PASO = np.where(esc, np.where(cnt_a >= cnt_b, v4p[a], v4p[b]), PASO)

    # Grupos de 1-2 pixeles de un tono rodeados por otro tono del mismo material: se unen a la mayoría
    if modelo.d.get('filtro_mayoria', True):
        nst = int(PASO.max()) + 1 if spr.any() else 1
        v8m, v8p = _vecinos8(MAT, -2), _vecinos8(PASO, -9)
        cuenta = np.zeros((nst, H, W), int)
        for k in range(8):
            mm = v8m[k] == MAT
            for s in range(nst):
                cuenta[s] += mm & (v8p[k] == s)
        propio = np.take_along_axis(cuenta, np.clip(PASO, 0, nst - 1)[None], 0)[0]
        cambio = spr & ~BRI & (propio <= 1) & (cuenta.max(0) >= 5)
        PASO = np.where(cambio, cuenta.argmax(0), PASO)

    # Color de relleno
    rgba = np.zeros((H, W, 4), np.uint8)
    TIPO = np.zeros((H, W), np.uint8)
    paleta = {}

    def poner(mask, hexcol, tipo):
        if not mask.any():
            return
        rgba[mask, :3] = color.hex_a_rgb(hexcol).astype(np.uint8)
        rgba[mask, 3] = 255
        TIPO[mask] = tipo
        paleta[hexcol] = paleta.get(hexcol, 0) + int(mask.sum())

    for mi, M in enumerate(mats):
        for si, c in enumerate(M.colores):
            poner(spr & (MAT == mi) & (PASO == si), c, RELLENO)
    TIPO[BRI & spr] = BRILLO

    # Líneas interiores: el pixel de atrás, junto a una pieza más cercana, toma la línea de la de adelante
    sin_linea = np.array([p['sin_linea'] for p in piezas] + [True])
    vP, vD, vG, vM = _vecinos(PID, -1), _vecinos(DEP, np.inf), _vecinos(GID, -1), _vecinos(MAT, -1)
    linea = np.zeros((H, W), bool)
    col_linea = np.full((H, W), -1)
    for k in range(4):
        with np.errstate(invalid='ignore'):
            salto = np.nan_to_num(DEP - vD[k], nan=0.0, posinf=0.0, neginf=0.0)
        cond = spr & (vP[k] >= 0) & ~sin_linea[vP[k]] & (
            ((vG[k] != GID) & (salto > modelo.umbral_linea)) | (salto > 4 * modelo.umbral_linea))
        nuevo = cond & ~linea
        col_linea[nuevo] = vM[k][nuevo]
        linea |= cond
    for mi, M in enumerate(mats):
        poner(linea & (col_linea == mi), M.linea, LINEA)

    # Contorno exterior (1 px, por fuera de la silueta)
    fuera = ~spr & np.logical_or.reduce([v >= 0 for v in _vecinos(PID, -1)])
    vecino_mat = np.full((H, W), -1)
    for v in _vecinos(MAT, -1)[::-1]:
        vecino_mat = np.where(fuera & (v >= 0), v, vecino_mat)
    for mi, M in enumerate(mats):
        m = fuera & (vecino_mat == mi)
        if modelo.contorno == 'selout':
            poner(m, M.contorno or M.linea, CONTORNO)
        else:
            poner(m, M.contorno or modelo.tinta, CONTORNO)

    r = Render()
    r.modelo, r.yaw, r.pitch, r.anim, r.cuadro = modelo, yaw, pitch, anim, cuadro
    r.rgba, r.pid, r.mat, r.paso, r.dep, r.tipo = rgba, PID, MAT, PASO, DEP, TIPO
    r.piezas = [p['nombre'] for p in piezas]
    r.V, r.cam, r.paleta = V, cam, paleta
    r.sombra = _sombra_suelo(modelo, piezas, grupos, O, D, Lm, spr) if modelo.d.get('sombra_suelo') else None
    _calcas(r, modelo, piezas, poner)
    if retocar:
        _retoques(r, modelo, poner)
    r.paleta = {c: n for c, n in paleta.items() if n}
    return r


def _ref_color(ref, modelo):
    if ref == 'tinta':
        return modelo.tinta
    if isinstance(ref, str) and ref.startswith('#'):
        return ref
    nombre, _, paso = str(ref).partition(':')
    M = modelo.materiales[nombre]
    return M.linea if paso == 'linea' else M.colores[int(paso or 2)]


def _calcas(r, modelo, piezas, poner):
    H, W = r.pid.shape
    nombres = {p['nombre']: i for i, p in enumerate(piezas)}
    ox, oy = modelo.origen
    for c in modelo.calcas:
        if c['pieza'] not in nombres:
            continue
        pi = nombres[c['pieza']]
        p = piezas[pi]
        a_m = (p['M'] @ np.append(np.asarray(c['pos'], float), 1))[:3]
        n_m = p['M'][:3, :3] @ np.asarray(c.get('normal', [0, 0, 1]), float)
        n_m /= np.linalg.norm(n_m)
        a_c, n_c = r.V @ a_m, r.V @ n_m
        ang = np.degrees(np.arccos(np.clip(n_c @ -r.cam.dir_c, -1, 1)))
        vistas = c['vistas']
        orden = [('frente', 28), ('tres_cuartos', 62), ('perfil', 100)]
        elegida = None
        for nombre, lim in orden:
            if ang <= lim and nombre in vistas:
                elegida = nombre
                break
        if elegida is None:
            if ang > 100:
                continue
            elegida = next((n for n, _ in orden[::-1] if n in vistas), None)
            if elegida is None:
                continue
        filas = vistas[elegida]
        voltear = (c['espejada'] if elegida == 'frente' else n_c[0] < 0)
        alto, ancho = len(filas), max(len(f) for f in filas)
        ax, ay = c.get('ancla', [ancho // 2, alto // 2])
        pu, pv = r.cam.proyectar(a_c[None])
        px0 = int(np.floor(ox + pu[0] * modelo.escala))
        py0 = int(np.floor(oy - pv[0] * modelo.escala))
        prof = float(r.cam.prof(a_c[None])[0])
        grupo = p['grupo']
        cols = c.get('colores', {})
        for fy, fila in enumerate(filas):
            for fx, ch in enumerate(fila):
                if ch in '. ' or ch not in cols:
                    continue
                dx = (ancho - 1 - fx) - (ancho - 1 - ax) if voltear else fx - ax
                x, y = px0 + dx, py0 + fy - ay
                if not (0 <= x < W and 0 <= y < H) or r.pid[y, x] < 0:
                    continue
                if piezas[r.pid[y, x]]['grupo'] != grupo or abs(r.dep[y, x] - prof) > c.get('tolerancia', 5):
                    continue
                m = np.zeros((H, W), bool)
                m[y, x] = True
                poner(m, _ref_color(cols[ch], modelo), CALCA)


def _sombra_suelo(modelo, piezas, grupos, O, D, Lm, spr):
    """Máscara de la sombra que el objeto proyecta sobre el suelo (y = 0), fuera de su silueta."""
    H, W = spr.shape
    out = np.zeros((H, W), bool)
    if D[1] > -1e-6 or Lm[1] <= 0:
        return out
    t = -O[:, 1] / D[1]
    G = O + D * t[:, None]
    libres = np.nonzero(~spr.ravel())[0]
    st = np.full(len(libres), 0.3)
    viva = np.ones(len(libres), bool)
    golpe = np.zeros(len(libres), bool)
    for _ in range(80):
        a = np.nonzero(viva)[0]
        if not len(a):
            break
        d = dist_escena(piezas, grupos, G[libres[a]] + Lm * st[a, None])
        b = d < 0.05
        golpe[a[b]] = True
        viva[a[b]] = False
        st[a[~b]] += np.maximum(d[~b], 0.2)
        viva[a[st[a] > 400]] = False
    out.ravel()[libres[golpe]] = True
    return out


def clave_retoque(yaw, pitch, anim, cuadro):
    return f'{yaw:g},{pitch:g},{anim or "-"},{cuadro}'


def _retoques(r, modelo, poner):
    H, W = r.pid.shape
    for clave in ('*', clave_retoque(r.yaw, r.pitch, r.anim, r.cuadro)):
        for x, y, c in modelo.retoques.get(clave, []):
            if 0 <= x < W and 0 <= y < H:
                m = np.zeros((H, W), bool)
                m[y, x] = True
                if c in ('.', 'borrar'):
                    r.rgba[y, x] = 0
                    r.tipo[y, x] = FONDO
                else:
                    poner(m, _ref_color(c, modelo), RETOQUE)
