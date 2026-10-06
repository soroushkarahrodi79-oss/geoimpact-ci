# GeoImpact CI v1.2.0 — final release record

**Published tag:** `v1.2.0`

**GitHub release:** [GeoImpact CI v1.2.0 — reproducible provenance](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/releases/tag/v1.2.0)

This release packages report contract V5, introduced through PR #15, without
expanding GeoImpact into a broader GIS platform or changing the underlying
spatial relationship semantics.

The release-preparation PR was merged and the post-merge `main` workflow
passed before publication. The annotated `v1.2.0` tag targets the verified
final release commit:

`45237d7caaea2aa4b81359e46f1623918645078c`

GitHub Release `v1.2.0` was published on 2026-10-06 as a stable release
(`draft=false`, `prerelease=false`). Existing `v1.0.0` and `v1.1.0`
tags were not moved.

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

The v1.2.0 package version is itself part of V5 engine provenance, so the
release report JSON/Markdown hashes intentionally differ from the development
V5 hashes above. Hosted Linux and Windows qualification produced the same final
v1.2.0 hashes:

| Case | report.json | report.md | relationship GeoJSON |
|---|---|---|---|
| Synthetic | `d09f70d2f7fa07cef3fa87f5b1fe73d932c8f9c4619487c4a0fe8c4cc1d7b8dd` | `65ca9d67dd7ff59bc148fccc003354ea3201f51707f3e73ca2fd96dac208d95a` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |
| Madrid | `29a9337a90c7a1c591f7c05c109ee29b8c38b33324e0bb02867c1fb6a6b272df` | `ec7124260275f8ae473a9eea00da59eca2866527a8cf57714ae5bb0d681b5253` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |
| Sierra | `b17899f1472500567bb2d2eb7d0a2a9c91731a3d7827896f5635a3ef353f7cf1` | `907db7fd57c1091927277b55f624d51fb7087b453facf9cc35bdffdea44d3a89` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` |

Only the report JSON/Markdown identities moved because the engine provenance
now records GeoImpact CI 1.2.0. The relationship-regression GeoJSON is unchanged
for all three qualification cases.

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

## Release closure

- [x] PR #15 merged and its post-merge workflow passed on Linux and Windows.
- [x] Package and citation metadata set to v1.2.0.
- [x] CHANGELOG and V5 migration documentation updated.
- [x] Final v1.2.0 canonical report hashes pinned and explained.
- [x] Release-preparation PR #16 passed Linux/Python 3.11 and Windows/Python 3.14.
- [x] Release-preparation PR #16 merged.
- [x] Post-merge main workflow `37445179013` passed.
- [x] Wheel and sdist qualification passed with installed package version 1.2.0.
- [x] Annotated tag `v1.2.0` created at `45237d7caaea2aa4b81359e46f1623918645078c`.
- [x] GitHub Release published as non-draft and non-prerelease.

The tag is an unsigned annotated tag. It is immutable for this release and
must not be moved or recreated. Signed tags may be considered for future
releases without rewriting v1.2.0.
