"""Prueba de Crisol: Teo (el caminante) en 8 ángulos y animado, al lado del Teo de Forja.

  python prueba_teo.py                 (desde herramientas/crisol/) 8 ángulos + reposo y caminar
  python prueba_teo.py --fuerzas       solo 3 ángulos con varias fuerzas, para escoger la buena

Lo que pinta el modelo se guarda en salida/cache/: si se vuelve a pedir lo mismo, no se vuelve a pintar.
"""
import hashlib
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from crisol import animar, guias, pixeles  # noqa: E402

SALIDA = os.path.join(AQUI, 'salida', 'teo')
CACHE = os.path.join(AQUI, 'salida', 'cache')
MODELO = os.path.join(AQUI, '..', 'forja', 'personajes', 'caminante.yaml')
# corta: CLIP lee 77 piezas como mucho y lo demás lo tira
DESCRIPCION = ('chibi desert wanderer boy, dark green hooded cloak, brown hair, sand scarf, tan tunic, '
               'brown boots, wooden staff')
TAM = 96          # lado del sprite en pixeles
COLORES = 20      # paleta común de cada personaje
FUERZA = 0.55
SEMILLA = 7
FONDO = (236, 228, 214)


class Pintor:
    """El modelo, cargado solo si hace falta pintar algo que no esté ya en la caché."""

    def __init__(self):
        self.motor = None
        self.pintadas = 0

    def __call__(self, base, bordes, yaw, fuerza=FUERZA):
        clave = hashlib.sha1(np.asarray(base).tobytes() + f'{yaw}|{fuerza}|{SEMILLA}|{DESCRIPCION}'.encode()).hexdigest()
        ruta = os.path.join(CACHE, clave[:20] + '.png')
        if os.path.exists(ruta):
            return Image.open(ruta).convert('RGB')
        if self.motor is None:
            from crisol.motor import Motor
            t = time.time()
            self.motor = Motor(DESCRIPCION)
            print(f'modelo cargado en {time.time() - t:.0f} s', flush=True)
        t = time.time()
        im = self.motor.pintar(base, bordes, yaw=yaw, semilla=SEMILLA, fuerza=fuerza)
        im.save(ruta)
        self.pintadas += 1
        print(f'  pintada en {time.time() - t:.0f} s', flush=True)
        return im


def guardar(sprites, nombre):
    for i, s in enumerate(sprites):
        Image.fromarray(s, 'RGBA').save(os.path.join(SALIDA, f'{nombre}_{i:02d}.png'))


def hoja(forjas, sprites, ruta, esc=4, texto=None):
    """Arriba Forja, abajo Crisol (el sprite a su tamaño real, ampliado ×esc sin suavizar)."""
    texto = texto or f'Arriba: Forja (guía). Abajo: Crisol, {TAM} px ampliado.'
    c = TAM * esc
    L = Image.new('RGB', (c * len(sprites), c * 2 + 30), FONDO)
    d = ImageDraw.Draw(L)
    for i, (f, s) in enumerate(zip(forjas, sprites)):
        L.paste(f.resize((c, c), Image.LANCZOS), (i * c, 0), f.resize((c, c), Image.LANCZOS))
        sp = Image.fromarray(s, 'RGBA').resize((c, c), Image.NEAREST)
        L.paste(sp, (i * c, c + 30), sp)
    d.text((6, c + 8), texto, fill=(60, 50, 40))
    L.save(ruta)


def gif(sprites, ruta, fps=20, esc=4):
    cuadros = [Image.fromarray(x, 'RGBA').resize((TAM * esc, TAM * esc), Image.NEAREST) for x in sprites]
    fondo = [Image.alpha_composite(Image.new('RGBA', q.size, FONDO + (255,)), q).convert('RGB') for q in cuadros]
    fondo[0].save(ruta, save_all=True, append_images=fondo[1:], duration=round(1000 / fps), loop=0)


def parpadeo(sprites):
    """Qué parte del personaje cambia de color de un cuadro al siguiente (en %)."""
    d = []
    for a, b in zip(sprites, sprites[1:] + sprites[:1]):
        ambos = (a[..., 3] > 0) & (b[..., 3] > 0)
        d.append(((a[..., :3] != b[..., :3]).any(-1) & ambos).sum() / ambos.sum())
    return round(float(np.mean(d)) * 100)


def angulos(pintor, fuerza=FUERZA, yaws=(0, 45, 90, 135, 180, 225, 270, 315), nombre='angulo'):
    forjas, crudas, mascaras = [], [], []
    for yaw in yaws:
        im, base, bordes, m = guias.guia(MODELO, yaw, 15)
        crudas.append(pintor(base, bordes, yaw, fuerza))
        forjas.append(im)
        mascaras.append(m)
    sps, _ = pixeles.sprites(crudas, mascaras, TAM, COLORES)
    guardar(sps, nombre)
    return forjas, sps


def animacion(pintor, anim, yaw=30, clave=0):
    from forja.pluma import Dibujo
    dib = Dibujo(MODELO)
    info = dib.d.get('animaciones', {}).get(anim, {})
    n, fps = info.get('cuadros', 16), info.get('fps', 20)
    gs = [guias.guia(dib, yaw, 15, anim, k) for k in range(n)]
    bases = [g[1] for g in gs]
    mascaras = [g[3] for g in gs]
    cuadros, generados = animar.animacion(bases, mascaras, lambda i: pintor(gs[i][1], gs[i][2], yaw),
                                          clave=clave, avisar=lambda s: print(f'{anim}: {s}', flush=True))
    sps, _ = pixeles.sprites(cuadros, mascaras, TAM, COLORES)
    guardar(sps, f'{anim}')
    gif(sps, os.path.join(SALIDA, f'{anim}.gif'), fps)
    # Forja reducido igual, para comparar cuánto cambia por sí solo
    forja_sps, _ = pixeles.sprites(bases, mascaras, TAM, COLORES)
    print(f'{anim}: {n} cuadros a {fps} fps; cambian por cuadro {parpadeo(sps)} % (Forja solo: {parpadeo(forja_sps)} %)',
          flush=True)
    paso = max(1, n // 8)
    hoja([gs[k][0] for k in range(0, n, paso)][:8], sps[::paso][:8], os.path.join(SALIDA, f'comparacion_{anim}.png'))
    return sps


def main():
    os.makedirs(SALIDA, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    t = time.time()
    pintor = Pintor()
    if '--fuerzas' in sys.argv:
        for f in (0.4, 0.55, 0.7):
            fo, s = angulos(pintor, f, (0, 90, 180), f'fuerza{int(f * 100)}')
            hoja(fo, s, os.path.join(SALIDA, f'comparacion_fuerza{int(f * 100)}.png'),
                 texto=f'Fuerza {f}: cuánto puede cambiar el dibujo de Forja.')
    else:
        fo, s = angulos(pintor)
        hoja(fo, s, os.path.join(SALIDA, 'comparacion_angulos.png'))
        for anim in (sys.argv[1:] or ['reposo', 'caminar']):
            animacion(pintor, anim)
    print(f'listo en {round(time.time() - t)} s; el modelo pintó {pintor.pintadas} imágenes nuevas')


if __name__ == '__main__':
    main()
