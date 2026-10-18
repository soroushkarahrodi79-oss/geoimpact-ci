# Product design — proposed, not implemented

**Status: design under HOLD.** Wireframes are illustrations, not screenshots
or tested interfaces. Any numbers shown below come from the reproduced
reports; abstract map placeholders are not real geography.

## Job, audience and information hierarchy

A spatial-data reviewer needs to answer: which declared relationship changed,
which retained inputs produced it, and why did the configured policy block?
The primary surface is a review workspace, not a KPI dashboard or risk score.
The audience is GIS analysts, spatial-data engineers and research reviewers.

1. Header: GeoImpact Review Studio; case selector; ES/EN control; read-only
   experiment label and software/report versions.
2. Case context: source snapshot dates, fixed-dependency retrieval, retained
   subset badge, input identity status and source attribution link.
3. Verdict: report token PASS/BLOCK, observed regression count and threshold,
   with an immediately visible interpretation sentence.
4. Review workspace: BASE/CANDIDATE maps and a relationship list. Selection
   connects both maps to before/after ID arrays and evidence detail.
5. Evidence panel: stable/evidence IDs, original scalar values, exact files,
   configuration, raw-byte identities, engine versions and curated limitations.

No generic charts, confidence gauges, scores, trend lines, inferred winners,
forecasting or AI explanations. The only changes to numbers are explicit
locale formatting and display rounding with original value available.

## Layout and visual direction

| Layout target | Proposed behavior |
|---|---|
| Desktop 1440 × 1000 CSS px | Two synchronized map panels occupy the main area; 340 px evidence column; paginated relationship table below. Case context and verdict stay above map controls. Sidebar has its own clear heading; no tiny floating panels over geometry. |
| Tablet 834 × 1112 CSS px | Full-width paired maps remain visible with shared controls; evidence and relationships stack below. No drag-only drawer or hover prerequisite. At narrow widths the same single-map snapshot switch as mobile is available. |
| Mobile 390 × 844 CSS px | One map with native BASE/CANDIDATE segmented buttons, shared camera and fixed snapshot label. Review / Relationships / Evidence anchors stack in document order. Scrolling is native; no horizontal page overflow, trapped map gestures or permanent overlay consuming the viewport. |
| 320 CSS px / 200% zoom | Single-column reflow; arrays and hashes wrap or expand; table becomes a semantic list of relationships; controls remain reachable and labels visible. Exact raw files remain downloadable. |

Direction: deep navy header (#122B39), paper background (#F3F6F4), dark text
(#183542), teal action accent (#166B61); amber/red is reserved for policy or
integrity language. System fonts only, no remote imagery. Restrained borders,
legible 16 px body text, 12 px spacing rhythm, explicit BASE/CANDIDATE labels.
Colour tokens are design choices; no WCAG compliance is claimed before tests.

Geometry encodings: BASE blue solid outline; CANDIDATE purple dashed outline;
primary statuses use a labelled legend: modified, added, removed, unchanged.
Regressions use a distinct point symbol plus text label; unchanged dependents
remain optional context. Boundary ambiguity is a separate labelled point style
and never counts as within. A point is fixed in space: switching snapshot
changes its membership label, never animates a physical relocation. Selection
outlines both the relevant primary IDs and the dependent point, without
recomputing containment.

The initial design does not draw the report's projected footprint geometry.
Show its reported area as a scalar with units and a notice that footprint
visualization is unavailable in this version. Never shade an invented impact
area. No basemap by default: say “retained vector subset; no basemap” so blank
context is not mistaken for missing loading tiles. Attribution is always
available below each map and in the source panel.

## Five review journeys and acceptance criteria

These are implementation requirements, **not completed tests**.

| Journey | Intended interaction | Measurable acceptance |
|---|---|---|
| J1 / understand a case | Select Madrid, read dates/subset and verdict | Report token BLOCK, observed 2,112, threshold 0 match JSON; interpretation text visible before opening a panel; no claim about all Madrid or dataset validity. Switching to Sierra shows PASS/0/0 and all 52 fixed records, including 12 unassigned in both states. |
| J2 / locate a transition | Search exact dependent ID, select list row | Madrid `portal_id=11007821` shows before `[2807901124]`, after `[2807901123]`; the same fixed point is highlighted on both views and the corresponding original primary IDs are selected. Evidence ID is complete and matches both artifacts. No hover required. |
| J3 / compare geometry | Fit case, pan/zoom, switch snapshot on narrow screen | Shared camera makes the same point occupy the corresponding location; BASE/CANDIDATE labels remain visible. Added features occur only in CANDIDATE and removed only in BASE, as recorded. Geometry status is not inferred in JS. Selecting the Sierra modified ID `69` never invents a regression despite changed geometry. |
| J4 / audit a result | Open Evidence → Inputs / Configuration / Sources | Exact source hashes, sizes, YAML bytes, report version and five engine versions are reachable; each displayed scalar traces to a JSON field. Attribution and source snapshot/retrieval dates are labelled as curated metadata. Downloads preserve bytes. Full arrays and IDs are available without truncation. |
| J5 / handle missing or inconsistent evidence | Load a bad/unsupported bundle or inspect empty evidence | Wrong hash, missing original, unknown V5 field contract/CRS, mixed-case manifest or orphan ID prevents normal review with “Evidence unavailable / Evidencia no disponible”, distinct from verdict. Sierra empty regressions show “0 changes; 52 fixed records reviewed” rather than loading/error. Missing scalar/geometry never becomes zero or guessed extent. |

Other essential controls: zoom +/−, fit all, fit selection, show all versus
regressions, point/primary layer toggles and accessible result pagination.
Filtering only reduces displayed rows; total and filtered counts are separate.
No threshold sliders, reclassification controls, editable source geometries,
approval/merge buttons or “accept dataset” actions.

## Evidence panel and unavailable information

| Panel | Fields and provenance |
|---|---|
| Relationship | `dependent_dataset`, `dependent_id`, `predicate`, `before[]`, `after[]`, `change_type`; regression `evidence_id` if present, otherwise explicit “no regression evidence ID”. |
| Geometry | Status from `primary_change.feature_geometry_status`; ID lists; `changed_footprint_area_m2`; `max_boundary_displacement_m` with “modified shared IDs only”. Exact scalar in expandable raw-value view, rounded display marked. |
| Policy | `rule`, `observed_value`, `threshold`, `status`, `evidence_ids`; report `verdict` unchanged. No browser verdict recomputation. |
| Inputs | V5 `hash_algorithm`, `inputs.*.sha256`, `size_bytes`; original BASE/CANDIDATE/dependency/config downloads with manifest identity status. |
| Versions | Report V5 and `provenance.engine.{geoimpact_ci,shapely,geos,pyproj,proj}`; do not invent OS, Python version, timestamp or run duration from V5. |
| Sources / limits | Pinned registers, provider links, required attributions, snapshot/retrieval dates, subset recipes, dependency temporal mismatch, source-data terms distinct from MIT. |
| Not available | Per-feature displacement, location of maximum displacement, legal effect, population affected, source accuracy, confidence, causal attribution, inferred renaming/splitting intent, historical equipment use. No placeholder numbers. |

## Accessibility and keyboard contract

- Skip link to review workspace; landmarks, ordered headings and native form
  controls. Case selector and language control have visible labels.
- All map functions have labelled buttons and a list-based equivalent. Tab
  enters/exits map without a trap; arrows pan only while map control has
  explicit focus; +/− zoom; Escape clears selection and returns focus to the
  invoking row/button. Preserve normal page scrolling otherwise.
- Enter/Space selects a relationship row through its button; selected state
  is exposed accessibly and announced in a polite live region. Keep reading
  order independent of screen position. Do not make 2,112 map points Tab stops.
- Lists/rows expose before/after arrays as text. Multi-assignment arrays are
  supported; an empty array is “no within assignment”, not an absent record.
  Do not rely on a visual map, colour, tooltips or pointer gestures alone.
- Focus indicator, text contrast ≥4.5:1, large text and non-text controls
  ≥3:1, target size design goal ≥44 × 44 CSS px. Verify measured tokens,
  reflow, zoom, reduced-motion and screen-reader behavior after implementation.
- Single-map BASE/CANDIDATE controls expose selected state. Preserve selection,
  camera, pagination and focus across language/layout changes where possible;
  changing case clears obsolete IDs and announces the new context.
- Loading, unsupported, missing and integrity-failed are explicit states;
  errors receive a heading and actionable file name without local system paths.
  Unavailable displays do not hide their error behind a PASS badge.

## ES/EN text contract

Verdict tokens, IDs, hashes and source proper names stay unchanged. The initial
future implementation should localize controls, state messages, units/context
and interpretation text, with `html[lang]` and locale-aware display numbers.
Raw artifacts keep their original language and bytes.

| ES | EN |
|---|---|
| Revisión de relaciones espaciales | Spatial relationship review |
| Experimento · solo lectura | Experiment · read only |
| Subconjunto retenido; no representa todo Madrid | Retained subset; does not represent all Madrid |
| BASE / CANDIDATE · inventario de referencia fijo | BASE / CANDIDATE · fixed reference inventory |
| BLOCK: el análisis terminó y superó el umbral configurado | BLOCK: analysis completed and exceeded the configured threshold |
| PASS: la política configurada no bloqueó las regresiones observadas | PASS: the configured policy did not block the observed regressions |
| El resultado no acredita la corrección de los datos ni efectos reales | The result does not establish data correctness or real-world effects |
| Evidencia no disponible; no se puede revisar este paquete | Evidence unavailable; this bundle cannot be reviewed |
| Identidad de bytes coincidente con el manifiesto retenido | Byte identity matches the retained manifest |
| Sin cambios de relación en los 52 registros de referencia | No relationship changes in the 52 reference records |
| Sin asignación within | No within assignment |
| Huella cartográfica no disponible en esta versión | Footprint map overlay unavailable in this version |
| Geometría modificada; no implica una relación alterada | Modified geometry does not imply an altered relationship |

## Scope of wireframes

[Desktop](design/desktop.svg), [tablet](design/tablet.svg) and
[mobile](design/mobile.svg) illustrate layout, hierarchy, case facts and
honest empty/unavailable states. Abstract map areas deliberately contain no
INE-derived coordinates. They have no working controls and do not establish
responsiveness, accessible behavior or usability. Those are future
implementation gates, not properties proven by these drawings.
