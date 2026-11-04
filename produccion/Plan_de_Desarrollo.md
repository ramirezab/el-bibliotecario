# PLAN DE DESARROLLO — De la biblia al juego

> Cómo convertir esta biblia en un juego jugable: qué construir primero, en qué orden, con qué herramientas y qué recortar si hace falta. Se apoya en todos los demás documentos; el pipeline técnico de efectos está en `arte/Biblia_de_Efectos_Visuales.md` §16.

---

## 1. EL PRINCIPIO RECTOR
**El juego vive o muere por cómo se siente una pelea.** Si la Réplica no es satisfactoria y los efectos no impresionan, nada más importa. Por eso todo el plan pone el combate primero y el contenido después.

> Regla de producción: **ningún Pliegue entra en producción hasta que una pelea contra un enemigo común sea divertida diez veces seguidas.**

---

## 2. ALCANCE POR NIVELES

Hay tres niveles de alcance. Se construye el primero, se prueba con jugadores y solo después se decide si se sigue.

| Nivel | Qué incluye | Para qué sirve |
|---|---|---|
| **A. Prototipo de combate** | 1 escenario, Teo, 1 Semillado, 4 enemigos, 1 minijefe, la Réplica completa, PA, Postura, 1 Iluminación. Arte provisional + **efectos finales en 3 habilidades**. | Probar que la pelea es divertida y que los efectos son el gancho. |
| **B. Rebanada vertical (demo)** | Prólogo Día 2 (la Guerra del Eclipse, como tutorial épico) + la Antesala + **el Pliegue Ámbar completo** con la Anfitriona + la restauración del Granero. Arte final. | Demo pública (Steam Next Fest), material de tráiler y prueba de todo el ciclo: explorar, pelear, liberar y reconstruir. |
| **C. Juego completo** | Todo lo que describe esta biblia. | Lanzamiento. |

### Contenido estimado del juego completo
| Elemento | Cantidad aproximada | Fuente |
|---|---|---|
| Zonas exploración | ~55 (Merova, viaje, 5 Pliegues × 8, aldea, Entrañas) | `mundo/` |
| Enemigos comunes | ~60 (incluidas variantes) | Bestiarios de cada Pliegue |
| Minijefes | 12–14 | Pliegues y Acto I |
| Jefes | 5 Señores + Brote Podrido + Heraldo del Gusano + combate final de 4 fases + jefes de los recuerdos | `mundo/`, `guion/` |
| Semillados | 30 líneas, con varias formas cada una | `sistemas/Semillados.md` |
| Nodos del Árbol del Saber | 180 | `sistemas/Progresion_y_Arbol_del_Saber.md` |
| Habilidades con efectos únicos | ~90 activas (las pasivas no necesitan efecto) | Árbol del Saber + Transcripciones |
| Iluminaciones | 7 (cinematografías completas) | `arte/Biblia_de_Efectos_Visuales.md` |
| Palabras de diálogo | ~120 000–150 000 | `guion/` + Pliegues |
| NPCs con retrato | ~35 | `historia/` |
| Páginas Perdidas | 150 | Pliegues |

---

## 3. HERRAMIENTAS RECOMENDADAS

| Área | Herramienta | Por qué |
|---|---|---|
| Motor | **Godot 4.x** | Luces 2D con mapas de normales, partículas por GPU, shaders de CanvasItem, licencia libre, ligero para móvil. *(Alternativa: Unity URP 2D si el equipo ya lo domina.)* |
| Pixel art y animación | **Aseprite** | Estándar del pixel art; exporta hojas de sprites y capas. |
| Retratos e ilustraciones | Krita / Photoshop / Clip Studio | Para las fichas estilo Nigromante y las viñetas de los Remates. |
| Efectos de fluidos | Simulador de fluidos (EmberGen o similar) → pixelizar | Ver pipeline de pixelización de la biblia de efectos. |
| Diálogo | **Dialogic 2** (plugin de Godot) o **Yarn Spinner** | Ramas, variables (`corrupcion`, `relacion_lys`...) y localización. |
| Datos de juego | Recursos de Godot (`.tres`) o tablas CSV/JSON | Enemigos, habilidades, objetos y nodos del árbol como datos, no como código. |
| Música | DAW a elección; música adaptativa por capas | El tema de cinco notas debe poder superponerse en cualquier pista. |
| Control de versiones | Git + Git LFS | Para arte y audio pesados. |
| Gestión | Tablero tipo Kanban (Trello, Notion o GitHub Projects) | Una tarjeta por enemigo, habilidad y escena. |

---

## 4. ARQUITECTURA DEL CÓDIGO (módulos)

```
nucleo/
  estado_juego        variables narrativas y de progreso (ver historia/Trama_del_Juego.md §8)
  guardado            atriles, perfiles, autoguardado
  eventos             bus de eventos (señor_vencido, carta_recibida, eclipse_inicio...)
combate/
  motor_turnos        línea de iniciativa, PA, comandos
  replica             ventanas de timing, glifos, Réplica Perfecta, accesibilidad
  postura             Postura, Ruptura, Remate Ilustrado
  fases_lunares       rotación de fases y Eclipse
  habilidades         definición por datos: costo, objetivo, daño, efectos, VFX asociados
  ia_enemiga          patrones por enemigo, fintas, cambios de fase de jefes
  calificacion        cálculo de nota y botín
  director_camara     zooms, paneos, cortes, viñetas
  director_vfx        dispara efectos por eventos del combate (impacto, crítico, desvío...)
exploracion/
  mundo               zonas, transiciones, Mundo Velado (capa del Paso Lunar)
  habilidades_mapa    Viento de Molino, Martillo, Visión de Tinta, Brote, Paso Lunar, Escritura
  interacciones       leer, leer al tacto, atriles, cofres
progresion/
  arbol_saber         nodos, dependencias, reinicio
  grimorio            espacios de Memoria, equipables
  equipo              rarezas, afijos, runas, reliquias
  semillados          vivero, evolución por barrio, lealtad
aldea/
  barrios             estados de restauración
  edificios           niveles, costos, producción
  npcs                rutinas, diálogos por evento
narrativa/
  dialogos            integración con Dialogic/Yarn
  codice              El Cuento (dos versiones por entrada)
  cartas              Cartas del Hereje y respuestas
  suenos              Sueños de Plata
```

**Regla técnica clave:** el combate tiene que poder correr sin gráficos (modo "simulación") para equilibrar números con miles de combates automáticos. Los efectos visuales se enganchan por eventos, nunca están mezclados con la lógica.

---

## 5. HITOS

Estimación para un **equipo pequeño** (4–6 personas: 1–2 programación, 2 arte de pixel/animación, 1 efectos visuales, 1 diseño y narrativa, más música y sonido externos). Para **un solo desarrollador** con arte contratado, multiplicar los tiempos por 2,5–3.

| Hito | Duración | Entregable | Criterio para pasar |
|---|---|---|---|
| **H0. Preproducción** | 1–2 meses | Documento técnico, guía de estilo validada con 3 personajes y 1 escenario final, lista de módulos. | El arte de prueba se ve como las referencias, pero propio. |
| **H1. Prototipo de combate** | 2–3 meses | Nivel A. | 10 testers juegan 20 minutos y piden más. La Réplica Perfecta provoca reacción en voz alta. |
| **H2. Prototipo de exploración** | 1–2 meses (en paralelo con H1) | 1 zona del Banquete Hueco en gris, con 2 habilidades de mapa y bloqueos. | Moverse se siente bien; los secretos se encuentran. |
| **H3. Rebanada vertical** | 4–6 meses | Nivel B completo con arte, sonido y efectos finales. | Demo pública. Métricas: tiempo de juego, abandono, nota media de la Réplica. |
| **H4. Producción de Pliegues** | 12–18 meses | Pliegues 2–5, uno cada 3–4 meses, con equipos solapados. | Cada Pliegue pasa una prueba de juego antes de empezar el siguiente. |
| **H5. Acto III y finales** | 3–4 meses | Las Entrañas, combate final y los tres finales. | El combate final se prueba más que cualquier otra cosa. |
| **H6. Pulido y equilibrio** | 3–4 meses | Equilibrio con simulaciones, accesibilidad, rendimiento, localización. | Sin errores bloqueantes. 60 fps en el hardware objetivo. |
| **H7. Lanzamiento** | — | PC (Steam) primero; consolas después. Móvil como adaptación posterior. | — |

**Total estimado:** 2,5–3,5 años con equipo pequeño.

---

## 6. ORDEN DE PRODUCCIÓN DE LOS EFECTOS
Los efectos son la prioridad del juego y el mayor riesgo de costo. Orden recomendado:

1. **El vocabulario base** (sirve para todo): impacto de grabado, hit-stop, sacudida de pantalla por niveles, números de daño caligráficos, chispa de Desvío y estallido de Réplica Perfecta.
2. **La escuela de Tinta completa**: es la de Teo y la que más se ve.
3. **Una Iluminación de punta a punta** (la de Tinta o la de Savia) como pieza de tráiler.
4. **Los efectos de la Anfitriona**: el primer jefe de la demo.
5. Después, una escuela por Pliegue, junto con su Pliegue.
6. Al final, Las Entrañas: el Eclipse en tiempo real, el Vaso y Sapros.

> Cada efecto pasa el **checklist de aprobación** de la biblia de efectos antes de darse por terminado.

---

## 7. RIESGOS Y CÓMO REDUCIRLOS

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| **El alcance es demasiado grande** | Alta | Crítico | Niveles A → B → C con decisión en cada paso. Lista de recortes preparada (§8). |
| **La Réplica se siente injusta** | Media | Crítico | Ventanas configurables por dificultad, sonido de anticipación siempre presente, opción de asistencia y pruebas tempranas con jugadores de distintos niveles. |
| **Los efectos ahogan la legibilidad** | Media | Alto | Regla de la biblia de efectos: el Glifo de Intención **siempre** se lee por encima de cualquier efecto. Modo de efectos reducidos. |
| **Rendimiento en móvil** | Alta | Medio | Móvil es una adaptación posterior; escalado de efectos por niveles desde el inicio (biblia §16.9). |
| **Demasiado texto** | Media | Medio | Todo diálogo largo tiene versión corta; los Sueños y las Cartas son opcionales. Edición de guion en H4. |
| **Inconsistencias de lore** | Media | Bajo | `01_CANON.md` como fuente de verdad; revisión de nombres antes de cada hito. |
| **Equilibrio del Árbol del Saber** | Alta | Medio | Simulación de combates sin gráficos; builds de ejemplo como casos de prueba. |
| **Que el juego se compare con otros del género** | Media | Medio | Identidad propia: la tinta que se vuelve luz, el bibliotecario, los Pliegues como miedos, la Réplica como "contestar un argumento". |

---

## 8. LISTA DE RECORTES (de menos a más doloroso)

Si el tiempo o el dinero no alcanzan, se recorta en este orden **sin romper la historia**:

1. Contenido de fin de juego (arena, revanchas, desafíos).
2. Semillados: de 30 líneas a 15; las formas por barrio, de 5 a 3.
3. Páginas Perdidas: de 150 a 80.
4. Misiones largas: conservar Ilse Varga, Pío, los Recuerdos del Rey y el Mar para Lys; recortar el resto.
5. Zonas: cada Pliegue, de 8 zonas a 6.
6. Final malo: se conserva como escena corta sin combate distinto.
7. Fases del combate final: la fase 4 (Escritura Verdadera) se vuelve cinemática interactiva en vez de combate.

**Lo que nunca se recorta:** la Réplica, los efectos de los cinco Señores y del combate final, los cuatro recuerdos del prólogo, los Sueños de Plata principales y la revelación del rey.

---

## 9. LOCALIZACIÓN
- **Idioma original: español latinoamericano.** Toda la biblia está escrita así.
- Inglés como segundo idioma desde el lanzamiento (título: *The Librarian*).
- Cuidado especial con: juegos de palabras de Folio (requieren adaptación, no traducción), canciones (traducir con métrica), el Glifo Lunar (es un alfabeto inventado; no se traduce, se subtitula) y los nombres propios (no se traducen, salvo títulos como "La Anfitriona" → *The Hostess*).
- Todo el texto vive en tablas de localización desde el primer día; nunca dentro del código.

---

## 10. AUDIO (resumen)
- **Tema principal**: la Canción de Cuna de Ebrón (cinco notas), arreglada de forma distinta en cada lugar: laúd en Merova, voz sola en el Mar de Sal, coro en el árbol, metales en la Forja, música de caja en la Biblioteca, tambores en el Bastión, coro femenino en el Templo y la versión invertida (desafinada) para Sapros.
- **Música adaptativa en combate**: capas que entran con la Inspiración; la Réplica Perfecta silencia la música un instante (ver biblia de efectos, sincronía con audio).
- **Sonido de la Réplica**: cada tipo de defensa tiene un sonido único e inconfundible: Esquivar suena a papel, Desviar a pluma que rasga, Refutar a campanilla y Saltar a página que pasa. El sonido de anticipación de cada ataque enemigo es **obligatorio** (accesibilidad).
- **Voces**: actuación de voz parcial (gritos de combate y frases clave de cinemáticas) más texto. Folio con voz completa si el presupuesto lo permite: es el personaje que más vende.

---

## 11. MARKETING (ganchos)
- **Frase de venta:** *"Un cuento para niños que resultó ser verdad."*
- **Gancho visual:** la Réplica Perfecta: la pantalla se vuelve papel y el contraataque se pinta en tres trazos.
- **Gancho emocional:** el mendigo que era rey.
- **Tráiler de anuncio** (60 s): ver los 10 momentos de `historia/Trama_del_Juego.md` §9.
- **Demo**: la rebanada vertical (Guerra del Eclipse + Antesala + Banquete Hueco).
- **Comunidad**: los misterios en capas (`lore/Misterios_y_Secretos.md`) están pensados para que los jugadores los discutan. No revelar los secretos de nivel Obsesivo en ningún material oficial.

---

## 12. PRÓXIMOS PASOS CONCRETOS
1. Validar con el autor las **decisiones abiertas** de `00_INDICE.md` (plataforma, modelo de negocio, Semillados).
2. Encargar la **guía de estilo**: Teo, Folio y la Anfitriona en pixel art + 1 escenario del Banquete Hueco + la ficha ilustrada de Teo al estilo de la referencia.
3. Montar el **prototipo de combate** (Nivel A) en Godot 4 con datos de `sistemas/Combate_y_Replica.md`.
4. Producir los **tres primeros efectos finales** (Desvío, Réplica Perfecta y una habilidad de Tinta) para validar que el gancho visual funciona.
5. Primera prueba con jugadores.
