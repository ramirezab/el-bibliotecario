"""Vistas para revisar un sprite: hoja de revisión, texto ASCII, giros, animaciones y paletas."""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import color

FONDOS = {'papel': (242, 232, 213), 'noche': (24, 20, 38), 'banquete': (122, 68, 22), 'pasto': (88, 140, 64)}


def _fuente(t=12):
    for f in ('C:/Windows/Fonts/consola.ttf', 'C:/Windows/Fonts/arial.ttf'):
        if os.path.exists(f):
            return ImageFont.truetype(f, t)
    return ImageFont.load_default()


def imagen(rgba, escala=1, fondo=None):
    im = Image.fromarray(rgba, 'RGBA')
    if escala != 1:
        im = im.resize((im.width * escala, im.height * escala), Image.NEAREST)
    if fondo is not None:
        base = Image.new('RGBA', im.size, tuple(fondo) + (255,))
        base.alpha_composite(im)
        return base
    return im


def ampliado(rgba, z=8, marcas=None, cuadricula=True):
    """Vista ampliada con cuadrícula, reglas cada 8 px y marcas rojas en los problemas."""
    H, W = rgba.shape[:2]
    m = 22
    im = Image.new('RGBA', (W * z + m, H * z + m), (60, 60, 70, 255))
    tablero = Image.new('RGBA', (W * z, H * z))
    d0 = ImageDraw.Draw(tablero)
    for y in range(0, H * z, z * 2):
        for x in range(0, W * z, z * 2):
            d0.rectangle([x, y, x + z - 1, y + z - 1], fill=(205, 205, 210, 255))
            d0.rectangle([x + z, y + z, x + 2 * z - 1, y + 2 * z - 1], fill=(205, 205, 210, 255))
    d0.rectangle([0, 0, W * z, H * z], outline=None)
    fondo = Image.new('RGBA', (W * z, H * z), (225, 225, 230, 255))
    fondo.alpha_composite(tablero)
    fondo.alpha_composite(imagen(rgba, z))
    im.paste(fondo, (m, m))
    d = ImageDraw.Draw(im)
    f = _fuente(10)
    if cuadricula:
        for x in range(W + 1):
            c = (90, 90, 110, 255) if x % 8 == 0 else (150, 150, 165, 110)
            d.line([m + x * z, m, m + x * z, m + H * z], fill=c)
        for y in range(H + 1):
            c = (90, 90, 110, 255) if y % 8 == 0 else (150, 150, 165, 110)
            d.line([m, m + y * z, m + W * z, m + y * z], fill=c)
    for x in range(0, W, 8):
        d.text((m + x * z + 1, 4), str(x), fill=(230, 230, 240), font=f)
    for y in range(0, H, 8):
        d.text((1, m + y * z + 1), str(y), fill=(230, 230, 240), font=f)
    for (x, y), col in (marcas or []):
        d.rectangle([m + x * z, m + y * z, m + (x + 1) * z - 1, m + (y + 1) * z - 1], outline=col, width=2)
    return im


def _falso_color(mapa, n):
    rng = np.random.default_rng(7)
    tabla = rng.integers(60, 255, size=(max(n, 1) + 1, 3)).astype(np.uint8)
    out = np.zeros(mapa.shape + (4,), np.uint8)
    m = mapa >= 0
    out[m, :3] = tabla[mapa[m] % len(tabla)]
    out[m, 3] = 255
    return out


def silueta(rgba):
    out = np.zeros_like(rgba)
    out[..., 3] = (rgba[..., 3] > 0) * 255
    out[..., :3] = 20
    return out


def valores(rgba):
    lab = color.rgb_a_oklab(rgba[..., :3].astype(float))
    g = np.clip(lab[..., 0] * 255, 0, 255).astype(np.uint8)
    out = rgba.copy()
    out[..., 0] = out[..., 1] = out[..., 2] = g
    return out


def mapa_pasos(paso):
    tabla = np.array([[40, 30, 90], [90, 60, 160], [200, 120, 80], [250, 200, 90], [255, 250, 210],
                      [255, 255, 255], [255, 255, 255]], np.uint8)
    out = np.zeros(paso.shape + (4,), np.uint8)
    m = paso >= 0
    out[m, :3] = tabla[np.clip(paso[m], 0, len(tabla) - 1)]
    out[m, 3] = 255
    return out


def hoja(r, informe=None, referencia=None, titulo=''):
    """Hoja de revisión: ampliado con marcas, tamaños reales sobre varios fondos y mapas de análisis."""
    rgba = r.rgba
    H, W = rgba.shape[:2]
    z = max(3, min(8, 640 // max(W, H)))
    marcas = []
    if informe:
        for k, col in (('huerfanos', (255, 0, 80, 255)), ('huecos_contorno', (0, 200, 255, 255)),
                       ('dientes', (255, 160, 0, 255)), ('bandas', (180, 0, 255, 255)),
                       ('fuera_de_paleta', (255, 255, 0, 255))):
            marcas += [(p, col) for p in informe.get(k, [])]
    a = ampliado(rgba, z, marcas)
    paneles = []
    for nombre, fondo in FONDOS.items():
        paneles.append((nombre + ' x1', imagen(rgba, 1, fondo)))
    for nombre in ('papel', 'noche', 'banquete'):
        paneles.append((nombre + ' x2', imagen(rgba, 2, FONDOS[nombre])))
    paneles.append(('silueta', imagen(silueta(rgba), 2, FONDOS['papel'])))
    paneles.append(('valor', imagen(valores(rgba), 2, (128, 128, 128))))
    paneles.append(('piezas', imagen(_falso_color(r.pid, len(r.piezas)), 2, (40, 40, 40))))
    paneles.append(('pasos de luz', imagen(mapa_pasos(r.paso), 2, (40, 40, 40))))
    ref = None
    if referencia:
        ref = Image.open(referencia).convert('RGBA')
        k = a.height / ref.height
        ref = ref.resize((max(1, int(ref.width * k)), a.height), Image.LANCZOS)
    f = _fuente(12)
    col_w = max(p.width for _, p in paneles)
    columnas = 3
    filas_p = [paneles[i:i + columnas] for i in range(0, len(paneles), columnas)]
    alto_p = sum(max(p.height for _, p in fila) + 18 for fila in filas_p)
    ancho = a.width + 16 + columnas * (col_w + 10) + (ref.width + 16 if ref else 0)
    alto = max(a.height, alto_p) + 30
    hoja_im = Image.new('RGBA', (ancho, alto), (44, 42, 52, 255))
    d = ImageDraw.Draw(hoja_im)
    d.text((8, 6), titulo, fill=(240, 230, 210), font=_fuente(14))
    hoja_im.paste(a, (8, 26))
    x0 = a.width + 24
    y = 26
    for fila in filas_p:
        x = x0
        for nombre, p in fila:
            d.text((x, y), nombre, fill=(200, 200, 210), font=f)
            hoja_im.paste(p, (x, y + 16))
            x += col_w + 10
        y += max(p.height for _, p in fila) + 18
    if ref:
        hoja_im.paste(ref, (ancho - ref.width - 8, 26))
    return hoja_im


def texto(rgba, zona=None):
    """El sprite como texto: cada color es una letra; sirve para leer y señalar pixeles exactos."""
    H, W = rgba.shape[:2]
    x0, y0, x1, y1 = zona or (0, 0, W - 1, H - 1)
    letras = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@$%&*+=?'
    leyenda, lineas = {}, []
    lineas.append('    ' + ''.join(str((x // 10) % 10) if x % 10 == 0 else ' ' for x in range(x0, x1 + 1)))
    lineas.append('    ' + ''.join(str(x % 10) for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        fila = []
        for x in range(x0, x1 + 1):
            if rgba[y, x, 3] == 0:
                fila.append('.')
                continue
            h = color.rgb_a_hex(rgba[y, x, :3])
            if h not in leyenda:
                leyenda[h] = letras[len(leyenda) % len(letras)]
            fila.append(leyenda[h])
        lineas.append(f'{y:3d} ' + ''.join(fila))
    lineas.append('')
    lineas += [f'{v} = {k}' for k, v in leyenda.items()]
    return '\n'.join(lineas)


def tira(rgbas, escala=1, fondo=None, sep=0):
    """Pone varios sprites en fila (para giros y hojas de animación)."""
    ims = [imagen(x, escala, fondo) for x in rgbas]
    w = sum(i.width for i in ims) + sep * (len(ims) - 1)
    out = Image.new('RGBA', (w, max(i.height for i in ims)), (0, 0, 0, 0))
    x = 0
    for i in ims:
        out.alpha_composite(i, (x, 0))
        x += i.width + sep
    return out


def cebolla(rgbas, escala=4):
    """Papel cebolla: cada cuadro sobre el anterior en rojo translúcido."""
    out = []
    for i, x in enumerate(rgbas):
        prev = rgbas[i - 1].copy()
        prev[..., :3] = [230, 60, 60]
        prev[..., 3] = (prev[..., 3] > 0) * 90
        base = imagen(prev, escala, FONDOS['papel'])
        base.alpha_composite(imagen(x, escala))
        out.append(base)
    w = sum(i.width for i in out) + 6 * (len(out) - 1)
    hoja_im = Image.new('RGBA', (w, out[0].height), (44, 42, 52, 255))
    xx = 0
    for i in out:
        hoja_im.paste(i, (xx, 0))
        xx += i.width + 6
    return hoja_im


def gif(rgbas, ruta, fps=8, escala=4, fondo=FONDOS['papel']):
    ims = [imagen(x, escala, fondo).convert('RGB') for x in rgbas]
    ims[0].save(ruta, save_all=True, append_images=ims[1:], duration=int(1000 / fps), loop=0, disposal=2)


def muestras(modelo):
    """Rampas de todos los materiales con sus códigos HEX."""
    f = _fuente(12)
    filas = list(modelo.materiales.values())
    im = Image.new('RGBA', (560, 26 * len(filas) + 34), (44, 42, 52, 255))
    d = ImageDraw.Draw(im)
    d.text((8, 6), f'Paleta de {modelo.nombre} (tinta {modelo.tinta})', fill=(240, 230, 210), font=f)
    for i, M in enumerate(filas):
        y = 28 + i * 26
        d.text((8, y + 4), M.nombre, fill=(220, 220, 230), font=f)
        for j, c in enumerate(M.colores + [M.linea]):
            x = 120 + j * 62
            d.rectangle([x, y, x + 56, y + 20], fill=c)
            d.text((x + 2, y + 22 - 12), c, fill=(255, 255, 255) if color.luminosidad(c) < 0.6 else (0, 0, 0),
                   font=_fuente(9))
    return im
