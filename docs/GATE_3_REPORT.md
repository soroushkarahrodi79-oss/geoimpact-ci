# Gate 3 — local execution contract

## Result

**GATE 3 — PASS** for the tested Windows environment: Python 3.14.5,
Shapely 2.1.2 / GEOS 3.13.1, PyProj 3.7.2 / PROJ 9.5.1, and PyYAML 6.0.3.
The CLI is a small adapter around the Gate 2 `run_from_config` runner. No
analysis, policy, or artifact implementation was duplicated.

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

Before implementation, direct `run_from_config` on verified `origin/main`
produced the Gate 2 canonical hashes in the tested environment. The canonical
BLOCK CLI run produced the same hashes, and a test compared each direct-runner
artifact to its CLI counterpart byte-for-byte.

| Artifact | SHA-256 |
|---|---|
| `report.json` | `569f018c06ba8ec9fcd7d60c1ac08bab57735978aa0101c1e57cfd285992f872` |
| `report.md` | `d161a55cbf1441e078ce1ea3181dbc41d2ee8d73e540b311f5a52690379f202e` |
| `relationship-regressions.geojson` | `93a00d6255cc20325f54ba6ac79b431ba3432c9c4b2c1d92817ac4bb2530d4a1` |

The BLOCK and PASS reports preserve exactly the Gate 1 evidence IDs:

- `relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49`
- `relationship-regression-b9209f0fa3ca1ab124fd412de95dc593c002219a36c5053a94071855602a0c68`

Changing only the policy threshold leaves the analysis, primary geometry
change, relationship records, regression evidence, boundary evidence,
evidence IDs, and relationship GeoJSON bytes unchanged. Only the expected
policy threshold/status, top-level verdict, and derived Markdown consequences
differ.

## Tests

On the originally tested Windows environment the full suite completed with
**38 passed**. The final audit pass (below) added two tests, for a total of
**40**. It retains all Gate 1 and Gate 2 tests and adds subprocess coverage for
required arguments, PASS, BLOCK, expected errors, output completeness,
canonical hashes, evidence identity, working-directory independence,
direct-runner byte equality, PASS/BLOCK scientific invariance, and
clean-environment console-script installation, plus the two
exception-boundary tests described under the final audit.

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

### Cross-platform reproduction note

The canonical `report.json` and `relationship-regressions.geojson` SHA-256
hashes were frozen on the documented Windows environment. On a Linux container
(same PyProj 3.7.2 / PROJ 9.5.1), the reprojected coordinate serialization
differs in low-order floating-point digits — operating-system `libm`
transcendental-math variance, not a PROJ-version difference and not a
scientific defect. The verdict, changed features, relationship records, and
evidence IDs are byte-identical across both platforms; only the embedded
reprojected coordinates differ. Consequently the three byte-hash tests
(`canonical hashes`, `cwd-independence`, and `clean-venv install`) pass on
Windows but fail on Linux. This is the known Gate 2 limitation that no
cross-platform byte determinism is claimed, and it is the reason this gate is
not yet portable to a Linux CI runner.

## Limitations and deferred work

The scientific scope and deterministic report contract remain those of Gates
1 and 2. This gate makes no claim of cross-platform or cross-version byte
determinism, general GIS support, or production readiness. No GitHub Actions
workflow or other CI integration was added; it is explicitly deferred to a
later gate. The CLI does not expand supported formats, predicates, metrics,
policies, or CRS behavior.
