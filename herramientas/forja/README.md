# Forja: herramienta de pixel art

Forja es la herramienta con la que Claude dibuja, revisa y anima el arte de *El Bibliotecario*. No usa modelos que generan imágenes. Cada personaje, edificio o efecto se escribe como un archivo de texto con piezas, colores y huesos, y un motor en Python lo convierte en pixel art. Por eso:

- el mismo personaje sale idéntico desde cualquier ángulo y en cada cuadro de animación;
- cualquier parte se puede cambiar (el sombrero, un color, la pose) sin redibujar el resto;
- cada render pasa por una revisión automática que señala pixeles sueltos, huecos en el contorno, curvas con dientes, bandas de sombra y colores que no se distinguen.

![Teo en 8 ángulos, atacando y recibiendo un golpe](muestras/teo_angulos_y_animaciones.png)

![Escena de aldea generada con la herramienta](muestras/aldea.png)

![Efectos de ataque cuadro a cuadro](muestras/efectos.png)

![Teo ataca: personaje, tajo e impacto](muestras/teo_ataca.gif)

## Cómo funciona

1. **Modelo.** Cada pieza es una forma con volumen (esfera, elipsoide, cápsula, caja, cilindro, cono, toro o polígono extruido), pegada a un hueso. Las piezas de un mismo grupo se funden suavemente.
2. **Render.** El motor traza un rayo por cada pixel del tamaño final, sin suavizado. Calcula la luz por pasos de una rampa de color con giro de tono (las sombras se enfrían y las luces se calientan), oclusión, sombras proyectadas y brillos.
3. **Limpieza.** Quita pixeles sueltos y escaleras de un pixel, y une grupos de 1 o 2 pixeles al tono que los rodea.
4. **Líneas.** Dibuja un contorno exterior de 1 px y líneas interiores entre piezas que se tapan, con el color de la pieza de adelante.
5. **Calcas y retoques.** Detalles pintados a mano (boca, pecas) que cambian según el ángulo, y correcciones de pixel por cuadro.
6. **Revisión.** Una hoja con la vista ampliada y las marcas de los problemas, el sprite sobre varios fondos, la silueta, el mapa de valores, las piezas y los pasos de luz.

## Uso

Requiere Python 3.12 con `numpy`, `Pillow` y `PyYAML`. Desde `herramientas/forja/`:

```bash
python -m forja hoja personajes/teo.yaml
```

| Orden | Para qué sirve |
|---|---|
| `hoja modelo.yaml [--yaw --pitch --anim --cuadro --ref imagen]` | Render con hoja de revisión e informe de problemas |
| `giro modelo.yaml [--yaws 0,45,90,...]` | El modelo desde varios ángulos (con negativos: `--yaws=-12,30`) |
| `animar modelo.yaml --anim nombre` | Tira de cuadros, papel cebolla, GIF y control de parpadeo |
| `texto modelo.yaml [--zona x0,y0,x1,y1]` | El sprite como letras, para leer y corregir pixeles exactos |
| `paleta modelo.yaml` | Las rampas de color de todos los materiales |
| `escena escena.yaml` | Compone un escenario: suelo, objetos, bosque repartido y sombras |
| `efecto efecto.yaml` | Un efecto de combate cuadro a cuadro, más su máscara de brillo |

A los archivos que son bibliotecas de objetos se les agrega `--objeto nombre`. Cada corrida queda en `salida/<modelo>/` con número de versión y una copia del archivo usado, para comparar contra versiones anteriores.

## Qué contiene

| Carpeta | Contenido |
|---|---|
| `forja/` | El motor: `modelo`, `render`, `sdf` (formas), `color` (rampas en OKLab), `revisar`, `vistas`, `baldosas`, `escena`, `efectos` |
| `personajes/` | Teo, con postura base, reposo, ataque y golpe |
| `mundo/` | Casa, pino, roble, biblioteca de objetos (barril, caja, rocas, tocón, cerca, arbusto, heno) y la escena de la aldea |
| `efectos/` | Tajo de pluma, impacto, Gota de Tinta, Réplica Perfecta, Subrayar y chispa de Pavesa |
| `muestras/` | Imágenes de ejemplo |

## Cámaras

- **Combate:** ortográfica con giro (`yaw`) e inclinación (`pitch`). Teo usa yaw 35 y pitch 12.
- **Mundo:** oblicua (`proyeccion: oblicua`). El suelo se ve desde arriba sin deformar y los objetos casi de frente (`alto: 1.0`, `fondo: 0.55`), como en los juegos de aldea cenitales.

## Formato del modelo (resumen)

```yaml
nombre: Teo
lienzo: [112, 124]          # tamaño del sprite
origen: [56, 116]           # pixel donde cae el punto entre los pies
camara: {yaw: 35, pitch: 12}
materiales:
  abrigo: {color: '#2f3680'}               # rampa de 5 tonos generada
  ojo: {colores: [...], plano: true, brillo: 0.3}
huesos:
  - {nombre: hombro, padre: torso, pos: [11, 15, 0], espejo: true}   # crea hombro.i y hombro.d
piezas:
  - {nombre: manga, hueso: hombro, forma: capsula, a: [0, 1, 0], b: [0, -8, 0], ra: 3.4, rb: 3, material: abrigo}
    # regiones: franja, caja, esfera, semiespacio, cuadros, rayas, ladrillos, ruido
    # rugosidad: {escala, fuerza} para follaje y rocas
pose_base: {codo.d: [-60, 0, 0]}
animaciones:
  reposo: {cuadros: 8, pose: {torso: {pos: [0, 'floor(0.5 + 0.9*sin(tau*t))', 0]}}}
  ataque: {cuadros: 10, bucle: false, claves: [{t: 0, pose: {}}, {t: 0.3, pose: {...}}]}
```

## Límites actuales

- El acabado todavía no iguala a un pixel artista profesional en caras y telas. Para eso están las calcas y los retoques de pixel, que hay que ir afinando a mano.
- Los efectos son la forma en pixel. El resplandor se agrega en el motor del juego usando la máscara de brillo que exporta cada efecto.
- Las baldosas exportables por esquinas (`juego_de_esquinas`) existen, pero todavía no hay exportación directa a Godot.
