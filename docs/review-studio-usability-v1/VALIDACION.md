# Registro ejecutado de preparación y auditoría

Fecha: 2026-10-18. Producto fijado en
`32f3ab50bb8a91d21118610bfc135b33e3fb2f3c`; revisión aislada en
`docs/review-studio-usability-v1`. No se han ejecutado sesiones humanas.

## Comandos y evidencia real

| Ejecución | Resultado y archivo |
|---|---|
| `npm ci --ignore-scripts` dentro de `experiments/review-studio-local` | Exit 0; dependencias de desarrollo del lock existente, sin cambio de package.json/lock. |
| `node docs/review-studio-usability-v1/evidence/probe.mjs` desde la raíz | Exit 0; 13 bloques de inspección, **6 VERIFIED_WITH_FINDING y 7 VERIFIED**, no 13 éxitos de usabilidad. [Salida](evidence/probe-output.txt), [JSON detallado](evidence/technical.json). |
| `node docs/review-studio-usability-v1/evidence/open-session.mjs --scenario normal --lang en --allow-local-sierra --self-check` | Exit 0; contexto efímero limpio, welcome en EN, sin grabación. |
| `node docs/review-studio-usability-v1/evidence/open-session.mjs --scenario load-error --lang es --width 390 --height 844 --allow-local-sierra --self-check` | Exit 0; contexto móvil emulado con 404 interceptado y vista científica retirada. |

Las dos salidas de utilidad están en [self-check-output.jsonl](evidence/self-check-output.jsonl).
Los logs se normalizaron a LF y las entradas de las trazas de foco se compactaron
a una línea por observación, sin cambiar valores, para facilitar la revisión.
`self_check: true` identifica comprobaciones de ingeniería headless, no personas
ni sesiones de investigación. El modo de utilidad con ventana visible debe
ensayarse por el moderador antes de la primera sesión; no se declara probado
como interacción humana por haber pasado el self-check.

Entorno de las ejecuciones: Windows, Node 24.11.0, Playwright 1.56.1,
Chromium 153.0.8010.12. `STUDIO_URL` no definido: loopback 8765 por defecto.
`STUDIO_CHROMIUM_EXECUTABLE` apuntó a ese Chromium instalado, omitiendo su ruta
absoluta privada del registro publicable. `STUDIO_AUDIT_SIERRA=1` en el probe:
la preparación local existente incluía Sierra y el caso se verificó sin guardar
su captura. La opción `--allow-local-sierra` se pasó conscientemente a las dos
comprobaciones de utilidad por ese catálogo; no equivale a autorización legal.

Los siete archivos servidos coincidieron con los bytes Git del commit. Los
27 archivos de datos/manifiestos del inventario local mantuvieron sus hashes
antes/después. Se comprobó la identidad de configuración y descarga del reporte,
sin recalcular asignaciones, política o métricas. Los errores se introdujeron
solo como respuestas interceptadas en contextos aislados, sin escribir sobre
fixtures o reportes. No hubo solicitudes externas de página, excepciones no
capturadas ni errores ordinarios de consola en la ejecución final.

Las inspecciones automáticas cubrieron seis viewports, contraste de una muestra
de pares CSS, diálogos/foco, semántica de Chromium, selección/mapas/cámara,
ocho pasos ES/EN, requisito de práctica, filtros, procedencia y los estados de
fallo. Se inspeccionaron visualmente capturas de foco cubierto, mapas en tablet
y móvil, evidencia filtrada y requisito de práctica. Las capturas contienen
únicamente sintéticos; no muestran participantes ni hardware físico.

Las iteraciones de diagnóstico ajustaron una expectativa inicial demasiado
amplia del probe: se había exigido reproducir el foco cubierto en cada tamaño.
El resultado real de 1440×1000 fue cero en esa secuencia, por lo que el probe
pasó a registrar el fenómeno donde ocurre, sin atribuirlo a todos los tamaños.
No se cambió la aplicación para producir ese resultado. Solo la ejecución
final completa se conserva como evidencia.

## Comprobaciones documentales y de aislamiento

Se verificaron enlaces relativos existentes, JSON/CSV válidos y plantillas
humanas vacías; ninguna respuesta, participante reclutado o tiempo humano se
rellenó. Se revisaron rutas privadas absolutas y direcciones de correo: no
aparecen en los archivos publicables. Los datos operativos de consentimiento
son campos explícitos pendientes, no identidades inventadas.

El diff protegido frente a la referencia está vacío para `src`, `tests`,
`scripts`, `research`, `experiments`, `.github`, pyproject y atributos Git.
Todos los cambios de este incremento están dentro de
`docs/review-studio-usability-v1/`. [manifest.json](evidence/manifest.json)
identifica scripts, evidencia, documentos y capturas por SHA-256. El servidor
utilizado sigue sirviendo la referencia; este PR documental no cambia su UI.

No se ha repetido innecesariamente la suite científica de 113 pruebas en una
rama sin cambios de motor. La [CI del commit evaluado](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/39163924184)
es el antecedente Linux/Windows comprobado; no se presenta como resultado de
usuarios ni como certificación de accesibilidad. Cualquier CI de esta rama
documental es un registro separado y no reemplaza los probes de interfaz.

## Alcance del veredicto

**GO al estudio moderado local**, una vez completados consentimiento operativo,
equipo y ajustes de acceso. Las condiciones de parada están en el protocolo.
V01 y V02 se mantienen visibles como problemas de interacción; no se ocultan
para obtener una tasa artificial de éxito. El estudio podrá revelar otros
problemas o que las hipótesis no se sostienen.

Sin pruebas humanas no hay evidencia de comprensión, éxito de tareas o
satisfacción. Sin lector de pantalla/hardware físico no hay evidencia de
soporte real de esas combinaciones. Sin evaluación completa no hay declaración
WCAG. **R1 OPEN mantiene HOLD para Madrid y el visor completo.** No se ha
modificado, fusionado, desplegado o publicado la aplicación ni enviado mensajes.
