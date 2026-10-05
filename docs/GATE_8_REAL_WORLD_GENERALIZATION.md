# Gate 8 — Independent Real-World Generalization

**Gate status: MODIFY. Research record: ACCEPTED.** The unchanged case
produced zero relationship regressions, so the original nonzero-demonstration
criterion remains unmet. Its independent negative-control result is accepted
as a reproducible research record. The original V2 Linux/Windows displacement
drift is preserved below; Gate 9 fixed that generic portability defect, and
the unchanged case now reproduces byte-identical V3 artifacts across both
platforms.

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

## Original V2 artifact and cross-platform status

V2 artifact SHA-256 values by execution environment:

| Artifact | Local Windows 3.12 | Hosted Windows 3.14 | Hosted Linux 3.11 |
|---|---|---|---|
| `report.json` | `5f25074a325be9a0c504893aa67432c1444775e539e4201110c4a9899f6aefd4` | `5f25074a325be9a0c504893aa67432c1444775e539e4201110c4a9899f6aefd4` | `21332438c94dd67692c04f61ea5c205c46a264fa2d27b5ffae975761addd6a70` |
| `report.md` | `3d56e9c0f3105373b87d3e9a99f639a18a6a99cc70e971be2c1c4182f13794fa` | `3d56e9c0f3105373b87d3e9a99f639a18a6a99cc70e971be2c1c4182f13794fa` | `eee743d495bb49f97deaaaeea7126cb869283ea07ca134dd4c5bf468af69e574` |
| `relationship-regressions.geojson` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` |

Cross-platform output bytes are **not equal**. Hosted Linux and Windows have
identical input hashes, relationship identity, evidence digest, assignments,
and empty regression GeoJSON. The only report value difference is
`primary_change.max_boundary_displacement_m`: Windows reports
`368.8250959451751 m`; Linux reports `368.82509594532814 m`, a difference of
approximately `1.53e-10 m`. This low-order scalar difference changes the JSON
and Markdown hashes. The Gate 8 verifier reports this drift rather than
rebaselining it. Product code and V2 scalar serialization were left unchanged.

The verifier is conditional on `research/gate-8-independent-case`; ordinary
`main` CI is unchanged. In the hosted run, Linux and Windows each passed the
63-test full suite, Gate 4 CLI/hash checks, and Gate 6 Madrid benchmark. Gate 8
exact-hash/reference verification passed on Windows and failed on Linux at the
artifact hash check. Gate 4 canonical hashes and Gate 6 Madrid hashes/digests
remain exact on both platforms.

Hosted workflow run [37314122890](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37314122890)
on PR head `ac2ae14e248ce3940abc3871f0b1db680ebd9998`: `windows-py314`
success; `linux-py311` failed only the Gate 8 byte-hash comparison.

## Limitations and final status

This comparison establishes only that one official protected-area geometry
changed and records how a fixed reference inventory is spatially related to
the two states. It makes no claims about causality, legal impact, administrative
intent, service accessibility, visitor access, socioeconomic effects, or
historical individual impact. The source data's survey scale, boundary
precision, and update lineage constrain interpretation. The dependency
inventory can change over time and was not historically aligned.

**Original Gate 8 verdict: MODIFY.** The case produced zero relationship
regressions, so it did not meet the nonzero independent blast-radius
demonstration criterion. Hosted Linux also differed from Windows in the
unrounded Hausdorff-displacement scalar, so original V2 output bytes were not
cross-platform equal. No fallback, fixture alteration, or product change was
made to hide either result.

### Gate 9 follow-up at the time

Gate 9 should first investigate a deterministic cross-platform contract for
`max_boundary_displacement_m`, which differed by `1.53e-10 m` for the same
frozen case, without changing the scientific geometry or claim about source
accuracy. Then establish a manifest-driven multi-case benchmark harness for
frozen source/input hashes, installed-CLI execution, V2 artifact and identity
digests, and independent exhaustive-reference checks across Linux and
Windows. Keep predicate and policy semantics frozen. Carry Madrid and Sierra
de Baza forward as separate contracts, and pre-register a new independent case
before execution if a nonzero blast-radius demonstration is still required.
Gate 9 subsequently addressed the displacement portability defect and was
merged. The details and V3 reconciliation are recorded below.

## Gate 8 reconciliation on report contract V3

Gate 9 changed the active report contract to V3 and defined maximum boundary
displacement on temporary geometry copies conformed to the explicit
`1e-6 m` grid. This preserves full-precision relationship predicates and does
not mutate any source or fixture geometry. PR #8 was rebased onto Gate 9's
merged main (`fc78007df9969d67d849d2a5f9179fc9b62ab4ed`). The conflict in the
decision log was resolved by preserving Gate 9's D-032 exactly; D-033 records
acceptance of this research record without changing the original Gate verdict.

All four committed Sierra inputs retain their original SHA-256 values listed
above. The unchanged case was rerun under V3 with report version **3** and
maximum boundary displacement **368.82509547712834 m**. Results remain:

- GeoImpact policy verdict: **PASS** (the configured regression threshold is
  zero and observed regressions are zero).
- Relationships: **52**; unchanged **52**; assignment changed **0**; gained
  **0**; lost **0**.
- Transition histogram: **12** records with `[] -> []`; **40** records with
  `["69"] -> ["69"]`.
- Boundary ambiguities: **0**.
- Relationship identity SHA-256:
  `d57c99dd3f497d57ec3538c66b6aed2be2ef053a638d3fc68962690c8a50539a`.
- Evidence-ID SHA-256 (empty evidence list):
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
- V3 `report.json`: `be2176458956834eebadb83c422b0e9496d496f3fa6cd1af54b00cec30748cbb`.
- V3 `report.md`: `0884e42afc3c3327d1456cf055b9308e1540a8e7259c05cf9ed020fd1d763be7`.
- V3 `relationship-regressions.geojson`:
  `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a`.

The Gate 8 verifier continues to check the frozen input hashes, installed CLI,
exit code, V3 report contract, full transition semantics, exact artifact
hashes, and equality with an independent exhaustive all-pairs reference.
Hosted Linux and Windows must each pass this verifier and the existing suite,
Gate 4 V3 contracts, and Madrid V3 benchmark before the PR is ready for review.

**Final Gate 8 verdict: MODIFY. Research record: ACCEPTED.** Sierra is a
reproducible independent negative control. Its zero-transition result remains
valid and does not meet the predeclared nonzero blast-radius criterion. The PR
is accepted as a research record because it preserves an independently
selected and validated real-world case, frozen attributed inputs, and the
reproducible portability defect that led to Gate 9. Acceptance of the record
does not mean the Gate passed and does not claim a successful nonzero
demonstration.
