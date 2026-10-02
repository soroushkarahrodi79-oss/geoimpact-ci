# Prior-art audit

Research date: 2026-10-02. This is a capability audit, not a claim that an
unlisted tool cannot be extended to do a capability. `Yes` means the named
tool documents that capability as a first-class workflow; `Partial` means a
nearby primitive or an aggregate-only variant; `No` means it is outside the
documented scope. In particular, a `No` is not a claim of impossibility.

## Sources examined

- [CONFUZ3 GeoLint](https://github.com/CONFUZ3/geolint): validation, repair,
  contracts, cross-layer coverage and CI outputs.
- [jajego GeoLint](https://github.com/jajego/geolint): GeoJSON quality,
  delivery budgets, and semantic aggregate baselines.
- [Kart](https://github.com/koordinates/kart): distributed data version
  control with feature edits, diffs, commits, branches, and merges.
- [GeoGig](https://github.com/locationtech/geogig) and its
  [`diff`](https://geogig.org/manpages/diff.html) command: a GIS DVCS with a
  detailed feature diff and changed bounds.
- [Eurostat GeoDiff](https://github.com/Eurostat/geodiff): two-version vector
  diff, optional ID field, geometric resolution, Hausdorff segments, gains /
  losses, and ID-stability output.
- [Mergin Maps geodiff](https://github.com/MerginMaps/geodiff): table-level
  insert/update/delete changesets for GeoPackage and optionally PostGIS.
- [GeoParquet Validator](https://github.com/geoparquet/geoparquet-validator)
  and the [GeoParquet specification](https://github.com/opengeospatial/geoparquet):
  file/spec conformance, not change analysis.
- [Great Expectations](https://docs.greatexpectations.io/docs/0.18/core/introduction/introduction/)
  and [Soda contracts](https://docs.soda.io/soda-documentation/soda-v3/data-contracts):
  representative data-quality/data-contract systems.

## Competitive capability matrix

| Capability | CONFUZ3 GeoLint | jajego GeoLint | Kart | GeoGig | Eurostat GeoDiff | Mergin geodiff | GeoParquet Validator | Data contracts / DQ |
|---|---|---|---|---|---|---|---|---|
| Dataset validation | Yes | Yes (GeoJSON) | No | No | No | No | Yes (spec) | Yes |
| Dataset versioning | No | No | Yes | Yes | No | Partial (sync/merge) | No | No |
| Explicit BASE vs CANDIDATE spatial diff | No | Partial (aggregate baseline) | Yes | Yes | Yes | Yes | No | Partial (checks over runs) |
| Feature-level identity | Yes (uniqueness) | Yes (ID rule) | Yes (PK) | Yes (repository feature) | Yes (`-id`) | Yes (rows/PK) | No | Yes (keys) |
| Geometry-change metrics | Partial (quality/topology) | No | Partial (feature diff) | Partial (coordinates/bounds) | Yes (resolution, Hausdorff segment, gains/losses) | No documented metric suite | No | No |
| Spatial change footprint | No | No | Partial (diff) | Partial (changed bounds) | Yes (gains/losses) | No | No |
| Declared dependency layers | Cross-layer validation only | No | No | No | No | No | No | Partial (lineage, non-spatial) |
| Cross-layer relationship regression | No | No | No | No | No | No | No | No |
| Downstream spatial blast-radius analysis | No | No | No | No | No | No | No | No |
| Configurable regression policies | Yes (quality thresholds) | Yes (budgets/baselines) | No | No | No | No | No | Yes (quality contracts) |
| Deterministic PASS/WARN/BLOCK | Partial (severity/exit) | Partial (errors/warnings/exit) | No | No | No | No | Pass/fail only | Partial (pass/fail/severity) |
| PR-native reporting | Yes (SARIF, Action) | Yes (JSON/exit, usable in CI) | Git-oriented, no dedicated gate | Git-oriented, no dedicated gate | No documented PR integration | No documented PR integration | CLI report only | Yes/Partial |
| Machine-readable evidence artifacts | Yes (JSON, SARIF, GeoJSON errors) | Yes (schema-versioned JSON) | Diff formats | Diff output | Yes (GeoDiff + geometry layers) | Yes (JSON changeset) | Yes (validation report) | Yes |

### Important overlaps and boundaries

**jajego GeoLint is the closest naming and workflow overlap.** It is a mature
enough warning sign, not something to dismiss. It calls itself a quality and
regression linter, has committed semantic baselines, thresholds, JSON output,
and CI exit status. Its documented regression baseline is an aggregate
snapshot: feature/vertex counts, file size, geometry distribution, property
shape, and ID quality. It intentionally does not offer a topology engine or
domain-specific GIS validation. It does not resolve stable feature identities
between two supplied datasets, calculate changed-geometry metrics, inspect a
changed footprint, or re-evaluate relations to a dependent layer.

**CONFUZ3 GeoLint is a validator, not a transition analyser.** It is broader
than a GeoJSON linter: it checks geometry validity, CRS, topology, contracts,
and static inter-layer `must-not-overlap` / `must-be-covered-by` rules. Those
checks ask whether a current state meets a condition. It does not document a
BASE/CANDIDATE dependency-relationship delta.

**Kart and GeoGig solve data versioning.** Both make it practical to store or
compare versions. Kart explicitly tracks feature additions, edits, and
deletions in its working copy. GeoGig's `diff --bounds` emits changed bounds.
Neither documented workflow evaluates a declared dependency graph after a
candidate boundary change or produces policy evidence about reassigned
features. GeoImpact must consume ordinary files/CI refs; it must not recreate
their repository, merge, or synchronization functions.

**Eurostat GeoDiff is the closest spatial-diff primitive.** It compares two
versions using an ID field; it emits Hausdorff maximum segments, spatial gains
and losses, and detects potential ID instability. This materially narrows the
novelty claim: GeoImpact should reuse the idea of feature-level geometry
evidence where compatible, rather than claim that such metrics or footprints
are new. GeoDiff does not document dependent layers, relationship deltas,
policies, or a PR gate.

**Mergin geodiff is a changeset and synchronization library.** It creates and
applies table-level changesets and reconciles conflicts for GeoPackage and
PostGIS. It is not a geometry-impact or cross-layer-regression engine.

**GeoParquet Validator and generic contracts validate a state.** The former
checks GeoParquet conformance and distribution advice; contracts enforce
schema/value/freshness/quality expectations. Neither represents a spatial
transition or computes how a change alters a declared dependent layer.

## Gate-0 conclusion from prior art

No audited mature open-source project implements the full, specific workflow:

`BASE primary layer + CANDIDATE primary layer + stable feature IDs + declared
dependent layers + deterministic topological relationship delta + explicit
policy verdict + feature evidence`.

That is a defensible **niche**, not a broad claim of novelty. The niche is
small and depends on refusing to compete with validators, version-control
systems, generic GeoJSON regression tools, or spatial diff libraries. If V0
loses the dependent relationship-delta and evidence workflow, it becomes
overlapping glue and should be stopped or redesigned.
