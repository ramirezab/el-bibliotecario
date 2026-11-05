"""Animación sin parpadeo: el modelo pinta el cuadro clave y los demás cuadros se sacan moviendo sus pixeles.

Cada cuadro de Forja dice cómo se movió el personaje. Ese movimiento (flujo óptico entre los dibujos de Forja, que
son limpios y planos) se aplica a lo ya pintado por Crisol. Así los ojos, los pliegues y la textura son los mismos
en todos los cuadros: solo se mueven.

Cada pixel de un cuadro se busca, en orden:
  1. en el cuadro clave (no se acumula error),
  2. en el cuadro anterior ya terminado (una pierna que apareció sigue igual en los siguientes),
  3. si queda hueco: pequeño, se rellena con los vecinos; grande, el modelo pinta ese cuadro y se toma de ahí.
"""
import cv2
import numpy as np
from PIL import Image

_DIS = None


def _flujo(desde, hacia):
    """Para cada pixel de `desde` (RGB), cuánto hay que moverse para encontrarlo en `hacia`."""
    global _DIS
    if _DIS is None:
        _DIS = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    a = cv2.cvtColor(np.asarray(desde), cv2.COLOR_RGB2GRAY)
    b = cv2.cvtColor(np.asarray(hacia), cv2.COLOR_RGB2GRAY)
    return _DIS.calc(a, b, None)


def traer(guia_origen, pintado_origen, mascara_origen, guia, mascara, tolerancia=24):
    """Lleva lo pintado en el cuadro de origen al cuadro `guia`. Devuelve (imagen movida, pixeles válidos).

    Un pixel vale solo si su origen cae dentro del personaje y en un color de Forja parecido; si no, es algo que
    en el origen estaba tapado."""
    f = _flujo(guia, guia_origen)
    h, w = f.shape[:2]
    xs, ys = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    mx, my = xs + f[..., 0], ys + f[..., 1]
    movido = cv2.remap(np.asarray(pintado_origen), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    origen = cv2.remap(np.asarray(guia_origen), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    dentro = cv2.remap(mascara_origen.astype(np.uint8), mx, my, cv2.INTER_NEAREST) > 0
    parecido = np.abs(origen.astype(int) - np.asarray(guia).astype(int)).max(-1) <= tolerancia
    return movido, dentro & parecido & mascara


def animacion(guias, mascaras, pintar_cuadro, clave=0, umbral=0.05, avisar=print):
    """Todos los cuadros de una animación.

    `guias`: dibujos de Forja (RGB, uno por cuadro); `mascaras`: siluetas; `pintar_cuadro(i)`: pide al modelo el
    cuadro i (solo se llama para el cuadro clave y para los que tengan un hueco mayor que `umbral`)."""
    clave_pint = np.asarray(pintar_cuadro(clave))
    out, generados = [], [clave]
    anterior = None
    orden = list(range(clave, len(guias))) + list(range(0, clave))
    hechos = {}
    for i in orden:
        g, m = guias[i], mascaras[i]
        if i == clave:
            hechos[i] = clave_pint
            anterior = i
            continue
        im, vale = traer(guias[clave], clave_pint, mascaras[clave], g, m)
        if anterior is not None and anterior != clave:
            im2, vale2 = traer(guias[anterior], hechos[anterior], mascaras[anterior], g, m)
            nuevo = vale2 & ~vale
            im[nuevo] = im2[nuevo]
            vale = vale | vale2
        hueco = m & ~vale
        frac = hueco.sum() / max(1, m.sum())
        if frac > umbral:
            propio = np.asarray(pintar_cuadro(i))
            im[hueco] = propio[hueco]
            generados.append(i)
        elif hueco.any():
            im = cv2.inpaint(im, hueco.astype(np.uint8) * 255, 5, cv2.INPAINT_TELEA)
        hechos[i] = im
        anterior = i
    avisar(f'cuadros pintados por el modelo: {sorted(generados)} de {len(guias)}')
    return [Image.fromarray(hechos[i]) for i in range(len(guias))], sorted(generados)
