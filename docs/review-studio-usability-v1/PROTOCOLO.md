# Estudio moderado: guion exclusivo del equipo de investigación

Estado: **PREPARADO, NO EJECUTADO**. Se planifican cuatro personas; no hay
reclutamiento, citas, respuestas ni tiempos humanos registrados. No compartir
este documento con participantes: contiene las respuestas de referencia.

## Preguntas y diseño

Determinar si una primera visita permite comprender el propósito, vincular
mapa y relación, explicar una asignación, interpretar la política, rastrear
evidencia y reconocer conclusiones no respaldadas. Interesa el razonamiento
y la posibilidad de recuperar errores, no solo llegar al último botón.

Estudio cualitativo moderado con think-aloud opcional, cinco tareas en orden
T1–T5. Se mantiene el orden porque se investiga aprendizaje progresivo; no se
interpreta como comparación causal entre ayudas. No obligar a usar onboarding,
no enseñar dónde están los controles antes de las tareas y registrar cada
ayuda vista. Una respuesta copiada del tour no prueba comprensión transferible.
T3 utiliza otro ID para observar transferencia después de hotel_813.

La preparación sigue las recomendaciones de tareas con metas neutrales y
observación moderada de [GOV.UK](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing).
Las decisiones concretas de muestra, tareas, tiempos y puntuación de este
protocolo son propuestas para este producto, no umbrales validados por esa guía.

## Cuatro plazas de reclutamiento, no participantes inventados

| Plaza prevista | Perfil buscado | Contexto previsto |
|---|---|---|
| R01 | Profesional GIS que no haya usado GeoImpact ni participado en su desarrollo | Escritorio 1440×900; idioma preferido. |
| R02 | Planificación territorial/ambiental, experiencia intermedia con mapas | Tablet emulada 834×1112 si es cómoda; registrar que usa ordenador. |
| R03 | Planificación o gestión turística, poca experiencia con evidencia GIS técnica | Escritorio; buscar voluntariamente una persona competente en EN para comprobar el segundo idioma. |
| R04 | Persona no especializada, sin entrenamiento GIS | Móvil emulado 390×844 si es cómodo; idioma preferido. |

Las plazas son objetivos de selección, no identidades ni sesiones. Si alguien
necesita otro viewport o modo de acceso, acomodarlo y anotarlo; no forzar un
formato que impida participar. Buscar al menos una persona que use habitualmente
teclado o ampliación; no recoger diagnóstico médico. Intentar incluir un usuario
habitual de lector de pantalla si puede hacerse con soporte adecuado. Si no,
dejar explícita esa falta de cobertura y planificar una sesión específica.

Preguntas mínimas de cribado: experiencia previa con GeoImpact (excluir),
actividad general entre esas categorías, uso de GIS (ninguno/ocasional/habitual),
idioma cómodo ES/EN y ajustes de acceso preferidos. No pedir edad exacta,
empleador, domicilio, datos demográficos sensibles o ejemplos de trabajo real.
Los contactos para organizar citas se guardan separados de las observaciones.
No reclutar colaboradores del PR como sustitutos de primeras visitas.

Cuatro casos permiten detectar y describir dificultades en esta ronda;
**no estiman prevalencia, representatividad estadística ni diferencias entre
perfiles, idiomas o dispositivos**. Perfil y formato pueden estar confundidos.
No prometer saturación ni porcentajes de problemas descubiertos. Cualquier
resultado debe expresarse con denominador y exposición real, por ejemplo
«n de las personas que intentaron T3», sin extrapolarlo a la población.

## Duración y preparación

Sesión prevista: 50–60 minutos, más descansos o ajustes acordados. Distribución:
consentimiento/contexto 8 min; T1 7, T2 8, T3 6, T4 7, T5 7; cierre 8.
La extensión Sierra añade hasta 3 min y puede omitirse sin penalización.
Estos topes sirven para organizar la sesión, no como SLA de usabilidad.

Antes de reclutar, completar [consentimiento](CONSENTIMIENTO.md), responsable,
contacto, observadores, acceso y fechas de borrado. No se ha invitado a nadie.
Asignar moderador ajeno al diseño y observador cuando sea posible; declarar
si solo hay una persona y esa limitación. Ensayar el guion con un colega sin
contarlo en la muestra ni anticipar respuestas a futuros participantes.

Antes de cada sesión:

1. Verificar el commit/bytes con el probe, servidor loopback y ausencia de
   Madrid. Preparar solo sintéticos salvo decisión previa de usar Sierra local.
2. Abrir un contexto efímero nuevo con `open-session.mjs --scenario normal`.
   No usar el navegador personal del participante, sesiones de desarrollador,
   cookies previas o onboarding ya completado. Establecer el idioma acordado
   mediante `--lang`; anotar ese ajuste, no evaluarlo como descubrimiento.
3. Preparar una segunda ventana `--scenario load-error` para T5 y dejarla
   fuera de vista hasta la tarea. Ningún fallo altera archivos originales.
4. Confirmar Escape, Ayuda y salida del tour; V01 es conocido. No ensayar
   previamente el recorrido con la persona ni ocultar los fallos al puntuar.
5. Usar solo notas locales por defecto. Cualquier grabación requiere permiso
   independiente y carpeta privada fuera del repositorio. Desactivar avisos
   personales y mostrar únicamente la ventana del estudio.

Para Sierra: revisar la decisión [GO_LOCAL_ONLY retenida](../../experiments/review-studio-local/rights/sierra-local.json),
identidades/atribuciones y limitaciones del caso antes de fijar la variante.
No se ofrece una autorización nueva. Si no se acredita esa preparación local,
omitirla y registrar NO EVALUADO; el estudio sintético sigue siendo válido.

## Introducción neutral

«Gracias por participar. Evaluamos la aplicación, no tus conocimientos.
Queremos observar cómo interpretas lo que aparece y cómo intentas realizar
las tareas. No hay decisiones reales que tomar con estos ejemplos. Puedes
pedir una pausa, omitir una tarea o terminar sin explicar el motivo. Si te
resulta cómodo, dinos en voz alta qué buscas y qué esperas. Usar ayuda está
permitido. Primero te dejaremos intentarlo; si necesitas apoyo, lo anotaremos.»

No explicar de entrada BASE, CANDIDATE, PASS, BLOCK, umbral, hashes ni la
asignación de hotel_813. El consentimiento informa del contexto del prototipo
y puede generar algo de orientación; no llamar al estudio «primera exposición
sin información previa». Facilitar las [tarjetas](TARJETAS_TAREAS.md) una a una.

## Tareas, criterios y preguntas de comprensión

### T1 — Primera visita (7 min)

Inicio: bienvenida visible de un contexto nuevo. Dejar elegir Start, Explore
o Not now; ninguna opción es un fallo por sí misma. Meta: explicar el propósito
y elegir un próximo paso plausible; encontrar Ayuda si decide necesitarla.

Criterio operativo: navega sin quedar atrapado. Comprensión completa: revisión
de cambios ya analizados entre versiones y posibilidad de rastrear evidencia;
no editar, predecir o calcular impactos nuevos. Aceptar palabras propias, no
exigir terminología GIS. Registrar qué parte de welcome/tour/práctica vio y
qué terminó antes de responder. No confundir terminar ocho pasos con entender.

Pregunta: «¿Qué esperarías poder hacer aquí y qué no?». Si no descubre Ayuda,
preguntar al final «¿Dónde intentarías buscar orientación?» sin señalar cabecera.

### T2 — hotel_813 en synthetic BLOCK (8 min)

Debe poder localizar el registro, seleccionarlo, relacionarlo con ambos mapas
y mostrar asignaciones y respaldo original. Referencia del reporte, no lectura
inferida del mapa: `hotels / hotel_813`, within, BEFORE `["chamberi"]`, AFTER
`["tetuan"]`, `assignment_changed`, JSON pointer `/relationships/0`, evidence_id
`relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49`.
BLOCK registra 2 regresiones con umbral 1. No exigir memorizar/copiar 64 caracteres:
basta localizar el identificador completo y el registro original correspondiente.

Criterio científico: explica cambio de asignación entre geometrías y política
superada; no movimiento físico del hotel, daño demostrado o datos certificados.
Preguntar «¿Qué cambió para este registro? ¿Cómo se relaciona con el resultado?».
No ofrecer primero alternativas con la respuesta correcta. Si utiliza la práctica,
registrar asistencia del producto y V02; un Comprobar rechazado no prueba que la
respuesta humana sea incorrecta.

### T3 — PASS y transferencia a poi_212 (6 min; Sierra opcional +3)

Caso `synthetic-pass`: 2 regresiones, umbral 2, 3 relaciones; `tourism_pois /
poi_212` conserva BEFORE `["chamberi"]` y AFTER `["tetuan"]`. Debe localizarlo,
explicar que PASS puede contener cambios y que el resultado depende de la
política. Filtrar cambia lo visible, no el reporte. No debe usar el veredicto
como certificado de calidad, legalidad o ausencia de efectos.

Preguntas: «¿Qué te permite afirmar este resultado? ¿Qué está mostrando ahora
la lista y qué muestra la evidencia seleccionada?». Si un filtro conserva una
selección fuera de sus filas, observar V03. No provocar esa combinación con
instrucciones de clic antes de observar el uso espontáneo. Puede explorarse
al final como sonda adicional; marcarla como inducida y no como tarea espontánea.

Sierra, solo si se fijó previamente: 52 relaciones, cero regresiones, parque
`69` modificado; 40 asignadas a 69 y 12 sin asignación en ambos estados. El
registro sin cambios no tiene evidence_id de regresión. La geometría cambiada
no obliga a que cambie una relación. Datos de equipamientos fijos al 2026-10-05,
no demostración de operación histórica. Puntuar esta parte como extensión
separada; no reemplazar el PASS sintético ni mezclar tiempos/éxitos entre variantes.

### T4 — Procedencia y límites (7 min)

Volver al caso sintético si se usó Sierra; ese cambio explícito del facilitador
se registra como transición de preparación, no ayuda para encontrar procedencia.
Debe localizar `report.json`, SHA-256, identidad y versiones registradas, con
posibilidad de abrir/descargar el original. El hash retenido de BLOCK es
`d09f70d2f7fa07cef3fa87f5b1fe73d932c8f9c4619487c4a0fe8c4cc1d7b8dd`;
en PASS es otro archivo y no se exige que coincida con BLOCK. Contrastar siempre
contra el manifiesto del caso activo; no declarar discrepancia por cambiar caso.

Comprensión: coincidencia de bytes frente a una referencia retenida; no firma
del proveedor ni licencia, exactitud absoluta o prueba de daño. Pedir ejemplos
de lo que seguiría sin comprobar. No exigir conocer el algoritmo SHA-256 o todas
las bibliotecas; sí localizar Report V5, geoimpact_ci y el conjunto de versiones
disponible. No presentar metadatos curados de fuente como campos nuevos de V5.

### T5 — ERROR, ayuda y recuperación (7 min)

Mostrar dos situaciones, con orden AB para plazas R01/R03 y BA para R02/R04,
fijado antes de observar conducta. No comparar órdenes causalmente con n=4.

- A: el caso distribuido `synthetic-error`, ejecución real de configuración
  ausente, exit 2, sin informe ni veredicto científico. El facilitador puede
  dejar la pantalla preparada; no se puntúa la elección de este caso como
  descubrimiento si la realizó el facilitador.
- B: otra ventana/contexto del mismo commit con `--scenario load-error`;
  report.json responde 404 solo en ese contexto. Es un fallo de carga, no una
  nueva ejecución del motor. El reporte retenido en disco sigue intacto.

Criterio: describe ambas indisponibilidades sin convertirlas en PASS/BLOCK o
cero regresiones, intenta una recuperación plausible y encuentra ayuda segura.
Debe reconocer que no puede revisar evidencia válida de esa carga. No es
necesario diagnosticar el código MISSING ni arreglar el error real. En B,
Reintentar seguirá fallando mientras la interceptación esté activa; no puntuar
eso como fallo del participante. Volver a A/ventana normal es una intervención
del facilitador, registrada; la recuperación científica no puede inventarse.

Preguntas: «¿Qué comunicarías de cada pantalla? ¿Qué necesitarías para seguir?
¿Dónde buscarías ayuda?». No exigir enviar un issue: no abrir cuentas ni publicar
datos. Al terminar, se puede pedir recuperar tour/glosario desde Ayuda en la
ventana normal. La recuperación tras retirar la condición de fallo es técnica,
no un éxito autónomo del participante.

## Medidas, asistencia y errores críticos

Para cada tarea, anotar inicio al terminar de leer la tarjeta, fin al declarar
haber terminado o alcanzar el tope; registrar tiempo transcurrido, pausas y
latencia de carga aparte. El transcurrido incluye lectura, ayudas y think-aloud;
no restar tiempos silenciosamente ni tratarlo como velocidad de trabajo real.
Al llegar al tope, ofrecer continuar brevemente o pasar: si se continúa,
conservar el exceso, no ajustar el umbral a posteriori. No presionar a alguien
con adaptación de acceso para cumplir el mismo tiempo; documentar la diferencia.

Separar ejecución y comprensión usando la [hoja](OBSERVACION_Y_RESULTADOS.md):
sin ayuda del moderador, con ayuda del producto, con intervención o no completado.
Codificar comprensión con respuesta literal anonimizada y razonamiento: 0
incorrecta, 1 parcial, 2 suficiente y matizada, NE no evaluada. Una respuesta
correcta tras enseñar el camino no se etiqueta como espontánea. Las opciones
cerradas de la práctica no sustituyen preguntas abiertas del estudio.

Errores críticos de interpretación, observables solo si ocurren: afirmar que
el hotel se movió físicamente; PASS significa cero cambios/datos certificados;
BLOCK demuestra daño; hashes prueban autenticidad o derechos; ERROR equivale a
cero regresiones o un veredicto; Sierra permite inferir equipamientos históricos.
Registrar la frase y el contexto, preguntar «¿En qué te basas?» una vez, sin
corregir durante las tareas relacionadas. Al final, realizar debrief correctivo;
si alguien quiere aplicar el resultado a una decisión real, interrumpir esa
aplicación y recordar el carácter experimental. No hay decisiones reales del
estudio ni datos personales de localización.

## Parada, cierre y síntesis

Parar por retirada, malestar, problema de acceso sin recuperación o incidencia
de privacidad. HOLD técnico si los bytes/versión no son los fijados, aparece
Madrid, se muestra evidencia inválida tras ERROR o se detectan valores ajenos
al reporte. Corregir el entorno antes de continuar; no ocultarlo en la puntuación.
V01: si el foco se pierde bajo el panel, observar brevemente, ofrecer Escape
como ayuda explícita si hace falta y anotar la tarea afectada; no forzar que
continúe a ciegas ni atribuir el problema a falta de habilidad.

Cierre: pedir explicación del mayor obstáculo, algo útil y algo incierto;
no preguntar «¿te gustó?» como medida principal. Repasar las limitaciones
científicas, confirmar voluntariedad y recordar contacto/código para retirada.
Preguntar qué cambiaría la persona, sin comprometer una solución o anunciar
funciones nuevas. No dar a las personas acceso a las notas de otras sesiones.

Dos revisores deberían contrastar códigos/interpretaciones cuando sea posible;
si solo hay uno, declararlo. Relacionar cada problema con tarea, observación,
asistencia y exposición a onboarding. Informar casos y denominadores, no
porcentajes poblacionales. Mantener resultados humanos separados de los trece
bloques de ingeniería. Aplicar [PRIORIDADES](PRIORIDADES.md) para una iteración
pequeña y después repetir tareas pertinentes con personas nuevas.
