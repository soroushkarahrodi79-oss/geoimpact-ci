# Auditoría técnica y de interacción del commit 32f3ab5

## Alcance y método

Se inspeccionaron onboarding, mapas, controles, lista, evidencia, procedencia
y fallos del producto servido localmente. Los siete archivos de interfaz se
compararon por SHA-256 con el commit completo
`32f3ab50bb8a91d21118610bfc135b33e3fb2f3c` antes de abrir Chromium.
Las aserciones y trazas nuevas están en [probe.mjs](evidence/probe.mjs);
los resultados ejecutados, en [technical.json](evidence/technical.json).

Es una revisión de ingeniería separada de las aserciones de aceptación
anteriores, por el mismo asistente que implementó el producto. No se atribuye
independencia humana o institucional inexistente. La evaluación moderada debe
ser conducida por alguien ajeno a la implementación. No se ha observado a
personas, medido comprensión humana ni realizado una evaluación estética con
usuarios. Los supuestos sobre dificultad se identifican como hipótesis.

Chromium 153.0.8010.12, headless, Playwright 1.56.1, Node 24.11.0, Windows.
Se usan tamaños CSS y zoom CSS, no dispositivos físicos ni lector de pantalla.
Las capturas retenidas son originales del navegador con datos sintéticos;
Sierra se comprobó localmente sin conservar su imagen ni geometría en este
paquete. No se visualizó Madrid.

## Observaciones verificadas

### V01 — El panel del recorrido puede ocultar el control que recibe foco

Con el paso 1 abierto, Tab sale de los controles del recorrido y recorre la
aplicación. Algunos controles reciben foco visible por CSS, pero su rectángulo
queda completamente dentro del panel fijo; una comprobación de hit testing
confirma que el panel está encima. Reservar espacio al final de `main` y
desplazar el objetivo resaltado no garantiza que el siguiente foco sea visible.

Reproducción mínima: Chromium 1440×900, bienvenida → Iniciar recorrido o
Ayuda → Iniciar recorrido; desde el título enfocado, pulsar Tab 12 veces. En
la traza registrada `fit-all` recibe foco bajo el panel. No hay que seleccionar
datos ni modificar la página. [Captura](evidence/screenshots/covered-focus-1440.png).
Escape sale del recorrido y devuelve el foco a Ayuda; existe recuperación.

| Viewport | Ocurrencias totalmente cubiertas entre 50 pulsaciones Tab |
|---|---:|
| 1440×900 | 8 |
| 1440×1000 | 0 en esta secuencia |
| 834×1112 | 4 |
| 390×844 | 15 |
| 375×812 | 15 |
| 320×812 | 17 |

Son ocurrencias de una secuencia técnica, algunas repetidas, no controles únicos,
tasas de incidencia ni frecuencia humana. Las trazas incluyen ID, rectángulo,
posición del panel, hit test y estilo de foco. [Tablet](evidence/screenshots/covered-focus-834.png)
y [móvil](evidence/screenshots/covered-focus-390.png). Se evalúa como P1; su
impacto en abandono o errores de personas no se ha medido. La evaluación
preliminar de WCAG y sus límites están en [accesibilidad](ACCESIBILIDAD.md).

### V02 — La práctica exige una visita mediante un control específico

En el paso 4 de la práctica, desplazar el resultado a la vista y marcar la
respuesta correcta no permite avanzar. `actions.result` solo se registra al
activar «Ir al resultado» o el enlace de procedencia definido en ese paso.
El probe conserva el paso 4 tras Comprobar; activar «Ir al resultado» permite
avanzar con la misma respuesta. [Captura](evidence/screenshots/practice-explicit-action-gate.png).

La pista sí indica utilizar ese botón. No se ha demostrado un error del
veredicto ni una conclusión científica incorrecta; es una restricción de
interacción adicional a la lectura visual. La hipótesis H02 es que pueda
producir una sensación de fallo pese a haber realizado la investigación.
La aprobación del paso no constituye una prueba de comprensión.

### V03 — Los filtros pueden ocultar la relación que sigue seleccionada

Seleccionar hotels/hotel_813, conservar la búsqueda y elegir «Sin cambio» deja
0 filas visibles, pero conserva hotel_813 en mapas, resumen de selección y
evidencia. No aparece un aviso específico de «selección fuera de los filtros».
[Captura](evidence/screenshots/selection-outside-filter.png).

Los totales y el reporte no se alteran y el panel identifica hotel_813. Esto
no prueba que el filtro esté mal calculado. H03 pregunta si una persona puede
atribuir por error esa evidencia al conjunto filtrado o confundir cero filas
con cero regresiones. El estudio debe observarlo sin enseñarle la respuesta.

### V04 — Las salvaguardas científicas observadas siguen funcionando

- Selección real de hotel_813: BEFORE `["chamberi"]`, AFTER `["tetuan"]`;
  evidencia existente conservada. El ID y el JSON pointer se muestran como
  texto; la revisión no deriva una nueva asignación.
- Synthetic PASS conserva 2 regresiones con umbral 2. BLOCK conserva 2 con
  umbral 1. La interfaz muestra los valores del reporte; el probe compara
  lo mostrado con la referencia, sin implementar la política.
- Procedencia contiene ocho filas de archivos y cinco versiones; expandir
  configuración conserva su hash y descargar report.json conserva exactamente
  su SHA-256 retenido. Las limitaciones se mantienen accesibles.
  [Captura de procedencia](evidence/screenshots/provenance-desktop.png).
- El ERROR de análisis distribuido oculta la vista científica y elimina el
  veredicto y puntos anteriores. Ayuda y glosario funcionan; iniciar una
  práctica/recorrido queda deshabilitado.
- Una respuesta 404 y un cambio de bytes interceptados solo en el navegador
  producen MISSING/HASH_MISMATCH; no se abre bienvenida ni se mantiene una
  vista científica válida. [ERROR de análisis](evidence/screenshots/analysis-error.png)
  y [ERROR de integridad](evidence/screenshots/integrity-error-mobile.png).
- Sierra local mantiene 52 puntos y cero regresiones al filtrar; seleccionar
  una relación no inventa un evidence_id. No se ha vuelto a auditar el régimen
  jurídico de las fuentes ni se autoriza redistribución de su geometría.
- Los 27 archivos servidos retenidos en el inventario coinciden con sus
  manifiestos antes/después. Cero solicitudes externas, excepciones no
  capturadas o errores ordinarios de consola durante la ejecución final.
  Los fallos inyectados son explícitos, no resultados de análisis nuevos.

La CI científica Linux/Windows del commit está verde en el
[run de referencia](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/39163924184).
Es un antecedente comprobado en GitHub, no una nueva ejecución local de los
113 tests del motor en esta rama documental. No se confunde con usabilidad.

### V05 — Estructura, controles y presentación adaptativa

Se verificaron bucles Tab/Shift+Tab dentro del diálogo nativo, cierre con
Escape y restauración de foco a Ayuda. El recorrido conserva el paso al
cambiar ES/EN en sus ocho pasos. En condiciones normales, flechas desplazan
los mapas con foco, zoom/encuadre funcionan y Tab permite salir. En móvil,
BASE/CANDIDATE cambia el snapshot y expone `aria-pressed`; no elimina el punto.
Las listas ofrecen una alternativa textual a la selección cartográfica.

No se observó desbordamiento horizontal en los seis tamaños ni en la
comprobación de zoom CSS al 200% en escritorio. Esto **no** implica que todo
foco esté visible: V01 es compatible con un scrollWidth correcto. La semántica
de Chromium muestra el diálogo con nombre y botones con nombres de ayuda,
regiones tituladas, formularios etiquetados e imágenes de mapa; no equivale a
una prueba de anuncio/comportamiento en tecnología de apoyo.

La inspección visual de [escritorio](evidence/screenshots/tour-maps-1440.png),
[tablet](evidence/screenshots/tour-maps-834.png) y
[móvil](evidence/screenshots/tour-maps-390.png) confirma que el tamaño pequeño
usa un objetivo real más compacto y que el panel tiene scroll interno. Parte
del mapa puede quedar detrás del panel mientras se lee. La evidencia, hashes
y campos técnicos permanecen detallados, con texto de 9–13 px en varias áreas.
La legibilidad subjetiva y el coste de alternar mapa/panel requieren personas.

## Hipótesis UX: pendientes, no hallazgos humanos

| ID | Hipótesis y riesgo | Evidencia que la motiva | Cómo contrastarla |
|---|---|---|---|
| H01 | Bienvenida + ocho pasos + práctica pueden ser demasiada introducción antes de revisar un dato. | Tres experiencias disponibles en secuencia; no obligación de completarlas. | T1: qué se elige/abandona, tiempo de ayuda y explicación del propósito con palabras propias. |
| H02 | El requisito de pulsar un control específico puede hacer parecer incorrecta una revisión ya realizada. | V02 y feedback genérico. | T2: intentos de Comprobar, si se abre la pista, explicación del bloqueo antes de ayuda del moderador. |
| H03 | Evidencia retenida fuera del filtro puede atribuirse a las filas visibles. | V03. | T3: pedir que describa el conjunto actual y cómo deshace el filtro. |
| H04 | BASE/CANDIDATE y before/after pueden entenderse como desplazamiento físico del punto. | Dos geometrías, mismos puntos; tokens en inglés. | T2/T3: explicación libre del cambio y demostración en ambos snapshots. |
| H05 | PASS/BLOCK o «Bytes verificados» pueden interpretarse como calidad, ausencia de efectos o autenticidad. | Badges prominentes, cautelas presentes. | T3/T4: preguntar qué afirma y qué no afirma cada resultado, sin opciones de respuesta iniciales. |
| H06 | Hashes, JSON pointer y términos técnicos pueden ocultar la ruta a un documento verificable; lectores de pantalla pueden recibir anuncios repetidos. | Panel extenso; dos regiones vivas del tour, sin prueba auditiva. | T4/T5 y una comprobación posterior con lector de pantalla; no asumir repetición por ver dos nodos. |

No se han evaluado comprensión, satisfacción, esfuerzo percibido, aprendizaje
retenido, decisiones reales de planificación, discapacidad o seguridad de
dominio. Ninguna preferencia visual del revisor se convierte en una necesidad
de producto. Las mejoras propuestas y sus condiciones de aceptación están en
[PRIORIDADES](PRIORIDADES.md); no se ha implementado un rediseño.
