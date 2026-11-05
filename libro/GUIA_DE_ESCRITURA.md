# Guía de escritura de *Mil Años bajo la Luna*

Notas de producción del libro de lore. No forman parte del libro.

## Qué es

*Mil Años bajo la Luna: Crónica del Reino de Orvalis* es un libro de lore que el jugador recibe como regalo al completar el juego al 100 %. Narra las épocas de Orvalis, desde la Rueda hasta la Noche de la Quiebra y los mil años de exilio del rey. Puede contar todas las verdades y secretos del canon, porque quien lo recibe ya terminó el juego. Tiene que ser **extenso y entretenido**: se lee como una novela, no como una enciclopedia.

## El marco

- **El compilador** es Teo de Merova, el Bibliotecario, ya terminado el juego. Reunió el libro con los anales de la Gran Biblioteca restaurada, las canciones, las inscripciones que se leen con Visión de Tinta, las Páginas Perdidas, los diarios y el testimonio del rey Aldemar (el Viejo Polilla). Su voz aparece en las **notas del compilador**: humilde, curiosa, con humor de lector obsesivo, y a veces conmovida. Admite cuándo no sabe algo y cuándo las fuentes se contradicen.
- **Al margen** escribe a veces una segunda mano, la del rey Aldemar: correcciones, recuerdos, una línea de dolor. Él vivió las últimas décadas (nació hacia el 951 AO) y el exilio; de lo anterior solo sabe lo que leyó de príncipe. Su voz es seca, de pocas palabras, a veces con ternura. Úsala poco: dos o tres veces por capítulo como máximo.

Formato de esas voces en Markdown:

```
> **Nota del compilador.** Texto de Teo…

> *Al margen, con letra antigua y temblorosa:* "Texto de Aldemar."
```

## El estilo: Tolkien y Martin, en castellano

No se nombra a ninguno de los dos autores ni se copian sus frases, nombres o mundos. Se toma su manera de contar:

- **De Tolkien:**
  - el tono de mito y elegía;
  - la sensación de tiempo profundo, con genealogías, nombres que pesan y lugares que tienen historia;
  - canciones y versos dentro del relato;
  - el paisaje como personaje;
  - la tristeza de lo que se pierde aunque se gane;
  - la luz contra la podredumbre.
- **De Martin:**
  - la crónica política y la intriga;
  - personajes grises, con buenas razones para hacer cosas terribles;
  - el precio concreto de cada decisión;
  - el hambre, la sangre y el barro contados sin adorno pero sin morbo;
  - escenas cercanas con diálogo;
  - traiciones que se sienten venir;
  - el cronista que compara fuentes que se contradicen ("los *Anales del Tronco* dicen…, pero las canciones de los barqueros cuentan…");
  - humor seco;
  - muertes que importan.
- **La mezcla cambia con el tiempo:**
  - las épocas más antiguas (la Rueda, los Gemelos) se cuentan como mito, casi como escritura sagrada;
  - a medida que la historia se acerca a la Quiebra, el relato se vuelve crónica con escenas, diálogos y puntos de vista;
  - el final (la Quiebra y el exilio) se lee como novela.

## Reglas

1. **El canon manda.** Antes de escribir, lee `01_CANON.md` y `lore/Historia_de_Orvalis.md`, y lo que corresponda de `historia/Personajes_Principales.md`, `lore/Textos_del_Mundo.md`, `lore/Reliquias_de_Orvalis.md`, `lore/Misterios_y_Secretos.md` y `mundo/`. Los nombres, fechas, hechos, reliquias y muertes del canon no se cambian.
2. **Se puede inventar** lo que llena huecos: personajes menores, escenas, diálogos, canciones, fuentes del mundo, anécdotas o rumores. Siempre que no contradiga el canon y que sirva a lo que ya existe. No inventes dioses, reliquias mayores ni destinos nuevos para los personajes del canon.
3. **Fechas:**
   - AO (Años de Orvalis) para el reino;
   - EM (Era Menguante) para los mil años posteriores a la Quiebra (el año 0 EM es la Quiebra; el presente del juego es el 1000 EM; Teo nació en el 981 EM).
4. **Castellano neutro latinoamericano**, como el resto de la biblia: tú y ustedes, nunca vosotros. El tono antiguo se logra con la cadencia y el vocabulario, no con arcaísmos forzados.
5. **Prosa viva:**
   - frases de largo variado;
   - imágenes concretas;
   - nada de listas en la narración (esto es un libro, no un documento de diseño);
   - verbos fuertes;
   - pocos adjetivos, bien elegidos.
   - Cada capítulo necesita al menos dos escenas dramatizadas con diálogo, y momentos de humor o calidez entre lo duro.
6. **Fuentes del mundo** que se pueden citar o inventar en esta línea:
   - *Anales del Tronco* (la crónica oficial);
   - *Crónica de los Juncales*;
   - las *Canciones del Camino* (de los maestros ambulantes);
   - los informes de la Guardia;
   - las *Memorias* de Ysolde Vantelle;
   - las *Páginas del Gusano* (de Corvan);
   - el diario de Lys;
   - *El Cuento de Orvalis*, con su "Lo que dice el cuento" contra "Lo que fue";
   - las notas al margen de los libros de la Biblioteca.

## Formato de cada capítulo

- Un archivo Markdown por capítulo en `libro/`, con el nombre indicado en el índice.
- Título: `# Capítulo N · Título`, y debajo en cursiva las fechas que abarca.
- Un epígrafe al empezar (canción, inscripción, dicho o fragmento de una fuente) en bloque de cita.
- Secciones separadas con un título `##` evocador, no con números.
- **Entre 4.000 y 5.000 palabras** por capítulo.
- Al final de cada capítulo, una línea en cursiva que enlace con lo que viene, como una página que se da vuelta.

## Índice

| Archivo | Capítulo | Épocas |
|---|---|---|
| `00_Prologo.md` | Prólogo del compilador | Escrito después del juego |
| **Libro primero: La Rueda y la Semilla** | | |
| `01_La_Rueda.md` | La Rueda | Los cuatro dioses, el valle del Albar, sus tribus, Ebrón el Ciego y Vela |
| `02_Los_Gemelos_del_Eclipse.md` | Los Gemelos del Eclipse | c. −18 a 7 AO: Irelda, la canasta, la Colina de la Lechuza, la fundación, el Trazo, la Ley del Libro Abierto, la discusión de los muros y la Semilla de Plata |
| `03_Los_Reyes_Pastores.md` | Los Reyes Pastores | 7–150 AO: Orval I y la Corona de Corteza, la unión de las tribus, Orval II y el Octavo Maestro, las Escuelas del Camino y el Consejo de la Raíz |
| **Libro segundo: El Árbol que Canta** | | |
| `04_La_Primera_Floracion.md` | La Primera Floración | c. 150 AO: Maela la Sembradora, el Canto de Crecimiento, los Velas Negras y los primeros Semillados |
| `05_Imelda_la_Lectora.md` | Imelda la Lectora | 198–242 AO: la reina que no sabía pelear, la Gran Biblioteca, la Academia Arcana y el fin de la pena de muerte |
| `06_El_Castillo_y_la_Conservacion.md` | El Castillo y la Conservación | 300–400 AO: Casimir II, el castillo que crece, la Conservación, Teobaldo Ruiseñor y la nota en tinta verdosa |
| **Libro tercero: Eclipse y Gusano** | | |
| `07_La_Guerra_del_Eclipse.md` | La Guerra del Eclipse | 412 AO: Kassar Vhal, Tolvar de las Arenas, las tres noches, Ismara II, la Noche de las Mil Semillas y Madreroble |
| `08_La_Herejia_Verde.md` | La Herejía Verde | 605–611 AO: la Tos de Musgo, Ulma Cienoverde, los Hijos del Gusano, las Galerías Hondas, el gran debate y Bertrand el Sellador |
| `09_Los_Siglos_Tranquilos.md` | Los Siglos Tranquilos | 650–950 AO: Leonor IV y el Tratado de las Mareas, la Encuadernación Viva, las Protecciones de Eclipse, el Coro de las Ramas y las artes |
| **Libro cuarto: Ceniza y Hierro** | | |
| `10_El_Anio_Sin_Luna.md` | El Año Sin Luna | 958–961 AO: el Monte Ascuar, la cadena del desastre, los niños de la ceniza (Hestra, Mireya, Selio), la reina Adelia y la Vigilia del Regreso |
| `11_La_Guerra_de_las_Cinco_Coronas.md` | La Guerra de las Cinco Coronas | 977–983 AO: el Pacto del Hierro, la Rama Baja, el Puente de Raíz, la muerte de Osric y el Vado Albar |
| `12_Aldemar_el_Justo.md` | Aldemar el Justo | 982–998 AO: el reinado, Elisenda, el amor callado de Corvan, la fiebre del 991, la profecía y el Plan de la Raíz Eterna |
| **Libro quinto: La Quiebra** | | |
| `13_Los_Desaparecidos_del_Invierno.md` | Los Desaparecidos del Invierno | 999–1000 AO: la capitana Ilse Varga, Pío y los cuarenta y tres |
| `14_La_Noche_de_la_Quiebra.md` | La Noche de la Quiebra | 1000 AO: el jubileo, la traición, Sapros, Ilunara y el Sueño de Plata |
| **Libro sexto: Mil Años Afuera** | | |
| `15_Mil_Anios_Afuera.md` | Mil Años Afuera | 0–1000 EM: el exilio del rey inmortal, el hundimiento de las Salinas, el ascenso de Kesh, el Cuento que se esparce y el bebé en la puerta de la Biblioteca de Merova |
| `16_La_Ultima_Pagina.md` | La Última Página | El viaje de Teo y el final, contado por él |
| `17_Apendices.md` | Apéndices | Cronología, monarcas, el Glifo Lunar, canciones y glosario |
