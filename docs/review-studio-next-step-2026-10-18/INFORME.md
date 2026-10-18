# GeoImpact Review Studio: derechos, reconciliación y siguiente incremento

> Actualización de alcance: este informe conserva la decisión histórica. La instrucción posterior separa #22 documental de un nuevo Draft PR funcional; véase [reconciliación](../../experiments/review-studio/RECONCILIATION.md).

Fecha de auditoría: **18 de octubre de 2026**. Resultado: **R1 OPEN; HOLD del visor completo Madrid + Sierra; GO condicionado para un futuro prototipo exclusivamente local de Sierra de Baza y datos sintéticos**. En este encargo se entrega documentación, sin implementar ese prototipo.

La condición local reduce el alcance de publicación; no sustituye una autorización de uso. El GO de Sierra se apoya en condiciones positivas de sus proveedores y exige conservarlas y atribuirlas. El GO técnico y los hashes coincidentes no resuelven derechos, utilidad, accesibilidad ni validez externa.

## Evidencia y límites de esta auditoría

Se revisaron los commits completos de [PR #21](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/21) (`ae0244fae0032dba7f5a890476897056c7ef4cf5`) y [PR #22](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/22) (`447b17db96f4358ec5e35542d2148c03cd0f5306`), sus descripciones, archivos, estado de checks y conversaciones. Ambos estaban OPEN y Draft; no había comentarios de conversación, revisiones ni comentarios inline al consultar. Las decisiones siguientes son de esta auditoría, no aprobaciones de terceros.

La base científica es `v1.2.0`, commit resuelto `45237d7caaea2aa4b81359e46f1623918645078c`, contrato Report V5. La base documental común de los PR es `c39733b61b60abe3b6e9e9c50f74f5c206022399`. Las referencias a archivos de PR usan esos commits, evitando depender del contenido futuro de sus ramas.

[evidence.json](evidence.json) conserva las respuestas de metadatos de GitHub, las URL oficiales consultadas, fecha UTC, tamaño y SHA-256 de las respuestas HTTP obtenidas y observaciones de licencias. No contiene geometrías. Las respuestas completas del proveedor no se archivan aquí: los hashes permiten comparar futuras capturas, pero no reconstruir la respuesta ni acreditar su autenticidad. Las dos páginas legales de Creative Commons devolvieron 403 al cliente HTTP directo y se leyeron con la herramienta web; se registra esa diferencia, sin inventar hashes de esas respuestas. La guía INE se examinó mediante su texto PDF; sus capturas no se usan como prueba jurídica.

Se contrastaron **los seis hashes retenidos en #22 con los manifiestos esperados del tag** y coinciden. No se volvió a ejecutar el motor ni se presenta esa comparación como una nueva reproducción. Los resultados de ejecución previos están en [VALIDATION de #22](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/447b17db96f4358ec5e35542d2148c03cd0f5306/experiments/review-studio/VALIDATION.md). No hubo pruebas nuevas de navegador ni participantes.

## Fase A: R1 permanece OPEN

### Fuentes oficiales y hallazgos

| Ref. | Fuente oficial | Evidencia relevante y alcance |
|---|---|---|
| I1 | [Colección Secciones_2024, HTML](https://www.ine.es/geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01:Secciones_2024?f=text%2Fhtml) | Identifica la colección y EPSG:25830. El pie etiqueta el contenido CC BY-SA 4.0, pero el atributo `href` del mismo enlace conduce a `https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1`. |
| I2 | [Colección Secciones_2025, HTML](https://www.ine.es/geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01:Secciones_2025?f=text%2Fhtml) | Repite la contradicción etiqueta BY-SA / destino BY; no se resuelve escogiendo uno de los dos. |
| I3 | [Índice oficial API Features](https://www.ine.es/geoserver/ogc/features/v1/collections?f=text%2Fhtml) | Acceso gratuito condicionado a atribución: «Seccionado cedido por el Instituto Nacional de Estadística». Es una condición expresa del servicio; no determina por sí sola la licencia de cada derivado redistribuido. |
| I4 | [Aviso legal enlazado desde las colecciones](https://www.ine.es/dyngs/AYU/index.htm?cid=125) | Régimen general CC BY 4.0 para información estadística de origen INE, salvo indicación contraria; atribución, fecha de actualización cuando figure y ausencia de respaldo institucional. No permite elegir qué significado tiene el pie contradictorio. |
| I5 | [Datos abiertos INE](https://www.ine.es/datosabiertos/) | Presenta CC BY 4.0 y enlaza la cartografía. Refuerza el contexto general, sin identificar inequívocamente las condiciones de estos dos snapshots y sus subconjuntos. |
| I6 | [2024 JSON](https://www.ine.es/geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01:Secciones_2024?f=application%2Fjson) y [2025 JSON](https://www.ine.es/geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01:Secciones_2025?f=application%2Fjson) | En las respuestas inspeccionadas no hay campos explícitos de licencia/derechos ni enlaces de licencia o metadatos que aclaren esta cuestión. La ausencia no concede permisos. |
| I7 | [WFS del espacio de trabajo INE](https://www.ine.es/geoserver/WMS_INE_SECCIONES_G01/wfs?service=WFS&request=GetCapabilities&version=2.0.0) | `Fees=NONE`, `AccessConstraints=NONE`; entradas para ambas colecciones sin una aclaración específica de licencia. Estos valores de servicio no equivalen a dominio público, CC0 ni permiso de redistribución. |
| I8 | [Guía técnica API Features, diciembre 2025](https://ine.es/geoserver/www/guias/OGC_API_Feature_Seccionado.pdf) | Explica consultas, descarga, clientes y aplicaciones propias; describe la nomenclatura histórica. No contiene una licencia específica que deshaga la contradicción. Su texto no respalda atribuirle una restricción de uso privado. |

La distinción nueva frente a #22 es **interna al propio enlace de cada colección**, además de la diferencia con el aviso general. Puede ser un error de plantilla, pero esa explicación es una hipótesis. No hay base concluyente en las fuentes examinadas para declarar aplicable una licencia específica a los dos snapshots y a todas las reutilizaciones previstas. Tampoco se concluye que el uso esté prohibido.

### Qué permite afirmar la evidencia por operación

| Operación prevista | Evidencia positiva | Decisión para Madrid mientras R1 esté OPEN |
|---|---|---|
| Acceso y consulta del servicio | I3 e I8 documentan acceso gratuito con atribución y consultas. | Documentar ese acceso; no convertirlo en autorización para otra operación. Esta auditoría solo consultó metadatos. |
| Reproducción y copia de archivos | I4 contempla copia bajo el régimen general; I1/I2 introducen la ambigüedad aplicable. | No autorizar nuevas copias destinadas a un paquete visual. |
| Modificación: selección, conversión, reproyección o simplificación | I4 y las licencias CC consideradas admiten ciertos usos derivados bajo condiciones. No se ha fijado cuál rige estos datos. | No generar nuevos derivados de Madrid para el prototipo. No atribuir a todas las transformaciones la misma categoría jurídica. |
| Visualización pública, capturas, mapas o teselas | La licencia general contempla comunicación pública; el servicio ofrece visualización técnica. Ninguna prueba despeja por sí sola el alcance de las condiciones contradictorias. | HOLD de mapas públicos y capturas con geometrías INE. Rasterizar o usar WMS no elimina la cuestión. |
| Redistribución de un subconjunto o huella derivada | Necesita identificar licencia, atribución, modificaciones y, si procede, CompartirIgual; un subconjunto pequeño no está automáticamente exento. | HOLD de GeoJSON, bundles, teselas, descargas y geometrías derivadas de Madrid. |

Son decisiones de gate del proyecto, no una declaración jurídica de infracción. La presencia previa de fixtures en GitHub, el carácter de investigación, la gratuidad y la licencia MIT del software no acreditan estos permisos. No se reinterpretan retrospectivamente como una autorización para nuevas distribuciones.

### CC BY 4.0 frente a CC BY-SA 4.0

Ambas permiten compartir y adaptar, incluso comercialmente, si se cumplen sus términos. Ambas exigen reconocimiento, referencia a la licencia e indicación de modificaciones; deben conservarse los avisos suministrados que correspondan. BY no impone CompartirIgual a las contribuciones del adaptador. Véase [CC BY 4.0, secciones 2–4](https://creativecommons.org/licenses/by/4.0/legalcode.es).

BY-SA añade condiciones cuando se comparte Material Adaptado: licencia con los mismos elementos en la versión admitida o una compatible reconocida y ausencia de restricciones adicionales incompatibles. Incluye reglas sobre derechos sui generis de bases de datos. No significa automáticamente que todo código del visor pase a BY-SA, ni que cualquier conversión técnica constituya Material Adaptado: ambas licencias distinguen modificaciones técnicas y adaptación jurídica. Véase [CC BY-SA 4.0, secciones 1–4](https://creativecommons.org/licenses/by-sa/4.0/legalcode.es).

Si INE confirmara BY-SA, habría que delimitar y documentar sus efectos sobre subconjuntos, huellas, mapas y bases de datos combinadas. No se usará BY-SA «por prudencia» para suplir la falta de determinación del titular, ni se asumirá una doble licencia a elección del usuario.

### Evidencia exacta necesaria para cerrar R1

Una aclaración del INE competente o términos oficiales inequívocos deben identificar **ambas colecciones históricas**, los snapshots de Madrid recuperados el 2026-10-03, su procedencia y los usos concretos. Registrar URL/documento, fecha, alcance, atribución exigida, cambios permitidos, redistribución y obligaciones de derivados/bases de datos. Si la respuesta solo trata acceso o una de las colecciones, R1 continúa OPEN para el resto.

Los snapshots canónicos del registro de Madrid se identifican por SHA-256 `120692f71460f8cfd12f6542d4d7917337d916a781cac29e918bbd1b0e8946e8` (2024) y `3ce9184cf5f2ff3f0f9bcaf9211a50ea5826487d2320ee96976d53e00b8eb70d` (2025). Son identidades locales de los subconjuntos recuperados, no firmas del INE. Véase el [registro fijado de fuentes Madrid](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/447b17db96f4358ec5e35542d2148c03cd0f5306/docs/GATE_5_SOURCE_REGISTER.md).

Se entrega la [consulta profesional al INE](CONSULTA_INE_BORRADOR.md), **sin enviar**. El canal propuesto es el formulario oficial indicado en I4. No se necesita resolver R1 para continuar con la planificación documental del incremento acotado.

## Fase B: reconciliación de #21 y #22

Para la matriz, **E** = evidencia ejecutada retenida en #22, no repetida aquí; **D** = requisito cubierto como diseño; **P** = parcial o discrepancia documental; **F** = pendiente de un gate futuro. Cobertura de diseño no equivale a implementación.

Referencias fijadas: [especificación #21](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/ae0244fae0032dba7f5a890476897056c7ef4cf5/docs/REVIEW_STUDIO_FEASIBILITY_V0_1.md), [AUDIT #22](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/447b17db96f4358ec5e35542d2148c03cd0f5306/experiments/review-studio/AUDIT.md), [DESIGN #22](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/447b17db96f4358ec5e35542d2148c03cd0f5306/experiments/review-studio/DESIGN.md), [VALIDATION #22](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/447b17db96f4358ec5e35542d2148c03cd0f5306/experiments/review-studio/VALIDATION.md).

| Requisito importante de #21 | Cobertura concreta de #22 | Estado |
|---|---|---|
| §§0–1: baseline v1.2.0/V5, jerarquía actual e hipótesis de revisión | README: Scope; AUDIT: release, Existing versus new | D |
| §2: Polygon/MultiPolygon, IDs estables, dependencias Point fijas, `within` | AUDIT: inventario; probe: `indexed_features`, `check_joins` | D/E |
| §2: separar geometría primaria, relación, frontera y verdict; ERROR no es BLOCK | AUDIT A5; DESIGN: encodings y J5; VALIDATION: exits 0/1/2 | D/E; UI F |
| §§2–3: CRS84 de inputs/export y EPSG:25830 del report | AUDIT A4; DESIGN: overlay omitido; probe comprueba CRS del report | D/E; ruta cartográfica F |
| §3: JSON autoritativo, Markdown de referencia, GeoJSON solo regresiones, originales necesarios | AUDIT: inventario; DESIGN: Evidence panel | D |
| §3: hashes/tamaños de config, BASE, CANDIDATE, dependencias y cinco versiones | AUDIT A6; probe `probe_case`; DESIGN J4 | D/E |
| §3: falta/mismatch/no comprobado; identidad no es autenticidad | AUDIT: límites de hash y A6; DESIGN J5 y estados | D/E; UI F |
| §4: Madrid BLOCK/2.112, 26 pares, subset acotado, sin causalidad ni extrapolación | AUDIT: casos y anotaciones; evidence-summary; VALIDATION | D/E |
| §4: selección y agrupación Madrid por before→after | DESIGN J2 y búsqueda; no prescribe expresamente filtro por los 26 pares | P: añadir filtro de pares como requisito futuro, sin inferir split/merge |
| §4: atribución INE/Ayuntamiento y separación de MIT | AUDIT: rights gate; bundle detenido por R1 | D/F por R1 |
| §5: Sierra PASS/0, 52 relaciones, 40 dentro/12 fuera, geometría modificada | AUDIT: casos; DESIGN J1/J3/J5; probe de cobertura | D/E |
| §5: inventario fijo 2026 frente a límites 2015/2025; Gate 8 MODIFY no cambia por PASS | AUDIT trata fechas y límites, pero no repite explícitamente el resultado histórico MODIFY | P: conservar esa nota en la fuente principal |
| §5: no asumir CC BY 4.0 para todos los WFS REDIAM | AUDIT: tabla de fuentes distingue catálogo 2015 de respuestas actuales | D |
| §6: inspeccionar, explicar, distinguir, auditar, reproducir | DESIGN J1–J5; VALIDATION: comandos reproducibles | D/E; utilidad externa F |
| §7: selector de casos, threshold visible, mapas, puntos sin cambios, inspector, audit drawer | DESIGN: jerarquía, J1–J5 y paneles | D/F |
| §7: filtros solo alteran filas visibles; total original permanece | DESIGN: controles y totales separados | D/F |
| §§7–8: lector aislado, manifiesto pequeño, sin uploads, backend, LLM, GIS adicional ni política editable | AUDIT A1/A2/A8; DESIGN: exclusiones y controles | D/F |
| §8: rechazar V4, no inventar procedencia; overlay aplazado | AUDIT A4/A6; probe rechaza versión distinta de 5 | D/E |
| §9 F0: viabilidad documentada y límites honestos | README/AUDIT/DESIGN/VALIDATION completos; sin visor | D |
| §9 F1: reproducción limpia, tests, exits y hashes oficiales | VALIDATION: tag, entorno, 113 tests, verifiers y seis hashes; se retiene resumen | E, verificable por comandos |
| §9 F2: rechazo de hashes, IDs/evidencias, originales obligatorios, 52/52 | probe + ocho pruebas acotadas; no validador general ni adaptador UI | E para probe; F para adaptador completo |
| §9 F3: navegadores y tamaños 1440×900, 834×1112, 375×812 | #22 cambia a 1440×1000, 834×1112, 390×844; SVG móvil de contenido 390×1100 | P: ningún tamaño se probó; mantener los cinco viewports de ambas propuestas en el plan |
| §9 F3: teclado, lista accesible, ES/EN, sin color como única clave, rendimiento medido | DESIGN: contratos detallados; VALIDATION: futuros gates | D/F; sin resultados de rendimiento |
| §9 F4: estudio independiente y separación de External Validation V1 | AUDIT y VALIDATION proponen estudio; no lo ejecutan ni alteran el protocolo CLI | D/F |
| §§9–10: publicación solo tras derechos, controles reales de seguridad/accesibilidad y riesgos | AUDIT A6 concreta seguridad; VALIDATION gates; sin publicación | D/F; evaluación de seguridad aún pendiente |
| §11: entrega `F1_ARTIFACT_INTEGRITY_GATE.md`; F2 separado | #22 incorpora la evidencia en VALIDATION y evidence-summary, sin ese archivo ni referencia desde #21 | P: equivalencia sustantiva, falta reconciliar estructura y transición de gates |
| §§0/11: alcance del GO/HOLD | #21 admite F2 local condicionado; #22 detiene la implementación de dos casos por R1 | P: divergencia de alcance que debe quedar explícita, no resolverse con un cambio de etiqueta |

**Conclusión:** #22 cubre los elementos científicos, de integridad y diseño centrales de #21; no se puede afirmar cobertura literal completa ni finalización de F2–F4. Los huecos son principalmente de trazabilidad, alcance y criterios de aceptación, además de implementación/validación futura deliberadamente pendiente.

### Un único PR principal propuesto

Mantener **#22 como único PR principal, Draft**, con su evidencia y experimento aislado. Integrar allí, en una futura actualización documental, la especificación de #21 con una nota de supersesión y enlaces a esta matriz, preservando el contenido útil y su historial. Identificar VALIDATION + evidence-summary como la entrega F1 equivalente; conservar expresamente Gate 8 MODIFY, añadir el filtro de pares y reconciliar los viewports. No basta cerrar #21 sin trasladar estos requisitos.

Tras comprobar la cobertura en #22, proponer cerrar #21 como sustituido por #22 **sin merge**. Este informe no actualiza, comenta ni cierra ninguno. No se propone fusionar las dos ramas entre sí ni llevar contenido a main en este encargo. Un futuro incremento local Sierra/sintéticos quedaría delimitado dentro del experimento principal; no heredaría el título de producto de dos casos terminado.

### Qué acredita el CI verde

Los jobs `linux-py311` y `windows-py314` de #22 concluyeron SUCCESS: [Linux](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/39155882822/job/117758892356), [Windows](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/39155882822/job/117758892118). #21 también está verde según la captura de metadatos.

El workflow existente ejecuta la suite, contratos CLI, verificadores Madrid/Sierra y empaquetado. `pyproject.toml` limita la colección por defecto a `tests/`; las ocho pruebas del probe experimental no forman parte de ese CI y #22 las declara locales. El CI no valida derechos, wireframes, funcionamiento web, dispositivos, usabilidad ni accesibilidad. No se reinterpretará su verde como cierre de R1 o aceptación del producto.

## Fase C: siguiente incremento viable, solo diseñado

### Base positiva de uso y límites

| Material permitido para el alcance local | Base oficial revisada | Condición del incremento |
|---|---|---|
| Sierra BASE 2015, feature `69` | [Catálogo EENNPP 2015](https://www.juntadeandalucia.es/datosabiertos/portal/dataset/limites-de-los-espacios-naturales-protegidos-de-andalucia-eennpp-2015) indica CC BY 4.0 | Conservar atribución, enlace, versión y transformaciones documentadas. |
| Sierra CANDIDATE, edición diciembre 2025 recuperada 2026-10-05 | [WFS RENPA, GetCapabilities](https://www.juntadeandalucia.es/medioambiente/mapwms/REDIAM_RENPA?service=WFS&request=GetCapabilities) declara uso libre y gratuito con reconocimiento de autores y propietarios | Uso local de la feature retenida; conservar condición y proveedor. No asignar por extensión la licencia estándar del catálogo 2015. |
| 52 equipos del inventario fijo recuperado 2026-10-05 | [WFS Patrimonio Natural, GetCapabilities](https://www.juntadeandalucia.es/medioambiente/mapwms/REDIAM_WFS_Patrimonio_Natural?service=WFS&request=GetCapabilities) contiene la misma condición positiva | Uso local de los puntos retenidos con créditos. No presentar una serie histórica 2015–2025. |
| Geometrías y reportes sintéticos | Crear datos originales o usar fixtures sintéticos existentes cuya procedencia se compruebe en el tag | Sin trazado, copia, simplificación ni desplazamiento de geometrías Madrid. Rotularlos como SINTÉTICOS; fijar licencia propia y procedencia. |

En los dos WFS se ha comprobado la condición y el proveedor nombrado, además del [registro científico de Sierra](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/447b17db96f4358ec5e35542d2148c03cd0f5306/docs/GATE_8_SOURCE_REGISTER.md). El GO es una inferencia acotada para revisar localmente esos datos conforme a la condición expresa, **sin decidir derechos de publicación o redistribución del paquete completo**. Si una condición específica del snapshot no conciliable aparece, se retira Sierra del alcance hasta aclararla; el sintético original permite avanzar por separado.

Crédito visible previsto: Fuente: Red de Información Ambiental de Andalucía (REDIAM), Junta de Andalucía. Conservar también el nombre del proveedor/autores que conste en cada registro, sus enlaces, fechas y la explicación de selección/reproyección. La licencia del código permanece diferenciada de cada dato.

### Alcance mínimo propuesto

1. **Paquete local permitido.** Manifiesto explícito con Sierra y escenarios sintéticos; lectura por lista permitida de archivos exactos, sin selector Madrid, importación arbitraria, servicios remotos, telemetría, CDN ni mapa base. Recursos locales y futuro servidor estático ligado a `127.0.0.1`; no puertos publicados. No barrido ni empaquetado del repositorio completo. No copiar el report de Madrid, que contiene geometría derivada, ni ninguna representación geográfica, huella, tesela o captura basada en sus datos.
2. **Mapa BASE/CANDIDATE.** Dos paneles con cámara compartida en escritorio y selector BASE/CANDIDATE en anchuras pequeñas. Polígonos originales CRS84 con IDs; puntos fijos cuya posición no se anima como traslado. Leyenda y tabla separan geometría modificada de relación modificada. Omitir inicialmente `changed_footprint_geometry` EPSG:25830; sus escalares se leen del report con unidades, sin recomputación.
3. **Selección de relaciones.** Lista accesible con clave `(dependent_dataset, dependent_id)`, búsqueda y filtro sin cambiar el total científico. Seleccionar un punto/registro resalta las geometrías referidas por `before[]` y `after[]`, usando exclusivamente joins por IDs. Mostrar arrays completos, incluidos `[]` y multiasignaciones. No ejecutar `within`, nearest, overlays, métricas ni política en el navegador.
4. **Panel de evidencia.** Dataset/ID, predicado, before/after, change_type, ambigüedad de frontera y `evidence_id` solo si existe en la regresión. Un registro unchanged no recibe ID de evidencia inventado. Enlazar el campo/registro exacto del JSON local. PASS/BLOCK, observed y threshold se muestran como constan; ERROR de análisis o fallo de carga/integridad son estados separados sin verdict nuevo.
5. **Procedencia V5.** Hash y bytes de config, BASE, CANDIDATE y dependencias; cinco versiones del motor; identidad de report/Markdown/export ligada a un manifiesto confiable. Comparar bytes antes de interpretar, distinguir verificado/faltante/no comprobado/mismatch; rechazar mezclas, IDs huérfanos, versión no soportada y contradicciones. Fuentes, licencias y fechas son metadatos curados separados: V5 no los prueba ni autentica al editor.
6. **Cero significativo.** Sierra abre con PASS, observed 0, threshold 0, **52 relaciones unchanged**, 40 con `[69]→[69]` y 12 con `[]→[]`; 0 ambigüedades. Cargar los 52 puntos originales y enlazarlos a `relationships`. El GeoJSON de regresiones vacío es válido; mostrar «0 regresiones; 52 relaciones evaluadas». La geometría `69` sí está modificada; el desplazamiento máximo reportado es `368.82509547712834 m`. El filtro de regresiones puede quedar vacío sin ocultar el inventario, el total ni su significado.
7. **Escenarios sintéticos suficientes.** Incluir casos claramente rotulados para assignment_changed/gained/lost, sin cambio, frontera y arrays múltiples; consumir resultados auténticos del CLI fijado fuera del visor. Aprovechar fixtures existentes cuando cubran el caso; cualquier nueva entrada será experimental, nunca una modificación de fixtures canónicos. Casos inválidos/mismatch se crean como copias de prueba del paquete, sin editar evidencia oficial ni fabricar resultados para Sierra. Comprobar también que PASS puede admitir regresiones bajo otro umbral mediante un caso sintético, si ese escenario está disponible.

No debe afirmarse que los equipos existían, estaban abiertos o funcionaban en 2015, ni que PASS demuestra ausencia de efectos reales. Sierra continúa siendo el control negativo reproducible; el resultado histórico MODIFY de Gate 8 permanece porque no se alcanzó su objetivo original de regresiones no nulas.

### Aceptación del futuro incremento

Estos criterios están **pendientes**; no se han implementado ni ejecutado en este encargo.

| Gate | Evidencia mínima para aceptar el futuro prototipo local |
|---|---|
| C0: alcance y derechos | Manifiesto permitido, créditos y condiciones retenidas por fuente; revisión de archivos demuestra cero contenido Madrid y ninguna geometría trazada a partir de él. R1 figura OPEN y el visor completo HOLD. |
| C1: integridad | Sierra conserva sus tres hashes oficiales y entradas V5; joins 52/52; prueba negativa real de hash incorrecto, mezcla de caso, archivo ausente, ID huérfano y V4. Ningún fallo se convierte en PASS/BLOCK. |
| C2: mapa y evidencia | Seleccionar un punto dentro y otro fuera de Sierra; abrir ambos before/after sin inferencia espacial; seleccionar una regresión sintética; comprobar etiquetas BASE/CANDIDATE y rutas CRS. |
| C3: cero y semántica | Ver 52 puntos y 52 registros con export vacío; filtro muestra cero filas de regresión y total 52; primary modified permanece visible; unchanged carece de evidence_id de regresión. |
| C4: navegador y acceso | Navegador real documentado; 1440×900 y 1440×1000, 834×1112, 375×812 y 390×844; reflow 320 px/200%, teclado, foco y lista alternativa, mensajes ES/EN. Capturas solo Sierra/sintéticos; emulación diferenciada de hardware. |
| C5: aislamiento y seguridad | Registro de red sin peticiones externas; acceso solo loopback; cadenas tratadas como texto, rutas del manifiesto acotadas, sin ejecución de contenido, revisión de dependencias fijadas y licencias del renderer. Tamaño/tiempo inicial medidos en entorno declarado, sin SLA inventado. |
| C6: trazabilidad | Cada valor remite al report; filtros no cambian métricas; descargas, si se ofrecen localmente, preservan bytes. Revisión del diff confirma ausencia de cambios científicos y CI existente sigue válido. |

La aceptación local no exige reclutar participantes ni modifica External Validation V1. Una evaluación posterior de comprensión/usabilidad tendría protocolo y participantes separados antes de cualquier afirmación de adopción o accesibilidad certificada.

## Riesgos pendientes y decisión

| Riesgo | Estado y tratamiento |
|---|---|
| R1 INE: licencia y derechos de derivados sin determinar | **OPEN, bloqueante para Madrid y visor completo.** Consulta redactada; cierre solo con evidencia suficiente para ambos snapshots/usos. |
| REDIAM: respuestas mantenidas y alcance de publicación del paquete | Condición positiva constatada para uso local; no extrapolar CC BY 2015 a 2025/2026 ni abrir distribución pública con este GO. Retener evidencia por snapshot antes del futuro uso. |
| Alcance inconsistente entre los dos PR | Matriz identifica discrepancias; #22 principal propuesto, supersesión documental de #21 pendiente. |
| Falso cero, joins incompletos, hashes no confiables o CRS equivocado | Controles C1–C3; gate aún pendiente. Hashes no prueban propiedad ni autenticidad. |
| PASS/BLOCK mal interpretado o causalidad atribuida | Mensajes persistentes, casos sintéticos y límites temporales; comprensión externa no validada. |
| Seguridad, accesibilidad, rendimiento y utilidad | Diseño sin pruebas web ni estudio; C4–C5 y evaluación posterior. CI verde no sustituye estos gates. |
| Contaminar evidencia científica o protocolo CLI | Adaptador independiente, sin recálculo; investigación externa separada y fuentes originales intactas. |

**Decisión responsable:** GO para planificar y, en un encargo posterior, construir el prototipo local aislado Sierra + sintéticos bajo C0–C6. **HOLD para implementar el visor completo de dos casos, incorporar Madrid al paquete visual, publicar o desplegar.** Este informe no levanta ese HOLD ni declara el producto terminado.

Los únicos cambios entregados aquí son este informe, el borrador de consulta y el registro documental de evidencia. Permanecen intactos `src/geoimpact`, algoritmos, CLI, política, fixtures, serialización determinista, contratos científicos, CI y dependencias. No se ha enviado correspondencia, publicado comentarios, modificado PR remotos, hecho merge ni desplegado.
