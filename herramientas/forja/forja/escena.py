"""Compositor de escenas del mundo: suelo por baldosas + objetos ordenados por profundidad + sombras.

Archivo de escena (YAML):
  nombre, tam (px por baldosa), escala (para la vista previa)
  terrenos: lista de abajo hacia arriba {letra, nombre, base, tipo, semilla, ...}
  vertices: una línea por fila de vértices, una letra por vértice
  objetos: {modelo, objeto (si es biblioteca), en: [x, y] en baldosas, yaw, anim, cuadro}
"""
import os

import numpy as np
import yaml
from PIL import Image

from . import baldosas, color
from .modelo import Modelo
from .render import renderizar

SOMBRA = color.hex_a_rgb('#1c1630')


def _dispersar(d, vertices, fijos):
    """Reparte objetos al azar (reproducible) sobre un terreno, lejos de otros terrenos y sin encimarse.

    dispersar: [{modelo, objeto, terreno: 'p', cantidad: 40, distancia: 0.9, lejos_de: 't', margen: 1.0,
                 semilla: 1}]
    """
    salida = []
    colocados = [tuple(o['en']) for o in fijos]
    filas, cols = len(vertices), len(vertices[0])
    for regla in d.get('dispersar', []):
        r = np.random.default_rng(regla.get('semilla', 1))
        lejos = [(x, y) for y in range(filas) for x in range(cols) if vertices[y][x] in regla.get('lejos_de', '')]
        puestos, intentos = 0, 0
        while puestos < regla.get('cantidad', 20) and intentos < 5000:
            intentos += 1
            x, y = r.uniform(0, cols - 1), r.uniform(0, filas - 1)
            if vertices[int(round(y))][int(round(x))] not in regla.get('terreno', 'p'):
                continue
            if lejos and min(np.hypot(x - a, y - b) for a, b in lejos) < regla.get('margen', 1.0):
                continue
            if colocados and min(np.hypot(x - a, y - b) for a, b in colocados) < regla.get('distancia', 0.9):
                continue
            o = {k: v for k, v in regla.items() if k in ('modelo', 'objeto', 'yaw', 'anim', 'cuadro')}
            o['en'] = [x, y]
            salida.append(o)
            colocados.append((x, y))
            puestos += 1
    return salida


def componer(ruta):
    with open(ruta, encoding='utf-8') as f:
        d = yaml.safe_load(f)
    base_dir = os.path.dirname(os.path.abspath(ruta))
    tam = d.get('tam', 32)
    terrenos = []
    for t in d['terrenos']:
        kw = {k: v for k, v in t.items() if k not in ('letra', 'nombre', 'base', 'tipo', 'semilla')}
        terrenos.append((t['letra'], baldosas.Terreno(t['nombre'], t['base'], t.get('tipo', 'pasto'), t.get('semilla', 1), **kw)))
    vertices = [line.strip() for line in d['vertices'].strip().splitlines()]
    suelo = baldosas.suelo(vertices, terrenos, tam).astype(float)
    H, W = suelo.shape[:2]

    sprites = []
    cache = {}
    objetos = list(d.get('objetos', []))
    objetos += _dispersar(d, vertices, objetos)
    for o in objetos:
        ruta_m = os.path.join(base_dir, o['modelo']) if not os.path.isabs(o['modelo']) else o['modelo']
        clave = (ruta_m, o.get('objeto'), o.get('yaw'), o.get('anim'), o.get('cuadro', 0))
        if clave not in cache:
            m = Modelo(ruta_m, o.get('objeto'))
            cache[clave] = (m, renderizar(m, o.get('yaw'), None, o.get('anim'), o.get('cuadro', 0)))
        m, r = cache[clave]
        wx, wy = o['en'][0] * tam, o['en'][1] * tam
        x0, y0 = int(round(wx - m.origen[0])), int(round(wy - m.origen[1]))
        sprites.append((wy, x0, y0, r))

    # Sombras proyectadas sobre el suelo
    for _, x0, y0, r in sprites:
        if r.sombra is None:
            continue
        hs, ws = r.sombra.shape
        ys, xs = np.nonzero(r.sombra)
        ys, xs = ys + y0, xs + x0
        ok = (ys >= 0) & (ys < H) & (xs >= 0) & (xs < W)
        suelo[ys[ok], xs[ok]] = suelo[ys[ok], xs[ok]] * 0.7 + SOMBRA * 0.3
    lienzo = Image.fromarray(np.clip(suelo, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    for _, x0, y0, r in sorted(sprites, key=lambda s: s[0]):
        spr = Image.fromarray(r.rgba, 'RGBA')
        capa = Image.new('RGBA', lienzo.size, (0, 0, 0, 0))
        capa.paste(spr, (x0, y0))
        lienzo = Image.alpha_composite(lienzo, capa)
    return lienzo, d
