# External Validation V1 — evaluator record

Duplicate this file once per eligible evaluator. Use an anonymous ID only.
Complete the protocol/version fields before the session and retain all
failures, skipped tasks, zero results, and deviations. Sanitize paths and
personal details before storing or sharing notes. Do not attach private input
data.

## Session metadata

| Field | Record |
|---|---|
| Anonymous evaluator ID | `EV__` |
| Session date (`YYYY-MM-DD`) | |
| Protocol version | `1.1` |
| Initial protocol candidate | `1.0` / `11cd26f8614734588756e97ebeb429225c21f0e1`; no evaluator participated under it |
| Final protocol freeze commit SHA (final PR #20 head) | |
| Software under test | `GeoImpact CI v1.2.0`, Report V5 |
| Software tag target SHA | `45237d7caaea2aa4b81359e46f1623918645078c` |
| Documentation/adoption surface commit SHA | `f4745f934e7929b8b96278ba0460bc5c033c1da5` |
| Pinned README permalink | `https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/f4745f934e7929b8b96278ba0460bc5c033c1da5/README.md` |
| Documentation tree permalink | `https://github.com/soroushkarahrodi79-oss/geoimpact-ci/tree/f4745f934e7929b8b96278ba0460bc5c033c1da5/docs` |
| Eligible under protocol? | Yes / No / Unclear |
| Exclusion check completed before tasks? | Yes / No |
| Broad role category | GIS analyst / researcher / spatial-data engineer / research software / data analyst / other broad category |
| GIS or spatial-data experience | <1 year / 1–3 years / 4–7 years / 8+ years / prefer not to say |
| Python experience | None / basic / regular / advanced / prefer not to say |
| Command-line and virtual-environment experience | None / basic / regular / advanced / prefer not to say |
| Operating system and version | |
| Python version | |
| Prior GeoImpact knowledge/use | None / read public docs / used release / other; describe without personal detail |
| New-case source familiarity before run | None / general / familiar; no expected GeoImpact output known? Yes / No |
| New-case prior GeoImpact run or expected output known? | No / Yes (if yes, case task is non-qualifying) |
| Prior exposure to `EXTERNAL_VALIDATION_V1_PROTOCOL.md`? | No / Yes; when and which material: |
| Prior exposure to `EXTERNAL_VALIDATION_V1_FACILITATOR.md`? | No / Yes; when and which material: |
| Prior exposure to previous evaluator records? | No / Yes; when and which material: |
| Prior exposure to internal scoring/rubric material? | No / Yes; when and which material: |
| Contamination assessment for Tasks 1, 4, and 6 | None / Task 1 / Task 4 / Task 6 / multiple; explain: |
| Consent to retain anonymized product feedback | Yes / No |
| Consent to publish anonymized quotes (optional) | Yes / No |

## Task record

For each row, record completion as `complete`, `partial`, `failed`, `skipped`,
or `not run`. Assistance: `L0`, `L1`, `L2`, or `deviated`. Add details below;
do not omit negative outcomes.

| Task | Completion | Assistance | Approx. time | Severity finding(s) | Evidence/note reference |
|---|---|---|---:|---|---|
| 1. Product understanding | | | | | |
| 2. Install v1.2.0 | | | | | |
| 3. Included fixture | | | | | |
| 4. Report interpretation | | | | | |
| 5. New case and config | | | | | |
| 6. Controlled ERROR | | | | | |
| 7. Practical usefulness | | | | | |

### Task 1 — initial, uncorrected responses

- What GeoImpact does:
- Inputs it compares:
- What PASS means:
- What BLOCK means:
- One major limitation:
- Correct understanding after public documentation, if different:

### Task 2 — installation

- Clean environment and documented route used:
- Commands attempted (sanitize machine-specific paths):
- Install success/failure and installed package version evidence:
- Errors and undocumented fixes:
- Time to working installation, if measured:

### Task 3 — known fixture

- Commands attempted:
- Process exit status:
- Did execution complete? How did evaluator decide?
- Were `report.json`, `report.md`, and `relationship-regressions.geojson` found?
- Output-directory understanding:
- Evaluator's interpretation of exit status and verdict:

### Task 4 — report interpretation

- What changed, according to evaluator:
- Why the report gave its verdict:
- Report fields used as evidence:
- Does this prove real-world harm, causality, or source-data correctness? Why?
- What evaluator would investigate next:
- Interpretation mistakes and successful corrections after public docs:

### Task 5 — new case and configuration

- Case name/category (no confidential detail):
- Distinct from Madrid and Sierra? Yes / No:
- Route used: evaluator-owned / evaluator-selected public / pre-registered blind:
- Source/version/snapshot date or private-data note:
- Selection basis recorded before any GeoImpact output for this case? Yes / No:
- Config and input identities/hashes recorded before run? Yes / No:
- CRS84 primary and dependency inputs; EPSG:25830 analysis; polygon/point types; stable IDs; fixed dependency; exact `within` confirmed? Yes / No / Unknown:
- Config fields/semantics understood without undocumented GeoImpact help? Yes / No; details:
- Result/verdict, including zero if zero:
- Output artifact identities/hashes and storage location (no private data):
- Source/data limitations stated by evaluator:

### Task 6 — controlled ERROR

- Error observed:
- Evaluator's explanation:
- Did they state that ERROR has no PASS/BLOCK policy verdict? Yes / No:
- Did they distinguish ERROR from a completed BLOCK? Yes / No:
- Evaluator's no-hints definitions of PASS, BLOCK, and ERROR after public docs:
- Did they state that PASS does not prove correctness or real-world impact? Yes / No:

### Task 7 — practical usefulness

- Realistic workflow where useful or not useful:
- Decision it could inform:
- Additional evidence needed before action:
- A workflow outside the current contract:

## Cross-task observations

- Total CRITICAL findings:
- Total MAJOR findings:
- Total MINOR findings:
- Total OBSERVATION items:
- Critical blockers:
- Non-critical friction:
- Evaluator suggestions (preserve their meaning; distinguish quote from summary):
- Facilitator observations:
- Commands attempted and errors (sanitized; attach continuation if needed):
- Documentation confusion:
- Interpretation errors:
- Successful interpretations:

## Assistance log

| Task/time | Level | Evaluator problem recorded before help? | Exact clarification/rescue | Effect on task result |
|---|---|---|---|---|
| | | | | |

## Protocol deviations

| Task | What changed | Reason/decision | Expected effect | How classified |
|---|---|---|---|---|
| | | | | |

## Finding register

| Finding ID | Severity | Task/evidence | Reproducible? | Product/documentation link | Status/action owner |
|---|---|---|---|---|---|
| | | | | | |

## Evaluator-level conclusion

- Eligible result included in V1 sample? Yes / No; reason:
- Core tasks 1, 2, 3, 4, 6, and 7 all completed? Yes / No:
- Any Level 2 rescue on a core task? Yes / No; task(s):
- Tasks 1, 4, and 6 free of material rubric contamination? Yes / No; details:
- Qualifying core-workflow record for PASS? Yes / No; reason:
- PASS/BLOCK/ERROR distinguished correctly after public documentation? Yes / No:
- New compatible case executed and preserved? Yes / No:
- Did this evaluator's new case count toward the one-case PASS criterion? Yes / No:
- Unresolved CRITICAL or MAJOR findings:
- Evaluator record status: complete / incomplete / non-qualifying:
- Voluntary withdrawal? Yes / No; record that withdrawal alone is not a product finding:
