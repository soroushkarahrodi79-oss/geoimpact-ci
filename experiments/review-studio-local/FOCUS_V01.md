# V01 / P1-01 — focused controls behind the nonmodal tour

2026-10-19. Scoped correction in functional Draft PR #23; original audit in
[Draft PR #24](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/24)
continues to describe **32f3ab50bb8a91d21118610bfc135b33e3fb2f3c**. No other UX
finding is implemented here. No participants or human results exist.

## Cause and bounded change

Native Tab scrolling considers the whole viewport, including the fixed guide
dock. Highlighting the tour target did not protect the independently focused
application control. On focus, the onboarding module now scrolls that control
into the space above the dock, with an 8px gap. Resizing also reveals retained
focus. A map taller than the available space exposes its top and keyboard focus;
this patch does not promise that an oversized map fits in one screen.

The tour/practice remains nonmodal. No focus reassignment, Tab interception,
keyboard trap, inert application, CSS/layout redesign or scientific calculation
is added. Manual scrolling remains free; the next focused control is revealed.
Modal welcome/Help and closed/paused tours are excluded from this adjustment.

## Reproduce

Prepare the local server with the existing README, then from this experiment:

```powershell
npm test
npm run test:browser
npm run test:onboarding
npm run test:focus -- --baseline
npm run test:focus
```

`STUDIO_URL` may select another loopback port. `STUDIO_CHROMIUM_EXECUTABLE` may
select an installed Chromium; otherwise use the existing Playwright install.
The baseline test serves only the original onboarding module from its exact Git
blob inside an isolated browser response. Six other interface files must match
that commit. It neither switches the checkout nor changes server/scientific
bytes. Baseline failure reproduction is an expected successful test outcome.

## Executed evidence

Windows; Node 24.11.0, Playwright 1.56.1, headless Chromium 153.0.8010.12.
Six viewports: 1440×900, 1440×1000, 834×1112, 375×812, 390×844 and 320×812.

| Check | Actual result |
|---|---|
| Original 50 Tab presses per size | Covered events **8 / 0 / 4 / 15 / 15 / 17**, total **59**; matches the historical audit. |
| Additional original 50 Shift+Tab per size | 0 covered events; this direction is new baseline evidence. |
| Corrected matrix | **86 sequences / 1,900 key presses, zero completely covered or entirely offscreen focused controls**. |
| Matrix actions | Tab/Shift+Tab, manual wheel/PageUp, map step, live resizing, ES/EN, practice, CSS zoom 200% at every size. |
| Native page zoom 200% | 1440×1000 browser viewport: effective 720×500, devicePixelRatio 2, CSS zoom 1; 50 Tab + 50 Shift+Tab, zero hidden focus. |
| Existing unit and browser tests | **26 unit tests, 12 workspace groups, 18 onboarding groups passed**. Actual hotel_813 practice, Escape/focus restoration, maps, filtering, PASS with changes, BLOCK, analysis/load/integrity ERROR and Sierra 52/0 retained. |
| Existing scientific tests | **113 passed**, no failed/skipped tests. |
| Frozen v1.2.0 verifiers | PASS/BLOCK/ERROR contract verifiers and all **nine canonical output hashes match** (synthetic, Madrid, Sierra). Madrid runs only as the existing scientific CLI regression check; it is never served by this viewer. |
| Data and boundaries | All 27 prepared local scientific/manifest files unchanged against the before-work snapshot; protected tracked scopes unchanged. No external runtime requests or ordinary browser errors in the final runs. |

[Raw before](qa/focus-v01/before.json), [raw after](qa/focus-v01/after.json),
[commands/output](qa/focus-v01/commands.log), [scientific commands/output](qa/focus-v01/engine-checks.json)
and [source/data/screenshot identities](qa/focus-v01/validation.json) retain
engineering evidence. The acceptance check measures actual focus geometry and
hit testing after two animation frames, checks access to application controls
outside the guide and checks Escape restoration. It does not infer accessibility
from screenshots alone.

Real synthetic before/after captures use the same key positions:

| Size and focus | Before | After |
|---|---|---|
| 1440×900, Tab 12, fit-all | [covered](qa/screenshots/focus-v01/before-1440x900.png) | [visible](qa/screenshots/focus-v01/after-1440x900.png) |
| 834×1112, Tab 33, original report download | [covered](qa/screenshots/focus-v01/before-834x1112.png) | [visible](qa/screenshots/focus-v01/after-834x1112.png) |
| 390×844, Tab 9, provenance link | [covered](qa/screenshots/focus-v01/before-390x844.png) | [visible](qa/screenshots/focus-v01/after-390x844.png) |

[Native 200% capture](qa/screenshots/focus-v01/after-native-zoom-200.png).
Visual inspection confirms the selected control is visible above the dock in
the desktop/tablet/mobile after captures. These new records do not overwrite
the original PR #24 traces or captures.

## Decision and limits

**GO to start the bounded, moderated local study on the exact corrected commit
pinned by PR #24**, after its ordinary consent/access/environment preflight.
If covered focus recurs, stop the affected task and record the defect and help
given; do not score it as unassisted success. Other audit findings remain pending
human validation; this patch is not a redesign or evidence of comprehension.

Viewport emulation is not physical-device testing. Native page zoom here is an
automated desktop Chromium profile setting, not a human toolbar interaction;
CSS-zoom results are labelled separately. No screen-reader validation, WCAG
conformance or human usability outcome is claimed. GeoImpact CI v1.2.0, CLI,
Report V5, fixtures and scientific results remain intact. **R1 OPEN / full
Madrid viewer HOLD**. No merge, deployment, public demo or participant contact.
