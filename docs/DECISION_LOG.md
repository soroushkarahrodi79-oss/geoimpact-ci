# Gate 0 decision log

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-001 | Analyse a dataset transition, not an isolated dataset. | Accepted | Distinct from validation and contracts. |
| D-002 | Require declared stable IDs; never fuzzy-match renames. | Accepted | Adds/removals are deterministic; probable instability is diagnostic evidence only. |
| D-003 | Accept only single-file GeoJSON and GeoParquet in V0. | Accepted | Limits I/O and makes CRS/feature semantics controllable. |
| D-004 | Use an explicit projected metre-based analysis CRS. | Accepted | Degree-based metric thresholds are unsafe; global/antimeridian cases are excluded. |
| D-005 | Fail closed for invalid, null, empty, GeometryCollection, or unsupported geometry. | Accepted | Repair would analyse a dataset different from the candidate. |
| D-006 | Implement only within/contains/intersects and report boundary cases. | Accepted | Simple Features semantics are precise; no invented tie-breaking. |
| D-007 | Dependencies are immutable; only the primary layer transitions. | Accepted | Enables causal attribution; multi-layer transition is deferred. |
| D-008 | Use explicit PASS/WARN/BLOCK thresholds; no score. | Accepted | Every verdict stays traceable to evidence. |
| D-009 | JSON is the source artifact; Markdown/GeoJSON are derived. | Accepted | Makes CI use and human review consistent. |
| D-010 | Shapely/GEOS is normative; DuckDB Spatial is optional acceleration. | Accepted | Prevents two spatial engines becoming competing truth sources. |
| D-011 | Do not build a generic validator, DVCS, or PR API. | Accepted | Existing tools already own those categories. |
| D-012 | Gate 0 result is PASS subject to a scoped Gate 1 proof. | Proposed | Prior art lacks the defined relationship-delta gate, but overlap remains close if scope expands. |

## Gate 1 decisions to close

1. Pin a first GeoParquet encoding/version and prove reader/CRS compatibility.
2. Lock PyProj/PROJ and prove the selected Madrid CRS transforms/metre units.
3. Define `report.json` schema and evidence field names.
4. Benchmark small/realistic fixtures before admitting DuckDB acceleration.
5. Decide whether a topologically equal but structurally different geometry is
   warning-only or a distinct policy measurement.
