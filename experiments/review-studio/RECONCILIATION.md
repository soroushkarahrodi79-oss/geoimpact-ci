# Requirements reconciliation: PR #21 → documentary PR #22

2026-10-18. This is the controlling scope addendum. PR #22 remains a **Draft,
documentation/design/probe PR**. Functional development belongs to a separate
[Draft PR #23](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/23)
on `experiment/review-studio-local-v0-1`. No merge,
deployment, Madrid visual distribution or INE correspondence is authorized.

## Retained requirements and traceability

The complete [#21 specification](../../docs/REVIEW_STUDIO_FEASIBILITY_V0_1.md)
has been incorporated byte for byte from commit
`ae0244fae0032dba7f5a890476897056c7ef4cf5`. Its historical GO is read together
with this addendum: synthetic-only functional work is authorized; Sierra is
conditional on source-specific local-use evidence; Madrid stays HOLD with R1
OPEN. Earlier statements that all implementation waits for R1 refer to the
original Madrid + Sierra viewer, not this newly authorized restricted scope.

The [audit matrix](../../docs/review-studio-next-step-2026-10-18/INFORME.md)
maps every major #21 section to AUDIT, DESIGN and VALIDATION. These are design
requirements and prior technical results, not claims that a UI was already
built. F1 is documented by [VALIDATION](VALIDATION.md) and
[evidence-summary.json](evidence-summary.json); the named
`F1_ARTIFACT_INTEGRITY_GATE.md` is an index to that evidence. F2/F3 implementation
and UI tests are recorded only in the separate functional PR. F4 external
usefulness remains pending and separate from External Validation V1.

The following are binding additions to DESIGN:

- Trace every displayed scientific value to a report JSON pointer. Each row
  joins by `(dependent_dataset, dependent_id)` and every regression joins to
  its existing `evidence_id`; sources and dates remain curated metadata.
- Provide a before-array → after-array transition filter. It only selects
  existing relationship rows; it never infers splits, merges or renames and
  never changes scientific totals or policy. The 26-pair Madrid acceptance
  example remains deferred under R1; exercise the same control on synthetic
  data. Empty arrays and multiple assignments must remain intact.
- Test all five requested CSS viewports: **1440×900, 1440×1000, 834×1112,
  375×812 and 390×844**, plus 320 px reflow and 200% zoom. Browser emulation
  is not a physical-device test; drawings are not screenshots.
- Preserve Sierra's historical **Gate 8 MODIFY** research conclusion: the
  initial nonzero-regression objective was unmet. Its reproducible PASS/0 is
  a negative control and does not replace that historical research decision.
- Preserve projected footprint omission, exact-byte verification, explicit
  missing/mismatch/not-checked states, a non-map list alternative, fixed point
  locations, original scientific artifacts and the prohibition on JS science.

J1/J2 are scoped to synthetic cases and, if cleared for local use, Sierra.
Their original Madrid examples are retained as future requirements and are
not claimed to pass. J3–J5 apply unchanged within the permitted cases. An
analysis ERROR has no report verdict; a load/integrity ERROR must not show a
stale PASS/BLOCK, map or relationships from the previous case.

PR #21 remains open. This reconciliation demonstrates design coverage and
preserves the specification; it is not independent approval to close it.

## Publication and evidence review

The Spanish audit, INE draft and HTTP/GitHub evidence were read in full.
The published evidence copy removes commit-author personal metadata while
retaining commit OIDs, URLs, checks and retrieval dates. Its redaction record
retains the SHA-256 of the original local document; that original is not
included. There are no machine-specific absolute paths, tokens or private
contact details in the copied documents. Placeholder sender fields in the
INE draft remain placeholders. Source-provider organization names are retained
because attribution is required.

Source observations were checked against the official INE collection footer,
legal notice and metadata, and REDIAM source conditions. INE's visible BY-SA
label links to BY, so R1 remains OPEN. Current source conditions do not prove
past publisher authenticity; byte hashes do not establish permission.

The previous Spanish report's proposal for one combined principal PR is
historical. The user's later instruction supersedes it: **#22 documentary;
separate functional Draft PR**, mutually linked. No code is added to #22.
