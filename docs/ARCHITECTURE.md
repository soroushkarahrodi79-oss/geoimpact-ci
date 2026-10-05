# Historical design proposal — not the current v1 architecture

This document preserves the earlier V0 proposal. The implemented v1 contract
is documented in [ARCHITECTURE_V1.md](ARCHITECTURE_V1.md).

# Proposed V0 architecture

## Design constraints

One local Python 3.12+ process reads files, performs deterministic analysis,
writes artifacts, and exits. It requires no server, Docker image, Node.js,
database, map, cloud account, or network request. Package versions are locked
in Gate 1; reports record the resolved versions.

```text
YAML config + base file + candidate file + dependency files
                         |
       input/CRS/ID preflight (fail closed on analysis error)
                         |
      normalized in-memory feature records in analysis CRS
                         |
    ID join -> feature delta -> geometry metrics -> footprint
                         |                         |
                         +------ dependency STRtree + full predicates
                                                   |
                                     relation/assignment delta
                                                   |
                                      policy evaluator (pure)
                                                   |
                     JSON as source of truth -> Markdown / GeoJSON evidence
```

## Components and responsibilities

| Component | Responsibility | Must not do |
|---|---|---|
| Config loader | Parse/validate YAML into a versioned internal model | Guess an ID/CRS/rule |
| Readers | Read GeoJSON or GeoParquet, preserve source provenance | Repair or coerce geometry |
| Preflight | Enforce IDs, schema essentials, CRS compatibility, valid/allowed geometry | Become a generic validator |
| Normalizer | Transform to analysis CRS and form canonical attribute/ID records | Mutate source input |
| Differ | Deterministically ID-join and classify changes | Match similar anonymous features |
| Metric/footprint engine | Compute declared metrics and evidence geometries | Make severity decisions |
| Relation engine | Index dependencies and compute predicate-pair/assignment deltas | Infer domain semantics |
| Policy engine | Turn explicit measurements into rule results | Score risk or hide evidence |
| Report writer | Stable JSON/Markdown/optional GeoJSON outputs | Communicate with GitHub |
| CLI | Accept paths, write directory, select failure exit | Host a service |

## Technology evaluation

| Technology | V0 decision | Reason / constraint |
|---|---|---|
| Python 3.12+ | Required | Small local runtime, typed models, cross-platform CI. |
| PyArrow | Required | Direct Parquet/GeoParquet metadata and columnar reading without a server. |
| Shapely 2.1+ | Required | GEOS validity, topology, overlay, STRtree, equality, Hausdorff, centroid/area/length. |
| PyProj 3.6+ | Required addition | Shapely has no CRS awareness. Deterministic metre metrics require explicit CRS parsing/transformation and `always_xy`. This is technically necessary, not infrastructure. |
| DuckDB Spatial | Optional V0 accelerator, not authority | Useful for scalable GeoParquet scans and spatial candidate filtering. Do not make results depend on an optional SQL path; Shapely/GEOS is the normative V0 predicate/metric engine. Gate 1 must benchmark whether it is worth enabling. |
| PyYAML | Required | Minimal declarative configuration reader; `safe_load` only. |
| Typer | Required | Small typed CLI with no web/API surface. |
| pytest | Required | Fixture-driven deterministic acceptance tests. |

DuckDB Spatial is a sensible future performance layer, but DuckDB's geometry
functions and Shapely/GEOS must not be mixed as interchangeable truth engines
within a run. The V0 reference result is Shapely/GEOS. If an optional DuckDB
prefilter is used, it may over-select but may never exclude a pair that the
reference bounding-box selection would test; sampled parity tests are required.

## Minimal CLI contract (design only)

`geoimpact analyze --config geoimpact.yml --base BASE --candidate CANDIDATE --out artifacts/`

Success writes `report.json` and `report.md`, plus evidence only when enabled.
Exit 0 means PASS/WARN completed; exit 1 means at least one BLOCK; exit 2
means invalid configuration/input or an internal analysis error. CI may choose
to treat WARN as failure outside the engine, but V0's three-state verdict is
preserved.

## Reproducibility contract

- Inputs are identified by SHA-256 and paths are presentation metadata only.
- Config bytes/digest, logical input identities, engine/dependency versions,
  `analysis_crs`, tolerances, buffer and densification settings are stored.
- ID collections, changed feature records, relation pairs and rule evidence
  have specified sort orders.
- JSON has a schema version and deterministic key/array order; Markdown is
  generated solely from that JSON.
- No timestamps enter the deterministic content. An optional generated-at
  field, if ever added, is excluded from content hashes and defaults off.

## Security and scale boundary

V0 treats data as untrusted: reject path traversal in output names, YAML
unsafe tags, malformed WKB/GeoJSON, duplicate IDs, unsupported nesting, and
unbounded geometry collections. It does not execute expressions from YAML.
Full inputs are materialized in memory initially; documented fixtures establish
correctness before any streaming optimization. The first performance question
is which rows/columns PyArrow can select and which dependents an STRtree can
shortlist—not distributed infrastructure.
