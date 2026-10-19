# Hoja de observación, codificación y resultados

**Estado real: estudio no ejecutado.** Ninguna fila de resultado humano está
rellenada. Los códigos R01–R04 del protocolo son plazas previstas, no personas
reclutadas. Los trece bloques de ingeniería pertenecen a otro conjunto de datos.

Copiar [sesión](plantillas/sesion.md), [CSV vacío](plantillas/tareas.csv) y
[resumen vacío](plantillas/resumen.json) a una carpeta privada fuera del
repositorio. No rellenar las copias públicas con notas, consentimientos,
grabaciones ni respuestas. Una plantilla sin nombres sigue necesitando revisión
de anonimización cuando se rellena; las notas reales son seudonimizadas.

## Registrar hechos antes de interpretarlos

Durante la tarea, anotar secuencia concreta, control/caso activo, lo que se ve,
acción, respuesta y ayuda. Separar:

- **HECHO:** acción o estado observado con tiempo relativo y referencia de tarea.
- **RESPUESTA:** palabras reales, reducidas/eliminadas si identifican a la persona.
- **INTERPRETACIÓN DEL OBSERVADOR:** explicación tentativa del problema.
- **HIPÓTESIS:** qué falta contrastar; enlazar H01–H06 cuando corresponda.
- **INCIDENTE TÉCNICO:** carga, viewport, foco, fallo de entorno; no penalizar a
  la persona como si fuese desconocimiento científico.

No atribuir intención a una pausa o un clic. Preguntar «¿Qué esperabas?» cuando
corresponda. No escribir citas de ejemplo como si se hubieran dicho ni rellenar
blancos con respuestas supuestas.

## Códigos separados de ejecución y comprensión

| Campo | Valores y significado |
|---|---|
| `completion` | `COMPLETE_NO_MODERATOR_HELP`, `COMPLETE_MODERATOR_HELP`, `NOT_COMPLETED`, `STOPPED`, `NOT_ATTEMPTED`. La ayuda del producto se registra aparte. |
| `moderator_assistance` | `A0` ninguna; `A1` repetir meta/recordar pensar en voz alta sin pista UI; `A2` orientación de área; `A3` indicar control/acción; `A4` demostración/rescate. Registrar el máximo y la secuencia. A1 no enseña el camino. |
| `product_help` | Ninguna / welcome / tour con pasos vistos / práctica con pasos vistos / pista / glosario / otra. Varias permitidas. |
| `comprehension` | `0` afirmación incorrecta o crítica; `1` parcial con límites omitidos; `2` explicación suficiente con matices y respaldo; `NE` no evaluada. Usar los criterios de cada tarea, sin exigir palabras idénticas. |
| `response_exposure` | Antes de ayuda / después de ayuda del producto / después de ayuda del moderador / sin respuesta. No mezclar al sintetizar. |
| `critical_interpretation` | Código(s) crítico(s), `NONE` o `NE`; conservar el hecho que lo justifica. No marcar NONE si no se preguntó/observó. |
| `ease_optional_1_7` | Pregunta opcional tras la tarea: «¿Qué tan difícil o fácil te resultó?», 1 muy difícil, 7 muy fácil. EN: “How difficult or easy was this task?”, 1 very difficult, 7 very easy. No sustituye éxito o comprensión. |

Un éxito operativo exige los estados observables de la tarea, no solo una
autodeclaración. Un éxito científico exige comprensión 2 sin interpretación
crítica persistente. Informar ambos, no colapsarlos en un único «aprobado».
Si el producto enseña la respuesta y luego se ejecuta correctamente, puede
ser una tarea completada con autoayuda; no es evidencia de comprensión previa.

## Errores críticos: libro de códigos

| Código | Interpretación que debe comprobarse con una pregunta neutral |
|---|---|
| C01 | El punto/hotel se desplazó físicamente porque cambió su asignación. |
| C02 | PASS garantiza cero cambios o corrección/calidad de los datos. |
| C03 | BLOCK demuestra daño real o invalidez del conjunto por sí mismo. |
| C04 | SHA-256/«Bytes verificados» prueba autenticidad, derechos o exactitud del proveedor. |
| C05 | ERROR o cero filas filtradas equivale a cero regresiones o un veredicto científico válido. |
| C06 | Sierra permite deducir operación histórica de equipamientos o ausencia de cambio geométrico por tener cero regresiones. |

Una duda expresada como pregunta no es automáticamente un error crítico.
Registrar si se sostiene tras «¿En qué te basas?», si se autocorrige y cuándo
se corrige. No aplicar puntuaciones retrospectivas sin revisar la evidencia.

## Tiempo y asistencia

Reloj relativo por tarea: inicio al finalizar la lectura de la tarjeta,
fin al declarar terminada o al parar. Registrar `elapsed_s`, `pause_s` y
`load_s` por separado. `load_s` forma parte del transcurrido; no se resta de
forma implícita. Si se deriva un tiempo sin pausas, etiquetarlo y conservar
siempre las medidas originales. Registrar topes excedidos, accesibilidad y
think-aloud como contexto; no tratarlos como diferencias de habilidad.

Anotar también tiempo dedicado a onboarding/ayuda, intentos de Comprobar,
retrocesos, cambios de caso, consultas a evidencia/procedencia, incidentes de
foco y recuperación. Los conteos técnicos de Tab del probe no son métricas
humanas. No iniciar grabación ni cronometraje identificable sin consentimiento.

## Síntesis futura, cuando existan sesiones

Para cada hallazgo: problema, evidencia de tarea/código, casos observados,
condiciones, impacto, relación con los hallazgos técnicos, prioridad y
aceptación. Expresar `n observado / n que intentó la tarea`, con asistencia y
exposición a ayudas. No presentar «n/4» si hubo retirada, omisión o versión
distinta. No convertir denominadores pequeños en porcentajes de población.

Si se usan mediana/rango de tiempos, mostrarlos solo como descripción de esos
intentos, separados por completado/asistido y variante; no pruebas de
significancia, intervalos de confianza ni comparación causal por idioma o
dispositivo. Explicaciones y errores críticos pesan más que un tiempo menor.

Revisar códigos con otra persona cuando sea posible; documentar desacuerdos.
Un único caso grave puede justificar una corrección, pero no prevalencia.
Mostrar también aciertos, casos contradictorios y partes no evaluadas.
Confirmar las interpretaciones críticas en el debrief, corrigiendo límites
científicos después de las tareas para reducir contaminación entre ellas.

No publicar esta síntesis como «validación independiente externa» si el equipo
no lo fue. El repositorio solo recibirá una versión anonimizada y revisada
tras autorización; este trabajo no envía invitaciones ni publica respuestas.
