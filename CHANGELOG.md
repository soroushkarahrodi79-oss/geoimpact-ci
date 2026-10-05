# Changelog

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
- No repository-wide software license has yet been declared.
- Results do not establish source correctness, legal meaning, administrative
  intent, causality, or real-world harm.
