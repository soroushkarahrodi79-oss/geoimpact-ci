# GeoImpact CI v1.2.0 — release candidate

**Proposed tag:** `v1.2.0`

**Proposed GitHub release title:** `GeoImpact CI v1.2.0 — reproducible provenance`

This release packages report contract V5, introduced through PR #15, without
expanding GeoImpact into a broader GIS platform or changing the underlying
spatial relationship semantics.

The release tag must be created only after this release-preparation PR is merged
and the post-merge `main` workflow passes. The tag target must be that verified
final `main` SHA. Existing `v1.0.0` and `v1.1.0` tags must not move.

## Release scope

GeoImpact CI v1.2.0 keeps the v1 CLI, YAML configuration schema, supported
geometry model, EPSG:25830 analysis CRS, and exact `WITHIN` relationship
contract.

Report schema V5 adds deterministic provenance:

- SHA-256 and byte size for the exact config bytes used to build the contract;
- SHA-256 and byte size for BASE and CANDIDATE inputs;
- deterministic dependency identities ordered by dataset name;
- GeoImpact CI, Shapely, GEOS, PyProj, and PROJ runtime versions;
- no local paths, timestamps, usernames, hostnames, runner names, or working
  directories in the provenance object.

V4 reports remain valid V4 documents. V5 does not change relationship,
geometry, policy, or verdict semantics.

## Qualification baseline

PR #15 was merged to:

`e10344b5aa262944b1775582d21181f3ee92d5ca`

Post-merge workflow:

`37443475350`

That workflow passed on Linux/Python 3.11 and Windows/Python 3.14 with 113
tests, PASS/BLOCK/ERROR verification, Madrid, Sierra, and wheel/sdist
qualification.

Development V5 under package version 1.1.0 produced:

| Case | report.json | report.md | relationship GeoJSON |
|---|---|---|---|
| Synthetic | `7c30c65f1228197e0fd457084c509911d40446f4b6e281907b167c30e47985ab` | `0ae2da4f039b9a4dc1b7545deae2bcd968fdc401c5bb9874eaaae9648333d2ec` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |
| Madrid | `d79a9bc7cf9780ee86fae4f4bb2302d0ed87a3e12bda64bdd9c033e67d42d374` | `f0a943bad800cba1360c6a74714d295dfe341de63a05f56d812de20fcac31a43` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |
| Sierra | `bde8bd26982e776c589286d277e51f1ef123d7091d245a579f500c61bffec3a9` | `920a27b275147fd04cf6a17e9f64212e6bec111673798d1e0e549688bf80f834` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` |

The v1.2.0 package version is itself part of V5 engine provenance, so final
v1.2.0 report JSON/Markdown hashes are expected to differ from those
development hashes. They must be recalculated and pinned by CI before release.
Relationship-regression GeoJSON is expected to remain unchanged. Any other
scientific drift is a release blocker.

## Frozen scientific results

Madrid remains:

- 2,112 relationship changes;
- 26 transition pairs;
- 1,768 split-like and 344 merge-like patterns;
- zero gained/lost assignments;
- zero boundary ambiguities.

Sierra de Baza remains:

- 52 relationships;
- zero regressions;
- zero boundary ambiguities;
- maximum boundary displacement `368.82509547712834 m`.

## Package and metadata

For v1.2.0:

- `pyproject.toml` version is `1.2.0`;
- `CITATION.cff` version is `1.2.0`;
- wheel and sdist metadata must report `1.2.0`;
- report contract remains V5;
- no DOI is claimed by this release record.

## Limitations

V5 provenance identifies exact bytes but does not embed or authenticate the
source files. Inputs are expected to remain stable during a run; provenance
capture does not lock files against concurrent replacement.

This release does not add arbitrary CRS support, new predicates, raster or
network analysis, PostGIS/database integration, web UI/API, QGIS integration,
AI, scoring, automatic repair, fuzzy identity matching, or simultaneous
dependent-layer transitions.

## Release checklist

- [x] PR #15 merged.
- [x] PR #15 post-merge workflow passed on Linux and Windows.
- [x] v1.2.0 package version prepared.
- [x] v1.2.0 citation version prepared.
- [x] CHANGELOG updated with V5 provenance scope.
- [x] Release qualification script points to v1.2.0.
- [ ] Final v1.2.0 canonical report hashes pinned and explained.
- [ ] Release-preparation PR CI passes on Linux and Windows.
- [ ] Release-preparation PR merged.
- [ ] Post-merge main CI passes.
- [ ] Tag v1.2.0 created at the verified final main SHA.
- [ ] GitHub Release published as non-draft and non-prerelease.
