# PROGRESIÓN Y EL ÁRBOL DEL SABER

> Documento de diseño de sistemas. Depende de `01_CANON.md` (§11) y de `sistemas/Combate_y_Replica.md`.
> Cifras de primera versión; se ajustan en pruebas de juego.
> Corrupción, Cartas del Hereje y Páginas del Gusano siguen lo fijado en `historia/Trama_del_Juego.md` (Corrupción de 0 a 100, final malo con ≥ 70, 6 Cartas y 12 Páginas del Gusano).

---

## 1. Resumen

Teo progresa por **cinco vías**, cada una ligada a la fantasía de "bibliotecario que se vuelve mago":

| Vía | Qué da | Fuente |
|---|---|---|
| **Nivel** | Atributos, PH y vida | XP de combates, misiones y descubrimientos |
| **El Árbol del Saber** | Habilidades, pasivas, Glosas y Piedras Angulares | PH |
| **Lecturas** | Bonos permanentes y PH extra | Libros encontrados en el mundo y leídos en un atril |
| **Transcripción** | Habilidades copiadas de los enemigos | Leer y Réplica en combate |
| **Equipo** | Estadísticas, afijos, runas y efectos únicos | Botín, forja, reliquias |

---

## 2. Nivel y experiencia

### 2.1 Curva
- **Nivel máximo: 60.** La historia termina alrededor del nivel 45; del 45 al 60 es contenido de fin de juego.
- XP necesaria para pasar del nivel *n* al *n+1*:
```
XP(n) = redondeo(40 × n^1.8 + 60 × n)
```

| Nivel | XP para el siguiente | Nivel | XP para el siguiente |
|---|---|---|---|
| 1 | 100 | 30 | 20 036 |
| 5 | 1 025 | 35 | 26 164 |
| 10 | 3 124 | 40 | 33 008 |
| 15 | 6 136 | 45 | 40 524 |
| 20 | 9 988 | 50 | 48 720 |
| 25 | 14 632 | 55 | 57 580 |
| | | 59 | 65 140 |

XP total del 1 al 60: unos **1.47 millones**.

### 2.2 Ritmo esperado por acto
| Tramo | Nivel al entrar | Nivel al salir |
|---|---|---|
| Prólogo (los recuerdos usan personajes con estadísticas fijas) | — | 1 |
| Acto I: El Viaje | 1 | 8 |
| 1.er Pliegue | 8 | 16 |
| 2.º Pliegue | 16 | 22 |
| 3.er Pliegue | 22 | 28 |
| 4.º Pliegue | 28 | 34 |
| 5.º Pliegue | 34 | 40 |
| Acto III: Las Entrañas | 40 | 45 |
| Fin de juego | 45 | 60 |

El orden de los Pliegues es libre; el **Eco de Poder** (ver Combate §18) mantiene a los Señores a la altura del jugador.

### 2.3 Fuentes de XP
| Fuente | XP |
|---|---|
| Enemigo | `12 × nivel del enemigo × rango` (común 1 · élite 3 · mini-jefe 8) × multiplicador de Calificación |
| Señor | Equivale a 1.5 niveles en el momento de vencerlo |
| Misión secundaria | De 0.3 a 1 nivel según su tamaño |
| Página Perdida | 2 % del nivel actual |
| Primera entrada completa del Bestiario | 1 % del nivel actual |
| Descubrir una zona del mapa | 0.5 % del nivel actual |

### 2.4 Lo que da cada nivel
| Recompensa | Valor |
|---|---|
| Puntos de Atributo | **+3** para repartir |
| Puntos de Habilidad (PH) | **+1** |
| Cada 5 niveles ("Capítulo Cumplido") | **+1 PH** extra y la vida y los PA se rellenan |
| Vida base | +15 por nivel (ver fórmula) |

### 2.5 Fuentes de PH a lo largo del juego
| Fuente | PH totales |
|---|---|
| Niveles 2–60 | 59 |
| Capítulos Cumplidos (niveles 5, 10 … 60) | 12 |
| Señores vencidos (+3 cada uno) | 15 |
| Hereje y Sapros | 5 |
| Lecturas de Obras Mayores (+1 cada una) | 10 |
| Hitos de Páginas Perdidas | 6 |
| **Total** | **107** |

El Árbol tiene **180 nodos** que cuestan en total unos **300 PH**. Un jugador completo llega a ~35 % del árbol: **las builds importan**.

---

## 3. Los seis atributos

Teo empieza con: Vigor 10 · Intelecto 12 · Destreza 10 · Voluntad 10 · Fe Lunar 8 · Memoria 10.
- **Tope suave: 60.** A partir de ahí, cada punto vale la mitad.
- **Tope duro: 99.**

| Atributo | Fórmulas y efectos |
|---|---|
| **Vigor** | Vida = `40 + Nivel × 15 + Vigor × 9` · DEF +1 por punto · resistencia a *Pudrición* +0.3 % por punto |
| **Intelecto** | POD = `POD de la Pluma + POD del Tomo + Intelecto × 2` · el daño a la Postura de las habilidades mágicas sube 0.5 % por punto |
| **Destreza** | ATQ = `ATQ de la Pluma + Destreza × 2` · VEL = `80 + Destreza` · Crítico = `5 % + Destreza × 0.15 %` (tope 40 %) · **ventana de Réplica +1 frame cada 25 puntos** (máximo +3) |
| **Voluntad** | PA máximo = `6 + floor((Voluntad − 10) / 15)` (tope 10) · RES +1 por punto · resistencia a estados `× (1 − Voluntad × 0.004)` |
| **Fe Lunar** | Curación ×`(1 + Fe Lunar × 0.008)` · daño Luna +0.6 % por punto · Inspiración ganada +0.3 % por punto · con 40 o más, *Plegaria de Vigilia* funciona |
| **Memoria** | Espacios del Grimorio = `4 + floor(Memoria / 12)` (tope 10) · Glosas activas = `2 + floor(Memoria / 15)` · Transcripción +1 % de velocidad por punto · XP +0.2 % por punto |

---

## 4. El Grimorio y las Glosas

- **Grimorio**: las habilidades **activas** que Teo puede usar en combate. Su número depende de Memoria (de 4 a 10). Las pasivas y las Piedras Angulares **no** ocupan espacio.
- Las **habilidades transcritas** ocupan espacio del Grimorio (salvo con *El Copista*).
- **Glosas**: nodos que modifican una habilidad concreta. Una Glosa comprada no se aplica sola: hay que **activarla** en el menú del Grimorio. El número de Glosas activas depende de Memoria (de 2 a 8). Así, Memoria define **cuántas habilidades** se llevan y **qué tan refinadas** están.
- El Grimorio solo se edita en un **atril**, nunca en combate.
- Se pueden guardar **3 configuraciones** ("Marcadores") y cambiar entre ellas en el atril.

---

## 5. EL ÁRBOL DEL SABER

### 5.1 Estructura
La pantalla del Árbol es **el árbol de Orvalis dibujado en un pergamino**:
- **Tronco** (Tinta): disponible desde el inicio.
- Cinco **ramas** de color: Savia (ámbar), Brasa (carmesí), Glifo (índigo), Guardia (jade) y Luna (plata). Cada una aparece **seca y gris** hasta liberar su sección; al liberarla, la rama "brota" con una animación.
- **Raíces** (pasivas generales): disponibles desde el inicio.
- **Raíz Podrida**: oculta. Aparece al vencer al 2.º Señor y leer la primera Carta del Hereje.
- **Sinergias**: nodos dorados donde se tocan dos ramas.

### 5.2 Tipos de nodo
| Tipo | Icono | Costo habitual |
|---|---|---|
| **Activa** | Círculo | 1–2 PH |
| **Pasiva** | Hoja | 1–2 PH |
| **Glosa** (modifica una activa) | Nota al margen | 1 PH |
| **Piedra Angular** (cambia la build, con costo o contrapartida) | Piedra tallada | 3 PH |
| **Sinergia** (requiere nodos en dos ramas) | Hoja dorada | 2 PH |
| **Iluminación** (desbloquea la definitiva de la escuela) | Capitular iluminada | 3 PH |

**Requisitos:** cada nodo exige el nodo anterior de su camino (columna *Req.*). Las Iluminaciones exigen además 8 nodos de su rama.

### 5.3 TRONCO — Tinta (26 nodos)
| ID | Nodo | Tipo | PH | Req. | Efecto |
|---|---|---|---|---|---|
| T-01 | **Gota de Tinta** | Activa | 1 | — | 1 PA · Tinta 80 a un objetivo; 30 % de *Mancha de Tinta*. [Trazo] |
| T-02 | **Subrayar** | Activa | 1 | — | 1 PA · Aplica *Subrayado* |
| T-03 | **Pluma Afilada** | Pasiva | 1 | — | Ataque básico +10 %; el 3.er Trazo hace +4 de Postura |
| T-04 | **Borrón** | Activa | 1 | T-01 | 2 PA · Tinta 60 a todos los enemigos; 40 % de *Mancha* |
| T-05 | **Tintero Hondo** | Pasiva | 2 | T-03 | +1 PA máximo |
| T-06 | Glosa: **Gota Rebotada** | Glosa | 1 | T-01 | *Gota de Tinta* rebota a un segundo objetivo al 60 % |
| T-07 | **Párrafo** | Activa | 2 | T-04 | 3 PA · 4 golpes de Tinta 45. [Trazo] |
| T-08 | **Signo de Interrogación** | Activa | 1 | T-02 | 1 PA · Revela todas las intenciones del objetivo durante 2 turnos |
| T-09 | **Punto y Aparte** | Activa | 1 | T-02 | 2 PA · Tinta 50 y empuja al objetivo 2 posiciones atrás en la línea de iniciativa |
| T-10 | **Margen Amplio** | Pasiva | 2 | T-03 | Desviar y Esquivar +1 frame |
| T-11 | **Lector Atento** | Pasiva | 1 | T-08 | Una vez por combate, *Leer* no ocupa el turno |
| T-12 | **Tinta Densa** | Pasiva | 1 | T-04 | *Mancha de Tinta* dura +1 turno y además baja −10 % de DEF |
| T-13 | **Cita Textual** | Activa | 2 | T-07 | 2 PA · Repite la última habilidad usada por cualquier aliado al 60 % |
| T-14 | Glosa: **Párrafo Largo** | Glosa | 1 | T-07 | *Párrafo* hace 6 golpes, pero cuesta 4 PA |
| T-15 | **Errata Encadenada** | Pasiva | 1 | T-09 | Cada vez que retrasas a un enemigo en la línea, +1 PA (máx. 1 por turno) |
| T-16 | **Caligrafía** | Pasiva | 1 | T-03 | Los Trazos Firmes hacen +15 % adicional |
| T-17 | **Nota al Pie** | Activa | 1 | T-13 | 1 PA · Un aliado gana *Nota al Margen* |
| T-18 | **Tachón** | Activa | 2 | T-12 | 3 PA · Anula un efecto positivo del objetivo y hace Tinta 120 |
| T-19 | **Fe de Erratas** | Activa | 1 | T-17 | 2 PA · Quita 2 estados negativos a un aliado y lo cura un 10 % |
| T-20 | **Índice** | Pasiva | 2 | T-11 | Empiezas cada combate con +1 PA por cada tipo de enemigo presente con su entrada de Bestiario completa (máx. +3) |
| T-21 | **Capítulo Uno** | Pasiva | 2 | T-05 | En el primer turno: +2 PA y +20 de Inspiración |
| T-22 | Glosa: **Borrón Pegajoso** | Glosa | 1 | T-04 | *Borrón* aplica también *Errata* |
| T-23 | **Manuscrito** | Activa | 2 | T-18 | 5 PA · Tinta 300 a un objetivo; ignora el 30 % de su RES |
| T-24 | Piedra Angular: **El Lector** | P. Angular | 3 | T-20 | Cada *Leer* sobre un enemigo le pone 1 pila de *Conocimiento* (máx. 5): +6 % de daño contra él por pila. **Contrapartida:** −10 % de vida máxima |
| T-25 | Piedra Angular: **Tinta Inagotable** | P. Angular | 3 | T-06 | *Gota de Tinta* cuesta 0 PA. **Contrapartida:** las demás activas cuestan +1 PA |
| T-26 | Iluminación: **Érase una Vez** | Iluminación | 3 | 8 nodos del Tronco | Desbloquea la Iluminación de Tinta |

### 5.4 SAVIA — rama Ámbar (22 nodos) · *se abre al liberar el Granero*
| ID | Nodo | Tipo | PH | Req. | Efecto |
|---|---|---|---|---|---|
| S-01 | **Resina** | Activa | 1 | — | 1 PA · Cura a un aliado (Potencia 60) |
| S-02 | **Gota de Ámbar** | Activa | 1 | — | 2 PA · Savia 70; 35 % de *Ambarizado* |
| S-03 | **Espigas** | Activa | 1 | S-02 | 2 PA · Savia 55 a todos; VEL −10 % durante 2 turnos |
| S-04 | **Cosecha** | Pasiva | 1 | S-01 | Al derrotar a un enemigo, el grupo se cura un 5 % |
| S-05 | **Pan Compartido** | Activa | 2 | S-01 | 3 PA · Cura a todo el grupo (Potencia 45) y aplica *Savia Viva* |
| S-06 | **Viento de Molino** | Activa | 1 | S-03 | 2 PA · Ráfaga: *Errata* a todos los enemigos y Savia 30 |
| S-07 | **Insecto en Ámbar** | Pasiva | 1 | S-02 | Los enemigos *Ambarizados* reciben +25 % de daño Tinta |
| S-08 | Glosa: **Resina Espesa** | Glosa | 1 | S-01 | *Resina* también da *Amparo* del 10 % de vida |
| S-09 | **Raíz Dulce** | Pasiva | 1 | S-04 | Por encima del 50 % de vida, regeneras 3 % por turno |
| S-10 | **Granero Lleno** | Pasiva | 1 | S-04 | Los objetos curan +30 % |
| S-11 | **Ámbar Lento** | Activa | 2 | S-06 | 3 PA · VEL −30 % a un enemigo durante 3 turnos |
| S-12 | **Sello de Ámbar** | Activa | 2 | S-07 | 4 PA · *Ambariza* a un aliado: inmune a todo durante 1 turno (pierde su turno) |
| S-13 | Glosa: **Gota Cristalina** | Glosa | 1 | S-02 | *Gota de Ámbar*: +25 % de probabilidad de ámbar, −20 % de daño |
| S-14 | **Fermentar** | Pasiva | 1 | S-07 | Cuando un enemigo sale del ámbar, explota: Savia 60 a sus aliados |
| S-15 | **Diezmo** | Activa | 1 | S-11 | 1 PA · Roba un efecto positivo del objetivo y te lo pone a ti |
| S-16 | **Abundancia** | Pasiva | 2 | S-05 | La curación sobrante se vuelve *Amparo* (hasta el 20 % de la vida) |
| S-17 | **Trigo Espinado** | Activa | 1 | S-09 | 2 PA · Postura: el siguiente golpe físico que recibas devuelve Savia 90 |
| S-18 | **Lluvia de Otoño** | Activa | 2 | S-16 | 4 PA · Cura a todos (Potencia 50) y quita toda la *Pudrición* y *Ascua* |
| S-19 | **Semilla de Reserva** | Pasiva | 2 | S-18 | Una vez por combate, el primer aliado que caiga revive con un 15 % |
| S-20 | Piedra Angular: **Mesa Abundante** | P. Angular | 3 | S-16 | Toda curación ×1.5. **Contrapartida:** no puedes usar objetos en combate |
| S-21 | Piedra Angular: **Tiempo Detenido** | P. Angular | 3 | S-14 | *Ambarizado* dura 2 turnos. **Contrapartida:** los enemigos en ámbar reciben −50 % de daño (en vez de −30 %) |
| S-22 | Iluminación: **Ámbar Eterno** | Iluminación | 3 | 8 nodos de Savia | Desbloquea la Iluminación de Savia |

### 5.5 BRASA — rama Carmesí (22 nodos) · *se abre al liberar la Forja*
| ID | Nodo | Tipo | PH | Req. | Efecto |
|---|---|---|---|---|---|
| B-01 | **Chispa** | Activa | 1 | — | 1 PA · Brasa 70; 30 % de *Ascua* |
| B-02 | **Pluma Candente** | Activa | 1 | — | 2 PA · El ataque básico hace +30 % de daño Brasa durante 3 turnos |
| B-03 | **Fuelle** | Activa | 1 | B-01 | 2 PA · Las *Ascuas* del objetivo suben +1 pila y duran +1 turno |
| B-04 | **Golpe de Yunque** | Activa | 2 | B-02 | 3 PA · Físico/Brasa 150; ×2 de daño a la Postura. [Rompe] [Trazo] |
| B-05 | **Metal al Rojo** | Pasiva | 1 | B-04 | Contra Constructos y Febriles ignoras el 20 % de su DEF |
| B-06 | **Lluvia de Escoria** | Activa | 2 | B-03 | 4 PA · Brasa 90 a todos y *Ascua* al 50 % |
| B-07 | **Temple** | Pasiva | 1 | B-04 | Después de un Desvío, tu siguiente habilidad de Brasa hace +25 % |
| B-08 | Glosa: **Chispa Doble** | Glosa | 1 | B-01 | *Chispa* se lanza dos veces al 60 % |
| B-09 | **Combustión** | Pasiva | 2 | B-03 | *Ascua* llega a 5 pilas; con 5 pilas explota (Brasa 200) y se reinicia |
| B-10 | **Fiebre Útil** | Activa | 1 | B-07 | 2 PA · Te aplicas *Fiebre* sin el *Aturdido* final |
| B-11 | **Martillo de Glifo** | Activa | 2 | B-04 | 3 PA · Brasa 110; destruye el *Amparo* y las armaduras de partes |
| B-12 | **Fragua Interior** | Pasiva | 1 | B-02 | Cada habilidad de Brasa da +3 de Inspiración |
| B-13 | **Mediodía** | Activa | 2 | B-09 | 5 PA · Brasa 260 a un objetivo; +30 % en Luna Nueva o Sin Luna |
| B-14 | **Ceniza en los Ojos** | Pasiva | 1 | B-06 | Los enemigos con *Ascua* tienen −15 % de precisión |
| B-15 | Glosa: **Yunque Resonante** | Glosa | 1 | B-04 | *Golpe de Yunque* alcanza a los enemigos contiguos al 50 % |
| B-16 | **Brasa Paciente** | Pasiva | 1 | B-09 | Cada tic de *Ascua* hace 3 de daño a la Postura |
| B-17 | **Escudo de Escoria** | Activa | 1 | B-11 | 2 PA · *Amparo* del 15 %; quien te golpee recibe *Ascua* |
| B-18 | **Chispas del Fuelle** | Pasiva | 1 | B-17 | Cada Desvío aplica *Ascua* al atacante |
| B-19 | **Bronce Vivo** | Pasiva | 1 | B-10 | Con menos del 30 % de vida, Brasa +30 % |
| B-20 | Piedra Angular: **El Horno** | P. Angular | 3 | B-13 | Daño Brasa +40 %. **Contrapartida:** pierdes el 3 % de tu vida máxima por turno |
| B-21 | Piedra Angular: **Forjador** | P. Angular | 3 | B-12 | El ataque básico se vuelve Brasa y da 1 pila de *Calor*; con 5 pilas, tu siguiente habilidad cuesta 0 PA. **Contrapartida:** el ataque básico ya no genera PA |
| B-22 | Iluminación: **El Último Ocaso** | Iluminación | 3 | 8 nodos de Brasa | Desbloquea la Iluminación de Brasa |

### 5.6 GLIFO — rama Índigo (22 nodos) · *se abre al liberar la Biblioteca*
| ID | Nodo | Tipo | PH | Req. | Efecto |
|---|---|---|---|---|---|
| G-01 | **Runa Menor** | Activa | 1 | — | 1 PA · Tinta 75; −10 % de RES durante 2 turnos |
| G-02 | **Lectura Profunda** | Activa | 1 | — | 1 PA · Análisis completo: debilidades, golpes ocultos y Transcripción +50 %. No ocupa el turno |
| G-03 | **Olvido Inducido** | Activa | 1 | G-01 | 2 PA · 50 % de *Olvido* |
| G-04 | **Palimpsesto** | Activa | 2 | G-03 | 3 PA · Convierte el último efecto positivo del objetivo en su equivalente negativo |
| G-05 | **Escritura Invertida** | Pasiva | 1 | G-02 | Refutar devuelve el 60 % en lugar del 40 % |
| G-06 | **Círculo de Glifos** | Activa | 2 | G-01 | 3 PA · Zona de 3 turnos: las habilidades mágicas del grupo cuestan −1 PA (mínimo 1) |
| G-07 | **Transcriptor** | Pasiva | 1 | G-02 | Transcripción +50 % de velocidad |
| G-08 | Glosa: **Runa Encadenada** | Glosa | 1 | G-01 | *Runa Menor* salta a 3 objetivos |
| G-09 | **Mente Ordenada** | Pasiva | 2 | G-07 | +1 espacio del Grimorio |
| G-10 | **Corrección** | Activa | 1 | G-03 | 2 PA · Quita 1 estado negativo a un aliado y lo convierte en +10 de Inspiración |
| G-11 | **Silencio de Biblioteca** | Activa | 2 | G-03 | 3 PA · *Silencio de Tinta* durante 2 turnos |
| G-12 | **Pie de Página** | Pasiva | 1 | G-05 | Los glifos enemigos aparecen +10 frames antes |
| G-13 | **Ex Libris** | Activa | 1 | G-07 | 2 PA · Marca al objetivo: tus habilidades transcritas le hacen +30 % |
| G-14 | **Biblioteca Interior** | Pasiva | 2 | G-13 | Las habilidades transcritas cuestan −1 PA |
| G-15 | Glosa: **Olvido Total** | Glosa | 1 | G-03 | *Olvido* sella 2 habilidades; la probabilidad baja −15 % |
| G-16 | **Rasqueta** | Activa | 1 | G-04 | 2 PA · Tinta 90 y quita 1 efecto positivo |
| G-17 | **Antítesis** | Pasiva | 1 | G-05 | Cada Refutar completo da +1 PA adicional |
| G-18 | **Laberinto** | Activa | 1 | G-11 | 3 PA · *Desorientado* durante 2 turnos |
| G-19 | **Tesis** | Activa | 2 | G-16 | 4 PA · Tinta 40 × número de estados negativos distintos del objetivo (sin tope) |
| G-20 | Piedra Angular: **El Copista** | P. Angular | 3 | G-14 | Abre el **Apéndice**: 4 espacios extra solo para habilidades transcritas. **Contrapartida:** tus habilidades propias de Glifo hacen −20 % |
| G-21 | Piedra Angular: **Erudición** | P. Angular | 3 | G-09 | Intelecto cuenta ×1.5 en todas las fórmulas. **Contrapartida:** Vigor cuenta ×0.75 |
| G-22 | Iluminación: **El Códice Abierto** | Iluminación | 3 | 8 nodos de Glifo | Desbloquea la Iluminación de Glifo |

### 5.7 GUARDIA — rama Jade (22 nodos) · *se abre al liberar el Bastión*
| ID | Nodo | Tipo | PH | Req. | Efecto |
|---|---|---|---|---|---|
| J-01 | **Escudo de Corteza** | Activa | 1 | — | 1 PA · *Amparo* del 12 % de vida a un aliado |
| J-02 | **Llamado al Muro** | Activa | 1 | — | 1 PA · Provocación durante 2 turnos (a ti o a un Semillado) |
| J-03 | **Brote Guardián** | Activa | 1 | J-01 | 2 PA · Invoca un brote señuelo con el 20 % de tu vida que atrae un ataque |
| J-04 | **Disciplina** | Pasiva | 1 | J-02 | Desviar +1 frame |
| J-05 | **Contraguardia** | Pasiva | 2 | J-04 | Las Réplicas Perfectas hacen +30 % de daño |
| J-06 | **Formación** | Pasiva | 1 | J-01 | Los Semillados activos tienen +10 % en todas sus estadísticas |
| J-07 | **Orden del Mariscal** | Activa | 1 | J-06 | 2 PA · Un Semillado actúa de inmediato |
| J-08 | Glosa: **Corteza de Jade** | Glosa | 1 | J-01 | *Escudo de Corteza* además devuelve el 20 % del daño absorbido |
| J-09 | **Espinas** | Pasiva | 1 | J-04 | Quien te golpee con un ataque físico recibe el 8 % de ese daño |
| J-10 | **Muro de Raíces** | Activa | 2 | J-08 | 4 PA · *Amparo* del 15 % a todo el grupo |
| J-11 | **Relevo** | Activa | 1 | J-07 | 1 PA · Cambia un Semillado sin gastar su turno |
| J-12 | **La Guardia No Duerme** | Pasiva | 2 | J-05 | Los Semillados defendidos con Réplica Perfecta contraatacan con su habilidad básica y ganan +1 PA |
| J-13 | **Lanza de Jade** | Activa | 1 | J-03 | 3 PA · Físico/Savia 140; atraviesa (golpea también al de atrás al 50 %) |
| J-14 | Glosa: **Brote Explosivo** | Glosa | 1 | J-03 | El brote señuelo explota al caer: Savia 80 a todos |
| J-15 | **Estandarte** | Activa | 2 | J-10 | 3 PA · El grupo hace +15 % de daño durante 3 turnos |
| J-16 | **Contraataque Ensayado** | Pasiva | 1 | J-09 | Cada Desvío inflige al instante el 25 % de tu ataque básico |
| J-17 | **Vigilia** | Activa | 2 | J-15 | 3 PA · Un aliado gana *Vigilia* |
| J-18 | **Tronco Firme** | Pasiva | 1 | J-10 | Eres inmune a *Errata* y a ser empujado en la línea |
| J-19 | **Vínculo de Savia** | Pasiva | 1 | J-06 | El 25 % del daño que recibe Teo pasa al Semillado con más vida |
| J-20 | Piedra Angular: **El Que No Cae** | P. Angular | 3 | J-17 | Una vez por combate sobrevives a un golpe mortal con 1 de vida; por debajo del 25 % de vida, todas las ventanas de Réplica +2 frames. **Contrapartida:** curación recibida −20 % |
| J-21 | Piedra Angular: **Pastor del Bosque** | P. Angular | 3 | J-11 | 3 Semillados activos en lugar de 2. **Contrapartida:** el daño propio de Teo baja −25 % |
| J-22 | Iluminación: **La Noche de las Mil Semillas** | Iluminación | 3 | 8 nodos de Guardia | Desbloquea la Iluminación de Guardia |

### 5.8 LUNA — rama Plata (22 nodos) · *se abre al liberar el Templo*
| ID | Nodo | Tipo | PH | Req. | Efecto |
|---|---|---|---|---|---|
| L-01 | **Rayo de Luna** | Activa | 1 | — | 1 PA · Luna 80 (con multiplicador de fase) |
| L-02 | **Bendición Menor** | Activa | 1 | — | 2 PA · Cura a un aliado (Potencia 75) |
| L-03 | **Cambio de Fase** | Activa | 1 | L-01 | 2 PA · Avanza la fase lunar un paso. No ocupa el turno (máx. 1 por turno) |
| L-04 | **Marea** | Pasiva | 1 | L-03 | En Luna Llena: +1 PA por turno |
| L-05 | **Deslumbrar** | Activa | 1 | L-01 | 2 PA · *Deslumbrado* durante 2 turnos |
| L-06 | **Resurrección Plateada** | Activa | 2 | L-02 | 4 PA · Revive a un aliado con el 40 % |
| L-07 | **Halo** | Pasiva | 1 | L-02 | +15 % de curación recibida |
| L-08 | Glosa: **Rayo Creciente** | Glosa | 1 | L-01 | En Creciente, *Rayo de Luna* golpea dos veces |
| L-09 | **Menguante Afilada** | Pasiva | 1 | L-04 | En Menguante: +15 % de crítico (se suma al de la fase) |
| L-10 | **Luna Nueva Oculta** | Pasiva | 1 | L-04 | En Luna Nueva: Esquivar +3 frames |
| L-11 | **Lluvia de Estrellas** | Activa | 2 | L-05 | 4 PA · Luna 70 × 4 golpes a objetivos al azar |
| L-12 | **Purificar** | Activa | 1 | L-07 | 2 PA · Quita *Pudrición* y *Devoción* a un aliado; Luna 100 a un Pútrido |
| L-13 | **Plegaria de Vigilia** | Pasiva | 1 | L-07 | Con Fe Lunar ≥ 40, el combate empieza en Llena |
| L-14 | **Velo Plateado** | Activa | 2 | L-12 | 3 PA · RES del grupo +30 % durante 3 turnos |
| L-15 | Glosa: **Resurrección Plena** | Glosa | 1 | L-06 | Revive con el 80 %, pero cuesta 6 PA |
| L-16 | **Ojo de la Diosa** | Pasiva | 2 | L-14 | Refutar +2 frames |
| L-17 | **Fase Inmóvil** | Activa | 2 | L-03 | 3 PA · Congela la fase actual durante 3 rondas |
| L-18 | **Luz que Recuerda** | Pasiva | 1 | L-13 | Inmune a *Olvido*; +10 % de Inspiración ganada |
| L-19 | Piedra Angular: **Sacerdote del Eclipse** | P. Angular | 3 | L-17 | Durante un Eclipse, tus habilidades de Luna se vuelven **Luna Negra**: no se reducen; hacen +50 % y aplican *Deslumbrado*. **Contrapartida:** fuera del Eclipse, la curación de Luna −25 % |
| L-20 | **Eclipse Propio** | Activa | 2 | L-19 | 6 PA · Provoca un Eclipse durante 2 rondas (una vez por combate) |
| L-21 | Piedra Angular: **Marea Alta** | P. Angular | 3 | L-04 | Al llegar a la Llena, la fase ya no avanza durante el resto del combate. **Contrapartida:** la curación −30 % |
| L-22 | Iluminación: **Marea de Plata** | Iluminación | 3 | 8 nodos de Luna | Desbloquea la Iluminación de Luna |

### 5.9 RAÍCES — pasivas generales (18 nodos) · *desde el inicio*
| ID | Nodo | PH | Efecto |
|---|---|---|---|
| R-01 | **Raíz Profunda** | 1 | +5 % de vida máxima |
| R-02 | **Raíz Ágil** | 1 | +5 de VEL |
| R-03 | **Lectura Rápida** | 1 | *Leer* da +2 PA en lugar de +1 |
| R-04 | **Ahorro** | 1 | +10 % de Orvales |
| R-05 | **Coleccionista** | 1 | +10 % de probabilidad de botín |
| R-06 | **Sueño Ligero** | 1 | Descansar en un atril da *Inspirado* en el primer combate siguiente |
| R-07 | **Golpe Certero** | 1 | El Golpe de Iniciativa resta −30 de Postura (en vez de −15) |
| R-08 | **Retirada Elegante** | 1 | Huir +25 %; no se pierden Orvales al huir |
| R-09 | **Piel de Pergamino** | 1 | +8 % de DEF y RES |
| R-10 | **Mente Clara** | 1 | +10 % de resistencia a estados |
| R-11 | **Inspiración Temprana** | 1 | Empiezas cada combate con 15 de Inspiración |
| R-12 | **Raíz Compartida** | 1 | Los Semillados de la banca ganan el 100 % de la XP (en vez del 50 %) |
| R-13 | **Contra el Borrador** | 1 | Tu Borrador tiene −20 % en todas sus estadísticas |
| R-14 | **Buen Comensal** | 1 | Las comidas de Berta duran una expedición más |
| R-15 | **Despertador** | 1 | +15 % de Ecos |
| R-16 | **Ojo de Bibliotecario** | 1 | Las Páginas Perdidas cercanas aparecen en el minimapa (radio corto) |
| R-17 | **Estudio Nocturno** | 1 | +5 % de XP |
| R-18 | **Lengua de Plata** | 1 | Precios de las tiendas −10 % y +10 % al vender |

### 5.10 RAÍZ PODRIDA — la rama prohibida (14 nodos)

**Cómo aparece:** al vencer al 2.º Señor y leer la primera Carta del Hereje, en la base del Árbol aparece una raíz negra con moho que antes no estaba. Sus niveles se abren según las Cartas **leídas**:
- Nivel I: tras la Carta 1.
- Nivel II: tras la Carta 3.
- Nivel III: tras la Carta 5.

**Reglas de Corrupción** (escala 0–100):
- Cada nodo comprado suma su **Corrupción** a la *Corrupción de raíz* (columna "Corr.").
- **Contestar** una Carta suma +5 a la *Corrupción de mancha* y abarata en −1 PH (mínimo 1) el siguiente nodo podrido.
- Cada uso de *Florecimiento* suma +10 de mancha.
- La interfaz muestra un solo número, la suma de ambas.

| ID | Nodo | Tipo | PH | Req. | Corr. | Nivel | Efecto |
|---|---|---|---|---|---|---|---|
| P-01 | **Moscas** | Activa | 1 | — | 2 | I | 1 PA · Podredumbre 60; 2 pilas de *Pudrición* |
| P-02 | **Sangría** | Activa | 1 | — | 3 | I | 0 PA · Sacrificas el 10 % de tu vida y ganas +2 PA |
| P-03 | **Hambre del Gusano** | Pasiva | 1 | P-01 | 3 | I | Robas como vida el 15 % del daño de Podredumbre |
| P-04 | **Contagio** | Activa | 1 | P-01 | 3 | I | 2 PA · Copia la *Pudrición* del objetivo a todos sus aliados |
| P-05 | Glosa: **Moscas Hambrientas** | Glosa | 1 | P-01 | 2 | I | *Moscas* aplica también el estado *Moscas* |
| P-06 | **Carne Terca** | Pasiva | 2 | P-03 | 4 | II | Una vez por combate sobrevives con 1 de vida; después pierdes el 5 % de vida por turno |
| P-07 | **Ofrenda** | Activa | 2 | P-02 | 5 | II | 3 PA · Un Semillado pierde el 50 % de su vida y haces Podredumbre 300. **El Semillado pierde 1 de Lealtad** |
| P-08 | **Susurro del Hereje** | Pasiva | 1 | P-04 | 4 | II | Los enemigos con 4 o más pilas de *Pudrición* tienen 20 % de caer en *Devoción* cada turno |
| P-09 | **Moho en la Página** | Pasiva | 1 | P-03 | 3 | II | Las habilidades de Podredumbre cuestan −1 PA (mínimo 1) |
| P-10 | **Plaga** | Activa | 2 | P-08 | 4 | II | 5 PA · 4 pilas de *Pudrición* a todos los enemigos |
| P-11 | **Daga de Hueso** | Activa | 2 | P-09 | 4 | III | 4 PA · Podredumbre 250; ignora DEF y RES |
| P-12 | **Rueda Rota** | Pasiva | 2 | P-10 | 3 | III | Durante un Eclipse: +30 % a todo tu daño y ventanas de Réplica sin penalización |
| P-13 | Piedra Angular: **El Vaso** | P. Angular | 3 | P-11 | 8 | III | Podredumbre ×1.6. **Contrapartida:** solo te curas con robo de vida |
| P-14 | Iluminación: **Florecimiento** | Iluminación | 3 | P-12 | 2 (+10 por uso) | III | Desbloquea la Iluminación de Podredumbre |

**Total de la rama:** 50 de Corrupción de raíz. Con las 6 Cartas contestadas (+30), un jugador que tome toda la rama llega a 80: por encima del umbral del final malo.

**Umbrales de Corrupción:**
| Corrupción | Efecto |
|---|---|
| 0–24 | Nada visible |
| **25** | Moho en los bordes de la interfaz; los menús hacen un zumbido de moscas al abrirse |
| **50** | Los aldeanos comentan que Teo "huele a sótano"; los Semillados con Lealtad baja dudan (10 % de perder su turno) |
| **70** | **Final "El Nuevo Vaso" disponible** (sus otros requisitos están en la Trama). La Pluma de Teo gotea tinta verde y la música del Árbol del Saber cambia |
| 90+ | Las Cartas del Hereje empiezan a llegar **ya contestadas**, con la letra de Teo |

**Bajar la Corrupción (Sanatorio del Templo):**
- *Purga*: −15 de **mancha** por 1 Lágrima de Luna + 500 × nivel Orvales.
- *Sellar raíz*: devuelve los PH de un nodo podrido y quita su Corrupción de **raíz**. El nodo queda sellado (se puede volver a comprar).
- La Corrupción de raíz **nunca** baja mientras tengas el nodo. Así se evita comprar toda la rama y "limpiarse" gratis.

### 5.11 SINERGIAS (12 nodos dorados)
| ID | Nodo | PH | Requiere | Efecto |
|---|---|---|---|---|
| X-01 | **Tinta Ardiente** | 2 | T-04 + B-01 | La *Mancha de Tinta* sobre un enemigo con *Ascua* explota: Brasa/Tinta 120 |
| X-02 | **Caramelo** | 2 | S-02 + B-01 | Golpear con Brasa a un enemigo en ámbar lo libera, pero ese golpe hace ×2 |
| X-03 | **Astronomía** | 2 | G-02 + L-03 | Una vez por ronda, *Cambio de Fase* cuesta 0 PA y revela las próximas 3 intenciones enemigas |
| X-04 | **Vivero de Batalla** | 2 | J-06 + S-04 | Los Semillados activos regeneran el 5 % de vida por turno |
| X-05 | **Edición Crítica** | 2 | T-06 + G-07 | Las Glosas del Tronco también se pueden aplicar a las habilidades transcritas |
| X-06 | **Forja de Guerra** | 2 | B-17 + J-10 | Todo el grupo empieza el combate con *Escudo de Escoria* |
| X-07 | **Rocío** | 2 | L-02 + S-05 | En Luna Llena, toda curación también quita 1 estado negativo |
| X-08 | **Táctica** | 2 | G-06 + J-07 | *Orden del Mariscal* también da +2 PA al Semillado |
| X-09 | **Crepúsculo** | 2 | L-01 + B-01 | Cada cambio de fase lanza una *Chispa* y un *Rayo de Luna* gratis a un enemigo al azar |
| X-10 | **Tinta de Plata** | 2 | T-07 + L-04 | Tus habilidades de Tinta usan el multiplicador de fase de la Luna (en vez del de Tinta) |
| X-11 | **La Rueda** | 2 | P-01 + S-04 | Cada tic de *Pudrición* sobre un enemigo cura al grupo el 50 % de ese daño. **No suma Corrupción** y reduce a la mitad la Corrupción de cada uso de *La Gran Ceniza*. *(Pista de diseño: es la única forma "sana" de usar la podredumbre, y anticipa el final verdadero.)* |
| X-12 | **Luna Enferma** | 2 | P-08 + L-05 | *Deslumbrado* también aplica 2 pilas de *Pudrición*. **+4 de Corrupción** |

**Conteo total:** 26 + 22 × 5 + 18 + 14 + 12 = **180 nodos.**

---

## 6. Builds de ejemplo (nivel 45)

### 6.1 "Lector de Réplica" (defensa que se vuelve ataque)
- **Atributos:** Destreza 55 · Voluntad 35 · resto balanceado.
- **Nodos clave:** *Margen Amplio*, *Disciplina*, *Contraguardia*, *La Guardia No Duerme*, *Contraataque Ensayado*, *Antítesis*, *Escritura Invertida*, *Pie de Página*, Piedra Angular *El Que No Cae*.
- **Bucle:** Guardar → defender combos enteros → Réplica Perfecta → Ruptura → Remate. Casi no gasta PA en atacar: los gasta en Escudos y en *Estandarte*.
- **Semillados:** Robleguardia (provoca, para concentrar los golpes) y Atlante de Jade.
- **Debilidad:** contra muchos ✦ y en Eclipse.

### 6.2 "Pirómano Erudito" (daño Brasa por acumulación)
- **Atributos:** Intelecto 60 · Voluntad 30.
- **Nodos clave:** *Chispa* + *Chispa Doble*, *Fuelle*, *Combustión*, *Brasa Paciente*, *Mediodía*, *Tinta Ardiente*, Piedra Angular *El Horno*.
- **Bucle:** sembrar *Ascua* en todos → *Fuelle* → explosiones de *Combustión* que además rompen Postura → *Mediodía* contra el que quede.
- **Semillados:** Ignaria y Escarabajo Solar (potencia el fuego); Robledulce para compensar el castigo de *El Horno*.
- **Debilidad:** Febriles (absorben Brasa). Obliga a volver al Mediodía Eterno con otra build o con otro Tintero.

### 6.3 "Pastor de Semillados" (el grupo es el arma)
- **Atributos:** Fe Lunar 40 · Memoria 40 · Vigor 35.
- **Nodos clave:** *Formación*, *Orden del Mariscal*, *Relevo*, *Táctica*, *Vivero de Batalla*, *Raíz Compartida*, Piedra Angular *Pastor del Bosque*.
- **Bucle:** Teo apoya (órdenes, PA y escudos) y 3 Semillados hacen el daño. Las Iluminaciones a Dúo son su clímax.
- **Debilidad:** daño propio bajo; sufre si le marchitan a dos Semillados.

### 6.4 "Sacerdote del Eclipse" (convertir el miedo de Orvalis en arma)
- **Atributos:** Fe Lunar 60 · Voluntad 35.
- **Nodos clave:** *Cambio de Fase*, *Fase Inmóvil*, Piedra Angular *Sacerdote del Eclipse*, *Eclipse Propio*, *Lluvia de Estrellas*, *Astronomía*. Opcional: *Rueda Rota* (podrida).
- **Bucle:** controlar la fase hasta Menguante → *Eclipse Propio* → dos rondas de Luna Negra devastadora. Contra jefes que provocan eclipses es la build que mejor responde.
- **Debilidad:** fuera del Eclipse cura poco. El Mediodía Eterno (Sin Luna) es su pesadilla.

### 6.5 "El Copista" (aprender del enemigo)
- **Atributos:** Memoria 60 · Intelecto 40.
- **Nodos clave:** *Lectura Profunda*, *Transcriptor*, *Ex Libris*, *Biblioteca Interior*, *Edición Crítica*, *Mente Ordenada*, Piedra Angular *El Copista*.
- **Bucle:** llegar a cada zona, leer y refutar para transcribir, y pelear con las armas de los Señores (por ejemplo, *Himno de los Mil* contra el propio Frente Eterno).
- **Debilidad:** al principio de cada Pliegue nuevo es débil hasta transcribir.

### 6.6 "El Corrompido" (el camino del Hereje)
- **Atributos:** Intelecto 50 · Vigor 40.
- **Nodos clave:** toda la Raíz Podrida, Piedra Angular *El Vaso*, *Sangría*, *Plaga*, *Daga de Hueso*, *La Gran Ceniza*.
- **Bucle:** *Sangría* → PA infinitos → *Plaga* → robo de vida. La build más poderosa en daño puro del juego, **a propósito**.
- **Precio:** supera 70 de Corrupción, los Semillados pierden Lealtad, los aldeanos se alejan y se abre el final "El Nuevo Vaso". La tentación de Corvan, ahora en manos del jugador.
- **Contrapunto sano:** *La Rueda* permite una "build de compost" con una parte de la rama podrida sin pasar de 40 de Corrupción.

---

## 7. Reinicio del Árbol (Aula de la Biblioteca)

| Opción | Costo | Notas |
|---|---|---|
| Primer reinicio total | Gratis | Una sola vez |
| Reinicio total | 1 Lágrima de Luna la segunda vez; +1 por cada reinicio siguiente (tope 5) | El Hermano Glosa: *"Releer no es de cobardes. Es de sabios con tiempo."* |
| Reiniciar una rama | 300 × nivel Orvales | Devuelve los PH de esa rama y sus Sinergias |
| Reiniciar atributos | 1 Lágrima de Luna | Devuelve todos los Puntos de Atributo |
| Nodos podridos | Solo en el Sanatorio, con *Sellar raíz* | El Aula no los toca |

---

## 8. Transcripción

### 8.1 Reglas
- Disponible después de liberar el **Índigo** (*Visión de Tinta*).
- Solo algunas habilidades enemigas son **transcribibles** (marcadas con una pluma dorada al Leerlas).
- Progreso: *Leer* +25 % · *Lectura Profunda* +50 % · *Refutar* esa habilidad +34 % · *Desviar* esa habilidad +20 % · *Transcriptor* ×1.5 · Memoria +1 % por punto.
- Al llegar al 100 %, se obtiene el **Borrador de Transcripción**: la habilidad al 70 % de su potencia original.
- En el **Scriptorium** de la Biblioteca se puede **pasar en limpio**: sube al 100 % y gana una Glosa propia. Cuesta Pergamino, Tinta Ferrogálica y Orvales.
- Las habilidades de los **Señores** solo se transcriben durante su combate y requieren *Lectura Profunda* + refutarlas o desviarlas al menos 2 veces. Son las mejores del juego.

### 8.2 Ejemplos de habilidades transcribibles
*Los nombres definitivos los fijan los documentos de cada Pliegue; esta lista sirve como plantilla de equilibrio.*

| Origen | Habilidad | PA | Efecto en manos de Teo (pasada en limpio) |
|---|---|---|---|
| Mar de Sal | **Coletazo de Sal** | 2 | Físico 90 a todos; *Errata* al 30 % |
| Selva Murmurante | **Rugido Verde** | 2 | Provocación sobre un Semillado y +20 % de DEF al grupo |
| Banquete Hueco | **Bocado Hueco** | 2 | Savia 100; roba el 30 % como vida; *Hambre* al objetivo |
| Banquete Hueco | **Servir la Mesa** | 3 | Cura al grupo un 25 %, pero con curación "hueca": dura 2 turnos y luego se pierde la mitad |
| Mediodía Eterno | **Martillazo Febril** | 3 | Brasa 160 [Rompe]; *Fiebre* a ti mismo |
| Mediodía Eterno | **Sudor de Bronce** | 1 | DEF +40 %, VEL −20 % durante 3 turnos |
| Palimpsesto | **Raspado** | 2 | Tinta 110 ◯◯; quita 1 efecto positivo |
| Palimpsesto | **Tachadura** | 3 | *Olvido* garantizado sobre 1 habilidad durante 2 turnos |
| Frente Eterno | **Grito de Trinchera** | 2 | El grupo gana *Carne Terca* durante 1 turno |
| Frente Eterno | **Carga Terca** | 3 | Físico 180; ignora la Provocación enemiga |
| Luna Falsa | **Nana de Polilla** | 3 | *Devoción* al 40 % a un enemigo |
| Luna Falsa | **Himno** | 2 | +1 PA por turno al grupo durante 2 turnos (*Marea Alta*); te aplica *Deslumbrado* |
| Señor (Anfitriona) | **Banquete Sin Fondo** | 5 | Cura al grupo por completo; los enemigos ganan *Hambre* |
| Señor (Sol Cautivo) | **Corazón de Horno** | 5 | Brasa 380 a todos; tú recibes el 10 % de tu vida |
| Señor (Gran Correctora) | **Fe de Ratas** | 4 | Borra los 2 últimos turnos de un enemigo: vuelve atrás su vida y su Carga |
| Señor (El Que No Cae) | **No Hoy** | 4 | Todo el grupo gana *Vigilia* |
| Señor (Voz del Coro) | **Coro de los Mil** | 5 | *Devoción* al 60 % a todos los enemigos durante 1 turno |

---

## 9. Lecturas (libros que hacen más fuerte a Teo)

- Los **libros** se encuentran en el mundo (estanterías, arcones, recompensas de misión). Se leen en un **atril**: una pantalla de lectura con una página de texto de ambientación y una ilustración.
- Cada **Lectura** da un bono permanente. Las **Obras Mayores** (★) también dan +1 PH.
- Hay **30 libros**: 10 Obras Mayores y 20 menores. Leerlos todos completa el logro *Bibliófilo*.

| Libro | Dónde (sugerencia) | Bono |
|---|---|---|
| ★ *Gramática del Glifo Lunar* (Academia Arcana) | Palimpsesto | +2 Memoria · +1 PH |
| ★ *Tratado de Esgrima de la Reina Ismara* | Frente Eterno | +2 Destreza · +1 PH · Desviar +1 f |
| ★ *Las Mil Semillas: Crónica del 412* | Bastión | +2 Fe Lunar · +1 PH · Semillados +5 % |
| ★ *Leyes del Libro Abierto* (copia de Orval I) | Antesala, tras el 1.er Señor | +2 Voluntad · +1 PH |
| ★ *Recetario de la Gran Ceniza* (Hestra Moll, joven) | Banquete Hueco | +2 Vigor · +1 PH · objetos +10 % |
| ★ *Cuaderno de Fundición del Maestro Ferrum* | Mediodía Eterno | +2 Intelecto · +1 PH · Brasa +5 % |
| ★ *Cartas Celestes de Ptolem* | Luna Falsa | +2 Fe Lunar · +1 PH · con Fe Lunar ≥ 30 el combate empieza en Creciente |
| ★ *Diario de Imelda la Lectora* | Palimpsesto (zona secreta) | +2 Intelecto · +1 PH · Leer +1 PA |
| ★ *Manual del Arquitecto de Savia* | Raíces del árbol | +2 Vigor · +1 PH · Amparo +10 % |
| ★ *El Cuento de Orvalis, edición de la Corona* | Las Entrañas | +3 a todos los atributos · +1 PH |
| *Bestiario Menor de Merova* | Merova (Prólogo) | +5 % de daño contra Bestias |
| *Coplas de la Caravana* | Zahra | +5 % de Orvales |
| *Herbolaria de la Selva* | Selva Murmurante | Las curas de objetos +10 % |
| *Tratado sobre la Sal* | Mar de Sal | +10 % de resistencia a *Hambre* |
| *Ordenanzas del Mercado* (Salvio) | Granero | Precios −5 % |
| *Del Temple del Bronce* | Mediodía Eterno | DEF +5 % |
| *Índice de los Índices* | Palimpsesto | Transcripción +10 % |
| *Catálogo del Ala Sellada* (incompleto) | Palimpsesto | Revela la ubicación de 3 Páginas del Gusano |
| *Cantos de Trinchera* | Frente Eterno | Provocación +1 turno |
| *Himnario de Ilunara* | Luna Falsa | Inmunidad a *Devoción* durante el primer turno de cada combate |
| *Manual de la Guardia* | Bastión | Réplica Perfecta +5 % |
| *Cartografía del Albar* | Hito de 60 Páginas Perdidas (Archivo) | Muestra el mapa completo de cada Pliegue al entrar (sin secretos) |
| *Calendario de Eclipses* | Observatorio | El Eclipse enemigo se anuncia con 1 turno más de anticipación |
| *Los Hijos del Gusano* (texto sellado) | Las Entrañas | +5 % Podredumbre. **+2 Corrupción** |
| *Cuadernos de Anatomía Conservada* | Las Entrañas | +5 % de vida |
| *Fábulas para Princesas* | Templo | Iluminación +5 % |
| *Tratado de Postura* | Arena del Bastión | Daño a la Postura +5 % |
| *Arte de la Huida* | Mar de Sal | Huir +10 % |
| *Florilegio de Errores* | Encuadernador | Tu Borrador suelta +10 % de intereses |
| *Poemas Inacabados* (autor desconocido, firmados "C.") | Al reunir 4 Páginas del Gusano | Inspiración +5 %. *(Son de Corvan joven.)* |

---

## 10. Equipo

### 10.1 Espacios
| Espacio | Qué aporta |
|---|---|
| **Pluma** (arma) | ATQ, POD y forma del ataque básico (número de Trazos, alcance). Define la animación del Remate |
| **Tomo** (mano secundaria) | POD, Memoria y 1 pasiva propia |
| **Atuendo** | DEF, RES, vida y resistencias a estados |
| **Tintero** | **Cambia el elemento del ataque básico** y añade un efecto a los Trazos |
| **Marcapáginas ×2** (accesorios) | Afijos libres y efectos especiales |

### 10.2 Tinteros (definen el estilo del ataque básico)
| Tintero | Elemento | Efecto en el Trazo Firme |
|---|---|---|
| **Tinta Común** (inicial) | Tinta | — |
| **Tinta Ferrogálica** | Tinta | +3 de Postura |
| **Tinta de Ascua** | Brasa | 20 % de *Ascua* |
| **Tinta de Resina** | Savia | 10 % de *Ambarizado* |
| **Tinta de Nácar** | Luna | +1 de Inspiración extra |
| **Tinta de Hierro** | Físico | +10 % de daño crítico |
| **Tinta de Sepia** | Tinta | 25 % de *Mancha de Tinta* |
| **Tinta de Agalla Negra** | Podredumbre | 1 pila de *Pudrición*. **+3 de Corrupción la primera vez que se equipa** |

### 10.3 Rarezas
| Rareza | Color | Afijos | Engarces | Notas |
|---|---|---|---|---|
| **Común** | Gris | 0 | 0 | — |
| **Raro** | Azul | 1–2 | 0 | — |
| **Épico** | Violeta | 2–3 | 1 | — |
| **Legendario** | Dorado | 3 + 1 **afijo único** | 2 | Efecto especial con nombre |
| **Primigenio** | Plata lunar | 2 fijos + 1 efecto único | 3 | Reliquias de Orvalis con entrada propia en el Cuento. Se mejoran (+1 a +5) en el **Horno de Reliquias** con Corazones de Señor y Lágrimas de Luna |

- **Nivel de objeto** = nivel del enemigo o cofre (±2). Sus estadísticas base escalan +4 % por nivel.
- **Mejora en la Herrería**: de +1 a +10; cada nivel da +4 % a las estadísticas base. Costo en §4 de `Economia_Recompensas_y_Aldea.md`.

### 10.4 Afijos (ejemplos a nivel 45)
| Prefijo (ofensivo) | Rango | Sufijo (defensivo y utilidad) | Rango |
|---|---|---|---|
| **Afilado**: ATQ + | 8–22 | **…del Roble**: vida + | 40–120 |
| **Erudito**: POD + | 8–22 | **…del Atril**: Memoria + | 1–4 |
| **Candente**: daño Brasa % | 5–15 % | **…de la Muralla**: DEF % | 5–15 % |
| **Resinoso**: daño Savia % | 5–15 % | **…del Velo**: RES % | 5–15 % |
| **Plateado**: daño Luna % | 5–15 % | **…del Mariscal**: resistencia a estados % | 5–15 % |
| **Entintado**: daño Tinta % | 5–15 % | **…de la Vigilia**: ventana de Réplica + (frames) | 1 |
| **Certero**: crítico % | 2–6 % | **…del Molino**: VEL + | 3–9 |
| **Rompedor**: daño a la Postura % | 5–15 % | **…del Banquete**: curación recibida % | 5–15 % |
| **Inspirado**: Inspiración ganada % | 5–12 % | **…del Tintero**: PA máximo + | 1 (solo Legendario) |
| **Encadenado**: Réplica Perfecta % | 5–15 % | **…del Viajero**: Orvales % | 5–15 % |

**Afijos únicos de Legendarios (ejemplos):**
- *"El tercer Trazo siempre es Firme."*
- *"Cada Ruptura te da una Nota al Margen."*
- *"Al refutar, la letra devuelta rebota a otro enemigo."*
- *"Si terminas un combate sin recibir daño, el siguiente empieza con 50 de Inspiración."*

### 10.5 Runas y Palabras Rúnicas
Las **runas** son letras del **Glifo Lunar** talladas en Piedra Lunar. Se engarzan en el **Taller de Runas** de la Forja. Al reforjar en el Taller nivel 5, un Legendario gana un 3.er engarce.

| Runa (letra) | Bono solo |
|---|---|
| **A** (Ala) | +5 de VEL |
| **C** (Cera) | +8 % de curación recibida |
| **E** (Eco) | +5 % de daño de la Réplica Perfecta |
| **F** (Fuelle) | +5 % de Brasa |
| **I** (Índice) | +1 de Memoria |
| **L** (Lámpara) | +5 % de Luna |
| **M** (Molino) | +5 % de Savia |
| **N** (Noche) | Esquivar +1 frame |
| **O** (Ojo) | +3 % de crítico |
| **R** (Raíz) | +5 % de vida |
| **S** (Sello) | +8 % de resistencia a estados |
| **U** (Umbral) | +5 % de Orvales |
| **Z** (Zarza) | +5 % de devolución de daño físico |

**Palabras Rúnicas** (3 runas en el orden exacto, en un mismo objeto):
| Palabra | Runas | Efecto |
|---|---|---|
| **LUZ** | L-U-Z | En Luna Llena, tus Réplicas Perfectas lanzan un *Rayo de Luna* gratis |
| **SOL** | S-O-L | Inmunidad a *Fiebre* y a *Ascua* |
| **MAR** | M-A-R | +1 PA cada vez que cambia la fase lunar |
| **ECO** | E-C-O | El contraataque de la Réplica Perfecta golpea dos veces |
| **FIN** | F-I-N | Los Remates Ilustrados dan +1 Ecos y +10 de Inspiración |
| **SAL** | S-A-L | Inmunidad a *Hambre*; +10 % de vida |
| **MIL** | M-I-L | Los brotes señuelo y los Semillados invocados duran 1 turno más |

### 10.6 Ejemplos de Primigenios
*Se forjan en el Horno de Reliquias con el Corazón de cada Señor. Sus historias van en el Cuento.*

| Primigenio | Espacio | Efecto único |
|---|---|---|
| **Cucharón de la Anfitriona** | Pluma | Cada golpe básico cura al grupo un 2 %. "Comida que sí alimenta." |
| **Delantal del Maestro Ferrum** | Atuendo | Inmune a *Ascua*; los Desvíos hacen Brasa 60 |
| **Lentes de Ysolde** | Marcapáginas | *Leer* revela también la siguiente intención de **todos** los enemigos. *(Solo si Ysolde fue salvada; si no, se obtienen los **Lentes Rotos**: la mitad del efecto.)* |
| **Estandarte del Que No Cae** | Tomo | Una vez por combate, todo el grupo gana *Vigilia* al bajar del 30 % de vida |
| **Velo de la Penitente** | Marcapáginas | Inmune a *Devoción*; Refutar +2 frames |
| **Marcapáginas de Lys** | Marcapáginas | +10 de Inspiración por turno durante las fases Llena y Creciente. *(Se consigue en los Sueños de Plata.)* |
| **Tintero de Imelda** | Tintero | Tinta; cada Trazo Firme tiene 25 % de devolver 1 PA |
| **Corona de Corteza (astilla)** | Marcapáginas | +2 a todos los atributos; los Semillados ganan +1 de Lealtad más rápido. *(Al final, el Viejo Polilla la reconoce.)* |

---

## 11. Resumen para implementación
- **Datos de nodos:** tabla con `id, rama, tipo, costo_ph, requisitos[], corrupción, efecto_id, parámetros`.
- **Efectos:** componentes reutilizables (daño, estado, PA, iniciativa, fase, escudo, invocación, modificador de ventana) que se combinan por parámetros, no en código especial por habilidad.
- **Las Glosas** se implementan como *modificadores* sobre la definición de una activa (por ejemplo, `hits += 2; costo_pa += 1`).
- **Las Piedras Angulares** son modificadores globales con una regla de contrapartida.
- **La Corrupción** se guarda en dos campos (`corrupcion_raiz` y `corrupcion_mancha`) y se muestra como su suma.
