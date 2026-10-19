# GeoImpact Review Studio — evaluación formativa V1

**Decisión: GO para iniciar un estudio moderado local con cuatro personas,
con los defectos y reglas de parada descritos aquí.** No es un GO de producto,
de accesibilidad ni del visor completo. **R1 OPEN; Madrid permanece HOLD.**
No se ha reclutado a nadie ni se ha celebrado ninguna sesión.

**Actualización V01/P1-01, 2026-10-19:** futuras sesiones deben utilizar PR #23,
commit corregido **`4133c2262fb16546a0dd41f09dd5a6a92b64c100`**, según la
[versión y preflight del protocolo](PROTOCOLO.md#versión-para-las-próximas-sesiones--2026-10-19).
La evidencia original de este PR permanece sin sobrescribir y describe la
versión anterior. El [registro de comprobación](evidence/v01-version-check.json)
distingue ambas identidades. No se modifica ningún otro hallazgo UX.

La auditoría histórica evalúa [Draft PR #23](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/23),
commit **`32f3ab50bb8a91d21118610bfc135b33e3fb2f3c`**. El trabajo está en una
rama documental separada: `docs/review-studio-usability-v1`. No cambia la
aplicación, el motor v1.2.0, Report V5, geometrías, fixtures ni resultados.
Tampoco modifica o cierra los PR #21/#22/#23.

## Qué se ha hecho y qué falta

| Clase de evidencia | Estado |
|---|---|
| Ingeniería reproducida | Inspección nueva del código y Chromium sobre el commit exacto; seis tamaños, teclado, diálogos, mapas, selección, procedencia, PASS con cambios, ERROR y Sierra local con cero regresiones. |
| Hipótesis UX | Claridad, descubrimiento, carga cognitiva e interpretación: preguntas para el estudio, no resultados de personas. |
| Resultados humanos | **0 participantes reclutados, 0 sesiones, 0 respuestas.** Plantillas vacías; ninguna tasa de éxito humana. |
| Independencia | Separación de método, rama y evidencia respecto a la implementación. La revisión la realiza el mismo asistente que implementó el onboarding; **no es una auditoría humana externa ni la aprobación de un equipo independiente real**. Un moderador ajeno a la implementación debe ejecutar el estudio. |

El hallazgo técnico principal es **V01**: durante el recorrido, Tab puede
enfocar controles enteramente cubiertos por el panel fijo. Se reproduce en
cinco de seis tamaños; no en la secuencia medida de 1440×1000. Escape permite
salir. También se ha observado que la práctica exige una visita mediante un
control concreto y que una selección puede permanecer fuera de los filtros.
Su efecto en comprensión o abandono sigue siendo una hipótesis.

## Paquete para ejecutar el estudio

1. Leer [auditoría técnica](AUDITORIA_TECNICA.md) y [accesibilidad](ACCESIBILIDAD.md).
2. Completar las identidades y fechas del [consentimiento](CONSENTIMIENTO.md)
   antes de invitar a participantes. No enviar el formulario con campos vacíos.
3. Ejecutar la comprobación técnica, probar el guion con un colega y preparar
   los dos contextos de T5 sin editar archivos científicos.
4. Ejecutar las cinco tareas del [protocolo](PROTOCOLO.md), con un moderador y
   una persona observadora cuando sea posible. El ensayo del guion no cuenta
   entre las cuatro personas del estudio.
5. Registrar hechos y respuestas fuera del repositorio usando
   [observación y resultados](OBSERVACION_Y_RESULTADOS.md). Aplicar las reglas
   de parada y la [priorización/iteración](PRIORIDADES.md).

No se exige que cada persona complete el tour o la práctica. Esa elección es
un dato: las ayudas vistas deben registrarse para no confundir aprendizaje
guiado con comprensión espontánea. El estudio es diagnóstico, no una prueba
estadística representativa ni un experimento causal de idioma o dispositivo.

## Reproducción técnica

Utilizar un checkout que conserve el commit de referencia. Preparar el
servidor siguiendo el [README del prototipo](../../experiments/review-studio-local/README.md)
y la versión congelada del motor. Por defecto, preparar **solo sintéticos**.
No servir la raíz del repositorio ni abrir la aplicación a la red. Si el
servidor ya está en `http://127.0.0.1:8765`, el probe verifica que los siete
archivos de la interfaz coincidan byte a byte con el commit de referencia.

Desde la raíz de la rama documental, en PowerShell:

Este probe reproduce **solo la auditoría histórica en 32f3ab5**. Para las
próximas sesiones usar los self-checks con referencia corregida indicados abajo.

```powershell
npm --prefix experiments/review-studio-local ci --ignore-scripts
npx --prefix experiments/review-studio-local playwright install chromium
node docs/review-studio-usability-v1/evidence/probe.mjs
```

Si se usa otro puerto de loopback, definir `STUDIO_URL`. Un Chromium ya
instalado puede seleccionarse mediante `STUDIO_CHROMIUM_EXECUTABLE`; no se
requiere una ruta de máquina en el proyecto. Las dependencias son exclusivamente
de desarrollo y las solicitudes de la aplicación se restringen al mismo origen.

Sierra es opcional: preparar localmente bajo la revisión de derechos retenida,
con sus atribuciones, y definir `STUDIO_AUDIT_SIERRA=1` para comprobar su cero
válido. Esto no constituye una nueva autorización legal o de redistribución.
El probe no conserva capturas de Sierra. La ejecución registrada sí incluyó
el caso local ya preparado; con preparación solo sintética se registra
`NOT_EVALUATED` para Sierra y el resto sigue siendo reproducible.

Los resultados de ingeniería están en [technical.json](evidence/technical.json),
con las versiones, hashes del código servido, trazas de foco, pares de contraste,
estados y comparación de bytes antes/después. **`VERIFIED_WITH_FINDING` significa
que la inspección encontró un problema, no que la aplicación aprobó accesibilidad.**
Las [capturas](evidence/screenshots/) contienen exclusivamente datos sintéticos.
Los registros anteriores de PR #23 son antecedentes; no se sustituyen por
supuestos resultados humanos.

La [validación ejecutada](VALIDACION.md) conserva comandos, salidas y límites
de esta revisión. Si cambia la versión de Chromium, registrar la nueva y
revisar los hallazgos; no asumir que los conteos de foco serán idénticos.

## Abrir un contexto limpio para una sesión futura

La utilidad no inicia una investigación ni registra a una persona por sí sola.
Abre Chromium visible con almacenamiento efímero y sin grabación, contra el
servidor local ya preparado. Cerrar la ventana termina el proceso.

```powershell
node docs/review-studio-usability-v1/evidence/open-session.mjs --reference 4133c2262fb16546a0dd41f09dd5a6a92b64c100 --scenario normal --lang es --width 1440 --height 900
node docs/review-studio-usability-v1/evidence/open-session.mjs --reference 4133c2262fb16546a0dd41f09dd5a6a92b64c100 --scenario load-error --lang es --width 1440 --height 900
```

La segunda ventana intercepta únicamente `report.json` con un 404 en su propio
contexto. No cambia el servidor, el reporte original ni su manifiesto. Es el
fallo de carga controlado de T5, distinto del ERROR de análisis ya distribuido.
`--lang en` adapta el idioma mediante el control real. `--allow-local-sierra`
exige una decisión explícita del facilitador si el catálogo local la contiene.
`--self-check` prueba la utilidad en headless y **no cuenta como sesión humana**.
Ejecutar ambos comandos con `--self-check` antes de abrir las ventanas de sesión.
La emulación de 834×1112 o 390×844 en un ordenador no equivale a una tablet o
teléfono físico; anotarlo así en los resultados.

## Condiciones del GO

Antes de una sesión: consentimiento operativo completo, moderador asignado,
casos y referencia verificados, contexto nuevo, medios de acceso acordados y
salida con Escape ensayada. V01 debe estar corregido en la versión fijada; si
reaparece, parar la tarea, registrar fallo/ayuda y salir del recorrido, sin atribuírselo a la
persona. No convertir esa tarea en un éxito sin asistencia. Una persona debe
poder parar o usar su modo de acceso habitual; no excluirla para mejorar cifras.

**HOLD de la sesión** si hay discrepancia de versión/bytes, evidencia científica
incorrecta o residual tras ERROR, falta de consentimiento o imposibilidad de
salir/continuar de forma accesible con los ajustes acordados. No se ha reproducido
un P0 científico en esta auditoría. Los P1 no justifican un rediseño antes del
estudio; sí justifican registrar sus efectos y planificar correcciones pequeñas.

No se ha hecho merge, despliegue, demo pública, envío al INE ni contacto con
participantes. La comprensión real y la accesibilidad con tecnología de apoyo
quedan pendientes hasta que ocurran las sesiones correspondientes.
