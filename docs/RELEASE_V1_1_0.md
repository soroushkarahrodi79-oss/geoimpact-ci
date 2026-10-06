# GeoImpact CI v1.1.0 — release candidate

**Proposed tag:** `v1.1.0`

**Proposed GitHub release title:** `GeoImpact CI v1.1.0 — primary-change correctness hardening`

This release candidate packages the post-v1.0 correctness hardening that was
merged through PR #12. It does not expand GeoImpact into a broader GIS platform.

The release tag must be created only after this release-preparation change is
merged and the post-merge `main` workflow passes. The tag target must be the
then-current verified `main` SHA, never the earlier v1.0.0 release commit.

## Release scope

GeoImpact CI v1.1.0 keeps the v1 CLI and YAML configuration contract while
advancing the report schema from V3 to V4.

The principal correctness change is that the primary stable-ID universe is now
complete:

- shared equal IDs: `unchanged`;
- shared changed IDs: `modified`;
- candidate-only IDs: `added`;
- base-only IDs: `removed`.

The deterministic primary change footprint now includes full candidate geometry
for additions, full base geometry for removals, and symmetric difference for
modified shared features. Maximum boundary displacement remains defined only
for modified shared IDs.

Expected malformed inputs now fail closed with controlled exit 2 behavior,
including malformed/non-Feature GeoJSON members, unsupported geometry types,
unknown YAML fields, invalid UTF-8, missing/duplicate IDs, and invalid geometry.
Unexpected programming errors are not disguised as user errors.

## Compatibility

The command remains:

`geoimpact analyze --config PATH --out DIRECTORY`

Exit codes remain:

- 0 — completed PASS;
- 1 — completed BLOCK;
- 2 — operational/configuration/input ERROR.

The YAML config remains version 1.

Report consumers must inspect `report_version`. V4 retains the existing
top-level report structure and relationship semantics while expanding the
`primary_change` section to the complete stable-ID universe. Existing V3
reports remain valid V3 documents.

See [REPORT_V4_MIGRATION.md](REPORT_V4_MIGRATION.md) for exact semantic and
canonical-hash changes.

## Qualification baseline

The merged PR #12 state on `main` was independently qualified before release
preparation:

- main SHA: `204bed0e42efc61e1309ec7f301cce8ad6dacc8f`;
- post-merge workflow: `37369916070`;
- Linux/Python 3.11: PASS;
- Windows/Python 3.14: PASS;
- 105 tests passed on both hosted environments;
- installed CLI PASS/BLOCK/ERROR contracts passed;
- wheel and sdist qualification passed;
- Madrid benchmark passed;
- Sierra negative control passed.

Canonical synthetic V4 hashes:

| Artifact | SHA-256 |
|---|---|
| `report.json` | `a3245fb06b1a49c9cfec7d7b46cd70871937fdcb40700ad6c9733f470f73df13` |
| `report.md` | `222d3e3da2f7dc5c1c466249746022379a1735210792e3165435e49fae40d2f4` |
| `relationship-regressions.geojson` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |

Madrid V4 preserves 2,112 relationship changes across 26 transition pairs,
zero gained/lost assignments, and zero boundary ambiguities, while explicitly
recording 19 added, 7 removed, and 30 modified primary IDs.

Sierra de Baza preserves 52 relationships, zero regressions, zero boundary
ambiguities, and maximum boundary displacement
`368.82509547712834 m`.

## Package and metadata

For v1.1.0:

- `pyproject.toml` version is `1.1.0`;
- `CITATION.cff` version is `1.1.0`;
- release qualification requires the v1.1.0 release record;
- wheel and sdist metadata must report `1.1.0`;
- canonical scientific hashes remain the V4 hashes above.

No DOI is claimed by this release record.

## License and research data

GeoImpact CI software remains released under the MIT License.

Research fixtures and third-party source data retain their source-specific
attribution, reuse conditions, provenance, and limitations. Inclusion in the
repository does not relicense those datasets under MIT. Consult
[../NOTICE.md](../NOTICE.md), the Madrid source register, and the Sierra source
register.

## Release checklist

- [x] PR #12 merged.
- [x] PR #12 post-merge workflow passed on Linux and Windows.
- [x] v1.1.0 package version prepared.
- [x] v1.1.0 citation version prepared.
- [x] CHANGELOG updated with V4 correctness-hardening scope.
- [x] Release qualification script updated for 1.1.0.
- [ ] Release-preparation PR CI passes on Linux and Windows.
- [ ] Release-preparation PR reviewed and merged.
- [ ] Post-merge `main` CI passes.
- [ ] Annotated tag `v1.1.0` created at the verified post-merge `main` SHA.
- [ ] GitHub Release published as a non-draft, non-prerelease release.

## Release boundaries

v1.1.0 does not add arbitrary CRS support, new spatial predicates, raster
analysis, network analysis, PostGIS/database integration, a web UI/API, QGIS
integration, AI, scoring, automatic repair, fuzzy identity matching, or
simultaneous dependent-layer transitions.

Those remain future work only when supported by a concrete external need.
