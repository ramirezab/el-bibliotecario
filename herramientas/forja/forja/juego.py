"""Exporta dibujos a tinta (pluma) como hojas de cuadros para el juego.

Cada pedido es una animación vista desde un ángulo: se dibujan todos sus cuadros con el mismo recorte, se
empacan en una imagen WebP y se anota en el JSON la celda, las columnas, los fps, si es un ciclo y el punto
de apoyo (el punto entre los pies, para pararlo en el suelo).

  pedidos = [{'clave': 'caminar_90', 'anim': 'caminar', 'yaw': 90, 'pitch': 30, 'paso': 1}, ...]
"""
import json
import math
import os

import numpy as np
from PIL import Image

from .pluma import dibujar


def exportar(dib, pedidos, carpeta, prefijo, zoom, calidad=88, margen=4):
    os.makedirs(carpeta, exist_ok=True)
    meta = {}
    for p in pedidos:
        clave, anim, paso = p['clave'], p.get('anim'), p.get('paso', 1)
        if anim and anim in dib.animaciones:
            a = dib.animaciones[anim]
            idx = list(range(0, a.get('cuadros', 1), paso))
            fps, bucle = a.get('fps', 12) / paso, a.get('bucle', True)
        else:
            idx, fps, bucle = [0], 1, True
        cuadros = [dibujar(dib, p.get('yaw'), p.get('pitch'), anim, i, zoom=zoom, cara=p.get('cara')).rgba
                   for i in idx]
        alfa = np.any([f[..., 3] > 6 for f in cuadros], axis=0)
        ys, xs = np.where(alfa)
        x0, y0 = max(int(xs.min()) - margen, 0), max(int(ys.min()) - margen, 0)
        x1, y1 = int(xs.max()) + margen + 1, int(ys.max()) + margen + 1
        cw, ch = x1 - x0, y1 - y0
        cols = max(1, min(len(cuadros), 4096 // cw))
        filas = math.ceil(len(cuadros) / cols)
        hoja = Image.new('RGBA', (cw * cols, ch * filas), (0, 0, 0, 0))
        for i, f in enumerate(cuadros):
            hoja.paste(Image.fromarray(f[y0:y1, x0:x1], 'RGBA'), ((i % cols) * cw, (i // cols) * ch))
        nombre = f'{prefijo}_{clave}.webp'
        hoja.save(os.path.join(carpeta, nombre), 'WEBP', quality=calidad, method=6)
        ox, oy = dib.origen[0] * zoom - x0, dib.origen[1] * zoom - y0
        meta[clave] = {'img': nombre, 'celda': [cw, ch], 'columnas': cols, 'n': len(cuadros), 'fps': fps,
                       'bucle': bucle, 'apoyo': [round(ox, 1), round(oy, 1)]}
        print(f'  {nombre}: {len(cuadros)} cuadros de {cw}×{ch}')
    return meta


def guardar_meta(meta, ruta):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))
