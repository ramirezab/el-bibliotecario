"""Baldosas de suelo sin costuras y transiciones entre terrenos por esquinas (16 variantes).

Cada terreno es una rampa de color + un patrón determinista (ruido periódico, matas, piedritas o
adoquines de Voronoi). Las transiciones usan un campo suave entre las 4 esquinas de la baldosa con
ruido periódico, así dos baldosas vecinas siempre coinciden en el borde. El borde del terreno de
arriba recibe luz arriba y sombra abajo, como el pasto que sobresale sobre un camino de tierra.
"""
import numpy as np

from . import color


def _hash2(ix, iy, semilla):
    n = (ix * 73856093) ^ (iy * 19349663) ^ (semilla * 83492791)
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)
    return (n & 0xFFFF) / 65535.0


def ruido_periodico(alto, ancho=None, celda=8, semilla=0, octavas=2):
    """Ruido de valor 2D de alto x ancho que se repite sin costura en ambos ejes."""
    ancho = ancho or alto
    y, x = np.mgrid[0:alto, 0:ancho].astype(float)
    total, amp, norma = 0.0, 1.0, 0.0
    for o in range(octavas):
        c = max(1, celda // (2 ** o))
        nx, ny = max(1, ancho // c), max(1, alto // c)
        gx, gy = x / c, y / c
        ix, iy = np.floor(gx).astype(np.int64), np.floor(gy).astype(np.int64)
        fx, fy = gx - ix, gy - iy
        ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        v = lambda a, b: _hash2(np.mod(a, nx), np.mod(b, ny), semilla + o)
        acc = (v(ix, iy) * (1 - ux) * (1 - uy) + v(ix + 1, iy) * ux * (1 - uy)
               + v(ix, iy + 1) * (1 - ux) * uy + v(ix + 1, iy + 1) * ux * uy)
        total = total + amp * acc
        norma += amp
        amp *= 0.5
    return total / norma


class Terreno:
    def __init__(self, nombre, base, tipo='pasto', semilla=1, **kw):
        self.nombre, self.tipo, self.semilla = nombre, tipo, semilla
        self.rampa = kw.get('rampa') or color.rampa(base, 5, 2, kw.get('dL', 0.09), kw.get('giro', 14))
        self.kw = kw

    def pasos(self, alto, ancho=None):
        """Mapa de pasos de rampa (0..4; 9 = flor) de este terreno para un área de alto x ancho."""
        ancho = ancho or alto
        r = np.random.default_rng(self.semilla)
        n = ruido_periodico(alto, ancho, self.kw.get('celda', 8), self.semilla, 3)
        s = np.clip(np.digitize(n, self.kw.get('cortes', [0.3, 0.44, 0.64, 0.8])), 1, 3)
        area = alto * ancho / 1024.0
        if self.tipo == 'pasto':
            for _ in range(int(self.kw.get('matas', 5) * area)):
                x, y = r.integers(0, ancho), r.integers(0, alto)
                for dx, dy, v in ((0, 0, 4), (-1, 1, 3), (1, 1, 3), (0, 1, 3), (-1, 2, 1), (1, 2, 1)):
                    s[(y + dy) % alto, (x + dx) % ancho] = v
            for _ in range(int(self.kw.get('flores', 0.6) * area)):
                x, y = r.integers(0, ancho), r.integers(0, alto)
                s[y, x] = 9
                s[(y + 1) % alto, x] = 0
        elif self.tipo == 'tierra':
            for _ in range(int(self.kw.get('piedritas', 7) * area)):
                x, y = r.integers(0, ancho), r.integers(0, alto)
                s[y % alto, x % ancho] = 4
                s[y % alto, (x + 1) % ancho] = 3
                s[(y + 1) % alto, x % ancho] = 1
                s[(y + 1) % alto, (x + 1) % ancho] = 0
        elif self.tipo == 'adoquin':
            s = self._adoquines(alto, r)
        return s

    def colores(self):
        """Rampa más el color de flor (paso 9)."""
        tabla = [color.hex_a_rgb(c) for c in self.rampa]
        tabla += [tabla[-1]] * (9 - len(tabla)) + [color.hex_a_rgb(self.kw.get('flor', '#f4e8a8'))]
        return np.array(tabla, np.uint8)

    def _adoquines(self, tam, r):
        k = self.kw.get('piedras', 10)
        pts = r.random((k, 2)) * tam
        y, x = np.mgrid[0:tam, 0:tam].astype(float)
        d1 = np.full((tam, tam), 1e9)
        d2 = np.full((tam, tam), 1e9)
        cel = np.zeros((tam, tam), int)
        for i, (px, py) in enumerate(pts):
            for ox in (-tam, 0, tam):
                for oy in (-tam, 0, tam):
                    d = np.hypot(x - px - ox, y - py - oy)
                    nuevo = d < d1
                    d2 = np.where(nuevo, d1, np.minimum(d2, d))
                    cel = np.where(nuevo, i, cel)
                    d1 = np.where(nuevo, d, d1)
        borde = (d2 - d1) < 1.6
        s = np.full((tam, tam), 2)
        arriba = np.roll(borde, 1, 0) | np.roll(borde, 1, 1)
        abajo = np.roll(borde, -1, 0) | np.roll(borde, -1, 1)
        s = np.where(abajo & ~borde, 1, s)
        s = np.where(arriba & ~borde, 3, s)
        s = np.where(borde, 0, s)
        return s


def _campo_esquinas(tam, esquinas, semilla):
    """Campo 0..1 suave entre los valores de las 4 esquinas (ai, ad, bi, bd) con borde irregular."""
    y, x = (np.mgrid[0:tam, 0:tam].astype(float) + 0.5) / tam
    ai, ad, bi, bd = esquinas
    f = ai * (1 - x) * (1 - y) + ad * x * (1 - y) + bi * (1 - x) * y + bd * x * y
    return f + (ruido_periodico(tam, tam, max(4, tam // 4), semilla + 99, 2) - 0.5) * 0.45


def baldosa(arriba, abajo, esquinas, tam=32):
    """Baldosa donde `arriba` cubre las esquinas marcadas con 1 sobre el terreno `abajo` (RGBA)."""
    sa, sb = np.clip(arriba.pasos(tam), 0, 4), np.clip(abajo.pasos(tam), 0, 4)
    if all(e == 1 for e in esquinas):
        m = np.ones((tam, tam), bool)
    elif all(e == 0 for e in esquinas):
        m = np.zeros((tam, tam), bool)
    else:
        m = _campo_esquinas(tam, esquinas, arriba.semilla) > 0.5
    rgb = np.zeros((tam, tam, 3), np.uint8)
    pa = np.array([color.hex_a_rgb(c) for c in arriba.rampa], np.uint8)
    pb = np.array([color.hex_a_rgb(c) for c in abajo.rampa], np.uint8)
    # Borde: luz arriba del terreno superior, sombra que proyecta sobre el inferior
    m_ab = np.vstack([m[:1], m[:-1]])     # pixel de arriba es terreno superior
    m_ar = np.vstack([m[1:], m[-1:]])     # pixel de abajo es terreno superior
    borde_sup = m & ~m_ar                 # borde inferior del terreno de arriba
    borde_luz = m & ~m_ab
    sombra = ~m & m_ab
    sa2 = np.where(borde_sup, 0, np.where(borde_luz, np.maximum(sa, 3), sa))
    sb2 = np.where(sombra, np.maximum(sb - 2, 0), sb)
    rgb[m] = pa[np.clip(sa2, 0, 4)][m]
    rgb[~m] = pb[np.clip(sb2, 0, 4)][~m]
    return rgb


def juego_de_esquinas(arriba, abajo, tam=32):
    """Las 16 baldosas por esquinas (índice = ai*8 + ad*4 + bi*2 + bd)."""
    return {i: baldosa(arriba, abajo, ((i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1), tam) for i in range(16)}


def suelo(vertices, terrenos, tam=32):
    """Pinta un suelo completo, sin repetición visible, a partir de una cuadrícula de vértices.

    `vertices` es una lista de cadenas, una letra por vértice; `terrenos` es una lista ordenada de
    abajo hacia arriba [(letra, Terreno), ...]. El límite entre terrenos se interpola entre vértices
    con un borde irregular; el terreno de arriba recibe luz en su borde superior, una línea oscura
    en el inferior, y proyecta una sombra corta sobre el de abajo.
    """
    filas, cols = len(vertices) - 1, len(vertices[0]) - 1
    H, W = filas * tam, cols * tam
    nivel = {k: i for i, (k, _) in enumerate(terrenos)}
    niv_v = np.array([[nivel[c] for c in fila] for fila in vertices], float)
    yy, xx = (np.mgrid[0:H, 0:W].astype(float) + 0.5) / tam
    i0, j0 = np.clip(np.floor(yy).astype(int), 0, filas - 1), np.clip(np.floor(xx).astype(int), 0, cols - 1)
    fy, fx = yy - i0, xx - j0
    ruido = (ruido_periodico(H, W, max(4, tam // 4), 99, 2) - 0.5) * 0.45
    lvl = np.zeros((H, W), int)
    for k in range(1, len(terrenos)):
        ind = (niv_v >= k).astype(float)
        f = (ind[i0, j0] * (1 - fx) * (1 - fy) + ind[i0, j0 + 1] * fx * (1 - fy)
             + ind[i0 + 1, j0] * (1 - fx) * fy + ind[i0 + 1, j0 + 1] * fx * fy) + ruido
        lvl = np.where(f > 0.5, k, lvl)
    img = np.zeros((H, W, 3), np.uint8)
    arriba = np.vstack([lvl[:1], lvl[:-1]])
    abajo = np.vstack([lvl[1:], lvl[-1:]])
    for k, (_, t) in enumerate(terrenos):
        m = lvl == k
        if not m.any():
            continue
        st = t.pasos(H, W)
        st = np.where(m & (abajo < k), 0, st)
        st = np.where(m & (arriba < k) & (st < 9), np.maximum(st, 3), st)
        st = np.where(m & (arriba > k) & (st < 9), np.maximum(st - 2, 0), st)
        img[m] = t.colores()[np.clip(st, 0, 9)][m]
    return img
