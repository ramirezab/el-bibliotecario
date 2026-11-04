"""Física de la ropa: telas y cadenas con peso que se mueven como consecuencia del esqueleto.

Las capas y mantos son mallas de puntos con masa colgadas de su borde de arriba; las puntas de capucha, trapos
y colas son cadenas colgadas de un hueso. En cada cuadro el esqueleto se mueve (lo que dicen las claves) y la
ropa lo sigue sola: tiene inercia, gravedad, viento, choca con el cuerpo y un resorte suave la devuelve a su
forma de diseño. Nada de la ropa se anima a mano.

Se simula en el espacio del modelo, así que el resultado no depende de la cámara. Los ciclos (reposo, caminar)
se simulan varias vueltas para que el cuadro final empalme con el primero; las animaciones de una sola vez
empiezan con la ropa ya asentada.

  fisica:
    gravedad: 600            # unidades del modelo por segundo²
    pasos: 8                 # subpasos por cuadro
    viento: {dir: [-1, 0, -0.4], fuerza: 60, rafaga: 0.5, ciclos: 1}
    colisiones:              # cápsulas del cuerpo: de a a b (b puede ir pegado a otro hueso), radio r
      - {nombre: torso, hueso: torso, a: [0, 0, 0], b: [0, 20, 0], r: 7}
      - {nombre: brazo, hueso: hombro, a: [0, 0, 0], b: [codo, 0, 0, 0], r: 4, espejo: true}
    telas:
      - {pieza: capa_larga, rigidez: 0.05, amortiguar: 0.04, choca: [torso, brazo.i]}
    cadenas:
      - {nombre: capucha, huesos: [capucha1, capucha2, capucha3], punta: [0, -4.5, -0.8], rigidez: 0.06}
"""
import math

import numpy as np

from .modelo import _sumar_poses


class _Cuerpo:
    """Puntos con masa: los `fijos` siguen al esqueleto, el resto se simula."""

    def __init__(self, nombre, tipo, cfg, reposo, fijos, aristas):
        self.nombre, self.tipo, self.cfg = nombre, tipo, cfg
        self.fijos = np.asarray(fijos, bool)
        self.libres = ~self.fijos
        aristas = np.asarray(aristas, int).reshape(-1, 2)
        self.i, self.j = aristas[:, 0], aristas[:, 1]
        self.largo = np.linalg.norm(reposo[self.j] - reposo[self.i], axis=1)
        self.rigidez = cfg.get('rigidez', 0.05)
        self.amortiguar = cfg.get('amortiguar', 0.05)
        self.gravedad = cfg.get('gravedad', 1.0)
        self.viento = cfg.get('viento', 1.0)
        self.grosor = cfg.get('grosor', 0.6)
        self.max_desvio = cfg.get('max_desvio', 30.0)
        self.choca = cfg.get('choca')
        self.previo = {}


def rejilla_campana(p):
    """Los puntos de una campana en su marco: aros de arriba abajo × 2·ondas ángulos (bordes y centros de cada
    paño). Devuelve (puntos R×K×3, radios R×K, ángulos K)."""
    aros = p['aros']
    n = p.get('ondas', 8)
    r = p.get('redondeo', 1.5)
    K = 2 * n
    ang = math.radians(p.get('fase', 0)) + np.arange(K) * math.tau / K
    caidas = [p['caidas'][i % len(p['caidas'])] for i in range(n)] if 'caidas' in p else [p.get('caida', 2.0)] * n
    puntas = p.get('puntas', False)
    filas, radios = [], []
    for y, rx, rz in aros[:-1]:
        filas.append(np.stack([rx * np.sin(ang), np.full(K, float(y)), rz * np.cos(ang)], 1))
        radios.append(np.full(K, float(r)))
    y, rx, rz = aros[-1]
    ruedo, rr = [], []
    for k, a in enumerate(ang):
        if k % 2 == 0:
            ruedo.append([rx * math.sin(a), y, rz * math.cos(a)])
            rr.append(0.3 if puntas else r * 0.6)
        else:
            f = 1.04 if puntas else 1.0
            ruedo.append([rx * f * math.sin(a), y - caidas[k // 2], rz * f * math.cos(a)])
            rr.append(0.05 if puntas else r * 0.6)
    filas.append(np.array(ruedo, float))
    radios.append(np.array(rr, float))
    return np.stack(filas), np.stack(radios), ang


def paño_abierto(p, ang, i):
    """El paño i cae en la abertura de adelante (no se dibuja ni se cose con sus vecinos)."""
    abertura = p.get('abertura', 0)
    am = ang[2 * i + 1]
    return bool(abertura) and abs((math.degrees(am) + 180) % 360 - 180) < abertura / 2


class Fisica:
    def __init__(self, dib):
        d = dib.d.get('fisica') or {}
        self.dib = dib
        self.g = float(d.get('gravedad', 600.0))
        self.pasos = int(d.get('pasos', 8))
        self.iteraciones = int(d.get('iteraciones', 5))
        self.viento = d.get('viento')
        self.colisiones = []
        for c in d.get('colisiones', []):
            lados = ('i', 'd') if c.get('espejo') else (None,)
            for lado in lados:
                nombre = c.get('nombre', c['hueso']) + (f'.{lado}' if lado else '')
                self.colisiones.append(dict(c, nombre=nombre, lado=lado))
        self.cuerpos = []
        for t in d.get('telas', []):
            self.cuerpos.append(self._tela(t))
        for c in d.get('cadenas', []):
            self.cuerpos.append(self._cadena(c))

    # ------------------------------------------------------------------ armado
    def _pieza(self, nombre):
        pz = next((q for q in self.dib.piezas if q['nombre'] == nombre), None)
        if pz is None or pz['forma'] != 'campana':
            raise ValueError(f'fisica.telas: "{nombre}" no es una pieza con forma campana.')
        if pz['lado']:
            raise ValueError(f'fisica.telas: la campana "{nombre}" no puede llevar espejo.')
        return pz

    def _tela(self, cfg):
        pz = self._pieza(cfg['pieza'])
        G, _, ang = rejilla_campana(pz['p'])
        R, K, _ = G.shape
        idx = np.arange(R * K).reshape(R, K)
        n = K // 2
        abiertos = {i for i in range(n) if paño_abierto(pz['p'], ang, i)}

        def cosida(k0, k1):
            # una arista horizontal o diagonal entre las columnas k0 y k1 = k0+1 existe si su paño no está abierto
            return (k0 // 2) not in abiertos

        aristas = []
        for r in range(R):
            for k in range(K):
                k1 = (k + 1) % K
                if cosida(k, k1):
                    aristas.append((idx[r, k], idx[r, k1]))
                if r + 1 < R:
                    aristas.append((idx[r, k], idx[r + 1, k]))
                    if cosida(k, k1):
                        aristas.append((idx[r, k], idx[r + 1, k1]))
                        aristas.append((idx[r, k1], idx[r + 1, k]))
                if r + 2 < R:
                    aristas.append((idx[r, k], idx[r + 2, k]))
        fijos = np.zeros(R * K, bool)
        fijos[:K] = True
        c = _Cuerpo(cfg['pieza'], 'tela', cfg, G.reshape(-1, 3), fijos, aristas)
        c.pieza, c.local, c.forma = pz, G.reshape(-1, 3), (R, K)
        return c

    def _cadena(self, cfg):
        huesos = cfg['huesos']
        W = self.dib.matrices(_sumar_poses(self.dib.d.get('pose_base', {}), {}, 0.0), 0.0)
        c = _Cuerpo(cfg.get('nombre', huesos[0]), 'cadena', cfg, self._puntos_cadena(cfg, W),
                    [True] + [False] * len(huesos), [(k, k + 1) for k in range(len(huesos))])
        c.huesos, c.punta = huesos, np.asarray(cfg.get('punta', [0, -4, 0]), float)
        return c

    @staticmethod
    def _puntos_cadena(cfg, W):
        huesos = cfg['huesos']
        P = [W[h][:3, 3] for h in huesos]
        P.append((W[huesos[-1]] @ np.append(np.asarray(cfg.get('punta', [0, -4, 0]), float), 1))[:3])
        return np.array(P)

    # ------------------------------------------------------------------ objetivos y colisiones de un cuadro
    def objetivos(self, W):
        salida = []
        for c in self.cuerpos:
            if c.tipo == 'tela':
                M = W[c.pieza['hueso']] @ c.pieza['local']
                salida.append(c.local @ M[:3, :3].T + M[:3, 3])
            else:
                salida.append(self._puntos_cadena(c.cfg, W))
        return salida

    def capsulas(self, W):
        caps = {}
        for c in self.colisiones:
            h = self.dib.hueso_lado(c['hueso'], c['lado'])
            a = np.asarray(c.get('a', [0, 0, 0]), float)
            b = c.get('b', c.get('a', [0, 0, 0]))
            if c['lado'] == 'd':
                a = a * [-1, 1, 1]
            A = (W[h] @ np.append(a, 1))[:3]
            if isinstance(b[0], str):
                hb = self.dib.hueso_lado(b[0], c['lado'])
                bb = np.asarray(b[1:4], float) * ([-1, 1, 1] if c['lado'] == 'd' else 1)
                B = (W[hb] @ np.append(bb, 1))[:3]
            else:
                bb = np.asarray(b, float) * ([-1, 1, 1] if c['lado'] == 'd' else 1)
                B = (W[h] @ np.append(bb, 1))[:3]
            caps[c['nombre']] = (A, B, float(c['r']))
        return caps

    # ------------------------------------------------------------------ simulación
    def _paso(self, c, x, xp, T, caps, h, tiempo):
        v = (x - xp) * (1 - c.amortiguar)
        xp[:] = x
        a = np.array([0.0, -self.g * c.gravedad, 0.0])
        x += v + a * h * h
        if self.viento and c.viento:
            vt = self.viento
            d = np.asarray(vt.get('dir', [-1, 0, 0]), float)
            d /= np.linalg.norm(d)
            fase = math.tau * vt.get('ciclos', 1) * tiempo - 0.09 * x[:, 1] + 0.05 * x[:, 0]
            f = vt.get('fuerza', 40) * (1 - vt.get('rafaga', 0.5) * (0.5 + 0.5 * np.sin(fase)))
            x += (f[:, None] * d) * c.viento * h * h
        x += (T - x) * c.rigidez
        x[c.fijos] = T[c.fijos]
        w = c.libres.astype(float)
        wi, wj = w[c.i], w[c.j]
        suma = np.maximum(wi + wj, 1e-9)
        cuantas = np.zeros(len(x))
        np.add.at(cuantas, c.i, 1)
        np.add.at(cuantas, c.j, 1)
        cuantas = np.maximum(cuantas, 1)[:, None]
        nombres = c.choca if c.choca is not None else list(caps)
        for _ in range(self.iteraciones):
            d = x[c.j] - x[c.i]
            L = np.linalg.norm(d, axis=1)
            k = ((L - c.largo) / np.maximum(L, 1e-9))[:, None] * d
            corr = np.zeros_like(x)
            np.add.at(corr, c.i, k * (wi / suma)[:, None])
            np.add.at(corr, c.j, -k * (wj / suma)[:, None])
            x += corr / cuantas * 1.6
            for nombre in nombres:
                A, B, r = caps[nombre]
                q = _mas_cercano(x, A, B)
                dq = x - q
                dist = np.linalg.norm(dq, axis=1)
                lim = r + c.grosor
                n = dq / np.maximum(dist, 1e-9)[:, None]
                dentro = dist < lim
                # La tela no se deja atravesar: si el hueso la cruzó desde el paso anterior, vuelve al lado en el
                # que estaba. Así un brazo que sube por debajo del manto lo levanta en vez de pasarlo.
                prev = c.previo.get(nombre)
                if prev is not None:
                    pd = np.linalg.norm(prev, axis=1)
                    cruzo = ((dq * prev).sum(1) < 0) & (pd < lim + 2.0)
                    n[cruzo] = prev[cruzo] / np.maximum(pd[cruzo], 1e-9)[:, None]
                    dentro |= cruzo
                dentro &= c.libres
                if dentro.any():
                    x[dentro] = q[dentro] + n[dentro] * lim
            x[c.fijos] = T[c.fijos]
        for nombre in nombres:
            A, B, r = caps[nombre]
            c.previo[nombre] = x - _mas_cercano(x, A, B)
        dev = x - T
        m = np.linalg.norm(dev, axis=1)
        lejos = m > c.max_desvio
        if lejos.any():
            x[lejos] = T[lejos] + dev[lejos] * (c.max_desvio / m[lejos])[:, None]

    def simular(self, Ws, fps, bucle, calentar=1.0):
        """Simula una secuencia de esqueletos (uno por cuadro) y devuelve, por cuadro, {cuerpo: puntos}."""
        n = len(Ws)
        T = [self.objetivos(W) for W in Ws]
        C = [self.capsulas(W) for W in Ws]
        x = [t.copy() for t in T[0]]
        xp = [t.copy() for t in T[0]]
        for c in self.cuerpos:
            c.previo = {}
        h = 1.0 / fps / self.pasos
        duracion = n / fps

        def correr(orden, guardar):
            nonlocal x, xp
            estados = []
            previo = orden[0]
            for f in orden:
                for s in range(1, self.pasos + 1):
                    u = s / self.pasos
                    caps = {k: tuple(C[previo][k][i] * (1 - u) + C[f][k][i] * u for i in range(2)) + (C[f][k][2],)
                            for k in C[f]}
                    tiempo = ((f - 1 + u) / fps) / max(duracion, 1e-9) if bucle else (f + u) / fps
                    for ci, c in enumerate(self.cuerpos):
                        Tc = T[previo][ci] * (1 - u) + T[f][ci] * u
                        self._paso(c, x[ci], xp[ci], Tc, caps, h, tiempo)
                previo = f
                if guardar:
                    estados.append({c.nombre: x[ci].copy() for ci, c in enumerate(self.cuerpos)})
            return estados

        if bucle:
            correr(list(range(n)) * 2, False)
            return correr(list(range(n)), True)
        correr([0] * max(int(calentar * fps), 1), False)
        return correr(list(range(n)), True)

    # ------------------------------------------------------------------ resultado sobre el esqueleto
    def aplicar(self, W, estado):
        """Gira los huesos de cada cadena para que pasen por los puntos simulados. Devuelve las telas."""
        telas = {}
        for c in self.cuerpos:
            P = estado[c.nombre]
            if c.tipo == 'tela':
                telas[c.nombre] = P.reshape(c.forma[0], c.forma[1], 3)
                continue
            K = self._puntos_cadena(c.cfg, W)
            for j, hueso in enumerate(c.huesos):
                R = _rotacion_entre(K[j + 1] - K[j], P[j + 1] - P[j])
                M = W[hueso].copy()
                M[:3, :3] = R @ M[:3, :3]
                M[:3, 3] = P[j]
                W[hueso] = M
        return telas


def _mas_cercano(x, A, B):
    ab = B - A
    t = np.clip(((x - A) @ ab) / max(ab @ ab, 1e-9), 0, 1)
    return A + t[:, None] * ab


def _rotacion_entre(a, b):
    a = a / max(np.linalg.norm(a), 1e-9)
    b = b / max(np.linalg.norm(b), 1e-9)
    v = np.cross(a, b)
    c = float(a @ b)
    if c < -0.9999:
        eje = np.cross(a, [1, 0, 0] if abs(a[0]) < 0.9 else [0, 1, 0])
        eje /= np.linalg.norm(eje)
        return 2 * np.outer(eje, eje) - np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx / (1 + c)
