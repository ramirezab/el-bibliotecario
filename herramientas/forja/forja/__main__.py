"""Línea de comandos de Forja.

  python -m forja hoja    modelo.yaml [--yaw 35 --pitch 15 --anim reposo --cuadro 0 --ref img.png]
  python -m forja giro    modelo.yaml [--yaws 0,45,90,135,180,225,270,315 --pitch 15]
                          (con ángulos negativos: --yaws=-12,30)
  python -m forja animar  modelo.yaml --anim reposo [--yaw 35 --pitch 15]
  python -m forja texto   modelo.yaml [--zona x0,y0,x1,y1]
  python -m forja paleta  modelo.yaml
  python -m forja escena  escena.yaml [--escala 3]
  python -m forja efecto  efecto.yaml

Con una biblioteca de objetos se agrega --objeto nombre.

Cada corrida guarda sus imágenes en salida/<modelo>/ con un número de versión y una copia del YAML,
para poder comparar contra versiones anteriores.
"""
import argparse
import json
import os
import shutil
import sys

from . import revisar, vistas
from .modelo import Modelo
from .render import renderizar


def _carpeta(modelo, ruta_yaml, base='salida'):
    d = os.path.join(base, modelo.nombre.lower().replace(' ', '_'))
    os.makedirs(os.path.join(d, 'historial'), exist_ok=True)
    n = 1 + max([int(f[:3]) for f in os.listdir(d) if f[:3].isdigit()] + [0])
    shutil.copy(ruta_yaml, os.path.join(d, 'historial', f'{n:03d}.yaml'))
    return d, n


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(prog='forja')
    ap.add_argument('orden', choices=['hoja', 'giro', 'animar', 'texto', 'paleta', 'escena', 'efecto'])
    ap.add_argument('modelo')
    ap.add_argument('--yaw', type=float)
    ap.add_argument('--pitch', type=float)
    ap.add_argument('--anim')
    ap.add_argument('--cuadro', type=int, default=0)
    ap.add_argument('--yaws', default='0,45,90,135,180,225,270,315')
    ap.add_argument('--ref')
    ap.add_argument('--zona')
    ap.add_argument('--salida', default='salida')
    ap.add_argument('--objeto')
    ap.add_argument('--escala', type=int, default=3)
    a = ap.parse_args(argv)

    if a.orden == 'escena':
        from .escena import componer
        im, d = componer(a.modelo)
        carpeta = os.path.join(a.salida, 'escenas')
        os.makedirs(carpeta, exist_ok=True)
        n = 1 + max([int(f[:3]) for f in os.listdir(carpeta) if f[:3].isdigit()] + [0])
        ruta = os.path.join(carpeta, f"{n:03d}_{d.get('nombre', 'escena').lower()}.png")
        im.save(ruta.replace('.png', '_x1.png'))
        im.resize((im.width * a.escala, im.height * a.escala), 0).save(ruta)
        print('Escena:', ruta)
        return

    if a.orden == 'efecto':
        from . import efectos
        spec = efectos.cargar(a.modelo)
        fr = efectos.cuadros(spec)
        nombre = os.path.splitext(os.path.basename(a.modelo))[0]
        carpeta = os.path.join(a.salida, 'efectos', nombre)
        os.makedirs(carpeta, exist_ok=True)
        n = 1 + max([int(f[:3]) for f in os.listdir(carpeta) if f[:3].isdigit()] + [0])
        pre = os.path.join(carpeta, f'{n:03d}')
        rgbas = [x for x, _ in fr]
        vistas.tira(rgbas, 1).save(pre + '_hoja_x1.png')
        vistas.tira(rgbas, 3, vistas.FONDOS['noche'], 4).save(pre + '_tira_noche.png')
        vistas.tira(rgbas, 3, vistas.FONDOS['banquete'], 4).save(pre + '_tira_banquete.png')
        import numpy as np
        brillos = []
        for _, b in fr:
            im = np.zeros(b.shape + (4,), np.uint8)
            im[b] = (255, 255, 255, 255)
            brillos.append(im)
        vistas.tira(brillos, 1).save(pre + '_brillo_x1.png')
        vistas.gif(rgbas, pre + '.gif', spec.get('fps', 20), 4, vistas.FONDOS['noche'])
        colores = {tuple(px) for x in rgbas for px in x[x[..., 3] > 0][:, :3].tolist()}
        print(f'{len(rgbas)} cuadros, {len(colores)} colores. Tira: {pre}_tira_noche.png')
        return

    m = Modelo(a.modelo, a.objeto)
    d, n = _carpeta(m, a.modelo, a.salida)
    pre = os.path.join(d, f'{n:03d}')

    if a.orden == 'hoja':
        r = renderizar(m, a.yaw, a.pitch, a.anim, a.cuadro)
        inf = revisar.revisar(r)
        vistas.imagen(r.rgba).save(pre + '_sprite.png')
        titulo = f'{m.nombre} v{n:03d} · yaw {r.yaw:g} · pitch {r.pitch:g} · {a.anim or "pose base"} {a.cuadro}'
        vistas.hoja(r, inf, a.ref, titulo).save(pre + '_hoja.png')
        with open(pre + '_revision.json', 'w', encoding='utf-8') as f:
            json.dump(inf, f, ensure_ascii=False, indent=1)
        print(titulo)
        print(revisar.resumen(inf))
        print('Hoja:', pre + '_hoja.png')

    elif a.orden == 'giro':
        yaws = [float(x) for x in a.yaws.split(',')]
        rs = [renderizar(m, y, a.pitch, a.anim, a.cuadro) for y in yaws]
        vistas.tira([r.rgba for r in rs], 3, vistas.FONDOS['papel'], 6).save(pre + '_giro.png')
        vistas.tira([r.rgba for r in rs], 1).save(pre + '_giro_x1.png')
        for y, r in zip(yaws, rs):
            inf = revisar.revisar(r)
            print(f'yaw {y:g}: {inf["colores"]} colores, {len(inf["huerfanos"])} huérfanos, '
                  f'{len(inf["huecos_contorno"])} huecos, {len(inf["dientes"])} dientes')
        print('Giro:', pre + '_giro.png')

    elif a.orden == 'animar':
        if a.anim not in m.animaciones:
            sys.exit(f'No existe la animación "{a.anim}". Hay: {", ".join(m.animaciones)}')
        an = m.animaciones[a.anim]
        rs = [renderizar(m, a.yaw, a.pitch, a.anim, i) for i in range(an.get('cuadros', 1))]
        cuadros = [r.rgba for r in rs]
        vistas.tira(cuadros, 1).save(pre + f'_{a.anim}_hoja_x1.png')
        vistas.tira(cuadros, 3, vistas.FONDOS['papel'], 6).save(pre + f'_{a.anim}_tira.png')
        vistas.cebolla(cuadros, 3).save(pre + f'_{a.anim}_cebolla.png')
        vistas.gif(cuadros, pre + f'_{a.anim}.gif', an.get('fps', 8))
        c = revisar.comparar_cuadros(rs)
        print(json.dumps(c, ensure_ascii=False))
        print('Animación:', pre + f'_{a.anim}_tira.png')

    elif a.orden == 'texto':
        r = renderizar(m, a.yaw, a.pitch, a.anim, a.cuadro)
        zona = tuple(int(v) for v in a.zona.split(',')) if a.zona else None
        print(vistas.texto(r.rgba, zona))

    elif a.orden == 'paleta':
        vistas.muestras(m).save(pre + '_paleta.png')
        print('Paleta:', pre + '_paleta.png')


if __name__ == '__main__':
    main()
