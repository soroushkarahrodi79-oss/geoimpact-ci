# Report V4 migration record

Date: post-v1.0.0 correctness hardening.

## Why the report version changed

Report V3 measured primary geometry change only across the intersection of
BASE and CANDIDATE stable IDs. That left candidate-only and base-only primary
features out of both the status map and the primary change footprint. V4
classifies the complete stable-ID union and includes added and removed
geometries in the footprint. This changes the meaning and completeness of the
`primary_change` section, so it is a semantic schema change rather than a
serialization-only revision.

## V4 primary-change semantics

- Shared equal geometry: `unchanged`.
- Shared different geometry: `modified`, contributing the fixed-grid
  symmetric difference.
- Candidate-only: `added`, contributing the full candidate geometry.
- Base-only: `removed`, contributing the full base geometry.
- `changed_feature_ids` is the sorted union of added, removed, and modified
  IDs. The three category lists are also sorted.
- Displacement is calculated only for modified shared IDs. Added/removed-only
  transitions report `0.0` displacement.

## Reading earlier reports

V3 reports remain valid V3 documents. Their `primary_change` data describes
only shared IDs and cannot be interpreted as proof that no primary additions
or removals occurred. Consumers should branch on `report_version`; V4 keeps
the V3 top-level report layout and relationship sections while adding the
three explicit category lists and complete status/footprint coverage.

## Deterministic output implications

The report version and primary-change fields change synthetic, Madrid, and
Sierra `report.json` and Markdown bytes. Madrid newly reports 19
candidate-only, 7 base-only, and 30 modified section IDs. Its complete
footprint area is 13,463,975.784613162 m²; the V3 shared-ID-only area was
13,463,975.315541148 m². The increase is the union contribution from the 26
added/removed primary geometries, under the same footprint precision model.
Madrid still has 2,112 relationship changes, zero gained/lost assignments, and
zero boundary ambiguities.

The changes below are intentional semantic report changes plus the V4 version
and field serialization. Relationship GeoJSON hashes remain identical. The
remaining relationship assignments, regression evidence IDs, boundary
ambiguity results, verdicts, and input hashes also remain unchanged.

| Case and artifact | V3 SHA-256 | V4 SHA-256 |
|---|---|---|
| Synthetic `report.json` | `2bfc39f79dbe11d9dc84d58923bba486ad29763155da905eb273cf0257433188` | `a3245fb06b1a49c9cfec7d7b46cd70871937fdcb40700ad6c9733f470f73df13` |
| Synthetic `report.md` | `0a3525f5bf376fd47120175bc161de13769005cbcd194b9d350771a69a63009b` | `222d3e3da2f7dc5c1c466249746022379a1735210792e3165435e49fae40d2f4` |
| Synthetic relationship GeoJSON | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |
| Madrid `report.json` | `9a04ee2dc5c3ec52a55fc12451edc23a573f0030e730d0947c3f1c602d6fadb8` | `2657b69c8e173e8997fcca10e50df36a96e80ec5226f57299039fe3c817c8d2b` |
| Madrid `report.md` | `87528179d747c430dfe6726237dfa5510c787329c632e29fb4117e151e667e21` | `74ce6c7f7e614bcec7ad94203747dce0f59dbda4e4e1e4fb0522e515665531d1` |
| Madrid relationship GeoJSON | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |
| Sierra `report.json` | `be2176458956834eebadb83c422b0e9496d496f3fa6cd1af54b00cec30748cbb` | `41c7add0c2f55a8778671661efbc30427ab0856d2e1e68ec5a904e11b8c88fcd` |
| Sierra `report.md` | `0884e42afc3c3327d1456cf055b9308e1540a8e7259c05cf9ed020fd1d763be7` | `dc522a1fc60cb083669d89b793994d57da8e996c5c667cb1b8a785f5d8beb09e` |
| Sierra relationship GeoJSON | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` |
