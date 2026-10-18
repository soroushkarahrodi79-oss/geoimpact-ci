# Local prototype validation — executed 2026-10-18

**GO for the bounded local prototype. R1 OPEN; full Madrid + Sierra viewer
HOLD.** No merge, public demo or deployment. This record describes implemented
software and real captures, separately from the wireframes/prior experiments
in documentary [PR #22](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/22).

## Executed evidence

| Check | Result | Scope |
|---|---|---|
| Existing suite, functional checkout | **113 passed**, 58.26 s | Existing engine tests unchanged; no experiment tests injected into the scientific suite. |
| Existing suite, exported release | **113 passed**, 62.54 s | Exact `v1.2.0` source commit `45237d7caaea2aa4b81359e46f1623918645078c`. |
| CLI contracts | PASS/0, BLOCK/1 and intentional ERROR/2 verified | Actual released CLI; analysis ERROR produces no report/verdict. |
| Canonical outputs | **All nine output hashes unchanged** | Three synthetic, three Madrid and three Sierra artifacts, checked by unchanged release verifiers. Madrid was never added to `web/`. |
| Preparation | Four cases generated; synthetic source bytes and Sierra source bytes checked against the fixed release | BLOCK/PASS share exact original synthetic geometry; optional Sierra generated locally only. |
| New reader tests | **22 passed**, 0 failed, 0 skipped with local Sierra present | Byte integrity, schema, CRS, composite joins, primary identity/presence, evidence/coordinates, meaningful zero, unsupported reports and failure states. |
| Chromium end-to-end | **12 acceptance groups passed** | [Full result record](qa/browser-results.json); actual Chromium 153.0.8010.12, headless, Windows, Playwright 1.56.1, Node 24.11.0. |
| Runtime network | **0 external requests**, 0 uncaught errors, 0 ordinary console errors | Requests intercepted and audited; one deliberately injected missing-file console error is separately recorded as an expected fault. |
| Isolation | Loopback static serving, repository paths unavailable, directory listing disabled, remote Host rejected | No mutation/backend/engine API. No remote fonts, tiles, dependencies or source requests. |
| Dependency audit | `npm audit`: 0 known vulnerabilities at execution | Pinned development-only Playwright. No npm runtime dependencies. This is not a comprehensive security audit. |
| Protected scope | Empty diff from main for `src/geoimpact`, tests/fixtures, scripts, scientific contract/policy, packaging and existing CI | Changes are confined to `experiments/review-studio-local/`. |

[qa/validation.json](qa/validation.json) pins the actual tested UI/reader/test
source bytes, preparation/server/dependency files and screenshot hashes.
[qa/engine-checks.json](qa/engine-checks.json) retains exact commands/exits.
The browser record's base commit is the checkout parent; it does not pretend
that the previously uncommitted UI files belonged to main. Use the source
digest manifest to identify the tested implementation, and Git history to
identify the final functional commit.

## J1–J5 within the permitted scope

| Journey | Executed acceptance |
|---|---|
| J1: understand | Synthetic BLOCK 2/1, PASS 2/2 and three records; Sierra PASS 0/0 and 52 records. Dates, synthetic/local-only labels, policy semantics and HOLD visible. No Madrid acceptance claim. |
| J2: trace | Search `hotel_813`, keyboard select, exact `["chamberi"]→["tetuan"]` and existing evidence ID in both views/panel. Transition filter preserves total. Real downloaded report hash equals the frozen value. Sierra assigned and unassigned records have no invented regression ID. |
| J3: compare | Both original geometries, original point inventory, shared fit/pan/zoom, primary-ID selection, layer toggles and narrow snapshot switch retaining selection. Source-coordinate routing checked by the reader; no projected footprint is rendered. |
| J4: audit | All exact file identities/sizes, configuration bytes, five V5 versions, source credits/conditions and interpretation limits available. ES/EN switches preserve selected identities. Scientific values trace to report fields; source metadata stays distinct. |
| J5: fail/zero | Intercepted missing file, whitespace-tampered report and unsupported V4 disable normal review. Analysis ERROR clears stale verdict/map. Sierra regression filter has zero rows while **52 original points remain**, with an explicit valid-empty explanation. |

All five requested CSS sizes passed: **1440×900, 1440×1000, 834×1112,
375×812, 390×844**, plus **320×812**. Reflow checks assert no horizontal page
overflow. The initial 320 px overflow from long traceability text was corrected
with shrinkable grid tracks and wrapping; the final run passed.

Keyboard checks used actual Tab, Enter, Space, arrows, + and Escape events:
skip link, row selection, map exit and focus restoration passed. Pointer map
selection and pan/zoom buttons were exercised. The list is the equivalent
non-map route; SVG points do not become 52 Tab stops. Body text contrast was
measured as **11.86:1** for its actual foreground/background pair. Other token
pairs have not been comprehensively audited; this is not a WCAG claim.

The 200% check is explicitly **CSS zoom emulation**, not browser-chrome zoom
or physical-device qualification. Screen readers, physical phones/tablets and
independent human comprehension/adoption were not tested. The existing frozen
CLI external-validation protocol was not changed or executed.

## Real screenshots, not drawings

All screenshots below come from the implemented UI in Chromium, using only
synthetic geometry. They are suitable for review of the local prototype:

- [Desktop 1440×900](qa/screenshots/synthetic-1440x900.png)
- [Desktop 1440×1000](qa/screenshots/synthetic-1440x1000.png)
- [Tablet viewport 834×1112](qa/screenshots/synthetic-834x1112.png)
- [Mobile viewport 375×812](qa/screenshots/synthetic-375x812.png)
- [Mobile viewport 390×844](qa/screenshots/synthetic-390x844.png)
- [Mobile map and controls](qa/screenshots/synthetic-mobile-review.png)
- [Mobile selected evidence](qa/screenshots/synthetic-mobile-evidence.png)
- [Mobile complete page](qa/screenshots/synthetic-mobile-full.png)
- [320 px reflow](qa/screenshots/synthetic-320x812.png)
- [200% CSS zoom emulation](qa/screenshots/synthetic-zoom-200.png)
- [Analysis ERROR](qa/screenshots/analysis-error.png)
- [Integrity ERROR](qa/screenshots/integrity-error.png)

Sierra's full-page meaningful-zero capture and mobile capture remain in
ignored `qa/local/sierra-zero-desktop.png` and `qa/local/sierra-mobile.png`.
They are delivered locally, not uploaded to the PR or treated as authorization
for public visualization. They show actual retained geometry, never a mockup.

## Technical assessment and practical limits

The assessment follows observed files, source conditions and fault tests,
rather than equating the implementation's existence with scientific validity.
There has been **no separate human reviewer or external product validation**.
The report does not label this self-review as independent human approval.

The useful local task is supported: trace an existing spatial assignment to a
fixed source/version and policy result. The meaningful counterexamples are
Sierra's changed polygon with zero relationship regressions and the synthetic
PASS with two regressions. Neither licenses a conclusion about real-world harm,
population, administrative decisions, historic equipment or source correctness.

The renderer is a small native SVG adapter rather than the proposed OpenLayers
dependency. Original rings and holes are retained with an affine lon/lat
display; it is not an equal-area/metric projection. View-framing bounds and
visual zoom are presentation operations only. No JS spatial predicate,
relationship classification, geometry diff, metric or policy computation is
introduced. No new synthetic geometry was authored; all fixtures are from the
frozen release. Gained/lost, multiple assignments, holes and boundary records
are structurally supported but not all have a dedicated retained visual case
in this prototype; no broader scientific qualification is claimed.

Trust is bounded: hashes show consistency with a retained manifest and V5
input bytes, not signatures, rights or publisher authenticity. A malicious
replacement of both application and trust files is outside this check. There
is no arbitrary-upload/parser-hardening or broad public-service security claim.

Cold-load timings in the browser record are single local loopback automation
observations, not a performance study or SLA. The viewport matrix is layout
emulation on one Windows host, not OS/device coverage. The existing Linux and
Windows scientific CI remains a separate result from these new local tests.

**No blocking defect remains for continued local synthetic/Sierra review in
this scope.** The blocker to adding Madrid/the full two-real-case viewer is
**R1 OPEN**. Public deployment, data redistribution and product readiness are
outside this GO; no such action was performed. No INE consultation was sent.
