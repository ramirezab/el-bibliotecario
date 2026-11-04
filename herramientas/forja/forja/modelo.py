"""Modelo: carga el YAML de un personaje u objeto y arma la escena para una pose.

Convenciones
- Unidades del modelo = pixeles a escala 1. Y hacia arriba, el personaje mira hacia +Z.
- El origen (0, 0, 0) es el punto entre los pies; ahí gira la cámara.
- Un hueso o pieza con `espejo: true` se duplica: `.i` (lado +X tal como se escribió) y `.d` (reflejado).
- Los ángulos van en grados [x, y, z]; se aplican en orden X, luego Y, luego Z.
"""
import math

import numpy as np
import yaml

from . import color
from .sdf import FORMAS

S = np.diag([-1.0, 1, 1, 1])
RESERVADAS = {'nombre', 'hueso', 'forma', 'pos', 'rot', 'material', 'grupo', 'suave', 'op', 'espejo',
              'sin_linea', 'regiones', 'sin_contorno', 'oculta'}


def rot(e):
    x, y, z = np.radians(np.asarray(e, float))
    cx, sx, cy, sy, cz, sz = np.cos(x), np.sin(x), np.cos(y), np.sin(y), np.cos(z), np.sin(z)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    M = np.eye(4)
    M[:3, :3] = Rz @ Ry @ Rx
    return M


def tras(v):
    M = np.eye(4)
    M[:3, 3] = v
    return M


_ENTORNO = {k: getattr(math, k) for k in ('sin', 'cos', 'pi', 'tau', 'floor', 'exp', 'sqrt')}
_ENTORNO['abs'] = abs
_ENTORNO['min'] = min
_ENTORNO['max'] = max


def _valor(v, t):
    """Un número o una expresión en función de la fase t (0..1), p. ej. '4*sin(tau*t)'."""
    if isinstance(v, str):
        return float(eval(v, {'__builtins__': {}}, dict(_ENTORNO, t=t)))
    return float(v)


def _vec(v, t=0.0):
    return np.array([_valor(x, t) for x in v], float)


class Material:
    def __init__(self, nombre, d, tinta):
        self.nombre = nombre
        if 'colores' in d:
            self.colores = list(d['colores'])
        else:
            self.colores = color.rampa(d['color'], d.get('pasos', 5), d.get('indice', 2), d.get('dL', 0.105),
                                       d.get('giro', 12.0), croma=d.get('croma', 1.0))
        n = len(self.colores)
        self.umbrales = d.get('umbrales') or list(np.linspace(0.3, 0.92, n - 1)) if n > 1 else []
        if n == 5 and not d.get('umbrales'):
            self.umbrales = [0.30, 0.50, 0.80, 0.95]
        self.brillo = d.get('brillo', 0.0)
        self.dither = d.get('dither', 0.0)
        self.plano = d.get('plano', False)
        self.linea = d.get('linea') or color.mezclar(self.colores[0], tinta, 0.5)
        self.contorno = d.get('contorno')
        self.textura = d.get('textura')


class Modelo:
    def __init__(self, ruta_o_dict, objeto=None):
        if isinstance(ruta_o_dict, dict):
            d = ruta_o_dict
        else:
            with open(ruta_o_dict, encoding='utf-8') as f:
                d = yaml.safe_load(f)
        if 'objetos' in d:
            # Biblioteca: varios objetos que comparten materiales, cámara y luz
            if objeto not in d['objetos']:
                raise ValueError(f'Este archivo es una biblioteca; elige un objeto: {", ".join(d["objetos"])}')
            base = {k: v for k, v in d.items() if k != 'objetos'}
            base.update(d['objetos'][objeto])
            base['nombre'] = f"{d.get('nombre', 'modelo')}_{objeto}"
            d = base
        self.d = d
        self.nombre = d.get('nombre', 'modelo')
        self.lienzo = tuple(d.get('lienzo', [96, 112]))
        self.origen = tuple(d.get('origen', [self.lienzo[0] / 2, self.lienzo[1] - 6]))
        self.escala = d.get('escala', 1.0)
        self.camara = {'yaw': 0.0, 'pitch': 0.0, **d.get('camara', {})}
        self.luz = np.asarray(d.get('luz', [-0.55, 0.7, 0.5]), float)
        self.borde_luz = d.get('borde_luz', 0.0)
        self.sombras = d.get('sombras', True)
        self.tinta = d.get('tinta', '#1a1220')
        self.contorno = d.get('contorno', 'tinta')
        self.umbral_linea = d.get('umbral_linea', 2.5)
        self.materiales = {}
        for nombre, md in d.get('materiales', {}).items():
            self.materiales[nombre] = Material(nombre, md, self.tinta)
        self.lista_mat = list(self.materiales)
        self._armar_huesos(d.get('huesos', [{'nombre': 'raiz'}]))
        self._armar_piezas(d.get('piezas', []))
        self.calcas = self._armar_calcas(d.get('calcas', []))
        self.poses = d.get('poses', {})
        self.animaciones = d.get('animaciones', {})
        self.retoques = d.get('retoques', {})
        self.grupos_cfg = d.get('grupos', {})

    # ---------------------------------------------------------------- huesos
    def _armar_huesos(self, lista):
        self.huesos, self.orden, self.espejados = {}, [], set()
        for h in lista:
            nombre, padre = h['nombre'], h.get('padre')
            if padre is not None and padre not in self.espejados and padre not in self.huesos:
                raise ValueError(f'El hueso "{nombre}" usa el padre "{padre}", que no está definido antes.')
            if h.get('espejo') or padre in self.espejados:
                self.espejados.add(nombre)
                for lado in ('i', 'd'):
                    p = f'{padre}.{lado}' if padre in self.espejados else padre
                    n = f'{nombre}.{lado}'
                    self.huesos[n] = dict(h, nombre=n, padre=p, lado=lado, base=nombre)
                    self.orden.append(n)
            else:
                self.huesos[nombre] = dict(h, lado=None, base=nombre)
                self.orden.append(nombre)

    def matrices(self, pose, t=0.0):
        W = {}
        for n in self.orden:
            h = self.huesos[n]
            prot, ppos = np.zeros(3), np.zeros(3)
            for clave in {n, h['base']}:
                r_, p_ = _como_dict(pose.get(clave), t)
                prot, ppos = prot + r_, ppos + p_
            L = tras(_vec(h.get('pos', [0, 0, 0])) + ppos) @ rot(h.get('rot', [0, 0, 0])) @ rot(prot)
            if h['lado'] == 'd':
                L = S @ L @ S
            W[n] = (W[h['padre']] if h.get('padre') else np.eye(4)) @ L
        return W

    # ---------------------------------------------------------------- piezas
    def _armar_piezas(self, lista):
        self.piezas = []
        for pz in lista:
            if pz.get('oculta'):
                continue
            hueso = pz.get('hueso', self.orden[0])
            if pz['forma'] not in FORMAS:
                raise ValueError(f'Pieza "{pz.get("nombre")}": forma desconocida "{pz["forma"]}". '
                                 f'Opciones: {", ".join(FORMAS)}')
            if pz.get('material') not in self.materiales:
                raise ValueError(f'Pieza "{pz.get("nombre")}": material "{pz.get("material")}" no definido.')
            if hueso in self.espejados or pz.get('espejo'):
                for lado in ('i', 'd'):
                    hb = f'{hueso}.{lado}' if hueso in self.espejados else hueso
                    self.piezas.append(self._pieza(pz, hb, lado))
            else:
                if hueso not in self.huesos:
                    raise ValueError(f'Pieza "{pz.get("nombre")}": hueso "{hueso}" no existe.')
                self.piezas.append(self._pieza(pz, hueso, None))

    def _pieza(self, pz, hueso, lado):
        nombre = pz.get('nombre', pz['forma']) + (f'.{lado}' if lado else '')
        grupo = pz.get('grupo', pz.get('nombre', nombre))
        if lado:
            grupo = f'{grupo}.{lado}'
        L = tras(pz.get('pos', [0, 0, 0])) @ rot(pz.get('rot', [0, 0, 0]))
        if lado == 'd':
            L = S @ L @ S
        params = {k: v for k, v in pz.items() if k not in RESERVADAS}
        regiones = []
        for r in pz.get('regiones', []):
            if r.get('material') not in self.materiales:
                raise ValueError(f'Región de "{nombre}": material "{r.get("material")}" no definido.')
            regiones.append(r)
        return dict(nombre=nombre, base=pz.get('nombre', pz['forma']), hueso=hueso, local=L, forma=pz['forma'],
                    params=params, material=self.lista_mat.index(pz['material']), grupo=grupo,
                    suave=pz.get('suave', 0.0), op=pz.get('op', 'union'), sin_linea=pz.get('sin_linea', False),
                    regiones=regiones, espejada=(lado == 'd'))

    def _armar_calcas(self, lista):
        salida = []
        for c in lista:
            lados = ('i', 'd') if c.get('espejo') or self._pieza_espejada(c['pieza']) else (None,)
            for lado in lados:
                pieza = c['pieza'] + (f'.{lado}' if lado else '')
                salida.append(dict(c, pieza=pieza, espejada=(lado == 'd')))
        return salida

    def _pieza_espejada(self, base):
        return any(p['base'] == base and p['nombre'].endswith(('.i', '.d')) for p in self.piezas)

    # ---------------------------------------------------------------- escena
    def escena(self, pose=None, t=0.0):
        """Devuelve las piezas con su matriz de mundo para una pose dada (sumada a `pose_base`)."""
        pose = _sumar_poses(self.d.get('pose_base', {}), pose or {}, t)
        W = self.matrices(pose, t)
        grupos, salida = {}, []
        for i, p in enumerate(self.piezas):
            M = W[p['hueso']] @ p['local']
            inv = np.linalg.inv(M)
            fdist, fenv = FORMAS[p['forma']]
            c_loc, r = fenv(p['params'])
            c_mundo = (M @ np.append(c_loc, 1))[:3]
            rug = p['params'].get('rugosidad', {}).get('fuerza', 0)
            item = dict(p, M=M, inv=inv, fdist=fdist, centro=c_mundo, radio=float(r) + 0.5 + rug)
            salida.append(item)
            grupos.setdefault(p['grupo'], []).append(len(salida) - 1)
        lista_grupos = []
        for g, idx in grupos.items():
            k = max([salida[i]['suave'] for i in idx] + [self.grupos_cfg.get(g.split('.')[0], {}).get('suave', 0)])
            lista_grupos.append(dict(nombre=g, piezas=idx, suave=k))
        return salida, lista_grupos

    def pose_de(self, anim=None, cuadro=0):
        """Pose (diccionario de huesos) y fase t para un cuadro de una animación, o la pose con ese nombre."""
        if not anim:
            return {}, 0.0
        if anim in self.poses and anim not in self.animaciones:
            return self.poses[anim], 0.0
        a = self.animaciones[anim]
        n = a.get('cuadros', 1)
        t = cuadro / n if a.get('bucle', True) else (cuadro / max(n - 1, 1))
        if 'pose' in a:
            return a['pose'], t
        claves = sorted(a['claves'], key=lambda k: k['t'])
        if t <= claves[0]['t']:
            return claves[0]['pose'], t
        for k0, k1 in zip(claves, claves[1:]):
            if k0['t'] <= t <= k1['t']:
                u = (t - k0['t']) / max(k1['t'] - k0['t'], 1e-9)
                if k1.get('curva', 'suave') == 'suave':
                    u = u * u * (3 - 2 * u)
                return _mezclar_poses(k0['pose'], k1['pose'], u, t), t
        return claves[-1]['pose'], t


def _como_dict(v, t):
    if v is None:
        return np.zeros(3), np.zeros(3)
    if isinstance(v, dict):
        return _vec(v.get('rot', [0, 0, 0]), t), _vec(v.get('pos', [0, 0, 0]), t)
    return _vec(v, t), np.zeros(3)


def _sumar_poses(a, b, t):
    """Pose b encima de la pose a: rotaciones y desplazamientos se suman hueso por hueso."""
    salida = {}
    for k in set(a) | set(b):
        ra, pa = _como_dict(a.get(k), t)
        rb, pb = _como_dict(b.get(k), t)
        salida[k] = {'rot': list(ra + rb), 'pos': list(pa + pb)}
    return salida


def _mezclar_poses(a, b, u, t):
    salida = {}
    for k in set(a) | set(b):
        ra, pa = _como_dict(a.get(k), t)
        rb, pb = _como_dict(b.get(k), t)
        salida[k] = {'rot': list(ra * (1 - u) + rb * u), 'pos': list(pa * (1 - u) + pb * u)}
    return salida
