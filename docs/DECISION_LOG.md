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
| D-012 | Gate 0 result is PASS subject to a scoped Gate 1 proof. | Verified | Gate 1 proved the deterministic relationship-delta mechanism within the accepted narrow scope; overlap risk remains if scope expands. |

## Gate 1 decisions to close

1. Pin a first GeoParquet encoding/version and prove reader/CRS compatibility.
2. Lock PyProj/PROJ and prove the selected Madrid CRS transforms/metre units.
3. Define `report.json` schema and evidence field names.
4. Benchmark small/realistic fixtures before admitting DuckDB acceleration.
5. Decide whether a topologically equal but structurally different geometry is
   warning-only or a distinct policy measurement.

## Gate 1 decisions

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-013 | The 40 m x 200 m control strip is geometrically consistent with the proposed 8,000 m² footprint and 40 m maximum displacement. | Verified | No Gate 0 control-value correction is required. |
| D-014 | Store the test fixtures as CRS84 GeoJSON and transform to EPSG:25830 with PyProj `always_xy=True`. | Accepted | Gate 0 requires RFC 7946 GeoJSON to be transformed before metre measurements; PyProj is therefore required for this slice. |
| D-015 | Gate 1 fixture metric assertions use ±1e-6 m / m², rather than the generic Gate 0 1e-9 suggestion. | Accepted | CRS84 decimal serialization and inverse projection yield an observed 8,000.0000001862645 m² footprint; the mathematical construction remains 8,000 m². |

## Gate 2 decisions

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-016 | Gate 2 accepts only contract version 1, EPSG:25830, GeoJSON FeatureCollections, WITHIN, and the `max_relationship_regressions` BLOCK rule. | Accepted | Keep file-backed invocation aligned with the narrow Gate 1 proof; other formats, CRSs, predicates, and policies remain deferred. |
| D-017 | Resolve relative input paths against the directory containing `geoimpact.yml`; omit resolved paths from scientific artifacts. | Accepted | Caller working directory and machine location do not affect report content. |
| D-018 | Serialize `report.json` canonically and derive both Markdown and RFC 7946 CRS84 relationship evidence from that report object. | Accepted | JSON remains authoritative; the map artifact uses explicit EPSG:25830-to-OGC:CRS84 transformation with `always_xy=True`. |
| D-019 | Pin Python package dependencies used by the local Gate 2 run in `pyproject.toml`; document the tested native GEOS/PROJ versions separately. | Accepted | Stable Python-level dependencies improve reproducibility, while native library and operating-system portability remain explicitly unclaimed. |

## Gate 3 decisions

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-020 | Expose the Gate 2 runner through one required-argument `geoimpact analyze --config PATH --out DIRECTORY` console command, with exit 0 for PASS, 1 for completed BLOCK, and 2 for execution or usage errors. | Accepted | A caller can distinguish policy blocking from failure to produce a valid analysis without changing the proven analysis or artifact contract. |
| D-021 | Keep the PASS fixture identical in spatial inputs and scientific declarations to the canonical BLOCK fixture, changing only threshold 1 to 2. | Accepted | Both successful exit states can be exercised while preserving Gate 1 evidence identity and spatial results. |

## Gate 3B decisions

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-022 | Bound published artifact coordinate representation to a fixed precision at the serialization boundary only: EPSG:25830 projected geometry to 6 decimal places (1 µm), and derived OGC:CRS84 GeoJSON to 8 decimal places (~mm in Madrid). The spatial analysis — WITHIN predicates, symmetric difference, area, Hausdorff displacement, regression detection, and evidence identity — continues at full internal double precision; rounding is applied only when coordinates cross the artifact boundary, and scalar scientific measurements (areas, displacements, counts, thresholds) are never rounded for hashing. | Verified (Linux + Windows) | Makes `report.json` and `relationship-regressions.geojson` byte-reproducible across operating systems whose libm differs in the low-order digits of CRS transformations, without altering any scientific conclusion or evidence ID. Verified by identical full-suite results (46 passed) and byte-identical canonical hashes on Linux (Python 3.11.15) and Windows 11 (Python 3.14.5) under the pinned Python dependencies; no `sys.platform` serialization branch exists. Determinism beyond these tested environments and pins is not claimed. **Serialization precision is a representation choice, not the precision or accuracy of the source data or the analysis.** The pre-portable Windows-only canonical hashes are superseded; evidence IDs are unchanged because coordinate serialization is not part of evidence identity. |

## Gate 4 decisions

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-023 | CI executes the installed GeoImpact CLI on Linux and Windows and validates PASS, BLOCK, and ERROR using exact subprocess exit codes 0, 1, and 2. | Accepted | CI distinguishes a completed policy BLOCK from an operational failure while enforcing the already-verified local contract; no analysis or policy implementation is duplicated. |
| D-024 | CI uploads the three verified BLOCK artifacts from each matrix leg even though the underlying CLI returns exit code 1 for BLOCK. | Accepted | A completed BLOCK remains a green CI scenario and retains reviewable evidence as a run artifact; missing outputs or upload failure still fail the job. |

## Gate 5 decisions

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-025 | Qualify the INE Madrid 2024-to-2025 census-section transition with the Ayuntamiento's fixed portal-address inventory as the first real-world case. | Verified (existing CLI) | The official annual polygon pair and stable address IDs produced 2,112 observed `WITHIN` assignment changes across 26 old-to-new section-ID pairs; this establishes one concrete spatial blast-radius case without expanding analysis semantics. |
| D-026 | Freeze only the reproducible change-footprint subset as a compact, attributed research fixture, keeping the sources' licenses distinct. | Accepted | A fixed input subset makes the observed case repeatable without checking in the 156 MB point snapshot or changing the code/test surface; the subset does not claim full-city coverage or a time-aligned historical address impact. |

## Gate 6 decisions

| ID | Decision | Status | Rationale / consequence |
|---|---|---|---|
| D-027 | Turn the bounded Gate 5 Madrid case into an installed-CLI regression benchmark on the existing Linux/Windows matrix, while retaining the synthetic Gate 4 contracts. | Accepted | The real-world case becomes continuously enforced without changing analysis semantics or replacing the controlled synthetic tests. |
| D-028 | Freeze aggregate results, all old-to-new transition counts, derived transition-pattern counts, and deterministic relationship/evidence identity digests. | Accepted | A future change cannot pass by reproducing only the same total count while changing affected locations or evidence identity. |
| D-029 | Treat Gate 5 output hashes as provisional until GitHub-hosted Linux and Windows reproduce identical artifact bytes. | Accepted | Cross-platform artifact hashes become canonical only after both required environments pass the same byte-level assertions. |
| D-030 | Version the derived change-footprint overlay as report contract V2 using a 1e-6 m fixed-precision grid and normalized output geometry. | Accepted (Linux + Windows verified) | Gate 6 exposed platform-dependent unrestricted-double area and decomposition. V1 hashes remain historical; V2 hashes were identical on both hosted systems. The grid is a derived-computation model, not source accuracy; relationship predicates and evidence semantics are unchanged. |
