"""Hojas de revisión para los dibujos a tinta (`pluma`): retrato, giro, cara de cerca, silueta, valores,
tamaño en juego, tiras de animación y GIF."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import color
from .pluma import dibujar
from .vistas import _fuente

PAPEL = (239, 230, 210)


def recortar(rgba, margen=14):
    a = rgba[..., 3] > 0
    if not a.any():
        return Image.fromarray(rgba, 'RGBA')
    ys, xs = np.where(a)
    y0, y1 = max(ys.min() - margen, 0), min(ys.max() + margen, rgba.shape[0])
    x0, x1 = max(xs.min() - margen, 0), min(xs.max() + margen, rgba.shape[1])
    return Image.fromarray(rgba[y0:y1, x0:x1], 'RGBA')


def fondo_bruma(ancho, alto, arriba='#0b1022', abajo='#2b3b66', semilla=3):
    """Fondo de cueva con niebla en capas y motas de luz, para ver el dibujo en un ambiente oscuro."""
    rng = np.random.default_rng(semilla)
    t = np.linspace(0, 1, alto)[:, None, None]
    c0, c1 = color.hex_a_rgb(arriba), color.hex_a_rgb(abajo)
    img = np.broadcast_to(c0 * (1 - t) + c1 * t, (alto, ancho, 3)).copy()
    yy, xx = np.mgrid[0:alto, 0:ancho]
    for _ in range(7):
        cx, cy = rng.uniform(0, ancho), rng.uniform(alto * 0.35, alto)
        rx, ry = rng.uniform(ancho * 0.25, ancho * 0.6), rng.uniform(alto * 0.06, alto * 0.16)
        g = np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))
        img += g[..., None] * np.array([70, 92, 140]) * rng.uniform(0.15, 0.35)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    motas = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(motas)
    for _ in range(int(ancho * alto / 9000)):
        x, y, r = rng.uniform(0, ancho), rng.uniform(0, alto), rng.uniform(1.0, 2.6)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(190, 220, 255, int(rng.uniform(60, 170))))
    halo = motas.filter(ImageFilter.GaussianBlur(3))
    im.alpha_composite(halo)
    im.alpha_composite(motas)
    return im


def sobre(im, fondo):
    if isinstance(fondo, Image.Image):
        base = fondo.resize(im.size) if fondo.size != im.size else fondo.copy()
    else:
        base = Image.new('RGBA', im.size, tuple(fondo) + (255,))
    base.alpha_composite(im)
    return base


def _silueta(im):
    a = np.array(im)[..., 3]
    out = np.full(a.shape + (3,), 255, np.uint8)
    out[a > 127] = (20, 18, 40)
    return Image.fromarray(out, 'RGB')


def _valores(im):
    x = np.array(im).astype(float)
    L = 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]
    a = x[..., 3] / 255
    g = L * a + 128 * (1 - a)
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), 'L').convert('RGB')


def _a_alto(im, alto):
    return im.resize((max(1, round(im.width * alto / im.height)), alto), Image.LANCZOS)


def _rotulo(lienzo, xy, texto, t=15, color=(60, 52, 80)):
    ImageDraw.Draw(lienzo).text(xy, texto, fill=color, font=_fuente(t))


def hoja(dib, titulo, yaw=None, pitch=None, anim=None, cuadro=0, giros=(0, 45, 90, 135, 180, 225, 270, 315)):
    r = dibujar(dib, yaw, pitch, anim, cuadro)
    heroe = recortar(r.rgba, 30)
    H = 640
    heroe_g = _a_alto(heroe, H)
    bruma = sobre(heroe_g, fondo_bruma(heroe_g.width, heroe_g.height))
    papel = sobre(heroe_g, PAPEL)

    # cara de cerca
    cab = next((it for it in r.items if it['nombre'] == 'cabeza'), None)
    z = 2.6
    rz = dibujar(dib, yaw, pitch, anim, cuadro, zoom=z)
    if cab is not None:
        b = cab['camino'].getBounds()
        cx, cy, lado = b.centerX() * z, b.centerY() * z, max(b.width(), b.height()) * z * 0.78
        cara = Image.fromarray(rz.rgba, 'RGBA').crop((int(cx - lado), int(cy - lado), int(cx + lado), int(cy + lado)))
    else:
        cara = recortar(rz.rgba)
    cara = sobre(_a_alto(cara, H), PAPEL)

    # giro completo
    vistas = [recortar(dibujar(dib, y, pitch, anim, cuadro).rgba, 10) for y in giros]
    alto_g = 300
    vistas = [_a_alto(v, alto_g) for v in vistas]

    # tamaño en juego (1:1) y lectura de forma
    juego = [_a_alto(heroe, h) for h in (96, 160, 240)]
    sil = _a_alto(_silueta(heroe_g), 300)
    val = _a_alto(_valores(heroe_g), 300)

    ancho = max(bruma.width + papel.width + cara.width + 80, sum(v.width for v in vistas) + 40 * len(vistas))
    alto = 60 + H + 50 + alto_g + 60 + 320 + 30
    L = Image.new('RGBA', (ancho, alto), (250, 246, 238, 255))
    _rotulo(L, (20, 16), titulo, 20, (30, 26, 60))
    x, y = 20, 56
    for im, rot in ((bruma, 'En ambiente oscuro'), (papel, 'Sobre papel'), (cara, 'Cara de cerca')):
        L.alpha_composite(im, (x, y))
        _rotulo(L, (x, y + H + 6), rot)
        x += im.width + 20
    y += H + 36
    x = 20
    for g, v in zip(giros, vistas):
        L.alpha_composite(sobre(v, PAPEL), (x, y))
        _rotulo(L, (x, y + alto_g + 4), f'{g:g}°', 13)
        x += v.width + 30
    y += alto_g + 34
    x = 20
    for im, rot in ((sil, 'Silueta'), (val, 'Valores')):
        L.paste(im, (x, y))
        _rotulo(L, (x, y + im.height + 4), rot, 13)
        x += im.width + 30
    fondo_j = fondo_bruma(sum(j.width for j in juego) + 80, 300, semilla=5)
    xj = 20
    for j in juego:
        fondo_j.alpha_composite(j, (xj, 300 - j.height - 20))
        xj += j.width + 20
    L.alpha_composite(fondo_j, (x, y))
    _rotulo(L, (x, y + 304), 'Tamaño real en pantalla: 96, 160 y 240 px de alto', 13)
    return L.convert('RGB'), r


def animacion(dib, anim, yaw=None, pitch=None, alto=360):
    """Cuadros de una animación: tira sobre papel, GIF sobre la bruma y lo que se mueve entre cuadros."""
    a = dib.animaciones[anim]
    n = a.get('cuadros', 1)
    rs = [dibujar(dib, yaw, pitch, anim, i) for i in range(n)]
    # mismo recorte para todos los cuadros, así no tiembla
    al = np.any([r.rgba[..., 3] > 0 for r in rs], axis=0)
    ys, xs = np.where(al)
    m = 16
    caja = (max(xs.min() - m, 0), max(ys.min() - m, 0), xs.max() + m, ys.max() + m)
    ims = [_a_alto(Image.fromarray(r.rgba, 'RGBA').crop(caja), alto) for r in rs]
    tira = Image.new('RGBA', (sum(i.width for i in ims) + 10 * (n - 1), alto), PAPEL + (255,))
    x = 0
    for i in ims:
        tira.alpha_composite(i, (x, 0))
        x += i.width + 10
    if dib.d.get('fondo_revision') == 'papel':
        fondo = PAPEL
    else:
        fondo = fondo_bruma(ims[0].width, alto, semilla=7)
    fotos = [sobre(i, fondo).convert('RGB') for i in ims]
    return tira.convert('RGB'), fotos, a.get('fps', 8)


def guardar_gif(fotos, ruta, fps):
    pal = [f.quantize(colors=255, method=Image.Quantize.MEDIANCUT) for f in fotos]
    pal[0].save(ruta, save_all=True, append_images=pal[1:], duration=int(1000 / fps), loop=0, disposal=2)
