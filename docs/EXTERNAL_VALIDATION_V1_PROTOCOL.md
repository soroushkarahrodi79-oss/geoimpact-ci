# External Validation V1 — protocol and execution readiness

| Field | Value |
|---|---|
| Protocol version | 1.0 |
| Protocol status | Pre-registered; frozen by the first public commit containing this file |
| Pre-registration date | 2026-10-06 |
| Repository baseline | `f4745f934e7929b8b96278ba0460bc5c033c1da5` (`origin/main`) |
| Stable release under test | GeoImpact CI `v1.2.0`, Report V5 |
| Release tag target | `45237d7caaea2aa4b81359e46f1623918645078c` |
| External Validation V1 result | **PENDING — no independent evaluator has participated.** |

## Purpose and scope

This protocol evaluates whether an independent geospatial user can discover,
install, run, configure, and interpret the frozen GeoImpact CI v1.2.0 release.
It tests adoption and interpretation of the documented product contract. It
does not establish universal scientific validity, source-data correctness,
causality, or real-world impact.

GeoImpact compares BASE and CANDIDATE Polygon/MultiPolygon GeoJSON states with
fixed dependent Point GeoJSON features, using stable string IDs, OGC:CRS84
coordinates transformed to EPSG:25830, and exact `within` relationships.
PASS means the configured policy threshold was met; BLOCK means completed
analysis exceeded it; ERROR means analysis produced no policy verdict. A
verdict describes the configured inputs and policy only.

The materials in this protocol prepare an experiment. They contain no
participant results and do not claim that an external evaluation has occurred.

## Evaluator eligibility

### Suitable background

Recruit one or more people working as or training to become a GIS analyst,
geospatial researcher, spatial-data engineer, research software engineer, or
data analyst with practical GeoJSON/Python experience. Comparable practical
experience is acceptable. A GIS credential is not required.

The minimum skill profile is the ability to use a command line, create and
activate a Python virtual environment, install Python packages with `pip`,
work with files and folders, and read basic JSON or GeoJSON. Python 3.11 or
later and Git access are needed for the documented release path. Basic
familiarity with GeoJSON is expected; prior knowledge of GeoImpact is not.
Record the evaluator's broad experience bands rather than collecting a CV.

### Independence and exclusion

An eligible evaluator must not have authored or contributed code to GeoImpact,
designed its current architecture or analysis contract, or helped prepare this
protocol. They must not have been coached through the GeoImpact commands before
the session. For the new-case task, they must not already know a precomputed
GeoImpact result for the selected BASE/CANDIDATE/dependency combination or
have been shown its expected transition count, verdict, or report.

Prior general GIS, Python, GeoJSON, or spatial-analysis experience is
acceptable. Familiarity with the source dataset is acceptable if the evaluator
does not know the intended GeoImpact result for the selected case. Record such
familiarity before the new-case run. If an exclusion condition is discovered,
do not count that person toward the minimum sample; preserve any useful notes
as explicitly non-qualifying observations, with no identifying details.

## Frozen setup

1. Give each eligible evaluator an anonymous ID (`EV1`, `EV2`, …). Record the
   protocol version and the exact Git commit that first publishes this
   protocol.
2. Test only the `v1.2.0` tag/release. Use a clean environment and the public
   installation instructions. Do not use `main`, this documentation branch,
   an editable install from a modified checkout, or a later release.
3. Keep the same task wording and order below for every evaluator. Do not show
   them the facilitator's script, this protocol's answer rubric, expected
   fixture outcomes, or another evaluator's record during the session.
4. Before the new-case analysis, write down the source and selection basis,
   freeze the chosen inputs and config, and record hashes or another
   reproducible identity for each file. The selection basis must not use a
   GeoImpact result.
5. The Madrid census-section case and Sierra de Baza case are excluded from
   the new-case task. They may be used only as optional reproduction exercises
   after the new-case selection and run are preserved.

## Tasks and ordering

Use the exact prompts in the [facilitator script](EXTERNAL_VALIDATION_V1_FACILITATOR.md).
The evaluator should think aloud when comfortable. Do not correct an answer
before it is recorded. For every task, record completion, elapsed time if
practical, assistance level, commands, errors, confusion, and observations in
the [record template](EXTERNAL_VALIDATION_V1_RECORD_TEMPLATE.md).

### Task 1 — Understand the product from the landing page

Provide only the public repository URL. Ask the evaluator to use the landing
page and explain in their own words what GeoImpact does, what inputs it
compares, what PASS and BLOCK mean, and one major limitation. Record this
before they navigate elsewhere or receive clarification.

### Task 2 — Install the frozen release

Ask the evaluator to install v1.2.0 using the public README instructions in a
clean Python environment. Use the tagged source release/clone path. Record OS,
Python version, commands attempted, errors, whether any undocumented fix was
needed, and approximate time to a working v1.2.0 installation. Do not resolve
environment problems for them before recording them.

### Task 3 — Run an included fixture

Ask the evaluator to reproduce the included `tests/fixtures/geoimpact.yml`
example from the v1.2.0 checkout. Record how they find the command, whether
execution completes, the process exit status, whether the three documented
artifacts appear in the requested output directory, and how they interpret
those observations. In particular, record whether they treat exit code 1 as a
completed BLOCK analysis or as an operational failure. Do not prompt them with
the expected interpretation.

### Task 4 — Interpret a report

Ask the evaluator to inspect the report produced in Task 3 without an
introduction to its conclusion. Ask what changed, why the reported verdict
occurred, whether it proves a harmful real-world effect or causal relationship,
and what they would investigate next. Record their words and the report fields
they use to support the interpretation.

### Task 5 — Configure and execute a new case

The evaluator selects or brings a compatible case before seeing any GeoImpact
output for that case. Ask them to create or adapt a valid `geoimpact.yml` using
public documentation and to execute v1.2.0 on the new case. This task also measures
configuration comprehension: record whether they can identify required
fields, IDs, paths, CRS and predicate constraints, and policy threshold without
undocumented GeoImpact-specific help.

The case must use primary Polygon/MultiPolygon GeoJSON for BASE and CANDIDATE,
stable IDs, dependent Point GeoJSON, OGC:CRS84 coordinate inputs, EPSG:25830
analysis, exact `within`, and a fixed dependency layer. It must not be Madrid
census sections or Sierra de Baza. A zero-regression result is valid evidence;
there is no required nonzero result. Preserve the selected inputs, config,
provenance/source description, output artifacts, and hashes regardless of the
verdict. Do not discard, replace, or relabel a zero result as a failed case.

### Task 6 — Diagnose a controlled ERROR

Provide a copy of the known fixture config whose top-level schema `version`
has been changed from `1` to `2`. Ask the evaluator to run it and explain the
result. Record whether they identify an invalid configuration, understand that
ERROR produced no PASS/BLOCK policy verdict, and distinguish this from a
completed BLOCK. Do not reveal the malformed field before they inspect the
error.

### Task 7 — Assess practical usefulness

Ask the evaluator to name one realistic workflow where GeoImpact would be
useful or not useful, what decision it could inform, what additional evidence
would be required before acting, and a case where its current contract would
not fit. Record reasons and conditions, not a satisfaction score alone.

## New-case selection rule

Use these routes in order:

1. **Evaluator-owned or evaluator-selected compatible case.** The evaluator
   identifies a dataset they can lawfully use and selects the transition
   without running GeoImpact or inspecting an output. No confidential data is
   required. Do not copy private inputs into the repository or validation
   record.
2. **Evaluator-selected public case.** The evaluator chooses public sources
   and a pair/selection recipe without seeing GeoImpact results. Record source
   URLs or citations, snapshot dates, filters, conversion steps, and hashes
   needed for another person to understand the case.
3. **Project-prepared blind case.** This route is available only if the source
   selection rule, source/version, preparation recipe, and frozen input hashes
   are published before any evaluator session. No project-prepared blind case
   is designated by this protocol.

Before running GeoImpact on that case, record why the evaluator selected it and lock
the inputs/config by hash or equivalent. The selection must not be based on
whether GeoImpact is expected to PASS, BLOCK, or report nonzero regressions.
If the case proves incompatible, record the failure and reason; do not silently
substitute a project-author-selected case after seeing a result. A new case is
not a new filename or subset of Madrid or Sierra; it must be a distinct
spatial dataset/case not previously used as a GeoImpact scientific validation
case.

## Assistance policy

- **Level 0 — No assistance.** The evaluator uses public repository
  documentation. This is the default for discovery, installation, first
  execution, configuration, report interpretation, and ERROR diagnosis.
- **Level 1 — Clarification.** Only after the evaluator states and the
  facilitator records the difficulty. Permitted examples are explaining a
  generic Python/virtual-environment concept or confirming where a named
  output directory is on disk. A clarification must not supply a missing
  GeoImpact command, schema field, expected result, or interpretation.
- **Level 2 — Rescue.** A direct GeoImpact-specific instruction, correction,
  or troubleshooting step used only if the evaluator requests help or cannot
  continue after the problem has been recorded. Record the exact rescue and
  why it was needed. A task that needs Level 2 is not an unassisted success.

The evaluator may stop or skip a task. Do not pressure them to accept rescue.
If rescue is declined, preserve the failure and proceed only to tasks that do
not depend on the failed step.

## Data to record and privacy

Use one copy of the record template per evaluator and one sanitized aggregate
summary. Record only anonymous ID, date, broad role/background and
GIS/Python-experience bands, OS, Python version, release, task outcomes,
assistance, sanitized commands, errors, confusion, interpretation errors and
successes, blockers/friction, suggestions, facilitator observations, and
deviations.

Do not collect names, email addresses, employer names, precise location, CVs,
credentials, sensitive personal data, or private datasets. Do not record
audio/video or retain terminal screenshots by default. Redact usernames,
home-directory paths, tokens, and other incidental personal information from
command/error notes. Keep any private source data with its owner. Obtain
explicit permission before publishing an evaluator quote or identifiable
dataset description. Publish only anonymized, consented findings; never commit
raw private notes or confidential data.

This is product/usability validation, not a claim of formal human-subject
academic research or ethics/IRB approval. Do not describe participants as
research subjects. If results are later intended for formal human-subject
research publication, obtain a separate institutional ethics determination
before that work.

## Severity classification

Classify each observed finding using the highest supported severity and cite
the task evidence. A single issue may be counted once even if it appears in
multiple tasks; retain each occurrence in the record.

- **CRITICAL:** A documented release workflow cannot be completed in the
  documented/qualified environment because of a product or documentation
  defect; a documented command, used as documented, fails for that reason; a report is
  materially misleading; the public documentation encourages reading PASS as
  proof of correctness or real-world safety; a silent incorrect output is
  observed; or the stable release cannot reproduce its documented fixture.
- **MAJOR:** The evaluator needs undocumented GeoImpact-specific assistance;
  config semantics cause or nearly cause a wrong run; BLOCK is confused with
  an operational failure after public documentation; artifact purpose cannot
  be understood; or the README lacks information necessary for a task.
- **MINOR:** Wording, navigation, or command friction causes a brief delay but
  is recoverable from public documentation without a wrong run or rescue.
- **OBSERVATION:** A preference, use case, or enhancement idea without a
  demonstrated task failure.

An environment-specific failure outside the README's stated/qualified
environment is recorded, but is not automatically a CRITICAL product defect.
Do not downgrade a finding based on the evaluator's identity or the success of
another evaluator.

## Pre-registered decision rules

Apply these thresholds to all eligible evaluator records, including negative,
incomplete, and zero-regression outcomes.

### PASS

PASS requires all of the following:

1. At least **2 genuinely independent eligible evaluators** complete the
   protocol tasks or have every incomplete task fully explained in the record.
2. At least one evaluator completes the full workflow primarily at Level 0;
   any Level 1 clarification is logged and does not supply a missing
   GeoImpact-specific answer. No Level 2 task counts toward this condition.
3. No unresolved CRITICAL finding remains, and no confirmed MAJOR finding
   requiring a product or documentation change has been found. A confirmed
   MAJOR finding yields MODIFY pending a new evaluation of the change.
4. Both evaluators correctly distinguish PASS, BLOCK, and ERROR after using
   only public documentation: PASS is a completed policy result within
   threshold, BLOCK is a completed policy result over threshold, and ERROR is
   no policy verdict; they do not interpret PASS as proof of data correctness
   or real-world causality.
5. At least one genuinely new compatible case is executed and its result,
   including zero if zero, is preserved.
6. No scientific interpretation error is traceable to misleading project
   documentation, and the v1.2.0 known fixture is reproducible.

### MODIFY

Use MODIFY when real eligible evaluation has produced useful evidence but one
or more MAJOR adoption or interpretation findings require a documentation or
product change, with no evidence of materially incorrect analysis. Record the
finding and required action. Changes made in response to these results are
post-validation changes; they cannot be represented as fixes validated by the
same observations. A new protocol/release evaluation is needed to assess them.

### BLOCK

Use BLOCK when the tagged workflow or documented fixture cannot be reproduced,
outputs are materially incorrect, or project documentation leads to an unsafe
or scientifically invalid interpretation. Preserve the evidence and stop any
claim of adoption readiness until the issue is resolved and a new evaluation
is registered.

With fewer than two eligible evaluators, External Validation V1 is
**INCOMPLETE/PENDING**, not PASS. A demonstrated critical defect may be
reported as a provisional BLOCK before the minimum sample is reached. Do not
change these thresholds after seeing results to obtain PASS. The V1 result
describes this small falsification/usability exercise and is not a statistical
population estimate.

## Protocol deviations and result handling

Record each deviation with evaluator ID, task, what changed, why, who decided,
and likely effect. Do not change task order, assistance definitions, case
selection rule, severity, or decision thresholds after viewing participant
results. A safety or accessibility accommodation may be made and recorded; the
affected task is marked deviated and is not silently treated as standard
execution.

If protocol wording or execution must change after any participant has seen
it, publish a new protocol version and commit it before the next evaluator.
Keep earlier records attached to the version they followed; do not
retroactively score them under the new wording. Retain failures, skipped tasks,
negative findings, and zero results. Do not select only successful evaluators
or suppress findings.

## Materials

- [Structured evaluator record template](EXTERNAL_VALIDATION_V1_RECORD_TEMPLATE.md)
- [Recruitment brief](EXTERNAL_VALIDATION_V1_RECRUITMENT.md)
- [Facilitator script](EXTERNAL_VALIDATION_V1_FACILITATOR.md)
- [README product contract](../README.md)
- [v1 architecture](ARCHITECTURE_V1.md)
- [v1.2.0 release record](RELEASE_V1_2_0.md)

No messages have been sent and no evaluators have been recruited by this
protocol-preparation change.
