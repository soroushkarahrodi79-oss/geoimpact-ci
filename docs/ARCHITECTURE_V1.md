# GeoImpact CI — current v1 architecture and contract

Status: current implementation contract, report schema V4. GeoImpact is a
deterministic local geospatial regression tool. Given a BASE and CANDIDATE
primary GeoJSON layer and fixed dependent point layers, it reports which
declared `within` assignments change and applies the configured PASS/BLOCK
policy.

## Supported input model

- GeoJSON `FeatureCollection` input with a required, unique, non-empty string
  stable ID on every feature.
- Primary BASE and CANDIDATE geometries: `Polygon` or `MultiPolygon` only.
- Dependent geometries: `Point` only.
- GeoJSON coordinates are interpreted as OGC:CRS84 and transformed to the
  fixed analysis CRS EPSG:25830. No arbitrary CRS declaration or inference is
  supported.
- Config schema version 1 supports only the documented fields in README;
  unknown fields are rejected.
- Invalid UTF-8/JSON, malformed feature records, unsupported geometry types,
  duplicate or missing IDs, missing/empty/invalid geometry, and unreadable
  files fail with a concise exit-2 error. No policy verdict is produced.

## Primary feature changes

The stable-ID universe is the sorted union of BASE and CANDIDATE IDs. Each ID
is classified as `unchanged`, `modified`, `added`, or `removed`. Shared IDs
with topologically equal geometry are unchanged; other shared IDs are
modified. Candidate-only IDs are added. Base-only IDs are removed. No identity
or rename is inferred across IDs.

The primary footprint contributions are:

- modified: symmetric difference of BASE and CANDIDATE geometry;
- added: full CANDIDATE geometry;
- removed: full BASE geometry.

Contributions are unioned deterministically after applying the existing
`CHANGE_FOOTPRINT_GRID_SIZE_M = 1e-6` grid to derived overlay operations. This
precision grid is a representation and robustness model, not source positional
accuracy. Source geometries are not mutated.

Maximum boundary displacement is computed only for modified shared IDs using
the existing one-micrometre measurement grid. Added and removed IDs have no
counterpart and therefore produce no displacement pair. If no shared ID is
modified, displacement is `0.0` even when IDs were added or removed.

## Relationship engine

For every fixed dependent Point, the engine independently computes exact GEOS
`within` assignments against BASE and CANDIDATE polygons. STRtree envelope
queries shortlist candidates only; exact predicates determine assignments.
The result is `unchanged`, `assignment_changed`, `assignment_lost`, or
`assignment_gained`, based on the before/after stable-ID lists. Adding or
removing a primary ID has no special relationship shortcut and cannot imply a
rename. Exact boundary touches are reported separately and do not count as
`within`.

## Report and compatibility

Internal module boundaries use explicit standard-library type contracts for
the stable configuration, analysis, policy, evidence, and report structures.
These annotations describe the existing dictionaries; they do not change the
serialized or public contract.

V4 retains the V3 top-level sections and relationship semantics. Its
`primary_change` section includes `feature_geometry_status`,
`changed_feature_ids`, `added_feature_ids`, `removed_feature_ids`,
`modified_feature_ids`, `changed_footprint_area_m2`,
`changed_footprint_geometry`, and `max_boundary_displacement_m`. V3 had status
and footprint data only for shared IDs; V4 expands that section to represent
the complete primary ID universe. See [REPORT_V4_MIGRATION.md](REPORT_V4_MIGRATION.md)
for the migration rationale and canonical output implications.

JSON is canonical and is the source for Markdown and relationship GeoJSON.
Output IDs and records are sorted deterministically under the pinned runtime
dependencies. PASS means the configured regression threshold was met; BLOCK
means it was exceeded; ERROR means analysis did not produce a verdict.

## Out of scope

The implementation does not support GeoParquet, rasters, PostGIS, other
predicates, arbitrary CRS handling, simultaneous dependent-layer transitions,
automatic repair, inferred IDs, scoring, WARN policy, an API, or a web UI.
Historical Gate and V0 documents remain records of earlier proposals and
development decisions, not current product requirements.
