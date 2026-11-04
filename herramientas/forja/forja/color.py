"""Color: conversiones sRGB <-> OKLab y rampas con giro de tono (reglas de Slynyrd y Arne)."""
import numpy as np


def hex_a_rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def rgb_a_hex(c):
    c = np.clip(np.round(np.asarray(c, float)), 0, 255).astype(int)
    return '#%02x%02x%02x' % tuple(c)


def _lineal(c):
    c = np.asarray(c, float) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _gamma(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055) * 255


_M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005]])
_M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                [1.9779984951, -2.4285922050, 0.4505937099],
                [0.0259040371, 0.7827717662, -0.8086757660]])
_M2i = np.array([[1, 0.3963377774, 0.2158037573],
                 [1, -0.1055613458, -0.0638541728],
                 [1, -0.0894841775, -1.2914855480]])
_M1i = np.array([[4.0767416621, -3.3077115913, 0.2309699292],
                 [-1.2684380046, 2.6097574011, -0.3413193965],
                 [-0.0041960863, -0.7034186147, 1.7076147010]])


def rgb_a_oklab(rgb):
    lms = np.cbrt(_lineal(rgb) @ _M1.T)
    return lms @ _M2.T


def _oklab_a_lineal(lab):
    return ((np.asarray(lab, float) @ _M2i.T) ** 3) @ _M1i.T


def oklab_a_rgb(lab):
    return _gamma(_oklab_a_lineal(lab))


def a_oklch(rgb):
    L, a, b = rgb_a_oklab(rgb)
    return L, float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)) % 360)


def desde_oklch(L, C, h):
    """Convierte OKLCH a sRGB bajando el croma hasta que el color quepa en la gama."""
    hr = np.radians(h)
    for _ in range(40):
        lin = _oklab_a_lineal([L, C * np.cos(hr), C * np.sin(hr)])
        if np.all(lin >= -1e-4) and np.all(lin <= 1 + 1e-4):
            break
        C *= 0.93
    return _gamma(lin)


def _girar(h, objetivo, maximo):
    delta = ((objetivo - h + 180) % 360) - 180
    return (h + np.sign(delta) * min(abs(delta), maximo)) % 360


def rampa(base, pasos=5, indice=2, dL=0.105, giro=12.0, calido=75.0, frio=285.0, croma=1.0):
    """Rampa de `pasos` colores alrededor de `base` (que queda en `indice`).

    Hacia la luz: más claro con pasos cada vez más cortos, tono hacia lo cálido.
    Hacia la sombra: más oscuro, tono hacia lo frío. El croma alcanza su pico cerca de la base.
    """
    L0, C0, h0 = a_oklch(hex_a_rgb(base))
    C0 *= croma
    salida = []
    for i in range(pasos):
        k = i - indice
        if k > 0:
            L = L0 + sum(dL * (0.82 ** j) for j in range(k))
            h = _girar(h0, calido, giro * k)
            C = C0 * max(0.45, 1 - 0.13 * k * k)
        elif k < 0:
            L = L0 + dL * 1.05 * k
            h = _girar(h0, frio, giro * -k)
            C = C0 * max(0.5, 1 - 0.07 * k * k) + 0.012 * -k
        else:
            L, h, C = L0, h0, C0
        salida.append(rgb_a_hex(desde_oklch(float(np.clip(L, 0.06, 0.98)), C, h)))
    return salida


def mezclar(c1, c2, t):
    """Mezcla en OKLab: t=0 da c1, t=1 da c2."""
    a, b = rgb_a_oklab(hex_a_rgb(c1)), rgb_a_oklab(hex_a_rgb(c2))
    return rgb_a_hex(oklab_a_rgb(a * (1 - t) + b * t))


def luminosidad(hexcol):
    return float(rgb_a_oklab(hex_a_rgb(hexcol))[0])
