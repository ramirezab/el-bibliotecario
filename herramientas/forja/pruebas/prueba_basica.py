import sys, time
sys.path.insert(0, '.')
from PIL import Image
from forja.modelo import Modelo
from forja.render import renderizar

d = {
  'lienzo': [64, 64], 'origen': [32, 58],
  'materiales': {
    'rojo': {'color': '#c8323c'},
    'azul': {'color': '#2b3170'},
    'oro': {'color': '#e8b04b', 'brillo': 0.08},
  },
  'huesos': [{'nombre': 'raiz'}],
  'piezas': [
    {'nombre': 'cuerpo', 'forma': 'caja', 'tam': [24, 20, 14], 'radio': 4, 'pos': [0, 10, 0], 'material': 'azul',
     'regiones': [{'tipo': 'franja', 'eje': 'y', 'desde': -3, 'hasta': -1, 'material': 'oro'}]},
    {'nombre': 'bola', 'forma': 'esfera', 'r': 12, 'pos': [0, 32, 0], 'material': 'rojo'},
    {'nombre': 'aro', 'forma': 'toro', 'R': 5, 'r': 1.2, 'pos': [0, 32, 12], 'material': 'oro'},
  ],
}
m = Modelo(d)
for yaw, pitch in [(0, 0), (35, 15)]:
    t = time.time()
    r = renderizar(m, yaw=yaw, pitch=pitch)
    print(yaw, pitch, 'ms', int((time.time() - t) * 1000), 'colores', len(r.paleta))
    Image.fromarray(r.rgba).resize((64 * 6, 64 * 6), Image.NEAREST).save(f'salida/basica_{yaw}.png')
