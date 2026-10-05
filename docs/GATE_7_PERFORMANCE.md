# Gate 7 — full-city performance and spatial index qualification

## Purpose and starting state

Gate 7 measures whether GeoImpact can scale relationship analysis while keeping
the V2 spatial semantics, ordering, evidence IDs, and serialized artifacts
unchanged. It started from clean `origin/main` at
`557d60d6ce60ae8b25da6e8a28054ac4e7d8339b`, with PR #6 merged and its Linux
and Windows workflow green. The Gate 5 fixture files were checked before work;
no fixture or configuration bytes have been changed.

This report separates the pre-optimization baseline from later measurements.
The deterministic Gate 5 fixture is a bounded correctness benchmark. Synthetic
generated workloads are performance measurements, not scientific evidence.
Any downloaded full-city data is labeled by its retrieval date and hash and is
not a new canonical product contract.

## Existing relationship algorithm

`derive_within_assignments` sorts every dependent ID, then scans every sorted
primary ID twice for each dependent: once with exact `within`, once with exact
`touches`. BASE and CANDIDATE are evaluated separately. For `D` dependents and
`P_base`, `P_candidate` polygons, that creates
`2 × D × (P_base + P_candidate)` exact GEOS predicate calls, with O(DP)
relationship time and O(D) assignment output. Stable sorting is part of the
observable behavior.

## Pre-optimization baseline

Environment: Windows 11 build 26200; Python 3.14.5; Shapely 2.1.2 / GEOS
3.13.1; PyProj 3.7.2 / PROJ 9.5.1; Intel Core i7-8550U, 4 cores / 8 logical
processors. The run used the existing Gate 5 subset: 37 BASE polygons, 49
CANDIDATE polygons, and 2,112 dependent points.

Three fresh-process installed-module CLI invocations (using the frozen config
and separate temporary output directories) completed as BLOCK / exit 1 in
2.827 s, 2.728 s, and 2.691 s. Median: 2.728 s. The editable console script
was unavailable in this local Python setup, so these baseline invocations used
`python -m geoimpact.cli`, with the same CLI implementation and fixture.

A cProfile run of `run_from_config` took 4.590 s including first-import cost.
Both calls to `derive_within_assignments` took 2.893 s cumulative (70.9% of
the 4.080 s runner call). Shapely `within` was called 181,632 times and
`touches` 181,632 times: 363,264 measured exact geometry predicate calls.
Theoretical pair opportunities are 2,112 × (37 + 49) = 181,632 geometry
pairs, each tested with two predicates. The assignment code is therefore a
measured dominant hotspot on this fixture. Artifact rendering/writing took
about 0.473 s under cProfile; the profile also attributes about 0.33 s to
relationship GeoJSON rendering. Profile timing is instrumented and is not
compared with the unprofiled CLI timing above.

The exact-source full-city baseline has not yet been established. Gate 5's
source register records 2,450 and 2,462 INE sections and a 161,190-row Callejero
portal snapshot retrieved on 2026-10-03, but that raw snapshot is not committed.
Any live retrieval will be labeled current-source and compared by hash to the
recorded snapshots before analysis. The Gate 5 report documents a previous
broader run (complete section layers and 5,480 points) stopped after about
2.5 minutes without output; this is historical context, not a measured full
city runtime or a baseline for the new probe.

## Optimization and qualification

Pending baseline work: deterministic small, medium, and large synthetic
workloads; current-source acquisition and full-city probe; indexed candidate
work and repeated same-machine timing; edge-case and fixed-seed semantic
equivalence; byte-identical Gate 4 / Gate 6 outputs; final local and hosted
Linux / Windows verification.

## Verdict

**Baseline established; Gate 7 remains in progress.** No production relationship
code has been changed at this baseline checkpoint.
