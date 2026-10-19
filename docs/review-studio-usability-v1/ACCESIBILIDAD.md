# Accesibilidad: inspección técnica preliminar

Referencia exacta: `32f3ab50bb8a91d21118610bfc135b33e3fb2f3c`. Se usan la
ejecución y trazas de [technical.json](evidence/technical.json), inspección de
código y capturas reales. **No hay declaración de conformidad WCAG** ni prueba
con lector de pantalla. Una instantánea semántica de Chromium no sustituye
una sesión con una persona que use tecnología de apoyo.

## Matriz de comprobaciones

| Área | Hallazgo verificado | Límite / comprobación pendiente |
|---|---|---|
| Teclado normal | Selección con Enter, pan con flechas, zoom/encuadre con botones, Tab sale del mapa. La lista es alternativa textual. | Atajos con NVDA/JAWS/VoiceOver, browse mode, reconocimiento de voz y switches no evaluados. |
| Foco del recorrido | **V01: controles totalmente cubiertos en 5 de 6 secuencias** de 50 Tab. Escape recupera Ayuda. | Requiere corrección pequeña y retest de todo foco, no solo del objetivo resaltado. No afirmar «teclado accesible» globalmente. |
| Diálogo nativo | Nombre accesible, foco dentro con Tab y Shift+Tab, Escape cierra y vuelve a Ayuda. | Lectura inicial, orden de anuncio, navegación por encabezados y scroll con lector de pantalla pendientes. |
| Orden / semántica | Un main y h1; regiones tituladas, controles nativos, campos etiquetados y estados seleccionados. Instantáneas semánticas retenidas en JSON. | No se ha comprobado todo el árbol en todas las combinaciones de estado/idioma. SVG con role=img necesita validación del modo de interacción con tecnología de apoyo. |
| Navegación | Ayuda en cabecera, reinicio del recorrido, opción de saltar, cierre y enlaces de evidencia/procedencia alcanzables. | El coste de tabular hasta Ayuda desde un panel lejano se debe observar con personas. |
| Mensajes | ERROR tiene role=alert; carga/selección/progreso disponen de regiones vivas. ERROR elimina datos anteriores y deshabilita ayudas dependientes de evidencia. | La frecuencia y posibles anuncios duplicados no están probados auditivamente. |
| Reflow | Sin overflow horizontal en 1440×900, 1440×1000, 834×1112, 390×844, 375×812 y 320×812 en los estados inspeccionados. | 320 px de viewport no certifica por sí solo todos los requisitos de reflow. |
| Zoom | CSS zoom 200% en escritorio: contenido y tour operables sin overflow horizontal en esa comprobación. | Zoom real del navegador 200/400%, solo texto, preferencias de fuente y espaciado de texto pendientes. CSS zoom no se presenta como equivalente completo. |
| Contraste de texto | Pares CSS opacos medidos; mínimo muestreado ≈5.025:1 en `.row small` sobre blanco. Véase tabla. | No se midieron todos los estados de foco/hover/deshabilitado, antialiasing, superposiciones, placeholder, contraste forzado o modos del sistema. |
| Color y mapa | BASE/CANDIDATE tienen texto y trazos distintos; cambios usan símbolo y etiquetas; antes/después están en texto. | Contraste no textual de todas las líneas, anillos y selección sobre todos los rellenos sin evaluar exhaustivamente. No inferir cumplimiento por contraste del texto. |
| Tamaños de interacción | Los controles principales tienen mínimos CSS de 44 px de alto; los enlaces de texto no siempre. | No se certifica SC 2.5.8/áreas de separación ni precisión táctil. Medir en hardware real y con uso motor habitual. |
| Movimiento | Modo reduced-motion solicitado en Chromium; no requiere animación para avanzar. | Preferencias reales del sistema y tolerancia individual pendientes. |
| Idioma | html[lang] y texto cambian ES/EN sin perder paso; IDs y tokens técnicos se conservan. | Pronunciación de términos mixed-language y adecuación lingüística con personas pendientes. |

## Contraste: evidencia limitada y reproducible

Se calculó luminancia relativa con valores CSS de texto y el primer fondo
opaco de sus ancestros. No se aplicó ese método simplificado a fondos
transparentes compuestos, mapas, imágenes o estados no muestreados. Las
comparaciones se hacen con el valor sin redondear; las cifras de esta tabla
se redondean solo para lectura.

| Muestra | Colores | Relación observada |
|---|---|---:|
| Cuerpo | `#183542` / `#f3f6f4` | 11.864:1 |
| Nota de alcance | `#52696c` / `#f3f6f4` | 5.367:1 |
| Dataset en fila | `#587477` / `#ffffff` | 5.025:1 |
| Hash en procedencia | `#183542` / `#ffffff` | 12.909:1 |
| Botón Ayuda | `#eef6f3` / `#1c3947` | 11.075:1 |
| Cautela | `#334c3a` / `#f3f6ed` | 8.595:1 |

El criterio de texto normal de referencia es 4.5:1; cumplir esos pares no
certifica legibilidad de texto pequeño ni el resto de la interfaz.
[W3C, contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
El contraste de elementos no textuales requiere una revisión propia:
[W3C, contraste no textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

## Interpretación de V01 y siguiente comprobación

V01 es un defecto de foco observable y un riesgo respecto a SC 2.4.11 y 2.4.7.
No se emite una clasificación de conformidad de toda la página: deben
considerarse el contexto, las excepciones aplicables y la forma de revelar
un elemento sin mover su foco. La captura prueba que el componente recibe
foco bajo contenido del autor; la existencia de Escape evita un encierro
permanente, pero cerrar el tour cambia el foco a Ayuda.
[W3C, foco no oculto](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum).

Aceptación propuesta para una corrección posterior: durante el recorrido,
cada componente alcanzado con Tab/Shift+Tab conserva una zona enfocada
visible y operable; preferiblemente todo el componente y su indicador.
Verificar los seis tamaños, scroll manual y zoom, sin convertir el recorrido
en una trampa modal ni romper los mapas. La prueba actual solo del objetivo
resaltado debe ampliarse a la navegación real entre controles.

La semántica y gestión de foco del diálogo se contrastan con el patrón
[APG de diálogo modal](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/),
que es guía de diseño, no una certificación. Para teclado y reflow se usan
[SC 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) y
[SC 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) como
referencias de inspección, no como una lista exhaustiva de conformidad.

Antes de declarar soporte de tecnología de apoyo, ejecutar al menos un
recorrido completo con una persona usuaria habitual y su combinación real
de lector/navegador: propósito, salto de mapa a lista, selección, valores,
procedencia, ERROR, idioma y salida. Registrar versiones y problemas sin
recoger diagnósticos médicos. Si no se consigue reclutar ese perfil entre
las cuatro personas, dejarlo explícitamente pendiente y organizar una ronda
específica; cuatro participantes diversos no cubren todas las discapacidades.

En hardware físico posterior: orientación, tacto/scroll, teclado virtual,
zoom del navegador, tamaño real de texto/objetivos y navegación asistida.
Usar localhost en el propio dispositivo o un entorno previamente autorizado;
no abrir este servidor a LAN ni publicar una demo para obtener esa cobertura.
