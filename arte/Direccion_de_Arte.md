# EL BIBLIOTECARIO — DIRECCIÓN DE ARTE

> Basado en `01_CANON.md`. Este documento define cómo se ve el juego. Los efectos visuales de combate tienen su propio documento: `Biblia_de_Efectos_Visuales.md`, que es la prioridad número uno de producción.

---

## 1. VISIÓN EN UNA FRASE

**"Un manuscrito iluminado que se pudrió y vuelve a florecer."**

Todo en *El Bibliotecario* debe parecer sacado de un libro antiguo muy querido: papel, tinta, pan de oro, sellos de cera, marcapáginas. La podredumbre de Sapros es lo contrario: humedad, moho, manchas, páginas que se deshacen. El jugador debe sentir, solo con mirar, cuándo un lugar está "escrito" (vivo, ordenado, Orvalis) y cuándo está "comido" (Sapros).

### Las tres capas visuales
| Capa | Dónde | Técnica | Sensación buscada |
|---|---|---|---|
| **Exploración** | Merova, viaje, Pliegues, aldea del árbol, Entrañas | Pixel art HD, vista 3/4 cenital, luz dinámica con mapas de normales, partículas en alta resolución | Diorama vivo y detallado, como las referencias de aldea y mazmorra, pero con luz de película |
| **Combate** | Arenas de batalla | Escenario diorama 2.5D en capas, sprites grandes pixelados, efectos híbridos (forma pixel + brillo HD) | Escenario de teatro de ópera: cada ataque es un número musical |
| **Retratos** | Diálogos, menús, El Cuento, fichas | Ilustración pintada estilo anime-fantasía, línea limpia, sombreado suave | Personajes expresivos, con la calidad de una ficha de personaje profesional |

### Diez reglas de oro
1. **La silueta manda.** Cualquier personaje o enemigo debe reconocerse en negro puro a 32 px de alto.
2. **La forma es pixel; el brillo es HD.** Los contornos y formas de sprites y efectos se dibujan a mano en pixel. La luz, el bloom, las partículas finas y la distorsión se renderizan a resolución nativa.
3. **Nunca blanco puro ni negro puro.** El "blanco" es papel (`#F2E8D5`); el "negro" es tinta (`#0E1030`).
4. **Un acento por pantalla.** Cada escena tiene un color dominante (el de su Pliegue) y un solo acento contrario.
5. **Orvalis es curvo; Sapros es caído.** Ver §6.
6. **Todo lo mágico de Teo empieza como tinta.** Sin excepción.
7. **La luz cuenta la historia.** En los Pliegues la fuente de luz siempre es el problema (el sol febril, la luna falsa, la luz de banquete que nunca cambia).
8. **El detalle va donde mira el jugador.** Personajes, puntos de interés e interactivos tienen el doble de detalle que el fondo.
9. **El mundo reacciona.** Lo que se quema queda quemado; lo que se restaura crece en pantalla.
10. **Belleza antes que horror.** Incluso lo pútrido tiene composición y paleta cuidadas; asquea por lo que es, no por lo mal que se ve.

---

## 2. RESOLUCIONES Y TAMAÑOS

### Exploración
| Parámetro | Valor |
|---|---|
| Resolución interna del arte | **640 × 360** |
| Escalado | ×2 (720p), ×3 (1080p), ×4 (1440p), ×6 (4K), siempre entero |
| Cuadrícula de tiles | 16 × 16 px; metatiles de 32 × 32 |
| Personajes jugables y NPC | 24 × 32 px (Teo 22 × 32; niños 18 × 24; Viejo Polilla 24 × 30, encorvado) |
| Enemigos en el mapa | 24 × 24 a 64 × 64 px |
| Señores vistos en el mapa | 96 × 128 px o más (aparecen de fondo) |
| Movimiento de cámara | Suavizado por subpíxel en la capa de render final; el arte siempre se ajusta a la cuadrícula de pixel |
| Luz | Luces 2D dinámicas, mapas de normales en todos los tiles y sprites principales, máscaras emisivas |

### Combate
| Parámetro | Valor |
|---|---|
| Resolución interna del arte | **960 × 540** (×2 = 1080p, ×4 = 4K) |
| Teo | 64 × 96 px |
| Semillados | 48 × 48 (fase 1), 80 × 80 (fase 2), 128 × 128 (fase 3) |
| Enemigos comunes | 64 × 64 a 160 × 160 px |
| Élites y minijefes | 160 × 220 a 256 × 256 px |
| Señores de los Pliegues | 320 × 480 a 512 × 512 px, armados en piezas (rig por partes) con capas independientes |
| Sapros | Fuera de escala: solo se ven fragmentos del cuerpo (cabeza 600 px, anillos que cruzan el fondo) |
| Capas del diorama | 7: cielo · lejano · medio-lejano · escenario · suelo de combate · primer plano · capa de efectos de pantalla |
| Efectos | Forma en pixel a 960 × 540; partículas, luz y post a resolución nativa |

### Retratos e ilustración
| Pieza | Tamaño |
|---|---|
| Retrato de diálogo (busto) | 1024 × 1024, mínimo 6 expresiones por personaje principal |
| Retrato de NPC menor | 768 × 768, 3 expresiones |
| Ilustración de ficha de personaje | 2480 × 3508 (A4 a 300 ppp) |
| Ilustración de evento (CG) | 3840 × 2160 |
| Arte de entrada en El Cuento | 1600 × 1200, estilo grabado coloreado a mano |

---

## 3. PALETAS (HEX)

### 3.1 Paleta global "Manuscrito"
| Nombre | HEX | Uso |
|---|---|---|
| Papel | `#F2E8D5` | El "blanco" del juego, destellos y fondos de menú |
| Papel sombra | `#D9C9A8` | Pliegues de página, bordes |
| Tinta | `#0E1030` | El "negro" del juego, contornos |
| Índigo de Teo | `#2B3170` | Abrigo de Teo, tinta brillante |
| Oro de iluminación | `#E8B04B` | Pan de oro, críticos, iluminaciones |
| Oro profundo | `#A8741F` | Sombra del oro |
| Plata lunar | `#C9D6E8` | Magia de luna, interfaz noble |
| Rojo listón | `#C8323C` | La bufanda-marcapáginas de Teo y acentos de peligro |
| Cera | `#8E1F2A` | Sellos y barra de postura |

### 3.2 Paletas por Pliegue
**Ámbar — El Banquete Hueco** (luz de atardecer fija, dorada, empalagosa)
| `#FFD98A` | `#F4A72C` | `#E07B1F` | `#A44E14` | `#5A2A0C` | `#2E140A` | acento enfermo: `#C9C76A` |
- La comida brilla demasiado (saturación alta), pero la gente es gris y desaturada. Ese contraste es la calamidad.

**Carmesí — El Mediodía Eterno** (sol febril, cielo blanco-amarillo, sombras rojo vino)
| `#FFF4D6` | `#FFC857` | `#FF6A2B` | `#C2272D` | `#7A1418` | `#2A080A` | bronce: `#B07A3A` / `#6E4520` |
- No existen sombras azules en este Pliegue: no hay cielo, no hay luna. Todas las sombras tiran a rojo.

**Índigo — El Palimpsesto** (biblioteca infinita, luz de vela fría y polvo suspendido)
| `#E9E1CC` | `#B6BFEF` | `#8FA2FF` | `#4B56C8` | `#2A2F7A` | `#0E1030` | borrado: `#9A9AA0` / `#C4C4C8` |
- Lo olvidado se pinta en grises sin tono. Lo recordado recupera color a manchas, como acuarela.

**Jade — El Frente Eterno** (trincheras entre ramas, niebla verde, cielo de humo)
| `#D8F5C6` | `#58C9A0` | `#1F8A70` | `#0E3B33` | barro: `#4A3B2A` | óxido: `#8C4A2F` | podre: `#7FA33A` |
- El jade limpio es Orvalis; el verde amarillento sucio es la Marea Pútrida. Nunca se tocan sin un contorno oscuro de por medio.

**Plata — El Santuario de la Luna Falsa** (noche eterna, nácar, una luna enorme)
| `#EEF3FA` | `#C9D6E8` | `#9FA9C4` | `#5E6A8A` | `#232A45` | `#0B0F1E` | luna falsa: `#DDE8B8` / `#B4C27A` |
- La luna verdadera es azul-plata fría. La luna falsa es plata con un tinte verde-hueso apenas perceptible. El jugador atento lo nota; el resto lo siente.

**Corazón — Las Entrañas** (violeta pútrido, bilis, carne)
| `#D4E05A` | `#9DB83A` | `#A8636B` | `#5B2A6E` | `#3A1F3D` | `#120A12` |
- La única luz limpia es la del cuerpo de Lys: plata pura `#EEF3FA`.

**Mundo presente — Merova y el viaje**
| Merova: `#E6C9A0` `#C49A6C` `#7E5A3C` `#3D2B22` | Mar de Sal: `#F5F2EA` `#D8D2C4` `#A9A08E` | Selva: `#2F6B3A` `#5E9A4A` `#1A3324` |

**Aldea de Orvalis restaurada (hub)**: cada barrio adopta su color de Pliegue, pero limpio y sano: el ámbar huele a pan, no a empalago; el carmesí es fragua, no fiebre. El árbol pasa de gris muerto (`#7D7A75`) a corteza viva (`#6B4A2B` con vetas del color de cada sección liberada).

### 3.3 Paletas por escuela de magia
| Escuela | Base | Media | Brillo | Núcleo | Contraste |
|---|---|---|---|---|---|
| **Tinta** | `#0E1030` | `#2B3170` | `#5A63D6` | `#E8B04B` (oro al encenderse) | `#F2E8D5` |
| **Savia** | `#8C5A1E` | `#F2A93B` | `#FFD27A` | `#FFF1C9` | `#3A2208` |
| **Brasa** | `#7A1418` | `#C2272D` | `#FF5A1F` | `#FFF4D6` | `#FFB000` |
| **Glifo** | `#2A2F7A` | `#4B56C8` | `#8FA2FF` | `#B6F0FF` | `#E9E1CC` |
| **Guardia** | `#0E3B33` | `#1F8A70` | `#58C9A0` | `#D8F5C6` | madera `#6B4A2B` |
| **Luna** | `#5E6A8A` | `#C9D6E8` | `#EEF3FA` | `#FFFFFF` solo en núcleo de 1–2 px | `#9FB4FF` |
| **Podredumbre** | `#3A1F3D` | `#5B2A6E` | `#9DB83A` | `#D4E05A` | carne `#A8636B` |

---

## 4. LUZ Y AMBIENTE

- **Sistema**: luces 2D con mapas de normales en todo sprite importante. Cada escena tiene tres luces mínimas: **clave** (la fuente narrativa), **relleno** (color complementario suave) y **contorno** (para separar al personaje del fondo).
- **Ciclo día-noche**: solo en la aldea del árbol y en el mundo presente. En los Pliegues la luz está congelada; esa inmovilidad se nota a propósito.
- **Neblina por capas**: cada capa del diorama recibe un tinte de atmósfera según su profundidad.
- **Polvo, polen, ceniza, esporas**: siempre hay partículas en el aire, distintas por zona (motas de harina en el Granero, chispas en la Forja, polvo de papel en el Palimpsesto, esporas en el Frente, escamas de polilla en el Santuario).
- **Rayos de luz**: rayos volumétricos falsos (sprites aditivos con ruido) en interiores con ventanas, raíces y bibliotecas.
- **Restauración**: cuando un barrio vuelve a la vida, se reproduce una secuencia de luz (ver Biblia de VFX, §16).

---

## 5. DISEÑO VISUAL DE PERSONAJES

### 5.1 Teo
- **Silueta**: triángulo (abrigo largo que se abre abajo) + una **línea roja ondulante** (la bufanda-marcapáginas). Esa línea es su firma: siempre se mueve, incluso en idle.
- **Rasgos**: 19 años, delgado, postura un poco encorvada de lector que se endereza en combate. Pelo castaño rojizo desordenado con un mechón que nunca baja. Lentes redondos de montura de latón. Pecas. Mancha de tinta permanente en el dedo índice derecho.
- **Ropa**: abrigo índigo de estudiante (`#2B3170`) con forro papel, una docena de bolsillos de los que asoman marcapáginas de colores; camisa crema; pantalón café; botas de viaje gastadas. Morral de cuero lleno de libros con un tintero colgando.
- **La bufanda-marcapáginas**: listón de seda roja (`#C8323C`) de 2,5 veces su altura, con el borde deshilachado y una borla dorada. En combate actúa como capa: dibuja estelas, se tensa en las Réplicas y es lo último en quedarse quieto.
- **Arma (Pluma)**: báculo largo rematado en una pluma enorme con punta de metal. La punta deja un trazo de tinta flotante al moverse.
- **Evolución visual**: con cada sección liberada, Teo gana un detalle permanente en su atuendo: espiga de trigo en el ojal (Ámbar), guardas de bronce en los guantes (Carmesí), lentes con runas grabadas (Índigo), hoja de jade en la borla (Jade), hilo de plata en el listón (Plata). Al final del juego, su atuendo cuenta su viaje.
- **Corrupción**: en niveles altos, manchas de moho en el abrigo, el listón se vuelve morado y las puntas de los dedos se oscurecen.

### 5.2 Folio
- Lechuza de origami de papel envejecido con el **mapa todavía visible** en sus alas (rutas punteadas, la rosa de los vientos en el pecho).
- Ojos: dos círculos recortados por donde se ve la luz de detrás (en la oscuridad brillan plata: pista de que es Vela).
- Animación: aletea con sonido de páginas; se despliega parcialmente cuando se asusta (vuelve a ser un mapa a medias); se arruga cuando se enoja.
- Tamaño en exploración: 12 × 12 px, volando sobre el hombro de Teo. En retrato: busto expresivo pese a ser papel (los pliegues cambian para formar cejas).

### 5.3 El Viejo Polilla (rey Aldemar)
- Silueta: curva de signo de interrogación (espalda encorvada, bastón alto).
- Barba blanca larguísima con polillas dormidas en ella; ojos nublados con un brillo plateado.
- Capa harapienta y remendada; en la espalda, un escudo bordado casi borrado: **lechuza plateada sobre un árbol**.
- Una **jaula de pájaro vacía** colgada del bastón; la puerta está abierta.
- Las polillas lo orbitan siempre: 3–6 sprites de 3 px que se iluminan al acercarse a fuentes de luz de luna.
- **Recuerdos jugables (rey joven)**: Aldemar a los 31 años con armadura de corteza y plata, capa azul noche, corona de corteza con incrustaciones de piedra lunar y barba corta castaña. Al ver al rey joven y luego al viejo, el jugador debe sentir el peso de los mil años.

### 5.4 Princesa Lysandra "Lys"
- **En los Sueños de Plata**: figura de luz plateada que poco a poco se define. Primeros sueños: solo contorno y ojos. A mitad del juego: rostro, pelo negro azulado largo y suelto, túnica de novicia blanca. Al final: color completo y expresiones propias.
- **Con su ropa real** (retrato del castillo y batalla final): chaqueta corta de esgrimista azul medianoche con bordados de constelaciones, falda pantalón para moverse, astrolabio colgado del cinturón y florete fino de plata. Mirada desafiante.
- **Con Ilunara dentro**: los ojos se vuelven completamente plateados y le flota sobre la cabeza un halo creciente.

### 5.5 Corvan Edrys
- **Humano (recuerdo del Vado Albar, retrato del castillo)**: 31 años, alto, elegante, guapo de manera severa, pelo negro peinado hacia atrás, ojos grises. Toga negra con forro violeta y bordados de plata, **broche de cuervo de plata**. Gesto característico: escribir en el aire con dos dedos.
- **El Hereje (Entrañas, 49 años)**: demacrado, pómulos marcados, pelo con canas largas. La toga está podrida en los bordes y le crecen hongos en los hombros. La daga de hueso sigue clavada en su pecho y la herida late con luz verde-bilis. Una corona de astas de hongo le está empezando a brotar.
- **El Vaso**: se le estira el cuerpo (2,5 veces la altura humana), las astas de hongo se ramifican como un candelabro y un enjambre de moscas forma una segunda capa, como una capa de humo negro. La cara humana queda en el centro, serena y llorosa: **esa contradicción es la clave del diseño**.
- **Sapros**: gusano colosal de anillos translúcidos. Dentro de cada anillo hay cosas que Orvalis "conservó": libros, panes, armaduras, rostros. La boca es una flor de dientes que se abre en pétalos. Nunca se ve completo.

### 5.6 Los Señores de los Pliegues
Cada Señor tiene **retrato humano** (en recuerdos, El Cuento y la galería del castillo) y **forma de Señor** (combate). La forma de Señor siempre conserva un detalle humano reconocible: el punto de compasión.

| Señor | Retrato humano | Forma de Señor | Detalle humano que conserva | Forma dominante |
|---|---|---|---|---|
| **Hestra Moll → La Anfitriona** | Mujer robusta de 52 años, mejillas rosadas, delantal sobre traje de tesorera, llavero enorme de graneros al cinto | Matrona colosal cuya parte inferior es una mesa de banquete infinita; seis brazos sirviendo; pelo de espigas de trigo; máscara de porcelana sonriente; boca vertical en el vientre que respira | **El llavero de graneros** cuelga de su cintura gigante | Óvalo / círculo (abundancia que se vuelve gula) |
| **Brannoc Ferrum → El Sol Cautivo** | Coloso de 60 años, calvo, barba trenzada quemada, delantal de cuero, brazos cubiertos de cicatrices | Gigante de bronce fundido que gotea; pecho abierto como horno con un pequeño **sol febril** en jaula de costillas; martillo de luz sólida | **Dos cintas de luto** atadas a la muñeca (por sus hijos) que nunca se queman | Cuadrado con un círculo en el centro (masa y núcleo) |
| **Ysolde Vantelle → La Gran Correctora** | Anciana pequeña de 70 años, parche en un ojo, chal de lana, gafas en la nariz y taza de té | Figura altísima y delgada envuelta en tiras de pergamino, con una página en blanco por cara, dedos de rasquetas de palimpsesto y corona de plumas de escribir | **La taza de té**, flotando a su lado, todavía humeante | Líneas verticales (columnas, estanterías) |
| **Dietrich Halden → El Que No Cae** | Hombre de 55 años, mandíbula cuadrada, cicatriz que le parte la boca, armadura de mariscal de corteza y acero | Centauro de madera y acero fundido con un Semillado deformado, cubierto de espinas de jade, con decenas de espadas clavadas y el estandarte de Orvalis desgarrado en la espalda | **El yelmo de mariscal**, abollado, que aún se quita para hablar | Triángulos y púas (resistencia agresiva) |
| **Mireya Solenne → La Voz del Coro** | Mujer de 50 años, serena y bella, pelo plateado trenzado, velo de sacerdotisa y voz de soprano | Sacerdotisa alta cuyo velo se deshace en miles de alas de polilla; a su espalda flota **la Luna Falsa** (una larva enorme con cara de luna y anillos de capullo) | **El rosario lunar** que le regaló Lys, con una cuenta rota | Medialuna y velo (curvas que envuelven) |

### 5.7 Otros
- **Zahra**: piel morena curtida por el sol, cicatriz en la mejilla izquierda, turbante color arena con cuentas de escarabajo, abrigo largo de caravanera, sable curvo y una flauta de caña a la espalda. Siempre lleva algo en las manos (fruta, cuerda, monedas).
- **Rosalba**: anciana alta y huesuda, moño apretado, lentes de media luna colgando de una cadena, cárdigan gris con parches, pañuelo rojo (el mismo rojo del listón de Teo: ella se lo dio).
- **Maestro Fennick**: cincuentón pulcro, barba de candado, túnica dorada del Colegio Arcano con soles de Kesh bordados, monóculo.
- **Nico**: niño de 8 años, gorra enorme, rodillas raspadas, un libro ilustrado que no sabe leer.
- **El Encuadernador**: figura alta encapuchada en una capa de cuero encuadernado y cosido con fibras de raíz; manos de corteza clara que asoman con aguja e hilo. **No proyecta sombra** (regla técnica: su sprite no recibe la máscara de sombras). Al quitarse la capucha (final verdadero): rostro de mujer joven idéntico a la estatua de Valis, con ojos de savia dorada.
- **Ilunara**: nunca se ve completa. Una silueta femenina inmensa hecha de luz y negativo de estrellas, con un ojo cerrado. Se representa más con luz que con forma.
- **Vela, la Lechuza Blanca**: lechuza gigante de plumas como láminas de luz lunar, ojos de luna llena. Folio transformado.

---

## 6. LENGUAJE DE FORMAS Y SILUETAS

| Facción | Formas | Líneas | Composición |
|---|---|---|---|
| **Orvalis** | Círculos, medialunas, curvas de rama, arcos ojivales que imitan hojas | Fluidas, con remates en espiral de helecho | Simétrica pero orgánica |
| **Sapros** | Óvalos caídos, agujeros, espirales hacia abajo, asimetría | Que cuelgan, gotean y se curvan hacia el suelo | Rota, desbalanceada, con peso abajo |
| **Kesh / Khar** | Triángulos, rayos de sol, rectángulos | Rectas y radiales | Rígida y jerárquica |
| **Semillados** | Bellota, semilla, hoja (formas "de juguete" en su primera etapa, más arquitectónicas al evolucionar) | Redondeadas | Centro de gravedad bajo y amigable |

**Prueba de silueta obligatoria:** todo enemigo nuevo pasa por una hoja de siluetas negras junto a los demás enemigos de su Pliegue; si dos se confunden, uno se rediseña.

**Indicadores de lectura rápida en combate:**
- Ataque físico inminente: el enemigo se ilumina por el borde con el color del glifo ◆.
- Conjuro inminente: el enemigo levanta un círculo de glifos ◯ a sus pies.
- Ataque de área a ras de suelo: el suelo se agrieta con la forma ▲.
- Imparable: aura de páginas rasgadas ✦ y un sonido distinto.

---

## 7. INTERFAZ (UI)

La interfaz es **un escritorio de bibliotecario**: papel, cuero, latón, cera, tinta. Nada de plástico ni de neón.

### 7.1 Tintero de PA
- Esquina inferior izquierda: **tintero de cristal** con hasta 6 gotas visibles (más si las pasivas lo amplían; el tintero se agranda con un anillo de latón extra).
- Al ganar PA cae una gota desde la pluma con salpicadura. Al gastarlos, la tinta sube por la pluma de Teo (conecta la UI con el sprite).
- Las PA sin usar al final del turno brillan suavemente para invitar a gastarlas.
- **En Eclipse**: la tinta se seca y aparecen costras negras en las gotas; las habilidades lunares se muestran craqueladas.

### 7.2 Glifos de Intención
| Glifo | Forma | Color | Defensa |
|---|---|---|---|
| ◆ | Rombo sólido | Oro `#E8B04B` | Desviar |
| ◯ | Círculo con un ojo | Plata `#C9D6E8` | Refutar |
| ▲ | Triángulo apuntando hacia abajo, con grieta | Rojo `#C8323C` | Saltar |
| ✦ | Estrella de cuatro puntas rasgada | Blanco papel con borde negro | Solo esquivar |
- Diseñados para leerse por **forma**, no por color (accesibilidad para daltonismo).
- Aparecen sobre la cabeza del enemigo y repiten el pulso del tempo del ataque: el glifo late al ritmo exacto en que vendrá el golpe.

### 7.3 Línea de iniciativa
- Arriba de la pantalla: un **listón de marcapáginas** horizontal con pestañas de papel que llevan el retrato de cada actor. La pestaña activa sobresale.
- Las habilidades que cambian el orden mueven las pestañas con animación de página que se reacomoda.

### 7.4 Barra de Postura
- Un **sello de cera** bajo cada enemigo. Al recibir daño de postura aparecen grietas en el sello; en la Ruptura el sello estalla en fragmentos rojos.

### 7.5 Inspiración
- El **marco de la pantalla** se va dorando poco a poco con motivos de manuscrito iluminado (enredaderas, letras capitulares). Cuando el marco se completa, la letra capitular de la esquina superior izquierda se enciende: la Iluminación está lista.

### 7.6 Fase lunar
- Medallón en la esquina superior derecha con la fase actual y un contador de turnos hasta el cambio. En Eclipse, el medallón se tapa con un disco negro con corona roja.

### 7.7 Corrupción: el moho que invade la UI
| Nivel | Efecto en la interfaz |
|---|---|
| 0 | Interfaz limpia |
| 1 | Manchas de humedad en las esquinas del papel |
| 2 | Moho verde-bilis creciendo en los bordes del tintero y del menú; alguna mosca cruza la pantalla en los menús |
| 3 | El moho cubre partes del texto; la tipografía de Teo se vuelve más angulosa; los íconos de Orvalis se oscurecen |
| 4 | El marco de Inspiración se pudre (las Iluminaciones se vuelven "Iluminaciones Negras"); los glifos de intención a veces aparecen con letras de Corvan |
- Todo el moho se anima con un shader de crecimiento por mapa de flujo (ver Biblia de VFX, §15). Purificarse en el Sanatorio del Templo retrae el moho con una animación de luz.

### 7.8 El Cuento (códice)
- Libro abierto a pantalla completa, a dos páginas. **Izquierda: "Lo que dice el cuento"** (tipografía de libro infantil, ilustraciones de grabado amable y colorido). **Derecha: "Lo que fue"** (letra manuscrita, ilustración más realista y oscura).
- Cuando se descubre una verdad, la página derecha **se escribe sola** frente al jugador: la tinta corre y la ilustración se pinta por capas.
- Marginalia en **Glifo Lunar** (letra del Viejo Polilla) visible solo con Visión de Tinta.

### 7.9 Tipografía
- **Títulos**: serif alta de inspiración incunable con letras capitulares decoradas.
- **Texto de diálogo**: serif humanista muy legible.
- **Voz de Teo en notas y cartas**: manuscrita ligera.
- **Cartas del Hereje**: caligrafía elegante y alargada en tinta violeta-negra que mancha la página.
- **Glifo Lunar**: alfabeto propio de 24 signos curvos, formados por medialunas y puntos (se diseña como fuente).

---

## 8. FICHAS DE PERSONAJE (formato oficial)

Las fichas son piezas de comunicación (redes, prensa, libro de arte) y guía interna. Se inspiran en la *estructura* de la ficha de referencia, pero con identidad propia de manuscrito:

```
┌───────────────────────────────────────────────────────────────┐
│ [NOMBRE EN SERIF ALTA, tinta índigo]          [chibi en marco] │
│ [3 miniaturas de expresión]                   [ícono de rol]   │
│                                                               │
│ ▌Presentación          [ILUSTRACIÓN PRINCIPAL      │ ▌Personaje│
│  Párrafo corto de       DE CUERPO ENTERO, pose     │  Turnaround│
│  quién es y su papel.   característica y efecto    │  frente/   │
│                         de su escuela]             │  perfil/   │
│ ▌Habilidad                                         │  espalda   │
│  [4 íconos circulares]                             │  a lápiz   │
│  Ataque: ...                                       │            │
│  Defensa / Réplica: ...                            │ ▌Equipo    │
│                                                    │ [3–5 props]│
│ [sello de cera de Orvalis]   [listón rojo cruzando el pie]     │
└───────────────────────────────────────────────────────────────┘
```
- Fondo: papel `#F2E8D5` con textura de fibra y una mancha de tinta en una esquina.
- Rótulos de sección: sobre una franja de cuero índigo `#2B3170` con letras papel.
- Cada ficha lleva al pie una línea en Glifo Lunar con una pista de lore (para la comunidad).
- Fichas obligatorias: Teo, Folio, Lys, Viejo Polilla, Corvan (las 3 formas), los 5 Señores (humano + Señor), Zahra, los 3 Semillados iniciales.

---

## 9. GUÍA DE ANIMACIÓN

### 9.1 Ritmo general
| Contexto | FPS de dibujo | Notas |
|---|---|---|
| Exploración: caminar y correr | 10 fps (caminar 6 cuadros, correr 8) | El listón de Teo se anima a 12 fps aparte |
| Exploración: idle | 6 fps, ciclo de 8–12 cuadros con respiración | Folio aletea cada 3–5 s |
| Combate: idle | 8 fps, 8 cuadros | Respiración + listón + brillo de la pluma |
| Combate: ataques | 12–24 fps variables, con **cuadros sostenidos** en las poses clave | La anticipación se sostiene y el impacto se dibuja en 1–2 cuadros |
| Efectos dibujados | 24 fps | Se pueden duplicar cuadros para 12 fps en estilo "golpe seco" |

### 9.2 Principios obligatorios
- **Anticipación clara**: cada ataque enemigo tiene una pose de anticipación legible de al menos 18 cuadros a 60 fps (0,3 s) antes del golpe, sincronizada con el glifo de intención. Esto es esencial para la Réplica.
- **Cuadros de difuminado (smear)**: en golpes rápidos, 1–2 cuadros de difuminado deformado en lugar de desenfoque.
- **Squash & stretch en pixel**: se permite deformar ±15 % en impactos y saltos.
- **Movimiento secundario**: listón, capas, barbas, velos, polillas. Se anima a mano en las poses clave y con física 2D (cadena de 6–10 segmentos) en idle y transiciones.
- **Mirada**: los personajes miran hacia donde va a ocurrir la acción un instante antes que el cuerpo.

### 9.3 Lista mínima de animaciones de combate
| Actor | Animaciones |
|---|---|
| **Teo** | idle · listo (inicio de turno) · ataque básico ×3 variaciones · conjuro nivel I / II / III · canalizar · Iluminación (entrada y pose final) · recibir golpe leve / fuerte · Esquivar · Desviar · Refutar (3 cuadros por glifo) · Saltar · Réplica Perfecta · usar objeto · Transcribir · aturdido · KO · victoria · derrota (se arrodilla abrazando el libro) |
| **Semillados** | idle · ataque · habilidad ×2 · golpe recibido · desviar (su versión) · KO · evolución · victoria |
| **Enemigos comunes** | idle · anticipación ×tipos de ataque · ataque ×2–3 · golpe recibido · ruptura (aturdido) · muerte (que se deshace según su Pliegue) |
| **Señores** | idle por fase · 6–10 ataques con anticipaciones únicas · golpe recibido (por partes) · ruptura · transición de fase (cinemática) · muerte (cinemática) |

### 9.4 Muertes por Pliegue (cómo se deshacen los enemigos)
- **Ámbar**: se desmoronan en migas doradas que nadie recoge.
- **Carmesí**: se enfrían de golpe: el bronce pasa de blanco a negro y se rompe.
- **Índigo**: se borran de arriba abajo como goma sobre papel y dejan un rastro gris.
- **Jade**: caen, intentan levantarse y finalmente se quedan quietos; brotan flores de jade (liberados).
- **Plata**: el velo se cae y queda solo un capullo vacío que se convierte en polillas.
- **Entrañas**: se licúan en podredumbre que la luz de Lys evapora.

### 9.5 Restauración en la aldea
- Los edificios restaurados **crecen**: brotan como plantas en una secuencia de 3–4 segundos y luego aparecen los detalles (tejas, ventanas, faroles). Los aldeanos despiertan sacudiéndose escarcha plateada.
