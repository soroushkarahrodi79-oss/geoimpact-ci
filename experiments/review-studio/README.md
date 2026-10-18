# GeoImpact Review Studio — feasibility experiment


> Scope update (2026-10-18): see [RECONCILIATION](RECONCILIATION.md).
> This PR remains documentary. Synthetic functional work and conditional local
> Sierra work belong to a separate Draft PR. Madrid stays HOLD; R1 OPEN.

**Decision, 2026-10-18: technical GO; implementation HOLD.**

A static, read-only review surface is technically possible from the retained
V5 artifacts and original GeoJSON inputs. The requested two-case portfolio
viewer is **not implemented**: the Madrid source register explicitly leaves
INE redistribution conditions unresolved. The experiment follows the user's
stop rule for missing data rights. Inclusion in an existing public repository
is not evidence of permission for a new visual distribution.

This directory contains an evidence-backed design and a reproducible,
non-spatial display-readiness probe. It contains no application, API,
basemap tiles, copied source geometries, or deployment configuration.

- [Feasibility audit and architecture decisions](AUDIT.md)
- [Product design, ES/EN copy and acceptance criteria](DESIGN.md)
- [Reproduction, executed validation and remaining gates](VALIDATION.md)
- [Machine-readable observations](evidence-summary.json)
- [Desktop design](design/desktop.svg), [tablet design](design/tablet.svg),
  [mobile design](design/mobile.svg)

The SVGs are **original design wireframes, not screenshots, implemented views,
real cartography, browser emulation or physical-device evidence**.

## Scope and provenance

Scientific baseline: released, non-prerelease `v1.2.0`, tag object
`5919059036ef58e175434a6266122a4c4b010bbc`, peeled commit
`45237d7caaea2aa4b81359e46f1623918645078c`. Repository/documentation audit
baseline: `c39733b61b60abe3b6e9e9c50f74f5c206022399` (main before this experiment).
The release tag's README/architecture/V5/fixtures and actual regenerated outputs
were read; newer main documentation was also checked for duplicate work.

All additions are confined here. The CLI, source package, public contracts,
policies, canonical serializers, reference fixtures and existing tests remain
untouched. The probe does not run predicates, calculate areas/displacements,
classify geometry, infer intent, or decide PASS/BLOCK. No new dependencies.

## Next concrete decision

Resolve **R1** in the audit by retaining an authoritative, dataset-specific
reuse basis for the exact INE section snapshots and their derived displays.
Then review the evidence and reopen the implementation gate. A Sierra-only or
synthetic-only viewer would change the requested two-case scope and is not
silently substituted here.

**English:** Static read-only review is technically feasible. Implementation
is on HOLD because the existing Madrid source register does not establish a
clear redistribution basis for the INE-derived geometry. This PR delivers
design and a reproducible artifact-readiness proof, not a finished viewer.
