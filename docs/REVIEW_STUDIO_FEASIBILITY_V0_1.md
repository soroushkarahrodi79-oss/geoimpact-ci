# GeoImpact Review Studio — feasibility specification V0.1

**Date:** 2026-10-18  
**Status:** DOCUMENTATION / DESIGN GATE ONLY — conditional GO for an isolated, local read-only proof of concept; HOLD on public product or dataset redistribution.  
**Repository baseline inspected:** `main` @ `c39733b61b60abe3b6e9e9c50f74f5c206022399`; stable executable `v1.2.0`; report contract V5.  
**Scope:** feasibility and accept/reject criteria. **No motor, CLI, test fixture, report-schema, data, or policy modifications. No UI implementation in this gate.**

## 0. Executive decision

**CONDITIONAL GO** to a strictly independent **read-only visual reviewer** that consumes the existing GeoImpact CI output and the already committed source fixtures. It must never become a second geospatial analysis engine. The purpose is to let an unfamiliar GIS analyst see *which declared relationships changed*, distinguish change from consequences, inspect `PASS`/`BLOCK` against the explicit policy, and recover source identities and interpretation limits.

**HOLD** on a publicly deployed demo of the Madrid INE-derived geometry until the documented dataset-specific reuse ambiguity is resolved, and on claims of product adoption, accessibility, or external comprehension until they are independently tested.

This recommendation is an **architectural and documentary inference**, not an executed proof of the new viewer. The existing repository contains a frozen, qualified CLI and two real-case verifiers; the proposed viewer has not been built, benchmarked or user-tested.

## 1. Authoritative source hierarchy

1. Active software: [README](../README.md), [v1 architecture](ARCHITECTURE_V1.md), `src/geoimpact/{models,analysis,artifacts,runner,provenance}.py`.
2. Report contract: [V5 migration](REPORT_V5_MIGRATION.md) and [v1.2.0 release](RELEASE_V1_2_0.md); expected-case V5 reports and digests in `tests/fixtures/madrid_benchmark_expected.json` and `research/sierra-de-baza-2015-2025/gate8_expected.json`.
3. Case selection, methods, attribution and limitations: [Madrid Gate 5](GATE_5_REAL_WORLD_CASE.md), [Madrid source register](GATE_5_SOURCE_REGISTER.md), [Gate 6 benchmark](GATE_6_REAL_WORLD_BENCHMARK.md); [Sierra Gate 8](GATE_8_REAL_WORLD_GENERALIZATION.md), [Sierra source register](GATE_8_SOURCE_REGISTER.md), and both `research/*/README.md`.
4. Existing external-adoption protocol: [External Validation V1](EXTERNAL_VALIDATION_V1_PROTOCOL.md), presently marked **PENDING**; do not treat an authored protocol as participant evidence or contaminate its frozen evaluation.

Historical Gate 0/V0 proposal documents do **not** override the current v1 contract.

## 2. Non-negotiable input and verdict semantics

| Dimension | Current v1.2.0 contract | Review Studio rule |
|---|---|---|
| Primary geometry | BASE/CANDIDATE `Polygon` or `MultiPolygon`; unique nonempty stable string IDs | Display exact supplied polygon records; retain source IDs; never infer renames |
| Dependencies | Fixed `Point` layers; exact GEOS `within` | Do not recalculate assignments or imply that dependent layers changed between editions |
| Input coordinates | OGC:CRS84 GeoJSON; internal analysis EPSG:25830 | Render source GeoJSON as longitude/latitude; never feed projected report geometry directly to a lon/lat browser map |
| Changes | Primary `unchanged/modified/added/removed`; relationships `unchanged/assignment_changed/assignment_lost/assignment_gained` | Keep primary geometry changes and dependent relationship changes as **separate** visual families |
| Boundaries | `touches` is documented separately, not `within` | Preserve `boundary_ambiguities`, including zero; do not style touches as gained/lost membership |
| Verdict | Completed `PASS` = observed regressions within configured threshold; completed `BLOCK` = exceeded threshold; CLI ERROR = exit 2 and **no policy verdict** | Never equate PASS with correct data or BLOCK with real-world damage; never render an input/error failure as a completed BLOCK |
| Interpretation | Geometry/declared relationships only | No administrative intent, resident movement, construction, legal effect, causal harm, usage or operational advice |

The case configurations use threshold `0` as a strict **research probe**, not a default policy recommendation.

## 3. V5 artifact inventory and display feasibility

| Input available to viewer | What it authoritatively supplies | Constraint / design consequence |
|---|---|---|
| `report.json` | `report_version="5"`, `analysis`, `primary_change`, `relationships`, `relationship_regressions`, `boundary_ambiguities`, `policy`, `verdict`, `provenance` | This is the single authoritative source for numbers, classifications, reasons and policy status |
| `report.md` | Human-readable rendering of the report | Optional download/reference, **not** a second calculation or authority |
| `relationship-regressions.geojson` | Point geometries in **CRS84**, with evidence ID, before/after, change type, dependent ID/dataset | Safe to plot as changes after identity consistency check. Contains **only regressions**; in Sierra it has **zero features** |
| `report.json.primary_change.changed_footprint_geometry` | Derived footprint geometry in **EPSG:25830** and measured area | **Do not place directly on a CRS84 map**. Defer overlay until a separately verified *display-only reprojection*, with explicit source/derivative separation |
| Frozen BASE/CANDIDATE GeoJSON files | Original primary geometry at each snapshot, in CRS84 | Supports side-by-side or switch-based visual comparison without recomputing overlay operations |
| Frozen dependency GeoJSON | The fixed point inventory and IDs | Needed to show **unchanged Sierra points**. Join display records to `report.relationships` by declared dataset and dependent ID; absence of change features is not absence of evaluated points |

### Provenance contract

V5 records SHA-256 and raw-byte size for config, BASE, CANDIDATE and dependent files, plus GeoImpact CI, Shapely/GEOS and PyProj/PROJ versions. SHA-256 identifies **exact bytes**, not normalized semantic content, ownership, publisher authenticity or the embedded data itself. A changed whitespace character can change a hash without altering the spatial semantics. The report deliberately excludes paths, usernames, timestamps and machine details.

The viewer may show:
- **Artifact identity verified** only after comparing the loaded raw bytes to the report's V5 hashes.
- **Mismatch / missing / not checked** as separate visible states.
- **Source attribution** from case-specific, versioned metadata, separate from V5 engine provenance.
- The report's actual engine versions, not versions guessed from the browser.

Never describe hash match as proof that a publisher authenticated the data. Keep the exact V5 report unchanged.

## 4. Case A — Madrid, bounded positive regression

**Fixture:** `research/madrid-ine-sections-2024-2025/`; primary `ine_sections`, ID `cusec`, sections 2024 vs 2025; fixed `madrid_portals` points, ID `portal_id`. Result expected under v1.2.0: **BLOCK**, exit 1; **2,112 relationship records**, all `assignment_changed`; 26 observed old→new transition pairs; 1,768 *split-like* and 344 *merge-like* patterns, zero gained/lost, zero boundary ambiguities.

**Correct story:** changing census section geometries changes point-in-polygon assignments of an explicitly selected, frozen set of Madrid portal points. *Split-like* and *merge-like* describe observed geometry/ID patterns, **not** official administrative motivations. The fixture is **not a complete citywide portal inventory**; the point subset was derived around the polygon-change footprint. It is methodologically invalid to extrapolate the 2,112 count to all Madrid.

**UI evidence:** BASE/CANDIDATE polygons, regression points grouped by before→after IDs, selectable point showing precise source ID, `before`, `after`, `change_type`, `evidence_id`; policy status and exploratory zero threshold. A 26-pair filter is a **display of the frozen relationship records** only, not new inference. Labels must use “cambios de asignación espacial”, not displacement of buildings or residents.

**Reuse gate:** INE attribution is required (“Seccionado cedido por el Instituto Nacional de Estadística”), but the dataset-specific license is not established in the existing source register. Madrid Callejero-derived point subset is CC BY 4.0 with Ayuntamiento de Madrid attribution. MIT software licensing does **not** relicense those datasets. Local developer demo is preferable until redistribution rights are reviewed.

## 5. Case B — Sierra de Baza, bounded negative control

**Fixture:** `research/sierra-de-baza-2015-2025/`; one primary stable-ID polygon `69`, 2015 EENNPP vs December 2025 boundary; **52** fixed REDIAM public-use equipment points retrieved **2026-10-05**.

Expected v1.2.0 result: **PASS**, exit 0; **0 regressions**, 52 unchanged relationships, 0 boundary ambiguities, maximum shared-ID boundary displacement **368.82509547712834 m**. Of the 52 points, 40 are within polygon `69` at both states, 12 outside at both states.

**Correct story:** boundary geometry changed, yet no `within` assignment changed for this preselected *2026 fixed point inventory*. It does **not** establish that historical equipment inventories were unchanged between 2015 and 2025, that access is lawful, or that operations were unaffected. The initial Gate 8 research outcome was **MODIFY** because its original nonzero-regression objective was not met, even though this outcome is a valid reproducible negative control.

**Critical empty-state test:** `relationship-regressions.geojson` contains no regression points for this case. The viewer must load `dependencies.geojson`, join the 52 IDs to `report.relationships`, and display the *unchanged* inventory transparently. Never render a blank map or “no data” merely because the regression export is empty.

**Reuse gate:** attribute “Fuente: Red de Información Ambiental de Andalucía (REDIAM), Junta de Andalucía”. The 2015 source catalogue records CC BY 4.0; do not silently assert the same blanket license for maintained 2025/2026 WFS responses. Respect provider naming and documented per-source conditions.

## 6. Product hypothesis and user jobs

**Proposed positioning:** “Inspect geospatial regression evidence before a merge.” Not “predict what a boundary change does”, “measure real-world impact”, or “AI spatial decision engine”.

Initial user jobs:
1. **Inspect:** see exactly what BASE and CANDIDATE cover and which stable primary IDs changed.
2. **Explain:** select a dependent point and read its original before/after assignments and evidence ID.
3. **Discriminate:** distinguish a changed polygon from a changed *relationship*; distinguish PASS/BLOCK/ERROR and missing evidence.
4. **Audit:** find input hashes, runtime versions, source provenance, license and limits without needing the project author.
5. **Reproduce:** follow documented instructions to run the same v1.2.0 CLI and verify frozen artifacts.

This is a hypothesis about usefulness, not demonstrated external demand.

## 7. Minimal V0 interface — intentionally constrained

Suggested information hierarchy:
1. **Case switcher:** Madrid / Sierra, pinned edition dates and “bounded fixture” badge.
2. **Verdict strip:** PASS or BLOCK, observed regression count, **explicit configured threshold** and link to what the verdict does/not mean.
3. **Primary map:** BASE/CANDIDATE switch or synchronized compare. Source polygons in CRS84. Separate toggle for regression points. For Sierra, independently toggle the **52 unchanged inventory points**.
4. **Evidence inspector:** selected polygon stable ID, geometry status; or selected dependency `before`, `after`, predicate, `change_type`, evidence ID (when present), and boundary ambiguity state. Link back to exact report records.
5. **Audit drawer:** five V5 provenance dimensions (config, primary BASE, primary CANDIDATE, dependencies, engine), raw-byte verification results, source attribution, case scope/temporal caveats and reproduction command.

**No** user data upload, GIS editing, runtime LLM, external API, simulation, prognostic score, arbitrary SQL, dashboard of tourism-pressure or new predicate in V0. No inferred “nearest impact”. No rankings. No unverified map-dependent numeric totals. A filter may change the number of **displayed rows**, but the source's original observed count must remain visible and unchanged.

The map engine, sync gestures, performance optimization, basemap source and styling are **implementation choices for the next gate**, not scientific requirements. Avoid publicly transmitted private geometry, uncontrolled tile requests and license/copyright obligations by default.

## 8. Architecture: read-only sidecar, no engine changes

```text
Pinned GeoImpact CI v1.2.0
   └─ existing CLI + frozen config/fixtures
       ├─ report.json (V5; authoritative)
       ├─ report.md (human summary)
       └─ relationship-regressions.geojson (CRS84; changed points)
                           │
   Frozen original BASE / CANDIDATE / dependent GeoJSON (CRS84)
                           │
          [read-only artifact adapter]
            - schema checks
            - compare raw-byte hashes where files present
            - identity joins; fail closed on inconsistent IDs
            - no geometry predicates or scientific recomputation
                           │
             GeoImpact Review Studio V0
             visual map + evidence inspector + audit drawer
```

**Decision:** start as an **independently versioned local static viewer** against a **small, explicit case manifest** that pins report/fixture paths, source credits and edition descriptions. Reuse the existing CLI-produced reports; do **not** reimplement the CLI as JavaScript. No backend or service tokens required for V0.

Do not embed the EPSG:25830 `changed_footprint_geometry` in a browser geographic map without a dedicated transformation qualification. Optional follow-on spike: offline, display-only EPSG:25830→CRS84 reprojection, preserving the authoritative original field and asserting non-scientific display semantics; otherwise **omit footprint polygon overlay** and still provide full BASE/CANDIDATE comparison.

A V4 report must not be silently “upgraded” to V5 or have missing provenance invented. V0 may explicitly **refuse non-V5 reports** with a documented version message.

## 9. Validation gates and measurable acceptance

**F0 — Feasibility (this document):** bounded scope, source mapping, licenses, assumptions, V5 field inventory, UX hypothesis and risks documented. **GO with conditions**. No implementation or new runtime test claimed.

**F1 — Artifact integrity, before UI:** use a clean checkout at tag `v1.2.0`, qualified dependencies, and the repository's existing verifiers:
- `python scripts/verify_madrid_benchmark.py`
- `python scripts/verify_gate8_case.py`
- `python -m pytest`
- `python scripts/verify_release_candidate.py` if release packaging is in scope.

Acceptance: each verifier matches the exact report version, expected verdict and committed output hashes; no canonical byte drift. A `BLOCK` CLI exit **1** is an expected completed verdict and must not be misreported as command failure. Current release notes report 113 passing tests on Linux/Python 3.11 and Windows/Python 3.14, **not independently rerun for this design gate**.

**F2 — Read-only adapter (separate, scoped PR):**
- Reject malformed schema, unsupported version, mismatched raw-byte hashes and missing mandatory case artifacts with explicit user-visible reasons.
- For every regression point in CRS84 export, match its `evidence_id`, dependent dataset/ID, predicate, change type and before/after to exactly one `report.relationship_regressions` record; never manufacture an evidence ID.
- For Sierra, join **52/52** original dependent IDs to `report.relationships`; show zero regressions **and** 52 observed assignments without presenting fabricated regression evidence.
- Show projected report geometry as **unsupported in geographic display** until a separately verified transformation exists.
- Source `verdict`, thresholds and totals only from the loaded report; fail closed on contradictions.

**F3 — Browser/UI verification (separate implementation gate):**
- Reproduce both expected case narratives at 1440×900, 834×1112 and 375×812, documenting browser emulation vs real hardware.
- From the initial screen, users can discover the verdict and its configured threshold; select one dependent relationship; reach provenance/limits without an author-led walkthrough.
- Regression dots, unchanged inventory points and primary geometry states have non-interchangeable symbols/labels; color alone cannot carry meaning.
- Keyboard navigation, visible focus, legible map alternatives, ES/EN terms and an accessible list/table equivalent are tested; do **not** claim WCAG compliance without an appropriate assessment.
- Measure cold start and point-filtering performance on a stated environment, especially the 2,112-point Madrid case; no unmeasured “fast”/“real-time” claims.

**F4 — External usefulness and release (separate decision):**
- Run a **separate** small, preregistered task-based study with independent GIS users; test comprehension of PASS/BLOCK, changed polygon vs changed assignment, and Sierra's meaningful zero.
- Preserve the already-frozen **External Validation V1** protocol for CLI adoption. A new Studio study must not change its evaluated software/docs or expose expected answers to its participants in advance.
- Public deployment remains **HOLD** until Madrid INE reuse is clarified, REDIAM obligations/credits are satisfied, and actual security/accessibility checks are documented.

## 10. Explicit risk register

| Risk | Severity | Control / release consequence |
|---|---|---|
| False equation of BLOCK with harm / PASS with accuracy | Critical | Mandatory policy wording; scenario-based comprehension test; HOLD if misinterpretation remains |
| Projected EPSG:25830 footprint plotted as CRS84 | Critical | No direct plotting; omit until qualified display-only transformation |
| Sierra zero regressions misrepresented as empty/unused dataset | High | 52/52 join from fixed input inventory; regression export empty state explained |
| Mistaken citywide Madrid representativeness | High | “bounded subset selected near change footprint” disclosure; no extrapolation |
| Unresolved INE-specific data rights / REDIAM conditions | High | Local prototype only; public redistribution HOLD |
| V5 hash interpreted as authenticated publisher identity | High | Raw-byte identity vs authentication explained; mismatches fail closed |
| Temporal mismatch of Sierra dependency inventory | High | Show 2015/2025 boundary dates and 2026-10-05 dependency date together |
| Demo contaminates frozen independent CLI-user study | Medium | Separate cohorts/material, versioned protocol and evidence trail |
| Performance / accessibility not tested on real devices | Medium | Provisional design only; measured browser and device gate before product release |
| Feature bloat or duplicated GIS analysis | High | Reader-only scope; no second predicate/geometry engine; one task per new feature |

## 11. Decision, scope of next increment and non-claims

**GO, but only to F1 then F2:** first reproduce the two frozen cases against v1.2.0, then create a read-only adapter and a **minimal local proof-of-concept** in an isolated branch/PR. Keep `src/geoimpact/`, CLI, source fixtures, tests, current releases and report V5 unchanged. No main merge or deployment without independent review.

**HOLD** on a public demo, unlimited user-upload workflow, arbitrary dataset support, runtime AI explanations of evidence, secondary GIS analysis, interpretation of legal/socioeconomic impacts, and institutional product-readiness claims.

**What this audit did not do:** clone or execute the repository locally, install the pinned engine, generate fresh V5 reports, render a new viewer, measure performance, run human studies, verify the publishers' current licenses, or prove a user would understand the proposed design. These are named follow-up tasks, not completed results.

**Proposed next deliverable:** `F1_ARTIFACT_INTEGRITY_GATE.md` with environment, frozen source IDs, exact commands, output SHA-256 matrix, PASS/BLOCK/ERROR interpretation and a GO/HOLD statement for building the reader.
