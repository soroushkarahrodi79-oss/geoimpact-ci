# GeoImpact CI v1.0.0 — release candidate

**Proposed tag:** `v1.0.0`

**Proposed GitHub release title:** `GeoImpact CI v1.0.0 — first stable reproducible research-demonstrator release`

This is the prepared release record for the Gate 10 candidate. The tag and
public GitHub release are created only after this change is merged and the
post-merge workflow passes. The release commit must be the verified `main` SHA.

## Release scope

GeoImpact CI v1.0.0 is the first stable reproducible research-demonstrator
release. It compares BASE and CANDIDATE polygon GeoJSON in EPSG:25830, requires
stable IDs, derives a deterministic change footprint and boundary displacement,
and measures fixed dependent point relationships with exact `WITHIN` semantics.
STRtree is a candidate filter; boundary `TOUCHES` are reported separately.
Configured relationship regressions yield PASS or BLOCK evidence.

The CLI is `geoimpact analyze --config PATH --out DIRECTORY`. Exit codes are 0
for completed PASS, 1 for completed BLOCK, and 2 for operational/config/input
ERROR. Outputs are `report.json`, `report.md`, and
`relationship-regressions.geojson`.

## Report and dependency contract

The active report contract is V3. The derived footprint precision grid and
boundary-displacement measurement grid are separately defined at `1e-6 m`.
They are computational reproducibility contracts, not source-accuracy claims.
The package pins Shapely 2.1.2, PyProj 3.7.2, and PyYAML 6.0.3. CI qualification
uses Linux/Python 3.11 and Windows/Python 3.14 and records Shapely/GEOS versions.

## Qualification evidence

- **Tests:** 69 baseline tests; the release qualification script adds no test
  cases.
- **Synthetic BLOCK contract (V3):** `report.json`
  `2bfc39f79dbe11d9dc84d58923bba486ad29763155da905eb273cf0257433188`;
  `report.md`
  `0a3525f5bf376fd47120175bc161de13769005cbcd194b9d350771a69a63009b`;
  regression GeoJSON
  `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978`.
- **Madrid positive benchmark:** 2,112 assignment changes, 26 transition
  pairs (1,768 split-like and 344 merge-like), zero gained/lost assignments,
  zero boundary ambiguities. Relationship identity:
  `4b1eac48876a66599a4eb0a8013625f81a64a1f7fedf47539324d4556d85ee38`;
  evidence digest:
  `d221ee2e751af2b46062fd0cd76581b2aff5307061919e0ba3f6e0f69bfe7cd8`.
  V3 output hashes are checked in
  [`GATE_9_DISPLACEMENT_PORTABILITY.md`](GATE_9_DISPLACEMENT_PORTABILITY.md).
- **Sierra negative control:** 52 relationships, all unchanged; zero
  regressions and zero boundary ambiguities; maximum displacement
  368.82509547712834 m. Relationship identity:
  `d57c99dd3f497d57ec3538c66b6aed2be2ef053a638d3fc68962690c8a50539a`;
  evidence digest:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
  V3 output hashes are checked in
  [`GATE_9_DISPLACEMENT_PORTABILITY.md`](GATE_9_DISPLACEMENT_PORTABILITY.md).
- **Performance observation:** on the controlled Gate 7 synthetic large
  workload (300 polygons, 1,500 dependents), indexed 0.134966 s versus
  exhaustive 15.420192 s, 114.25× median speedup and 99.667% candidate
  reduction. No general runtime SLA is claimed.
- **Package archive hashes:** generated locally for this candidate; these are
  observations from Windows with CPython 3.12.14, `build` 1.6.1, and setuptools
  84.0.0. They are not promised to match across platforms.

  | Artifact | SHA-256 |
  |---|---|
  | `geoimpact_ci-1.0.0-py3-none-any.whl` | `e0af02ff506f8fb0de3c55b72edbc5e1e71cd827b37eadfc1409023fb507d037` |
  | `geoimpact_ci-1.0.0.tar.gz` | `2721186ed24e815015f42d1f1259e803e1d4b5fff1959dac4b7b2a746404f5a4` |
- **Local package qualification:** wheel and sdist both built, passed archive
  content checks, installed into separate fresh virtual environments, reported
  version 1.0.0, and passed installed CLI PASS (0), BLOCK (1), ERROR (2), and
  synthetic BLOCK output hashes.
- **Hosted CI:** workflow run
  [37336921554](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37336921554)
  passed on both `linux-py311` and `windows-py314`, including full tests,
  synthetic PASS/BLOCK/ERROR and hashes, Madrid and Sierra verification, and
  wheel/sdist build and fresh-install qualification.
- **Security/privacy and hygiene:** no obvious secrets, private/local paths, or
  unintentional email addresses were found in the proposed tracked files.
  Generated build, distribution, CI-output, Python cache, and local work paths
  are ignored and are not part of the proposed diff.
- **Documentation consistency:** active public material states software 1.0.0
  and report V3. Gate-era V1/V2 values remain identified as historical records.

## Research provenance and limits

Madrid and Sierra fixtures retain their source-specific attribution, reuse
conditions, and interpretation limitations. See the [Madrid source
register](GATE_5_SOURCE_REGISTER.md) and [Sierra source
register](GATE_8_SOURCE_REGISTER.md). These dataset terms are distinct from the
license status of the software.

GeoImpact does not establish data correctness, legal impact, administrative
intent, causality, actual service use, or socioeconomic effects. The Madrid
labels describe observed ID/geometry patterns. Sierra uses a fixed reference
inventory that is not historically aligned with both boundary snapshots. The
bounded cases are not comprehensive GIS regression coverage.

## Release checklist

- [x] Authoritative starting `main` was `ccfa08b47284059c9a457f70e22ae429070308cb`.
- [x] PRs #8 and #9 are merged; named Gate 8/9 post-merge jobs were green.
- [x] Product documentation, changelog, citation, package version, and package
  metadata are prepared for 1.0.0.
- [x] Local wheel and sdist build and fresh-install qualification pass on this
  branch, including installed CLI PASS/BLOCK/ERROR and canonical synthetic
  BLOCK hashes.
- [x] Full local test suite passes (69 tests).
- [x] Synthetic, Madrid, Sierra, full test suite, and package qualification
  pass on Linux/Python 3.11 and Windows/Python 3.14 in workflow run
  [37336921554](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37336921554).
- [x] Secret/local-path, documentation consistency, and repository hygiene
  audits pass.
- [ ] Draft PR reviewed and merged by the owner.
- [ ] Post-merge `main` workflow passes before creating tag/release.
- [ ] Owner selects a repository-wide software license before describing the
  software as open source or enabling public open-source redistribution.

## Software license status

No repository-wide software license has yet been declared. No license is
invented by this release candidate. Absence of a license does not prevent a
private/internal technical release, but public open-source redistribution
remains an owner decision. It is separate from the data terms recorded in the
case source registers.

## Future-work boundary

Additional predicates and CRSs, GeoParquet, database integration, reusable
multi-case verification, broader real-world cases, package registry
publication, and a UI/API are deferred. They are not v1 release features. Any
future behavior change requires a concrete issue or use case, explicit version
planning, and compatibility analysis. After the verified v1.0.0 release, v1
behavior is frozen; there is no Gate 11 in this development sequence.
