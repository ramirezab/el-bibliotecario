"""Recorte: animación 2D por capas de un dibujo plano, sin redibujarlo.

El dibujo se separa en capas (cabeza, cuerpo, botas...) con un pivote cada una. Cada cuadro mueve, gira,
estira o inclina las capas alrededor de su pivote, como un muñeco de cartón o un esqueleto de Spine, así que
el dibujo queda exactamente igual. Lo que una capa tapa (la bota bajo la capa, el cuello bajo la barbilla) se
rellena para que no aparezcan huecos al moverse. Los gestos (parpadeo, dolor) son capas extra que se
encienden según la cara del cuadro.
"""
import math

import numpy as np
import yaml
from PIL import Image, ImageDraw

from .modelo import _valor
from . import color

PROPIEDADES = {'dx': 0.0, 'dy': 0.0, 'rot': 0.0, 'sx': 1.0, 'sy': 1.0, 'kx': 0.0}


def fondo_a_alfa(rgb, umbral=232):
    """Quita el fondo claro conectado al borde de la imagen y suaviza el borde de la figura."""
    h, w, _ = rgb.shape
    claro = rgb.min(2) >= umbral
    fondo = np.zeros((h, w), bool)
    pila = [(y, x) for x in range(w) for y in (0, h - 1) if claro[y, x]]
    pila += [(y, x) for y in range(h) for x in (0, w - 1) if claro[y, x]]
    while pila:
        y, x = pila.pop()
        if fondo[y, x] or not claro[y, x]:
            continue
        fondo[y, x] = True
        if y > 0:
            pila.append((y - 1, x))
        if y < h - 1:
            pila.append((y + 1, x))
        if x > 0:
            pila.append((y, x - 1))
        if x < w - 1:
            pila.append((y, x + 1))
    # islas pequeñas sueltas en el fondo (motas de compresión) también son fondo
    alfa = np.where(fondo, 0.0, 1.0)
    # el borde: pixeles del fondo pegados a la figura toman alfa según cuánto se oscurecen
    vecino = np.zeros_like(fondo)
    fig = ~fondo
    vecino[1:] |= fig[:-1]
    vecino[:-1] |= fig[1:]
    vecino[:, 1:] |= fig[:, :-1]
    vecino[:, :-1] |= fig[:, 1:]
    borde = fondo & vecino
    alfa[borde] = np.clip((255 - rgb[borde].mean(1)) / 160.0, 0, 1)
    rgba = np.dstack([rgb, (alfa * 255).astype(np.uint8)])
    oscuro = np.array(color.hex_a_rgb('#2e2610'), float)
    rgba[borde, :3] = oscuro.astype(np.uint8)
    return rgba


def _mascara(d, h, w):
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.zeros((h, w), bool)
    if 'rect' in d:
        x0, y0, x1, y1 = d['rect']
        m |= (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
    if 'circulo' in d:
        cx, cy, r = d['circulo']
        m |= (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
    if 'poligono' in d:
        im = Image.new('L', (w, h), 0)
        ImageDraw.Draw(im).polygon([tuple(p) for p in d['poligono']], fill=255)
        m |= np.array(im) > 0
    for sub in d.get('o', []):
        m |= _mascara(sub, h, w)
    for sub in d.get('menos', []):
        m &= ~_mascara(sub, h, w)
    return m


def _dibujar(formas, h, w, ss=4):
    """Capa de gesto dibujada a mano (elipses y trazos), con suavizado por sobremuestreo."""
    im = Image.new('RGBA', (w * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for f in formas:
        col = f['color']
        if 'elipse' in f:
            cx, cy, rx, ry = f['elipse']
            d.ellipse([(cx - rx) * ss, (cy - ry) * ss, (cx + rx) * ss, (cy + ry) * ss], fill=col)
        if 'trazo' in f:
            pts = [(x * ss, y * ss) for x, y in f['trazo']]
            d.line(pts, fill=col, width=int(f.get('ancho', 3) * ss), joint='curve')
            r = f.get('ancho', 3) * ss / 2
            for x, y in (pts[0], pts[-1]):
                d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    return np.array(im.resize((w, h), Image.LANCZOS))


class Recorte:
    def __init__(self, ruta):
        with open(ruta, encoding='utf-8') as f:
            self.d = yaml.safe_load(f)
        import os
        base = os.path.dirname(os.path.abspath(ruta))
        rgb = np.array(Image.open(os.path.join(base, self.d['imagen'])).convert('RGB'))
        self.nombre = self.d.get('nombre', 'recorte')
        self.margen = self.d.get('margen', 60)
        rgba = fondo_a_alfa(rgb, self.d.get('umbral_fondo', 232))
        h, w = rgba.shape[:2]
        m = self.margen
        lienzo = np.zeros((h + 2 * m, w + 2 * m, 4), np.uint8)
        lienzo[m:m + h, m:m + w] = rgba
        self.original = lienzo
        self.h, self.w = lienzo.shape[:2]
        figura = lienzo[..., 3] > 0
        tomado = np.zeros_like(figura)
        self.capas = []
        for p in self.d['partes']:
            c = dict(p)
            c['pivote'] = np.array(p.get('pivote', [w / 2, h]), float) + m
            if 'dibujo' in p:
                formas = [dict(f) for f in p['dibujo']]
                for f in formas:
                    if 'elipse' in f:
                        f['elipse'] = [f['elipse'][0] + m, f['elipse'][1] + m] + list(f['elipse'][2:])
                    if 'trazo' in f:
                        f['trazo'] = [[x + m, y + m] for x, y in f['trazo']]
                c['img'] = _dibujar(formas, self.h, self.w)
            else:
                if p.get('resto'):
                    sel = figura & ~tomado
                else:
                    sel = figura & _desplazar(_mascara(p['mascara'], h, w), m, self.h, self.w) & ~tomado
                tomado |= sel
                img = np.zeros_like(lienzo)
                img[sel] = lienzo[sel]
                if 'extender_arriba' in p:
                    img = _extender_arriba(img, int(p['extender_arriba']))
                if 'relleno' in p:
                    img = _rellenar(img, p['relleno'], m)
                c['img'] = img
            self.capas.append(c)
        self.animaciones = self.d.get('animaciones', {})

    # ----------------------------------------------------------------- poses
    def cara_de(self, anim, cuadro):
        a = self.animaciones.get(anim, {})
        n = a.get('cuadros', 1)
        t = cuadro / n if a.get('bucle', True) else cuadro / max(n - 1, 1)
        cara = a.get('cara', 'normal')
        for k in sorted(a.get('claves', []), key=lambda k: k['t']):
            if k['t'] <= t + 1e-9 and 'cara' in k:
                cara = k['cara']
        for tramo in a.get('caras', []):
            if tramo['desde'] <= t < tramo['hasta']:
                cara = tramo['cara']
        return cara

    def pose_de(self, anim, cuadro):
        a = self.animaciones[anim]
        n = a.get('cuadros', 1)
        t = cuadro / n if a.get('bucle', True) else cuadro / max(n - 1, 1)
        if 'pose' in a:
            return _evaluar(a['pose'], t)
        claves = sorted(a['claves'], key=lambda k: k['t'])
        if t <= claves[0]['t']:
            return _evaluar(claves[0].get('pose', {}), t)
        for k0, k1 in zip(claves, claves[1:]):
            if k0['t'] <= t <= k1['t']:
                u = (t - k0['t']) / max(k1['t'] - k0['t'], 1e-9)
                if k1.get('curva', 'suave') == 'suave':
                    u = u * u * (3 - 2 * u)
                p0, p1 = _evaluar(k0.get('pose', {}), t), _evaluar(k1.get('pose', {}), t)
                salida = {}
                for parte in set(p0) | set(p1):
                    a0, a1 = p0.get(parte, {}), p1.get(parte, {})
                    salida[parte] = {k: a0.get(k, v) * (1 - u) + a1.get(k, v) * u for k, v in PROPIEDADES.items()}
                return salida
        return _evaluar(claves[-1].get('pose', {}), t)

    # ----------------------------------------------------------------- dibujo
    def cuadro(self, anim=None, cuadro=0, pose=None, cara=None):
        pose = pose if pose is not None else (self.pose_de(anim, cuadro) if anim else {})
        cara = cara or (self.cara_de(anim, cuadro) if anim else 'normal')
        por_nombre = {c['nombre']: c for c in self.capas}
        mats = {}

        def matriz(nombre):
            if nombre not in mats:
                c = por_nombre[nombre]
                q = {**PROPIEDADES, **pose.get(nombre, {})}
                px, py = c['pivote']
                L = (_tras(px + q['dx'], py + q['dy']) @ _rot(q['rot']) @ _sesgo(q['kx']) @ _esc(q['sx'], q['sy'])
                     @ _tras(-px, -py))
                mats[nombre] = (matriz(c['padre']) @ L) if c.get('padre') else L
            return mats[nombre]

        for c in self.capas:
            matriz(c['nombre'])
        salida = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0))
        for c in sorted(self.capas, key=lambda c: c.get('z', 0)):
            if 'caras' in c and cara not in c['caras']:
                continue
            if cara in c.get('sin_caras', []):
                continue
            inv = np.linalg.inv(mats[c['nombre']])
            img = Image.fromarray(c['img'], 'RGBA').transform(
                (self.w, self.h), Image.AFFINE, tuple(inv[:2].ravel()), resample=Image.BICUBIC)
            salida.alpha_composite(img)
        return np.array(salida)

    def cuadros(self, anim):
        n = self.animaciones[anim].get('cuadros', 1)
        return [self.cuadro(anim, i) for i in range(n)]


def _evaluar(pose, t):
    return {parte: {k: _valor(v, t) for k, v in props.items()} for parte, props in (pose or {}).items()}


def _desplazar(m, d, h, w):
    out = np.zeros((h, w), bool)
    out[d:d + m.shape[0], d:d + m.shape[1]] = m
    return out


def _extender_arriba(img, n):
    """Copia la fila de arriba de cada columna hacia arriba (lo que queda escondido bajo otra capa)."""
    a = img[..., 3] > 0
    out = img.copy()
    # solo las columnas con cuerpo de verdad (no el borde suavizado ni pixeles sueltos)
    for x in np.where((img[..., 3] == 255).sum(0) >= 12)[0]:
        y0 = int(np.argmax(a[:, x]))
        out[max(y0 - n, 0):y0, x] = img[y0 + 2 if y0 + 2 < img.shape[0] else y0, x]
    return out


def _rellenar(img, r, m):
    """Pinta una forma de un color solo donde la capa está vacía (detrás de lo que tapa otra capa)."""
    h, w = img.shape[:2]
    forma = _desplazar(_mascara(r, h - 2 * m, w - 2 * m), m, h, w)
    if 'desde_y' in r:
        forma[:int(r['desde_y']) + m] = False
    vacio = img[..., 3] == 0
    out = img.copy()
    col = color.hex_a_rgb(r['color']).astype(np.uint8)
    sel = forma & vacio
    out[sel, :3] = col
    out[sel, 3] = 255
    return out


def _tras(x, y):
    return np.array([[1, 0, x], [0, 1, y], [0, 0, 1.0]])


def _rot(g):
    c, s = math.cos(math.radians(g)), math.sin(math.radians(g))
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def _esc(sx, sy):
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1.0]])


def _sesgo(k):
    return np.array([[1, k, 0], [0, 1, 0], [0, 0, 1.0]])


def hoja_de_juego(rec, anims, alto, espejo=False):
    """Hoja de cuadros para el juego: todas las animaciones en celdas iguales, más su descripción."""
    todos = {a: rec.cuadros(a) for a in anims}
    caja = None
    for fr in todos.values():
        for f in fr:
            ys, xs = np.where(f[..., 3] > 8)
            b = (xs.min(), ys.min(), xs.max(), ys.max())
            caja = b if caja is None else (min(caja[0], b[0]), min(caja[1], b[1]), max(caja[2], b[2]), max(caja[3], b[3]))
    x0, y0, x1, y1 = caja[0] - 4, caja[1] - 4, caja[2] + 5, caja[3] + 3
    k = alto / (y1 - y0)
    cw, ch = int(round((x1 - x0) * k)), alto
    total = sum(len(f) for f in todos.values())
    cols = min(total, 12)
    filas = math.ceil(total / cols)
    hoja = Image.new('RGBA', (cw * cols, ch * filas), (0, 0, 0, 0))
    meta = {'celda': [cw, ch], 'columnas': cols, 'animaciones': {}}
    i = 0
    for a, fr in todos.items():
        idx = []
        for f in fr:
            im = Image.fromarray(f, 'RGBA').crop((x0, y0, x1, y1)).resize((cw, ch), Image.LANCZOS)
            if espejo:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            hoja.alpha_composite(im, ((i % cols) * cw, (i // cols) * ch))
            idx.append(i)
            i += 1
        an = rec.animaciones[a]
        meta['animaciones'][a] = {'cuadros': idx, 'fps': an.get('fps', 8), 'bucle': an.get('bucle', True)}
    # punto de apoyo (entre los pies), en pixeles de la celda
    pie = rec.d.get('apoyo', [rec.w / 2 - rec.margen, rec.h - 2 * rec.margen])
    ax = (pie[0] + rec.margen - x0) * k
    meta['apoyo'] = [round(cw - ax if espejo else ax, 1), round((pie[1] + rec.margen - y0) * k, 1)]
    return hoja, meta
