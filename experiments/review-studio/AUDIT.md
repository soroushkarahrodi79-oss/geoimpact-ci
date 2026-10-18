# Feasibility audit and architecture decisions

Audit date: 2026-10-18. Baselines and scope: [README](README.md).

## Decision and release verification

**GO for static technical feasibility. HOLD for the requested two-case viewer.**
The blocker is unresolved Madrid geometry reuse conditions, not a missing
spatial capability. No claim is made that reuse is prohibited: available
records do not settle the condition sufficiently to clear the user's gate.
No permission request or legal determination is substituted for evidence.

GitHub's [v1.2.0 release](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/releases/tag/v1.2.0)
is published, non-draft and non-prerelease (2026-10-06). The annotated tag
peels to `45237d7caaea2aa4b81359e46f1623918645078c`. The release-tag file
`docs/RELEASE_V1_2_0.md` still contains unchecked preparation tasks; the
published release and actual tag establish release existence. It would be
incorrect to treat those historical unchecked boxes as an unreleased version.

Current contract sources inspected: release README,
`docs/ARCHITECTURE_V1.md`, `docs/REPORT_V5_MIGRATION.md`,
`src/geoimpact/{models,artifacts,evidence,provenance,geometry_change,relationships,policy,contract}.py`,
synthetic fixtures, both research cases, expected manifests, source registers,
NOTICE and reproducibility verifiers. Current main's README, coherence/adoption
record and External Validation V1 protocol were checked separately.

## What the files actually offer

| Retained artifact | Available information | Missing information / display consequence |
|---|---|---|
| `report.json` | Authoritative report V5; analysis CRS, dataset and ID-field names, predicate; per-primary-ID statuses and changed/added/removed/modified ID lists; footprint geometry and area; max displacement; all fixed-dependent before/after memberships; regressions with evidence IDs; boundary ambiguities; configured policy, observed count, threshold and verdict; raw-byte input hashes/sizes and five engine versions | Does not embed full original BASE/CANDIDATE or all dependent coordinates, source URLs, dataset dates, licenses or causal explanations. Its embedded geometry is EPSG:25830, not web-map longitude/latitude. No per-feature displacement or max-displacement location. |
| `report.md` | Existing human-readable rendering: verdict, primary counts/IDs, scalar metrics, regression detail and provenance | Not a second scientific result or a complete context dataset; does not replace the all-relationship array. Link/download exact bytes; do not parse it for UI values or implement another competing report. |
| `relationship-regressions.geojson` | CRS84 Point features for changed fixed-dependent relationships, with evidence ID, composite dependent identity, predicate, before/after IDs and change type | No BASE/CANDIDATE polygons, footprint polygons or unchanged dependents. A regression point is not a location where a boundary moved and is not a polygon of impact. Sierra's empty FeatureCollection is valid evidence, not a failed load. |
| Original BASE/CANDIDATE GeoJSON | Complete geometry **within each retained subset**, stable IDs and available source attributes, CRS84 coordinates | No full Madrid inventory; no scientific result can be inferred by matching outlines or ID proximity. Join report statuses using declared primary ID field. |
| Original dependent GeoJSON | Fixed CRS84 Point coordinates and IDs, including unchanged/unassigned points omitted from the regression GeoJSON | Not a pair of temporal dependent snapshots. Join on `(dependent_dataset, dependent_id)`, never ID alone across datasets. |
| Original YAML | Exact analysis declaration and source filenames, ID fields, predicate, threshold, severity | Raw bytes matter for V5 hash. Resolved local paths are not report provenance; avoid exposing machine paths. Never turn a display control into an implicit policy edit. |
| Source registers and case READMEs | Human-curated source dates, provider attribution, selection recipes, reuse conditions and interpretation limits | Not supplied by V5. Carry as explicitly curated case metadata linked to the pinned registers, not invented engine output. |

Report geometry coordinates are serialized to 6 decimal places in projected
metres; relationship GeoJSON coordinates to 8 decimal places in degrees.
Scalar scientific measurements retain their report values. These are
representation rules, not survey accuracy. The footprint and boundary
measurement use documented 1e-6 m grids; a UI must not label this as precision
of the source cartography.

Hashes establish byte identity relative to a retained trusted manifest. They
do not authenticate the publisher, prove source accuracy, establish permission,
or prevent someone replacing both a file and its untrusted manifest. V5 does
not lock inputs during analysis. Evidence IDs identify relationship semantics;
they are not a signature of source geometry or a confidence score.

## Reproduced cases (observed, not invented)

| Observation | Madrid | Sierra de Baza |
|---|---:|---:|
| BASE / CANDIDATE primary features in retained subset | 37 / 49 | 1 / 1 |
| Modified / added / removed primary IDs | 30 / 19 / 7 | 1 / 0 / 0 |
| Fixed dependents / relationship records | 2,112 / 2,112 | 52 / 52 |
| Relationship regressions | 2,112 | 0 |
| Boundary ambiguities | 0 | 0 |
| Policy threshold / observed | 0 / 2,112 | 0 / 0 |
| Recorded verdict / CLI exit | BLOCK / 1 | PASS / 0 |
| Maximum displacement, modified shared IDs only (m) | 2937.635066605893 | 368.82509547712834 |
| Recorded footprint area (m²) | 13463975.784613162 | 2003072.010849763 |
| Report JSON bytes | 2,303,114 | 837,612 |
| Regression GeoJSON bytes | 1,228,043 | 52 |
| All original input bytes including YAML | 480,834 | 327,163 |

The probe reads the scalar values above. It does not recalculate them. Output
SHA-256s match the release's frozen expected manifests for all six real-case
artifacts; full observations are in [evidence-summary.json](evidence-summary.json).
All relationship records join to retained dependent IDs and before/after
primary IDs. Geometry presence and identity joins are sufficient for a future
cartographic surface; rendering performance remains untested.

Madrid's 26 transition pairs and split-like/merge-like pattern counts already
exist in the Madrid verifier/manifest. They are **case-specific benchmark
annotations**, not generic V5 classifications or inferred administrative acts.
They should not become generic UI badges. The deterministic Madrid subset
selects points in a derived footprint; its 2,112/2,112 rate is not a city-wide
impact proportion. Sierra has 40 fixed points within in both versions and 12
unassigned in both, per its frozen transition histogram. None of the 52
changes membership; none of this proves equipment operated in 2015.

A small existing documentation discrepancy is preserved, not silently fixed:
Madrid's case README says 391 config bytes / 480,835 total; actual frozen config
and V5 provenance are 390 / 480,834. The source-register hash and output hashes
match. The display must use verified bytes, with source notes separately labeled.

## Rights and source gate

| Source | Existing retained basis | Experiment decision |
|---|---|---|
| INE Madrid sections 2024/2025 | `docs/GATE_5_SOURCE_REGISTER.md` and case README require the INE attribution and explicitly say to confirm licensing before broader redistribution; no settled dataset-specific license | **R1, blocking.** Do not copy polygons/derived footprint into a web bundle, publish map screenshots, or relabel the data MIT. |
| Ayuntamiento Madrid portals, fixed 2026-10-03 retrieval | CC BY 4.0 in Madrid register; retain Ayuntamiento attribution and source link | No new blocker established by repository audit; remains subject to recorded terms and subset/temporal limitations. |
| REDIAM EENNPP 2015 | Register records CC BY 4.0 and Junta/REDIAM attribution | Retain source and derived-data labels. |
| REDIAM latest boundary and fixed equipment retrieval 2026-10-05 | Register records WFS free-use condition with authors/owners named; no separate standard license is asserted for these responses | Preserve that exact conditional basis; do not mislabel 2026 data with a different 2016 catalog license. No new blocker established by repository audit. |

Official INE pages checked on 2026-10-18:

1. [2024 collection page](https://www.ine.es/geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01:Secciones_2024): identifies the collection, schema and EPSG:25830 storage CRS; footer labels the site/content CC BY-SA 4.0.
2. [Service collection index](https://www.ine.es/geoserver/ogc/features/v1/collections?f=text%2Fhtml): free service access conditional on the specified INE attribution.
3. [General INE legal notice](https://www.ine.es/dyngs/AYU/es/index.htm?cid=125): general CC BY 4.0 for INE-origin statistical information unless otherwise specified; requires attribution, dates where present and no implied endorsement.
4. [OGC API technical guide, December 2025](https://www.ine.es/geoserver/www/guias/OGC_API_Feature_Seccionado.pdf): describes access and client integration. Its fully retrieved text does **not** contain the private-use wording returned by an initial search snippet; that snippet is not relied on for the decision.

The general notice and the service footer are different labels. This audit
does not decide which governs these exact derived geometry snapshots. The
technical ability to access them, required attribution and their presence in
the repository do not resolve the recorded redistribution ambiguity. This is
a project evidence gate under the user's rule, not a finding of unlawful use.
The other sources were assessed against pinned registers; no claim is made
that every current upstream license page was independently revalidated.

R1 closes when a retained publisher clarification or authoritative,
dataset-specific terms establish the applicable reuse/display/redistribution
basis for both original snapshots and their derived subset, including any
share-alike obligations. Record URL or permission document, scope, date,
conditions and attribution; update case metadata in a subsequent reviewed
change. No messages to INE were sent. Removing Madrid requires an explicit
change to the requested scope rather than calling the two-case product done.

## Existing versus new

Existing: deterministic primary diff, full before/after relationship evidence,
PASS/BLOCK evaluation, Markdown rendering, point evidence, V5 identities,
Madrid benchmark, Sierra exhaustive negative control, release verification,
and an unexecuted External Validation V1 adoption protocol. Reuse them.
`docs/PRODUCT_SPEC.md` and `docs/ARCHITECTURE.md` are historical proposals;
WARN, extra predicates and GeoParquet there are not current capabilities.

New proposed work only: synchronized map navigation; declared-ID selection;
status styling; accessible relationship list and exact evidence detail;
source/config/version disclosure; explicit integrity failure states; local
language switching. No existing web UI/API was found. This experiment does
not run or amend External Validation V1, recruit evaluators, or report human
research; a Studio study would need a separate later protocol.

## Architecture decisions (proposed, not implemented)

| ADR | Decision and reason |
|---|---|
| A1 / boundary | Keep a standalone static directory, no import into `src/geoimpact`, no CLI changes, Python packaging changes, policy controls or automatic deployment. No runtime engine, backend, API, LLM, analytics or required third-party service. |
| A2 / bundle | After R1, prepare a case manifest with pinned report and artifact hashes, exact source bytes, curated source metadata and attribution. Build-time validation fails on missing files, wrong bytes, schema or unresolved rights. Original inputs stay unchanged. This manifest is a Studio package contract, not a V6 engine report. |
| A3 / renderer | Prefer vendored OpenLayers for independent vector sources, a shared view, pan/zoom, MultiPolygon holes and fixed-dependent Points. Preserve its license; pin exact version and review size/security before adding it. No CDN, remote fonts or required basemap. A custom SVG map would reduce download dependencies but add projection, navigation and accessibility maintenance. No library has been added here. |
| A4 / projection | Use original CRS84 input features and CRS84 regression GeoJSON for initial maps. Project for display only; never calculate assignments, topology, unions, buffers or metrics in JS. Report footprint is projected EPSG:25830: omit its overlay initially and disclose why. A later display-only reprojection of that geometry requires a separately tested adapter; do not treat projected coordinates as lon/lat or recompute a footprint from outlines. |
| A5 / interpretation | Primary geometry modification and relationship regression remain separate concepts and layers. Render exact report verdict and threshold; show integrity/load failures independently, never as PASS. An empty regression collection remains a valid empty state. |
| A6 / integrity | SHA-256 and byte-size checks bind supplied input bytes to V5; a trusted bundle manifest binds report/Markdown/GeoJSON. Validate IDs, field names and supported geometry/CRS before rendering. Fail closed on mixed cases, unknown schemas, missing inputs or inconsistent evidence. Do not silently accept V3/V4 as V5. Use textContent for input strings and plain-text Markdown download; no raw HTML or remote URL loading. |
| A7 / scale and offline | Retained bundles are roughly 4.32 MB (Madrid) and 1.17 MB (Sierra), uncompressed inputs plus outputs. Load one case at a time, paginate relationship rows; do not truncate evidence. Suitable scale for a static experiment, not a benchmark or SLA. Serve through any static HTTP server; Python used to serve files locally is not an application backend. Offline-after-download depends on all vendored assets being retained; no file:// or service-worker claim yet. |
| A8 / audit | Keep raw files downloadable with exact bytes; preserve IDs and language-independent verdict tokens; label display rounding and curated dates. Do not persist reviewer judgments into scientific artifacts. No authoring, repair, reanalysis, approvals or merging from the UI. |

## Professional value and risk

The useful task is a release reviewer tracing a declared assignment transition
from a point and stable IDs to the policy and exact source version. Sierra is
the necessary counterexample: visibly different outlines with PASS can teach
why geometric change alone is not relationship impact. A screenshot portfolio
without that distinction would weaken the project.

| Risk | Priority | Control / evidence still needed |
|---|---|---|
| Unsupported data redistribution | P0 | R1 must close before the requested two-case implementation. |
| Interpreting BLOCK as incorrect data, or PASS as safety/validity | P0 | Persistent exact semantics beside verdict; task-based interpretation study pending. |
| Plotting report EPSG:25830 as geographic coordinates | P0 | Source-specific CRS routes, unit tests, known geometry extents and browser inspection before implementation release. |
| Partial subset described as Madrid-wide; dates mistaken for current facts | P0 | Persistent subset and fixed-reference snapshot disclosure. |
| Missing/incorrect joins, mixed reports or tampered inputs | P0 | Trusted artifact hashes, V5 input identities and composite-ID joins; probe verifies retained cases only. |
| Motion/colour/hover-only interaction excludes reviewers | P1 | Accessible list equivalents and keyboard/zoom tests; design requirements are not evidence of compliance. |
| Duplicating the engine or implying causal/admin conclusions | P1 | No new spatial computations, scores, policy decisions, inferred splits or renames. |
| Time invested without adoption evidence | P1 | Time-box later implementation; judge by evidence-tracing task success, not visual polish or feature count. |

No measured improvement in review speed, usability, accessibility, scientific
validity, device performance or adoption is claimed. Those require the later
implementation and evaluation gates in [VALIDATION](VALIDATION.md).
