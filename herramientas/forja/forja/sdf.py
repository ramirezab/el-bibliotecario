"""Primitivas de distancia con signo (SDF), vectorizadas con numpy.

Cada primitiva recibe puntos P (N, 3) en coordenadas locales de la pieza y devuelve
la distancia (N,). Fórmulas de Inigo Quilez (iquilezles.org/articles/distfunctions).
Además de la distancia, cada forma informa una esfera envolvente para acelerar el trazado.
"""
import numpy as np


def _n(v):
    return np.linalg.norm(v, axis=-1)


def esfera(P, r):
    return _n(P) - r


def elipsoide(P, radios):
    r = np.asarray(radios, float)
    k0 = _n(P / r)
    k1 = _n(P / (r * r))
    return k0 * (k0 - 1) / np.maximum(k1, 1e-9)


def caja(P, tam, radio=0.0):
    q = np.abs(P) - (np.asarray(tam, float) / 2 - radio)
    return _n(np.maximum(q, 0)) + np.minimum(q.max(axis=1), 0) - radio


def cilindro(P, r, alto, radio=0.0):
    """Cilindro vertical (eje Y) centrado en el origen."""
    d = np.stack([np.hypot(P[:, 0], P[:, 2]) - r + radio, np.abs(P[:, 1]) - alto / 2 + radio], 1)
    return np.minimum(d.max(axis=1), 0) + _n(np.maximum(d, 0)) - radio


def toro(P, R, r):
    """Toro en el plano XY (el agujero mira hacia +Z), útil para lentes y aros."""
    q = np.stack([np.hypot(P[:, 0], P[:, 1]) - R, P[:, 2]], 1)
    return _n(q) - r


def cono_redondo(P, a, b, ra, rb):
    """Cápsula de radios distintos entre los puntos a (radio ra) y b (radio rb)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    ba = b - a
    l2 = ba @ ba
    rr = ra - rb
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pa = P - a
    y = pa @ ba
    z = y - l2
    x = pa * l2 - np.outer(y, ba)
    x2 = np.sum(x * x, 1)
    y2 = y * y * l2
    z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    return np.where(np.sign(z) * a2 * z2 > k, np.sqrt(x2 + z2) * il2 - rb,
                    np.where(np.sign(y) * a2 * y2 < k, np.sqrt(x2 + y2) * il2 - ra,
                             (np.sqrt(np.maximum(x2 * a2 * il2, 0)) + y * rr) * il2 - ra))


def cono(P, alto, r1, r2, radio=0.0):
    """Cono truncado vertical con base plana: radio r1 en y=0 y r2 en y=alto (Quilez, sdCappedCone)."""
    h = alto / 2
    q = np.stack([np.hypot(P[:, 0], P[:, 2]), P[:, 1] - h], 1)
    k1 = np.array([r2, h])
    k2 = np.array([r2 - r1, 2 * h])
    ca = np.stack([q[:, 0] - np.minimum(q[:, 0], np.where(q[:, 1] < 0, r1, r2)), np.abs(q[:, 1]) - h], 1)
    t = np.clip(((k1 - q) @ k2) / (k2 @ k2), 0, 1)
    cb = q - k1 + np.outer(t, k2)
    s = np.where((cb[:, 0] < 0) & (ca[:, 1] < 0), -1.0, 1.0)
    return s * np.sqrt(np.minimum(np.sum(ca * ca, 1), np.sum(cb * cb, 1))) - radio


def poligono2d(p, v):
    v = np.asarray(v, float)
    d = np.sum((p - v[0]) ** 2, axis=1)
    s = np.ones(len(p))
    j = len(v) - 1
    for i in range(len(v)):
        e = v[j] - v[i]
        w = p - v[i]
        t = np.clip((w @ e) / (e @ e), 0, 1)
        b = w - np.outer(t, e)
        d = np.minimum(d, np.sum(b * b, axis=1))
        c1 = p[:, 1] >= v[i, 1]
        c2 = p[:, 1] < v[j, 1]
        c3 = e[0] * w[:, 1] > e[1] * w[:, 0]
        s = np.where((c1 & c2 & c3) | (~c1 & ~c2 & ~c3), -s, s)
        j = i
    return s * np.sqrt(d)


def extrusion(P, puntos, grosor, radio=0.0):
    """Polígono en el plano XY extruido a lo largo de Z, con bordes redondeados opcionales."""
    d2 = poligono2d(P[:, :2], puntos) + radio
    w = np.stack([d2, np.abs(P[:, 2]) - grosor / 2 + radio], 1)
    return np.minimum(w.max(axis=1), 0) + _n(np.maximum(w, 0)) - radio


def _hash(ix, iy, iz, semilla):
    n = (ix * 73856093) ^ (iy * 19349663) ^ (iz * 83492791) ^ (semilla * 2654435761)
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)
    return (n & 0xFFFF) / 65535.0


def ruido3(P, escala=4.0, semilla=0, octavas=1):
    """Ruido de valor 3D suave en [0, 1]. Determinista: el mismo punto da siempre el mismo valor."""
    total, amp, norma = 0.0, 1.0, 0.0
    for o in range(octavas):
        Q = np.asarray(P, float) / (escala / (2 ** o))
        i = np.floor(Q).astype(np.int64)
        f = Q - i
        u = f * f * (3 - 2 * f)
        acc = 0.0
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    w = (u[:, 0] if dx else 1 - u[:, 0]) * (u[:, 1] if dy else 1 - u[:, 1]) * (u[:, 2] if dz else 1 - u[:, 2])
                    acc = acc + w * _hash(i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz, semilla + o)
        total = total + amp * acc
        norma += amp
        amp *= 0.5
    return total / norma


def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def smax(a, b, k):
    return -smin(-a, -b, k)


# Cada forma: (función de distancia, función de esfera envolvente local -> (centro, radio))
def _env_capsula(p):
    a, b = np.asarray(p['a'], float), np.asarray(p['b'], float)
    return (a + b) / 2, _n(b - a) / 2 + max(p.get('ra', p.get('r', 0)), p.get('rb', p.get('r', 0)))


def _env_extrusion(p):
    v = np.asarray(p['puntos'], float)
    c = v.mean(axis=0)
    return np.array([c[0], c[1], 0.0]), float(np.max(_n(v - c))) + p.get('grosor', 1) / 2


FORMAS = {
    'esfera': (lambda P, p: esfera(P, p['r']), lambda p: (np.zeros(3), p['r'])),
    'elipsoide': (lambda P, p: elipsoide(P, p['radios']), lambda p: (np.zeros(3), max(p['radios']))),
    'caja': (lambda P, p: caja(P, p['tam'], p.get('radio', 0)),
             lambda p: (np.zeros(3), _n(np.asarray(p['tam'], float)) / 2)),
    'cilindro': (lambda P, p: cilindro(P, p['r'], p['alto'], p.get('radio', 0)),
                 lambda p: (np.zeros(3), float(np.hypot(p['r'], p['alto'] / 2)))),
    'toro': (lambda P, p: toro(P, p['R'], p['r']), lambda p: (np.zeros(3), p['R'] + p['r'])),
    'capsula': (lambda P, p: cono_redondo(P, p['a'], p['b'], p.get('ra', p.get('r')), p.get('rb', p.get('r'))),
                _env_capsula),
    'extrusion': (lambda P, p: extrusion(P, p['puntos'], p['grosor'], p.get('radio', 0)), _env_extrusion),
    'cono': (lambda P, p: cono(P, p['alto'], p['r1'], p['r2'], p.get('radio', 0)),
             lambda p: (np.array([0.0, p['alto'] / 2, 0.0]), float(np.hypot(max(p['r1'], p['r2']), p['alto'] / 2)))),
}
