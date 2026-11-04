# SISTEMA DE COMBATE Y RÉPLICA

> Documento de diseño de sistemas. Depende de `01_CANON.md` (§11).
> Los nombres de enemigos que aparecen aquí son **ejemplos ilustrativos**. Los nombres definitivos de cada enemigo están en los documentos de cada Pliegue; las **familias** de enemigos y sus afinidades se definen aquí.
> Todas las cifras son de primera versión y se ajustan en las pruebas de juego.

---

## 1. Principios

1. **Pensar en tu turno, reaccionar en el del enemigo.** El turno propio es táctico (menús, PA, orden de iniciativa). El turno enemigo es activo: la **Réplica** convierte cada golpe recibido en una oportunidad.
2. **Leer antes de pelear.** Teo es bibliotecario: analizar al enemigo (comando **Leer**) siempre da información útil, PA y progreso de Transcripción.
3. **Nunca un turno muerto.** Incluso cuando el enemigo actúa, el jugador tiene algo que hacer.
4. **El espectáculo es una recompensa mecánica.** Las Réplicas Perfectas, las Rupturas, los Remates Ilustrados y las Iluminaciones dan ventajas reales, y además son los momentos visuales más fuertes del juego (ver `arte/Biblia_de_Efectos_Visuales.md`).
5. **La dificultad cambia los reflejos que se exigen, no la profundidad del sistema.** Todas las mecánicas existen en todas las dificultades; lo que cambian son las ventanas de tiempo.

---

## 2. Estructura de un encuentro

### 2.1 Participantes
| Lado | Composición |
|---|---|
| Jugador | **Teo** + hasta **2 Semillados activos** (1 durante el Acto I; el segundo espacio se abre al vencer al primer Señor). Banca de reserva: de 3 a 6 Semillados según el nivel del Vivero. Con la Piedra Angular *Pastor del Bosque* hay 3 Semillados activos. |
| Enemigos | De 1 a 5 enemigos. Los jefes pueden traer adds (refuerzos), partes destructibles (brazos o núcleos) o apoyos de escenario. |
| Invitados | En momentos de historia se suman aliados temporales controlados por el jugador (por ejemplo: Zahra en el Mar de Sal, Dietrich contra la Madre Larva y Lys en la batalla final). Ocupan un espacio adicional y no cuentan para la banca. |

### 2.2 Entrar al combate (exploración → batalla)
Los enemigos se ven en el mapa; no hay encuentros aleatorios.

| Situación | Efecto al iniciar |
|---|---|
| **Golpe de Iniciativa**: Teo golpea al enemigo con la Pluma en el mapa antes de que lo toque | El grupo actúa primero; todos los enemigos empiezan con **−15 Postura** y −10 % de Velocidad durante la primera ronda |
| **Encuentro neutral** (contacto frontal) | Orden normal según la Velocidad |
| **Emboscada** (el enemigo toca a Teo por la espalda) | Los enemigos actúan primero y el grupo empieza con 1 PA menos |
| **Evasión** | Con *Viento de Molino* Teo puede atravesar a un enemigo sin pelear; tiene un tiempo de espera de 6 s |
| Enemigos de nivel muy inferior (≥ 10 niveles por debajo) | Con el Golpe de Iniciativa se gana **sin pelear** (victoria automática con nota *Aprobado*) |

### 2.3 Fin del combate
- **Victoria**: aparece la pantalla de **Calificación** (§13) y se reparten XP, Orvales, Ecos y botín.
- **Derrota**: Teo despierta en el último atril y aparece **Tu Borrador** (§14).
- **Huida**: sin recompensas ni nota.

---

## 3. La Línea de Iniciativa (orden de turnos)

El combate usa **turnos por tiempo**, no rondas fijas. Arriba de la pantalla hay una tira con forma de **listón de marcapáginas** que muestra los **próximos 10 turnos** con el retrato de cada combatiente.

### 3.1 Fórmulas
```
Velocidad (VEL)     = 80 + Destreza + bonos de equipo y estados
Retraso base        = 10000 / VEL                         (en "ticks")
Retraso de acción   = Retraso base × Peso de la acción
Peso de la acción   = Ligera 0.8 · Normal 1.0 · Pesada 1.3 · Iluminación 1.5
```
- Cada combatiente tiene un contador. Actúa el que tiene el contador más bajo. Después de actuar, su contador sube según el **Retraso de acción**.
- **Ronda** = 1000 ticks del reloj del combate. Las Fases Lunares, los estados y las regeneraciones cuentan en rondas.
- En la tira de iniciativa se ve un **icono de luna** en el punto donde cambiará la fase.

### 3.2 Manipular la iniciativa
| Efecto | Qué hace |
|---|---|
| **Errata** (estado) | El siguiente turno del objetivo se retrasa +30 % de su Retraso base |
| **Punto y Aparte** (habilidad) | Empuja al objetivo 2 posiciones atrás en la tira |
| **Orden del Mariscal** | Un Semillado aliado actúa de inmediato |
| **Ruptura** | El enemigo roto pierde su siguiente turno y se va al final de la tira |
| **Fiebre** | Su Velocidad sube 20 % |

Al pasar el cursor por una habilidad, la tira muestra **una vista previa** de cómo quedaría el orden. Es la herramienta táctica principal.

---

## 4. Puntos de Acción (PA)

Los PA se muestran como **gotas de tinta dentro de un tintero** junto al retrato de Teo.

### 4.1 Reglas de Teo
| Regla | Valor |
|---|---|
| PA al iniciar el combate | 3 (más bonos: *Capítulo Uno*, *Índice* y emboscada −1) |
| PA ganados al inicio de cada turno de Teo | +2 |
| Máximo de PA | `6 + floor((Voluntad − 10) / 15)`, con tope de **10**. *Tintero Hondo* da +1 extra (máximo absoluto: 11) |
| Almacenamiento | Los PA que no se usan **se guardan** entre turnos hasta el máximo |
| Ataque básico | +1 PA (más +1 si los 3 Trazos son firmes) |
| Leer | +1 PA |
| Guardar (defender) | +2 PA, −40 % de daño recibido hasta el siguiente turno y +2 frames en todas las ventanas de Réplica |
| Desviar o refutar una acción enemiga completa | +1 PA (máximo 1 por acción enemiga, aunque tenga varios golpes) |
| Réplica Perfecta | +2 PA en total (no se suma al punto anterior) |
| Romper la Postura de un enemigo | +1 PA |

### 4.2 Semillados
Cada Semillado tiene **su propia reserva de PA**: máximo 5, empieza el combate con 2 y gana +2 por turno. Sus habilidades cuestan de 0 a 4 PA. Ver `sistemas/Semillados.md`.

### 4.3 Enemigos
Los enemigos no usan PA visibles. Usan **Carga**: algunos ataques necesitan 1 o 2 turnos de preparación, que se ven en el icono de intención. *Hambre* y *Errata* afectan la Carga.

---

## 5. Comandos

| Comando | Costo | Efecto |
|---|---|---|
| **Atacar** | 0 PA | Combo de 3 **Trazos** con la Pluma. El daño y el elemento dependen del **Tintero** equipado. Genera PA. |
| **Grimorio** | Variable | Habilidades equipadas: activas del Árbol del Saber y habilidades transcritas. |
| **Semillados** | — | **Ordenar** (el Semillado usa una habilidad en su turno; se le puede dejar en automático) · **Relevo** (cambiar por uno de la banca: ocupa el turno del Semillado que entra; *Relevo* del Árbol lo hace gratis) |
| **Objetos** | Ocupa el turno | Máximo 1 objeto por turno de Teo. Incluye las *Raciones* de Berta, tónicos y pergaminos de un solo uso. |
| **Leer** | Ocupa el turno, da +1 PA | Revela vida, afinidades, intención exacta y un rasgo oculto. Con *Visión de Tinta* también revela golpes ocultos y hace avanzar la Transcripción (§17). |
| **Guardar** | Ocupa el turno | Defensa (ver §4.1). |
| **Huir** | Ocupa el turno | Probabilidad `50 % + 2 % × (VEL de Teo − VEL media enemiga) + 15 % por cada intento fallido`, con un mínimo de 10 %. **Imposible contra jefes** y en combates de historia. |

### 5.1 Trazos: timing ofensivo
Cuando Teo ataca (ataque básico y habilidades marcadas como **[Trazo]**), en cada golpe aparece un **círculo de tinta** que se cierra. Si el jugador presiona en el instante del impacto:
- **Trazo Firme**: +20 % de daño, +2 de daño a la Postura y +2 de Inspiración.
- Si falla, el golpe hace daño normal. **Nunca hay castigo.** Es un premio, no una exigencia.
- La ventana del Trazo dura 8 frames en *Crónica* y no cambia mucho con la dificultad (ver §6.2).

---

## 6. LA RÉPLICA (defensa reactiva)

La Réplica es la columna vertebral del combate. Cuando un enemigo ataca a **cualquier miembro del grupo**, el jugador puede reaccionar. Narrativamente, Teo "le contesta" al ataque como quien rebate un argumento.

### 6.1 Glifos de Intención
Antes de cada golpe enemigo aparece **un glifo** sobre el objetivo, dentro de un **anillo de tinta que se cierra**. Cuando el anillo toca el borde del glifo, ocurre el impacto.

| Glifo | Tipo de golpe | Defensas válidas | Botón por defecto (mando / teclado / táctil) |
|---|---|---|---|
| ◆ | **Físico** | Desviar (ideal) o Esquivar | Botón derecho / `J` / tocar el glifo |
| ◯ | **Mágico** | Refutar (ideal) o Esquivar | Secuencia de direcciones / flechas / deslizar |
| ▲ | **Área a ras de suelo** | Saltar (ideal) o Esquivar | Botón inferior / `Espacio` / deslizar hacia arriba |
| ✦ | **Imparable** (agarres, rayos y golpes del final) | **Solo Esquivar** | Gatillo / `K` / deslizar hacia un lado |
| ? | **Golpe oculto** | Cualquiera, pero no se sabe cuál | Se revela con Leer o con Visión de Tinta |

Los glifos tienen **forma, color y sonido distintos**: se pueden jugar sin distinguir colores y sin ver la pantalla perfecta (§6.8).

### 6.2 Ventanas de tiempo (a 60 fps)
El **frame 0** es el impacto. La ventana se expresa como (inicio, fin) respecto al impacto.

| Acción | *Cuento* (fácil) | *Crónica* (normal) | *Epopeya* (difícil) | *Palimpsesto* (extremo, desbloqueable) |
|---|---|---|---|---|
| **Esquivar** | 20 f (−14, +6) | 14 f (−10, +4) | 10 f (−7, +3) | 8 f (−6, +2) |
| **Desviar** | 12 f (−8, +4) | 8 f (−6, +2) | 5 f (−4, +1) | 4 f (−3, +1) |
| **Desvío tardío** (50 % de daño) | +6 f después de la ventana | +4 f | +2 f | no existe |
| **Refutar** (por cada letra) | 16 f | 11 f | 8 f | 6 f |
| **Saltar** | 18 f | 13 f | 10 f | 8 f |
| **Trazo Firme** (ofensivo) | 12 f | 8 f | 7 f | 6 f |
| **Anticipación del glifo** (cuánto antes aparece) | 45 f | 35 f | 25 f | 20 f |
| **Bloqueo tras fallar** (evita machacar botones) | 10 f | 16 f | 20 f | 24 f |

**Modificadores de ventana** (se suman y tienen un tope de +4 f sobre la base):
- Destreza: +1 f cada 25 puntos (máximo +3).
- Nodos: *Margen Amplio* (+1 en Desviar y Esquivar), *Disciplina* (+1 en Desviar), *Ojo de la Diosa* (+2 en Refutar), *Luna Nueva Oculta* (+3 en Esquivar durante Luna Nueva).
- Guardar: +2 f en todas.
- Lealtad del Semillado defendido: de −2 f (Lealtad 0) a +2 f (Lealtad 5).
- Estados: *Deslumbrado* (−10 f de anticipación), *Eclipse* (−2 f en todas), *Enraizado* (no se puede esquivar).

### 6.3 Resultados de cada defensa
| Resultado | Daño recibido | Postura del atacante | PA | Inspiración | Notas |
|---|---|---|---|---|---|
| **Esquivar** correcto | 0 | — | — | +4 | Seguro, pero no rompe nada. Las Réplicas Perfectas no cuentan esquives |
| **Desviar** correcto | 0 | −8 por golpe | +1 por acción | +8 | Sonido de pluma rasgando papel y destello de tinta |
| **Desvío tardío** | 50 % | −3 | — | +3 | Golpe de "roce": salpicadura de tinta gris |
| **Refutar** completo | 0 y devuelve **40 %** del daño como Tinta | −10 | +1 por acción | +10 | *Escritura Invertida* sube la devolución a 60 % |
| **Refutar** parcial (algunas letras) | 100 % − 20 % por letra acertada | −2 por letra | — | +2 por letra | |
| **Saltar** correcto | 0 | — | — | +5 | Cuenta para la Réplica Perfecta |
| **Fallo** o sin reacción | 100 % | — | — | +4 (por recibir daño) | |
| **Desviar un ✦** | 100 % y **Vacilación** (−1 PA) | — | −1 | — | Castiga confundir un imparable con un golpe físico |

### 6.4 Refutar: la secuencia de letras
Los ataques ◯ muestran de **1 a 4 letras de Glifo Lunar** que entran al anillo una tras otra, cada una con una dirección (↑ ↓ ← →). El jugador marca la dirección cuando cada letra toca el borde.
- Conjuros débiles: 1 letra. Conjuros de élite: 2 o 3. Conjuros de Señor: 3 o 4, a veces con letras dobles (dos direcciones a la vez, en diagonal).
- En móvil, cada letra se contesta deslizando el dedo en su dirección.
- **Modo de un solo botón** (accesibilidad): todas las letras se contestan con el mismo botón; la devolución baja a 25 %.

### 6.5 Réplica Perfecta
**Condición:** el grupo contesta **todos los golpes** de una acción enemiga con Desviar, Refutar o Saltar. Los esquives no cuentan; los desvíos tardíos tampoco.

**Efecto:**
1. *Hit-stop* de 10 frames. El fondo se vuelve papel monocromo y Teo aparece en silueta de tinta (ver la biblia de efectos).
2. **Contraataque automático** de Teo:
   - Potencia 150 del elemento de su Tintero.
   - Postura −30.
   - Si el golpe mata o rompe al enemigo, encadena directo a un **Remate Ilustrado** (§8).
3. +2 PA y +25 de Inspiración.
4. **Cadena de Réplicas**: si en la misma ronda se logra otra Réplica Perfecta contra otro enemigo, el contraataque sube ×1.1 (acumula hasta ×1.5).
5. Con *Contraguardia* el contraataque gana +30 % de daño; con *La Guardia No Duerme*, los Semillados defendidos también contraatacan con su habilidad básica.

**Tamaño de los combos enemigos:**
| Rango del enemigo | Golpes por acción |
|---|---|
| Común | 1–2 |
| Élite | 2–4 |
| Mini-jefe | 3–5 |
| Señor | 3–7 (algunos golpes mezclan glifos distintos) |
| Final | Hasta 9, con ✦ intercalados |

### 6.6 Variaciones de ritmo (lo que hace profunda a la Réplica)
| Variación | Descripción | Cómo se lee |
|---|---|---|
| **Finta** | El enemigo amaga, se detiene de 15 a 40 frames y luego golpea | La tinta del anillo **tiembla**. El sonido de pluma (el aviso real) suena siempre **35 frames antes del impacto verdadero**. El oído no miente |
| **Retraso** | Golpe lento, con una carga larga | El anillo se cierra más despacio. Hay que medir el tiempo, no reaccionar al movimiento |
| **Eco** | El golpe se repite con un retraso fijo (por ejemplo, la Gran Correctora borra y "re-escribe" el golpe) | Aparece un **glifo fantasma** detrás del primero |
| **Doble glifo** | Dos golpes casi simultáneos de distinto tipo (◆ + ▲) | Se contesta con dos botones: *Desviar* y luego *Saltar* |
| **Golpe oculto ?** | El glifo no se ve | Se revela si el enemigo fue **Leído** en este combate o con Visión de Tinta |
| **Golpe a varios** | Ataque que cae sobre todo el grupo | Aparece un glifo sobre cada objetivo; se contesta una vez por objetivo, en orden de izquierda a derecha |
| **Cambio de objetivo** | El enemigo cambia de objetivo a mitad del combo | El glifo **salta** con una estela; el anillo se reinicia |
| **Ritmo musical** | Algunos jefes (Coristas, la Voz del Coro) atacan al ritmo de la música del combate | Los golpes caen en los tiempos fuertes del compás |

### 6.7 Quién defiende a quién
- El jugador contesta **por cualquier aliado atacado**: Teo, sus Semillados o un invitado.
- La ventana usa los modificadores del **objetivo** (Lealtad, estados).
- Un Semillado en **Relevo** durante el turno enemigo no puede ser defendido (sale del campo).

### 6.8 Accesibilidad y asistencia
| Opción | Efecto | Penalización |
|---|---|---|
| **Lectura Lenta** | El tiempo se ralentiza al 50 % durante los 20 frames anteriores a cada impacto | Ninguna |
| **Réplica Asistida** | Las ventanas se duplican | −20 % de Inspiración ganada por Réplica |
| **Réplica Automática** | El juego defiende solo con 60 % de éxito (solo Esquivar y Desviar) | Sin Réplica Perfecta; tope de Calificación: *Notable* |
| **Avisos de sonido reforzados** | Un tono distinto para cada tipo de glifo | Ninguna |
| **Un solo botón** | Todas las defensas usan el mismo botón; el juego elige la correcta | La devolución de Refutar baja a 25 %; Esquivar no existe por separado |
| **Glifos grandes y alto contraste** | Glifos al 150 % con borde blanco | Ninguna |
| **Vibración** | Pulso del mando 35 frames antes del impacto | Ninguna |
| **Reasignar controles** | Todo se puede reasignar | Ninguna |
| **Pantalla quieta** | Reduce el temblor de pantalla, los destellos y la aberración cromática | Ninguna |

Las opciones se pueden cambiar en cualquier momento y **no bloquean logros**, salvo los logros de Matrícula de Honor, que exigen Réplica manual.

---

## 7. Postura y Ruptura

Cada enemigo tiene una **barra de Postura** (blanca, debajo de su barra de vida). Al vaciarla, el enemigo sufre una **Ruptura**.

### 7.1 Valores de Postura
| Rango | Postura | Regeneración |
|---|---|---|
| Común | 40 | 10 % por turno propio si no recibió daño a la Postura en la última ronda |
| Élite | 80 | Igual |
| Mini-jefe | 150 | Igual |
| Señor (por fase) | 300 | 5 % por turno; tras una Ruptura, **Recomposición**: inmune a daño de Postura durante 2 turnos |
| El Hereje y Sapros | 400–600 | Reglas especiales por fase |

### 7.2 Daño a la Postura
| Fuente | Daño a la Postura |
|---|---|
| Golpe básico | 4 (el 3.er Trazo: 8) |
| Trazo Firme | +2 |
| Golpe a una debilidad | +10 |
| Crítico | +6 |
| Desviar (por golpe) | 8 |
| Refutar (acción completa) | 10 |
| Réplica Perfecta | 30 |
| Habilidades con la etiqueta [Rompe] | Fijo, según la habilidad (por ejemplo, *Golpe de Yunque*: ×2 de su daño normal a la Postura) |
| *Subrayado* en el objetivo | +20 en el siguiente golpe |
| Ascua con *Brasa Paciente* | 3 por cada tic de quemadura |

### 7.3 Efectos de la Ruptura
- El enemigo **pierde su siguiente turno** y se va al final de la línea de iniciativa.
- DEF y RES −50 %.
- **Todo daño ×1.5.**
- Su Carga acumulada se pierde.
- El grupo gana +1 PA y +15 de Inspiración.
- Se abre la opción de **Remate Ilustrado** si se cumplen las condiciones (§8).

---

## 8. Remate Ilustrado

Un golpe final con estética de **viñeta de cómic o manuscrito**: la pantalla se divide en paneles, el sonido se corta y el golpe se "dibuja".

| Condición | Efecto |
|---|---|
| Enemigo común o élite en Ruptura y con ≤ 50 % de vida | **Lo derrota** sin importar la vida que le quede. Botín +1 tirada y +5 puntos de Calificación |
| Mini-jefe en Ruptura y con ≤ 35 % de vida | Daño = 20 % de su vida máxima y fin de su fase actual |
| Señor en Ruptura y con ≤ 35 % de vida en la fase | Daño = 8 % de su vida máxima y escena especial; da una **Hoja Ilustrada** (material de forja) |
| Semillado Corrompido en Ruptura | Opción **Rescatar** en lugar de rematar: lo purifica y suelta su semilla (ver `Semillados.md`) |

- Cuesta **0 PA** y ocupa el turno de Teo.
- La animación depende de la combinación de **Pluma + Tintero**. Hay **24 remates coleccionables** que se registran en el Cuento como "Ilustraciones".

---

## 9. Fases Lunares y Eclipse

### 9.1 El ciclo
Cada combate tiene una **fase lunar** que avanza cada **2 rondas** en este orden: **Nueva → Creciente → Llena → Menguante → Nueva…**

- **Fase inicial**: la misma que la luna del reloj del mundo en la exploración (el cielo del árbol tiene ciclo día y noche). Con *Plegaria de Vigilia* y Fe Lunar ≥ 40, el combate empieza en Llena.

| Fase | Daño Luna | Otros efectos |
|---|---|---|
| **Luna Nueva** | ×0.7 | Tinta +10 % (*"lo escrito no necesita luz"*); +2 f en Esquivar; Pútridos +10 % de daño |
| **Creciente** | ×1.0 | +5 de Inspiración al inicio de cada turno de Teo |
| **Llena** | ×1.4 | Curación ×1.25; +2 f en Refutar; los Coristas ganan +10 % de daño |
| **Menguante** | ×1.1 | +10 % de probabilidad de crítico; daño a la Postura +20 % |

### 9.2 Reglas especiales por Pliegue
Son propuestas de sistema; los documentos de cada Pliegue pueden ajustarlas.

| Pliegue | Regla lunar |
|---|---|
| El Banquete Hueco (Ámbar) | **Luna de Cosecha** fija (cuenta como Llena), pero toda curación es ×0.6 ("hueca") |
| El Mediodía Eterno (Carmesí) | **Sin Luna**: la fase no avanza. Luna ×0.5. Solo objetos o habilidades raras crean una "luna de bolsillo" durante 2 rondas |
| El Palimpsesto (Índigo) | La fase **está oculta** (se ve "?") hasta que se usa Leer o Visión de Tinta |
| El Frente Eterno (Jade) | Las fases cambian **cada ronda** (el cielo de la guerra está loco) |
| El Santuario de la Luna Falsa (Plata) | **Llena Falsa**: la curación que hace Teo también cura 30 % a los enemigos Coristas. La Llena real se recupera en la fase final contra la Voz del Coro |
| Las Entrañas | Ciclo normal hasta el combate final, donde comienza **el Gran Eclipse** |

### 9.3 Eclipse
Lo provocan los jefes (lo anuncia el icono de un anillo negro en la línea de iniciativa) o Teo con *Eclipse Propio*. Dura **2 rondas**.

| Efecto | Valor |
|---|---|
| Daño Luna | ×0.25 |
| Curación | ×0.5 |
| Iluminaciones | No se puede usar la de Luna |
| Podredumbre | ×1.5 |
| Tinta | **Sin cambios.** Es la escuela de Teo y su salvavidas narrativo |
| Ventanas de Réplica | −2 f en todas (oscuridad) |
| **Folio** | Se esconde dentro del libro de Teo: no hay *Anotación* y las intenciones enemigas se ven como "?" |
| *Sacerdote del Eclipse* | Invierte el castigo de la Luna (ver el Árbol del Saber) |

**El Gran Eclipse** (combate final) es una versión permanente y gradual: la luna se cubre fase a fase durante el combate. Sus reglas exactas están en el documento de Las Entrañas.

---

## 10. Inspiración e Iluminaciones

### 10.1 Barra de Inspiración (0–100)
| Fuente | Inspiración |
|---|---|
| Golpe propio | +3 |
| Trazo Firme | +2 adicional |
| Crítico | +5 |
| Golpe a una debilidad | +6 |
| Esquivar / Saltar | +4 / +5 |
| Desviar | +8 |
| Refutar completo | +10 |
| Réplica Perfecta | +25 |
| Ruptura | +15 |
| Recibir daño | +4 |
| Creciente | +5 por turno de Teo |
| Habilidades de Brasa con *Fragua Interior* | +3 |

### 10.2 Iluminación
- Cuesta **100 de Inspiración**, ocupa el turno de Teo, **no cuesta PA** y tiene Peso 1.5.
- La pantalla se convierte en una **página de manuscrito iluminado** (orlas, pan de oro, capitular gigante).
- **Caligrafía**: el jugador traza 3 trazos rápidos con el stick, el mouse o el dedo, siguiendo una guía. La precisión da de **+0 a +30 % de daño**. Se puede activar el trazado automático (+15 % fijo).

| Iluminación | Escuela | Efecto |
|---|---|---|
| **Érase una Vez** | Tinta | Teo escribe una palabra en el aire y sus letras se vuelven una tormenta de proyectiles. Tinta 450 a todos, *Mancha de Tinta* garantizada y −30 de Postura a todos |
| **Ámbar Eterno** | Savia | Encierra a todo el campo enemigo en ámbar durante 1 turno; al romperse hace Savia 380 + 30 % del daño recibido mientras estaban encerrados |
| **El Último Ocaso** | Brasa | Un sol en miniatura cae sobre el centro del campo: Brasa 520 al objetivo y 300 al resto, 3 pilas de *Ascua* |
| **El Códice Abierto** | Glifo | Raspa y reescribe el combate: elimina todos los efectos positivos enemigos y roba una habilidad de cada enemigo durante 3 turnos (sin costo de Memoria) |
| **La Noche de las Mil Semillas** | Guardia | Brota un ejército de Semillados espectrales: Físico/Savia 60 × 12 golpes repartidos, *Amparo* del 25 % a todo el grupo y *Provocación* durante 2 turnos |
| **Marea de Plata** | Luna | Una luna gigante baja del cielo: Luna 480 a todos, revive a los aliados caídos al 50 % y fija la fase en Llena durante 3 rondas |
| **Florecimiento** | Podredumbre | La pantalla se llena de ceniza y moscas: Podredumbre 400, 5 pilas de *Pudrición* a todos y robo de vida del 30 %. **+10 de Corrupción** cada vez que se usa |
| **Iluminaciones a Dúo** | Teo + Semillado con Lealtad 5 | Una por cada línea de Semillado (ver `Semillados.md`) |
| **Plenilunio** (y **La Que Vela**, de Lys) | Teo + Lys | Solo en el combate final (ver Las Entrañas) |

---

## 11. Tipos de daño y familias de enemigos

### 11.1 Multiplicadores
| Símbolo | Significado | Multiplicador |
|---|---|---|
| **D** | Débil | ×1.75 |
| **–** | Normal | ×1.0 |
| **R** | Resiste | ×0.5 |
| **I** | Inmune | ×0 |
| **A** | Absorbe | Lo cura en 50 % del daño |

### 11.2 Tabla de afinidades
| Familia | Dónde aparece | Físico | Tinta | Brasa | Savia | Luna | Podredumbre |
|---|---|---|---|---|---|---|---|
| **Bestias del Exterior** | Mar de Sal, Selva Murmurante | – | – | D | R | – | – |
| **Comensales** | El Banquete Hueco | – | – | D | **A** (se lo comen) | – | R |
| **Febriles** | El Mediodía Eterno | R (metal) | – | **A** | D (la resina enfría y sella) | D (frescor lunar) | – |
| **Borrones** | El Palimpsesto | R (no tienen cuerpo fijo) | **D** (se les reescribe) | – | – | – | I |
| **Pútridos** | El Frente Eterno, Las Entrañas | – | – | D | R | D | **A** |
| **Semillados Corrompidos** | Todos los Pliegues | – | – | D | R | D | R |
| **Coristas** | La Luna Falsa | – | **D** (lo escrito contra lo cantado) | – | – | R (A durante Llena Falsa) | R |
| **Constructos** | Varios (armaduras, autómatas) | R | – | – | D (las raíces rompen la piedra) | – | I |
| **Ecos y Espectros** | Varios, sobre todo de noche | I | – | – | – | D | – |
| **Señores** | Jefes | Ver el documento de cada Pliegue | | | | | |

**Regla de diseño:** cada Pliegue tiene **al menos una familia débil a la escuela que ese mismo Pliegue regala** y **al menos una familia débil a una escuela de otro Pliegue**. Eso premia volver con habilidades nuevas.

---

## 12. Fórmula de daño

### 12.1 Estadísticas de combate
```
ATQ (físico)   = ATQ de la Pluma + Destreza × 2
POD (mágico)   = POD de la Pluma + POD del Tomo + Intelecto × 2
DEF            = DEF del Atuendo + Vigor + Nivel
RES            = RES del Atuendo + Voluntad + Nivel
Crítico (%)    = 5 + Destreza × 0.15 + bonos           (tope 40 %)
Daño crítico   = ×1.5 + bonos                           (tope ×2.5)
```

### 12.2 Cálculo
```
Bruto     = Potencia × Ataque / 50
            (Ataque = ATQ para habilidades físicas, POD para mágicas;
             las híbridas usan el promedio)
Mitigación = 100 / (100 + Defensa)
            (Defensa = DEF contra físicas, RES contra mágicas)
Daño final = Bruto × Mitigación
             × Afinidad          (D 1.75 · – 1 · R 0.5 · I 0 · A −0.5)
             × Crítico           (1 o multiplicador de crítico)
             × Fase lunar        (solo para Luna y Tinta, ver §9)
             × Ruptura           (1.5 si el objetivo está en Ruptura)
             × Trazo Firme       (1.2)
             × Bonos y penalizaciones (sumados entre sí, tope +200 %)
             × Varianza          (aleatorio de 0.95 a 1.05)
Redondeo hacia abajo. Mínimo 1.
```
Las **curaciones** usan `Potencia × POD / 50 × (1 + Fe Lunar × 0.008)`, sin mitigación.

### 12.3 Ejemplos
| Situación | Datos | Resultado |
|---|---|---|
| Nivel 1, Gota de Tinta contra un Comensal | Potencia 80, POD 34 (10 + 12×2), RES del enemigo 20 | Bruto 54.4 × 0.833 = **45** |
| Nivel 25, Chispa contra un Comensal | Potencia 70, POD 118, RES 70, débil | 165.2 × 0.588 × 1.75 = **170** |
| Nivel 45, Mediodía contra la Marea Pútrida en Ruptura | Potencia 260, POD 230, RES 150, débil, en Ruptura | 1196 × 0.4 × 1.75 × 1.5 = **1256** |

### 12.4 Referencias de vida
| Nivel | Teo (Vigor promedio) | Enemigo común | Élite | Señor (total de todas sus fases) |
|---|---|---|---|---|
| 1 | 145 | 60–90 | — | — |
| 10 | 360 | 220 | 600 | — |
| 20 | 560 | 480 | 1300 | 9000 (1.er Señor) |
| 30 | 780 | 750 | 2100 | 16 000 |
| 40 | 980 | 1050 | 3000 | 26 000 |
| 45 | 1080 | 1200 | 3500 | Hereje + Sapros: 60 000 |
| 60 (después del final) | 1480 | 1800 | 5200 | Refrescos de jefe: 90 000 |

---

## 13. Estados alterados

### 13.1 Negativos
| Estado | Icono | Efecto | Duración | Cómo se quita |
|---|---|---|---|---|
| **Mancha de Tinta** | Gota negra | Precisión −25 % | 2 turnos | Se cura sola, con *Fe de Erratas* o con un tónico |
| **Ascua** | Brasa | 4 % de vida máxima por turno y por pila (hasta 5 pilas) | 3 turnos (renovable) | Agua bendita, Savia o *Lluvia de Otoño* |
| **Ambarizado** | Gota dorada | Pierde su turno; recibe −30 % de daño; se rompe tras 2 golpes o 1 turno. Después, 2 turnos de inmunidad | 1 turno | Golpes |
| **Pudrición** | Gusano | 3 % de vida máxima por turno y por pila (hasta 8); −10 % de curación recibida por pila. **No expira sola** | Permanente | *Purificar*, *Lluvia de Otoño*, Agua de Luna |
| **Fiebre** | Termómetro de bronce | VEL +20 %, DEF −25 %. Al terminar: 1 turno de *Aturdido* | 3 turnos | Tónico frío o Savia |
| **Aturdido** | Estrellas | Pierde 1 turno | 1 turno | — |
| **Olvido** | Página en blanco | Sella 1 habilidad al azar del grimorio (o del repertorio enemigo) | 3 turnos | *Corrección*, *Luz que Recuerda* |
| **Errata** | Signo de intercalación | Su siguiente turno se retrasa +30 % | 1 uso | — |
| **Hambre** | Plato vacío | No puede usar objetos; pierde 1 PA (o 1 de Carga) por turno | 3 turnos | Comida de Berta (no la de los Comensales) |
| **Devoción** | Polilla | Controlado: ataca a sus aliados con su ataque básico | 1–2 turnos | Daño Tinta o *Despertar* de Folio |
| **Enraizado** | Raíz | No puede esquivar (solo Desviar, Refutar o Saltar); VEL −20 % | 2 turnos | Brasa o *Martillo de Glifo* |
| **Deslumbrado** | Destello | Enemigo: precisión −30 %. Aliado: los glifos aparecen 10 f más tarde | 2 turnos | — |
| **Silencio de Tinta** | Pluma rota | No puede usar habilidades mágicas | 2 turnos | *Fe de Erratas* |
| **Moscas** | Enjambre | Cada vez que actúa, 10 % de pasar 1 pila de Pudrición a un aliado contiguo | 3 turnos | Brasa |
| **Subrayado** | Raya roja | El siguiente golpe recibido es crítico y hace +20 de Postura | 1 golpe | — |
| **Desorientado** | Laberinto | Elige su objetivo al azar | 2 turnos | Recibir daño (50 %) |
| **Carne Terca** | Corazón cosido | No puede morir, pero tampoco curarse; si al terminar tiene 0 de vida, cae | 3 turnos | — (exclusivo del Frente Eterno) |
| **Vacilación** | Pluma temblorosa | −1 PA inmediato | Instantáneo | — |
| **Marchito** | Hoja seca | Un Semillado fuera de combate | Hasta revivirlo | *Resurrección Plateada*, objetos o atril |
| **Agotado** | Tintero vacío | Teo no gana PA en su siguiente turno | 1 turno | — (efecto de algunas habilidades de Podredumbre) |

### 13.2 Positivos
| Estado | Efecto | Duración |
|---|---|---|
| **Amparo** | Escudo que absorbe daño (valor indicado por la habilidad) | Hasta romperse o 3 turnos |
| **Nota al Margen** | La siguiente habilidad se repite gratis al 50 % | 1 uso |
| **Vigilia** | Sobrevive a un golpe mortal con 1 de vida | 1 uso o 3 turnos |
| **Inspirado** | +25 % de Inspiración ganada | 3 turnos |
| **Savia Viva** | Cura 5 % de vida máxima por turno | 3 turnos |
| **Marea Alta** | +1 PA por turno | 3 turnos |
| **Glosado** | La siguiente habilidad aplica también una Glosa que no tienes equipada | 1 uso |
| **Calor** (pilas) | Exclusivo de *Forjador*: con 5 pilas, la siguiente habilidad cuesta 0 PA | Hasta usarse |
| **Provocación** | Atrae los ataques enemigos | 2 turnos |

**Resistencia a estados:** `probabilidad final = probabilidad base × (1 − Voluntad × 0.004)`, con un mínimo del 10 %. Los Señores tienen resistencias fijas por estado (indicadas en su ficha).

---

## 14. Calificación (la nota del combate)

Al ganar aparece una **hoja de examen** con anotaciones en tinta roja y una nota final con sello.

### 14.1 Puntaje (0–100)
| Criterio | Puntos | Cálculo |
|---|---|---|
| **Réplica** | 40 | `40 × (suma de valores / golpes recibidos)`. Valores: Desviar, Refutar o Saltar = 1.0 · Esquivar = 0.6 · Desvío tardío = 0.4 · fallo = 0. Si el combate termina antes de que el enemigo actúe: 40 |
| **Integridad** | 20 | `20 × (1 − daño recibido / vida máxima total del grupo)`, mínimo 0 |
| **Ritmo** | 15 | Cada encuentro tiene un "par" de turnos (por diseño). ≤ par: 15; −3 por cada turno extra |
| **Erudición** | 10 | Al menos 2 golpes a debilidades: 5 · Al menos una Ruptura: 5 |
| **Estilo** | 10 | Remate Ilustrado 5 · Iluminación 3 · Réplica Perfecta 2 (tope 10) |
| **Sin objetos** | 5 | No se usó ningún objeto |
| Penalizaciones | — | Teo cayó y fue revivido: −15 · cada Semillado Marchito: −5 |

### 14.2 Notas y recompensas
| Nota | Puntaje | XP y Orvales | Ecos | Tiradas de botín | Extra |
|---|---|---|---|---|---|
| **Suspenso** | < 35 | ×0.8 | +0 | 1 | Folio hace un comentario mordaz |
| **Aprobado** | 35–59 | ×1.0 | +0 | 1 | — |
| **Notable** | 60–74 | ×1.15 | +1 | 1 (mejor tabla) | — |
| **Sobresaliente** | 75–89 | ×1.3 | +1 | 2 | — |
| **Matrícula de Honor** | ≥ 90 **y** sin caídas | ×1.5 | +2 | 2 + un objeto **Raro o mejor garantizado** | La primera vez contra cada Señor y contra el Hereje: +1 Lágrima de Luna y un **Sello de Honor** cosmético |

- **Racha de Honor**: 5 Matrículas seguidas dan +10 % de XP hasta romper la racha (indicador junto al minimapa).
- Las tablas de botín por nota están en `Economia_Recompensas_y_Aldea.md`.

---

## 15. Derrota: Tu Borrador

1. Si Teo cae (y no tiene Vigilia), entra en **Desvanecido** con una cuenta de **2 turnos**. Sus Semillados pueden revivirlo con habilidades u objetos. Si nadie lo hace, se pierde el combate.
2. Teo despierta en el **último atril** donde descansó, con el grupo curado.
3. Pierde el **30 % de los Orvales que llevaba** (los guardados en la Tesorería del Granero están a salvo). Las Lágrimas de Luna, los Ecos y los objetos no se pierden.
4. En el lugar de la derrota aparece **Tu Borrador**: una versión a medio dibujar de Teo, con líneas de boceto, colores sin rellenar y frases tachadas. Si fue un jefe, el Borrador espera en la puerta de su sala.
5. **El duelo contra el Borrador:**
   - Usa el grimorio equipado de Teo con el 70 % de sus estadísticas.
   - Repite la habilidad que más usó el jugador en los últimos 5 combates. Te obliga a enfrentarte a tus propias costumbres.
   - Al ganarle se recuperan los Orvales **más un 10 % de "intereses"**.
6. Si Teo vuelve a caer antes de recuperar sus Orvales, el Borrador anterior desaparece con lo que tenía y lo reemplaza uno nuevo.
7. En dificultad *Cuento* no se pierden Orvales (el Borrador aparece igual, con un regalo menor).
8. *Contra el Borrador* (Raíces) debilita al Borrador un 20 %.

---

## 16. Folio en combate

Folio no puede ser atacado (revolotea detrás de Teo). Sus acciones:

| Acción | Costo | Efecto | Se desbloquea |
|---|---|---|---|
| **Anotación** (pasiva) | — | Muestra el icono de intención del siguiente enemigo. Con Visión de Tinta: muestra la secuencia completa de glifos de su siguiente acción | Acto I / Índigo |
| **Consejo** | Gratis, sin turno | Una pista contextual ("¿Ya probaste quemarle la servilleta?") | Acto I |
| **Marcar** | 1 PA, espera 3 turnos | Aplica *Subrayado* a un enemigo | Acto I |
| **Despertar** | 1 PA, una vez por combate | Quita *Devoción*, *Ambarizado* o *Aturdido* a un aliado | Tras el 1.er Señor |
| **Pase de Página** | Una vez por combate de jefe | Reinicia el anillo de un glifo a mitad de un combo. Rescata una Réplica Perfecta | Tras el 3.er Señor |

Durante un **Eclipse**, Folio se esconde dentro del libro: no hay Anotación ni Despertar. Diálogo típico: *"No-no-no, eso no, no me gusta cuando se come la luna."* Es una pista de su origen (ver Misterios).

---

## 17. Leer y Transcripción en combate (resumen)

- **Leer** (siempre disponible): vida exacta, afinidades, siguiente intención y 1 rasgo oculto. Primera vez por tipo de enemigo: +1 entrada del Bestiario.
- **Con Visión de Tinta** (tras liberar el Índigo): Leer también revela los golpes ocultos y hace avanzar la **Transcripción** de una habilidad marcada como transcribible:
  - Leer: +25 %.
  - *Lectura Profunda*: +50 %.
  - Refutar esa habilidad: +34 %.
  - Desviar esa habilidad: +20 %.
  - Al llegar al 100 %, la habilidad pasa al grimorio como **Borrador de Transcripción**, que se puede pasar en limpio en la Biblioteca.
- Detalles y lista de habilidades transcribibles: `Progresion_y_Arbol_del_Saber.md` §8.

---

## 18. Jefes: reglas generales

1. **Fases**: cada Señor tiene 2 o 3 fases. Al cambiar de fase, **el escenario se transforma** (es la regla visual principal del juego).
2. **Barreras de fase**: el daño que sobra no pasa de una fase a otra.
3. **Patrones de intención**: los Señores muestran su intención con **2 turnos de anticipación** (en vez de 1) para permitir planear.
4. **Eco de Poder**: por cada Señor ya vencido, los que quedan ganan:
   - +4 niveles, +8 % de vida y +5 % de daño.
   - **Un movimiento "eco" del Señor caído** adaptado a su estilo (por ejemplo, tras vencer a la Anfitriona, el Sol Cautivo aprende *Bocado de Escoria*, una variante con glifo ▲ de la mordida del banquete).
   - El último Señor tiene 4 movimientos eco y una fase de 30 % de vida extra.
5. **Partes**: algunos jefes tienen partes destructibles con su propia Postura. Romperlas quita ataques y da materiales.
6. **Sin huida y sin victoria automática.**
7. **Recompensas fijas**: ver `Economia_Recompensas_y_Aldea.md` §5.

---

## 19. Inteligencia de los enemigos

| Rango | Comportamiento |
|---|---|
| Común | Patrón fijo de 2 o 3 acciones en ciclo. Si un aliado suyo cae, a veces entra en *Furia* (+20 % de daño) |
| Élite | Prioriza objetivos (el más herido, el que tiene más Inspiración o el que sana). Usa fintas |
| Mini-jefe | Guion por porcentaje de vida y reacciones: si es Leído, cambia su siguiente glifo por uno oculto ("no me gusta que me lean") |
| Señor | Guion por fases + respuestas a lo que hace el jugador: si el jugador hace muchas Réplicas Perfectas, el Señor añade fintas; si el jugador abusa de un elemento, el Señor gana resistencia temporal a ese elemento (−25 % durante 3 turnos, avisado en pantalla) |

---

## 20. Ejemplos de turnos narrados

### Ejemplo A — Acto I, el Mar de Sal (enseñando la Réplica)
*Teo (nivel 3) y **Zahra** (aliada invitada) contra dos Escorpiones de Cristal. Teo dio el Golpe de Iniciativa. (Todavía no hay Semillados ni Folio: el Semillado inicial se elige en la Antesala y Folio nace al llegar al árbol.)*

1. **Turno de Teo** (3 PA). La tira muestra: Teo → Zahra → Escorpión A → Escorpión B. Teo usa **Leer** sobre el Escorpión A: aprende que es débil a Brasa (no tiene Brasa) y que su siguiente acción es *Doble Pinza* (◆◆). +1 PA → 4 PA.
2. **Turno de Zahra**: *Tajo de Sable* al Escorpión A (Físico; el cristal resiste). Zahra: *"Duro como mi suegra. Haz tu magia, niño."*
3. **Escorpión A**: *Doble Pinza* contra Teo. Primer ◆: el jugador desvía (−8 Postura, +8 Inspiración). Segundo ◆: también. **¡Réplica Perfecta!** El fondo se vuelve papel, la pluma de Teo hace un trazo en tres tiempos y el escorpión sale volando. −30 de Postura: **Ruptura** (40 − 8 − 8 − 30 < 0).
4. **Escorpión B**: *Coletazo* (▲) contra Zahra. El jugador salta por ella. 0 de daño.
5. **Turno de Teo** (4 + 2 + 2 = 8 PA, tope 6). Remate Ilustrado sobre el Escorpión A, que está roto y con 40 % de vida: viñetas, la pluma "dibuja" el golpe final. Derrotado.
6. Zahra y Teo se encargan del Escorpión B. **Calificación: Matrícula de Honor.** Zahra: *"¿Dónde aprendiste a pelear así?"* — Teo: *"En un libro."* — Zahra: *"Claro."*

### Ejemplo B — Mediados del juego, El Palimpsesto (Transcripción)
*Teo (nivel 26), Pavesa (en su forma Fogata) y Lomito contra un **Raspador** (sirviente de la Correctora; ver bestiario de `mundo/Pliegue_3_Palimpsesto.md`).*

1. Teo usa *Lectura Profunda* (1 PA): revela que *Palimpsesto* (◯◯, 2 letras) es transcribible. Progreso: 50 %.
2. El Raspador lanza *Palimpsesto* contra Lomito. El jugador **refuta** las dos letras (→, ↓): 0 de daño, devuelve el 40 % como Tinta y la Transcripción sube a 84 %.
3. Teo usa *Gota de Tinta* (débil: ×1.75) y luego *Subrayar*. Fogata usa *Chispa* (el Raspador también es débil a Brasa). Lomito usa *Hoja Suelta*.
4. El Raspador repite *Palimpsesto* con un **eco** (glifo fantasma): el jugador refuta el original y el eco. Transcripción: 100 %. **"Has transcrito: Palimpsesto."** El Raspador rompe su Postura por los dos refutes.
5. Remate Ilustrado. En el siguiente atril, Teo puede equipar *Palimpsesto* en su grimorio.

### Ejemplo C — Final del juego, un Señor con Eco de Poder (Réplica avanzada)
*La Voz del Coro, quinta y última, con 4 movimientos eco. Fase 2, Llena Falsa.*

- La intención anunciada es *Himno de los Mil* (◯◯◯ ▲ ◆ ✦), al ritmo de la música.
- El jugador usa **Guardar** antes (+2 f en todas las ventanas).
- Al llegar el golpe: refuta las tres letras en los tiempos fuertes del compás, salta la onda ▲, desvía el ◆ tras una **finta** (la tinta tiembla, pero el sonido de la pluma marca el golpe real) y **esquiva** el ✦ (no se puede desviar).
- Como hubo un esquive, **no hay Réplica Perfecta**, pero los refutes devuelven daño Tinta (los Coristas son débiles a Tinta) y la Postura de la Voz baja 10 + 8 = 18.
- En el siguiente turno, Teo usa *Cambio de Fase* (×2) para saltarse la Llena Falsa: Menguante, críticos +10 % y daño a la Postura +20 %. Abre camino a la Ruptura.

---

## 21. Parámetros que se deben vigilar en pruebas de juego
- Que la Réplica Perfecta sea alcanzable el 30–40 % de las veces en *Crónica* por un jugador promedio a mitad del juego.
- Que el PA sobrante al final de un combate normal sea de 0 a 2 (señal de que el costo de las habilidades está bien).
- Que la Iluminación aparezca **1 o 2 veces por combate de Señor** y 0 o 1 en combates normales largos.
- Que los combates comunes duren de 60 a 120 s; los de élite, de 2 a 4 min; los de Señor, de 8 a 15 min.
- Que ninguna build supere 1.6 veces el daño medio del resto a igualdad de nivel y equipo.
