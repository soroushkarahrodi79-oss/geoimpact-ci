# Gate 6 — real-world regression benchmark

## Purpose and result

Gate 5 showed that the existing GeoImpact CLI detects a meaningful bounded
Madrid blast radius. Gate 6 turns that exact observation into a deterministic
CI contract on the existing Linux and Windows matrix. The benchmark uses the
installed CLI and the frozen Gate 5 inputs; it adds no GIS capability.

**Status: GATE 6 — MODIFY.** The first GitHub-hosted run passed on Windows but
failed the Linux artifact hash assertion. The benchmark correctly preserved
the provisional cross-platform hash contract; no expected value was changed.
The exact report field difference is isolated below.

The work started from clean `origin/main` at
`d5ec31e60d3ee236640a50a04a091ec063c01e95`. PR #5 was merged, Gate 5 was
recorded as PASS, and its `linux-py311` and `windows-py314` jobs were green in
[workflow run 37282948982](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37282948982).

## Frozen input contract

CI hashes the four fixture files before running the CLI. The hashes below are
SHA-256 of the checked-in bytes. Scoped `.gitattributes` entries keep these
text inputs at LF on Windows so the byte checks are identical across checkouts.
The committed Gate 5 blobs remain unchanged.

| Input | SHA-256 |
|---|---|
| `ine-sections-2024-focus.geojson` | `9987b42293ffdda93b3cb5a1d897bccea4b084ed1ba0e1bd5eaf7f4eb303c453` |
| `ine-sections-2025-focus.geojson` | `18956b960c4b8adf5d750c04cf51a5db638ed8054e5e83988003ea59ce4d9da3` |
| `madrid-portals-change-footprint.geojson` | `a8ad452cb74dcc77cdfe43fb040b5e4b6ecee38c63710932e3de4209f74f6ec0` |
| `geoimpact.yml` | `7395510b1bc4b760dd606f1998d2ec317af0512768d223198544c7b6e52fc5b1` |

The benchmark has no live-data or network dependency. The source attribution
and licensing qualification remain in the Gate 5 source register, including
the INE licensing ambiguity and the Ayuntamiento Callejero CC BY 4.0 statement.

## Execution and expected result

On each existing matrix leg, CI installs the project and test dependencies,
runs the complete pytest suite and the existing Gate 4 PASS/BLOCK/ERROR plus
hash checks, then runs:

```text
geoimpact analyze --config research/madrid-ine-sections-2024-2025/geoimpact.yml --out ci-output/madrid-benchmark
```

`scripts/verify_madrid_benchmark.py` invokes the installed `geoimpact` console
entry point through `PATH`. The CLI must return exactly `1`, meaning a completed
policy `BLOCK`; any other exit code fails the benchmark. CI remains green when
that exact code is followed by all passing benchmark assertions.

## Frozen regression contract

The human-readable expected contract is
[`tests/fixtures/madrid_benchmark_expected.json`](../tests/fixtures/madrid_benchmark_expected.json).
The verifier asserts `BLOCK`, 2,112 relationship records, all 2,112 of them
`assignment_changed`, zero gained, zero lost, zero boundary ambiguities, and
the complete 26-pair transition histogram below.

| From CUSEC | To CUSEC | Points |
|---|---|---:|
| 2807901124 | 2807901123 | 96 |
| 2807903070 | 2807903069 | 55 |
| 2807903088 | 2807903087 | 8 |
| 2807908087 | 2807908088 | 15 |
| 2807908160 | 2807908192 | 34 |
| 2807908176 | 2807908193 | 205 |
| 2807910004 | 2807910003 | 158 |
| 2807911182 | 2807911201 | 19 |
| 2807913056 | 2807913218 | 29 |
| 2807913206 | 2807913219 | 55 |
| 2807914006 | 2807914005 | 7 |
| 2807916114 | 2807916135 | 34 |
| 2807916124 | 2807916136 | 30 |
| 2807916131 | 2807916137 | 41 |
| 2807917106 | 2807917120 | 37 |
| 2807917113 | 2807917119 | 35 |
| 2807918054 | 2807918074 | 35 |
| 2807918057 | 2807918075 | 114 |
| 2807918058 | 2807918076 | 328 |
| 2807919002 | 2807919057 | 58 |
| 2807919052 | 2807919058 | 48 |
| 2807919053 | 2807919059 | 269 |
| 2807919054 | 2807919060 | 200 |
| 2807919054 | 2807919061 | 172 |
| 2807920016 | 2807920017 | 5 |
| 2807920121 | 2807920129 | 25 |

### Transition audit

The verifier reads feature ID sets and geometries from the checked-in BASE and
CANDIDATE files, then classifies the already-produced CLI transitions. It uses
geometry equality only to determine whether a retained feature changed; it does
not run spatial predicates or replace the CLI analysis.

- **Split-like: 1,768.** Old CUSEC remains in both versions with changed
  geometry; destination CUSEC is absent in BASE and present in CANDIDATE.
- **Merge-like: 344.** Old CUSEC is present in BASE and absent in CANDIDATE;
  destination remains in both with changed geometry.
- Both IDs retained across both versions: 0.
- Pure ID-only / renumbering patterns: 0.
- Unclassified transition patterns: 0.

These names describe observed ID and geometry patterns only. They do not infer
administrative intent.

### Relationship and evidence identity

For each relationship, the verifier projects `portal_id`, old CUSEC, new CUSEC,
and the derived classification. It sorts records by those four values, encodes
the list as UTF-8 JSON with recursively sorted object keys, compact separators
(`,` and `:`), and no trailing newline, then takes SHA-256. The expected digest
is:

```text
4b1eac48876a66599a4eb0a8013625f81a64a1f7fedf47539324d4556d85ee38
```

The 2,112 evidence IDs from `relationship_regressions` are separately sorted
and hashed using the same canonical JSON encoding. The expected evidence-ID
digest is:

```text
d221ee2e751af2b46062fd0cd76581b2aff5307061919e0ba3f6e0f69bfe7cd8
```

The verifier also requires the report policy's evidence-ID list to match those
sorted regression evidence IDs exactly.

## Output artifacts and cross-platform status

The artifact SHA-256 values currently match Gate 5's provisional local values
on the Windows development run:

| Artifact | SHA-256 |
|---|---|
| `report.json` | `164b113a8b1c2d69d2bb309b97461dde7c593dfb64cf22a1d45b7945bee813d5` |
| `report.md` | `e0fd0ab0ccfcd0261dad7a3bb50e9ac6402e6b34a74929a63f413fb081d2ed92` |
| `relationship-regressions.geojson` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |

They become canonical Gate 6 hashes only after GitHub-hosted Linux and Windows
produce the same bytes. No per-OS hashes or serialization changes are allowed
to make a mismatch pass.

On the first hosted run, Windows produced all three expected hashes. Linux
produced the expected `relationship-regressions.geojson` bytes, but its
`report.json` and derived `report.md` differed. The Linux values below are
recorded only as failure diagnostics; they are not per-OS goldens and are not
accepted by the verifier:

| First-run Linux diagnostic artifact | Observed SHA-256 |
|---|---|
| `report.json` | `d542802f6af63de72de5b35eda0e715da78f1e181d803537f585b85c75a71246` |
| `report.md` | `5ba9c9998556d307cf27ccf4b1e9a431fa568e06d83c5c7c9fdf8fe7bdd5be68` |
| `relationship-regressions.geojson` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |

The parsed report diff isolates the scalar change to
`primary_change.changed_footprint_area_m2`: Linux reported
`13463975.314658953`, while Windows reported `13463975.314659253` (a
`0.000000300` m² difference). The embedded
`primary_change.changed_footprint_geometry` also serialized a different
MultiPolygon decomposition (46 versus 47 components and different coordinate
sequences); the two decoded geometries compare topologically equal, with zero
area in their symmetric difference. The Markdown difference is the same area
scalar. The regression GeoJSON, relationship histogram, relationship identity,
and evidence identity were byte-identical or digest-identical.

The footprint is created in `measure_primary_change` from per-feature Shapely
`symmetric_difference` operations followed by `unary_union`; its full-precision
area is then included in JSON and Markdown. The evidence points to a
cross-platform geometry overlay/union representation and floating-point
measurement difference, rather than changed affected relationships. Gate 3
explicitly preserves coordinate topology representation and does not round
scalar scientific measurements. Gate 6 therefore does not rebaseline these
hashes, round the area, add platform-specific expected values, or change the
Gate 3 serializer.

| Run | OS / Python | Result | CLI runtime |
|---|---|---|---:|
| Local development | Windows / Python 3.12.14 | PASS; CLI exit 1; all assertions and provisional output hashes matched | 4.534 s |
| GitHub `linux-py311` | Linux / Python 3.11.16 | Full suite and Gate 4 passed; Madrid count/identity assertions passed, report hashes failed as described | 2.638 s (follow-up run) |
| GitHub `windows-py314` | Windows / Python 3.14.7 | Full suite, Gate 4, Madrid assertions, and all provisional hashes passed | 1.865 s (follow-up run) |

The initial PR workflow was
[run 37287236988](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37287236988)
for tested commit `e77ea64c10cfda6bc818f5e2126d7b9cdcea580e`. Both matrix legs
ran **51 tests successfully** and passed the existing Gate 4 contracts. The
Linux CLI returned 1 / `BLOCK`, as expected; only the real-world output hashes
failed. The Windows CLI returned 1 / `BLOCK` and passed every assertion. The
verifier now prints OS, Python version, CLI duration, and exit code before
assertions so a failed benchmark still records runtime.

The diagnostic follow-up was
[run 37287941216](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37287941216)
for commit `3eeaf8005375f8d476d216924a8dba2ec61662c9`. It again passed all 51
tests and Gate 4 checks on both platforms. Linux recorded a 2.638 s CLI run and
reported the same two hash mismatches; Windows recorded 1.865 s and passed all
three hash assertions. The follow-up verifier logged both observed Linux
hashes together and uploaded artifacts from both matrix jobs.

Local verification ran the full test suite: **51 passed in 47.41 seconds**.
Five focused tests cover deterministic digest behavior, pair histogram
construction, frozen-manifest validation, mismatch detection, and identity
digest stability. The GitHub suite result and CI runtime observations will be
recorded after the first successful hosted run.

CI uploads the three Madrid outputs under
`geoimpact-madrid-benchmark-linux-py311` and
`geoimpact-madrid-benchmark-windows-py314`, each retained for seven days. The
upload runs when any benchmark output exists, including after a verifier
failure, and ignores missing files so it cannot replace the original benchmark
failure with an artifact-not-found failure.

Both expected benchmark artifacts were uploaded from run 37287236988 and
downloaded for this comparison:
`geoimpact-madrid-benchmark-linux-py311` and
`geoimpact-madrid-benchmark-windows-py314`.

**GitHub workflow runs:** [37287236988](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37287236988) and [37287941216](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37287941216) (Linux hash failure; Windows success in both).

**Tested commit SHAs:** `e77ea64c10cfda6bc818f5e2126d7b9cdcea580e` and `3eeaf8005375f8d476d216924a8dba2ec61662c9`.

**Canonical cross-platform output hashes:** not promoted; Linux and Windows differ.

## Scope and limitations

Gate 6 freezes one bounded Madrid case and the behavior observed under the
existing `WITHIN`, EPSG:25830, GeoJSON, and `max_relationship_regressions`
contract. It adds no predicate, geometry algorithm, file format, policy type,
UI, service, cloud dependency, or live data access. It preserves the Gate 4
synthetic contract and does not establish full-city runtime, comprehensive
Madrid coverage, legal or statistical validity for individual addresses,
general GIS support, or arbitrary platform determinism.

## Final verdict

**GATE 6 — MODIFY.** The first actual hosted run exposed a cross-platform
artifact difference in the changed-footprint area value and geometry
representation. Windows passed and Linux failed the frozen hash assertion;
both artifacts were uploaded. The benchmark expectations remain unchanged and
the PR remains a draft. No merge is authorized by this result.

## Recommended Gate 7 scope

If Gate 6 passes, Gate 7 should qualify one independently selected, bounded
real-world change case using the same installed CLI, GeoJSON input contract,
`WITHIN` semantics, and benchmark-verifier pattern. Freeze and attribute its
inputs before observing output; do not add predicates, formats, or performance
targets in that gate.
