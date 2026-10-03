# Gate 4 — CI integration of the verified execution contract

## Status

**GATE 4 — MODIFY** — implementation is prepared; GitHub-hosted Linux and
Windows run evidence is pending. This is a CI integration gate, not a GIS
capability gate.

## Workflow

The workflow is `.github/workflows/geoimpact-ci.yml`. It runs for pull requests,
pushes to `main`, and manual `workflow_dispatch` runs. Its matrix has exactly
two GitHub-hosted environments and uses `fail-fast: false`:

| Identifier | Runner | Python |
|---|---|---:|
| `linux-py311` | `ubuntu-latest` | 3.11 |
| `windows-py314` | `windows-latest` | 3.14 |

It uses `actions/checkout@v7`, `actions/setup-python@v7`, and
`actions/upload-artifact@v7`. Workflow permissions are restricted to
`contents: read`. Each leg installs the package and test extra with
`python -m pip install ".[test]"`, runs the full pytest suite, and invokes the
installed `geoimpact` console command through `scripts/verify_ci_contract.py`.
No `PYTHONPATH` override is used.

## Execution contract

The wrapper accepts a CLI execution only when its actual subprocess return code
matches the expected value exactly:

| Scenario | Config | Expected CLI code | CI meaning |
|---|---|---:|---|
| PASS | `tests/fixtures/geoimpact-pass.yml` | 0 | Completed PASS |
| BLOCK | `tests/fixtures/geoimpact.yml` | 1 | Completed BLOCK; CI continues green |
| ERROR | Missing `tests/fixtures/missing_gate4.yml` | 2 | Controlled operational/input failure was recognized |

PASS and BLOCK each require all three output artifacts. ERROR must not report a
verdict or produce output files. After BLOCK, CI explicitly checks the three
Gate 3 canonical SHA-256 hashes. BLOCK files are uploaded per matrix leg as
`geoimpact-block-linux-py311` and `geoimpact-block-windows-py314`, with seven
days retention. Upload runs with `if: always()` and fails when the expected
files are absent; it does not create evidence files.

## Security and scope

The workflow uses GitHub-hosted runners, read-only repository contents
permission, no secrets, no downloaded scripts, and no repository mutation. It
does not configure branch protection, publish releases, or add a hosted service.
The frozen GIS scope remains unchanged: no new formats, predicates, metrics,
policies, CRS support, or spatial capabilities are introduced. Gate 1–3
scientific semantics, evidence IDs, and artifact serialization remain fixed.

## Limitations and run evidence

This gate establishes automation only for the two declared GitHub-hosted
environments and the existing pinned project dependencies. It does not claim
arbitrary-platform or cross-version determinism, production readiness, general
GIS support, branch protection, or release readiness.

Actual workflow run URLs, commit SHA, per-leg test counts, exit-code checks,
hash results, and uploaded-artifact confirmation will be recorded here only
after both GitHub-hosted matrix legs complete successfully. Until then the gate
remains **GATE 4 — MODIFY**.
