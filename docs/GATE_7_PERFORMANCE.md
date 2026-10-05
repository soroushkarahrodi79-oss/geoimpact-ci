# Gate 7 — full-city performance and spatial index qualification

> Historical Gate 7 record: its report and artifact claims use the then-active
> report V2 contract. Report V3 is the current contract; see the Gate 9 record.

## Purpose and verified starting state

Gate 7 qualifies relationship-analysis scaling while preserving V2 spatial
semantics, ordering, evidence IDs, and serialized artifacts. Work started from
clean `origin/main` at `557d60d6ce60ae8b25da6e8a28054ac4e7d8339b`. PR #6 was
merged, and workflow run
[37297166288](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37297166288)
passed on `linux-py311` and `windows-py314`. The four Gate 5 checked-in inputs
remain byte-identical to their recorded SHA-256 values.

The Gate 5 subset is a correctness and artifact contract, not a full-city
performance benchmark. Generated workloads below are explicitly synthetic and
are not scientific evidence. Full-city data were downloaded only to temporary
`work/` storage; they do not become a new canonical product result.

## Historical exhaustive baseline and current indexed algorithm

The exhaustive scan described below is the pre-STRtree Gate 7 comparison
baseline. The active relationship engine uses STRtree candidate filtering and
the same exact GEOS predicates.

Before optimization, `derive_within_assignments` sorted each dependent ID and
scanned all primary IDs twice per dependent: exact `within`, then exact
`touches`. BASE and CANDIDATE were scanned separately. For `D` dependents and
`P_base` / `P_candidate` polygons, this is
`2 × D × (P_base + P_candidate)` exact GEOS predicate calls, with O(DP)
relationship time. Sorted stable IDs are observable output behavior.

Baseline environment: Windows 11 build 26200; Python 3.14.5; Shapely 2.1.2 /
GEOS 3.13.1; PyProj 3.7.2 / PROJ 9.5.1; Intel Core i7-8550U, 4 cores and 8
logical processors. Dataset: 37 BASE polygons, 49 CANDIDATE polygons, 2,112
dependent points.

Three fresh-process CLI runs against the frozen Gate 5 config completed with
BLOCK / exit 1 in 2.827 s, 2.728 s, and 2.691 s (median 2.728 s). The local
editable CLI launcher was unavailable, so runs used `python -m geoimpact.cli`,
the same CLI implementation and config.

A cProfile run of `run_from_config` took 4.590 s including first-import cost;
the runner call took 4.080 s. The two relationship assignments took 2.893 s
cumulative (70.9% of runner time). Profiled GEOS calls were 181,632 `within`
and 181,632 `touches`, 363,264 total. That matches the theoretical workload:
2,112 × (37 + 49) pairs × 2 predicates. `measure_primary_change` took 0.257 s
cumulative; `write_artifacts` 0.473 s, including about 0.33 s for relationship
GeoJSON rendering. cProfile timing is instrumented and is not mixed with the
unprofiled CLI times.

Three-run relationship-only timings on these same frozen geometry inputs,
using the benchmark exhaustive reference and a reused index, were: BASE
2.186263 s naive / 0.230900 s indexed (9.47×); CANDIDATE 2.985699 s naive /
0.147408 s indexed (20.25×). A post-change cProfile run separately measured
`load_features` 0.992 s, both relationship assignments 0.669 s,
`measure_primary_change` 0.256 s, regression/evidence construction 0.432 s,
and artifact writing 1.182 s. Cumulative phase values overlap when nested.

## Measurement method

[`scripts/benchmark_relationship_engine.py`](../scripts/benchmark_relationship_engine.py)
builds deterministic square grids and point dependents for small, medium, and
large workloads. It compares a benchmark-only exhaustive reference with the
production indexed engine, verifies exact dictionary equality, queries the
index to count candidate pairs, and reports median timing across three runs.
It writes only to stdout; it never touches product fixtures or artifacts.
Normal CI does not run this timing benchmark.

## Optimization selected

One Shapely STRtree is built for BASE and one for CANDIDATE, then reused across
all dependent datasets. The tree only filters impossible bounding-box
candidates. Every candidate still passes through the existing exact GEOS
`within` and `touches` predicates. Candidate indices are translated to stable
IDs and sorted before output. No native tree order enters an artifact. The
index is local to one analysis; there is no global state or cache.

Rejected alternatives: nearest/centroid assignment, envelope-only evidence,
distance or buffer approximations, threads or processes, GPU, new GIS engines,
databases, and persistent caching. They are unnecessary for the measured
bottleneck or would expand architecture and semantics.

Decision D-031 records the accepted candidate-filter design. It states that
index results are not assignment evidence, exact predicates remain authoritative,
and deterministic order is restored after every query.

## Synthetic before / after results

All measurements below ran on the same Windows 11 / Python / GEOS / PROJ / CPU
environment described above. “Naive predicate calls” are theoretical exact
calls from the exhaustive algorithm. Indexed exact calls equal twice the
measured candidate pair count because both exact predicates remain in use.
Times are medians of three runs.

| Workload | Primaries | Dependents | Naive pairs | Indexed candidates | Candidate reduction | Exact calls naive → indexed | Time naive → indexed | Speedup |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Small | 30 | 120 | 3,600 | 120 | 96.667% | 7,200 → 240 | 0.106389 s → 0.005114 s | 20.80× |
| Medium | 100 | 500 | 50,000 | 500 | 99.000% | 100,000 → 1,000 | 1.140572 s → 0.019652 s | 58.04× |
| Large | 300 | 1,500 | 450,000 | 1,500 | 99.667% | 900,000 → 3,000 | 15.420192 s → 0.134966 s | 114.25× |

The indexed output matched the exhaustive output exactly for every synthetic
size. The per-size medians show increasingly clear improvement as candidate
search grows. Small Gate 5 CLI wall time was noisy and did not show a reliable
end-to-end speedup; that CLI includes parsing, projections, rendering, and
process startup. The scale result is based on the controlled synthetic
relationship benchmark, not that bounded CLI timing.

## Semantic and artifact equivalence

The exhaustive reference exists only in tests. Equivalence coverage includes
strict interior points, outside points with zero candidates, boundaries,
overlapping polygons with multiple valid assignments, holes, MultiPolygon,
near-identical envelopes, duplicate geometry shapes under distinct IDs,
many candidates sharing an envelope, reversed mapping order, and fixed-seed
random valid polygon/point cases. A reuse test confirms only two indexes are
built for BASE and CANDIDATE across two dependent datasets.

The installed-module CLI returned BLOCK / exit 1 after optimization. The Madrid
benchmark verifier confirmed 2,112 `assignment_changed`, 26 transition pairs,
1,768 split-like, 344 merge-like, zero gained/lost/boundary records, and exact
relationship identity
`4b1eac48876a66599a4eb0a8013625f81a64a1f7fedf47539324d4556d85ee38` and
evidence-ID digest
`d221ee2e751af2b46062fd0cd76581b2aff5307061919e0ba3f6e0f69bfe7cd8`.

All three Gate 6 Madrid V2 output hashes matched exactly:

| Artifact | SHA-256 |
|---|---|
| `report.json` | `7cb57ae5b8d4c4fdf33e1e359002ac8cb2c30d05ee5f9509d47f8408a8ee9733` |
| `report.md` | `8173dee60053deea746185bf12f3d1caa560907701ee9377db2e5ee78604e57f` |
| `relationship-regressions.geojson` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |

The Gate 4 synthetic V2 hashes remain enforced by the unchanged full test
suite. No serialization, report version, evidence, policy, CRS, predicate,
boundary, or fixture code was changed.

The exact synthetic hash assertions are `report.json`
`3c34e46927f20864438455bf6bf94daf4c247ffe86bab88e2206ec40642bb076`,
`report.md`
`0a3525f5bf376fd47120175bc161de13769005cbcd194b9d350771a69a63009b`, and
`relationship-regressions.geojson`
`a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978`.

## Current-source full-city performance probe

The authoritative Gate 5 acquisition recipe was used against the live INE OGC
API and Madrid CKAN DataStore on 2026-10-05. The result is a
**CURRENT-SOURCE PERFORMANCE PROBE**, not the exact Gate 5 source snapshot:
the canonicalized filtered INE source hashes differ from Gate 5 even though
the section counts match. No live data is a CI dependency.

| Input | Gate 7 count | Gate 7 canonical source SHA-256 | Gate 5 snapshot SHA-256 |
|---|---:|---|---|
| INE Madrid 2024 sections | 2,450 | `2d9d8da28fb722dea502dd477d0bc2dee430df76739915242ba011811507dc6d` | `120692f71460f8cfd12f6542d4d7917337d916a781cac29e918bbd1b0e8946e8` |
| INE Madrid 2025 sections | 2,462 | `e52cbf3f86ab254be57015e210a9525517cd894b246fde21ac5f2b466b7b534a` | `3ce9184cf5f2ff3f0f9bcaf9211a50ea5826487d2320ee96976d53e00b8eb70d` |
| Madrid portal records (`Tipologia del numero = Portal`) | 161,190 | `0b5b9dfec593951c88a65db844b37a6135dc15deeaa4c72c53f3a2554e1a149b` | `84a0324f4e4172b75f6749a57e99ecc45e895a9b1ca1c2f7a38063d1fb538004` |

The two INE hashes use the Gate 5 canonical format: filtered source
FeatureCollection, features sorted by `CUSEC`, compact sorted-key JSON and one
trailing LF. The portal hash covers a sorted full-row DataStore snapshot inside
a compact metadata-and-records envelope; it is a new Gate 7 source hash, not
a claim of byte-equivalent canonicalization to the archived Gate 5 source.
Portal metadata reported update date 2026-09-14. All temporary downloads and
generated full-city artifacts remained under `work/madrid-current-source/`
and are not committed.

Acquisition parameters: the INE OGC Features endpoint queried collections
`WMS_INE_SECCIONES_G01:Secciones_2024` and
`WMS_INE_SECCIONES_G01:Secciones_2025` with CQL2 filter `CUMUN='28079'`,
`filter-lang=cql2-text`, GeoJSON output, and `limit=5000`; retained records
have `TIPO=SECCIONADO`. The portal DataStore endpoint queried resource
`200075-1-callejero-csv` with filter
`{"Tipologia del numero":"Portal"}`, `limit=32000`, offsets 0 through 160000
in increments of 32000. Rows were sorted by `Codigo de numero`; the documented
DMS longitude/latitude fields were converted to CRS84 decimal coordinates.

The installed-module CLI completed twice against the full input with
BLOCK / exit 1. Observed wall times were 64.173 s and 105.166 s; the second
run's sampled peak working set was 311.3 MiB. Timing varied on the laptop, so
these values are observations, not a performance SLA. The report contains
161,190 relationship records, 2,112 regressions, and zero boundary
ambiguities.

For the 161,190 × (2,450 + 2,462) full-city assignment workload, the naive
theoretical count is 791,765,280 geometry pairs and 1,583,530,560 exact
predicate calls. Measured STRtree candidates were 398,638 BASE and 399,612
CANDIDATE pairs (798,250 total), corresponding to 1,596,500 exact predicate
calls and 99.899% fewer candidate pairs than exhaustive scanning. No naive
full-city run was attempted; no time extrapolation is reported.

Separately timing prepared input stages gave 1.815 s JSON parsing and 25.510 s
geometry construction plus CRS transformation for the 166,102 features.
This shows input preparation remains a material full-city cost after indexing.
The historical Gate 5 broader attempt (5,480 points, all sections) stopped
after about 2.5 minutes without output; it is not a directly comparable
baseline and is not extrapolated here.

## Tests, hosted CI, and limitations

Local full suite: **63 passed**. Hosted workflow run
[37304072274](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37304072274)
passed on implementation HEAD `a718dc16586d10a14a48254f6c28290af740d8cd`:

| Job | Result | Full tests | Gate 4 CLI and hashes | Gate 6 Madrid verifier |
|---|---|---:|---|---|
| `linux-py311` | success | 63 passed | success | success |
| `windows-py314` | success | 63 passed | success | success |

Both jobs also uploaded their verified BLOCK and Madrid evidence artifacts.
The final closeout commit changes documentation only; the PR workflow is run
again for its HEAD before the Gate 7 closeout is considered final.

The performance benchmark uses controlled disjoint boxes and points; real
geometries can return more envelope candidates. Index construction consumes
memory proportional to the primary layer. The current full-city source is a
single current snapshot, not a frozen scientific case. Performance may vary by
hardware, Shapely, GEOS, and source geometry complexity. No machine-specific
timing threshold was added to CI.

## Verdict and next scope

**GATE 7 — PASS** for the verified implementation: measured hotspot, large
synthetic and current-source full-city completion, exact semantic and artifact
equivalence, materially reduced candidate work, and green Linux/Windows
hosted verification are all established. The final documentation closeout
commit is checked by the same PR matrix; it does not change implementation.

Recommended Gate 8 scope: qualify one independently selected, bounded
real-world change case through the installed CLI and deterministic V2 verifier.
Freeze and attribute its input bytes before observing output; preserve the same
single `WITHIN` predicate, EPSG:25830 analysis, policy surface, and artifact
contract. Gate 8 should not add another format or CRS.
