# Gate 6 — real-world regression benchmark

> Historical Gate 6 record: this document records the report V2 footprint
> contract and its original hashes. Gate 9 supersedes V2 as the active report
> contract by defining displacement precision in report V3; see
> [Gate 9 displacement portability](GATE_9_DISPLACEMENT_PORTABILITY.md).

## Purpose and result

Gate 5 showed that the existing GeoImpact CLI detects a meaningful bounded
Madrid blast radius. Gate 6 turns that exact observation into a deterministic
CI contract on the existing Linux and Windows matrix. The benchmark uses the
installed CLI and the frozen Gate 5 inputs; it adds no GIS capability.

**Status: V2 implementation proof passed on both hosted systems.** The first
Gate 6 run exposed a Linux/Windows V1 footprint mismatch. Contract V2 now passes
locally and on both hosted matrix legs. This documentation closeout commit is
validated by the same PR workflow; PR #6 becomes ready only after both matrix
legs pass for the closeout commit.

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

## Artifact Contract V1 → V2 Migration

The initial Gate 6 run correctly rejected the V1 output hashes on Linux. Windows
matched them; Linux did not. The changed area differed by 0.000000300 m² and the
unrestricted-double overlay produced a different MultiPolygon decomposition.
Relationship assignments, the transition histogram, relationship identity,
evidence identity, and relationship GeoJSON were unchanged. This is the
cross-platform overlay difference discovered by the benchmark, not a Madrid
special case.

The first 1e-6 m fixed-precision experiment also changed Gate 4 report hashes,
so its existing V1 hash guard failed. That failure showed the derived-footprint
measurement itself needed a versioned contract; it was not a reason to weaken
the benchmark silently. The selected V2 computational precision is one
micrometre in EPSG:25830, applied only to derived per-feature symmetric
differences and their union, followed by geometry normalization. It is not a
source-accuracy claim. Relationship predicates, evidence, CRS transformations,
Hausdorff displacement, and source geometries retain their existing semantics.
No OS branch or Madrid-specific path was added. The config schema remains v1.
`report_version` is now `"2"`.

Synthetic Gate 4 equivalence, reconstructed from the same source geometries:

| Measurement | V1 unrestricted-double | V2 fixed precision |
|---|---:|---:|
| Footprint area | 8,000.0000001862645 m² | 8,000.0 m² |
| Components | 1 | 1 |
| Exterior ring coordinates | 11 | 5 |
| Valid | yes | yes |
| Changed primary IDs | 2 (`chamberi`, `tetuan`) | 2 (`chamberi`, `tetuan`) |
| Symmetric-difference area between footprints | — | 0.0000001862645 m² |
| Relative area delta | — | -2.328306436484486e-11 |

Madrid V1 areas were 13,463,975.314659253 m² on Windows and
13,463,975.314658953 m² on Linux. Recomputing the V1 Windows overlay from the
frozen inputs and comparing it to V2 gives:

| Measurement | V1 Windows | V2 |
|---|---:|---:|
| Footprint area | 13,463,975.314659253 m² | 13,463,975.315541148 m² |
| Components | 47 | 45 |
| Valid raw geometry | yes | yes |
| Changed primary IDs | 30 | 30 |
| Symmetric-difference area between footprints | — | 0.012952276636705937 m² |
| Absolute area delta | — | +0.0008818954229354858 m² |
| Relative area delta | — | 6.550037431926211e-11 |

The Linux V1 artifact's rounded geometry had a different component count
and could be invalid after serialization; its scalar remains a historical
measurement. Under V2, the serialized synthetic report geometry is valid, and
the Madrid benchmark verifier reconstructs the serialized `report.json`
footprint and requires validity. Both platform legs passed that check.

### Historical artifact contract V1 hashes

These values remain historical evidence. They are no longer active assertions
for report contract V2, which has itself been superseded by V3.

| V1 artifact | SHA-256 |
|---|---|
| Synthetic `report.json` | `234d31b08c18ed45e8698af2abf7e001b489bcb7efbf34ffb058e2113447388d` |
| Synthetic `report.md` | `d161a55cbf1441e078ce1ea3181dbc41d2ee8d73e540b311f5a52690379f202e` |
| Synthetic `relationship-regressions.geojson` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |
| Madrid `report.json` (Gate 5 / Windows) | `164b113a8b1c2d69d2bb309b97461dde7c593dfb64cf22a1d45b7945bee813d5` |
| Madrid `report.md` (Gate 5 / Windows) | `e0fd0ab0ccfcd0261dad7a3bb50e9ac6402e6b34a74929a63f413fb081d2ed92` |
| Madrid `relationship-regressions.geojson` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |

The first hosted Gate 6 V1 Linux diagnostic hashes were
`d542802f6af63de72de5b35eda0e715da78f1e181d803537f585b85c75a71246`
(`report.json`) and
`5ba9c9998556d307cf27ccf4b1e9a431fa568e06d83c5c7c9fdf8fe7bdd5be68`
(`report.md`). They document the failed V1 portability assertion and are not
per-platform goldens.

### Historical V2 canonical hashes (superseded by report V3)

These hashes preserve the Gate 6 V2 record. The active synthetic and Madrid
V3 hashes are listed in the [Gate 9 displacement portability record](GATE_9_DISPLACEMENT_PORTABILITY.md).

The local V2 outputs and both hosted platforms produced identical bytes. These
are the historical canonical report contract V2 expectations:

| V2 artifact | SHA-256 |
|---|---|
| Synthetic `report.json` | `3c34e46927f20864438455bf6bf94daf4c247ffe86bab88e2206ec40642bb076` |
| Synthetic `report.md` | `0a3525f5bf376fd47120175bc161de13769005cbcd194b9d350771a69a63009b` |
| Synthetic `relationship-regressions.geojson` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |
| Madrid `report.json` | `7cb57ae5b8d4c4fdf33e1e359002ac8cb2c30d05ee5f9509d47f8408a8ee9733` |
| Madrid `report.md` | `8173dee60053deea746185bf12f3d1caa560907701ee9377db2e5ee78604e57f` |
| Madrid `relationship-regressions.geojson` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |

The synthetic and Madrid relationship GeoJSON hashes are unchanged from V1.
V2 changes only the primary derived-footprint measurement and the report
version; the synthetic PASS/BLOCK/ERROR exit semantics and Madrid relationship
contract remain intact.

### Hosted verification and artifacts

V2 implementation commit `712687bc1241d933af05dbbe54c7acaa1ad71825` passed
[GitHub Actions run 37293722848](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37293722848)
on both jobs:

| Job | Runtime environment | Tests | Madrid CLI exit / verdict | Madrid CLI runtime |
|---|---|---:|---|---:|
| `linux-py311` | Linux / Python 3.11.16 | 57 passed | 1 / BLOCK | 2.051 s |
| `windows-py314` | Windows / Python 3.14.7 | 57 passed | 1 / BLOCK | 2.591 s |

Both legs passed Gate 4 PASS/BLOCK/ERROR and the exact V2 synthetic hashes.
Both passed Madrid input hashes, all 2,112 relationship assertions, all 26
transition pairs, split-like / merge-like classification, both identity digests,
serialized geometry validity, and the same three V2 Madrid hashes. Each leg
uploaded all three Madrid outputs (seven-day retention) as
`geoimpact-madrid-benchmark-linux-py311` and
`geoimpact-madrid-benchmark-windows-py314`.

The earlier V1 runs remain recorded as failure evidence: run
[37287236988](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37287236988)
showed the Linux hash mismatch and Windows success; diagnostic follow-up
[37287941216](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37287941216)
reproduced it. The Gate 6 implementation proof is cross-platform green. The documentation
closeout commit is validated separately by the same PR workflow, and PR #6 is
marked ready only after both jobs pass for that commit.

## Decision log

Decision **D-030** records the accepted V2 derived-footprint contract: a
1e-6 metre fixed-precision overlay with normalized output geometry, versioned
as report contract 2. It preserves the V1 hashes as historical evidence,
records the Gate 6 portability failure that motivated the migration, makes no
source-accuracy claim, and leaves relationship predicates and evidence
semantics unchanged.

## Scope and limitations

Gate 6 freezes one bounded Madrid case and the behavior observed under the
existing `WITHIN`, EPSG:25830, GeoJSON, and `max_relationship_regressions`
contract. It adds no predicate, geometry algorithm, file format, policy type,
UI, service, cloud dependency, or live data access. It preserves the Gate 4
synthetic contract and does not establish full-city runtime, comprehensive
Madrid coverage, legal or statistical validity for individual addresses,
general GIS support, or arbitrary platform determinism.

## Final verdict

**V2 implementation proof: PASS.** The V2 implementation and baselines passed
locally and in the hosted Linux/Windows matrix. The documentation closeout
commit is verified by that same workflow; PR #6 becomes ready only after both
jobs pass for its final commit. The PR remains open and is not merged.

## Recommended Gate 7 scope

If Gate 6 passes, Gate 7 should qualify one independently selected, bounded
real-world change case using the same installed CLI, GeoJSON input contract,
`WITHIN` semantics, and benchmark-verifier pattern. Freeze and attribute its
inputs before observing output; do not add predicates, formats, or performance
targets in that gate.
