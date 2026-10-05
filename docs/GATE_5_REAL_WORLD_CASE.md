# Gate 5 — first real-world spatial change case qualification

## Result

**GATE 5 — PASS.** The existing installed CLI was exercised on a real, published
2024-to-2025 census-section transition for Madrid, with a fixed official
municipal address-point inventory as its dependency. It reported actual
`WITHIN` assignment changes and completed with the expected policy `BLOCK`
(exit code 1). This qualifies one bounded case; it does not extend GeoImpact's
GIS capabilities or establish a general performance envelope.

## Qualified case

The primary inputs are the INE annual census-section collections for
municipality `28079` (Madrid), filtered to `TIPO = SECCIONADO` and identified by
`CUSEC`. The annual collections are distinct official versions. The complete
filtered source responses contained 2,450 sections in 2024 and 2,462 in 2025.
Of the 2,443 IDs common to both versions, 30 had geometries that were not
topologically equal; 19 IDs were added and 7 removed. All section geometries
in both snapshots were valid, non-empty `MultiPolygon`s. The returned
GeoJSON coordinates were longitude/latitude (CRS84); GeoImpact transformed
them to the declared analysis CRS, EPSG:25830.

The fixed dependency is the City of Madrid's monthly Callejero resource
“Direcciones postales vigentes con coordenadas geográficas,” filtered to
`Tipologia del numero = Portal`. It has 161,190 records in the retrieved
snapshot, each with a unique official `Codigo de numero`. The source describes
that code as the unique identifier for a numbered location and supplies
geographic coordinates referenced to ETRS89/WGS84. The snapshot was retrieved
on 2026-10-03; its published resource metadata says it was updated on
2026-09-14.

The checked-in files are a deterministic, local subset, not complete city
coverage. The subset keeps all 56 section IDs changed, added, or removed in the
annual pair. Its dependency keeps every portal point intersecting the union of
the 30 same-ID geometry symmetric differences and the full geometries of
added/removed sections. This selects points by the spatial change footprint,
not by the CLI's reported assignment results. It contains 37 BASE polygons,
49 CANDIDATE polygons, and 2,112 unique address points. Coordinates and point
locations are held fixed across the two boundary versions.

## CLI observation

Command, run with the installed `geoimpact` console entry point:

```text
geoimpact analyze --config research/madrid-ine-sections-2024-2025/geoimpact.yml --out <temporary-output-directory>
```

Observed on Windows with Python 3.12.14, GeoImpact 0.1.0, Shapely 2.1.2 /
GEOS 3.13.1, and PyProj 3.7.2 / PROJ 9.5.1:

| Observation | Result |
|---|---:|
| CLI verdict / exit code | BLOCK / 1 (completed analysis) |
| Modified common section geometries reported | 30 |
| Changed-footprint area for reported modified features | 13,463,975.314659253 m² |
| Maximum reported boundary displacement | 2,937.635066209976 m |
| Address-point relationship records | 2,112 |
| Relationship changes | 2,112 `assignment_changed` |
| Distinct old→new section ID pairs | 26 |
| Boundary ambiguities | 0 |

### Transition-type audit

The 2,112 `assignment_changed` relationships were independently audited
against the checked-in BASE/CANDIDATE feature IDs and geometries:

| Transition pattern | Count | Observed ID/geometry pattern |
|---|---:|---|
| Split-like | 1,768 | The old CUSEC exists in both versions and its polygon changes; the destination CUSEC is newly added in 2025. |
| Merge-like | 344 | The old CUSEC disappears in 2025; the destination CUSEC exists in both versions and its polygon changes. |
| Gained / lost | 0 / 0 | No relationship changes were classified as a pure gain or loss. |
| Both IDs retained in both versions | 0 | No transition has both old and new IDs present in both versions. |
| Pure ID-only / renumbering | 0 | No observed transition is a pure ID-only or renumbering case. |

Thus, the observed blast radius is not merely arbitrary CUSEC renumbering:
the audited transitions coincide with changed retained geometries and
added/removed section IDs. “Split-like” and “merge-like” describe only these
observed data patterns. No administrative intention or cause is inferred.

The largest observed address reassignment groups included `2807918058 →
2807918076` (328 points), `2807919053 → 2807919059` (269), `2807908176 →
2807908193` (205), and `2807919054 → 2807919060` (200) / `2807919061` (172).
These are exact `WITHIN` assignment changes under the existing contract, not a
claim that a particular address or service legally changed its electoral or
statistical designation on a particular date.

An independent, full-source exploratory join using Shapely's spatial index
also found 2,112 assignment changes across all 2,450/2,462 sections and all
161,190 fixed points; 197 points had no `WITHIN` section assignment in either
version. That cross-check is not a GeoImpact CLI result. A broader CLI attempt
with 5,480 points in the full change-area polygons and the full section layers
had not completed after about 2.5 minutes and was stopped before producing
artifacts. The checked-in footprint subset is the completed product execution;
it is not evidence that a full-city workload has acceptable runtime.

The exploratory policy threshold in the checked-in config is zero, solely to
make the observed relationship changes produce a visible `BLOCK`. It is not a
recommended production policy. The output directory is not committed.

The three output artifacts from this local run had SHA-256 values under
historical artifact contract V1. Gate 6 introduced report contract V2; these
values remain the Gate 5 observation and are not the active V3 CI expectations:

| Artifact | SHA-256 |
|---|---|
| `report.json` | `164b113a8b1c2d69d2bb309b97461dde7c593dfb64cf22a1d45b7945bee813d5` |
| `report.md` | `e0fd0ab0ccfcd0261dad7a3bb50e9ac6402e6b34a74929a63f413fb081d2ed92` |
| `relationship-regressions.geojson` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |

## Evidence classification

- **Source facts:** INE publishes annual section layers and identifies the
  collection storage CRS as EPSG:25830 and requires a specific attribution;
  dataset-specific license ambiguity is recorded in the source register. The
  Ayuntamiento publishes the monthly address resource, its identifier,
  coordinate fields, CC BY 4.0 license, and update date. Source links and
  licensing details are recorded in
  [the source register](GATE_5_SOURCE_REGISTER.md).
- **Derived observations:** feature counts, geometry validity, IDs, selected
  subset, assignment transitions, measurements, and source/input SHA-256
  values were computed from the retrieved snapshots. The small input files
  are checked in so the CLI observation can be repeated without relying on a
  future live API response.
- **Interpretation:** because INE describes census sections as basic units
  used by many statistical operations and Madrid describes its address
  inventory as a georeferencing resource, section reassignment of fixed
  numbered locations is a meaningful spatial blast-radius example.
- **Unknown:** the source pages do not establish the exact effective dates or
  administrative rationale for every 2024-to-2025 geometry change. The
  address snapshot is from 2026, so the probe asks how the two published
  section versions assign the current fixed address locations; it is not a
  time-aligned historical impact estimate. The probe does not validate legal,
  electoral, or statistical decisions for individual locations. The reason
  197 portal points lack a `WITHIN` assignment was not investigated.

## Reproducibility and limits

The checked-in subset and config have fixed SHA-256 values documented in the
source register. Rerunning the config should return exit code 1 and produce the
same 2,112 assignment-change records with the pinned project dependencies.
Gate 5 did not claim cross-platform canonical hashes for this new dataset.
The project workflow and Gate 4 tests remain unchanged; the full existing suite
was run locally after adding the research record. The longer full-layer CLI
attempt was not a Gate failure, but it limits this qualification to the
bounded checked-in case and flags performance as a separate future question.

No source, analysis, predicate, policy implementation, serialization, evidence
ID, or CI workflow code changed. The only configured predicate remains
`within`; the only analysis CRS remains EPSG:25830. The included subset is
purposefully bounded and should not be presented as a complete assessment of
all address points across Madrid.
