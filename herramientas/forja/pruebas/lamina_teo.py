import sys
sys.path.insert(0, '.')
from PIL import Image, ImageDraw
from forja.modelo import Modelo
from forja.render import renderizar
from forja import vistas

m = Modelo('personajes/teo.yaml')
giro = [renderizar(m, y, 12).rgba for y in (0, 45, 90, 135, 180, 225, 270, 315)]
ataque = [renderizar(m, 35, 12, 'ataque', i).rgba for i in range(10)]
golpe = [renderizar(m, 35, 12, 'golpe', i).rgba for i in range(6)]
f = vistas._fuente(18)
filas = [('Mismo modelo en 8 ángulos', vistas.tira(giro, 3, (242, 232, 213), 0)),
         ('Ataque (10 cuadros)', vistas.tira(ataque, 2, (122, 68, 22), 0)),
         ('Recibe golpe (6 cuadros)', vistas.tira(golpe, 2, (24, 20, 38), 0))]
W = max(im.width for _, im in filas) + 40
H = sum(im.height + 40 for _, im in filas) + 50
out = Image.new('RGB', (W, H), (44, 42, 52))
d = ImageDraw.Draw(out)
d.text((20, 12), 'Forja · Teo, sprite de combate hecho con la herramienta', fill=(240, 230, 210), font=vistas._fuente(22))
y = 50
for t, im in filas:
    d.text((20, y), t, fill=(220, 210, 190), font=f)
    out.paste(im.convert('RGB'), (20, y + 28))
    y += im.height + 40
out.save('salida/lamina_teo.png')
print(out.size)
