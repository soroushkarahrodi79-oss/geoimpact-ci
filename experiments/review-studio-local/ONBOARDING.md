# Guided onboarding V1 — local implementation

**GO for local synthetic onboarding review. R1 OPEN; the full Madrid viewer
remains HOLD.** This is an update to functional [Draft PR #23](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/23),
not a finished product or a public service. No engine, fixture, policy, V5
contract, source geometry or scientific CI changes.

## Inspected implementation and lifecycle

Inspection started at functional commit
`339b7cdf64d2ca27db1690dfb18b22a885b128e7`. The complete existing `index.html`,
`app.js`, `reader.js`, `style.css`, both original test files, README and VALIDATION
were read before implementation. The documentary [DESIGN](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/47994cf11ce0e229176a419539da93e40114caad/experiments/review-studio/DESIGN.md)
and reconciliation in PR #22 remain the reference for J1–J5; that PR is not
modified here. Its Madrid acceptance examples remain outside this local GO.

`changeCase()` hides the previous scientific view before verifying files.
Only a verified V5 bundle followed by a visible `#completed` is ready for
onboarding. Reader errors and recorded analysis ERROR clear normal review.
Selection and language changes rebuild evidence and other DOM content, so
the guide resolves semantic targets again instead of retaining stale nodes.
There is one language owner, `app.js` state; both guide language controls
delegate to the existing header control.

| Tour step | Actual semantic target | Small-screen fallback when the whole section cannot fit |
|---|---|---|
| 1 Purpose | `#heading`, `data-tour-target="purpose"` | Same heading |
| 2 Case | `#case`, `case` | Same native select |
| 3 Verdict and totals | `#policy-summary`, `verdict`, contains strip and `#stats` | Actual verdict strip |
| 4 Maps | `#review`, `maps` | Actual shared `.map-tools`, `map-controls` |
| 5 Search and filters | `#relationships`, `relationships` | Actual `#search` |
| 6 Evidence | `#evidence`, `evidence` | Actual evidence heading |
| 7 Provenance | `#provenance`, `provenance` | Actual provenance heading |
| 8 Interpretation | `#interpretation-limits`, `limitations` | Same real subsection, not the entire provenance card |

No positional selector is used. Practice also uses semantic search/list/file
targets and the existing composite dataset/ID identity. The highlighted
fallback belongs to the real section; it is not a duplicate demonstration.

## Four integrated experiences

The welcome is an opt-in native dialog after readiness. Its three actions
start the tour, persist dismissal, or postpone. The tour is a nonmodal dock:
the actual controls, maps and keyboard remain available. It shows eight
numbered, announced steps, highlights an available target, scrolls that target
above the dock and provides Back, Next, Skip, Escape and an explicit
go-to-section action. The final step offers Finish or the optional exercise.

Header **Ayuda / Help** always opens information, policy explanations and the
eleven-term glossary, including on ERROR. It also restarts the tour/practice,
reopens welcome and navigates to actual limitations when valid. The project
issue link is an explicit user action; merely opening Help makes no external
request. There is no analytics, account, CDN, API or remote asset.

The supplied approved ES/EN welcome, eight steps, cautions, five practice
instructions, completion text and menu are retained in
[`web/onboarding-copy.js`](web/onboarding-copy.js). No approved scientific
wording was changed. Additional bilingual text explains hints, unavailable
targets, recovery, the previous case and a short policy interpretation
question. Glossary translations preserve the specified meanings and technical
tokens. The original application's translation owner is reused; no competing
global language state is added.

## Exercise: observed state, not simulated progress

The guide reads the already verified released fixture through a small
read-only UI bridge. It checks its identity, V5 version and recorded
BLOCK/2/1 values; it never derives a verdict from those values. A failed check
keeps the current step with a hint and explicit skip. Nothing changes the
report, geometry, scientific selection rules or filters automatically.

| Action | Required observable condition |
|---|---|
| Choose synthetic BLOCK | Verified `synthetic-block`, Report V5, original BLOCK with observed 2 and threshold 1. Already active is acceptable. |
| Search | Actual search is `hotel_813` and the actual visible composite row `["hotels","hotel_813"]` exists. A wrong ID or a filter hiding it cannot pass. |
| Select and inspect | Actual selected record is hotels/hotel_813, its retained BEFORE is `["chamberi"]`, AFTER `["tetuan"]` and its existing regression evidence ID is available. Focusing a row alone cannot pass. Selection brings actual evidence into view. |
| Interpret BLOCK | User deliberately visits the result and chooses the threshold interpretation. Clicking Check alone or selecting harm/movement cannot pass. |
| Trace source | User deliberately locates the original `report.json` row or activates its real provenance link; the identity row is visible and five recorded engine versions are rendered. No download is required. |

The evidence ID remains
`relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49`.
These checks are specific to the released tutorial fixture, not an arbitrary
report validator. The unchanged reader remains the bundle authority.

Starting practice clearly announces the required case. The user changes case
through the normal selector. The previous case ID is held only in memory;
completion and exit provide an explicit return action when needed. That action
uses the ordinary case lifecycle and clears obsolete selection as usual.
Practice does not silently preserve/reset a previous case's filters. Back and
Help retain the exercise step. Closing Help restores its invoking focus;
the guide's go-to-section action returns to the task if focus restoration
has scrolled to the header.

## Persistence, focus and exceptional states

Only `geoimpact:review-studio:onboarding:v1` is used: localStorage contains
`{"status":"dismissed"}` or `{"status":"completed"}`; sessionStorage contains
only `seen`. No user ID, dataset, hash, evidence or selected case is stored.

| Action | Behavior |
|---|---|
| Start | Opt-in tour; marks the current session as offered. |
| Explore on my own | Persistent dismissal; no later automatic welcome. |
| Not now / welcome close / welcome Escape | Session postponement; a new browser session can offer welcome again. |
| Skip tour | Persistent dismissal; never reported as completion. |
| Tour close / Escape | Session postponement; never completion. |
| Finish tour | Persistent completion after the available eighth target. |
| Complete practice | Persistent completion only after all five real gates pass; skipping does not mark completion. |
| Help → Restart | Always available with a valid case, regardless of saved completion/dismissal. |
| Storage unavailable | Page-local fallback; Help and the exercise continue to work. Persistence cannot be guaranteed. |

Native modal semantics, an explicit Tab/Shift+Tab boundary, focus restoration,
Escape and visible focus are implemented. The nonmodal guide deliberately
does not trap keyboard focus. The dock reserves scroll space, caps its height
and scrolls its own long copy. Resizing recalculates placement; small-screen
snapshot tabs remain the application's controls. Reduced-motion mode needs no
animation. All information is text or a reachable control, without hover.

A missing/hidden target or invalid/loading case removes highlighting, explains
unavailability and disables advancing/completion. Rechecking or restoring the
real target resumes the same step. ERROR cannot launch welcome or a new tour;
an active tour pauses. Safe Help/glossary remain available. Changing language
preserves progress and source identities. Sierra is not a practice fixture:
its valid zero-regression export still has 52 relationships, and the guide
does not invent an evidence ID for an unchanged relationship.

## Acceptance objectives and interpretation limits

| A novice should be able to answer | Design/automated evidence |
|---|---|
| What problem does Studio solve? | Welcome and step 1 explain review of previously analysed changes, not prediction/editing. |
| BASE versus CANDIDATE? | Step 4 explains the reference/second snapshot and fixed points; existing snapshot/camera tests remain passing. |
| What changed for hotel_813? | Real selection gates and rendered arrays show chamberi → tetuan; no point movement is inferred. |
| Why BLOCK? | Retained 2/1 result plus deliberate policy question; wrong harm/movement answers fail the exercise gate. |
| Can PASS contain regressions? | Step 3, Help status and glossary; existing synthetic PASS remains 2 regressions with threshold 2. |
| Where does the result come from? | Step 7 and actual report identity interaction, versions, configuration and unchanged source downloads. |
| What conclusions are unsupported? | Step 8 and cautions exclude legal effects, displacement, causality, harm and absolute accuracy; hashes are not authenticity signatures or reuse licences. |

These are design and automated acceptance objectives, **not evidence of human
comprehension**. Selecting the correct answer is not proof that someone
understood the science. Independent novice testing and assistive-technology
assessment remain future validation work. No screen-reader, physical-device,
browser-chrome zoom, cross-browser, WCAG certification or real-user study is
claimed. Testing uses actual headless Chromium, viewport emulation and 200%
CSS zoom emulation on Windows.

The dock may require internal scrolling for long bilingual explanations on
narrow screens. Large sections connect through a real smaller anchor; users
still scroll the original section to inspect everything. Hash matching
establishes retained byte identity, not publisher authenticity, rights or
source correctness. The original affine map and temporal/source limitations
remain in force. No external human reviewer has independently approved this
implementation; this record is an engineering self-review with reproducible
acceptance evidence in [VALIDATION](VALIDATION.md).

There is no blocking defect identified for this bounded local onboarding.
**R1 OPEN is the blocker to adding Madrid/the full two-real-case viewer.**
No INE geometry is used by the exercise or committed screenshots, no scientific
data is published, and no merge, deployment or correspondence is performed.
