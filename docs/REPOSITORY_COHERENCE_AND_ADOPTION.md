# Repository coherence and adoption

## Baseline and current contract

Audit baseline: `origin/main` at
`a08f573a696bb196fd1d0293ce342cc9b5c7b01c` (2026-10-06). The working tree was
clean before this branch was created. The latest stable release is v1.2.0,
Report V5.

The current product contract is defined by [README.md](../README.md),
[ARCHITECTURE_V1.md](ARCHITECTURE_V1.md), `pyproject.toml`, and the v1.2.0
release record. The V4/V5 migration records define report-version compatibility;
the changelog records release changes. It accepts GeoJSON FeatureCollections
with Polygon or MultiPolygon primary geometries, Point dependencies, unique
non-empty string IDs, OGC:CRS84 coordinates transformed to EPSG:25830, fixed
dependent layers, and exact GEOS `within` relationship assignment. `touches` is
separate boundary evidence. Configured relationship-regression policy yields
PASS (exit 0), BLOCK (exit 1), or an operational/configuration/input ERROR
(exit 2). It writes `report.json`, `report.md`, and
`relationship-regressions.geojson`; V5 records deterministic raw-byte
identities and engine versions.

It does not support other geometry families, arbitrary CRS declarations,
additional predicates, GeoParquet, rasters, network analysis, databases or
PostGIS, simultaneous dependency changes, an API or web UI, generalized scores,
WARN policy, automatic repair, or inferred identity. A verdict concerns only
the configured data and policy. It does not establish data correctness, harm,
causality, legal status, accessibility, or socioeconomic effect.

## Coherence findings

- `docs/V0_SCOPE.md` and `docs/TEST_STRATEGY.md` presented pre-implementation
  GeoParquet, broader geometry/predicate, WARN, and cross-format cases without
  a clear historical label. These are now marked as historical proposals and
  point to the active contract.
- `docs/ARCHITECTURE.md` and `docs/PRODUCT_SPEC.md` already identify themselves
  as historical proposals. The Gate 0 decision log and v1.0/v1.1 release
  preparation files now clarify their archival status; their recorded
  decisions and checklists were not rewritten.
- Production module docstrings, CLI help, and contract errors still named
  development Gates. Those descriptions now name the v1 contract and current
  CLI behavior. No analysis or policy logic changed.
- The README already described the active schema and verdicts, but omitted the
  exact CRS84 input assumption, string-ID constraints, tagged installation,
  wheel/sdist route, and a minimal adopter CI invocation. These are now
  explicit.
- Historical Gate reports, migration records, and bounded case records remain
  as evidence of what was proposed, measured, and accepted at the time. Their
  outcomes and data were not edited.

## Installation and CI adoption

The supported path today is installation from the v1.2.0 Git tag or a clean
source checkout with Python 3.11 or later. Both paths were exercised on local
Windows/Python 3.14.5: the tagged VCS install in a fresh virtual environment
completed the BLOCK example with exit 1, and the repository's
`verify_release_candidate.py` built and installed wheel and sdist in fresh
environments. No PyPI package, downloadable wheel/sdist release asset, or
reusable GitHub Action exists. The README now shows direct tagged installation,
clone-based fixture use, editable test installation, wheel/sdist building and
qualification, and a minimal workflow invocation. Existing repository CI uses
the installed CLI and checks PASS, BLOCK, ERROR, canonical artifacts, both
real-world cases, and wheel/sdist installs.

No external publication, account, or release was created for this gate.

## Development-check decisions

- **Ruff:** not added. There is no existing lint configuration or demonstrated
  defect it would protect; adopting it across historical code creates style
  churn and maintenance work.
- **mypy/pyright:** not added. Typed internal contracts already describe the
  current data structures, while a new strict checker would require ongoing
  annotation and suppression policy without protecting a missing runtime
  contract.
- **Coverage reporting:** not added. Existing tests and canonical verifiers
  target externally observable behavior; a coverage percentage alone would
  not strengthen the scientific or reproducibility contract.
- **Dependency/security scanning:** not added in this gate. Runtime dependencies
  are directly version-pinned and the hosted qualification exercises the
  supported matrix; a scanner needs triage ownership and policy to avoid
  unreviewed noisy gates.
- **GitHub Action SHA pinning:** not changed. The workflow uses major-version
  tags; immutable pins can improve supply-chain control but require an update
  process. No automated pin-update policy is currently configured.

These checks can be reconsidered when an external maintainer workflow or
concrete failure mode justifies the added policy.

No documentation-drift test was added: the relevant current promises are
already exercised by the contract suite, while broad prose searches would be
fragile against historical records and explanatory text.

## Verification and artifact status

The current branch passed the following qualification on Windows/Python
3.14.5:

- `py -m pytest`: 113 passed.
- Installed CLI PASS, BLOCK, and ERROR contracts: exit codes 0, 1, and 2.
- Synthetic canonical report, Markdown, and relationship GeoJSON hashes:
  matched the frozen v1.2.0 values.
- Madrid verifier: PASS; 2,112 relationship records, 26 transition pairs, and
  all frozen output hashes matched.
- Sierra de Baza verifier: PASS; 52 relationships, zero regressions, zero
  boundary ambiguities, and all frozen output hashes matched.
- Release candidate verifier: wheel and sdist built, installed in fresh
  environments, and passed PASS/BLOCK/ERROR and both case verifiers at package
  version 1.2.0.
- Tagged VCS installation in a fresh environment completed the documented
  fixture BLOCK with exit code 1.

The latest `origin/main` workflow before this change passed on Linux/Python
3.11 and Windows/Python 3.14. The authoritative qualification commands are the
existing workflow steps in
[`.github/workflows/geoimpact-ci.yml`](../.github/workflows/geoimpact-ci.yml),
including `python -m pytest`, all three
`scripts/verify_ci_contract.py` scenarios, canonical BLOCK hashes,
`scripts/verify_madrid_benchmark.py`, `scripts/verify_gate8_case.py`, and
`scripts/verify_release_candidate.py` for fresh wheel and sdist installations.
All current-branch canonical scientific/report artifacts matched their frozen
hashes; no report or evidence output changed. Any future mismatch is a
release-blocking discrepancy.

## Remaining gaps and next gate

An adopter currently needs Python and Git access to install a tagged source
release. There is no package registry, reusable Action, DOI, or independent
external-user report. The README and current local CLI make a pinned CI trial
possible without new infrastructure.

Ranked next moves:

1. **Independent external-user validation** — ask an unaffiliated GIS or
   research user to install the tagged release, reproduce a case, and report
   friction and interpretation risks.
2. **Reusable GitHub Action / CI integration** — consider after validation
   shows repeated integration friction worth owning as a maintained interface.
3. **Package-registry publication** — useful for conventional Python
   installation after metadata and external installation feedback are settled.

Immediate recommendation: independent external-user validation. It tests the
current contract and install path before adding distribution or integration
maintenance. Zenodo DOI/research release remains useful, but does less to
validate everyday adoption friction at this stage.
