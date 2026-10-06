# Historical V0 scope proposal — not the current product contract

This document preserves a pre-implementation design. Its format, geometry,
predicate, and policy proposals are not current acceptance requirements. The
released v1 contract is documented in [ARCHITECTURE_V1.md](ARCHITECTURE_V1.md)
and [README.md](../README.md).

# V0 scope and relationship regression

## Fixed V0 inputs

Only single-file GeoParquet and RFC 7946 GeoJSON are accepted. A run has one
primary layer in two versions (`base`, `candidate`) and zero or more immutable
dependent layers. Every dataset declares a unique stable ID field. Primary
geometry must be Point/MultiPoint, LineString/MultiLineString, Polygon/
MultiPolygon; dependent geometry follows the same restriction. No file glob,
directory dataset, database connection, download, or inferred layer selection
is part of V0.

V0 evaluates geometry and attribute change, but only geometry changes can
produce relationship regressions. Attribute-only changes are still reported
and can be governed by feature-count policy; they do not make the relationship
engine reclassify a spatial pair.

## Relationship declaration

Each dependency is a stable, fixed dataset and relation definition:

```yaml
dependencies:
  - name: hotels
    path: data/hotels.parquet
    id: hotel_id
    relation: within
    subject: dependency
    target: primary
    boundary: report
```

V0 permits only these semantically explicit combinations:

| `relation` | `subject` | Pair is true when |
|---|---|---|
| `within` | `dependency` | dependent geometry is within primary geometry |
| `contains` | `primary` | primary geometry contains dependent geometry |
| `intersects` | either | the two geometries intersect |

`within` and `contains` are inverse spellings for a simple two-layer
containment test, but both are retained in evidence so configuration reads in
the domain's natural direction. Relations use two-dimensional OGC Simple
Features/GEOS predicates in the same `analysis_crs`; no distance buffering or
near-miss interpretation is hidden in a predicate.

`within`/`contains` do **not** include a dependent geometry lying only on a
primary boundary. `intersects` does. With `boundary: report`, every candidate
pair for which `touches(subject,target)` is true is emitted as an ambiguity
record; it does not itself create a gained/lost containment relationship. V0
has no `covers` rule because choosing boundary inclusion is a business
semantic decision. A future version may add an explicit `covers` relation.

## Evaluation algorithm and delta definitions

For each changed primary feature `p`, construct `U_p = union(p_base, p_candidate)`
from whichever geometries exist. Spatial-index the dependency layer and select
only candidates whose bounding box intersects `U_p`'s bounding box. Evaluate
the configured predicate exactly for every selected dependent feature `d` in
both states. This is an optimization only: the predicate result, not the
bounds, defines membership.

Let `R_before(p)` and `R_after(p)` be sets of tuple pairs
`(dependent_id, primary_id, relation)`. A pair is:

- **gained** iff it is in `R_after(p) - R_before(p)`;
- **lost** iff it is in `R_before(p) - R_after(p)`;
- **unchanged** iff it is in their intersection.

An **assignment** applies to `within`/`contains` where the primary layer is an
administrative partition. For dependent ID `d`, form primary-ID sets
`A_before(d)` and `A_after(d)` across all changed primary features plus any
unchanged primary candidate relevant to the changed feature query. The engine
reports `lost_assignments = A_before - A_after` and
`gained_assignments = A_after - A_before`. An **administrative reassignment**
is present when both sets are non-empty. It is not assumed to be one-to-one:
multiple memberships or zero memberships are reported as ambiguity, not
silently reduced to a label.

To avoid a false negative where a moved boundary reassigns a hotel from a
changed district to an unchanged neighbour, V0 evaluates the full primary
layer for each dependency candidate selected around any changed feature, not
only the changed primary ID. The report still attributes the evidence to the
changed primary feature(s) whose old/new envelope selected the dependent
feature.

An **ambiguous assignment** is any `d` with cardinality other than one in the
before or after assignment set, or a recorded boundary touch. It is a distinct
evidence category; the default policies count it separately from
relationship regressions. If an application needs tie-breaking, it is out of
scope for V0 and must not be invented by the engine.

## Required V0 output

The CLI produces:

- versioned JSON report: full data needed for automation;
- Markdown report: a deterministic reviewer summary generated from JSON;
- optional RFC 7946 GeoJSON evidence layers transformed to CRS84: changed footprint,
  geometry gain/loss, and dependent features participating in a relation delta.

Evidence features carry source IDs, before/after relation sets, change types,
and rule IDs. Evidence is sorted by logical dataset name then canonical ID;
JSON object keys are stable. GeoJSON output is transformed from the analysis
CRS to RFC 7946 CRS84 and the companion report records both CRSs; it does not
use the obsolete GeoJSON `crs` member.

## Deferred, deliberately

Raster; PostGIS; database/network filesystems; Shapefile; network,
accessibility, routing, distance-band, temporal, and raster relationships;
multiple changing layers; web UI/API; Docker/cloud; QGIS/ArcGIS plugins;
automatic risk scoring; AI/LLMs; probabilistic policies; automatic CRS/ID
inference; and Git provider actions/check annotations.

The V0 command is PR-native only in the narrow sense that a CI job can compare
a checked-out base artifact to a candidate artifact, write artifacts, and
return a non-zero code for BLOCK. It does not call a PR API.

## Minimal declarative policy

```yaml
schema_version: 1
analysis_crs: EPSG:25830
geometry:
  coordinate_tolerance_m: 0.0
  footprint_buffer_m: 1.0
  hausdorff_densify_fraction: 0.0
primary:
  name: madrid_districts
  id: district_id
dependencies:
  - name: hotels
    path: data/hotels.parquet
    id: hotel_id
    relation: within
    subject: dependency
    target: primary
    boundary: report
  - name: tourism_pois
    path: data/tourism_pois.geojson
    id: poi_id
    relation: within
    subject: dependency
    target: primary
    boundary: report
rules:
  - id: max_deleted_features
    measurement: removed_primary_feature_count
    operator: max
    value: 0
    unit: features
    severity: block
  - id: max_boundary_displacement_m
    measurement: maximum_hausdorff_distance_m
    operator: max
    value: 30.0
    unit: m
    severity: block
  - id: max_relationship_regressions
    measurement: dependent_assignment_reassignment_count
    operator: max
    value: 0
    unit: dependents
    severity: block
  - id: max_boundary_ambiguities
    measurement: boundary_ambiguity_count
    operator: max
    value: 0
    unit: dependents
    severity: warn
evidence:
  geojson: true
```

The CLI supplies BASE and CANDIDATE primary file paths, so policy identifies
the logical primary layer rather than branch-specific filenames. For `max`, a
rule passes when `measurement <= value`; equality passes. On failure the
configured severity is the result. V0 has only `max` and `min`; values must be
finite and unit-compatible. Rules only reference a versioned measurement
registry, never free-form expressions.

Each JSON rule evidence record includes `rule`, `measurement`, observed
`value`, `operator`, `threshold`, `unit`, `status`, stable `evidence_ids`, and
an optional `evidence_layer`. Thus a verdict always resolves to rule,
measurement, threshold, evidence, and status.
