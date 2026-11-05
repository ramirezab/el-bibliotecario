"""Guías desde Forja: el personaje dibujado en el ángulo y cuadro pedidos, centrado en un cuadrado, con sus bordes
(para ControlNet) y su silueta (para quitar el fondo después)."""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

FORJA = os.path.join(os.path.dirname(__file__), '..', '..', 'forja')
sys.path.insert(0, os.path.abspath(FORJA))
from forja.pluma import Dibujo, dibujar  # noqa: E402


def cuadrado(rgba, lado=1024, margen=0.1):
    """Recorta lo dibujado y lo centra en un cuadrado de `lado`, apoyado abajo como un sprite."""
    a = rgba[..., 3] > 8
    ys, xs = np.where(a)
    im = Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1], 'RGBA')
    k = lado * (1 - 2 * margen) / max(im.width, im.height)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    lienzo = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    lienzo.alpha_composite(im, ((lado - im.width) // 2, lado - int(lado * margen) - im.height))
    return lienzo


def bordes(im_rgba, umbral=40):
    """Bordes blancos sobre negro, como espera ControlNet canny: la línea de tinta y los cambios de color."""
    fondo = Image.new('RGBA', im_rgba.size, (255, 255, 255, 255))
    fondo.alpha_composite(im_rgba)
    g = fondo.convert('L').filter(ImageFilter.GaussianBlur(1.2))
    e = np.array(g.filter(ImageFilter.FIND_EDGES), float)
    # solo la tinta casi negra cuenta como línea (la capa verde oscura no)
    tinta = np.array(g, float) < 32
    m = (e > umbral) | tinta
    return Image.fromarray(np.where(m, 255, 0).astype(np.uint8), 'L').convert('RGB')


def sobre_blanco(im_rgba):
    fondo = Image.new('RGBA', im_rgba.size, (255, 255, 255, 255))
    fondo.alpha_composite(im_rgba)
    return fondo.convert('RGB')


def guia(modelo, yaw, pitch, anim=None, cuadro=0, lado=1024, zoom=1.2):
    """Devuelve (dibujo RGBA, dibujo sobre blanco para img2img, bordes para ControlNet, silueta)."""
    dib = modelo if isinstance(modelo, Dibujo) else Dibujo(modelo)
    r = dibujar(dib, yaw, pitch, anim, cuadro, zoom=zoom)
    im = cuadrado(r.rgba, lado)
    return im, sobre_blanco(im), bordes(im), np.array(im)[..., 3] > 8
