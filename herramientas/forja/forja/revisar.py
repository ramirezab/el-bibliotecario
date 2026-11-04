"""Revisión automática de un sprite: cada chequeo da un número y las posiciones (x, y) del problema.

Se basa en las reglas de oficio de Pixel Joint, Lospec, Slynyrd y Arne: paleta limitada, sin pixeles
huérfanos, contorno continuo, curvas sin dientes, sin bandas, sin sombreado de almohada y contraste
suficiente entre materiales.
"""
import numpy as np

from . import color
from .render import BRILLO, CALCA, CONTORNO, LINEA, RETOQUE


def _clave(rgba):
    return (rgba[..., 0].astype(np.int64) << 16) | (rgba[..., 1].astype(np.int64) << 8) | rgba[..., 2]


def _pad(a, v):
    return np.pad(a, 1, constant_values=v)


def huerfanos(rgba, tipo=None):
    """Pixeles distintos de sus 8 vecinos (se permiten brillos y calcas)."""
    op = rgba[..., 3] > 0
    k = np.where(op, _clave(rgba), -1)
    p = _pad(k, -1)
    H, W = k.shape
    iguales = np.zeros(k.shape, int)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy or dx:
                iguales += p[1 + dy:1 + dy + H, 1 + dx:1 + dx + W] == k
    m = op & (iguales == 0)
    if tipo is not None:
        m &= ~np.isin(tipo, [BRILLO, CALCA, RETOQUE])
    return [(int(x), int(y)) for y, x in zip(*np.nonzero(m))]


def huecos_contorno(rgba, umbral_L=0.38):
    """Pixeles del borde de la silueta que no son oscuros: el contorno tiene un hueco ahí."""
    op = rgba[..., 3] > 0
    p = _pad(op, False)
    borde = op & ~(p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:])
    lab = color.rgb_a_oklab(rgba[..., :3].astype(float))
    m = borde & (lab[..., 0] > umbral_L)
    return [(int(x), int(y)) for y, x in zip(*np.nonzero(m))]


def _corridas(seq):
    """Corridas de valores iguales: lista de (valor, largo, índice inicial)."""
    out, i = [], 0
    while i < len(seq):
        j = i
        while j + 1 < len(seq) and seq[j + 1] == seq[i]:
            j += 1
        out.append((seq[i], j - i + 1, i))
        i = j + 1
    return out


def dientes(rgba):
    """Escalones irregulares en el borde de la silueta (p. ej. corridas 3-1-3 en una curva)."""
    op = rgba[..., 3] > 0
    H, W = op.shape
    hallados = []
    for transpuesta in (False, True):
        m = op.T if transpuesta else op
        filas = [i for i in range(m.shape[0]) if m[i].any()]
        for lado in ('min', 'max'):
            xs = [(np.nonzero(m[i])[0].min() if lado == 'min' else np.nonzero(m[i])[0].max()) for i in filas]
            c = _corridas(xs)
            for a, b, d in zip(c, c[1:], c[2:]):
                pasos_mono = (a[0] - b[0]) * (b[0] - d[0]) > 0
                if pasos_mono and abs(a[0] - b[0]) == 1 and abs(b[0] - d[0]) == 1 \
                        and b[1] < min(a[1], d[1]) and min(a[1], d[1]) - b[1] >= 2:
                    fila = filas[b[2]]
                    x, y = (fila, b[0]) if transpuesta else (b[0], fila)
                    hallados.append((int(x), int(y)))
    return [(x, y) for x, y in hallados if 0 <= x < W and 0 <= y < H]


def bandas(paso, mat):
    """Tres pasos de sombra seguidos de 1 px cada uno (s-1, s, s+1) dentro de un mismo material."""
    hallados = []
    H, W = paso.shape
    for ej in (0, 1):
        a = paso if ej == 0 else paso.T
        b = mat if ej == 0 else mat.T
        mismo = (b[:, :-2] == b[:, 1:-1]) & (b[:, 1:-1] == b[:, 2:]) & (b[:, 1:-1] >= 0)
        sube = (a[:, 1:-1] - a[:, :-2] == 1) & (a[:, 2:] - a[:, 1:-1] == 1)
        baja = (a[:, 1:-1] - a[:, :-2] == -1) & (a[:, 2:] - a[:, 1:-1] == -1)
        ys, xs = np.nonzero(mismo & (sube | baja))
        for y, x in zip(ys, xs + 1):
            hallados.append((int(x), int(y)) if ej == 0 else (int(y), int(x)))
    return hallados


def almohada(paso, mat, luz):
    """Compara cuánto sigue el sombreado a la distancia al borde (almohada) y cuánto a la luz."""
    m = paso >= 0
    if m.sum() < 30:
        return 0.0, 0.0
    dist = np.zeros(paso.shape)
    cur = m.copy()
    k = 0
    while cur.any() and k < 40:
        dist[cur] += 1
        p = _pad(cur, False)
        cur = cur & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
        k += 1
    ys, xs = np.nonzero(m)
    cx, cy = xs.mean(), ys.mean()
    proy = (xs - cx) * luz[0] - (ys - cy) * luz[1]
    s = paso[m].astype(float)
    if s.std() == 0:
        return 0.0, 0.0
    c_borde = float(np.corrcoef(s, dist[m])[0, 1])
    c_luz = float(np.corrcoef(s, proy)[0, 1])
    return round(c_borde, 2), round(c_luz, 2)


def contraste_materiales(rgba, mat, tipo, nombres, minimo=0.07):
    """Pares de materiales vecinos cuyos colores casi no se distinguen (distancia OKLab media)."""
    lab = color.rgb_a_oklab(rgba[..., :3].astype(float))
    pares = {}
    for dy, dx in ((0, 1), (1, 0)):
        a = mat[:mat.shape[0] - dy, :mat.shape[1] - dx]
        b = mat[dy:, dx:]
        ta = tipo[:tipo.shape[0] - dy, :tipo.shape[1] - dx]
        tb = tipo[dy:, dx:]
        ok = (a >= 0) & (b >= 0) & (a != b) & (ta == 1) & (tb == 1)
        la = lab[:lab.shape[0] - dy, :lab.shape[1] - dx][ok]
        lb = lab[dy:, dx:][ok]
        dE = np.linalg.norm(la - lb, axis=1)
        for i, j, d in zip(a[ok], b[ok], dE):
            pares.setdefault(tuple(sorted((int(i), int(j)))), []).append(d)
    malos = []
    for (i, j), ds in pares.items():
        med = float(np.median(ds))
        if med < minimo:
            malos.append((nombres[i], nombres[j], round(med, 3)))
    return malos


def delgados(rgba):
    """Pixeles de 1 px de grosor (desaparecen o parpadean al animar)."""
    op = rgba[..., 3] > 0
    p = _pad(op, False)
    h = op & ~p[1:-1, :-2] & ~p[1:-1, 2:]
    v = op & ~p[:-2, 1:-1] & ~p[2:, 1:-1]
    return int((h | v).sum())


def revisar(r, paleta_permitida=None):
    rgba, tipo = r.rgba, r.tipo
    op = rgba[..., 3] > 0
    claves = np.unique(_clave(rgba)[op])
    inf = {}
    inf['colores'] = int(len(claves))
    if paleta_permitida:
        perm = {int(c.lstrip('#'), 16) for c in paleta_permitida}
        fuera = op & ~np.isin(_clave(rgba), list(perm))
        inf['fuera_de_paleta'] = [(int(x), int(y)) for y, x in zip(*np.nonzero(fuera))]
    inf['huerfanos'] = huerfanos(rgba, tipo)
    inf['huecos_contorno'] = huecos_contorno(rgba)
    inf['dientes'] = dientes(rgba)
    inf['bandas'] = bandas(r.paso, r.mat)
    c_borde, c_luz = almohada(r.paso, r.mat, r.modelo.luz)
    inf['almohada'] = {'sigue_al_borde': c_borde, 'sigue_a_la_luz': c_luz,
                       'sospecha': bool(c_borde > 0.5 and c_borde > c_luz + 0.15)}
    inf['contraste_bajo'] = contraste_materiales(rgba, r.mat, tipo, r.modelo.lista_mat)
    inf['delgados'] = delgados(rgba)
    ys, xs = np.nonzero(op)
    inf['caja'] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None
    inf['tamano'] = [int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)] if len(xs) else None
    return inf


def resumen(inf):
    lin = [f"Tamaño {inf['tamano'][0]}x{inf['tamano'][1]} px, {inf['colores']} colores." if inf['tamano'] else 'Vacío.']
    for k, txt in (('huerfanos', 'pixeles huérfanos'), ('huecos_contorno', 'huecos en el contorno'),
                   ('dientes', 'dientes en curvas'), ('bandas', 'bandas de sombra'),
                   ('fuera_de_paleta', 'pixeles fuera de paleta')):
        if k in inf:
            v = inf[k]
            lin.append(f"{len(v)} {txt}" + (f": {v[:8]}" if v else '.'))
    a = inf['almohada']
    lin.append(f"Sombreado sigue a la luz {a['sigue_a_la_luz']} y al borde {a['sigue_al_borde']}"
               + (' -> posible almohada.' if a['sospecha'] else '.'))
    if inf['contraste_bajo']:
        lin.append('Materiales que casi no se distinguen: ' + ', '.join(f'{a}/{b} ({d})' for a, b, d in inf['contraste_bajo']))
    lin.append(f"{inf['delgados']} pixeles de 1 px de grosor.")
    return '\n'.join(lin)


def comparar_cuadros(renders):
    """Consistencia de una animación: deriva de caja y paleta, pixeles que cambian y parpadeos."""
    cajas, paletas, cambios, parpadeos = [], [], [], 0
    claves = [np.where(r.rgba[..., 3] > 0, _clave(r.rgba), -1) for r in renders]
    for r, k in zip(renders, claves):
        ys, xs = np.nonzero(k >= 0)
        cajas.append([int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None)
        paletas.append(set(np.unique(k[k >= 0]).tolist()))
    n = len(claves)
    for i in range(n):
        a, b = claves[i], claves[(i + 1) % n]
        cambios.append(round(float((a != b).mean()) * 100, 1))
        if n >= 3:
            c = claves[(i + 2) % n]
            parpadeos += int(((a != b) & (a == c)).sum())
    union = set().union(*paletas)
    return {'cajas': cajas, 'colores_totales': len(union),
            'colores_que_no_estan_en_todos': len(union - set.intersection(*paletas)),
            'cambio_por_cuadro_%': cambios, 'pixeles_que_parpadean': parpadeos}
