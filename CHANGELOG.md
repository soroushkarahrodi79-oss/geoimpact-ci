# Changelog

## 1.1.0 — 2026-10-06

Correctness-hardening release for the narrow v1 contract. The CLI and config
shape remain compatible; the report schema advances from V3 to V4 so consumers
should continue branching on `report_version`.

### Added

- First-class primary stable-ID statuses for `added` and `removed` features,
  alongside `unchanged` and `modified`.
- Complete primary change footprints: added features contribute candidate
  geometry, removed features contribute base geometry, and modified features
  contribute their symmetric difference.
- Explicit V4 primary-change ID lists for added, removed, and modified features.
- Current implementation architecture documentation and a V3-to-V4 migration
  record.

### Fixed

- Maximum boundary displacement is now defined only for modified stable IDs
  present in both snapshots; added/removed-only transitions report `0.0`.
- Expected malformed GeoJSON, invalid UTF-8, unreadable inputs, malformed
  features, unsupported geometry types, duplicate or missing IDs, and invalid
  geometries fail closed as controlled input errors.
- FeatureCollection members must explicitly declare `"type": "Feature"`.
- Unknown YAML contract fields are rejected instead of being silently ignored.
- Custom primary dataset names are preserved through analysis, relationship
  evidence, and reports.

### Reproducibility

- Report contract V4 preserves deterministic serialization and the existing
  one-micrometre footprint/displacement precision models.
- Synthetic, Madrid, and Sierra V4 hashes are verified across the hosted
  Linux/Python 3.11 and Windows/Python 3.14 matrix.
- Relationship-regression GeoJSON hashes remain unchanged from V3 for the
  existing qualification cases.

### Research validation

- Madrid still records 2,112 relationship changes across 26 transition pairs,
  with zero gained/lost assignments and zero boundary ambiguities; V4 also
  records 19 added, 7 removed, and 30 modified primary IDs.
- Sierra de Baza remains a negative control with 52 relationships, zero
  regressions, zero boundary ambiguities, and maximum displacement
  368.82509547712834 m.

### Compatibility

- Existing v1 YAML configuration remains version 1 and the CLI contract remains
  `PASS=0`, `BLOCK=1`, `ERROR=2`.
- Report consumers that assume V3 primary-change semantics must inspect
  `report_version`; V4 expands the primary-change section to the complete
  stable-ID universe.
- Scope remains intentionally narrow: GeoJSON Polygon/MultiPolygon primaries,
  Point dependencies, EPSG:25830 analysis, and exact `WITHIN` relationships.

## 1.0.0 — 2026-10-05

First stable, reproducible research-demonstrator release. This version freezes
the current narrow v1 behavior; it does not claim universal GIS production
readiness.

### Added

- BASE/CANDIDATE polygon GeoJSON comparison with required stable IDs in
  EPSG:25830.
- Deterministic change-footprint and maximum-boundary-displacement evidence.
- Fixed dependent point relationship analysis using exact `WITHIN`, with
  boundary `TOUCHES` reported separately.
- PASS/BLOCK policy results and JSON, Markdown, and GeoJSON artifacts.
- Reproducible synthetic, Madrid positive, and Sierra negative-control checks.
- Package wheel and source-distribution qualification in the Linux/Windows CI
  matrix.

### Performance

- STRtree candidate filtering preserves exact GEOS predicate evaluation. A
  controlled synthetic large workload measured 114.25× median speedup; this is
  not a general runtime guarantee.

### Reproducibility

- Report contract V3 declares the footprint precision and separate displacement
  measurement precision at `1e-6 m`.
- Canonical synthetic, Madrid, and Sierra output hashes are checked in CI.

### Research validation

- The bounded Madrid benchmark records 2,112 assignment changes across 26
  transition pairs.
- The Sierra de Baza negative control records 52 unchanged relationships and
  zero regressions.
- Research fixtures preserve source-specific attribution and limitations.

### Limitations

- EPSG:25830, GeoJSON, stable IDs, and the `WITHIN` relationship contract only.
- GeoImpact CI software is MIT-licensed; research fixtures retain their
  source-specific attribution and reuse terms.
- Results do not establish source correctness, legal meaning, administrative
  intent, causality, or real-world harm.
