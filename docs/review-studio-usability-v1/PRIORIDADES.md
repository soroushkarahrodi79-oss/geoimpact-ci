# Prioridades y plan de iteración posterior

Las prioridades son propuestas de revisión, **no cambios implementados**.
Evidencia V = observación de ingeniería; H = hipótesis pendiente de personas.
No se infiere prevalencia humana de un fallo reproducido con automatización.

## P0 — Salvaguarda y parada, sin defecto científico P0 confirmado

| ID | Evidencia actual | Impacto y propuesta | Aceptación medible |
|---|---|---|---|
| P0-01 | V04 verifica bytes e identidad, PASS/BLOCK originales y retirada de vista científica ante ERROR. No se observó el fallo que activa esta prioridad. | Mantener preflight y parada: una versión distinta, Madrid, veredicto/evidencia inválida o falta de consentimiento impide iniciar/continuar esa sesión. No «arreglar» datos ni enseñar a ignorar ERROR. | Antes de cada sesión, 7 archivos UI idénticos al commit, catálogo permitido, consentimiento real, salida ensayada. Si falla una condición: sesión marcada HOLD/no iniciada, sin resultados humanos fabricados. Reanudar solo con entorno verificado y consentimiento vigente. |

No se propone alterar el motor para prevenir un supuesto problema no observado.
La invariancia de v1.2.0/V5 es una condición de todo incremento posterior.

## P1 — Correcciones pequeñas de interacción respaldadas por ingeniería

| ID | Evidencia y certeza | Impacto para la persona | Propuesta acotada | Aceptación medible después de la decisión de cambio |
|---|---|---|---|---|
| P1-01 Foco bajo panel | V01, trazas y capturas: 5/6 secuencias con controles completamente cubiertos; sin medición humana de abandono. | Una persona de teclado puede operar un control que no ve o perder orientación. Tiene recuperación mediante Escape. | Mantener visible el foco real al tabular durante el tour; no basta con desplazar el objetivo resaltado. Conservar el carácter no modal, navegación normal y salida. | Recorrer Tab y Shift+Tab por aplicación y tour en los seis tamaños; cero controles totalmente cubiertos por el panel en las secuencias antes fallidas. Preferir componente/indicador completos visibles. Probar scroll, resize y 200% zoom; sin trampa ni regresión de mapas/selección/idioma. |
| P1-02 Requisito de visita poco explícito | V02 confirma que respuesta correcta + scroll no avanzan; H02 sobre confusión aún no medida. La pista sí menciona el botón. | Puede parecer que una interpretación correcta fue rechazada por razones científicas. | Tras las sesiones, hacer visible qué requisito de interacción falta, en vez de depender solo del feedback genérico. No convertir un clic en prueba de comprensión ni recalcular política. | Si se responde correctamente sin la visita instrumentada, el feedback identifica esa visita pendiente y la acción accesible para realizarla. Después de la visita se avanza conservando la respuesta. ES/EN y teclado; ningún valor/ID/reporte cambia. Separar esta prueba de una respuesta incorrecta. |

P1-01 puede justificar un parche mínimo de accesibilidad con evidencia técnica,
pero este encargo no lo implementa. Durante el estudio actual se registra su
efecto y se ofrece recuperación si es necesaria. Si el modo de acceso de una
persona impide continuar, se pausa esa tarea/sesión; no se la sustituye por
otra persona para mejorar las cifras ni se llama éxito a la demostración.

## P2 — Hipótesis de producto y cobertura pendientes

| ID | Evidencia / hipótesis | Impacto posible | Propuesta posterior al estudio | Aceptación medible |
|---|---|---|---|---|
| P2-01 Alcance de selección y filtro | V03: evidencia permanece con 0 filas; H03: posible atribución al conjunto filtrado. | Confundir la relación activa con el filtro o cero filas con cero regresiones. | Si se observa confusión, indicar explícitamente que la selección está fuera de las filas visibles, con una salida sencilla usando controles existentes. No borrar evidencia a escondidas ni cambiar totales. | Caso hotel_813 + Sin cambio: identidad seleccionada y estado fuera del filtro expresados de forma visible y accesible; limpiar selección/filtros permite recuperar estado coherente. Reporte y política byte-idénticos. Repetir T3 y registrar si vuelve a producirse la atribución errónea. |
| P2-02 Carga de introducción y vocabulario | H01/H04/H06, motivadas por secuencia de bienvenida/tour/práctica, tokens GIS y campos de 9–13 px; no dificultad humana medida. | Lectura larga, abandono de ayudas, confusión entre cambio de geometría y movimiento o entre ID técnico y conclusión. | Elegir solo el problema observado y probar una reducción/clarificación de copia o jerarquía. No añadir otro tutorial, dashboard o función. Conservar cautelas y acceso a evidencia completa. | Mapear cada cambio a una observación real y a una de las siete preguntas de comprensión. Repetir T1–T4 con personas nuevas; informar respuestas, exposición y errores críticos, no solo tiempo. Mantener reflow/zoom, texto accesible y las ocho etapas funcionales. |
| P2-03 Validación con tecnología de apoyo y hardware | Semántica y CSS medidos; interacción real no evaluada. H06 sobre anuncios no confirmada. | Posibles barreras no visibles en capturas o navegación automatizada. | Programar revisión con usuario habitual de lector de pantalla y combinaciones reales; después probar tacto, orientación y teclado virtual sin publicar el visor. | Registrar al menos un recorrido completo real de T1–T5 con combinación documentada de lector/navegador, ajustes, incidencias y recuperación. Para móvil/tablet, registrar hardware real antes de afirmar soporte físico. Sin cubrir esas pruebas, mantenerlas como NO EVALUADAS y no declarar WCAG. |

## Orden de trabajo y decisiones

1. **Ahora:** congelar la referencia, completar operación/consentimiento y
   ensayar moderación. Ejecutar la ronda de cuatro personas con los defectos
   conocidos y reglas de parada. No hacer un rediseño antes de recoger datos.
2. **Tras cada sesión:** depurar notas y revisar privacidad; no modificar UI
   entre participantes silenciosamente. Si aparece P0, detener y registrar
   la ruptura de versión; separar cualquier ronda posterior, sin mezclar cifras.
3. **Tras las cuatro sesiones o las que consientan terminar:** contrastar
   codificación, reunir evidencia que apoya y contradice cada hipótesis,
   distinguir interacción de comprensión y priorizar gravedad/recuperabilidad.
   No eliminar un fallo grave por haber ocurrido una sola vez.
4. **Primera iteración:** parche pequeño de foco y, si procede, claridad del
   requisito de práctica. Máximo un problema de claridad adicional respaldado
   por sesiones; evitar reestructurar el layout entero. Mantener código/UI en
   un PR funcional separado de este paquete de investigación.
5. **Verificación:** repetir los probes pertinentes y los tests de onboarding,
   lector/navegador existentes; comprobar hashes y diff protegido. Después,
   repetir tareas con personas nuevas para no atribuir al parche el aprendizaje
   de las mismas personas. Las mismas personas pueden aportar accesibilidad
   o diagnóstico adicional, etiquetado como seguimiento, no primera visita.
6. **Decisión de ronda:** continuar la investigación si persisten interpretaciones
   críticas o barreras de acceso. Un resultado local favorable con n=4 no
   valida el producto para decisiones reales ni permite levantar R1.

Para el GO del estudio no es preciso declarar el prototipo listo. El valor
de la ronda consiste en observar problemas de un sistema ya funcional. El
riesgo científico se limita con datos sintéticos, moderación, ausencia de
decisiones reales, debrief y parada ante evidencia inválida. **R1 OPEN mantiene
HOLD para Madrid y el visor completo**, con independencia de cualquier mejora UX.
