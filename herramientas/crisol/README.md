# Crisol — generador local de pixel art guiado por Forja

Crisol hace en la computadora, sin servicios de internet, lo mismo que herramientas como PixelLab: un personaje en
pixel art visto desde varios ángulos y animado. La diferencia es de dónde sale la coherencia.

Un modelo de imágenes solo inventa cada cuadro por su cuenta. Así cambian la capucha, la cara y los colores entre
ángulos y entre cuadros, y eso fue lo que mató los intentos anteriores. En Crisol la estructura la pone **Forja**,
el modelo 3D con esqueleto y física de ropa. En cada ángulo y en cada cuadro de animación, el personaje es el mismo
modelo. El modelo de imágenes solo lo **repinta** en pixel art.

## Cómo funciona

1. **Guía (Forja).** Se dibuja al personaje en el ángulo y cuadro pedidos, centrado en un cuadrado de 1024 px.
   De ahí salen tres cosas:
   - el dibujo a color;
   - sus bordes;
   - su silueta.
2. **Repintado (Stable Diffusion XL).** Corre en la tarjeta de video y parte del dibujo a color (img2img).
   - El ajuste `pixel-art-xl` lo lleva a pixel art.
   - ControlNet de bordes sostiene la silueta.
   - La `fuerza` dice cuánto puede cambiar el dibujo: con poca se parece a Forja; con mucha inventa más.
   - La descripción incluye la vista ("back view…") y, de espaldas, se le prohíbe dibujar cara.
3. **Animación sin parpadeo** (`crisol/animar.py`).
   - Si el modelo pinta cada cuadro por su cuenta, los ojos, los pliegues y la textura "hierven": en el reposo de
     Teo cambiaba el 64 % de los pixeles de un cuadro al siguiente.
   - Por eso el modelo pinta **solo el cuadro clave**. Los demás cuadros se sacan **moviendo sus pixeles** con el
     movimiento de Forja (flujo óptico entre los dibujos de Forja, que son limpios y planos).
   - Cada pixel se busca primero en el cuadro clave y, si no está, en el cuadro anterior ya terminado.
   - Lo que aparece de nuevo (una parte que estaba tapada) se rellena con los vecinos si es poco. Si es más del 5 %
     del personaje, el modelo pinta ese cuadro y se toma de ahí.
   - Con esto, el reposo bajó a 26 % de pixeles cambiados por cuadro, menos que el 32 % del propio Forja reducido a
     la misma cuadrícula. Además, una animación de 32 cuadros cuesta una sola imagen del modelo.
4. **Limpieza a pixel art de verdad.**
   - Cada bloque de 8×8 px se vuelve un pixel: una cuadrícula de 128×128 (`pixeles.a_cuadricula`).
   - El fondo se quita con la silueta de Forja.
   - Se quitan de la orilla las celdas donde se coló el fondo blanco.
   - Se fija **una paleta común para todos los cuadros**: 32 colores sacados solo del personaje (k-means), para que
     los tonos no salten.
   - Se quitan los pixeles sueltos y se pone un contorno de 1 px.

## Instalación (una vez)

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu128
```

```bash
pip install -r herramientas/crisol/requirements.txt -r herramientas/forja/requirements.txt
```

La primera vez que corre baja los modelos de Hugging Face, unos 8 GB, a `~/.cache/huggingface`:

- `stabilityai/stable-diffusion-xl-base-1.0` (fp16);
- `madebyollin/sdxl-vae-fp16-fix`;
- `diffusers/controlnet-canny-sdxl-1.0-small`;
- `nerijs/pixel-art-xl`.

Funciona con 8 GB de video y 16 GB de RAM:

- la descripción de cada vista se codifica una vez al cargar y los codificadores de texto se sueltan;
- lo demás (unos 5,6 GB) vive en la tarjeta.

Tarda de 20 a 40 s por imagen en una RTX 5050 Laptop. No se usa la descarga a CPU de `diffusers`: con poca RAM
libre hacía caer el proceso.

## Uso

Desde `herramientas/crisol/`:

```bash
python prueba_teo.py --fuerzas
```

Prueba 3 ángulos con 3 fuerzas distintas, para escoger la buena.

```bash
python prueba_teo.py reposo caminar ataque golpe
```

Hace a Teo en 8 ángulos y en las animaciones pedidas. Deja sprites, hojas de comparación y GIFs, e imprime
cuánto cambia cada animación por cuadro comparado con Forja.

Los resultados quedan en `salida/`, que no se sube a git. Lo que pinta el modelo se guarda en `salida/cache/`: si
se vuelve a pedir la misma imagen, no se vuelve a pintar.

## Código

| Archivo | Qué hace |
|---|---|
| `crisol/guias.py` | Dibuja la guía con Forja: dibujo, fondo blanco, bordes y silueta |
| `crisol/motor.py` | Carga SDXL, ControlNet y el ajuste de pixel art; `pintar()` repinta una guía |
| `crisol/animar.py` | Lleva el cuadro clave a los demás cuadros siguiendo el movimiento de Forja |
| `crisol/pixeles.py` | Cuadrícula, orilla, paleta común, pixeles sueltos y contorno |
| `prueba_teo.py` | La prueba con Teo, las hojas de comparación, los GIF y la medida de parpadeo |

## Lo que sigue

- **Ajustar** la fuerza, la cuadrícula y la paleta con las pruebas.
- **Entrenar un ajuste (LoRA) propio** con los sprites que se aprueben. Así el modelo aprende *nuestro* estilo
  y no el genérico de `pixel-art-xl`. Es la parte de "entrenarse": no se entrena desde cero, se le enseñan
  unos cuantos ejemplos buenos.
- **Exportar** las hojas de sprites en el mismo formato que Forja (`forja/juego.py`), para que la demo las cargue
  directamente.
