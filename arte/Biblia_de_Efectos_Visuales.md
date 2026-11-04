# EL BIBLIOTECARIO — BIBLIA DE EFECTOS VISUALES

> **Prioridad de producción número uno.** Este documento manda sobre cualquier otra decisión estética en combate.
> Basado en `01_CANON.md` y en `arte/Direccion_de_Arte.md` (paletas, tamaños y UI).
> Escrito para que un artista de VFX, un programador gráfico y un diseñador de combate puedan producir con él.

---

## 0. MANIFIESTO

**Cada pelea es el clímax de una película.** Una pelea contra tres ratas de granero también. Que la escala cambie, pero que la intención no.

1. **El jugador debe querer ver su propio ataque otra vez.** Si un efecto no provoca eso, no está terminado.
2. **El efecto cuenta quién lo lanza.** Teo escribe, Corvan sangra, Sapros pudre, los Señores deforman lo que más amaron. Sin leer el nombre de la habilidad, se debe saber de quién es.
3. **La claridad es parte del espectáculo.** Un efecto que esconde el glifo de intención o el instante de contacto está roto, por bonito que sea. La Réplica depende de leer el golpe.
4. **Anticipar, pagar, respirar.** Todo efecto tiene anticipación, impacto y residuo. El impacto es breve y brutal; el residuo deja que el ojo descanse.
5. **El mundo se entera.** El fuego quema el fondo, el ámbar gotea en el suelo y la tinta mancha. Al final de una pelea, la arena cuenta lo que pasó.
6. **Lo pixelado da la forma y lo HD da la luz.** Forma dibujada a mano, brillo de película.
7. **El silencio también es un efecto.** Los mejores momentos se preparan quitando cosas.
8. **Cada efecto tiene una versión corta.** El espectáculo nunca debe volverse tedioso a la vigésima vez.

---

## 1. EL LENGUAJE FIRMA: "TINTA QUE SE VUELVE LUZ"

Toda magia de Teo sigue la misma gramática de tres tiempos. Es la identidad visual del juego.

### 1.1 Los tres tiempos
| Tiempo | Qué se ve | Color | Duración típica |
|---|---|---|---|
| **TRAZO** | La pluma de Teo dibuja en el aire (o en el suelo) un trazo caligráfico. El trazo tiene **presión**: empieza fino, engorda y termina en punta. Al moverse suelta gotitas de tinta. | Tinta `#0E1030` con brillo húmedo índigo `#5A63D6` | 30–50 % del efecto |
| **IGNICIÓN** | El trazo se enciende como una mecha, **del principio al final**, en el color de la escuela. El borde que avanza es dorado (`#E8B04B`) y la tinta "hierve" convirtiéndose en luz. | Color de la escuela + borde dorado | 10–20 % |
| **REVELACIÓN** | El trazo se transforma en el efecto real (fuego, ámbar, raíces, luz de luna...) y se desprenden letras de **Glifo Lunar** que flotan y se apagan. | Color de la escuela | 30–60 % |

**Regla:** si el jugador congela cualquier cuadro de un hechizo de Teo, debe ver al menos uno de estos tres elementos: tinta, letra o borde dorado.

### 1.2 La gramática contraria: "la luz que se vuelve moho" (Sapros)
| Tiempo | Qué se ve |
|---|---|
| **BRILLO** | Algo resplandece de forma enfermiza: demasiado saturado, demasiado dulce. |
| **MANCHA** | Aparecen manchas que crecen desde dentro, como moho en una fruta. |
| **DESCOMPOSICIÓN** | Todo se ablanda, cuelga, gotea y pierde color hacia el verde-bilis y el violeta. |

Los Señores mezclan las dos gramáticas: sus ataques empiezan con un motivo de Orvalis (bandejas de plata, martillo, páginas, estandarte, velo) y terminan pudriéndose. **Esa mezcla es su tragedia, contada sin palabras.**

### 1.3 La gramática rival: "tinta de sangre" (Corvan)
Corvan también es un escriba. Escribe en el aire con dos dedos, pero su trazo es **rojo oscuro** (`#8E1F2A` → `#3A1F3D`), no se enciende sino que **coagula**, y sus letras son alargadas y elegantes. Cuando Teo y Corvan lanzan al mismo tiempo, las dos tintas chocan (ver §12.6, *Choque de Plumas*).

### 1.4 Biblioteca de motivos (piezas reutilizables)
| Motivo | Producción | Uso |
|---|---|---|
| **Trazo caligráfico** | 12 trazos base (recto, curva, coma, espiral, gancho, firma...) como splines con shader `ink_stroke_reveal` | Todo hechizo de Teo |
| **Salpicadura de tinta** | 8 flipbooks de 8 cuadros + 6 calcomanías de mancha | Impactos, Desviar |
| **Gotitas** | Partícula circular con cola, gravedad y arrastre | Trazos, golpes |
| **Letras de Glifo Lunar** | 24 signos en 8 × 8 y 16 × 16 px, con versión brillante | Revelación, Réplica, Refutar |
| **Letra capitular** | 6 capitulares iluminadas (una por escuela) de 64 × 64 | Iluminaciones, UI |
| **Página** | 4 sprites de página + física de hoja (oscilación, giro) | Esquivar, Revelación, transiciones |
| **Pan de oro** | Partícula de lámina dorada que gira y destella | Críticos, Matrícula de Honor |
| **Sello de cera** | Sello que se agrieta en 4 estados + 12 esquirlas | Postura, Ruptura |
| **Listón** | Cinta física (cadena de 10 segmentos) con material de seda | Teo, efectos de Réplica |
| **Polilla** | Boid de 3–6 px con aleteo de 4 cuadros | Viejo Polilla, Luna, Plata |
| **Semilla** | 6 semillas con brote animado | Semillados, Guardia |
| **Grieta de papel** | Calcomanía de pliegue con sombra | Ruptura, entornos |

---

## 2. ANATOMÍA DE UN EFECTO

### 2.1 Las tres fases
1. **Anticipación**: atrae la mirada al lugar donde va a pasar algo. Concentra partículas *hacia dentro*, sube el brillo, curva la luz, oscurece levemente el entorno (viñeta del 5 al 15 %).
2. **Impacto**: el pago. Dura entre 1 y 6 cuadros visibles más el hit-stop. Es donde va el destello, la sacudida, la salpicadura, el número de daño y el sonido principal. **El cuadro de contacto es sagrado**: está marcado en datos y es la referencia para la ventana de Réplica.
3. **Residuo**: partículas que caen, humo que sube, tinta que se seca, brasas en el suelo y calcomanías persistentes. Devuelve el ritmo y le cuenta al jugador qué cambió en el escenario.

### 2.2 Presupuesto por nivel
| Nivel | Duración total | Anticipación | Hit-stop | Residuo | Partículas máx. simultáneas | Sacudida | Cámara | Posproceso |
|---|---|---|---|---|---|---|---|---|
| **Básico** (ataque normal) | 0,6–0,9 s | 0,2 s | 3 cuadros | 0,3 s | 150 | Nivel 1 | Fija | Ninguno |
| **Nivel I** | 1,0–1,4 s | 0,35 s | 4–5 | 0,5 s | 400 | 1–2 | Acercamiento suave | Bloom ligero |
| **Nivel II** | 1,5–2,2 s | 0,5 s | 6–8 | 0,8 s | 1 200 | 2–3 | Acercamiento + paneo que sigue al proyectil | Bloom + distorsión |
| **Nivel III** | 2,5–3,5 s | 0,8 s | 8–10 | 1,2 s | 3 000 | 3–4 | 1 corte cinemático | + aberración cromática y gradación de color |
| **Iluminación** | 7–9 s (corta: 3–3,5 s) | Secuencia | Secuencia | 2 s | 8 000 | 5 | Secuencia completa | Todo |
| **Ataque enemigo común** | 1,0–1,8 s | **≥ 0,6 s** (legible) | 3–6 | 0,4 s | 600 | 1–3 | Fija o acercamiento suave | Bloom |
| **Ataque de jefe** | 1,5–4 s | **≥ 0,8 s** | 6–12 | 1 s | 3 000 | 2–5 | Libre según el diseño | Libre |

*Los cuadros se cuentan a 60 fps de juego aunque el dibujo vaya a 12–24 fps.*

### 2.3 Reglas de composición
- **Regla del lienzo libre**: el glifo de intención, la barra de vida del objetivo y el tintero de PA nunca se tapan con partículas opacas. Las partículas que crucen la UI bajan a un 30 % de opacidad.
- **Regla de la dirección**: el impacto siempre "empuja" en la dirección del golpe: salpicaduras, chispas y sacudida van en el vector del ataque (70 % en el eje del golpe, 30 % aleatorio).
- **Regla del color dominante**: un efecto usa como máximo **tres tonos de su escuela + oro**. Si hace falta más, es que el efecto quiere decir dos cosas a la vez.
- **Regla del brillo**: solo el núcleo de 1–2 px puede tocar el blanco; el resto se queda en `#F2E8D5` o en el tono de núcleo de la escuela.

---

## 3. IMPACTO Y SENSACIÓN

### 3.1 Hit-stop (cuadros a 60 fps)
| Evento | Cuadros |
|---|---|
| Ataque básico | 3 |
| Habilidad Nivel I / II / III | 4 / 6 / 8 |
| Golpe crítico | +3 sobre el base |
| Golpe a debilidad | +2 sobre el base |
| Desviar exitoso | 6 (atacante y Teo congelados) |
| Refutar (cada glifo / último) | 4 / 10 |
| **Réplica Perfecta** | 14 + cámara lenta (ver §5.7) |
| **Ruptura** | 18 |
| **Remate Ilustrado** | 24 + 0,5 s a 25 % de velocidad |
| Teo recibe golpe leve / fuerte | 4 / 7 |
| Muerte de enemigo común | 6 |

**Cómo se ve el hit-stop:**
- Atacante y objetivo se congelan.
- El objetivo vibra 1 px por cuadro, alternando dirección (sensación de que "absorbe" el golpe).
- **Las partículas siguen corriendo al 10 % de velocidad**: la tinta sigue goteando aunque el mundo esté detenido. Nunca congelar todo; un congelado total se ve como un error del juego.

### 3.2 Sacudida de pantalla (modelo de "trauma")
Cada golpe suma trauma (0 a 1); la sacudida es proporcional a trauma² y el trauma decae con el tiempo. Se usa ruido suave de 25–30 Hz, no aleatorio puro.

| Nivel | Amplitud a 1080p | Duración | Rotación | Extra |
|---|---|---|---|---|
| 1 | 2 px | 0,15 s | — | — |
| 2 | 4 px | 0,25 s | — | — |
| 3 | 7 px | 0,35 s | 0,3° | — |
| 4 | 11 px | 0,5 s | 0,6° | Pulso de zoom de 1 % |
| 5 | 16 px | 0,8 s | 1,2° | Pulso de zoom de 2 % + polvo cayendo del "techo" del diorama |

- La sacudida se aplica a la imagen compuesta final; las capas pixeladas no pierden nitidez.
- Opción del jugador: intensidad de sacudida de 0 a 100 %.

### 3.3 Destellos
- **Destello de papel**: capa `#F2E8D5` a pantalla completa, máximo 60 % de opacidad, máximo 2 cuadros.
- **Destello de escuela**: lo mismo, pero teñido del color de núcleo de la escuela, al 35 %.
- **Fotosensibilidad**: máximo **3 destellos de pantalla completa por segundo**. Con la opción *Reducir destellos*, los destellos se sustituyen por un pulso de viñeta y un aumento de bloom localizado.

### 3.4 Impacto de Grabado (cuadro firma)
En críticos, Rupturas, Réplicas Perfectas y el golpe final de una Iluminación se insertan **2 cuadros de grabado**:
- **Cuadro 1**: la escena se invierte en silueta: todo lo que tiene forma se vuelve tinta `#0E1030` sobre papel `#F2E8D5`, como un grabado en madera. Los contornos se engrosan 1 px.
- **Cuadro 2**: el mismo grabado, pero el elemento golpeado y el arma se pintan del color de la escuela.
- Después se vuelve al color normal con el destello de papel cayendo en 4 cuadros.
Es el "cuadro de manga" de este juego: **todo es un libro, hasta el impacto.**

### 3.5 Aberración cromática
- Solo en críticos, Ruptura, Réplica Perfecta y los picos de las Iluminaciones.
- Radial desde el punto de impacto, máximo 3 px de separación a 1080p, decae en 8 cuadros.

### 3.6 Números de daño caligráficos
| Tipo | Estilo |
|---|---|
| Daño normal | Numerales manuscritos de la fuente "Escriba", color tinta con contorno papel. Salen con una pequeña salpicadura y luego **se secan**: pasan de tinta brillante a café mate en 0,8 s y se desvanecen. |
| Crítico | El doble de tamaño, contorno de pan de oro, y encima la palabra **"¡Crítico!"** con letra capitular. Dos láminas de oro giran alrededor. |
| Debilidad | El número aparece **subrayado dos veces con tinta roja** y la palabra "¡Débil!" en cursiva roja. |
| Resistencia | Número gris pequeño en cursiva; la palabra "Resiste" en gris. |
| Inmune | Un **sello de biblioteca** cae sobre el objetivo con la palabra "INMUNE" en tinta morada. |
| Curación | Cursiva fluida en ámbar o verde jade con un "+" que es un brotecito. |
| Daño de postura | Números pequeños color cera, rodeados de esquirlas. |
| Ganancia de PA | Gotitas de tinta que vuelan hacia el tintero. |
| Golpes múltiples | Los números se alinean uno tras otro como una frase y, al terminar, se escribe la **suma total** con una rúbrica: *"= 1 284"*. |

### 3.7 Reacción al golpe
- El sprite golpeado parpadea **2 cuadros con el color de la escuela atacante** (nunca blanco puro).
- Empuje de 4 a 12 px según el nivel, con retorno en 10 cuadros.
- En los enemigos grandes, la reacción es **por partes**: se mueve la pieza golpeada, no todo el cuerpo.

---

## 4. CÁMARA DE COMBATE

### 4.1 Encuadre base
- Diorama en 3/4 lateral: grupo de Teo a la izquierda, enemigos a la derecha. **Regla de los 180°**: el grupo siempre a la izquierda, incluso en cortes.
- Centro de cámara con un sesgo del 10 % hacia el actor activo.
- Simulación de órbita: hasta ±8° mediante desplazamiento de las capas del diorama (paralaje).

### 4.2 Movimientos por nivel
| Situación | Movimiento |
|---|---|
| Inicio de turno | Acercamiento del 5 % sobre el actor activo, 0,4 s con salida suave |
| Nivel I | Acercamiento del 8 % |
| Nivel II | Acercamiento del 12 % y paneo siguiendo el proyectil |
| Nivel III | Corte a primer plano del lanzador (anticipación) → corte a plano general (impacto) |
| Ataques colosales | Alejamiento hasta 0,6× para que quepa la escala |
| Golpe recibido por Teo | Micro-acercamiento del 3 % hacia Teo |

### 4.3 Reglas de cortes
- Máximo un corte cada 0,5 s.
- El plano del impacto se sostiene al menos 0,4 s.
- **La cámara nunca esconde el glifo de intención** durante una defensa del jugador; si un ángulo lo taparía, el glifo se reubica en la UI.

### 4.4 Paneles de Manuscrito (viñetas tipo manga)
La pantalla se divide en 2–4 paneles con bordes dibujados a tinta y esquinas doradas. Cada panel muestra una reacción simultánea. Al terminar, **los paneles se rompen como páginas arrancadas** y vuelve el plano completo.
- Se usan en: Réplica Perfecta, Rupturas de jefe, Técnicas de Dúo (Teo + Semillado), presentación de fase de cada jefe y el *Choque de Plumas*.
- Duración típica: 18–30 cuadros por panel.

### 4.5 Franjas cinematográficas
Para Iluminaciones y transiciones de jefe aparecen franjas de 2,35:1 con textura de **lomo de libro de cuero** (repujado dorado sutil), no barras negras planas.

### 4.6 Profundidad de campo
Desenfoque por capas: en primeros planos, las capas lejanas del diorama se desenfocan 2–4 px. Nunca se desenfoca la capa de combate.

---

## 5. LA RÉPLICA

La Réplica es el corazón del combate. Visualmente debe sentirse como **refutar un argumento**: elegante, preciso y satisfactorio.

### 5.1 El glifo de intención
- Aparece sobre el enemigo entre 0,6 y 1,2 s antes del contacto (según dificultad).
- Late al ritmo exacto del ataque: si el combo tiene tres golpes, el glifo da tres pulsos con la misma cadencia.
- **Anillo de lectura**: un anillo fino de tinta se contrae alrededor del glifo y se cierra justo en el cuadro de contacto. Se puede desactivar en el modo *Erudito* (más difícil, con mejor recompensa).
- Al cerrarse el anillo, el glifo destella si la defensa fue correcta o se mancha si falló.

### 5.2 Esquivar (cualquier glifo)
- Teo deja **3 imágenes residuales hechas de páginas sueltas** (siluetas de papel recortado) que salen volando y se dispersan en 20 cuadros.
- El listón dibuja un latigazo en S.
- **Esquiva perfecta** (ventana estrecha): la acción se ralentiza al 40 % durante 0,3 s y se escribe en dorado la palabra *"¡Esquiva!"* junto a Teo.
- **Fallo**: las imágenes de papel salen rasgadas y Teo recibe el golpe.

### 5.3 Desviar (◆, golpes físicos)
- **Contacto**: la punta de la pluma intercepta el golpe; 6 cuadros de hit-stop.
- **Chispa de tinta**: abanico de gotitas índigo-negras en dirección contraria al golpe, con chispas doradas en el borde.
- **Coma caligráfica**: en el punto de contacto aparece un trazo en forma de coma que se enciende y se apaga en 12 cuadros.
- Sacudida nivel 1. Sonido: "tinc" metálico + raspado de pluma.
- **Carga de Réplica**: una letra dorada vuela del contacto al medidor de Réplica (una pluma que se va llenando de oro).
- **Escalada en cadena**: el 1.er desvío da chispa índigo; el 2.º añade oro; el 3.º añade un anillo de letras; del 4.º en adelante, una pequeña ráfaga de páginas. **El jugador debe sentir que el combo va "subiendo de volumen".**
- **Fallo**: mancha de tinta cruzando a Teo; brillo rojo en sus lentes; tambaleo de 12 cuadros.

### 5.4 Refutar (◯, conjuros)
1. El proyectil mágico enemigo viaja con **una frase escrita orbitándolo** (el "argumento" del conjuro, en letras de su escuela).
2. Teo alza su libro y aparecen de 2 a 5 indicaciones de dirección sobre el proyectil.
3. **Cada acierto tacha una letra** de la frase con un trazo de tinta roja; el color del conjuro se apaga un poco.
4. **Último acierto**: la frase se reescribe con la letra de Teo, el conjuro **invierte su color** (giro de tono de 180° + contorno de tinta) y regresa al lanzador con un trazo dorado de "devolución".
5. Hit-stop de 4 cuadros por glifo y 10 en el último. En el último aparece el Impacto de Grabado si el conjuro era de nivel III o de jefe.
- **Fallo**: el conjuro golpea y las letras quedan quemadas sobre Teo un instante antes de desaparecer.

### 5.5 Saltar (▲, ondas a ras de suelo)
- La onda recorre el suelo como una grieta con escombros que saltan.
- Teo salta; en el punto más alto el listón forma un círculo completo.
- **Salto perfecto**: bajo sus pies aparece un instante una plataforma de páginas que se deshace al aterrizar.
- Aterrizaje con nube de polvo según el material del suelo.

### 5.6 Imparable (✦)
- Aura de páginas rasgadas alrededor del enemigo y sonido grave de papel desgarrándose.
- Si el jugador intenta desviar, la pluma "salpica" y no detiene nada: animación especial de fallo en la que la tinta se escurre de la punta.

### 5.7 RÉPLICA PERFECTA — cuadro a cuadro (60 fps)
**Disparador**: el último golpe de un combo enemigo es desviado o refutado después de haber defendido todos los anteriores.

| Cuadro | Imagen | Sonido |
|---|---|---|
| **0** | Contacto del último desvío. Empieza un hit-stop de 14 cuadros. Destello de papel al 40 % (2 cuadros). | "Tinc" + campana grave |
| **2–3** | **Impacto de Grabado** (2 cuadros). | — |
| **4–14** | El mundo pasa a **Modo Papel**: se desatura a sepia y aparece grano de papel (de 0 a 100 % en 10 cuadros). El enemigo gana un contorno de boceto a lápiz. Las partículas bajan al 5 % de velocidad. | La música baja a −12 dB y se filtra |
| **14–38** | **Paneles de Manuscrito**: la pantalla se divide en 3 paneles verticales: (1) el arma del enemigo rebotando; (2) **los ojos de Teo tras los lentes, con un destello en el cristal**; (3) la punta de la pluma soltando una sola gota. | Silencio. Latido. Una gota |
| **38** | La gota toca el suelo: **los paneles se rasgan como páginas** y vuelve el plano completo. Teo es ahora **una silueta de tinta pura**; solo el listón conserva su rojo. | Rasgado de papel |
| **38–62** | Teo cruza la pantalla en **tres trazos caligráficos** de 8 cuadros cada uno: horizontal, diagonal y un gancho final. Juntos forman la letra de la Réplica en Glifo Lunar. Cada trazo deja una estela negra sobre el mundo de papel. | Tres pinceladas secas, cada vez más agudas |
| **62–70** | Los tres trazos **se encienden en oro** del principio al final, como mechas. | Siseo creciente |
| **70** | **El color vuelve** desde los trazos hacia afuera (barrido radial). El enemigo recibe el daño: número grande, aberración cromática de 3 px, sacudida nivel 4 y hit-stop de 8 cuadros. | **Golpe musical** cuantizado al compás (±4 cuadros de margen) |
| **78–120** | Residuo: letras doradas flotan hacia arriba, la lluvia de tinta se detiene y el glifo de la Réplica queda grabado en el suelo y se apaga en 2 s. El sello de postura del enemigo se agrieta con fuerza. | La música vuelve a su volumen en 1 compás |

- Duración total: unos 2 s.
- **Versión corta** (activable o automática tras 3 Réplicas Perfectas en la misma pelea): se omiten los paneles y se pasa del cuadro 14 al 38 directamente (1,2 s).

### 5.8 Réplica de los Semillados
| Semillado | Defensa | Réplica Perfecta |
|---|---|---|
| **Brotín** | Alza un escudo de hoja que ondula como agua | La hoja se vuelve cuchilla giratoria |
| **Pavesa** | Responde con una chispa que quema el arma enemiga | Explosión de brasas en espiral |
| **Lunilla** | Se deshace en polvo de polilla y se recompone detrás | Lluvia de escamas plateadas que ciegan |
Las formas evolucionadas heredan el motivo y lo amplían (ver §13).

---

## 6. RUPTURA Y REMATE ILUSTRADO

### 6.1 El sello de postura
- 0–25 %: sello intacto con un brillo de cera.
- 25–75 %: grietas finas que se multiplican con cada golpe de postura.
- 75–99 %: el sello brilla rojo y late; pequeñas esquirlas se desprenden.
- 100 %: **Ruptura**.

### 6.2 Ruptura
| Cuadro | Imagen |
|---|---|
| 0 | El sello estalla: 12 esquirlas de cera roja salen hacia la cámara con física (rebotan "en la pantalla" y caen). |
| 2–3 | Impacto de Grabado. |
| 4–18 | Hit-stop. Sobre el sprite del enemigo aparece una **calcomanía de página doblada** (líneas de pliegue con sombra) y el enemigo se desatura al 50 %. |
| 18+ | El enemigo cae en su postura de aturdimiento. **En lugar de estrellitas, le orbitan letras revueltas** ("¿", "¡", "?", "&"). La viñeta oscurece la pantalla un 20 % y la música pasa por un filtro de graves durante 1,5 s. |

### 6.3 Remate Ilustrado
Disponible contra un enemigo en Ruptura. **La pantalla se convierte en una página de manuscrito.**
1. **0,0 s**: la arena se redibuja como grabado coloreado a mano, enmarcado en un margen de pan de oro.
2. **0,4 s**: el enemigo pasa a ser una **ilustración en el margen**.
3. **0,8 s**: Teo actúa sobre la ilustración según la escuela equipada:
   - **Tinta**: escribe "FIN" con letras enormes que atraviesan la ilustración.
   - **Savia**: vierte resina sobre la ilustración y la deja atrapada en ámbar.
   - **Brasa**: aplica un sello candente que quema la página.
   - **Glifo**: tacha la ilustración y escribe al lado *"(errata)"*.
   - **Guardia**: unas raíces brotan del margen y estrujan la ilustración.
   - **Luna**: la luz de la luna borra la ilustración como si se decolorara al sol.
4. **1,8 s**: la página se rasga en diagonal y volvemos a la arena: el enemigo real recibe un daño enorme.
5. Duración: 2,5 s (versión corta: 1,2 s).

**En los jefes, la ilustración del margen es el retrato humano del Señor.** Por un instante, la página nos recuerda a quién estamos golpeando. Es el punto de compasión aplicado al efecto visual.

---

## 7. LAS ESCUELAS

Cada escuela tiene identidad, motivos, partículas, shaders, sonido y tres habilidades de ejemplo descritas cuadro a cuadro (en cuadros de juego a 60 fps). Los nombres de habilidad son de ejemplo para producción; la lista definitiva está en el documento de progresión.

---

### 7.1 TINTA (Tronco — escuela base de Teo)
- **Identidad**: la gramática firma en estado puro. Caligrafía, gotas, letras, papel.
- **Paleta**: `#0E1030` · `#2B3170` · `#5A63D6` · oro `#E8B04B` · papel `#F2E8D5`.
- **Partículas**: gotas con cola (gravedad y arrastre); salpicaduras que dejan **calcomanías de mancha que se secan** (pasan de brillo húmedo a mate en 1,5 s); letras de Glifo Lunar; recortes de papel.
- **Shaders**: `ink_stroke_reveal`, `ink_ignite`, `ink_bleed` (mancha que se expande sobre el suelo), secado.
- **Sonido**: raspado de pluma, papel, salpicaduras húmedas, arpa pulsada.

**A) Flecha de Tinta** *(básico)*
- **0–12**: Teo sacude la pluma; se forma un trazo en forma de coma frente a él.
- **12**: la coma se enciende y se estira en una flecha de tinta con punta dorada.
- **12–28**: viaja con estela de gotitas; la cámara no se mueve.
- **28**: impacto. Salpicadura sobre el enemigo, 6 gotas y 3 letras doradas. Hit-stop de 3.
- **28–80**: la mancha se seca sobre el enemigo y desaparece.

**B) Párrafo Cortante** *(Nivel II, 5 golpes)*
- **0–30**: Teo escribe en el aire una línea de cinco palabras en Glifo Lunar, de izquierda a derecha. Cada letra deja una gotita que cae.
- **30–50**: la línea se enciende **letra por letra**, como cinco mechas seguidas.
- **50–56**: la línea se despega en cinco trazos-cuchilla, uno por palabra.
- **56–110**: las cinco cuchillas vuelan en secuencia y golpean, cada una con un hit-stop de 4 y la última de 7. La cámara hace un paneo que sigue la secuencia.
- **110**: las palabras quedan clavadas en el enemigo y **estallan en tinta** a la vez.
- **Residuo**: 5 manchas en el suelo con la forma de las palabras, secándose.

**C) Punto Final** *(Nivel III)*
- **0–30**: Teo levanta la pluma hacia arriba. Viñeta del 15 %. Las gotas del suelo **suben** hacia la pluma.
- **30**: corte al cielo del diorama. **Se forma una gota de tinta gigante** (200 px) que refleja letras en su superficie.
- **30–70**: la gota crece y tiembla. Sonido de gota que se estira.
- **70–96**: cae como un meteorito, con una estela de vapor índigo. Corte al plano general.
- **96**: impacto. Impacto de Grabado, sacudida nivel 4 y hit-stop de 8. Una **mancha perfectamente circular** (el punto) cubre el suelo bajo los enemigos y una onda de recortes de papel sale hacia afuera.
- **96–180**: el punto queda como un charco que **refleja la luna** del fondo y permanece en la arena 3 turnos.

---

### 7.2 SAVIA (Ámbar)
- **Identidad**: resina, ámbar, cosecha. El poder de **detener el tiempo como un insecto en ámbar**. Es lenta, densa y dorada.
- **Paleta**: `#8C5A1E` · `#F2A93B` · `#FFD27A` · núcleo `#FFF1C9`.
- **Partículas**: gotas de resina con viscosidad (se estiran antes de caer), granos de trigo, polen dorado, astillas de ámbar.
- **Shaders**: `amber_encase` (refracción, tinte miel, burbujas internas, **detiene la animación del sprite atrapado**), goteo viscoso (estiramiento por vértice).
- **Sonido**: madera que cruje, miel que se estira, viento sobre el trigo, flauta de madera.

**A) Gota de Resina** *(Nivel I, ralentiza)*
- **0–20**: trazo en espiral que se enciende en ámbar.
- **20–40**: la espiral se condensa en una gota de resina que cuelga de la pluma y se estira.
- **40–58**: la gota cae en parábola hacia el enemigo, dejando un hilo de miel.
- **58**: impacto pegajoso: la resina se extiende sobre el enemigo y lo hace más lento (su animación se reproduce al 70 % mientras dure el efecto). Hit-stop de 4.
- **Residuo**: gotas que caen del enemigo al suelo en cámara lenta y dejan calcomanías de ámbar que se endurecen.

**B) Prisión de Ámbar** *(Nivel II, inmoviliza)*
- **0–30**: Teo dibuja un hexágono alrededor del enemigo, a distancia.
- **30–45**: el hexágono se enciende; de sus esquinas brota resina a borbotones.
- **45–75**: la resina sube y encierra al enemigo **de abajo arriba**. En cuanto la resina lo cubre, **el sprite deja de animarse** y todo lo que tiene alrededor queda suspendido (partículas incluidas).
- **75**: cristalización con un destello de miel y un "clac" de vidrio. Dentro del ámbar se ven burbujas y un mosquito de 2 px (detalle de humor).
- **Al liberarse**: el ámbar se resquebraja en 4 cuadros y estalla en astillas doradas.

**C) Cosecha Dorada** *(Nivel III, curación de grupo)*
- **0–40**: Teo clava la pluma en el suelo; una línea de luz dorada corre bajo su grupo.
- **40–100**: **brota un campo de trigo** en el lado del grupo, de atrás hacia adelante, en 3 capas de paralaje. Atardecer en el cielo del diorama.
- **100–130**: cada espiga suelta polen dorado que viaja en curvas hacia los aliados.
- **130**: los aliados brillan en ámbar y aparecen números de curación en cursiva.
- **Residuo**: el trigo se mece 2 s y se convierte en hojas secas que se lleva el viento.

---

### 7.3 BRASA (Carmesí)
- **Identidad**: fuego de **forja**, no incendio salvaje. Metal fundido, yunque, temple, chispas. La pluma de Teo se pone al rojo vivo.
- **Paleta**: `#7A1418` · `#C2272D` · `#FF5A1F` · `#FFB000` · núcleo `#FFF4D6`.
- **Partículas**: chispas largas que rebotan en el suelo y se convierten en brasas (subemisores); brasas persistentes que titilan; gotas de metal fundido; bocanadas de humo.
- **Shaders**: `heat_distortion`, rampa de temperatura (negro → rojo → naranja → amarillo → blanco), enfriamiento (de vuelta a negro con grietas brillantes).
- **Sonido**: yunque, fuelle, siseo de metal enfriándose, tambores graves.

**A) Chispa de Yunque** *(básico de Brasa)*
- **0–10**: la punta de la pluma pasa de negro a rojo vivo.
- **10–16**: Teo golpea el aire como un herrero; aparece un yunque fantasmal de 1 cuadro.
- **16–30**: un chorro de chispas sale disparado en abanico.
- **30**: impacto; las chispas rebotan en el enemigo y en el suelo. Hit-stop de 3.
- **Residuo**: 8–12 brasas en el suelo que titilan 2 s.

**B) Temple** *(Nivel II, potencia el arma)*
- **0–30**: Teo sostiene la pluma horizontal; un círculo rúnico de forja gira bajo ella.
- **30–60**: tres martillazos fantasmales golpean la pluma; en cada uno hay destello, chispas y sacudida nivel 1.
- **60–80**: la pluma se pone al blanco y después **se templa**: una nube de vapor la envuelve con siseo.
- **80**: la pluma queda con un filo de luz roja permanente y estelas de calor durante el efecto.

**C) Colada** *(Nivel III, área)*
- **0–40**: Teo dibuja una línea en el suelo; la línea se agrieta y se ve el resplandor naranja debajo.
- **40–60**: la grieta se abre; distorsión de calor en toda la mitad derecha de la pantalla.
- **60–110**: **un río de bronce fundido** sale de la grieta y avanza hacia los enemigos, que quedan iluminados desde abajo (luz dinámica naranja).
- **110**: la colada los alcanza: chorros verticales de metal, sacudida nivel 3 y hit-stop de 8.
- **110–200**: el metal se enfría en el suelo: pasa de blanco a rojo y luego a negro con grietas que todavía brillan. **Queda como terreno durante el resto de la pelea.**

---

### 7.4 GLIFO (Índigo)
- **Identidad**: geometría arcana y texto. Analizar, anotar, tachar, corregir, copiar. Círculos de glifos, páginas flotantes y luz cian. **No es ciencia ficción**: todo es tinta luminosa, nunca hologramas.
- **Paleta**: `#2A2F7A` · `#4B56C8` · `#8FA2FF` · núcleo `#B6F0FF` · papel `#E9E1CC`.
- **Partículas**: letras, enjambres de páginas, líneas de luz, fragmentos geométricos.
- **Shaders**: `text_peel` (letras que se despegan del sprite enemigo), tachadura superpuesta, círculos rúnicos rotativos con trazo dibujado.
- **Sonido**: celesta, susurros, páginas hojeadas, timbres cristalinos.

**A) Anotación** *(Nivel I, marca una debilidad)*
- **0–20**: un corchete de tinta luminosa se dibuja junto al enemigo.
- **20–40**: aparece una nota al margen manuscrita con una flecha al punto débil ("*¡aquí!*") y el ícono del elemento débil.
- **40**: el punto débil del sprite recibe un contorno cian pulsante que dura mientras dure la marca.

**B) Tachadura** *(Nivel II, elimina una mejora enemiga)*
- **0–20**: el ícono de la mejora enemiga **sale de su barra de estado** y crece frente al enemigo.
- **20–35**: Teo traza una línea roja que lo tacha de lado a lado.
- **35–60**: el ícono se arruga como papel y se cae al suelo; el aura de la mejora **se despega del enemigo letra por letra**.
- **60**: destello cian y un sonido de "corrección".

**C) Transcripción** *(Nivel III, copia una habilidad enemiga)*
- **0–30**: Teo abre su libro frente al enemigo; las páginas se agitan solas.
- **30–90**: **un listón de letras** sale del enemigo (de la zona del cuerpo que usa esa habilidad) y fluye en espiral hacia el libro. Mientras sale, el enemigo parpadea y pierde un poco de color.
- **90–110**: la página del libro se llena de texto; aparece la ilustración de la habilidad en miniatura.
- **110**: el libro se cierra de golpe con un destello de pan de oro. Aparece el texto *"Transcrito: [nombre]"*.
- La primera vez que se transcribe una habilidad hay un Panel de Manuscrito extra con la ilustración ampliada.

---

### 7.5 GUARDIA (Jade)
- **Identidad**: raíces, corteza, jade, siluetas de guardianes. Protección pesada y orgánica. **La escuela del Bastión y de la Noche de las Mil Semillas.**
- **Paleta**: `#0E3B33` · `#1F8A70` · `#58C9A0` · núcleo `#D8F5C6` · madera `#6B4A2B`.
- **Partículas**: hojas, astillas de corteza, chispas hexagonales de jade, terrones de tierra.
- **Shaders**: escudo de cristal de jade (celdas hexagonales con brillo en los bordes), crecimiento de raíces (tiras de sprites que crecen por spline), siluetas espectrales de guardianes (superposición translúcida con ruido).
- **Sonido**: madera que cruje, cuernos graves, tambores profundos, hojarasca.

**A) Escudo de Corteza** *(Nivel I)*
- **0–20**: Teo apoya la pluma en el suelo; brota un anillo de raíces alrededor del aliado.
- **20–40**: las raíces se trenzan hacia arriba y se cubren de corteza, **dejando ver el jade por las grietas**.
- **40**: destello hexagonal; el escudo se vuelve casi transparente y queda como un contorno de jade alrededor del aliado.
- **Al recibir un golpe**: las celdas hexagonales se iluminan en el punto de impacto y caen astillas.

**B) Brote Centinela** *(Nivel II, invocación temporal)*
- **0–20**: una semilla cae del libro y se clava en el suelo.
- **20–60**: brota a cámara rápida un **centinela de madera** de 96 px (raíces, tronco y una máscara de corteza con ojos de jade).
- **60**: el centinela golpea el suelo con su lanza: onda de hojas y sacudida nivel 2.
- **Mientras dura**: respira y suelta hojas; al terminar se convierte otra vez en semilla, que rueda hasta el libro.

**C) Muralla de Raíces** *(Nivel III, provocación + contraataque)*
- **0–30**: el suelo del lado aliado tiembla y salen terrones de tierra.
- **30–80**: **una muralla de raíces** emerge en tres capas, de 1,5 veces la altura de Teo, con un estandarte de Orvalis tallado en la madera.
- **80**: un cuerno grave suena y los ojos de jade de la muralla se encienden; todos los enemigos giran la cabeza hacia ella (provocación).
- **Cuando la golpean**: cada golpe recibido dispara púas de raíz contra el atacante (hit-stop de 4 y chispas de jade).

---

### 7.6 LUNA (Plata)
- **Identidad**: la escuela más bella y limpia. Luz de plata, mareas, fases, resurrección. Usa el **espacio negativo** y las estrellas: muchas figuras de esta escuela están "rellenas de cielo nocturno".
- **Paleta**: `#5E6A8A` · `#C9D6E8` · `#EEF3FA` · `#9FB4FF` · blanco solo en el núcleo de 1–2 px.
- **Partículas**: polvo de estrellas que titila, motas de luz lunar, plumas de luz (de lechuza), gotas de agua plateada, polillas de luz.
- **Shaders**: rayos de luna (`godrays_2d`), ola de marea (desplazamiento), máscaras de fase en forma de medialuna, `starfield_fill`.
- **Sonido**: coro, armónica de cristal, campanillas, agua suave.
- **Regla**: la potencia visual de esta escuela **escala con la fase lunar del combate**. En Luna Llena, todo efecto lunar suma un 30 % de partículas y bloom; en Luna Nueva, es más tenue y estrellado.

**A) Rayo de Plata** *(Nivel I)*
- **0–20**: Teo traza una medialuna en el aire; se rellena de cielo estrellado.
- **20–30**: la medialuna gira y apunta al enemigo.
- **30–40**: un rayo de luz fino y recto sale de su centro.
- **40**: impacto: corona de polvo estelar y una pluma de luz que cae girando. Hit-stop de 4.

**B) Marea Creciente** *(Nivel II, curación)*
- **0–30**: aparece agua plateada bajo los pies del grupo, que refleja la luna del fondo.
- **30–80**: la marea **sube como una ola lenta** desde atrás del grupo y lo atraviesa sin mojarlo; al pasar, cada aliado queda delineado en plata.
- **80**: la ola rompe en espuma de estrellas. Números de curación.
- **Residuo**: charcos que reflejan la luna y se evaporan en motas.

**C) Vigilia** *(Nivel III, resurrección)*
- **0–40**: la escena se oscurece y aparece una columna de luz de luna sobre el aliado caído.
- **40–80**: **una polilla de luz** baja en espiral por la columna, despacio.
- **80**: la polilla se posa en el aliado. Silencio de 10 cuadros.
- **90**: destello plateado; el aliado se levanta envuelto en luz y las alas de la polilla se abren detrás de él un instante.
- **Residuo**: escamas plateadas que caen.

---

### 7.7 PODREDUMBRE (Raíz Podrida — rama prohibida)
- **Identidad**: la anti-gramática. Moscas, hongos, moho, humedad. **Le roba el color a lo que tiene alrededor.** Es poderosa y repugnante a la vez; tiene que tentar al jugador visualmente: es la escuela con el daño que *se ve* más fuerte.
- **Paleta**: `#3A1F3D` · `#5B2A6E` · `#9DB83A` · núcleo `#D4E05A` · carne `#A8636B`.
- **Partículas**: moscas (boids), esporas, manchas de moho (calcomanías que crecen), goteos, larvas diminutas.
- **Shaders**: `mold_growth` (crecimiento guiado por mapa de flujo), `hue_drain` (radio que desatura el entorno hacia la bilis), brillo húmedo.
- **Sonido**: zumbido de insectos, chapoteo húmedo, cuerdas desafinadas, una respiración que no es de nadie.
- **Regla**: cada uso deja **una mancha de moho en el sprite de Teo y en la UI** que tarda 3 turnos en desaparecer. Con Corrupción alta, las manchas ya no desaparecen.

**A) Mordida de Gusano** *(Nivel I)*
- **0–20**: la tinta de la pluma de Teo se vuelve violeta.
- **20–40**: del suelo, junto al enemigo, sale una boca anillada de gusano.
- **40**: muerde con un chasquido húmedo. Hit-stop de 5 (uno más que en las demás escuelas: se siente más "pesado").
- **Residuo**: una mancha de moho que crece en el suelo y no se seca.

**B) Plaga** *(Nivel II, daño continuo contagioso)*
- **0–30**: Teo sopla sobre su palma; sale una nube de esporas verde-bilis.
- **30–60**: la nube se posa sobre el objetivo: **manchas que crecen desde dentro** del sprite.
- **Cada turno**: líneas de esporas saltan del infectado a los enemigos cercanos como hilos de seda sucia, y el color del entorno de cada infectado se apaga en un radio de 40 px.

**C) Florecer Pútrido** *(Nivel III, detonación)*
- **0–40**: los enemigos infectados se hinchan; les salen sombreros de hongo.
- **40–60**: silencio de 6 cuadros. Solo zumbido.
- **60**: **estallan en una floración de hongos** con esporas, moscas y un destello verde enfermizo. Sacudida nivel 3. Hit-stop de 9.
- **Residuo**: anillos de hongos en el suelo durante toda la pelea. Teo se toca el pecho (pierde vida) y aparece una mosca en el borde de la UI.

---

## 8. LAS ILUMINACIONES

Las Iluminaciones son los ataques definitivos. **Deben ser lo mejor que el jugador haya visto en un RPG por turnos.**

### Estructura común
1. **Activación**: la letra capitular de la esquina superior izquierda (cargada por Inspiración) se enciende y **cae** girando hacia Teo.
2. **El marco se cierra**: el borde iluminado de la pantalla se completa y aparecen franjas de lomo de libro.
3. **La escena se vuelve página**: la arena se transforma en ilustración y la acción ocurre "dentro del libro".
4. **El clímax regresa al mundo real**: el golpe final siempre ocurre en la arena, no en la página.
5. **Residuo largo**: 2 s de calma visual (páginas cayendo, luz que baja).

- Duración completa: 7–9 s. **Versión corta** (desde la segunda vez, activable): 3–3,5 s, que conserva siempre el golpe final completo.
- La música cambia a un tema propio de cada Iluminación que vuelve al tema de batalla en el tiempo fuerte del compás.

---

### 8.1 TINTA — "Érase una Vez"
| Tiempo | Plano | Imagen |
|---|---|---|
| 0,0 s | General | El marco dorado se cierra. Teo abre su libro y **una página se desprende y crece hasta llenar la pantalla**. |
| 0,8 s | Página | Sobre la página, con estilo de libro infantil, **se dibujan los enemigos** trazo a trazo, como ilustraciones amables. |
| 2,0 s | Página, acercamiento | Bajo la ilustración se escribe sola, en caligrafía: *"Érase una vez..."* y luego *"...un monstruo que perdió."* (el texto cambia según el enemigo: "una bestia", "una sombra", "un señor"...). |
| 3,5 s | Página, giro de cámara | **Las letras se despegan** de la página: cientos de letras que se vuelven cuchillas y atraviesan las ilustraciones, que se rasgan. |
| 5,5 s | Página entera | Se escribe **"FIN"** en pan de oro, enorme. La página se dobla y **se cierra como un libro que se golpea**. |
| 6,0 s | General, arena | Corte a la arena real: los enemigos reciben el golpe al mismo tiempo con una explosión de tinta que llena la mitad derecha de la pantalla. Impacto de Grabado, sacudida 5. |
| 7,0 s | General | Lluvia de páginas en blanco que caen meciéndose. |

### 8.2 SAVIA — "Ámbar Eterno"
| Tiempo | Imagen |
|---|---|
| 0,0 s | El cielo del diorama se tiñe de otoño dorado; hojas en cámara lenta. |
| 1,0 s | Brota trigo hasta la cintura en toda la arena; la resina llueve en gotas gruesas que caen despacio. |
| 2,5 s | **Todo entra en ámbar**: la pantalla se cubre de miel cristalizada desde los bordes. |
| 3,5 s | **La cámara atraviesa el ámbar** (refracción completa) y vemos a los enemigos congelados dentro, como insectos fósiles, con burbujas a su alrededor. |
| 5,0 s | Teo, el único que se mueve, da un golpecito al ámbar con la punta de la pluma. *Tic.* |
| 5,4 s | Una grieta recorre toda la pantalla en zigzag. Silencio. |
| 6,0 s | **El ámbar estalla en miles de astillas** de luz dorada. Daño a los enemigos y curación a los aliados. |
| 7,0 s | Las astillas caen como hojas de otoño y se disuelven. |

### 8.3 BRASA — "El Último Ocaso"
| Tiempo | Imagen |
|---|---|
| 0,0 s | Teo clava la pluma en el suelo como un cincel. El cielo se blanquea de calor. |
| 0,8 s | **Un yunque fantasmal gigantesco** emerge del suelo bajo los enemigos, al rojo vivo. |
| 1,8 s | Desde arriba baja **un martillo de luz** sostenido por una silueta enorme. *Si Brannoc ya fue liberado, la silueta es claramente la suya, con las dos cintas de luto ondeando.* |
| 2,5 s / 3,5 s / 4,5 s | **Tres martillazos.** Cada uno: destello blanco-amarillo, onda de chispas que cubre la pantalla, sacudida 4 y un anillo de distorsión de calor. |
| 5,2 s | Del tercer golpe sale forjada **una hoja de luz solar** que cae sobre los enemigos como una guillotina. |
| 6,0 s | Impacto de Grabado y golpe final. |
| 6,5 s | **Enfriamiento y ocaso**: el sol del fondo, por fin, **se pone**. Todo pasa a negro-rojo con grietas brillantes y vapor que sale de la arena con un siseo largo. Asoma la primera estrella. *(Por eso se llama "El Último Ocaso": es la noche que Brannoc no tuvo en mil años.)* |

### 8.4 GLIFO — "El Códice Abierto"
| Tiempo | Imagen |
|---|---|
| 0,0 s | Círculos de glifos se abren en capas alrededor de Teo. |
| 1,0 s | **La pantalla se convierte en una página de texto**. Los enemigos **se transforman en líneas de texto** que los describen: *"Bestia de Ceniza. Fuerte. Inmune al fuego."* |
| 2,5 s | Teo **tacha palabras** con tinta roja y escribe encima: *"Débil. Vulnerable a todo. Muy cansada."* (el texto tiene humor). |
| 4,0 s | El texto corregido **vuelve a materializar a los enemigos** con su nueva descripción: los íconos de debilidad aparecen sobre ellos. |
| 5,0 s | Cascada de círculos rúnicos que explotan en orden sobre cada enemigo. |
| 6,5 s | Al pie de la pantalla aparece una nota: *"Fe de erratas: donde decía 'invencible', léase 'derrotado'."* |

### 8.5 GUARDIA — "La Noche de las Mil Semillas"
*Homenaje visual a la Guerra del Eclipse (412 AO).*
| Tiempo | Imagen |
|---|---|
| 0,0 s | Cae la noche sobre la arena en 0,5 s. |
| 0,8 s | Teo lanza al aire un puñado de semillas que brillan en jade y caen en cámara lenta. |
| 2,0 s | **Cada semilla brota en una silueta de guardián.** Son mil, que se pierden en la distancia gracias a 5 capas de paralaje con figuras cada vez más pequeñas. |
| 3,5 s | Suena un cuerno de guerra. Todas las siluetas giran la cabeza a la vez y sus ojos se encienden en jade. |
| 4,5 s | **Carga**: la ola de guardianes pasa por encima de los enemigos como una avalancha de luz verde. Sacudida 5 continua durante 1 s. |
| 6,0 s | Los guardianes se deshacen en hojas que se lleva el viento, y vuelve el cielo normal. |

### 8.6 LUNA — "Marea de Plata"
| Tiempo | Imagen |
|---|---|
| 0,0 s | La luna del fondo empieza a crecer. |
| 1,5 s | **La luna llena ocupa medio cielo**; toda la arena queda bañada en plata. |
| 2,5 s | Teo flota a un palmo del suelo. **Si la historia ya lo permite, detrás de él aparece la silueta de Lys**, con los ojos plateados, con la mano sobre su hombro. |
| 3,5 s | **Una marea de plata** sube desde el borde inferior y lava la arena. |
| 5,0 s | Los enemigos se disuelven en luz al paso de la marea; los aliados caídos se levantan y los vivos se curan. |
| 6,5 s | La luna vuelve a su tamaño. Plumas de luz caen girando. |

### 8.6-B LAS ILUMINACIONES DEL FINAL (solo en Las Entrañas)
- **"La Que Vela"**: la Iluminación propia de Lys cuando despierta con Ilunara dentro. Parte de la estructura de "Marea de Plata", pero es Lys quien flota y la marea sube **desde la Mesa de Piedra**. Si lleva **Albar**, la secuencia termina con un único tajo de esgrima que corta la luna del fondo en dos y la deja caer como lluvia.
- **"Plenilunio"**: la Iluminación **conjunta** de Teo y Lys que cierra el final "La Última Página". Manuscrito iluminado a doble página: a la izquierda Teo escribe "FIN"; a la derecha, Lys dibuja la luna. Guion visual completo en `mundo/Las_Entranas.md` (Resolución A).

### 8.7 PROHIBIDA — "Florecimiento"
*Solo disponible con Corrupción en nivel 4. Sustituye visualmente a la Iluminación equipada.*
| Tiempo | Imagen |
|---|---|
| 0,0 s | La capitular de la esquina **se pudre** en vez de encenderse; el marco iluminado se llena de moho. |
| 1,0 s | La página se mancha de humedad desde dentro. Teo escribe con tinta violeta. |
| 2,5 s | **Las moscas forman palabras** en el aire: frases de las Cartas del Hereje. |
| 4,0 s | Los enemigos se pudren desde dentro: hongos, colapso y licuefacción. |
| 5,5 s | Daño enorme. **Teo tose y pierde vida.** La cámara se queda un instante de más sobre él. |
| 6,0 s | El moho no se va: queda en la UI hasta el final de la pelea. |

---

## 9. FASES LUNARES Y ECLIPSE EN TIEMPO REAL

El cielo del diorama es una capa viva. **La fase lunar del combate se ve en el fondo, no solo en el medallón de la UI.**

### 9.1 Las cuatro fases
| Fase | Cielo | Luz de la escena | Efectos lunares |
|---|---|---|---|
| **Nueva** | Muy oscuro; estrellas nítidas y abundantes | Fría y tenue; contornos de luz casi apagados | Tenues y estrellados: se ve más el "cielo dentro" de las figuras |
| **Creciente** | Azul plata; luna en arco | Fría, en aumento | Normales |
| **Llena** | Plata brillante; halo alrededor de la luna | Luz de contorno fuerte en todos los personajes; reflejos en el suelo | +30 % de partículas y bloom; aparecen polillas en la escena |
| **Menguante** | Plata templada; tonos más cálidos | Más cálida y baja | Normales, con estelas más largas |

- **Transición entre fases**: 2 s. El terminador de la luna se desplaza, la temperatura de la luz cambia gradualmente, **las sombras rotan y cambian de longitud** y el LUT ambiental se interpola.
- **En el Mediodía Eterno** no hay luna: el medallón muestra un sol agrietado y el cielo es blanco febril. Cuando el Sol Cautivo cae, la primera luna aparece en el cielo de ese Pliegue (momento narrativo, ver §12.2).
- **En el Santuario de la Luna Falsa**, la luna del cielo es la falsa: las fases **mienten**. El medallón parpadea y a veces muestra una fase distinta de la que ilumina la escena. El jugador atento lo nota mirando el fondo.

### 9.2 Secuencia de Eclipse (provocado por un jefe)
| Tiempo | Imagen | Sonido |
|---|---|---|
| 0,0 s | El jefe hace su gesto. **Un disco negro asoma por el borde de la luna.** | Toda la mezcla baja 6 dB |
| 0,0–2,5 s | El disco "muerde" la luna. La luz ambiental pasa a violeta profundo (`#3A1F3D`) con contornos rojos (`#C8323C`). Las sombras se alargan y se vuelven rojizas. | Grave sostenido, como un órgano |
| 1,0 s | En la UI, **la tinta del tintero se seca**: costras negras en las gotas. Los íconos de habilidades lunares se craquelan. | Crujido seco |
| 2,5 s — **Totalidad** | Anillo de corona roja alrededor del disco negro. Aparecen estrellas nítidas en todo el cielo. Los efectos lunares de Teo se vuelven fantasmales (desaturados, 50 % de opacidad). Si Folio está en pantalla, tiembla. | Silencio con un zumbido agudo muy bajo |
| **Fin del eclipse** | **Anillo de diamante**: un único punto brillante estalla en el borde de la luna → destello plateado → vuelve la luz. La tinta seca **se rehidrata** con una animación de goteo. | Acorde luminoso |

---

## 10. ENTORNOS REACTIVOS

**Regla**: cada capa del escenario tiene etiquetas de material (pasto, madera, papel, metal, agua, piedra, carne/moho). Los efectos interactúan con ellas.

| Escuela o fuente | Pasto | Madera | Papel | Metal | Agua | Piedra | Carne/moho |
|---|---|---|---|---|---|---|---|
| **Brasa** | Se incendia 2 turnos y deja calcomanía de quemado | Se chamusca y sale humo | **Arde con bordes que se enroscan** | Se pone al rojo y luego se enfría | Vapor y siseo | Brasas que titilan | Se cauteriza (se apaga el moho) |
| **Savia** | Brotan espigas | Gotea resina que se endurece | Se pega y se amarillea | Capa de ámbar brillante | Gotas doradas flotando | Ámbar en las grietas | Atrapa el moho en ámbar |
| **Glifo** | Letras brillantes en el pasto | Inscripciones talladas que brillan | **Páginas que se escriben solas** | Grabados rúnicos | Letras reflejadas | Inscripciones | Texto tachado sobre el moho |
| **Guardia** | Brotan raíces y flores de jade | Las vetas brillan en jade | Hojas secas | Enredaderas lo envuelven | Lirios | Raíces que agrietan | Las raíces limpias empujan el moho |
| **Luna** | Rocío plateado | Contorno de luz | Se vuelve translúcido | Reflejos | **Charcos que reflejan la luna** | Brillo de nácar | El moho humea y retrocede |
| **Tinta** | Manchas que se secan | Manchas | Manchas que traspasan la hoja | Salpicaduras | La tinta se diluye en volutas | Manchas | — |
| **Podredumbre** | Se marchita | Se oscurece y se ablanda | Se humedece y se deshace | Se oxida | Se enturbia | Le crece liquen | **Se extiende** |

- **Destrucción en tres estados** para los objetos del escenario (intacto, dañado, en ruinas), activados por golpes de Nivel III, Iluminaciones y ataques de jefe. Ejemplo: las estanterías del Palimpsesto se vacían, luego se inclinan y finalmente caen en una cascada de libros.
- **Clima**: lluvia en el Frente Eterno, ceniza en el Mediodía Eterno, polvo de papel en el Palimpsesto, escamas de polilla en el Santuario. Interacciones: Brasa bajo la lluvia → vapor; Luna bajo la lluvia → gotas plateadas que brillan; Savia bajo la ceniza → la resina se cubre de gris.
- **Presupuesto**: máximo 64 calcomanías persistentes por arena; las más viejas se desvanecen.
- **La pelea deja huella**: al volver a la exploración, el lugar del combate conserva un rastro del combate durante un tiempo (pasto quemado, ámbar en el suelo, tinta seca, raíces).

---

## 11. TRANSICIONES DE COMBATE

### 11.1 Entrada
- **Normal**: la pantalla se vuelve una página que **se da vuelta** (shader `page_curl`, 0,5 s) y debajo la arena se dibuja en líneas de tinta y luego se colorea (0,3 s).
- **Emboscada enemiga**: la página **es rasgada por garras** con manchas de podredumbre en los bordes del desgarro.
- **Golpe de Iniciativa (ventaja de Teo)**: la pluma de Teo **corta la página** en diagonal con un trazo dorado.
- **Jefe**: la página se quema desde el centro con el color del Pliegue y aparece una **tarjeta de título** del Señor con su nombre en capitular y su título debajo ("HESTRA MOLL · La Anfitriona · Señora del Banquete Hueco").

### 11.2 Victoria
- El golpe final se reproduce al 50 % de velocidad durante 0,5 s.
- Los enemigos se deshacen según su Pliegue (ver Dirección de Arte, §9.4).
- **Sello de Calificación**: un sello de biblioteca cae sobre la pantalla con la nota. La *Matrícula de Honor* trae un sello de cera con listón dorado y lluvia de pan de oro.
- El botín se escribe a mano en una lista, línea por línea, con un sonido de pluma por objeto. Los objetos Legendarios y Primigenios se escriben con tinta dorada y tienen su propio destello.

### 11.3 Derrota
- Teo cae de rodillas abrazando el libro. La tinta se corre desde los bordes de la pantalla hacia el centro.
- Al despertar en el atril, en el lugar donde cayó queda **Tu Borrador**: un Teo a lápiz, sin terminar, con líneas de construcción visibles y sin color, salvo un listón gris. Cuando lo derrotas, se borra con una goma enorme que deja virutas.

---

## 12. EFECTOS FIRMA DE JEFES

Para cada jefe: arena, ataques firma con su glifo, transiciones de fase y muerte. **El Eco de Poder** (Señores fortalecidos por cada Señor caído) se ve como una **veta brillante de la podredumbre del color de los Señores ya derrotados** que recorre su cuerpo: cuantos más hayan caído, más vetas.

### 12.1 HESTRA MOLL — LA ANFITRIONA
- **Arena**: la mesa del banquete que se pierde en el horizonte; atardecer ámbar inmóvil; comensales grises masticando al fondo sin parar.
- **Ataques firma**:
  - **"Sírvase"** ◆: los seis brazos lanzan platos en ráfagas. La porcelana estalla y la comida que salpica **se vuelve ceniza gris al tocar algo** (comida hueca).
  - **"Bocado Eterno"** ◯: la boca del vientre aspira. Las partículas son *atraídas*: páginas, monedas y motas de vida salen de Teo hacia ella. Si se refuta, la aspiración se invierte y ella escupe luz dorada.
  - **"La Mesa Está Servida"** ▲: el mantel ondula por el suelo como una ola.
  - **"Hambre"** ✦: la máscara sonriente se agrieta y ella se lanza con la boca abierta.
- **Transición a la fase 2**: **la mesa se estira hasta el infinito**: un shader de perspectiva deforma el suelo, los platos se multiplican, el ámbar del cielo se oscurece y sus brazos pasan de seis a doce.
- **Fase 2, "Banquete Infinito"**: lluvia de platos desde el cielo en secuencias largas de Réplica, como un patrón de balas que se esquiva por ritmo.
- **Muerte**: la máscara cae y se rompe. Debajo, la cara cansada y humana de Hestra llorando. Por un instante **la comida se vuelve pan de verdad, caliente, humeante**. Luego todo el banquete se convierte en polvo dorado que flota. Al fondo, una puerta enorme de despensa se cierra con un golpe suave. El atardecer congelado **por fin avanza**: se hace de noche y aparecen las primeras estrellas.

### 12.2 BRANNOC FERRUM — EL SOL CAUTIVO
- **Arena**: plaza de forja bajo el sol febril; cielo blanco; distorsión de calor permanente; estatuas de metal de los trabajadores alrededor.
- **Ataques firma**:
  - **"Martillazo"** ◆: golpe pesado con lluvia de chispas que rebotan por toda la arena.
  - **"Fiebre"** ◯: una ola de luz febril que tiñe y deforma la pantalla. Al refutarla, se enfría en vapor azul.
  - **"Colada Ardiente"** ▲: río de bronce fundido por el suelo.
  - **"Mediodía"** ✦: el sol de su pecho se aviva y **la pantalla se blanquea por completo**; solo quedan siluetas. Hay que esquivar leyendo las siluetas.
- **Fase 2**: la armadura se agrieta, **el sol escapa de su pecho y sube al cielo**. La luz se vuelve tan dura que **desaparecen las sombras** (desorientación deliberada). Su cuerpo se enfría a bronce negro con grietas brillantes.
- **Fase 3 (con Eco de Poder)**: el sol baja hacia la arena para estrellarse; la pantalla se calienta progresivamente con distorsión creciente.
- **Muerte**: **el sol se pone por primera vez en mil años.** El cielo pasa de blanco a naranja, de naranja a violeta y de violeta a noche en 8 s. **Aparece la luna** en ese Pliegue y el medallón de la UI vuelve a mostrar una fase. Brannoc se enfría en una estatua de rodillas; las cintas de luto ondean con la primera brisa fresca; su martillo sigue brillando.

### 12.3 YSOLDE VANTELLE — LA GRAN CORRECTORA
- **Arena**: biblioteca imposible: escaleras al revés, libros flotando, estanterías que se pierden hacia arriba y hacia abajo.
- **Ataques firma**:
  - **"Raspado"** ◆: tajos de rasqueta que **borran partes del escenario**: donde golpean, el fondo pasa a papel en blanco.
  - **"Desmemoria"** ◯: si no se refuta, **borra temporalmente una habilidad del menú de Teo**: la ranura se raspa con polvo gris y el nombre desaparece letra por letra.
  - **"Nota al Pie"** ▲: bloques de texto caen desde arriba y se estrellan contra el suelo.
  - **"Corrección Total"** ✦: una goma gigante barre la pantalla. **El nombre de Teo en la HUD se borra** y queda "———" hasta el final de la fase.
- **Fase 2**: la arena se vuelve **papel en blanco**: solo quedan contornos a lápiz y no hay color. **Cada hechizo de Teo vuelve a pintar una parte de la arena** con su escuela. El jugador va recuperando el color del mundo mientras pelea.
- **Reescribir su nombre** (si se cumplen las condiciones): aparece la indicación *"Escribir su nombre"*. La cámara se acerca a la página en blanco de su cara. Teo escribe **Y-S-O-L-D-E** en pan de oro; cada letra le devuelve un rasgo (un ojo, una ceja, las arrugas, la sonrisa torcida). La figura altísima se encoge hasta ser la anciana pequeña con su taza de té. Las páginas que la envolvían salen volando como pájaros.
- **Muerte (si no se salva)**: se borra a sí misma por completo. Queda una silueta blanca y luego nada. Solo la taza de té cae y se rompe.

### 12.4 DIETRICH HALDEN — EL QUE NO CAE
- **Arena**: trinchera sobre una rama gigantesca, lluvia constante, y al fondo la guerra eterna en siluetas: soldados contra olas de podredumbre que nunca terminan.
- **Ataques firma**:
  - **"Carga del Mariscal"** ◆: combo de varios golpes con las espadas que lleva clavadas.
  - **"Estandarte"** ◯: alza el estandarte y crea un aura de arenga. Si se refuta, el estandarte **ondea hacia Teo** y el aura se transfiere.
  - **"Trinchera"** ▲: el suelo se abre en zanjas.
  - **"No Caeré"** ✦: recibe un golpe mortal y se levanta: las espadas clavadas se iluminan y **su barra de vida se rellena con madera de jade que crece**.
- **Transición**: Dietrich se arrodilla y se quita el yelmo. La Marea Pútrida sube. La cámara retrocede y revela la horda; la gradación de color se vuelve pútrida.
- **Fase de alianza contra la MADRE LARVA**: una reina-gusano colosal emerge del barro. Dietrich pelea junto a Teo con ataques de fuego de jade. Ataques de la Madre Larva: **enjambres de larvas** (boids), **escupitajo ácido** que corroe el suelo y **"Parto"** ✦ (una ola de crías que cubre la arena).
- **Muerte de la Madre Larva**: revienta en esporas que la lluvia lava. **La lluvia se detiene por primera vez** y entran rayos de sol entre el humo.
- **Muerte de Dietrich**: clava su espada en el suelo y se queda de pie. El estandarte se levanta con el viento. Le crecen flores de jade sobre la armadura hasta convertirlo en una estatua florecida. Al fondo, los soldados de la guerra eterna **se acuestan a descansar uno por uno**.

### 12.5 MIREYA SOLENNE — LA VOZ DEL CORO
- **Arena**: la copa-templo bajo la Luna Falsa, en noche eterna. Un coro de fieles enmascarados canta al fondo y hay nubes de polillas.
- **Ataques firma**:
  - **"Himno"** ◯: ondas de canto visibles como anillos plateados con letras. Refutarlo es una **contramelodía**: el libro de Teo emite notas doradas que cortan los anillos.
  - **"Velo de Polillas"** ◆: miles de polillas forman cuchillas.
  - **"Falsa Fase"**: el medallón lunar miente. **Algunos glifos de intención son FALSOS**: tienen un tinte verdoso casi imperceptible y su pulso no va al compás del ataque. El jugador atento los distingue.
  - **"Devoción"** ✦: la mirada de la Luna Falsa, un cono de luz enfermiza. Lo que toca queda bajo su control: un Semillado atrapado se cubre con una máscara de polilla.
- **Transición**: **la Luna Falsa abre su ojo**: la cara de luna se parte y un ojo enorme de larva mira a la cámara. El cielo se rasga.
- **Fase 2**: Mireya se vuelve una marioneta: hilos de seda van desde la luna hasta sus brazos y piernas.
- **Clímax**: la luna verdadera, tenue y lejana, **atraviesa el cielo con una grieta de plata real**. Mireya gira hacia ella. Los hilos se rompen. La Luna Falsa cae como una fruta podrida y estalla en polillas que **arden en la luz verdadera**.
- **Muerte**: Mireya se arrodilla bajo la luna verdadera. Su velo se deshace en polillas blancas y limpias que suben. Entrega **la Llave del Eclipse**: una llave de vidrio negro con un anillo de plata que brilla como la corona de un eclipse.

### 12.6 CORVAN — EL HEREJE (fase humana)
- **Arena**: la cámara del ritual. La Mesa de Piedra con Lys congelada en luz de plata. Antorchas rojo-violeta. Por un tiro hacia el cielo se ve el Gran Eclipse empezando.
- **Lenguaje visual**: **tinta de sangre** (§1.3). Corvan escribe en el aire con dos dedos.
- **Ataques firma**:
  - **"Edicto"** ◯: un pergamino de decreto se desenrolla y sus palabras se vuelven cadenas.
  - **"Plumas de Cuervo"** ◆: plumas de plata (como su broche) que vuelan como dagas.
  - **"Los Desaparecidos"** ▲: los nombres de las víctimas escritos en el suelo se levantan como espectros.
  - **"Sacrificio"** ✦: se corta la mano y detona un círculo de sangre.
- **Choque de Plumas**: cuando Teo y Corvan lanzan a la vez, los dos trazos (índigo-dorado contra rojo-negro) **chocan a mitad de pantalla**. La pantalla se divide por la mitad: tinta de Teo a la izquierda, tinta de Corvan a la derecha, empujándose. Se resuelve con un forcejeo de timing. Paneles de Manuscrito con los ojos de ambos.
- **Transición al Vaso**: la daga de su pecho late con un latido audible. Las astas de hongo brotan a cámara rápida. Las moscas salen de su toga como humo. El suelo de la arena se pudre.

### 12.7 EL VASO
- **Imagen**: Corvan estirado, con la capa de moscas y la corona de astas. **La cara humana, en el centro, está serena y llora lágrimas de plata**: lo último que queda de él.
- **Ataques**: **"Enjambre"** (las moscas forman cuervos, manos y caras); **"Esporada"** (el aire se llena de esporas, la imagen se vuelve granulada y verde); **"Corona"** (púas de asta brotan del suelo); **"Podrir"** (**la UI se pudre**: las barras de vida se llenan de moho y la tinta del tintero se vuelve violeta).
- **Transición a Sapros**: el suelo se hunde. **Secuencia de caída de 6 s**: la cámara cae con Teo atravesando capas de raíces que pasan a toda velocidad, con podredumbre bioluminiscente. Aterrizan sobre los anillos de Sapros.

### 12.8 SAPROS
- **Escala**: cámara alejada a 0,6×. Teo se ve diminuto. **Sapros nunca se ve completo**: la cabeza (boca de pétalos de dientes) y anillos que cruzan el fondo. Dentro de cada anillo translúcido flotan cosas que Orvalis se negó a dejar morir: libros, panes, armaduras, caras.
- **Cielo**: por un agujero lejano en lo alto se ve **el eclipse en totalidad**, con su corona roja.
- **Ataques**: **"Devorar"** ✦ (la boca-flor se abre y llena la pantalla); **"Ciclo"** ◯ (**todo lo que Teo hizo se deshace**: las calcomanías de la arena se rebobinan); **"Lluvia de Anillos"** ▲; **"Lo Conservado"** ◆ (de los anillos salen objetos que atacan).
- **Entrada de Lys**: una luz de plata atraviesa desde arriba. Lys desciende con alas hechas de polillas de luz. Técnica de dúo **"Luna y Tinta"**: Teo escribe y Lys ilumina; oro y plata juntos.
- **El Decreto del Rey**: la voz del Viejo Polilla resuena: *"Por decreto del rey..."*. Desde las paredes, **siluetas de guardianes de jade empujan** a Sapros.
- **Golpe final (final normal)**: un **Punto Final** a escala colosal cae sobre la cabeza de Sapros **justo cuando termina el eclipse**, con el anillo de diamante.
- **Final verdadero — Escritura Verdadera**: la pantalla entera se vuelve una página en blanco. **El jugador escribe la última frase** con indicaciones de entrada. La página se vuelve luz. El cuerpo de Sapros **se des-escribe** de Corvan. Sapros se encoge hasta ser un gusanito que vuelve a la tierra. La luna brilla más fuerte que nunca en todo el juego: el medallón de la HUD queda de plata pura.
- **Final malo**: Teo acepta. Su tinta se vuelve violeta, la UI se pudre por completo y la pantalla se funde a negro con moscas.

---

## 13. SEMILLADOS

- **Invocación**: una semilla cae del libro de Teo al suelo → se agrieta → brota → crece a cámara rápida (12 cuadros) → el Semillado se sacude la tierra. Los colores dependen del barrio donde se plantó.
- **Firmas de los iniciales**:
  - **Brotín** (Savia): escudo de hoja que ondula; cuchilla de hoja giratoria.
  - **Pavesa** (Brasa): cola con estela de brasas; estallidos de chispas al moverse.
  - **Lunilla** (Luna): polvo de polilla; las alas brillan con un tornasol plateado.
- **Evolución según el barrio**:
  1. El Semillado queda envuelto en un **capullo de corteza y raíces**.
  2. Las vetas del capullo brillan con el color del barrio.
  3. Latido (3 pulsos de luz).
  4. El capullo se agrieta y salen rayos de luz del color del barrio.
  5. Estallido de hojas, chispas, páginas, polillas o cristales de jade según el barrio.
  6. Pose final enmarcada en una **lámina de herbario** (ilustración botánica con su nombre y un nombre "científico" inventado).
- **Técnicas de Dúo** (Teo + Semillado): siempre con Paneles de Manuscrito; el trazo de Teo envuelve el ataque del Semillado.
- **KO**: el Semillado **se marchita hasta volverse semilla**, nunca muere visiblemente. Un brote pequeño queda latiendo hasta que lo reviven.

---

## 14. EFECTOS DE EXPLORACIÓN

Presupuesto menor (vista cenital, 640 × 360), pero con la misma gramática.

| Habilidad | Efecto |
|---|---|
| **Viento de Molino** | Una ráfaga levanta el abrigo de Teo; **las páginas de su libro forman alas** detrás de él; paja de trigo vuela alrededor; estela a lo largo del planeo; aterrizaje con soplo de paja. |
| **Martillo de Glifo** | Teo gira la pluma; se forma un glifo de martillo luminoso que golpea. Grietas, fragmentos de muro y polvo. Los braseros se encienden con chispas de Brasa. Los sellos de cera se derriten y gotean. |
| **Visión de Tinta** | Un anillo de tinta se expande desde Teo (barrido radial). Revela: textos de tinta invisible (brillan en azul), plataformas ocultas (contorno dorado punteado), muros falsos (parpadean). El resto del mundo se desatura un 40 % mientras está activa. |
| **Brote Guardián** | Una enredadera sale de la mano de Teo hacia un enchufe de semilla. El enchufe florece y el puente de enredadera crece segmento a segmento. En el gancho, líneas de velocidad hechas de hojas. |
| **Paso Lunar** | Transición entre el mundo real y el Mundo Velado: un **barrido vertical tipo página que se da vuelta**. El Mundo Velado se ve en plata y azul, con las sombras invertidas y plataformas de rayos de luna. Hay polillas por todas partes. El otro mundo se transparenta al 10 % como un eco. |
| **Escritura Verdadera** | Teo toca una palabra grabada; **las letras se levantan** de la superficie brillando; Teo las reescribe y las letras se reacomodan. El mundo cambia con una onda: si "CERRADO" pasa a "ABIERTO", la puerta de piedra se deshace en páginas. |
| **Atriles** | Brillo suave en reposo. Al descansar, el libro se abre, las páginas se agitan y baja un haz de luz de luna. La transición a un **Sueño de Plata** satura la pantalla de plata. |

---

## 15. MOMENTOS NARRATIVOS CON EFECTO PROPIO

| Momento | Efecto |
|---|---|
| **Nacimiento de Folio** | El Mapa de la Vigilia flota frente al árbol y **se dobla solo**: animación de origami en 24 pasos, cada pliegue marcado con una línea de luz de luna. Al final, dos círculos se recortan solos (los ojos) y se encienden en plata. |
| **El Mapa de la Vigilia** | En Merova, el papel parece en blanco. Cuando Teo *cree*, las líneas aparecen con tinta de luz que corre como agua por un cauce. |
| **Las Cartas del Hereje** | Una mancha violeta **traspasa la página del libro desde dentro**. Las palabras aparecen como si alguien escribiera del otro lado. Al leerlas, las letras se mueven un poco, como gusanos. **Romperla**: la carta se deshace en moscas que mueren al tocar la luz. **Guardarla**: se dobla y queda una mancha en el canto del libro. **Contestarla**: la tinta de Teo se vuelve violeta mientras escribe. |
| **Sueños de Plata** | Todo se vuelve vacío plateado con un suelo de agua que refleja. Lys se define un poco más en cada sueño (ver Dirección de Arte). Al despertar, escamas plateadas caen sobre Teo. |
| **Polillas del Viejo Polilla** | Siempre orbitan alrededor de él. Si hay luz de luna, brillan. En el momento lúcido de "*Lys... ¿dónde está mi hija?*", todas las polillas se posan sobre él a la vez y se encienden. |
| **La Floración de un barrio** (al liberar una sección) | La veta de color de la corteza del árbol late tres veces. Una **ola de color** avanza por el barrio: lo gris recupera su color con un borde de hojas y pétalos. Los edificios brotan. Los aldeanos sacuden escarcha plateada que cae en esquirlas. Los faroles se encienden uno por uno. 12 s guiados por la cámara, con la música creciendo. |
| **Apertura de las Entrañas** | Las cinco vetas de color recorren el tronco hasta el centro. **La corteza se abre como un libro** por el lomo. Una corriente de aire con polvo violeta sale del interior. |
| **El castillo congelado** | Guardias detenidos a media carrera, con partículas de polvo suspendidas en el aire alrededor de ellos. El jugador camina entre la escena congelada; al pasar junto a cada figura, el polvo se mueve apenas. |

---

## 16. PIPELINE TÉCNICO

### 16.1 Motor recomendado
**Godot 4.x** como opción principal: luces 2D con mapas de normales, partículas 2D por GPU, shaders de CanvasItem, AnimationPlayer para sincronizar efectos, sonido y cámara, y licencia libre. Alternativa: Unity con URP 2D si el equipo ya domina esa herramienta.

### 16.2 Estructura de render
- **Dos vistas compuestas**: (1) la **vista pixel** a resolución interna (640 × 360 en exploración o 960 × 540 en combate), escalada con vecino más cercano y siempre en múltiplos enteros; (2) la **vista HD** a resolución nativa para partículas finas, luces, bloom, distorsión y posproceso.
- Los sprites siempre se ajustan a la cuadrícula de pixel. Las partículas pueden ser HD o ajustarse a la cuadrícula según el efecto (modo **"crujiente"** para efectos que deben parecer dibujados).

### 16.3 Biblioteca de shaders
| Shader | Propósito | Parámetros clave |
|---|---|---|
| `ink_stroke_reveal` | Revelar un trazo a lo largo de su recorrido | `progress`, `edge_width`, `edge_color`, `noise_scale`, `wet_gloss` |
| `ink_ignite` | Mecha que enciende el trazo del inicio al fin | `ignite_progress`, `school_color`, `core_color`, `ember_noise` |
| `ink_bleed` | Mancha que se extiende y se seca | `spread`, `dry_amount`, `paper_tex` |
| `dissolve_pliegue` | Disolución con ruido por Pliegue (migas, raspado, grietas de enfriamiento, alas) | `amount`, `edge_color`, `edge_width`, `noise_tex` |
| `heat_distortion` | Refracción de calor con ruido en movimiento | `strength`, `speed`, `mask` |
| `shockwave` | Anillo de distorsión radial | `center`, `radius`, `thickness`, `strength` |
| `pixel_outline` | Contorno de 1–2 px según estado (objetivo, debilidad, Corrupción) | `color`, `thickness`, `pulse` |
| `palette_swap_lut` | Gradación por Pliegue y por estado (eclipse, Modo Papel, Corrupción) | `lut_a`, `lut_b`, `blend` |
| `paper_mode` | Sepia, grano de papel y contorno de lápiz por detección de bordes | `amount`, `grain`, `line_strength` |
| `woodcut_impact` | Cuadro de Impacto de Grabado | `threshold`, `ink_color`, `paper_color`, `accent_mask` |
| `amber_encase` | Refracción miel, burbujas y congelamiento de la animación | `fill`, `refraction`, `bubble_tex` |
| `mold_growth` | Crecimiento de moho guiado por mapa de flujo (mundo y UI) | `growth`, `flow_tex`, `color_ramp` |
| `moon_phase_sky` | Disco lunar con terminador, mordida de eclipse y corona | `phase`, `eclipse_amount`, `corona_intensity` |
| `starfield_fill` | Rellena un sprite con cielo estrellado animado | `density`, `twinkle_speed`, `tint` |
| `page_curl` | Transición de página que se da vuelta | `progress`, `curl_radius`, `back_tex` |
| `erase_scrape` | Borrado con raspones direccionales (la Correctora) | `progress`, `direction`, `scrape_tex` |
| `text_peel` | Letras que se despegan de un sprite | `progress`, `glyph_atlas`, `drift` |
| `chromatic_aberration` | Aberración radial con tope | `center`, `amount` (máx. 3 px a 1080p) |
| `godrays_2d` | Rayos de luz (conos aditivos con ruido) | `angle`, `intensity`, `noise_speed` |
| `hue_drain` | Radio que roba el color hacia la bilis | `center`, `radius`, `strength` |

### 16.4 Partículas, estelas y comportamientos
- **Partículas por GPU con subemisores**: chispa → rebote → brasa; gota → impacto → calcomanía.
- **Estelas**: cintas de malla para el listón de Teo, los proyectiles y el estandarte de Dietrich.
- **Boids**: moscas y polillas (máximo 300 en pantalla en PC/consola y 120 en móvil).
- **Calcomanías**: grupo reutilizable de sprites de mancha, quemado, ámbar y moho.

### 16.5 Luz
- Mapas de normales pintados a mano para Teo, Folio, los Semillados iniciales y todos los jefes; generados y retocados para tiles y enemigos comunes.
- **Máscaras emisivas** para lo que brilla por sí solo: la punta de la pluma, el horno de Brannoc, los ojos de Folio, la herida de Corvan.
- Oclusores de luz para sombras 2D.
- Cada efecto puede crear luces temporales. Presupuesto: **16 luces dinámicas en combate** (8 en móvil).

### 16.6 Producción de flipbooks
- Atlas de 4096 px. Convención de nombre: `vfx_[escuela]_[habilidad]_[fase]_[resolución].png` (ej.: `vfx_brasa_colada_impacto_hd.png`).
- **Pipeline de pixelización para fluidos**: simular humo o fuego en una herramienta de fluidos → renderizar a baja resolución → **cuantizar a la paleta del Pliegue o escuela** → limpiar a mano los cuadros clave en Aseprite. Así el fuego y el humo se ven pixel art pero se mueven con física real.

### 16.7 Datos y sincronía
Cada ataque tiene una **pista de eventos** en AnimationPlayer: inicio de anticipación, aparición del glifo, **cuadro de contacto**, hit-stop, señal de cámara, señal de audio y aparición de calcomanías. **El cuadro de contacto es la única fuente de verdad** para las ventanas de Réplica: si un artista mueve la animación, la ventana se mueve con ella.

### 16.8 Presupuesto de rendimiento (combate, 60 fps en PC y consola)
| Recurso | Límite |
|---|---|
| Tiempo de GPU para VFX | ≤ 4 ms por cuadro |
| Partículas simultáneas | ≤ 3 000 normalmente; ≤ 8 000 en picos de Iluminación |
| Sobredibujado en zonas calientes | ≤ 6× |
| Cadena de posproceso | ≤ 1,5 ms |
| Llamadas de dibujo | ≤ 400 |
| Luces dinámicas | ≤ 16 |
| Calcomanías persistentes | ≤ 64 |

### 16.9 Escalado a móvil
| Preset | Partículas | Bloom | Distorsión | Luces | Boids | Objetivo |
|---|---|---|---|---|---|---|
| **Alto** | ×1 | Media resolución | Sí | 16 | 300 | 60 fps en gama alta |
| **Medio** | ×0,5 | Cuarto de resolución | Simplificada | 8 | 120 | 60 fps en gama media |
| **Bajo** | ×0,25 | Horneado en los sprites | Sustituida por flipbooks | 4 | 60 | 30 fps estables |
- Escalado dinámico de calidad si el dispositivo se calienta.
- **Las Iluminaciones no se sustituyen por video**: en preset Bajo se eliminan capas de paralaje y partículas secundarias, pero se conserva la secuencia.

### 16.10 Herramientas sugeridas
Aseprite (pixel art y flipbooks), Krita o Photoshop (retratos e ilustraciones), un simulador de fluidos para generar bases de humo y fuego, y el editor de partículas y shaders del motor.

### 16.11 Opciones de accesibilidad visual
- **Reducir destellos** (ver §3.3).
- **Intensidad de sacudida** de 0 a 100 %.
- **Reducir movimiento**: sin cortes de cámara, Iluminaciones siempre en versión corta y sin Paneles de Manuscrito.
- **Glifos en alto contraste** y **tamaño de glifos** ajustable.
- Modos de daltonismo por LUT (los glifos ya se distinguen por forma).
- **Ventana de Réplica asistida**: el anillo de lectura se vuelve más grueso y lento (no cambia el efecto visual del acierto).

---

## 17. SINCRONÍA CON AUDIO Y MÚSICA

### 17.1 Capas de sonido por efecto
Cada efecto visual tiene su gemelo sonoro en tres capas:
1. **Transitorio** (0–30 ms): el golpe seco. **Debe caer a ±1 cuadro del contacto visual.**
2. **Cuerpo** (100–400 ms): el material (tinta, metal, madera, cristal).
3. **Cola** (reverberación, residuo): lo que queda en el aire.
- La anticipación lleva un **silbido ascendente** que sube de tono hacia el contacto.

### 17.2 Paleta de instrumentos por escuela
| Escuela | Sonido de efectos | Instrumentos en la música |
|---|---|---|
| Tinta | Raspado de pluma, papel, gotas | Arpa, pizzicato de cuerdas |
| Savia | Madera que cruje, miel que se estira | Flautas de madera, marimba |
| Brasa | Yunque, fuelle, siseo | Percusión metálica, tambores graves |
| Glifo | Páginas, campanillas | Celesta, susurros corales |
| Guardia | Cuernos, raíces, hojarasca | Cuernos graves, tambores de madera |
| Luna | Cristal, agua | Coro, armónica de cristal |
| Podredumbre | Insectos, chapoteos, respiración | Cuerdas desafinadas, drones |

### 17.3 Música adaptativa en combate
- Pistas por capas: base → **percusión** cuando la Inspiración pasa del 50 % → **coro** cuando llega al 100 %. El jugador "oye" cuándo está lista la Iluminación.
- **Réplica Perfecta**: golpe musical cuantizado al tiempo fuerte (margen de ±4 cuadros; la animación se estira o se acorta un poco para cuadrar).
- **Ruptura**: filtro de graves y caída de bajo durante 1,5 s.
- **Iluminación**: la música corta a un tema propio de 8 s que resuelve en el tiempo fuerte del tema de batalla.
- **Transiciones de fase de jefe**: esperan al final del compás (máximo 2 s); la animación de transición cubre la espera.

### 17.4 El silencio como herramienta
- Los paneles de la Réplica Perfecta: latido y una gota.
- **La Gran Correctora, fase 2: la música también se borra.** Los instrumentos desaparecen uno por uno hasta que solo queda un piano que Teo "repinta" con cada hechizo.
- Totalidad del eclipse: zumbido casi inaudible.

### 17.5 Leitmotivs
- **Tema de Orvalis**: el que tararea el Viejo Polilla.
- **Tema de Corvan** (violonchelo): **comparte las primeras cuatro notas con el de Orvalis**. Eran hermanos; la música lo sabe antes que el jugador.
- **Tema de Lys**: caja de música y armónica de cristal.
- **Tema de Sapros**: el tema de Orvalis tocado al revés y desafinado.

### 17.6 Vibración (control y móvil)
- Desviar: pulso corto y nítido.
- Réplica Perfecta: patrón de latido (dos pulsos) en los paneles y un golpe fuerte en el cuadro 70.
- Iluminación: vibración que crece hasta el golpe final.
- Eclipse: vibración grave y continua en la totalidad.

---

## 18. CHECKLIST DE CALIDAD (aprobación de un efecto)

Un efecto se aprueba solo si pasa **todas** las casillas, revisándolo a velocidad normal y a 0,25×.

**Lectura**
- [ ] La silueta del lanzador y del objetivo se lee en todo momento.
- [ ] El glifo de intención (en ataques enemigos) nunca queda tapado.
- [ ] El cuadro de contacto es inequívoco y coincide con la pista de eventos.
- [ ] Las partículas que cruzan la UI bajan su opacidad.

**Identidad**
- [ ] Si es de Teo, se ven los tres tiempos: Trazo, Ignición, Revelación.
- [ ] Usa como máximo tres tonos de su escuela + oro.
- [ ] No hay blanco puro (salvo núcleo de 1–2 px) ni negro puro.
- [ ] Sin leer el nombre, se entiende de quién es.

**Sensación**
- [ ] Hit-stop, sacudida y destello según las tablas.
- [ ] El sonido cae a ±1 cuadro del contacto.
- [ ] Tiene anticipación, impacto y residuo.
- [ ] El entorno reacciona según la tabla de materiales.

**Producción**
- [ ] Cumple el presupuesto de partículas, luces y GPU de su nivel.
- [ ] Tiene versión corta (Nivel III e Iluminaciones).
- [ ] Tiene variante para móvil (Alto, Medio y Bajo).
- [ ] Respeta las opciones de accesibilidad (destellos, sacudida, movimiento).

**La pregunta final**
- [ ] **¿Dan ganas de volver a verlo?** Si la respuesta es "más o menos", no está terminado.

**Aprobación**: líder de VFX + diseñador de combate + audio. Los jefes y las Iluminaciones también requieren la firma de dirección creativa.

---

## 19. ESTIMACIÓN DE VOLUMEN DE PRODUCCIÓN

| Bloque | Cantidad aproximada |
|---|---|
| Habilidades de Teo (todas las ramas del Árbol del Saber) | 120–150 efectos (muchos comparten base con variaciones de Glosa) |
| Iluminaciones | 7 secuencias (6 + la prohibida) |
| Remates Ilustrados | 6 variantes de escuela + 7 ilustraciones de jefe |
| Ataques de enemigos comunes | 40 familias × 2–3 ataques |
| Señores, Corvan, el Vaso, Sapros y la Madre Larva | 9 jefes × 6–10 ataques + transiciones + muertes |
| Semillados | Invocación, evolución por barrio y 2–3 habilidades por especie |
| Exploración | 6 habilidades + atriles + interactivos |
| Momentos narrativos | 8 secuencias (§15) |
| Shaders base | 20 (§16.3) |

**Orden de producción recomendado**: (1) gramática Tinta y Réplica, (2) Ruptura y Remate, (3) un Señor completo como prueba vertical (la Anfitriona), (4) las demás escuelas, (5) las Iluminaciones, (6) el resto de los jefes, (7) pulido y escalado a móvil.
