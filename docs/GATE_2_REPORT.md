# Gate 2 — file-backed analysis contract and deterministic artifacts

## Purpose and boundary

Gate 2 proves that the existing Gate 1 relationship-regression analysis can be
invoked from one declared file-backed contract and can emit deterministic
machine-readable and reviewable outputs. It does not expand the scientific
claim: the controlled primary polygon mutation produces two dependent WITHIN
assignment changes, deterministic evidence IDs, and the configured policy
result. No new spatial predicate or metric was introduced.

The canonical run uses only GeoJSON FeatureCollections, CRS84 fixture
coordinates, EPSG:25830 analysis, primary Polygon features, dependent Point
features, immutable dependencies, WITHIN, and
`max_relationship_regressions`. No optional impact footprint file or
production CLI is included.

## Contract and path semantics

The v1 contract is `tests/fixtures/geoimpact.yml`. It declares contract
version, analysis CRS, primary dataset name and ID field, base and candidate
files, every dependency's dataset/path/ID field/predicate, and the threshold
and severity for the sole policy rule. There are no scientific defaults for
these declarations. Gate 2 accepts only version `1`, `EPSG:25830`, predicate
`within`, and severity `block`; threshold must be a non-negative integer.
Unsupported declarations and missing files fail with a field-specific
`ContractError`.

Relative input paths resolve from the directory containing the configuration
file, regardless of the process working directory. The report does not include
resolved paths, config paths, host/user data, timestamps, temporary paths, or
random identifiers. The output directory controls only where files are
written.

The orchestration API is `geoimpact.runner.run_from_config(config_path,
output_directory)`. It loads and validates the contract, calls the existing
Gate 1 `analyze` function, builds the report object, then writes the three
artifacts. Existing Gate 1 functions remain directly testable.

## Canonical report schema and serialization

`report.json` is authoritative and has `report_version: "1"`. Its semantic
areas are:

- `analysis`: analysis CRS, primary dataset and ID field, and declared
  dependency identities/predicates (no file paths);
- `primary_change`: Gate 1 changed IDs, footprint area and embedded projected
  footprint geometry, and maximum boundary displacement;
- `relationships`: deterministic WITHIN records for dependency features;
- `relationship_regressions`: the Gate 1 regression evidence, including its
  embedded EPSG:25830 geometry;
- `boundary_ambiguities`: Gate 1 boundary evidence;
- `policy`: the one rule, observed value, threshold, evidence IDs and status;
- `verdict`: the same `PASS` or `BLOCK` result as the policy status.

Canonical JSON is UTF-8 without ASCII escaping, two-space indented, with
lexicographically sorted object keys and one final LF. Non-finite numbers are
rejected. Python's shortest round-trip float representation is retained; no
scientific values are rounded for serialization. Arrays are ordered by their
domain keys: dataset/feature ID for relationships and evidence, sorted stable
IDs within assignment sets, and sorted IDs for policy evidence. Repeating an
analysis on identical inputs and runtime produces byte-identical JSON.

## Derived Markdown and GeoJSON

`report.md` is rendered only from the canonical report object. It shows the
verdict, modified primary features, changed footprint area, maximum boundary
displacement, each relationship transition, the policy measurement and
threshold, and evidence IDs. It does not perform spatial computation.

`relationship-regressions.geojson` is an RFC 7946-style FeatureCollection
containing one feature per regression, ordered by dependent dataset and ID.
Properties are serialized with sorted keys and include evidence ID, dependent
dataset/ID, predicate, before/after assignments, and change type. Geometry is
transformed from EPSG:25830 to OGC:CRS84 by PyProj with `always_xy=True`, so
coordinates are longitude/latitude. The deprecated `crs` member is omitted.

Successful runs write exactly:

- `report.json`
- `report.md`
- `relationship-regressions.geojson`

## Determinism evidence

Two independent canonical runs wrote to separate temporary artifact
directories. They used the same config from two different current working
directories. A further run used a copied config and the complete copied
relative fixture bundle at a different temporary location. All three files
were byte-identical in all runs:

| Artifact | Run A SHA-256 | Run B SHA-256 |
|---|---|---|
| `report.json` | `569f018c06ba8ec9fcd7d60c1ac08bab57735978aa0101c1e57cfd285992f872` | `569f018c06ba8ec9fcd7d60c1ac08bab57735978aa0101c1e57cfd285992f872` |
| `report.md` | `d161a55cbf1441e078ce1ea3181dbc41d2ee8d73e540b311f5a52690379f202e` | `d161a55cbf1441e078ce1ea3181dbc41d2ee8d73e540b311f5a52690379f202e` |
| `relationship-regressions.geojson` | `93a00d6255cc20325f54ba6ac79b431ba3432c9c4b2c1d92817ac4bb2530d4a1` | `93a00d6255cc20325f54ba6ac79b431ba3432c9c4b2c1d92817ac4bb2530d4a1` |

The copied-bundle hashes matched Run A as well. The output scan found no
temporary root or absolute local path in any artifact.

> **Audit note (superseded by Gate 3B).** The three SHA-256 values above were
> generated on the documented Windows environment under the earlier *unbounded*
> floating-point coordinate serialization. They are **pre-portable-canonicalization
> hashes** and are not reproducible across operating systems, because the
> low-order digits of CRS-transformed coordinates vary with the platform's libm.
> Gate 3B introduced a precision-bounded artifact serialization contract (decision
> log D-022) that supersedes these values; the current canonical hashes are
> recorded in `GATE_3_REPORT.md`. These historical values are retained here as the
> original Gate 2 evidence, not as the active contract. The scientific results,
> verdict, and evidence IDs are unchanged between the two serializations.

## Canonical fixture result and tests

The primary fixture change remains two modified features (`chamberi` and
`tetuan`), a measured changed footprint area of
`8000.0000001862645 m²`, and maximum boundary displacement of `40.0 m`.
Regressions remain:

- `hotels / hotel_813`: `chamberi` -> `tetuan`
- `tourism_pois / poi_212`: `chamberi` -> `tetuan`

The existing Gate 1 evidence IDs are unchanged:

- `relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49`
- `relationship-regression-b9209f0fa3ca1ab124fd412de95dc593c002219a36c5053a94071855602a0c68`

The rule observes `2` against threshold `1`, returns `BLOCK`, and the
top-level verdict is `BLOCK`. The complete suite reports **26 passed**: all
8 retained Gate 1 tests pass, along with 18 Gate 2 tests covering contract
validation, relative paths, unchanged evidence IDs, report semantics,
byte-repeatability, working/config-location independence, and GeoJSON CRS84
coordinates/no legacy `crs` member.

## Local environment and limitations

`pyproject.toml` declares Python `>=3.11`, with exact local Python dependency
pins: Shapely `2.1.2`, PyProj `3.7.2`, PyYAML `6.0.3`, and pytest `8.4.2` in
the test extra. The tested environment was Windows, Python `3.14.5`, Shapely
`2.1.2`, GEOS `3.13.1`, PyProj `3.7.2`, PROJ `9.5.1`, PyYAML `6.0.3`, and
pytest `8.4.2`. The successful local pytest invocation limited BLAS/OpenMP
worker counts because this host has constrained memory.

Only this Windows environment was exercised. No cross-platform, cross-version,
or cross-GEOS/PROJ byte determinism is claimed. Native GEOS/PROJ packaging can
vary by platform. The suite currently has no GitHub CI workflow. This API is
not a CLI or release interface; the implementation remains limited to the
synthetic GeoJSON fixture and its declared field/CRS/predicate contract.

## Deferred scope

GeoParquet, Shapefile, GeoPackage, PostGIS, DuckDB, other predicates or
relationships, rasters, networks, arbitrary CRS inference, automatic repair,
new metrics, additional policy rules or scoring, CLI, GitHub Actions, REST,
UI, Docker, cloud infrastructure, AI/LLMs, plugins, and an optional impact
footprint GeoJSON remain deferred. Gate 3 is not started here.
