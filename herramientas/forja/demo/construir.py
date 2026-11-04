"""Construye todo el arte de la demo jugable (demo/arte/): hojas de cuadros de Teo, el escarabajo y los NPC, los
elementos del oasis, los retratos de diálogo, el suelo del mapa y el fondo de batalla.

  python demo/construir.py            (desde herramientas/forja/)
  python demo/construir.py suelo fondo   (solo esas partes)
"""
import copy
import json
import math
import os
import sys

import numpy as np
import skia
import yaml
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FORJA = os.path.dirname(AQUI)
sys.path.insert(0, FORJA)
from forja import juego, laminas  # noqa: E402
from forja.pluma import Dibujo, dibujar  # noqa: E402

SALIDA = os.path.join(FORJA, '..', '..', 'demo', 'arte')
Z_EXP = 0.42      # escala de exploración (Teo mide unos 185 px en el lienzo de 1920×1080)
Z_COMBATE = 0.66  # escala de combate
PITCH_EXP = 30
RES = 2           # el juego dibuja a 1920×1080 con coordenadas de 960×540


def ruta(*p):
    return os.path.join(FORJA, *p)


# ---------------------------------------------------------------------------- personajes
def caminante():
    with open(ruta('personajes', 'caminante.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


def sin_piezas(d, nombres):
    d['piezas'] = [p for p in d['piezas'] if p.get('nombre') not in nombres]
    return d


def colores(d, cambios):
    for m, c in cambios.items():
        d['materiales'][m] = {**d['materiales'].get(m, {}), **c}
    return d


BASTON = {'vara', 'nudo', 'atadura', 'trapo', 'cordel', 'amuleto'}


def npc_nadia():
    d = caminante()
    d['nombre'] = 'Nadia'
    sin_piezas(d, BASTON)
    d['fisica']['cadenas'] = [c for c in d['fisica']['cadenas'] if c['nombre'] != 'trapo']
    return colores(d, {
        'capa': {'color': '#9a3f2e', 'sombra': '#6e2a1e', 'hondo': '#4a1a12', 'luz': '#c0604a', 'linea': '#2a0e08'},
        'forro': {'color': '#6a2a1e', 'sombra': '#4a1a12', 'linea': '#2a0e08'},
        'bufanda': {'color': '#3a8f8a', 'sombra': '#266660', 'hondo': '#184440', 'luz': '#5ab0aa', 'linea': '#0e2a28'},
        'pelo': {'color': '#2a1a12', 'sombra': '#180e0a', 'hondo': '#0e0806', 'luz': '#4a3020'},
        'piel': {'color': '#c48a5e', 'sombra': '#a06a48', 'luz': '#e0aa80', 'linea': '#5a3420'},
        'tunica': {'color': '#e6d2a8', 'sombra': '#bca47a', 'hondo': '#8a7450', 'luz': '#f6e8c8'},
    })


def npc_basim():
    d = caminante()
    d['nombre'] = 'Basim'
    cab = next(p for p in d['piezas'] if p['nombre'] == 'cabeza')
    cab['calcas'] = [c for c in cab['calcas'] if 'normal' in (c.get('caras') or ['normal'])
                     or 'caras' not in c and 'sin_caras' not in c]
    cab['calcas'] += [
        {'trazo': [[3.4, 3.6], [7.2, 4.8], [11.0, 3.4]], 'anchos': [1.2, 1.6, 0.6], 'color': '#f2eee6', 'espejo': True,
         'linea': True}]
    d['piezas'].append({'nombre': 'barba', 'hueso': 'cabeza', 'forma': 'casco', 'material': 'barba', 'capa': 9,
                        'esferas': [[0, -12.5, 13.5, 4.6], [-6, -10.5, 12.5, 4.0], [6, -10.5, 12.5, 4.0],
                                    [0, -18.5, 10.5, 3.2], [0, -23, 8, 1.2]]})
    return colores(d, {
        'barba': {'color': '#efe9de', 'sombra': '#c8c0b2', 'luz': '#ffffff', 'linea': '#5a5246'},
        'capa': {'color': '#d6c8a8', 'sombra': '#ad9e7e', 'hondo': '#82745a', 'luz': '#efe4c8', 'linea': '#3e3424'},
        'forro': {'color': '#a89a7a', 'sombra': '#82745a', 'linea': '#3e3424'},
        'bufanda': {'color': '#2c406e', 'sombra': '#1c2a4c', 'hondo': '#121c34', 'luz': '#4a62a0', 'linea': '#0a1020'},
        'pelo': {'color': '#d8d4cc', 'sombra': '#aaa49a', 'hondo': '#7a766e', 'luz': '#f4f2ee', 'linea': '#4a463e'},
        'piel': {'color': '#d29a6e', 'sombra': '#ae7a54', 'luz': '#ecba8e', 'linea': '#5a3820'},
        'tunica': {'color': '#5a6a7a', 'sombra': '#3e4a58', 'hondo': '#2a323c', 'luz': '#7a8a9a'},
    })


def npc_kiko():
    d = caminante()
    d['nombre'] = 'Kiko'
    d['escala'] = 3.1
    sin_piezas(d, BASTON | {'morral'})
    d['fisica']['cadenas'] = [c for c in d['fisica']['cadenas'] if c['nombre'] != 'trapo']
    return colores(d, {
        'capa': {'color': '#c8902e', 'sombra': '#9a6a1e', 'hondo': '#6a4612', 'luz': '#e8b450', 'linea': '#2e1e08'},
        'forro': {'color': '#8a5e1a', 'sombra': '#6a4612', 'linea': '#2e1e08'},
        'bufanda': {'color': '#c0423a', 'sombra': '#8e2a26', 'hondo': '#5e1a18', 'luz': '#e06a5a', 'linea': '#2e0a08'},
        'pelo': {'color': '#1e1410', 'sombra': '#120c08', 'luz': '#3e2a20'},
        'piel': {'color': '#b47a50', 'sombra': '#8e5a3a', 'luz': '#d49a6e', 'linea': '#4a2a16'},
    })


def retrato(dib, nombre, cara='normal', parte='cabeza'):
    """El busto para la caja de diálogo: la cabeza de frente, recortada en un cuadrado."""
    r = dibujar(dib, 15, 4, zoom=1.3, cara=cara)
    cab = next(it for it in r.items if it['nombre'] == parte)['camino'].getBounds()
    cx, cy, lado = cab.centerX(), cab.centerY() + cab.height() * 0.12, max(cab.width(), cab.height()) * 0.78
    im = Image.fromarray(r.rgba, 'RGBA').crop((int(cx - lado), int(cy - lado), int(cx + lado), int(cy + lado)))
    im.resize((256, 256), Image.LANCZOS).save(os.path.join(SALIDA, f'retrato_{nombre}.webp'), 'WEBP', quality=90)


def exploracion(dib, prefijo, yaws, anims=(('reposo', 2), ('caminar', 1))):
    pedidos = [{'clave': f'{a}_{y}', 'anim': a, 'yaw': y, 'pitch': PITCH_EXP, 'paso': paso}
               for y in yaws for a, paso in anims]
    return juego.exportar(dib, pedidos, SALIDA, prefijo, Z_EXP)


def personajes(meta):
    print('Teo')
    teo = Dibujo(caminante())
    meta['teo'] = exploracion(teo, 'teo', [0, 45, 90, 135, 180])
    meta['teo_combate'] = juego.exportar(teo, [{'clave': a, 'anim': a, 'yaw': 60, 'pitch': 6} for a in
                                               ('reposo', 'caminar', 'ataque', 'golpe')], SALIDA, 'teo_combate', Z_COMBATE)
    retrato(teo, 'teo')
    retrato(teo, 'teo_dolor', 'dolor')
    for nombre, f in (('nadia', npc_nadia), ('basim', npc_basim), ('kiko', npc_kiko)):
        print(nombre)
        dib = Dibujo(f())
        meta[nombre] = exploracion(dib, nombre, [0, 90, 180], (('reposo', 2),))
        retrato(dib, nombre)


def pavesa(meta):
    print('Pavesa')
    dib = Dibujo(ruta('personajes', 'pavesa.yaml'))
    meta['pavesa'] = exploracion(dib, 'pavesa', [0, 90, 180], (('reposo', 1), ('caminar', 1)))
    meta['pavesa_combate'] = juego.exportar(dib, [{'clave': a, 'anim': a, 'yaw': 60, 'pitch': 6} for a in
                                                  ('reposo', 'caminar', 'ataque', 'golpe')], SALIDA, 'pavesa_combate', Z_COMBATE)
    retrato(dib, 'pavesa', parte='llama')


def escarabajo(meta):
    print('Escarabajo')
    esc = Dibujo(ruta('personajes', 'escarabajo.yaml'))
    meta['escarabajo_combate'] = juego.exportar(esc, [{'clave': a, 'anim': a, 'yaw': 60, 'pitch': 10} for a in
                                                      ('reposo', 'caminar', 'ataque', 'golpe')],
                                                SALIDA, 'escarabajo_combate', 0.7)
    meta['escarabajo'] = juego.exportar(esc, [{'clave': 'reposo_20', 'anim': 'reposo', 'yaw': 20, 'pitch': PITCH_EXP,
                                               'paso': 2}], SALIDA, 'escarabajo', Z_EXP * 1.1)


# tamaño de cada elemento respecto de Teo (que es cabezón): la palmera mide más del doble que él
TAMANO = {'pagina': 1.6, 'palmera': 2.6, 'tienda': 2.1, 'pozo': 1.7, 'vasijas': 1.4, 'cajas': 1.5, 'roca': 1.6, 'cactus': 1.7,
          'arbusto': 1.3, 'juncos': 1.5, 'columna': 2.2, 'arco': 2.4, 'bloque': 1.6}


def elementos(meta):
    with open(ruta('mundo', 'oasis.yaml'), encoding='utf-8') as f:
        lib = yaml.safe_load(f)
    meta['props'] = {}
    for o in lib['objetos']:
        k = TAMANO.get(o, 1.0)
        for sufijo, yaw in (('', 0), ('_b', 40)) if o in ('roca', 'arbusto', 'vasijas', 'cajas', 'bloque', 'columna') else (('', 0),):
            # más grande sin engrosar la línea: sube la escala y baja el grosor en la misma proporción
            d = {k2: v for k2, v in lib.items() if k2 != 'objetos'}
            d.update(lib['objetos'][o])
            d['materiales'] = {**lib['materiales'], **lib['objetos'][o].get('materiales', {})}
            d['nombre'] = f'Oasis_{o}'
            d['escala'] = lib['escala'] * k
            d['grosor'] = lib['grosor'] / k
            d['grosor_silueta'] = lib['grosor_silueta'] / k
            d['lienzo'] = [int(lib['lienzo'][0] * k), int(lib['lienzo'][1] * k)]
            d['origen'] = [lib['origen'][0] * k, lib['origen'][1] * k]
            dib = Dibujo(d)
            m = juego.exportar(dib, [{'clave': o + sufijo, 'yaw': yaw}], SALIDA, 'prop', Z_EXP)
            meta['props'].update(m)


# ---------------------------------------------------------------------------- pintura con skia
def c4(h, a=1.0):
    h = h.lstrip('#')
    return skia.Color4f(int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def pintura(h, a=1.0, blur=0.0, trazo=0.0):
    p = skia.Paint(AntiAlias=True)
    p.setColor4f(c4(h, a))
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if trazo:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(trazo)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def mancha(cx, cy, rx, ry, semilla, irregular=0.12, n=48):
    """Un contorno cerrado y suave alrededor de (cx, cy), irregular como dibujado a mano."""
    rng = np.random.default_rng(semilla)
    k = rng.normal(0, 1, 6)
    th = np.linspace(0, math.tau, n, endpoint=False)
    f = 1 + irregular * (k[0] * np.sin(2 * th + k[1]) + k[2] * np.sin(3 * th + k[3]) * 0.6 + k[4] * np.sin(5 * th + k[5]) * 0.3) / 2
    pts = np.stack([cx + rx * f * np.cos(th), cy + ry * f * np.sin(th)], 1)
    return curva_cerrada(pts)


def curva_cerrada(pts):
    p = skia.Path()
    n = len(pts)
    p.moveTo(*((pts[0] + pts[1]) / 2))
    for i in range(1, n + 1):
        a, b = pts[i % n], pts[(i + 1) % n]
        p.quadTo(float(a[0]), float(a[1]), float((a[0] + b[0]) / 2), float((a[1] + b[1]) / 2))
    p.close()
    return p


def curva_abierta(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        p.quadTo(float(a[0]), float(a[1]), float((a[0] + b[0]) / 2), float((a[1] + b[1]) / 2))
    p.lineTo(*pts[-1])
    return p


def a_imagen(sup):
    return Image.fromarray(sup.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType,
                                                           alphaType=skia.kUnpremul_AlphaType), 'RGBA')


MAPA = (2200, 1400)
CAMINO = [(1100, 1420), (1080, 1300), (1040, 1170), (960, 1060), (880, 960), (800, 840), (790, 720), (850, 600),
          (960, 500), (1060, 420), (1100, 330), (1100, 200)]
ESTANQUE = (1150, 740, 250, 130)


def suelo():
    W, H = MAPA
    sup = skia.Surface(W * RES, H * RES)
    cv = sup.getCanvas()
    cv.scale(RES, RES)
    rng = np.random.default_rng(7)
    cv.clear(c4('#e6c38a'))
    # manchas de arena más oscura y más clara
    for i in range(70):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(60, 220)
        cv.drawPath(mancha(x, y, r, r * 0.55, i, 0.3), pintura(rng.choice(['#d8b077', '#efd09a', '#dcb57c']), 0.5, 18))
    # ondas de arena
    for i in range(260):
        x, y, L = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(30, 80)
        pts = [(x + L * t, y + 6 * math.sin(t * 3.0 + i)) for t in np.linspace(0, 1, 6)]
        cv.drawPath(curva_abierta(pts), pintura('#cfa56c', 0.45, 0, 1.6))
    # dunas en los bordes (no se pueden cruzar)
    for i, (x, y, rx, ry) in enumerate([(-80, 700, 260, 820), (2280, 700, 260, 820), (1100, -90, 1300, 190),
                                       (300, 1480, 520, 160), (1900, 1480, 520, 160)]):
        d = mancha(x, y, rx, ry, 100 + i, 0.08)
        cv.drawPath(d, pintura('#cf9f62'))
        cv.drawPath(d, pintura('#a87642', 1, 0, 3.5))
        cresta = mancha(x, y, rx * 0.85, ry * 0.85, 120 + i, 0.08)
        cv.drawPath(cresta, pintura('#e2b878', 0.8, 10))
    # el camino de tierra apisonada
    camino = curva_abierta(CAMINO)
    cv.drawPath(camino, pintura('#c99f68', 1, 0, 86))
    cv.drawPath(camino, pintura('#efd6a6', 1, 0, 74))
    cv.drawPath(camino, pintura('#f6e2b8', 0.6, 6, 30))
    # lajas en el camino
    for i, (ax, ay) in enumerate(CAMINO[1:-1]):
        for k in range(3):
            x, y = ax + rng.uniform(-28, 28), ay + rng.uniform(-20, 20)
            laja = mancha(x, y, rng.uniform(10, 16), rng.uniform(6, 9), 300 + i * 3 + k, 0.2, 16)
            cv.drawPath(laja, pintura('#d6b98e'))
            cv.drawPath(laja, pintura('#8a6a44', 1, 0, 1.6))
    # plaza de las tiendas
    plaza = mancha(560, 960, 210, 120, 21, 0.1)
    cv.drawPath(plaza, pintura('#c99f68', 1, 0, 12))
    cv.drawPath(plaza, pintura('#ecd2a0'))
    # pasto y orilla mojada del estanque
    ex, ey, rx, ry = ESTANQUE
    pasto = mancha(ex, ey, rx + 120, ry + 80, 31, 0.1)
    cv.drawPath(pasto, pintura('#6a9442', 1, 0, 8))
    cv.drawPath(pasto, pintura('#8ab45a'))
    for i in range(140):
        a = rng.uniform(0, math.tau)
        rr = rng.uniform(0.85, 1.3)
        x, y = ex + (rx + 60) * rr * math.cos(a), ey + (ry + 40) * rr * math.sin(a)
        for k in range(3):
            dx = (k - 1) * 3
            cv.drawPath(curva_abierta([(x + dx, y), (x + dx * 1.6, y - 7 - k % 2 * 3)]), pintura('#5a8236', 1, 0, 1.4))
    orilla = mancha(ex, ey, rx + 18, ry + 12, 41, 0.06)
    cv.drawPath(orilla, pintura('#c7a070'))
    agua = mancha(ex, ey, rx, ry, 41, 0.06)
    cv.drawPath(agua, pintura('#4fb0c0'))
    cv.save()
    cv.clipPath(agua, skia.ClipOp.kIntersect, True)
    cv.drawPath(mancha(ex + 10, ey + 12, rx * 0.7, ry * 0.6, 42, 0.1), pintura('#3a92a8', 1, 14))
    cv.drawPath(mancha(ex - rx * 0.1, ey - ry * 0.75, rx * 1.05, ry * 0.35, 43, 0.1), pintura('#2e7c90', 0.7, 10))
    cv.restore()
    cv.drawPath(agua, pintura('#1e4a58', 1, 0, 3.5))
    # ruinas del norte: losas rotas
    for i in range(46):
        x, y = 1100 + rng.uniform(-260, 260), 250 + rng.uniform(-90, 110)
        if rng.uniform() < 0.25:
            continue
        losa = skia.Path()
        w, h = rng.uniform(34, 52), rng.uniform(18, 26)
        losa.addRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 3, 3)
        cv.drawPath(losa, pintura(rng.choice(['#d8bc92', '#ccad80', '#e2c8a0'])))
        cv.drawPath(losa, pintura('#7a5a3a', 1, 0, 1.6))
    # cristales de sal y piedritas sueltas
    for i in range(70):
        x, y = rng.uniform(80, W - 80), rng.uniform(150, H - 120)
        if (x - ex) ** 2 / (rx + 150) ** 2 + (y - ey) ** 2 / (ry + 110) ** 2 < 1:
            continue
        if rng.uniform() < 0.4:
            p = skia.Path()
            p.addPoly([skia.Point(x - 4, y), skia.Point(x, y - 12), skia.Point(x + 4, y)], True)
            cv.drawPath(p, pintura('#f4eefb'))
            cv.drawPath(p, pintura('#5a5078', 1, 0, 1.2))
        else:
            pie = mancha(x, y, rng.uniform(3, 7), rng.uniform(2, 4), 500 + i, 0.2, 12)
            cv.drawPath(pie, pintura('#b08a5e'))
            cv.drawPath(pie, pintura('#6a4c2e', 1, 0, 1.2))
    im = a_imagen(sup).convert('RGB')
    im.save(os.path.join(SALIDA, 'suelo.webp'), 'WEBP', quality=82, method=6)
    print('suelo', im.size)


def fondo_batalla():
    W, H = 960, 540
    sup = skia.Surface(W * RES, H * RES)
    cv = sup.getCanvas()
    cv.scale(RES, RES)
    rng = np.random.default_rng(3)
    cielo = skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, 300)], [c4('#d9805a').toColor(), c4('#f6cf94').toColor()]))
    cv.drawRect(skia.Rect.MakeWH(W, H), cielo)
    # sol bajo con halo
    cv.drawCircle(220, 210, 170, pintura('#fff0c0', 0.35, 60))
    cv.drawCircle(220, 210, 58, pintura('#fff6dc', 0.95))
    # nubes alargadas
    for i in range(7):
        x, y = rng.uniform(0, W), rng.uniform(40, 170)
        n = mancha(x, y, rng.uniform(80, 160), rng.uniform(10, 18), 60 + i, 0.2)
        cv.drawPath(n, pintura('#f8dcb0', 0.55, 3))

    def dunas(y0, amp, col, linea, semilla, cresta):
        p = skia.Path()
        xs = np.linspace(-40, W + 40, 9)
        r = np.random.default_rng(semilla)
        pts = [(x, y0 - amp * r.uniform(0.2, 1)) for x in xs]
        p.moveTo(-40, H + 10)
        p.lineTo(*pts[0])
        for i in range(1, len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            p.quadTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        p.lineTo(*pts[-1])
        p.lineTo(W + 40, H + 10)
        p.close()
        cv.drawPath(p, pintura(col))
        cv.drawPath(curva_abierta(pts), pintura(cresta, 0.8, 4, 6))
        cv.drawPath(p, pintura(linea, 1, 0, 2))

    dunas(285, 60, '#e8b27c', '#c08454', 1, '#f8d4a0')
    # ruinas lejanas
    for x, h in ((600, 120), (650, 90), (700, 140), (760, 70), (880, 110)):
        col = skia.Path()
        col.addRect(skia.Rect.MakeXYWH(x, 300 - h, 18, h + 20))
        cv.drawPath(col, pintura('#c9926a'))
        cv.drawPath(col, pintura('#9a6a46', 1, 0, 1.6))
    arco = skia.Path()
    arco.addRect(skia.Rect.MakeXYWH(640, 172, 80, 16))
    cv.drawPath(arco, pintura('#c9926a'))
    cv.drawPath(arco, pintura('#9a6a46', 1, 0, 1.6))
    dunas(330, 40, '#dda068', '#a86e40', 2, '#f0c48c')
    # suelo de la arena de combate
    suelo = skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 340), skia.Point(0, H)], [c4('#e6bc80').toColor(), c4('#c8945c').toColor()]))
    p = skia.Path()
    p.moveTo(-10, 360)
    p.quadTo(W / 2, 330, W + 10, 360)
    p.lineTo(W + 10, H + 10)
    p.lineTo(-10, H + 10)
    p.close()
    cv.drawPath(p, suelo)
    cv.drawPath(curva_abierta([(-10, 360), (W / 2, 345), (W + 10, 360)]), pintura('#a0703e', 1, 0, 2))
    for i in range(120):
        x, y, L = rng.uniform(0, W), rng.uniform(370, H), rng.uniform(20, 50)
        cv.drawPath(curva_abierta([(x + L * t, y + 3 * math.sin(t * 3 + i)) for t in np.linspace(0, 1, 5)]),
                    pintura('#b88650', 0.5, 0, 1.4))
    # losas rotas bajo los personajes
    for i in range(18):
        x, y = rng.uniform(80, 880), rng.uniform(400, 500)
        losa = skia.Path()
        losa.addRoundRect(skia.Rect.MakeXYWH(x, y, rng.uniform(40, 70), rng.uniform(12, 18)), 3, 3)
        cv.drawPath(losa, pintura('#d8b88a', 0.9))
        cv.drawPath(losa, pintura('#8a6440', 1, 0, 1.4))
    # cristales de sal
    for i in range(16):
        x, y, s = rng.uniform(30, 930), rng.uniform(380, 530), rng.uniform(0.7, 1.6)
        p = skia.Path()
        p.addPoly([skia.Point(x - 5 * s, y), skia.Point(x - 1 * s, y - 18 * s), skia.Point(x + 5 * s, y)], True)
        cv.drawPath(p, pintura('#f4eefb'))
        cv.drawPath(p, pintura('#5a5078', 1, 0, 1.4))
    # rocas en primer plano, para enmarcar
    for x, y, rx, ry, k in ((-20, 540, 150, 70, 1), (990, 540, 170, 80, 2), (140, 560, 120, 40, 3)):
        r = mancha(x, y, rx, ry, 80 + k, 0.15)
        cv.drawPath(r, pintura('#6e4a32'))
        cv.drawPath(r, pintura('#2e1c12', 1, 0, 3))
    im = a_imagen(sup).convert('RGB')
    im.save(os.path.join(SALIDA, 'fondo_batalla.webp'), 'WEBP', quality=86, method=6)
    print('fondo_batalla', im.size)


def main(partes):
    os.makedirs(SALIDA, exist_ok=True)
    ruta_meta = os.path.join(SALIDA, 'hojas.json')
    meta = json.load(open(ruta_meta, encoding='utf-8')) if os.path.exists(ruta_meta) else {}
    if not partes or 'personajes' in partes:
        personajes(meta)
    if not partes or 'pavesa' in partes:
        pavesa(meta)
    if not partes or 'escarabajo' in partes:
        escarabajo(meta)
    if not partes or 'elementos' in partes:
        elementos(meta)
    if not partes or 'suelo' in partes:
        suelo()
    if not partes or 'fondo' in partes:
        fondo_batalla()
    meta['_escala'] = {'res': RES, 'mapa': list(MAPA), 'camino': CAMINO, 'estanque': list(ESTANQUE)}
    juego.guardar_meta(meta, ruta_meta)
    print('listo:', ruta_meta)


if __name__ == '__main__':
    main(sys.argv[1:])
