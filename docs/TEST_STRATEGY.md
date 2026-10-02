# Test strategy — specified before implementation

## Test principles

Tests use hand-authored fixtures in EPSG:25830 unless a CRS test says
otherwise. Fixtures are written in both supported formats where relevant.
Expected JSON is a semantic golden result; numeric values compare within
`1e-9 m` / `1e-9 m²`, not rendered Markdown. Repeated execution must produce
bytewise-identical JSON because V0 contains no timestamps.

Unit tests isolate config, ID canonicalization, preflight, attributes, metric,
predicate, policy, and report ordering. Integration tests exercise full files.
Optional DuckDB prefilter parity tests must prove it cannot change the
Shapely-reference candidate set or result.

## Required acceptance cases

| Case | Fixture/action | Explicit expected outcome |
|---|---|---|
| Identical datasets | Same IDs, attributes, geometry, CRS. | 0 add/remove/modified; empty footprint; 0 relation deltas; all rules PASS. |
| Feature addition | Candidate adds primary ID `C`. | `C` added only; its geometry is footprint contribution; no B/C metric. |
| Feature deletion | Candidate omits `B`; max deletion=0/block. | `B` removed; base geometry in footprint; count 1 vs 0; BLOCK. |
| Attribute-only change | Same valid geometry; a non-ID property changes. | `attribute_modified=true`, `geometry_modified=false`; no relationship scan caused by it. |
| Geometry-only change | Polygon edge shifts 10 m. | Geometry modified; area/Hausdorff/symmetric-difference metrics in metre units; non-empty footprint. |
| ID instability | Same practical geometry has base ID `A`, candidate ID `B`. | Removal plus addition; never matched. Optional diagnostic only. |
| CRS mismatch | Untransformable/mismatched CRS with no compatible analysis CRS. | Analysis error, exit 2, no PASS/WARN/BLOCK. |
| Invalid geometry | Candidate self-intersecting polygon. | Analysis error with ID/reason; never repaired or predicated. |
| Tolerance boundary | Difference exactly `t_m`, then `t_m + 1e-6`. | Exact case unchanged; larger is changed. A metric equal to max threshold passes. |
| Relationship gained | Primary expands across fixed dependency point. | One gained `(dependent, primary, within)` pair with before/after evidence. |
| Relationship lost | Primary shrinks away from fixed dependency point. | One lost relation pair and dependent evidence feature. |
| Reassignment | Madrid fixture below. | Two dependencies lose Chamberi and gain Tetuan; two reassignments. |
| Boundary ambiguity | Dependency lies on candidate shared boundary. | Not within either; intersects true; ambiguity evidence; no arbitrary assignment. |
| Deterministic rerun | Same fixture/config in fresh output folders. | Same status and byte-for-byte JSON/Markdown/evidence. |
| Policy PASS | All measurements <= threshold. | All rules PASS; overall PASS; exit 0. |
| Policy WARN | Only warn maximum exceeded. | WARN evidence; overall WARN; exit 0. |
| Policy BLOCK | Block maximum exceeded. | BLOCK evidence; overall BLOCK; exit 1. |

## Madrid integration fixture oracle

District rectangles cover x=440000..440200 and y=4470000..4470200. BASE has
`Chamberi` x=440000..440100 and `Tetuan` x=440100..440200. CANDIDATE moves the
shared boundary to x=440060. Fixed points: `hotel_813` (440080,4470050),
`hotel_unchanged` (440030,4470050), and `poi_212` (440070,4470150).

Expected: two geometry modifications, each 40 m Hausdorff distance and
8,000 m² absolute area difference; one changed union of 8,000 m²; two
reassignments; four pair deltas (two lost and two gained); and no change for
`hotel_unchanged`. With boundary displacement maximum 30 m and reassignment
maximum 0, exactly two block-rule failures and an overall BLOCK are required.
A point at (440060,4470100) tests ambiguity.

## Non-functional gates

- Fuzz malformed JSON/WKB/Parquet, YAML unsafe tags, duplicate/null IDs.
- Cross-format parity: equivalent GeoJSON/GeoParquet has equal semantic
  results/evidence IDs.
- Metamorphic geometry checks: ring direction, feature ordering, and normalized
  multipart order preserve topological equality; a shift beyond tolerance does not.
- Report manifests Shapely/GEOS, PyProj/PROJ, PyArrow, and engine versions.
- Gate 1 measures fixture runtime/memory; it does not add infrastructure.
