# Gate 3 — local execution contract

## Result

**GATE 3 — PASS**, verified on both Linux and Windows. The local execution
contract and the Gate 3B portable artifact-serialization contract (below) are
complete, and the full suite passes on both operating systems with byte-identical
canonical artifacts:

- **Linux:** 46 passed (Python 3.11.15, Shapely 2.1.2 / GEOS 3.13.1,
  PyProj 3.7.2 / PROJ 9.5.1, PyYAML 6.0.3).
- **Windows 11:** 46 passed (Python 3.14.5, `sys.platform = win32`).

The CLI is a small adapter around the Gate 2 `run_from_config` runner; no
analysis, policy, or artifact implementation was duplicated.

This gate was previously **GATE 3 — MODIFY** pending that Windows confirmation.
Gate 3B intentionally changed the artifact serialization contract, so the new
canonical hashes had to be re-confirmed on the originally documented Windows
environment. That Windows run has now been performed and the three canonical
hashes match the Linux values exactly, closing the verification sequence. See
"Portable artifact canonicalization (Gate 3B)" below.

PASS here means GeoImpact now has a stable local CLI execution contract,
PASS/BLOCK/ERROR exit semantics, deterministic file-backed execution,
precision-bounded artifact serialization, byte-identical canonical artifacts
across the tested Linux and Windows environments, preserved evidence identity,
and preserved scientific results. It is **not** a claim of arbitrary-platform
determinism, production readiness, generalized GIS support, public release
readiness, or existing CI integration.

## Command and entry point

Install the project, then invoke:

```text
geoimpact analyze --config PATH --out DIRECTORY
```

Both options are required. The command does not search for a configuration
file, use the current directory as a default, prompt interactively, or access
the network. Contract-relative input paths retain Gate 2 behavior and resolve
from the configuration file's directory. `--out` may name a directory that
does not exist; the Gate 2 writer creates it and writes the three fixed
artifact names without deleting other files.

`pyproject.toml` exposes the installable console script:

```toml
[project.scripts]
geoimpact = "geoimpact.cli:main"
```

The executable delegates to `geoimpact.runner.run_from_config(config, out)`.
The same adapter is also callable for development with
`python -m geoimpact.cli analyze --config PATH --out DIRECTORY`.

## Exit codes and streams

| Exit code | Meaning |
|---:|---|
| 0 | Analysis completed and verdict is `PASS`. |
| 1 | Analysis completed and verdict is `BLOCK`; valid artifacts are written. |
| 2 | Analysis could not complete validly, or argparse rejected command usage. |

For a completed PASS or BLOCK analysis, stdout contains `GeoImpact CI`, the
verdict, and paths to `report.json`, `report.md`, and
`relationship-regressions.geojson`. It does not print the report body.
Expected contract, input, and filesystem errors use stderr in the form
`GeoImpact error: <diagnostic>` and do not print a traceback. No verdict is
printed for these errors. Unexpected programming errors remain visible.
Argparse's required-argument usage failures, such as omitting `--config` or
`--out`, return 2 and print usage to stderr.

## PASS, BLOCK, and ERROR executions

`tests/fixtures/geoimpact-pass.yml` points to the exact Gate 2 spatial files
and changes only the relationship threshold from 1 to 2. The observed count
remains 2, so the result is PASS. The canonical
`tests/fixtures/geoimpact.yml` remains unchanged: threshold 1, observed count
2, result BLOCK.

| Execution | Result | Artifacts |
|---|---|---|
| PASS config, threshold 2 | exit 0; stdout says `Verdict: PASS` | All three written |
| Canonical BLOCK config, threshold 1 | exit 1; stdout says `Verdict: BLOCK` | All three written |
| Missing config | exit 2; stderr says `GeoImpact error: config file does not exist: ...` | No output directory or scientific artifacts |
| Missing `primary.base` file | exit 2; stderr identifies `primary.base` and the missing file | No output directory or scientific artifacts |
| Missing required CLI option | exit 2; argparse usage on stderr | No analysis started |

The error path test also covers an invalid contract. The representative input
failures occur before artifact writing. As in Gate 2, an exceptional failure
during sequential artifact writes could leave partial files; transactional
filesystem behavior is outside this gate.

## Installation proof

The clean installation used the repository's supported `pyproject.toml`
metadata in a new temporary virtual environment, with Python 3.14.5:

```text
python -m venv <temporary-directory>/venv
<temporary-directory>/venv/Scripts/python.exe -m pip install .
```

From a working directory outside the repository, with `PYTHONPATH` unset, the
installed `Scripts/geoimpact.exe` ran the following commands:

```text
geoimpact analyze --config <repo>/tests/fixtures/geoimpact-pass.yml --out <temp>/pass
geoimpact analyze --config <repo>/tests/fixtures/geoimpact.yml --out <temp>/block
geoimpact analyze --config <temp>/missing.yml --out <temp>/error
```

Observed exit codes were respectively **0**, **1**, and **2**. PASS and BLOCK
wrote all three artifacts. The error wrote no verdict or artifacts and printed
one actionable diagnostic to stderr. This proves local console-script
installation and import resolution only; it is not a claim of release or
public packaging quality.

## Artifact and evidence invariance

The canonical BLOCK CLI run and direct `run_from_config` produce byte-identical
artifacts, and a test compares each direct-runner artifact to its CLI
counterpart byte-for-byte. The hashes below were canonical under the Gate 3B
portable serialization contract (decision log D-022). They are now
**historical artifact contract V1** values; report contract V2 is documented in
`GATE_6_REAL_WORLD_BENCHMARK.md` and its current hashes are enforced by CI.

| Artifact | SHA-256 (portable, Gate 3B) |
|---|---|
| `report.json` | `234d31b08c18ed45e8698af2abf7e001b489bcb7efbf34ffb058e2113447388d` |
| `report.md` | `d161a55cbf1441e078ce1ea3181dbc41d2ee8d73e540b311f5a52690379f202e` |
| `relationship-regressions.geojson` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |

`report.md` is unchanged from the pre-portable record because it embeds no
coordinates. The pre-portable `report.json`
(`569f018c06ba8ec9fcd7d60c1ac08bab57735978aa0101c1e57cfd285992f872`) and
`relationship-regressions.geojson`
(`93a00d6255cc20325f54ba6ac79b431ba3432c9c4b2c1d92817ac4bb2530d4a1`) are
recorded here as history, not as the active contract.

The BLOCK and PASS reports preserve exactly the Gate 1 evidence IDs:

- `relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49`
- `relationship-regression-b9209f0fa3ca1ab124fd412de95dc593c002219a36c5053a94071855602a0c68`

Changing only the policy threshold leaves the analysis, primary geometry
change, relationship records, regression evidence, boundary evidence,
evidence IDs, and relationship GeoJSON bytes unchanged. Only the expected
policy threshold/status, top-level verdict, and derived Markdown consequences
differ.

## Tests

The full suite is **green on Linux with 46 passed** (Python 3.11.15). It retains
all Gate 1 and Gate 2 tests and adds subprocess coverage for required arguments,
PASS, BLOCK, expected errors, output completeness, canonical hashes, evidence
identity, working-directory independence, direct-runner byte equality,
PASS/BLOCK scientific invariance, and clean-environment console-script
installation; the two exception-boundary tests from the hardening pass; and the
Gate 3B canonicalization tests (projected and CRS84 precision bounds, negative
zero, non-finite rejection, structure preservation, and proof that
canonicalization touches only artifact representation, not analysis).

## Final audit (hardening pass)

A later audit/hardening pass made four non-scientific corrections to the Gate 3
change. None alter the Gate 1 or Gate 2 scientific outputs: the verdicts,
changed features, relationship records, regression evidence, evidence IDs, and
the canonical artifact serialization are all unchanged. These are audit
corrections, not a claim that there were no prior Gate corrections.

- **Reconciled the historical Gate 2 hash record.** The `GATE_2_REPORT.md`
  determinism table listed a Run B SHA-256 for
  `relationship-regressions.geojson` with a copy typo (a dropped `4b2c`
  segment). The documentation now records the canonical
  `93a00d6255cc20325f54ba6ac79b431ba3432c9c4b2c1d92817ac4bb2530d4a1` for both
  runs. Only the report text changed; no scientific output or serialization was
  modified to match.
- **Closed D-012.** The Gate 0 decision log entry D-012 was still `Proposed`
  pending a scoped Gate 1 proof. Gate 1 proved the deterministic
  relationship-delta mechanism within the accepted narrow scope, so D-012 is
  now `Verified` (overlap risk remains if scope expands).
- **Narrowed the CLI exception boundary.** The CLI previously caught the
  built-in `ValueError` as a broad operational-error category, which would
  disguise an unrelated programming bug as a controlled `GeoImpact error`. A
  dedicated `geoimpact.errors.GeoImpactError` base now marks expected
  domain/input failures; `contract.ContractError` subclasses it (retaining
  `ValueError`), and the analysis input-validation failures raise a new
  `errors.InputError`. The CLI now catches only
  `(GeoImpactError, OSError, UnicodeError)`. Expected malformed/invalid input
  still yields exit 2 with a concise stderr diagnostic and no traceback; an
  unexpected programming `ValueError` is no longer swallowed and remains
  visible. Two tests assert this distinction.
- **Ignored generated packaging output.** `.gitignore` now excludes `build/`
  and `*.egg-info/` so local installation proofs do not leave untracked build
  artifacts in the tree.

## Portable artifact canonicalization (Gate 3B)

### Root cause

The pre-portable `report.json` and `relationship-regressions.geojson` embedded
CRS-transformed coordinates serialized at full `repr` precision. On a Linux
container (same PyProj 3.7.2 / PROJ 9.5.1 as the documented Windows host) those
coordinates differ from the Windows bytes in their low-order digits —
operating-system `libm` transcendental-math variance, not a PROJ-version
difference and not a scientific defect. The verdict, changed features,
relationship records, scalar measurements, and evidence IDs were already
byte-identical across platforms; only the embedded coordinate digits drifted,
so the three byte-hash tests failed on Linux. The exact fields that differed
were `primary_change.changed_footprint_geometry`,
`relationship_regressions[*].evidence_geometry` (both EPSG:25830, in
`report.json`), and the inverse-transformed CRS84 point coordinates in the
GeoJSON.

### Representation-only fix

Gate 3B bounds the **serialized** coordinate representation at the artifact
boundary only (decision log D-022). The analysis engine is untouched: WITHIN
predicates, symmetric difference, area, Hausdorff displacement, regression
detection, and evidence identity all continue on full-precision double
geometries. No `shapely.set_precision` is applied to analysis geometry. A small
standard-library serializer rounds only the numeric ordinates of embedded
geometries when writing artifacts, preserving geometry type, coordinate order,
and topology, normalizing `-0.0` to `0.0`, and rejecting non-finite ordinates.
The inverse CRS transform still runs on full-precision projected geometry; only
its CRS84 output is rounded. Scalar scientific measurements
(`changed_footprint_area_m2`, `max_boundary_displacement_m`, counts, thresholds)
are never rounded.

### Precision policy

| Artifact geometry | CRS | Serialization precision | Resolution |
|---|---|---|---|
| `report.json` embedded geometry | EPSG:25830 (metres) | 6 decimal places | 1 µm |
| `relationship-regressions.geojson` | OGC:CRS84 (degrees) | 8 decimal places | ~mm in Madrid |

These are **serialization** precisions — a representation choice, not the
precision or accuracy of the source data or the analysis.

### Result

The full suite passes on both Linux and Windows and artifacts are byte-identical
across repeated runs, working directories, and copied config locations. Evidence
IDs and all scientific conclusions are unchanged from the pre-portable
serialization.

| Environment | Python / platform | Tests | report.json | report.md | relationship-regressions.geojson |
|---|---|---:|---|---|---|
| Linux | 3.11.15 | 46 passed | `234d31b0…447388d` | `d161a55c…79f202e` | `a3557416…42318978` |
| Windows 11 | 3.14.5 (`win32`) | 46 passed | `234d31b0…447388d` | `d161a55c…79f202e` | `a3557416…42318978` |

Both environments produced the identical full canonical hashes recorded under
"Artifact and evidence invariance" above; the installed console script worked
from outside the repository with `PYTHONPATH` unset on both; and the CLI returned
exit 0 (PASS), 1 (BLOCK), and 2 (expected error) on both. No `sys.platform`
branching, per-platform expected hashes, skips, or weakened hash checks exist —
there is one canonical representation, now verified cross-platform under the
tested pinned Python dependencies. Determinism beyond these two tested
environments and dependency pins is not claimed.

## Limitations and deferred work

The scientific scope remains that of Gates 1 and 2. Gate 3B makes the artifact
serialization precision-bounded and byte-reproducible, now verified on the
tested Linux and Windows environments under the pinned Python dependencies;
determinism on arbitrary platforms, Python versions, or GEOS/PROJ builds is not
claimed. The gate asserts no general GIS support or production readiness. No
GitHub Actions workflow or other CI integration was added; it is explicitly
deferred to a later gate. The CLI does not expand supported formats, predicates,
metrics, policies, or CRS
behavior.
