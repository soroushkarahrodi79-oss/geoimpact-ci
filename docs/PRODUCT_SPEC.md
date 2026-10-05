# Historical design proposal — not the current v1 contract

This Gate 0 proposal records an earlier product direction. The released v1
contract is documented in [ARCHITECTURE_V1.md](ARCHITECTURE_V1.md) and
[README.md](../README.md). In particular, GeoParquet, extra predicates, and
PASS/WARN/BLOCK are not implemented.

# GeoImpact CI — product boundary

Status: Gate 0 proposal. This document specifies no implementation.

## One job

GeoImpact CI evaluates whether a **transition** of one declared spatial layer
is safe under explicit, repository-owned policies:

```text
BASE primary layer -> CANDIDATE primary layer
                               |
                    changed footprint and metrics
                               |
                    declared dependent layers
                               |
              relationship regressions + policy evidence
                               |
                         PASS | WARN | BLOCK
```

Validation asks: **“Is this dataset valid?”**

GeoImpact asks: **“Is this change safe for the spatial relationships we
declare?”**

It may fail early when input makes analysis unsound (for example an invalid
geometry or CRS mismatch), but it is not a general validator or repair tool.

## Product contract

Given two immutable inputs for a primary dataset, immutable dependent
datasets, a declared stable ID for each, a CRS/metric policy, and a YAML
policy, the same inputs and pinned engine versions shall yield the same:

- feature-change classification;
- geometry metric values rounded at documented stages;
- footprint;
- relationship-pair deltas;
- rule evidence; and
- overall verdict.

The analysis has no network calls, inference, sampling, automatic repair, or
automatic risk score. Results are evidence, not a declaration of real-world
harm.

## In scope for V0

- File-to-file GeoParquet and GeoJSON comparisons.
- A declared, non-null, unique, stable feature ID on every primary and
  dependent dataset.
- Attribute and geometry deltas, deterministic geometry metrics, and changed
  footprint.
- `within`, `contains`, and `intersects` relationship comparison between a
  dependent layer and the primary layer.
- Explicit count/metric thresholds and PASS/WARN/BLOCK outputs.
- JSON, Markdown, and optional GeoJSON evidence.
- Local CLI suitable for a CI job. CI provider integration is a documented
  invocation pattern, not a GitHub Action in V0.

## Explicit non-goals

- Dataset repair, broad validity/conformance linting, or auto-fixing.
- Data version control, snapshots, merges, storage remotes, or synchronization.
- Raster, PostGIS, Shapefile, network/accessibility analysis, web UI, REST
  API, cloud services, QGIS/ArcGIS plugins, AI/LLMs, probabilistic rules, or
  opaque scores.
- Inferring feature IDs, CRS, dependencies, semantics, or thresholds.
- Evaluating a dependency whose own candidate version changes in the same run.
  V0 dependencies are fixed reference layers; a future design needs a
  multi-layer transition model.

## Verdict semantics

Every evaluated rule returns `PASS`, `WARN`, or `BLOCK`; a rule cannot be
silently skipped. Configuration/input errors are an operational error with a
distinct non-zero process status, not a PASS/WARN/BLOCK assessment.

Overall verdict is the maximum severity of all evaluated rule results:

`BLOCK > WARN > PASS`.

An empty rule set is invalid configuration. A rule evidence record contains
the rule name, measurement definition and value, comparator and threshold,
status, units, input identities, and stable IDs or evidence-layer references.

## Acceptance boundary

V0 is successful only if a reviewer can answer, from committed evidence,
which changed primary feature changed which dependent feature's relationship,
how, and which configured rule caused the verdict. A feature count or a map
image alone is not sufficient.

## Gate 0 verdict and limits

**GATE 0 — PASS.** The audited tools cover validation, versioning, feature
diffs, geometry evidence, aggregate GeoJSON regression, and static inter-layer
checks, but not the defined end-to-end relationship-delta policy gate. The
distinction is meaningful only while GeoImpact remains a narrow analysis layer
on top of ordinary files and CI, rather than replacing those tools.

Known risks are: stable IDs may not exist in source datasets; a wrong or
unsuitable analysis CRS makes metre metrics misleading; `within` has strict
boundary semantics that may conflict with business rules; dependencies held
fixed cannot explain a simultaneous dependent-layer change; overlay/predicate
results remain sensitive to pinned GEOS/PROJ versions; and large layers may
need performance work after correctness is proven. None justifies adding AI,
automatic scoring, a server, or a UI to V0.

**Exact Gate 1 action:** implement only the Madrid fixture vertical slice and
its specified tests: deterministic GeoJSON/GeoParquet readers, preflight,
stable-ID diff, projected geometry metrics/footprint, `within` assignment
delta, explicit policy evaluation, and JSON/Markdown/GeoJSON evidence. Gate
1 passes only if the fixture produces the stated two reassignment events and
BLOCK on repeated execution, with cross-format parity. It must not add
additional formats, infrastructure, or generic validation features.
