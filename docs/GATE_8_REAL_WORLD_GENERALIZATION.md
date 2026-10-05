# Gate 8 — Independent Real-World Generalization

**Gate status: MODIFY pending hosted cross-platform qualification; the local
case produced zero relationship regressions, so it cannot demonstrate a
nonzero independent blast radius.** This result does not invalidate the
observed polygon change or the exact zero-transition result.

## Purpose and starting state

Gate 8 asks whether the unchanged GeoImpact product can produce defensible
spatial evidence for an independent real-world case outside Madrid census
sections and Madrid Callejero portal points.

- Verified starting `origin/main`: `c9b45099d3eb45b1dc575322ed6b4d55a48be349`.
- Starting checkout was clean on `perf/gate-7-spatial-index`; PR #7 was merged.
- `docs/GATE_7_PERFORMANCE.md` records Gate 7 PASS.
- Post-merge workflow run [37307832947](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37307832947) completed successfully for `linux-py311` and `windows-py314`.
- Switched local `main` to the fast-forwarded `origin/main`, verified the same SHA, and created `research/gate-8-independent-case` at that SHA with a clean tree and no initial diff.
- No file under `src/geoimpact/` was changed.

The case selection is pre-registered in [`GATE_8_CASE_SELECTION.md`](GATE_8_CASE_SELECTION.md) and committed before any Gate 8 GeoImpact run. Four candidate families were screened; no GeoImpact relationship result was a selection criterion.

## Candidate scorecard

Scores are 1–5 and were frozen before product execution.

| Candidate | Authority | Paired snapshots | Stable IDs | License | WITHIN | Change evidence | Dependency stability | Reproducibility | Independence | Size | Interpretation | Scientific defensibility | Total / 60 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Andalusia EENNPP | 5 | 4 | 3 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 5 | 5 | **51** |
| Spain Red Natura 2000 | 5 | 4 | 4 | 4 | 5 | 3 | 3 | 4 | 5 | 3 | 4 | 5 | **49** |
| Valencia PATRICOVA | 5 | 2 | 2 | 3 | 4 | 3 | 3 | 2 | 5 | 3 | 4 | 4 | **40** |
| Barcelona low-emission zone | 5 | 2 | 2 | 4 | 4 | 2 | 3 | 2 | 5 | 5 | 4 | 4 | **42** |

## Selected case and sources

**Primary:** Sierra de Baza Natural Park, Andalusia. The primary snapshots are
the official EENNPP layer updated May 2015 and the latest published layer,
December 2025. The source page specifically states that Sierra de Baza's
boundary was updated after its new PORN was approved in December 2025. The
target feature was fixed by source attributes `CODIGOESPA=69`,
`NOMBRE=SIERRA DE BAZA`, and `FIGURA=Parque Natural` before examining any
dependent assignments.

**Pre-registered fallback:** MITECO Red Natura 2000, 2021 to the latest release
reported through December 2024. It was not used. The primary was operationally
usable; a zero relationship count is not a permitted reason to switch.

Source owner, exact endpoints, dates, CRS, geometry types, counts, licenses,
attribution, raw source hashes, and fixture hashes are recorded in
[`GATE_8_SOURCE_REGISTER.md`](GATE_8_SOURCE_REGISTER.md).

The primary case is independent of Gate 5: environmental protected-area
planning replaces census sections, Sierra de Baza is outside Madrid, and the
dependent inventory is REDIAM public-use equipment rather than Callejero
portals.

### Temporal alignment

The primary states are May 2015 and December 2025. The REDIAM public-use
equipment response is a fixed inventory retrieved 2026-10-05. It is not
historically aligned with both boundary states. Results therefore describe a
spatial counterfactual using a fixed reference inventory. They do not identify
historical individual impacts or establish when a facility existed.

## Primary-change qualification, completed before dependent analysis

The selected feature is one common, unique stable ID in both states. Its
source geometries are non-empty and valid; no source repair was applied.

| Measure | BASE | CANDIDATE |
|---|---:|---:|
| Selected primary features | 1 | 1 |
| Common stable IDs | 1 (`69`) | 1 (`69`) |
| Added / removed IDs | 0 / 0 | 0 / 0 |
| Modified common geometries | 1 | 1 |
| Invalid / empty geometries in selected feature | 0 / 0 | 0 / 0 |
| Duplicate selected stable IDs | 0 | 0 |

Independent source-coordinate comparison found a symmetric-difference
change-footprint area of **2,003,072.0089 m²** and maximum Hausdorff boundary
displacement of **368.8251 m**. The complete CANDIDATE source response also
contains one invalid polygon and repeated codes elsewhere, outside the
preselected Sierra de Baza feature; neither was repaired or included in the
bounded case. The report's serialized footprint area after CRS84 round-trip
and the required 1 µm derived grid is **2,003,072.01085 m²**.

## Fixture derivation and frozen inputs

The fixed dependency layer contains point geometries and the stable source ID
field `CODIGOEQUI`. A deterministic subset retains every point within the
primary change-footprint bounding envelope expanded by exactly **10,000 m** on
each side. The expansion is only a research fixture selection rule; it is not
a GeoImpact predicate or policy buffer. The rule was set without observing
assignments. It yielded 52 dependency points, all with present unique IDs.

The canonical GeoJSON fixture inputs and config were hashed and committed
before the CLI run:

| Input | SHA-256 |
|---|---|
| `base.geojson` | `eae31120ec45e51c53b48515c0bde6e1d1c269edafea51076f862c16854d2799` |
| `candidate.geojson` | `4f4b4ff369befb14c8f1d26e902fda4b431de26432f85897d2cd77df9485cc17` |
| `dependencies.geojson` | `617d4b71921b8d66692f1c8457a56b9b6224abb0c044bb06ce7608e2524c0f6c` |
| `geoimpact.yml` | `f7e3245517cc5c16d97b34c08b0760e5055cfc25a71a39f1ee847413c0ee2520` |

Raw source hashes and the executable deterministic preparation recipe are
preserved in the source register and case directory. The input contract is
V1, EPSG:25830, WITHIN, threshold 0 with BLOCK severity. Threshold 0 is an
exploratory research detection setting, not an operational recommendation.

## Installed CLI result

The installed console entry point was used:

```text
geoimpact analyze --config research/sierra-de-baza-2015-2025/geoimpact.yml --out <output-directory>
```

- Local CLI exit: **0**.
- Report version: **V2**.
- GeoImpact policy verdict: **PASS** (0 observed regressions against a zero threshold).
- Initial local CLI runtime observation: **2.028 s**; verification rerun runtime: **1.497 s**. These are observations only; no timing threshold was applied.
- Relationship records: **52**.
- Relationship regressions: **0**.
- Change types: 52 unchanged; 0 assignment changed; 0 gained; 0 lost.
- Complete assignment transition histogram: no assignment → no assignment, 12; `69` → `69`, 40.
- Boundary ambiguities: **0**.
- Changed primary IDs: `69`; report footprint area **2,003,072.01085 m²**; maximum displacement **368.8250959452 m**.

The zero relationship result is reported as observed. No dependency source,
snapshot, or spatial filter was changed after observing it. GeoImpact PASS is
the configured policy result; the Gate 8 outcome is **MODIFY** because the
case does not demonstrate a nonzero independent relationship regression.

## Independent validation and identity digests

A small all-pairs reference join independently transformed the frozen
GeoJSON inputs to EPSG:25830 and applied exact Shapely/GEOS `within` and
`touches` calls to every dependent/primary pair. It matched all 52 indexed
GeoImpact relationship rows and all boundary results exactly. This also found
no STRtree semantic drift for this bounded fixture.

- Relationship identity digest: `d57c99dd3f497d57ec3538c66b6aed2be2ef053a638d3fc68962690c8a50539a`.
- Sorted evidence-ID digest: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty evidence list).

The identity projection contains dependent stable ID, BASE assignment(s),
CANDIDATE assignment(s), and change type, sorted deterministically and hashed
as canonical JSON. The preparation and one-off reference scripts do not
change or duplicate the production engine.

## Artifact and cross-platform status

Local V2 artifact SHA-256 values:

| Artifact | Local SHA-256 |
|---|---|
| `report.json` | `5f25074a325be9a0c504893aa67432c1444775e539e4201110c4a9899f6aefd4` |
| `report.md` | `3d56e9c0f3105373b87d3e9a99f639a18a6a99cc70e971be2c1c4182f13794fa` |
| `relationship-regressions.geojson` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` |

Linux and Windows cross-platform output hashes: **pending hosted workflow**.
The Gate 8 verifier is conditional on the research branch and leaves ordinary
CI unchanged on `main`. The existing Gate 4 hashes and Gate 6 Madrid hashes
have not been rebaselined; their final verification is pending the full test
and hosted run.

## Limitations and final status

This comparison establishes only that one official protected-area geometry
changed and records how a fixed reference inventory is spatially related to
the two states. It makes no claims about causality, legal impact, administrative
intent, service accessibility, visitor access, socioeconomic effects, or
historical individual impact. The source data's survey scale, boundary
precision, and update lineage constrain interpretation. The dependency
inventory can change over time and was not historically aligned.

**Gate 8 verdict: MODIFY** if hosted Linux and Windows reproduce the local
hashes, the full suite stays green, and canonical Gate 4/Gate 6 contracts remain
unchanged. This valid case produced zero relationship regressions, so it does
not meet the Gate's nonzero independent blast-radius demonstration criterion.
If any cross-platform or canonical contract check fails, report that additional
failure without changing the case.

### Recommended Gate 9 scope

Build a manifest-driven multi-case benchmark harness for frozen source/input
hashes, installed-CLI execution, V2 artifact and identity digests, and
independent exhaustive-reference checks across Linux and Windows. Keep
GeoImpact semantics frozen. Carry Madrid and Sierra de Baza forward as
separate contracts, and pre-register a new independent case before execution
if Gate 9 also requires a nonzero blast-radius demonstration. Do not modify
Gate 9 in this work.
