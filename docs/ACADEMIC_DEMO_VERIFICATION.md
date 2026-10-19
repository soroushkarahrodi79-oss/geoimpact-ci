# Private Academic Demo V1 — verification record

Date: 2026-10-19. Base: Draft PR #23 commit
`4133c2262fb16546a0dd41f09dd5a6a92b64c100`. Frozen engine: GeoImpact CI
1.2.0 commit `45237d7caaea2aa4b81359e46f1623918645078c`.

This record separates completed local evidence from checks that require an
owner-approved real host. A future run must replace PENDING with recorded HTTP
and browser evidence; it must not relabel it PASS in advance.

## Reproduction

From the repository root, export/install the exact `v1.2.0` tag as described in
`experiments/review-studio-local/README.md`. Then run:

```powershell
work/studio-venv/Scripts/python.exe experiments/review-studio-local/prepare.py --engine work/release-engine
python experiments/review-studio-local/build_demo.py
python experiments/review-studio-local/verify_package.py
cd experiments/review-studio-local
npm ci
npm test
```

The static output is deterministic except for a future intentional source
change: `academic-demo-dist/package-manifest.json` pins every deployed byte.

## Results

| Requirement | Status | Actual evidence |
|---|---|---|
| Static package allowlist, hashes and Report V5 | PASS | `verify_package.py` accepted exactly 32 files / 152,501 bytes and all package SHA-256/size entries; BLOCK/PASS reports are V5 from engine 1.2.0. |
| Nine scientific reference hashes | PASS | Frozen release verifiers accepted three synthetic BLOCK, three Madrid benchmark and three Gate 8 output hashes. The six real-case artifacts were generated only in ignored release QA output and are not packaged. |
| Real-data exclusion | PASS | Exact package set verified; known real-case markers absent; only the three synthetic case IDs accepted. Fail-closed probes confirmed rejection of both an unexpected file and an excluded-data reference. |
| Secrets/unexpected files/external requests | PASS (local/package) | Secret-pattern and file-set scan passed; no analytics/telemetry; browser ordinary flows made zero external runtime requests. Real authentication-origin behavior is PENDING. |
| ES/EN | PASS | Bilingual unit and browser assertions cover welcome, tour, practice and main interface. |
| Eight-step tour and `hotel_813` practice | PASS | 17 onboarding acceptance groups completed all gates, evidence and return flow. |
| Maps, filters, selection and original evidence | PASS | 11 browser acceptance groups completed BASE/CANDIDATE, camera, filters, record selection and downloads. |
| PASS/BLOCK/ERROR | PASS | Frozen CLI contract and browser state checks passed; ERROR has exit 2, no report and no verdict. |
| Keyboard, focus, mobile and zoom | PASS with limits | 86 focus traversals reported zero hidden/offscreen controls. Automated Chrome viewports 1440×900, 1440×1000, 834×1112, 375×812, 390×844 and 320×812 plus 200% CSS/native zoom checks passed. No physical-device, cross-browser or screen-reader certification is claimed. |
| Direct unauthenticated asset routes | **PENDING** | Requires real Access-protected host. Must test every hostname and representative direct data/file path before publication. |
| Engine integrity | PASS | Frozen v1.2.0: 113 pytest tests passed in 129.32 s; PASS/0, BLOCK/1, ERROR/2 contract checks passed. Protected engine/source paths have no diff from the frozen PR #23 base. |
| Report V5 integrity | PASS | Package reader validates report version, engine identity, input identities, joins and report/export agreement without recalculation. |

## Exact executed commands

The final PR record must retain command exits and counts for:

```text
python build_demo.py
python verify_package.py
npm test
npm run test:browser
npm run test:onboarding
npm run test:focus
python -m pytest -q                         # frozen v1.2.0 export
python scripts/verify_ci_contract.py pass   # frozen export
python scripts/verify_ci_contract.py block
python scripts/verify_ci_contract.py error
python scripts/verify_ci_contract.py hashes
python scripts/verify_madrid_benchmark.py   # verification only; never packaged
python scripts/verify_gate8_case.py         # verification only; never packaged
```

Reference values are recorded in
`experiments/review-studio-local/scientific-reference-hashes.json`. That file is
QA metadata and is not in the deployable allowlist.

Environment: Windows, Python 3.12.10, Node 24.11.0, Playwright 1.56.1 and
Google Chrome 155.0.8059.80. Unit result: 25 passed, 0 failed and one
deliberately skipped historical real-case test because that case is absent from
the academic-demo catalog. Browser, onboarding and focus runs reported zero
external requests, uncaught errors and ordinary console errors.

## Real-host access test plan — PENDING

Run with a clean browser profile and no Access cookie against production,
preview and custom-domain aliases:

```text
GET /
GET /index.html
GET /app.js
GET /catalog.json
GET /data/synthetic-block/report.json
GET /data/synthetic-pass/districts_base.geojson
GET /package-manifest.json
HEAD /data/synthetic-block/report.md
```

Every request must reach Access before returning static bytes. Repeat with an
allowed OTP identity (content available), a denied email (no OTP/access), an
expired session and after logout. Confirm `X-Robots-Tag`, CSP, no-store and
framing headers on HTML, JavaScript, JSON, GeoJSON and Markdown responses.
Record redirect chains/status codes rather than a screenshot alone.

## Verdict

**GO for owner review of the prepared candidate. HOLD for publication.** No
hosting, account, DNS, Access policy, deployment, invitation, merge or email was
created by this work.
