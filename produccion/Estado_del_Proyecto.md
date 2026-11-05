# Estado del proyecto (5 de noviembre de 2026)

Nota para seguir el trabajo en otra computadora. Si eres Claude empezando una sesión nueva: lee esto antes de tocar el arte, porque aquí está lo que el autor ya aprobó y lo que rechazó.

## Qué hay en el repositorio

| Parte | Dónde | Estado |
|---|---|---|
| Biblia del juego (historia, lore, mundo, guion, sistemas, arte) | `01_CANON.md`, `historia/`, `lore/`, `mundo/`, `guion/`, `sistemas/`, `arte/` | Completa, unas 200 000 palabras |
| Prototipo de combate | `prototipo/index.html` | Al autor le gustaron las mecánicas y los efectos; el arte en pixel no |
| Demo jugable del Oasis de Sal | `demo/index.html` | Exploración, 3 NPC, páginas, emboscada y pelea con la Réplica. Arte hecho con Forja |
| Forja, la herramienta de arte | `herramientas/forja/` | Motor de pixel art, motor de tinta (pluma), física de ropa, animación por capas y exportador para el juego |
| Referencias de arte | `arte/referencias/` | El dibujo del autor y tres capturas de inspiración |
| Libro de lore *Mil Años bajo la Luna* | `libro/` | Completo: prólogo, 16 capítulos y apéndices, unas 83.000 palabras. Se regala al completar el juego al 100 %. Su guía de estilo está en `libro/GUIA_DE_ESCRITURA.md` |

## Cómo correr todo

Requiere Python 3.12.

```bash
pip install -r herramientas/forja/requirements.txt
```

- **Jugar la demo en local:** doble clic en `jugar_demo_local.bat` (abre `http://localhost:8765/demo/index.html`). El autor prefiere probar en local, no en GitHub Pages.
- **Volver a dibujar el arte de la demo:** desde `herramientas/forja/`, `python demo/construir.py` (todo) o por partes: `personajes`, `pavesa`, `escarabajo`, `elementos`, `suelo`, `fondo`. Después `python demo/armar_html.py` vuelve a armar `demo/index.html` a partir del prototipo y de `demo/exploracion.js`.
- **Revisar un modelo:** `python -m forja hoja personajes/caminante.yaml` y `python -m forja animar personajes/caminante.yaml --anim ataque`.

## Lo que el autor decidió sobre el arte

**Rechazado:**
- El pixel art armado con piezas en 3D (Teo "parecía un zombie").
- El estilo de tinta ilustrado de Forja, en todas sus versiones. Su última palabra: "no me gusta para nada el arte".
- Copiar los colores del Caballero de Hollow Knight: quería el estilo de dibujo, no esa paleta.
- Todas las caras de dolor probadas (le parecen caras de Mii de Nintendo). Sigue sin resolverse.

**Pedidos que siguen valiendo:**
- La consistencia entre ángulos y cuadros de animación es lo más importante.
- Cámara de exploración lejana: personajes chicos en un mundo amplio.
- Todo lo que se ve en el juego debe cargarse desde un modelo o archivo; nada de arte dibujado por el código del juego. Los efectos de combate le gustan como están.
- Animaciones extremadamente fluidas (20 a 24 cuadros por segundo) y con mucho movimiento.
- La ropa con física y pesos: el manto debe levantarse con el brazo y quedar siempre encima del hombro. La capucha tapa el pelo; solo se ve el flequillo.
- El protagonista actual es un caminante del desierto con capucha verde oscuro y pelo café (`herramientas/forja/personajes/caminante.yaml`). Le pareció "más o menos".

## El generador local "como PixelLab": Crisol

El autor quiere poder hacer en local lo mismo que PixelLab: personajes, ángulos, animaciones, objetos y escenarios en pixel art de alta calidad. Antes había rechazado los modelos de generación de imágenes por inconsistentes; esta propuesta lo resuelve usando Forja como guía. Aprobó la instalación y ya está hecho: **`herramientas/crisol/`** (ver su README).

**Qué se aprendió en las primeras pruebas (5 de noviembre de 2026):**
- Pasarle al modelo solo los bordes de Forja no sirve: inventa los colores en cada imagen (capucha verde, café o gris según el ángulo, cara de espaldas, cara verde en unos cuadros del reposo).
- Partir del dibujo a color de Forja (img2img) con fuerza 0,55 sí da coherencia: la capucha es verde en todos los ángulos y de espaldas no aparece cara. Con 0,4 queda casi igual a Forja; con 0,7 empieza a inventar (ojos verdes, otra bufanda).
- La paleta común tiene que salir solo de los pixeles del personaje (k-means), no del fondo, o se pierden colores.
- Pintar cada cuadro de una animación con el modelo hace que los detalles "hiervan": el 64 % de los pixeles cambiaba por cuadro. El arreglo es que el modelo pinte solo el cuadro clave y que los demás cuadros muevan esos mismos pixeles con el movimiento de Forja (flujo óptico). Con eso cada animación cambia por cuadro lo mismo que Forja: reposo 13 % contra 12 %, caminar 28 % contra 25 %, ataque 46 % contra 44 % y golpe 43 % contra 43 %. Las cuatro animaciones de Teo (94 cuadros) costaron 12 imágenes del modelo.
- 96 px con 20 colores se ve más limpio que 128 px con 32, y con la cámara alejada sobra. A 64 px se pierde la cara.
- **Lo que falta para calidad PixelLab:** la textura del manto todavía sale manchada, la cara es muy simple y el bastón se corta en algunos cuadros. El diseño sigue siendo el de Forja, que al autor no le gustó: Crisol lo pinta mejor, pero no lo rediseña. Los siguientes pasos son entrenar un LoRA propio con los sprites que el autor apruebe y probar otro diseño de personaje en Forja.
- Con 15 GB de RAM y otros programas abiertos, la descarga a CPU de `diffusers` hacía caer el proceso. Ahora los textos se codifican una vez y el resto del modelo vive en la tarjeta de video: 19 a 36 s por imagen y 6,7 GB de video.

**Cómo funcionaría:**
1. Forja da la estructura: el modelo 3D de cada personaje con su esqueleto, en cada ángulo y cuadro.
2. Un modelo local (Stable Diffusion XL + el ajuste `pixel-art-xl`) pinta encima, guiado por ControlNet con los renders de Forja (profundidad y contorno), con la misma semilla.
3. Se reduce al tamaño real del sprite, se fija la paleta y se limpia con las herramientas de revisión de Forja.
4. Con 20 a 40 imágenes que apruebe el autor se entrena un LoRA de su estilo y de cada personaje.

**Lo que necesita la computadora:**
- Tarjeta NVIDIA con 8 GB de video o más. Las RTX serie 50 necesitan PyTorch con CUDA 12.8 o más nuevo.
- Unos 13 GB para instalar, más espacio de trabajo: conviene tener 25 GB libres o más.

**Descargas, todas de fuentes oficiales:**

| Qué | De dónde | Tamaño |
|---|---|---|
| PyTorch con CUDA | download.pytorch.org | ~3 GB |
| `diffusers`, `transformers`, `accelerate`, `peft` | PyPI | ~0,2 GB |
| Stable Diffusion XL base 1.0 | Hugging Face, `stabilityai` | ~7 GB |
| `pixel-art-xl` | Hugging Face, `nerijs` | ~0,2 GB |
| ControlNet de profundidad y contorno para SDXL | Hugging Face, `diffusers` | ~1–2,5 GB |

**Lo instalado** en esta computadora: PyTorch 2.11 con CUDA 12.8 (RTX 5050 Laptop, 8 GB), `diffusers` 0.42 y los modelos de la tabla (se usó ControlNet de contorno, la versión chica), unos 8 GB en `~/.cache/huggingface`.

**Riesgos conocidos:** los modelos generales rinden peor en sprites muy chicos, los detalles pueden cambiar entre cuadros de una animación y no igualará a PixelLab el primer día. El plan B es la API de pago de PixelLab, usando Forja como guía y revisión.
