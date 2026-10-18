# Reproduction and validation record


> Scope update (2026-10-18): see [RECONCILIATION](RECONCILIATION.md).
> This PR remains documentary. Synthetic functional work and conditional local
> Sierra work belong to a separate Draft PR. Madrid stays HOLD; R1 OPEN.

**Executed 2026-10-18.** Technical proof only; implementation remains HOLD.
All result claims below refer to executed commands or the retained output
hashes, not the visual wireframes.

## Reproduce from this experiment branch

Keep this branch checked out for the design/probe and put the released engine
in a separate worktree. These commands do not modify the engine or fixtures.
Python 3.11+ and Git are required; use the repository's pinned dependencies.
No API keys, map service or backend are required for this proof.

```text
git worktree add --detach work/studio-engine v1.2.0
python -m venv work/studio-venv
```

Activate the environment:

- Linux/macOS: `source work/studio-venv/bin/activate`
- Windows PowerShell: `work\studio-venv\Scripts\Activate.ps1`

Then, from the experiment repository root:

```text
python -m pip install -e "./work/studio-engine[test]"
cd work/studio-engine
python -m pytest -q
python scripts/verify_ci_contract.py pass
python scripts/verify_ci_contract.py block
python scripts/verify_ci_contract.py error
python scripts/verify_ci_contract.py hashes
python scripts/verify_madrid_benchmark.py
python scripts/verify_gate8_case.py
cd ../..
python experiments/review-studio/probe.py --repo work/studio-engine --outputs work/studio-engine/ci-output
python experiments/review-studio/test_probe.py --repo work/studio-engine --outputs work/studio-engine/ci-output -v
```

The existing verifiers return **0 when their checks pass**. Internally they
expect the analysis CLI to return 1 for Madrid/BLOCK, 0 for Sierra/PASS and 2
for the intentional missing-config case. A BLOCK is completed evidence, not
a failed computation. Running the raw CLI directly instead will expose those
policy exits to the shell.

The new probe uses only Python's standard library. It reads existing expected
manifests, outputs and exact source bytes. It checks byte identities and
identity/property joins; it never invokes spatial predicates, reconstructs a
footprint, measures distances, classifies topology or recalculates policy.
Its accepted input space is deliberately limited to these two frozen cases,
with one dependency dataset each. It is **not** a general V5 schema validator
or a reusable scientific case verifier replacing the existing scripts.

The stdout JSON should match the committed `evidence-summary.json`. To compare
portably, save stdout to a temporary file and parse both as JSON; Windows
PowerShell redirection can change text encoding. Do not rewrite canonical
source/report artifacts to make a comparison pass. Regeneration should happen
inside the ignored worktree output directory, not `research/` or a new public
web bundle. The retained summary contains identities/counts/scalars, not source
geometries or full individual relationship records.

The design SVGs are source artifacts viewable in any SVG-capable viewer.
Desktop is 1440×1000, tablet 834×1112, mobile is a 390×1100 content drawing for
a proposed 390×844 scrolling viewport. Fixed artwork sizes do not prove CSS
reflow or physical-device behavior.

## Executed environment and evidence

| Check | Observed result | Limits |
|---|---|---|
| Released source selection | Clean detached worktree at `45237d7caaea2aa4b81359e46f1623918645078c` | Separate from current documentation/main baseline. |
| Runtime | Linux, Python 3.12.14; GeoImpact CI 1.2.0; Shapely 2.1.2 / GEOS 3.13.1; PyProj 3.7.2 / PROJ 9.5.1 | This is a local supplementary run; it does not replace the release's hosted Linux/Python 3.11 + Windows/Python 3.14 qualification. |
| Release test suite | **113 passed** | No new external dataset validity claim. |
| Experiment-branch existing test suite | **113 passed** | Existing main tests also remain green; no engine tests edited. |
| PASS / BLOCK / ERROR verifier | All three expected exit contracts passed | Missing-config error was intentional. |
| Synthetic canonical artifacts | All three hashes matched | Existing release manifests, no rebaselining. |
| Madrid existing benchmark verifier | PASS; 2,112 regressions, 26 transition pairs; all three hashes matched | Underlying CLI returns BLOCK/1. No city-wide extrapolation. |
| Sierra existing verifier | PASS; 52 relationships, zero regressions, zero boundary ambiguities; exhaustive equality and all three hashes matched | Fixed 2026 reference points against 2015/2025 polygons. |
| New display-readiness probe | Both cases passed hashes, V5 raw-byte identities, full dependent joins, primary references, evidence/property joins | Metadata/identity proof; no coordinate-rendering, browser or load-performance test. |
| New failure-mode tests | **8 passed** | Standalone suite in this experimental directory; not added to the engine's default tests or CI contract. |
| Protected scope | All additions confined to `experiments/review-studio/` | No engine, CLI, policy, serializer, fixture, package, CI or release file edited. |
| Design assets | Three SVGs XML-parsed, rasterized locally and visually inspected | Rasterization is design QA, not browser screenshots or a functional UI test. |

The eight probe tests cover both successful retained cases including Sierra's
empty evidence, whitespace-only source tampering, equivalent-JSON artifact
byte changes, missing artifact, unknown report version, missing dependent ID,
nonexistent primary reference and mismatched geographic evidence properties.

Initial proof commands loaded released modules from the detached worktree
using explicit `PYTHONPATH=src` and an installed 1.2.0 distribution. A direct
editable installation of that detached release was then used to confirm
normal CLI/module resolution. No main-branch scientific implementation was
substituted for the tagged source.

## Exact real-case output hashes

| Case | Artifact | SHA-256 |
|---|---|---|
| Madrid | report.json | `29a9337a90c7a1c591f7c05c109ee29b8c38b33324e0bb02867c1fb6a6b272df` |
| Madrid | report.md | `ec7124260275f8ae473a9eea00da59eca2866527a8cf57714ae5bb0d681b5253` |
| Madrid | relationship-regressions.geojson | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |
| Sierra | report.json | `b17899f1472500567bb2d2eb7d0a2a9c91731a3d7827896f5635a3ef353f7cf1` |
| Sierra | report.md | `907db7fd57c1091927277b55f624d51fb7087b453facf9cc35bdffdea44d3a89` |
| Sierra | relationship-regressions.geojson | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` |

## Browser and hardware record

| Surface | Real browser process | Viewport emulation | Physical hardware | Screenshots of implemented UI |
|---|---|---|---|---|
| Desktop 1440×1000 | Not run | Not run | Not tested | None; no implemented viewer |
| Tablet 834×1112 | Not run | Not run | Not tested | None; SVG is a design |
| Mobile 390×844 | Not run | Not run | Not tested | None; SVG is a design |

The user's rights stop rule prevents proceeding to a two-case application;
therefore no functional UI, real UI screenshots or passing browser QA are
claimed. No preview server, public site or deployment was created. These
missing checks are explicit gates for a later implementation, not successes
in this report. No physical iPad/iPhone/Windows Chrome tests, human participant
study or independent adoption session occurred.

## Gates before calling a later prototype complete

1. **R1 / data rights:** close the Madrid reuse condition with retained,
   authoritative evidence and required attribution/derived-data terms.
2. **Bundle integrity:** implement a supported, bounded case manifest;
   demonstrate byte-identity failure and mixed-case rejection without modifying
   any engine output. Document unavailable overlays and unsupported schemas.
3. **Functional UI:** implement J1–J5 from DESIGN; trace every displayed value
   and selected ID to source; verify no new science/policy computations or
   required network services. Static serving/offline claims need an actual test.
4. **Real browser automation:** run J1–J5 in actual Chromium at desktop/tablet/
   mobile CSS viewports; capture screenshots of each, inspect clipping,
   selection, empty states, resize, 200% zoom, 320 px reflow, keyboard navigation,
   focus restoration, errors and ES/EN. Check console/network errors and no
   external requests. Confirm regression point coordinate routing and modified/
   added/removed geometry. Record browser/version/OS/test commit. Viewport
   emulation must remain labelled as emulation.
5. **Accessibility and devices:** measure contrast; perform keyboard and
   screen-reader review; record any physical tablet/mobile runs separately.
   Do not claim device coverage from Chromium viewport dimensions.
6. **Professional usefulness:** a later separate study should ask independent
   reviewers to trace evidence, explain PASS/BLOCK and recognize Sierra's
   counterexample. Proposed release target: every qualifying participant
   distinguishes policy outcome from correctness/real effects, with all task
   errors and timing reported. No speed or adoption claim until measured.

This Draft PR is a feasibility/design decision. It is not a merge, release,
scientific-contract migration, deployment or completion of the portfolio app.
