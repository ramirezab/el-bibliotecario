# SEMILLADOS — LAS CRIATURAS GUARDIANAS

> Documento de diseño de sistemas. Depende de `01_CANON.md` (§4, §8 y §11) y de `sistemas/Combate_y_Replica.md`.
> Cifras de primera versión.

---

## 1. Qué son (lo que el juego le cuenta al jugador)

Los **Semillados** son criaturas que brotan de las semillas del árbol de Orvalis. Aparecieron por primera vez hacia el 150 AO, durante un ataque de saqueadores (*la Primera Floración*). En el 412 AO, durante la **Noche de las Mil Semillas**, mil de ellos salvaron al reino del Imperio de Khar. El más famoso, **Madreroble**, mató al emperador Kassar Vhal.

Un Semillado no es una mascota: es **un guardián que eligió proteger**. Por eso no se "captura". Se **planta**, se **cría** o se **rescata**.

**Regla de oro del sistema:** *la tierra donde se planta una semilla decide en qué se convierte.* Una misma semilla da un guardián distinto en la Forja que en la Biblioteca, porque el árbol "aprende" del barrio que lo rodea.

> Nota para guion: Nana Brote lo explica así: *"Las semillas escuchan. Si las plantas junto al horno, sueñan con fuego. Si las plantas entre libros, sueñan con palabras."*

---

## 2. Ciclo de vida

```
SEMILLA ──(germinar)──> ETAPA 1: Brote
        ──(nivel 14 + Lealtad 1, en cualquier atril)──> ETAPA 2: Retoño
        ──(nivel 30 + Lealtad 2 + 3 Savia de Jade, replantado en una Parcela)──> ETAPA 3: Guardián
```

### 2.1 Conseguir semillas
| Fuente | Qué da | Notas |
|---|---|---|
| **Elección inicial** (Acto I, en la Antesala) | Brotín, Pavesa o Lunilla | Las otras dos semillas iniciales se pueden conseguir más tarde (ver §6.1) |
| **Semillas Dormidas** | Semillas comunes del Pliegue | Vainas brillantes incrustadas en paredes, raíces y ruinas. 3–5 por Pliegue |
| **Rescate** | La semilla de un Semillado Corrompido | En combate, al dejar en Ruptura a un Semillado Corrompido, el Remate Ilustrado cambia a **Rescatar**: el guardián se purifica y suelta su semilla |
| **Nana Brote** | Semillas raras | Regalos al subir el Vivero y misiones del Bastión |
| **Caravana de Zahra** | Semillas silvestres del exterior | Inventario rotativo (Salinito, Raicita) |
| **El Encuadernador** | Semillas extrañas | Las de dos etapas (Ratón de Biblioteca, Hongo Amable…) |
| **Semillas de Señor** | Un Semillado legendario por Pliegue | Aparece en el barrio restaurado tras vencer a su Señor |
| **Secreto** | Gusarapo | Las Entrañas (ver §6.4) |

#### Correspondencia: semillas nombradas en los Pliegues → líneas del roster
Los documentos de cada Pliegue nombran sus semillas por su apariencia. Esta tabla dice qué línea del roster sale de cada una.

| Semilla (nombre en el Pliegue) | Dónde | Línea que germina |
|---|---|---|
| Semilla de Espiga | Pliegue Ámbar · recompensa de Tobías | **Espiguín** (#4) |
| Semilla de Cuna | Pliegue Ámbar · el Ánima Famélica (Ilda Moll) | **Calabacín** (#6) |
| Semilla Melífera | Pliegue Ámbar · silo agrietado de los Bancales | **Panalito** (#5) |
| Semilla Brasera | Pliegue Carmesí · recompensa del Abuelo Fuelle | **Fuellecito** (#7) |
| Semilla de Escoria | Pliegue Carmesí · Arsenal Infinito | **Chispilla** (#9) |
| Semilla de Temple | Pliegue Carmesí · fondo de la Pila de Temple | **Yunquín** (#8) |
| Semilla de Lacre | Pliegue Índigo · recompensa de Hermano Glosa | **Lomito** (#11) |
| Semilla de Índice | Pliegue Índigo · recompensa de los Gemelos | **Ratón de Biblioteca** (#19; también la vende el Encuadernador) |
| Semilla de Tintero | Pliegue Índigo · Sala de los Errores | **Gotín** (#10) |
| Semillas Heridas (3) | Pliegue Jade · para Nana Brote | **Musguito** (#12), **Cardillo** (#13) y **Oseznillo** (#14, línea de Madreroble) |
| Madreselvita | Pliegue Jade · si se purifica a Madreselva | Forma bebé especial de **Madreselva** (fuera del roster numerado; mismo esquema que una línea de tres etapas de Savia) |
| Rescate del Guardián de Nácar | Pliegue Plata · élite corrompido | **Ciervito de Corteza** (#24) |
| Semillas Dormidas del Plata | Pliegue Plata · vainas en el Jardín de Nácar | **Rocío** (#15), **Hilillo** (#16) y **Corderito Lunar** (#21) |

### 2.2 Germinar
- **Acto I:** solo existe la **Maceta Antigua** de la Antesala: 1 semilla a la vez y germina tras **1 Jornada** (cada vez que Teo descansa en un atril o vuelve al árbol).
- Cuando un barrio se libera, aparece su **Parcela**: un huerto con tierra de ese barrio (2 espacios; con mejoras, hasta 4). Las Parcelas germinan en 1 Jornada.
- **Tras liberar el Bastión:** el **Vivero de Nana Brote** permite germinar varias semillas a la vez, acelera el crecimiento y abre funciones avanzadas (§5).

### 2.3 Etapa 2 (Retoño)
- Requisitos: **nivel 14 y Lealtad 1**.
- Se hace en **cualquier atril**. Es la misma forma para todas las semillas de la misma línea.
- La animación: el Semillado se envuelve en hojas, la pantalla se llena de polen dorado y sale el Retoño.

### 2.4 Etapa 3 (Guardián): la decisión importante
- Requisitos: **nivel 30, Lealtad 2 y 3 Savia de Jade**.
- El Retoño **se replanta en la Parcela de un barrio liberado**. Esa tierra decide su forma final:

| Tipo de línea | Regla |
|---|---|
| **Iniciales** (Brotín, Pavesa, Lunilla) | **5 formas finales posibles**, una por barrio |
| **Comunes** | **2 formas finales**: la **natural** (en su barrio de origen) y la **cruzada** (en su barrio afín). En cualquier otro barrio la semilla "se niega a soñar" y Nana Brote lo explica |
| **De dos etapas** | No tienen Etapa 3 |
| **Legendarios** | No evolucionan |

- **Cambiar de opinión:** en el Vivero, con *Replantar*, se puede cambiar la forma final de un Guardián por **1 Lágrima de Luna**. Conserva su nivel, su Lealtad y sus habilidades aprendidas.

---

## 3. Estadísticas

### 3.1 Las seis estadísticas
PV (vida) · ATQ (ataque físico) · POD (poder mágico) · DEF (defensa) · RES (resistencia mágica) · VEL (velocidad).

```
Estadística(L) = floor(Base × (1 + 0.06 × (L − 1)))
PV(L)          = floor(Base_PV × 3 × (1 + 0.06 × (L − 1)))
```

| Etapa | Suma de bases (aprox.) | Ejemplo a nivel 45 (PV) |
|---|---|---|
| Etapa 1 | 300 | 400–600 |
| Etapa 2 | 420 | 550–800 |
| Etapa 3 | 540 | 700–1050 |
| Legendario | 580 | 800–1100 |

- Los Semillados tienen **menos vida que Teo**, pero mejores estadísticas especializadas.
- **Nivel:** comparten la XP de Teo: 100 % los activos y 50 % los de la banca (100 % con *Raíz Compartida*). Su nivel nunca supera el de Teo.

### 3.2 Roles
| Rol | Reparto típico | Para qué sirve |
|---|---|---|
| **Atacante** | ATQ o POD altos, VEL media | Daño |
| **Protector** | PV y DEF/RES altos, VEL baja | Provocación y escudos |
| **Sanador** | POD y RES altos | Curas y quitar estados |
| **Controlador** | VEL y POD | Estados alterados y manipular la iniciativa |
| **Apoyo** | VEL alta | Mejoras al grupo, dar PA y quitar mejoras enemigas |

### 3.3 Habilidades
- Cada Semillado tiene **4 habilidades equipadas** de su lista (aprendidas por nivel, por Tomos de Brote y por Injertos).
- Usan **su propia reserva de PA**: máximo 5, empiezan con 2 y ganan +2 por turno.
- Toda línea tiene una **Habilidad Firma** que solo aprende ella.
- En **Etapa 3** aprenden su **Habilidad de Guardián** (la más fuerte), que depende de la forma final.
- **Modo automático:** se puede dejar a cualquier Semillado en "Instinto" (IA con prioridades configurables: Atacar / Proteger / Curar / Equilibrado).

---

## 4. Lealtad (0 a 5 corazones)

### 4.1 Cómo sube
| Acción | Puntos |
|---|---|
| Ganar un combate como activo | +1 |
| Ganar con Matrícula de Honor sin que se Marchite | +3 |
| Defenderlo con una Réplica Perfecta | +1 |
| Comida de Berta compartida (en el Granero) | +5 (una vez por Jornada) |
| Regalo de su **comida favorita** | +8 (una vez por Jornada) |
| Cuidados en el Vivero (regar, cepillar, jugar) | +2 por Jornada |
| Que Teo lo reviva en combate | +2 |

### 4.2 Umbrales
| Corazones | Puntos acumulados | Efecto |
|---|---|---|
| 0 | 0 | Ventanas de Réplica **−2 frames** al defenderlo. A veces ignora órdenes (5 %) |
| 1 | 20 | Ventana normal. Permite la Etapa 2 |
| 2 | 50 | +1 frame. Permite la Etapa 3 |
| 3 | 100 | 10 % de aguantar un golpe mortal con 1 PV (*Terquedad*) |
| 4 | 170 | +2 frames. Ataque de seguimiento cuando Teo hace un Trazo Firme (15 %) |
| 5 | 260 | **Iluminación a Dúo** (si su línea la tiene) o su **Gesto de Lealtad** (pasiva única) |

### 4.3 Cómo baja
| Acción | Efecto |
|---|---|
| Usar *Ofrenda* (Raíz Podrida) sobre él | −1 corazón |
| Corrupción de Teo ≥ 50 | −20 % de puntos ganados; con Lealtad baja, 10 % de perder el turno |
| Marchitarse 3 veces en la misma expedición | −5 puntos |

---

## 5. El Vivero de Nana Brote (Bastión)

Se abre al **liberar el Bastión**. Antes de eso, todo funciona con la Maceta y las Parcelas.

| Nivel del Vivero | Banca | Funciones nuevas |
|---|---|---|
| 1 | 3 | Germinar 3 semillas a la vez; cuidados diarios |
| 2 | 4 | **Injertos**: pasar una habilidad aprendida de un Semillado a otro de su mismo tipo (consume 1 Tomo de Brote) |
| 3 | 5 | **Entrenamiento**: los Semillados de la banca ganan XP en cada Jornada (10 % de un nivel) |
| 4 | 5 | **Replantar** (cambiar la forma final por 1 Lágrima); Lealtad +25 % |
| 5 | 6 | **Semillas Gemelas**: una vez por Jornada, una semilla común ya criada da un duplicado; Nana Brote regala una semilla rara por semana de juego |

**Espacios activos en combate:** 1 en el Acto I · 2 tras vencer al primer Señor · 3 con la Piedra Angular *Pastor del Bosque*.

---

## 6. ROSTER

**Leyenda:** Tipo = elemento de su daño principal (Físico, Tinta, Brasa, Savia, Luna o Podredumbre). Barrios: **Ám** (Ámbar/Granero), **Ca** (Carmesí/Forja), **Ín** (Índigo/Biblioteca), **Ja** (Jade/Bastión), **Pl** (Plata/Templo).

### 6.1 Las tres líneas iniciales

En la Antesala, tres semillas brotan de las grietas del suelo frente al Atril Mayor y Teo elige una. Las otras dos **no se pierden**:
- La segunda aparece en el Vivero cuando se libera el Bastión.
- La tercera se consigue tras el Asedio de la Antesala.

#### Línea de BROTÍN — Savia · Protector/Atacante
| Etapa | Nombre | Concepto visual |
|---|---|---|
| 1 | **Brotín** | Brote del tamaño de un gato con dos hojas por brazos, casco de bellota y escudito de hoja. Ojos enormes y valientes |
| 2 | **Espinardo** | Escudero de madera con armadura de corteza, lanza de rama con espinas y cresta de hojas |
| 3 · Ám | **Robledulce** | Roble robusto con savia de ámbar en las grietas, flores en los hombros y panal en el pecho. Sanador y tanque |
| 3 · Ca | **Carbonroble** | Roble chamuscado con un núcleo de brasas en el pecho y corteza como placas de hierro negro. Golpeador |
| 3 · Ín | **Robleletra** | Roble con letras grabadas en la corteza que brillan al lanzar conjuros; sus hojas son páginas. Controlador |
| 3 · Ja | **Robleguardia** | El caballero de roble clásico: escudo de corteza de jade, yelmo de bellota y capa de musgo. Provocación y contraataque |
| 3 · Pl | **Abedul de Luna** | Caballero de abedul blanco y plateado, con hojas que tintinean como campanillas. Revive y protege |

- **Firma:** *Hojazo* (Savia 60 [Trazo]; +10 % de DEF durante 2 turnos).
- **Habilidades de Guardián:** Robledulce *Savia de Panal* · Carbonroble *Corazón de Carbón* · Robleletra *Corteza Escrita* · Robleguardia *Muro Viviente* · Abedul de Luna *Campana del Alba*.
- **Comida favorita:** pan con miel.
- **Campo:** *Cortar* (abre matorrales espinosos que esconden cofres).
- **Iluminación a Dúo — "Raíz y Pluma":** Teo escribe RAÍZ en el aire; el Semillado clava su arma en el suelo y el campo se llena de un bosque instantáneo que empala a todos los enemigos. Físico/Savia 520; da *Amparo* del 30 % a todo el grupo.

**Ejemplo de lista de habilidades (Brotín → Robleguardia):**
| Nivel | Habilidad | PA | Efecto |
|---|---|---|---|
| 1 | Hojazo | 1 | Savia 60; DEF +10 % |
| 4 | Provocar Bellota | 1 | Provocación durante 2 turnos |
| 9 | Raíz Atadora | 2 | 40 % de *Enraizado* |
| 14 | *(Etapa 2)* Estocada de Espina | 2 | Físico 110; 20 % de *Subrayado* al objetivo |
| 20 | Corteza Gruesa | 2 | DEF y RES +30 % durante 3 turnos |
| 26 | Barrido de Lanza | 3 | Físico 80 a todos |
| 30 | *(Etapa 3)* Muro Viviente | 4 | Todo el grupo gana *Amparo* del 20 % y Robleguardia gana Provocación |
| 36 | Contraguardia de Roble | 2 | Postura: devuelve el 50 % del siguiente golpe |
| 42 | Juramento del Bastión | 3 | Durante 2 turnos recibe los golpes dirigidos a Teo |

#### Línea de PAVESA — Brasa · Atacante
| Etapa | Nombre | Concepto visual |
|---|---|---|
| 1 | **Pavesa** | Zorrito nacido de una piña en llamas, con cola de fuego que chisporrotea cuando se emociona |
| 2 | **Fogata** | Zorro mediano con melena de hollín y patas de brasa que dejan huellas encendidas |
| 3 · Ám | **Melaza** | Zorra de pelaje de miel fundida: fuego pegajoso que atrapa. Controladora (Ascua + Ambarizado) |
| 3 · Ca | **Ignaria** | Zorra de fragua con un delantal de llamas y pulmones de fuelle que avivan cada golpe. Daño puro |
| 3 · Ín | **Hollín** | Zorro negro de hollín que escribe runas ardientes con la cola. Quemaduras en área y debilitamientos |
| 3 · Ja | **Ascuaguarda** | Zorro con armadura de brasas que protege a los aliados y quema a quien los toca |
| 3 · Pl | **Fatua** | Zorra fantasmal de fuego azul plateado, como un fuego fatuo. Sus llamas curan a los aliados y queman a los enemigos |

- **Firma:** *Mordisco de Chispa* (Brasa 70; 30 % de *Ascua*; si el objetivo ya tenía *Ascua*, +1 pila).
- **Habilidades de Guardián:** Melaza *Caramelo Hirviente* · Ignaria *Fuelle Interior* · Hollín *Firma de Fuego* · Ascuaguarda *Brasero Guardián* · Fatua *Llama que Vuelve*.
- **Comida favorita:** castañas asadas.
- **Campo:** *Encender* (velas y faroles pequeños que revelan pasajes y polillas guía).
- **Iluminación a Dúo — "La Fragua y la Página":** Teo abre su libro; el zorro salta dentro y sale convertido en un incendio con forma de zorro gigante que recorre el campo. Brasa 540 a todos y 5 pilas de *Ascua*.

#### Línea de LUNILLA — Luna · Sanadora/Apoyo
| Etapa | Nombre | Concepto visual |
|---|---|---|
| 1 | **Lunilla** | Semilla alada parecida a una polilla diminuta, con alas plateadas que dejan polvo de luz |
| 2 | **Nacarina** | Polilla grande con alas de nácar que reflejan el cielo |
| 3 · Ám | **Ambarina** | Polilla de alas de ámbar que congela el tiempo a su alrededor. Control (*Ambarizado*) y protección |
| 3 · Ca | **Candelaria** | Polilla que se enamoró de la llama y se volvió llama. Daño Brasa/Luna y sacrificio heroico |
| 3 · Ín | **Marginalia** | Polilla cuyas alas están cubiertas de notas al margen. Copia estados, refuerza la Transcripción |
| 3 · Ja | **Atlante de Jade** | Polilla gigante y acorazada, inspirada en la polilla atlas, con alas como escudos. Protectora |
| 3 · Pl | **Selenia** | La polilla lunar pura: enorme, luminosa, con antenas como coronas. La mejor sanadora del juego |

- **Firma:** *Polvo de Luz* (cura a un aliado con Potencia 40 y le da +5 de Inspiración a Teo).
- **Habilidades de Guardián:** Ambarina *Ala Detenida* · Candelaria *Último Vuelo* · Marginalia *Nota de Ala* · Atlante de Jade *Escudo de Ala* · Selenia *Plenilunio*.
- **Comida favorita:** néctar de flor nocturna.
- **Campo:** *Iluminar* (rodea a Teo con luz en zonas oscuras y revela textos lunares sencillos).
- **Iluminación a Dúo — "Vuelo de Polillas":** miles de polillas levantan a Teo hasta una luna pintada en el cielo; desde ahí cae como un cometa. Luna 500 a todos; cura al grupo un 50 % y fija la fase en Llena durante 2 rondas.
- **Nota de guion:** Folio se pone celoso de Lunilla. *"Yo también tengo alas. De papel, pero alas."*

---

### 6.2 Líneas comunes de tres etapas (15)
| # | Etapa 1 → Etapa 2 | Natural (barrio) | Cruzada (barrio) | Tipo · Rol | Concepto | Firma | Campo |
|---|---|---|---|---|---|---|---|
| 4 | **Espiguín** → **Gavillo** | **Segador Dorado** (Ám) | **Segador de Ceniza** (Ca) | Savia/Físico · Atacante | Conejo de espigas que se vuelve un segador con hoz de trigo | *Siega*: Físico 70 a todos; más daño a enemigos con < 50 % de vida | Cortar pasto alto |
| 5 | **Panalito** → **Colmenar** | **Reina de Ámbar** (Ám) | **Colmena Escriba** (Ín) | Savia · Controlador | Semilla-panal con abejas de resina; la cruzada tiene abejas que escriben en cera | *Picadura Dulce*: Savia 50; 35 % de *Ambarizado* | Polinizar flores (cofres ocultos) |
| 6 | **Calabacín** → **Calabazón** | **Gran Cosecha** (Ám) | **Calabaza Farola** (Pl) | Savia · Protector | Calabaza caballero; la cruzada es un farol vivo con luz de luna | *Cáscara Dura*: *Amparo* del 15 % propio y Provocación | Rodar (romper vasijas) |
| 7 | **Fuellecito** → **Salamandruca** | **Salamandra de Fragua** (Ca) | **Salamandra Lunar** (Pl) | Brasa · Atacante | Salamandra con branquias de fuelle; la cruzada tiene fuego frío plateado | *Soplo de Fuelle*: Brasa 60; aviva las *Ascuas* | Encender braseros pequeños |
| 8 | **Yunquín** → **Martillón** | **Gran Yunque** (Ca) | **Yunque de Jade** (Ja) | Físico · Protector | Tortuga con caparazón de yunque; el Gran Yunque lleva un martillo por cola | *Caparazón Templado*: DEF +40 %; devuelve el 20 % | Pisotón (activar placas de presión) |
| 9 | **Chispilla** → **Escarabrasa** | **Escarabajo Solar** (Ca) | **Escarabajo Dorado** (Ám) | Brasa · Apoyo | Escarabajo que rueda una bolita de sol; el dorado rueda grano de oro | *Bola de Sol*: aliados +15 % de daño Brasa durante 3 turnos | Empujar bloques pequeños |
| 10 | **Gotín** → **Tintero Vivo** | **Pulpo de Tinta** (Ín) | **Pulpo de Nácar** (Pl) | Tinta · Controlador | Gota de tinta con ojitos que se vuelve un pulpo calígrafo | *Chorro de Tinta*: Tinta 55; 50 % de *Mancha de Tinta* | Ensuciar (revelar huellas invisibles en el suelo) |
| 11 | **Lomito** → **Tomazo** | **Grimorio Andante** (Ín) | **Herbario Andante** (Ám) | Tinta · Atacante mágico | Librito con patas (un "lomo" con piernas); el herbario tiene flores prensadas que curan | *Hoja Suelta*: Tinta 65; si el objetivo está Leído, +30 % | Leer carteles que Teo no alcanza |
| 12 | **Musguito** → **Musgolem** | **Muralla Musgosa** (Ja) | **Muralla de Escoria** (Ca) | Físico · Protector | Piedrita con musgo que crece hasta ser un muro andante | *Musgo Blando*: absorbe el siguiente golpe a un aliado | Hacer de puente sobre zanjas pequeñas |
| 13 | **Cardillo** → **Cardón** | **Erizo Lancero** (Ja) | **Erizo de Plata** (Pl) | Físico/Savia · Atacante | Erizo de cardo con púas que se lanzan | *Púas*: Físico 40 × 3 a objetivos al azar | Explotar globos de esporas |
| 14 | **Oseznillo** → **Oso de Corteza** | **Madreroble** (Ja) | **Oso del Sueño Largo** (Pl) | Físico · Protector/Atacante | La **línea de Madreroble**: oso cachorro con orejas de bellota que crece hasta ser un oso-roble colosal con hombreras de raíz. La forma cruzada duerme de pie y despierta con la luna | *Abrazo de Corteza*: Físico 90; *Enraizado* al 40 % | Olfatear (encuentra objetos enterrados) |
| 15 | **Rocío** → **Medusa de Nácar** | **Marea Plateada** (Pl) | **Marea de Ámbar** (Ám) | Luna · Sanador | Gota de rocío flotante que se vuelve una medusa de luz | *Lluvia Fina*: cura a todos (Potencia 25) | Mojar (apagar fuegos pequeños) |
| 16 | **Hilillo** → **Cintaluna** | **Serpiente de Plata** (Pl) | **Serpiente Marcapáginas** (Ín) | Luna/Tinta · Controlador | Serpiente-listón de luz de luna; la cruzada es un listón rojo de marcapáginas, igual que la bufanda de Teo | *Enroscar*: *Errata* al objetivo y +1 PA a Teo | Atar (hacer tirolesas cortas en postes) |
| 17 | **Salinito** → **Cangrejo de Sal** | **Coloso de Sal** (Ca) | **Coloso de Ámbar** (Ám) | Físico · Protector | Cangrejo de cristales de sal del Mar de Sal; el coloso es un cangrejo-fortaleza | *Pinza de Cristal*: Físico 70; 20 % de *Errata* | Excavar en la arena |
| 18 | **Raicita** → **Trepaliana** | **Rey de la Selva** (Ja) | **Mono Escriba** (Ín) | Savia · Apoyo | Monito de raíz de la Selva Murmurante; el Mono Escriba roba páginas y las lee en voz alta | *Lianazo*: Savia 55; roba 1 efecto positivo | Trepar (bajar objetos de lugares altos) |

**Habilidades de Guardián (todas las formas finales comunes):**
| Forma | Habilidad de Guardián | Efecto |
|---|---|---|
| Segador Dorado | *Última Gavilla* | Físico 220 a un objetivo; si lo derrota, actúa de nuevo |
| Segador de Ceniza | *Rastrojo en Llamas* | Brasa 120 a todos; 2 pilas de *Ascua* |
| Reina de Ámbar | *Enjambre de Resina* | 60 % de *Ambarizado* a todos los enemigos |
| Colmena Escriba | *Panal de Letras* | Aplica *Olvido* y *Mancha de Tinta* a todos |
| Gran Cosecha | *Granero Andante* | *Amparo* del 25 % al grupo y cura un 10 % |
| Calabaza Farola | *Farol de Medianoche* | Revela a todos los enemigos (como Leer) y cura un 15 % |
| Salamandra de Fragua | *Escupitajo de Escoria* | Brasa 200; elimina el *Amparo* del objetivo |
| Salamandra Lunar | *Fuego Frío* | Luna/Brasa 160; *Deslumbrado* |
| Gran Yunque | *Martillo de Cola* | Físico 180 [Rompe]; ×2 a la Postura |
| Yunque de Jade | *Bóveda de Jade* | Él y Teo reciben −50 % de daño durante 2 turnos |
| Escarabajo Solar | *Amanecer Rodante* | Grupo +30 % de Brasa y +1 PA |
| Escarabajo Dorado | *Diezmo Dorado* | +50 % de Orvales del combate (no se acumula) y el grupo +15 % de daño |
| Pulpo de Tinta | *Ocho Plumas* | Tinta 40 × 8 a objetivos al azar; cada golpe aplica *Mancha* |
| Pulpo de Nácar | *Tinta de Perla* | Cura al grupo un 25 % y quita *Mancha* y *Deslumbrado* |
| Grimorio Andante | *Capítulo Prohibido* | Tinta 260; 40 % de *Silencio de Tinta* |
| Herbario Andante | *Flores Prensadas* | Cura a todos un 30 % y aplica *Savia Viva* |
| Muralla Musgosa | *Muralla Viva* | Provocación durante 3 turnos y DEF +60 % |
| Muralla de Escoria | *Muro Ardiente* | Provocación; quien la golpee recibe 2 pilas de *Ascua* |
| Erizo Lancero | *Lluvia de Púas* | Físico 50 × 6 a todos al azar |
| Erizo de Plata | *Corona de Púas* | Devuelve el 40 % del daño físico durante 3 turnos |
| **Madreroble** | *La Garra del 412* | Físico 300 [Rompe]; si el objetivo es un jefe, ×1.3. Su Iluminación a Dúo (ver abajo) |
| Oso del Sueño Largo | *Hibernar* | Duerme 1 turno: se cura por completo y gana *Vigilia* |
| Marea Plateada | *Pleamar* | Cura al grupo un 40 %; con Luna Llena, revive al 25 % |
| Marea de Ámbar | *Marea Lenta* | Todos los enemigos VEL −30 % durante 3 turnos |
| Serpiente de Plata | *Órbita* | Empuja a todos los enemigos 1 posición atrás en la línea |
| Serpiente Marcapáginas | *Señalar la Página* | Teo gana *Nota al Margen* y +2 PA |
| Coloso de Sal | *Fortaleza de Sal* | El grupo es inmune a *Hambre* y *Pudrición* durante 3 turnos |
| Coloso de Ámbar | *Cristal de Ámbar* | Él mismo se *Ambariza* y Provoca: los golpes que recibe se devuelven al salir |
| Rey de la Selva | *Rugido Verde* | Grupo +20 % de ATQ y DEF durante 3 turnos |
| Mono Escriba | *Plagio* | Copia la última mejora enemiga y se la da a todo el grupo |

**Iluminación a Dúo de la línea de Madreroble — "El Abrazo del 412":** la pantalla se tiñe de sepia como un tapiz antiguo de la Noche de las Mil Semillas. Madreroble se levanta en dos patas y aplasta al enemigo mientras Teo "borda" el golpe en el tapiz. Físico 600 a un objetivo y Ruptura automática salvo en los jefes finales.

**Gesto de Lealtad** (pasivas con 5 corazones de las demás líneas comunes; ejemplos):
- *Segadores:* +10 % de daño a enemigos con menos del 50 % de vida.
- *Pulpos:* la *Mancha de Tinta* que aplican dura 1 turno más.
- *Murallas:* una vez por combate, protegen a Teo de un ✦ automáticamente.
- *Serpientes:* empiezan cada combate dándole 1 PA a Teo.

---

### 6.3 Líneas de dos etapas (6)
*Semillas raras que vende el Encuadernador o que regalan las misiones. No tienen Etapa 3, pero llegan a la Etapa 2 con estadísticas de Etapa 3 menos un 10 % y una habilidad única.*

| # | Etapa 1 → Etapa 2 | Tipo · Rol | Concepto | Habilidad única | Campo |
|---|---|---|---|---|---|
| 19 | **Ratón de Biblioteca** → **Archivero** | Tinta · Apoyo | Ratón con lentes y una hoja de pergamino por capa; el Archivero lleva un carrito de libros | *Catalogar*: el enemigo cuenta como Leído; Transcripción +25 % | Olfatear libros (encuentra Lecturas ocultas) |
| 20 | **Grillo de Horno** → **Grillo Herrero** | Brasa · Apoyo | Grillo que canta sobre las brasas y toca un yunquecito | *Canción de Fragua*: el grupo gana *Inspirado* y +1 PA | Cantar (calma a las bestias y despierta a los aldeanos dormidos) |
| 21 | **Corderito Lunar** → **Carnero de Nácar** | Luna · Protector | Corderito de lana luminosa; el carnero tiene cuernos de nácar en espiral | *Vellón de Luna*: el grupo gana RES +30 % y es inmune a *Devoción* durante 2 turnos | Dormir (siesta que hace avanzar la hora del día) |
| 22 | **Hongo Amable** → **Seta Sabia** | Podredumbre/Savia · Sanador | Hongo pequeño con sombrero de ancianito; la Seta Sabia tiene barba de micelio | *Compostar*: quita toda la *Pudrición* de un aliado y la convierte en curación | Descomponer (deshace muros de madera podrida) |
| 23 | **Lombriz de Jardín** → **Gusano Labrador** | Podredumbre/Savia · Controlador | Lombriz rosada con sombrerito de paja; el labrador ara la tierra del campo de batalla | *Arar*: el terreno del enemigo queda "removido": VEL −20 % y *Enraizado* al 30 % | Excavar túneles cortos |
| 24 | **Ciervito de Corteza** → **Ciervo Atalaya** | Físico/Luna · Atacante | Cervatillo con astas de ramas; el adulto tiene astas que son atalayas con farolitos | *Embestida de Astas*: Físico 120; empuja al objetivo al final de la línea | Saltar (cruza arroyos con Teo encima) |

> **Nota de diseño y narrativa:** el *Hongo Amable* y la *Lombriz de Jardín* son Semillados de Podredumbre **buenos**. Existen para enseñar sin palabras que la podredumbre tiene un lugar sano en la Rueda. NPCs como la Acólita Selia se asustan al verlos y Nana Brote los defiende: *"Sin gusanos no hay tierra, niña. Sin tierra no hay semillas."* Es una pista directa del final verdadero.

---

### 6.4 Legendarios (6)
*No evolucionan. Una sola copia por partida. Cada uno es la "redención" de su Pliegue: la versión sana de la calamidad.*

| # | Nombre | Cómo se consigue | Tipo · Rol | Concepto | Habilidad única | Iluminación a Dúo |
|---|---|---|---|---|---|---|
| 25 | **Cornucopio** | Semilla de Señor del Ámbar (tras la Anfitriona) | Savia · Sanador | Una criatura con forma de cuerno de la abundancia con patitas, de donde sale comida **que sí alimenta**. Sonríe como sonreía Hestra antes del Banquete | *Mesa Verdadera*: cura al grupo un 35 %, quita *Hambre* y da +1 PA a todos | **"La Despensa Abierta"**: lluvia de pan dorado; cura por completo y da 3 turnos de *Savia Viva* |
| 26 | **Lumbre** | Semilla de Señor del Carmesí (tras el Sol Cautivo) | Brasa · Atacante | El pequeño sol febril, ya curado: una esfera de fuego cálido con carita, que flota y ronronea como un horno | *Calor de Hogar*: Brasa 180 a todos los enemigos y +15 % de ATQ y POD al grupo | **"El Sol en Casa"**: Lumbre crece hasta ser un sol de mediodía sano: Brasa 560 a todos e inmunidad a *Fiebre* |
| 27 | **Glosador** | Semilla de Señor del Índigo (tras la Gran Correctora) | Tinta · Controlador | Espíritu de papel sin cara que va escribiéndose una cara distinta según su humor. Si Ysolde fue salvada, una de sus caras es la de ella de joven | *Reescribir*: devuelve a un aliado a como estaba hace 1 turno (vida, PA y estados) | **"Edición Definitiva"**: reescribe el último turno enemigo: anula todo su daño y se lo devuelve como Tinta |
| 28 | **Milsemilla** | Semilla de Señor del Jade (tras El Que No Cae) | Físico/Savia · Protector | Un enjambre de cientos de semillas guardianas diminutas que forman distintas figuras (un escudo, una lanza, un caballero) | *Formación de las Mil*: alterna entre forma Escudo (Provocación y DEF +50 %) y forma Lanza (Físico 60 × 5) | **"Guardia de Honor"**: las mil semillas forman la silueta de Dietrich, que da un tajo: Físico 580 y *Vigilia* a todo el grupo |
| 29 | **Alba** | Semilla de Señor de la Plata (tras la Voz del Coro) | Luna · Sanador/Apoyo | Una polilla enorme de alas rosadas y doradas que trae el amanecer. Es lo contrario de la Luna Falsa: no promete nada, solo ilumina | *Primera Luz*: quita todos los estados negativos al grupo y aplica *Deslumbrado* a todos los enemigos | **"Después de la Noche"**: el cielo amanece en pantalla; revive y cura a todo el grupo al 100 % (una vez por combate) |
| 30 | **Gusarapo** | Secreto: un capullo húmedo en el pozo más hondo de Las Entrañas. Exige tener a los 5 legendarios anteriores (o a 4, más el Hongo Amable) | Podredumbre · variable | Larva translúcida que se ve distinta según la Corrupción de Teo:<br>• **Gusarapo Limpio** (Corrupción < 25 o con la Sinergia *La Rueda*): larva dorada que convierte lo muerto en tierra fértil.<br>• **Gusarapo Voraz** (Corrupción ≥ 50): larva negra con dientes. | Limpio: *Ciclo* (los enemigos derrotados curan al grupo un 15 %). Voraz: *Devorar* (Podredumbre 280 y roba el 40 % como vida) | Limpio: **"La Rueda Gira"**: todo vuelve a la tierra: Podredumbre/Savia 500 a todos y cura al grupo lo mismo. Voraz: **"Hambre de Dios"**: Podredumbre 650 a un objetivo y **+5 de Corrupción** |

---

## 7. Semillados Corrompidos y el Rescate

En cada Pliegue hay **Semillados Corrompidos**: guardianes del árbol deformados por la calamidad (con hongos, metal fundido, borrones o máscaras de luna). Son una familia de enemigos (ver Combate §11).

1. Al romper su Postura, el **Remate Ilustrado** se reemplaza por la opción **Rescatar** (sin costo de PA).
2. La animación: Teo pone una mano sobre el guardián, la corrupción se desprende como ceniza y queda una semilla brillante.
3. El Rescate da la **semilla** de esa línea (no el Semillado ya criado), +2 Ecos y +1 entrada del Bestiario.
4. Si se elige **Rematar**, se gana más XP (+50 %) pero no la semilla. *(Pequeño dilema moral. Folio: "Técnicamente era un guardián del reino. Técnicamente.")*
5. Algunos corrompidos son **únicos** (élites con nombre). Su rescate da una variante de color (**Variante Antigua**) de su línea, con +5 % en todas las estadísticas.

---

## 8. Uso en exploración

1. **Acompañante:** el Semillado de la primera posición sigue a Teo por el mapa con animaciones propias (Pavesa se calienta junto a las fogatas, Lunilla persigue polillas y Brotín se esconde detrás de Teo cuando hay enemigos).
2. **Habilidad de Campo:** un botón usa la habilidad de campo del acompañante (ver las tablas). **Regla de diseño:** las habilidades de campo **solo abren secretos opcionales** (cofres, Páginas, atajos menores). El camino principal siempre depende de las seis habilidades de Teo (Viento de Molino, Martillo de Glifo, Visión de Tinta, Brote Guardián, Paso Lunar y Escritura Verdadera).
3. **Reacciones:** los Semillados reaccionan al mundo: gruñen ante los Semillados Corrompidos ocultos, se ponen nerviosos cerca de Páginas del Gusano y se duermen junto a los atriles.
4. **Rincones de Semillados:** en cada Pliegue hay 2 o 3 puzzles pensados para un tipo concreto (por ejemplo, un brasero sellado que solo enciende un Semillado de Brasa). Premian llevar variedad en la banca.

---

## 9. Equilibrio y reglas de implementación
- **Datos de cada línea:** `id, etapas[], forma_final_por_barrio{}, tipo, rol, bases{PV, ATQ, POD, DEF, RES, VEL}, lista_habilidades[(nivel, habilidad)], firma, habilidad_guardian{forma: habilidad}, campo, comida_favorita, duo (opcional)`.
- **Los Semillados no pueden morir de forma permanente.** Marchitos, vuelven a la vida al descansar en un atril.
- **Tope de poder:** ningún Semillado debe superar el 70 % del daño por turno de un Teo especializado (salvo *Pastor del Bosque*, que lo compensa con el daño reducido de Teo).
- **Variedad incentivada:** las afinidades de cada Pliegue (Combate §11) hacen que convenga rotar Semillados entre zonas.
- **Total: 30 líneas** (3 iniciales con 5 formas finales, 15 comunes con 2, 6 de dos etapas y 6 legendarios) = **99 formas distintas** (100 contando los dos aspectos de Gusarapo).
