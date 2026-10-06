# External Validation V1 — facilitator script

Use this script with the frozen [protocol](EXTERNAL_VALIDATION_V1_PROTOCOL.md).
The facilitator records observations but does not act as an evaluator. The
author may facilitate a session but must not be counted among the evaluators.

## Before the session

1. Confirm the evaluator meets the protocol's skill and independence
   requirements without asking for names, employer, CV, or sensitive details.
2. Create an anonymous ID and blank [record](EXTERNAL_VALIDATION_V1_RECORD_TEMPLATE.md).
3. Prepare the task-6 invalid config by copying
   `tests/fixtures/geoimpact.yml` from tag `v1.2.0` and changing only its
   top-level `version: 1` to `version: 2`. Keep it hidden until Task 6.
4. Do not prepare or select the evaluator's new case. The evaluator selects or
   brings it under the protocol rule. Do not prepare a new-case expected result.
5. Do not display this script, internal answer rubric, other evaluator notes,
   or private expected outcomes. Do not modify the release or task wording.

## Opening — read verbatim

> Thanks for taking part. Today we are evaluating the GeoImpact v1.2.0
> software and its public instructions, not testing you. Please say what you
> are thinking when that is comfortable, including when something is unclear.
> I will not explain GeoImpact or correct your interpretation during the
> tasks. If you get stuck, say so; I will record the problem before offering
> any allowed help. You may pause, skip a task, or stop at any time. Please do
> not use confidential data. I will take anonymous written notes only; I will
> not record audio or video. I will not publish a quote or identifiable case
> detail without your explicit permission. Your participation is not an
> endorsement of GeoImpact. Is it okay to continue and retain anonymized
> product feedback?

If they decline permission to retain feedback, stop note collection and end
the session. Do not treat this as a negative finding.

## Task prompts and facilitator behavior

### Task 1 — product understanding

Give only the repository URL. Say:

> Please use the repository landing page and tell me, in your own words, what
> GeoImpact does, what inputs it compares, what PASS and BLOCK mean, and one
> major limitation.

Remain silent while they read and answer. Do not point at README sections or
repeat the prompt with hints. Record their first answer verbatim or as a close,
clearly marked summary before they navigate elsewhere.

### Task 2 — install v1.2.0

Say:

> Please install the tagged GeoImpact CI v1.2.0 release using the public
> repository instructions in a clean Python environment. Tell me when you
> believe it is ready.

Do not suggest commands, troubleshoot, or tell them how to verify the version
before the problem and attempted steps are recorded. Record OS, Python
version, commands, time if practical, and each error. Do not silently update
Python, packages, Git settings, or environment variables.

### Task 3 — known fixture

Say:

> From the v1.2.0 checkout, please reproduce the included fixture described in
> the README. Tell me when execution has finished and explain what you think
> happened.

Do not tell them the expected exit status or verdict. Let them locate the
command, run it, inspect the output, and identify the output directory. Record
whether they see all three artifacts and whether they understand a completed
BLOCK can return a nonzero process code.

### Task 4 — report interpretation

Say:

> Please inspect the report from that run. What changed, why did it receive
> that verdict, does it prove harmful real-world impact or causality, and what
> would you investigate next?

Do not paraphrase the report for them or validate their answer during the
task. Record which fields they use and their uncorrected interpretation.

### Task 5 — new case and config

Say:

> Please choose a compatible case that has not been used as a GeoImpact
> scientific validation case. Before running GeoImpact on that case, tell me
> the source and why you selected it, then save the inputs and config you plan
> to use. Please create or adapt the config and run the tagged release using
> the public documentation. A zero result is fine.

Do not suggest candidate datasets, field names, config values, filters,
expected outputs, or a likely verdict. Confirm only whether the case is one of
the excluded Madrid/Sierra cases or whether the evaluator has already seen an
expected GeoImpact result; if either is true, record the task as
non-qualifying. Record source/selection basis and hashes before execution.
Never ask the evaluator to disclose private input data. If preparation is too
large or the case is incompatible, record that and stop or reschedule; do not
substitute an author-picked case.

### Task 6 — controlled ERROR

Provide the prepared config with `version: 2` and say:

> Please run this configuration with the v1.2.0 CLI and explain the result.

After the evaluator has explained the error, ask without hints:

> Based on the public documentation and what you observed, what do PASS, BLOCK,
> and ERROR each mean? Does PASS prove the data are correct or that a real-world
> impact occurred?

Do not point out the changed field. Record whether they distinguish an
operational/configuration ERROR from a completed BLOCK, whether they
understand no policy verdict was produced, and their explanation of all three
outcomes. Ask the follow-up only after their initial ERROR explanation has
been recorded.

### Task 7 — usefulness

Say:

> What is one realistic workflow where GeoImpact would or would not be useful?
> What decision could it inform, what other evidence would you need before
> acting, and what kind of case would not fit its current contract?

Do not steer them toward a positive use case. Record their reasoning and
conditions, not a satisfaction score alone.

## Silence, neutral prompts, and assistance

During a task, wait without filling pauses. Neutral prompts are limited to
“What are you thinking now?”, “What would you try next?”, and “Please say when
you feel stuck.” Do not answer the problem inside a neutral prompt.

For any help request, first ask the evaluator to describe what is blocking
them and record it. Then:

- **Level 0:** remain silent; they use public docs.
- **Level 1:** only generic Python environment clarification or output-folder
  location confirmation after recording the problem. Do not provide a
  GeoImpact-specific command, schema field, expected output, or interpretation.
- **Level 2:** only if requested or the evaluator cannot continue after the
  issue is recorded. State the exact intervention and record it. Mark that
  task rescued, not unassisted.

Do not coach, debug silently, operate the evaluator's computer, show a
successful terminal, or explain expected results. Never change the
pre-registered thresholds or case rule during a session.

## Think-aloud notes

Take written notes against the task and anonymous ID. Separate exact evaluator
words from facilitator summaries and later interpretation. Note time and
observable actions where useful: navigation choice, command attempted, error,
pause, reread, correction, or request for help. Do not infer competence or
motivation. Do not capture screens, audio, video, names, employer, or local
paths by default. Redact incidental personal information from notes.

## Installation failure and stopping

If installation fails, let the evaluator finish explaining and record the
commands/error before offering rescue. Do not patch the installation or switch
to another branch. Ask whether they prefer to stop or continue with tasks that
do not require that installation. Mark dependent execution tasks not run or
rescued; do not count a facilitator-provided install as an unassisted success.
If they stop, retain the installation finding and do not pressure them to
continue.

Stop immediately if the evaluator asks, if confidential data is exposed, or if
the session would require revealing a new-case expected result. Record only a
minimal deviation and do not retain exposed private data. A task may be skipped
without penalty. Do not select a replacement evaluator based on whether this
person succeeded.

## Close

Ask whether the evaluator has a final observation or suggestion. Thank them
without endorsing or disputing their conclusions. Confirm the record contains
no identifying details and that quotes/case descriptions will not be
published without explicit permission. Do not promise a specific change or
outcome during the session.

This is product/usability validation; do not claim IRB/ethics approval or refer
to the evaluator as a research subject. A later formal human-subject research
publication requires a separate institutional ethics determination.
