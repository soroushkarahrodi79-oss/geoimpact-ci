# Gate 4 — CI integration of the verified execution contract

## Status

**GATE 4 — PASS.** GitHub-hosted Linux and Windows checks completed
successfully for the implementation commit. This is a CI integration gate, not
a GIS capability gate.

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
verdict or produce output files. At Gate 4, CI checked the then-current Gate 3
V1 canonical SHA-256 hashes; active V2 hashes are recorded in the Gate 6 report.
BLOCK files are uploaded per matrix leg as
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

## GitHub-hosted verification

The first pull-request workflow run completed successfully on both matrix legs:

- Run: [37105965245](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37105965245)
- Tested implementation commit: `39651cae99543b2b3d0a1612ec612bab78adbb2e`
- Linux (`ubuntu-latest`, Python 3.11.16): **46 passed**; installed CLI PASS,
  BLOCK, and ERROR checks passed; all V1 canonical hashes matched; BLOCK evidence
  upload succeeded.
- Windows (`windows-latest`, Python 3.14.7): **46 passed**; installed CLI PASS,
  BLOCK, and ERROR checks passed; all V1 canonical hashes matched; BLOCK evidence
  upload succeeded.

Each CLI wrapper validated the underlying exit code exactly: PASS `0`, BLOCK
`1`, ERROR `2`. The historical artifact contract V1 BLOCK SHA-256 results
matched on both systems:

| Artifact | SHA-256 |
|---|---|
| `report.json` | `234d31b08c18ed45e8698af2abf7e001b489bcb7efbf34ffb058e2113447388d` |
| `report.md` | `d161a55cbf1441e078ce1ea3181dbc41d2ee8d73e540b311f5a52690379f202e` |
| `relationship-regressions.geojson` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |

The uploaded artifacts are [geoimpact-block-linux-py311](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37105965245/artifacts/11267329009)
and [geoimpact-block-windows-py314](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37105965245/artifacts/11267718859).

## Limitations

This gate establishes automation only for the two declared GitHub-hosted
environments and the existing pinned project dependencies. It does not claim
arbitrary-platform or cross-version determinism, production readiness, general
GIS support, branch protection, or release readiness.
