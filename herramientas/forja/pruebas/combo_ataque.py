"""Teo ataca: animación del personaje + tajo de pluma + impacto, compuestos cuadro a cuadro."""
import sys
sys.path.insert(0, '.')
import numpy as np
from PIL import Image, ImageDraw
from forja.modelo import Modelo
from forja.render import renderizar
from forja import efectos, vistas

teo = Modelo('personajes/teo.yaml')
ataque = [renderizar(teo, 35, 12, 'ataque', i).rgba for i in range(10)]
tajo = [x for x, _ in efectos.cuadros(efectos.cargar('efectos/tajo_pluma.yaml'))]
golpe = [x for x, _ in efectos.cuadros(efectos.cargar('efectos/impacto.yaml'))]
W, H = 230, 140
fondo = np.zeros((H, W, 4), np.uint8)
fondo[...] = (40, 22, 18, 255)
fondo[96:, :] = (92, 52, 24, 255)
fondo[96:98, :] = (140, 86, 40, 255)
cuadros = []
for i in range(17):
    im = Image.fromarray(fondo.copy(), 'RGBA')
    sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse([40, 116, 84, 124], fill=(20, 10, 8, 150))
    im.alpha_composite(sombra)
    im.alpha_composite(Image.fromarray(ataque[min(i, 9)], 'RGBA'), (6, 6))
    j = i - 4
    if 0 <= j < len(tajo):
        im.alpha_composite(Image.fromarray(tajo[j], 'RGBA'), (36, 2))
    k = i - 6
    if 0 <= k < len(golpe):
        im.alpha_composite(Image.fromarray(golpe[k], 'RGBA'), (124, 40))
    cuadros.append(np.array(im))
vistas.gif(cuadros, 'salida/combo_ataque.gif', 15, 3, None)
tira = vistas.tira(cuadros[2:14], 2, None, 4)
tira.save('salida/combo_ataque_tira.png')
print(tira.size)
