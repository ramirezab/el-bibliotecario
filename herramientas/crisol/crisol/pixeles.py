"""Limpieza a pixel art de verdad: la imagen generada (1024 px) se lleva a su cuadrícula real, se le quita el fondo
con la silueta de Forja, se fija una paleta común y se quitan los pixeles sueltos."""
import numpy as np
from PIL import Image


def _multiplo(im, tam, filtro):
    """Lleva la imagen a un lado múltiplo de `tam` (1024 no se divide exacto entre 96, por ejemplo)."""
    n = max(1, round(im.width / tam))
    return im if im.width == tam * n else im.resize((tam * n, tam * n), filtro)


def a_cuadricula(im, tam=128):
    """Cada celda de la cuadrícula toma la mediana del centro de su bloque (no el promedio de todo el bloque: así
    no mezcla los colores de la orilla con los del vecino)."""
    a = np.array(_multiplo(im.convert('RGB'), tam, Image.NEAREST))
    n = a.shape[0] // tam
    bloques = a[:n * tam, :n * tam].reshape(tam, n, tam, n, 3).transpose(0, 2, 1, 3, 4).reshape(tam, tam, n * n, 3)
    # el centro del bloque representa bien al pixel de pixel-art-xl; se usa la mediana de un núcleo central
    c = bloques.reshape(tam, tam, n, n, 3)[:, :, n // 4:n - n // 4, n // 4:n - n // 4].reshape(tam, tam, -1, 3)
    return np.median(c, axis=2).astype(np.uint8)


def mascara_cuadricula(mascara, tam=128, minimo=0.5):
    mascara = np.array(_multiplo(Image.fromarray(mascara.astype(np.uint8) * 255), tam, Image.NEAREST)) > 127
    n = mascara.shape[0] // tam
    m = mascara[:n * tam, :n * tam].reshape(tam, n, tam, n).mean(axis=(1, 3))
    return m >= minimo


PESO = np.array([0.30, 0.59, 0.11]) ** 0.5 * np.sqrt(3)   # el ojo ve más la diferencia en verde que en azul


def _cercanos(px, pal):
    d = (((px[:, None, :] - pal[None, :, :]) * PESO) ** 2).sum(-1)
    return d.argmin(1)


def paleta(rgbs, mascaras, colores=32, vueltas=20, semilla=0):
    """Una paleta común para todos los cuadros (así no cambian los tonos entre ángulos ni entre cuadros).

    Solo cuenta los pixeles del personaje, no el fondo. k-means con semilla fija: el mismo resultado siempre."""
    px = np.concatenate([r[m].reshape(-1, 3) for r, m in zip(rgbs, mascaras)]).astype(float)
    rng = np.random.default_rng(semilla)
    # inicio k-means++: cada centro nuevo, lejos de los que ya hay
    pal = [px[rng.integers(len(px))]]
    for _ in range(colores - 1):
        d = (((px[:, None, :] - np.array(pal)[None]) * PESO) ** 2).sum(-1).min(1)
        pal.append(px[rng.choice(len(px), p=d / d.sum())])
    pal = np.array(pal)
    for _ in range(vueltas):
        e = _cercanos(px, pal)
        nueva = np.array([px[e == k].mean(0) if (e == k).any() else pal[k] for k in range(colores)])
        if np.allclose(nueva, pal, atol=0.5):
            break
        pal = nueva
    return np.round(pal).astype(np.uint8)


def aplicar_paleta(rgb, pal):
    h, w, _ = rgb.shape
    e = _cercanos(rgb.reshape(-1, 3).astype(float), pal.astype(float))
    return pal[e].reshape(h, w, 3)


def sin_sueltos(rgb, mascara, pasadas=2):
    """Un pixel cuyo color no comparte con ninguno de sus 4 vecinos toma el color más común alrededor."""
    out = rgb.copy()
    h, w, _ = rgb.shape
    for _ in range(pasadas):
        cambio = False
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if not mascara[y, x]:
                    continue
                v = [out[y - 1, x], out[y + 1, x], out[y, x - 1], out[y, x + 1]]
                if not any((c == out[y, x]).all() for c in v):
                    vs = [tuple(c) for c, mm in zip(v, [mascara[y - 1, x], mascara[y + 1, x], mascara[y, x - 1], mascara[y, x + 1]]) if mm]
                    if vs:
                        out[y, x] = max(set(vs), key=vs.count)
                        cambio = True
        if not cambio:
            break
    return out


def contorno(rgb, mascara, color=(26, 18, 14)):
    """Contorno exterior de 1 px, como en el pixel art de juegos."""
    m = mascara
    borde = np.zeros_like(m)
    borde[1:] |= m[:-1] & ~m[1:]
    borde[:-1] |= m[1:] & ~m[:-1]
    borde[:, 1:] |= m[:, :-1] & ~m[:, 1:]
    borde[:, :-1] |= m[:, 1:] & ~m[:, :-1]
    out = np.dstack([rgb, np.where(m, 255, 0).astype(np.uint8)])
    out[borde] = (*color, 255)
    return out


def sin_fondo_en_borde(rgb, m, claro=215, pasadas=2):
    """Quita de la silueta las celdas de la orilla que salieron del color del fondo blanco (el fondo se coló)."""
    m = m.copy()
    for _ in range(pasadas):
        fuera = ~m
        orilla = np.zeros_like(m)
        orilla[1:] |= fuera[:-1]
        orilla[:-1] |= fuera[1:]
        orilla[:, 1:] |= fuera[:, :-1]
        orilla[:, :-1] |= fuera[:, 1:]
        blanco = rgb.min(-1) >= claro
        quitar = m & orilla & blanco
        if not quitar.any():
            break
        m &= ~quitar
    return m


def preparar(generada, mascara1024, tam=128):
    """La imagen generada en su cuadrícula real y la silueta limpia: (rgb, mascara), antes de la paleta."""
    rgb = a_cuadricula(generada, tam)
    m = sin_fondo_en_borde(rgb, mascara_cuadricula(mascara1024, tam))
    return rgb, m


def sprite(rgb, m, pal):
    """Sprite final RGBA a partir de lo preparado: paleta común, sin pixeles sueltos y con contorno."""
    rgb = aplicar_paleta(rgb, pal)
    rgb = sin_sueltos(rgb, m)
    return contorno(rgb, m)


def sprites(generadas, mascaras1024, tam=128, colores=32):
    """Varios cuadros con una paleta común."""
    prep = [preparar(g, m, tam) for g, m in zip(generadas, mascaras1024)]
    pal = paleta([r for r, _ in prep], [m for _, m in prep], colores)
    return [sprite(r, m, pal) for r, m in prep], pal
