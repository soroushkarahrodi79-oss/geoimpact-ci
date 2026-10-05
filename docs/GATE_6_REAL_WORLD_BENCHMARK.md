# Gate 6 — real-world regression benchmark

## Purpose and result

Gate 5 showed that the existing GeoImpact CLI detects a meaningful bounded
Madrid blast radius. Gate 6 turns that exact observation into a deterministic
CI contract on the existing Linux and Windows matrix. The benchmark uses the
installed CLI and the frozen Gate 5 inputs; it adds no GIS capability.

**Status: implementation complete; GitHub-hosted Linux/Windows verification
pending. Gate 6 is not PASS until both matrix legs and the final documentation
commit have succeeded and uploaded their benchmark artifacts.**

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

| Run | OS / Python | Result | CLI runtime |
|---|---|---|---:|
| Local development | Windows / Python 3.12.14 | PASS; CLI exit 1; all assertions and provisional output hashes matched | 4.534 s |
| GitHub `linux-py311` | Pending | Pending actual PR workflow | Pending |
| GitHub `windows-py314` | Pending | Pending actual PR workflow | Pending |

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

**GitHub workflow run:** pending.  
**Tested commit SHA:** pending.  
**Canonical cross-platform output hashes:** pending.

## Scope and limitations

Gate 6 freezes one bounded Madrid case and the behavior observed under the
existing `WITHIN`, EPSG:25830, GeoJSON, and `max_relationship_regressions`
contract. It adds no predicate, geometry algorithm, file format, policy type,
UI, service, cloud dependency, or live data access. It preserves the Gate 4
synthetic contract and does not establish full-city runtime, comprehensive
Madrid coverage, legal or statistical validity for individual addresses,
general GIS support, or arbitrary platform determinism.

## Final verdict

**Pending actual GitHub-hosted Linux and Windows verification and final
documentation-commit CI.** Gate 6 may be marked PASS only after both matrix legs
pass the frozen assertions, all three output hashes match on both systems, the
two benchmark artifacts are uploaded, and the final documentation commit is
green. Do not merge automatically.

## Recommended Gate 7 scope

If Gate 6 passes, Gate 7 should qualify one independently selected, bounded
real-world change case using the same installed CLI, GeoJSON input contract,
`WITHIN` semantics, and benchmark-verifier pattern. Freeze and attribute its
inputs before observing output; do not add predicates, formats, or performance
targets in that gate.
