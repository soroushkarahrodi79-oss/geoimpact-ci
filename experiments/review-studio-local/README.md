# GeoImpact Review Studio — local prototype 0.1

A standalone, static, read-only review of **existing GeoImpact CI v1.2.0 / V5
artifacts**. Compare original BASE/CANDIDATE, select fixed relationships, inspect
before/after, follow evidence IDs and verify bytes. No application backend,
browser GIS analysis, policy execution, uploads, CDN, analytics or basemap.

**GO for this bounded local prototype. R1 OPEN / Madrid + Sierra full viewer
HOLD.** Madrid source geometry, derived footprints and portal data are excluded
from the bundle. The released synthetic rectangles use historical district
names as IDs; they are mathematical fixtures, **not INE geometry**. See the
[original construction](../../docs/GATE_1_REPORT.md).

Documentary/design [Draft PR #22](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/pull/22)
is separate from the functional PR on `experiment/review-studio-local-v0-1`.
The [requirements reconciliation](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/blob/experiment/review-studio-feasibility/experiments/review-studio/RECONCILIATION.md)
retains the complete #21 specification, transition filter, JSON traceability,
five viewports and F1 evidence. #21 remains open. No merge or deployment.

## Reproduce on Windows PowerShell

From the repository root, use Python 3.11+ and Node.js 22+ for development tests.
The app itself needs only a static HTTP server and a modern browser with Web
Crypto. These commands export the release into an ignored directory; they do
not switch or modify the scientific checkout. Avoid PowerShell redirection
when writing binary archives or canonical reports.

```powershell
git fetch origin tag v1.2.0
New-Item -ItemType Directory -Force work/release-engine | Out-Null
git archive --format=tar --output=work/studio-release.tar v1.2.0
tar -xf work/studio-release.tar -C work/release-engine
python -m venv work/studio-venv
work/studio-venv/Scripts/python.exe -m pip install -e "work/release-engine[test]"
work/studio-venv/Scripts/python.exe experiments/review-studio-local/prepare.py --engine work/release-engine
python experiments/review-studio-local/serve.py
```

Open **http://127.0.0.1:8765**. Keep the server terminal running; Ctrl+C stops
it. `--port 8766` chooses another loopback port. A local HTTP server is required:
`file://` is not a supported launch mode. Do not serve the repository root.

On Linux/macOS, the equivalent interpreter is
`work/studio-venv/bin/python`. The remaining scripts and options are the same.
`tar` is a normal Git/Windows or system prerequisite, not an app dependency.

Default preparation includes:

- **Synthetic BLOCK:** 2 regressions, threshold 1, 3 relationship records.
- **Synthetic PASS:** same original geometry and 2 regressions, threshold 2.
  PASS must not be interpreted as zero changes or proof of correctness.
- **Analysis ERROR:** an actual missing-config CLI execution, exit 2, no report
  and no verdict. Its stored stderr redacts the local config path explicitly.

### Optional Sierra: local generation only

The [file-specific rights review](rights/sierra-local.json) supports the
proposed local use with attribution: dated 2015 CC BY 4.0, and the maintained
boundary/equipment WFS positive free-use condition naming authors/owners. It
does not assign the 2015 CC license to 2025/2026 responses or authorize a new
public bundle. Original fixture hashes must match the release manifest.

```powershell
work/studio-venv/Scripts/python.exe experiments/review-studio-local/prepare.py --engine work/release-engine --sierra-local
```

Restart/reload the local page. This includes exact retained Sierra inputs and
fresh byte-matching outputs in ignored `web/data/` only. Its screenshots in
`qa/local/` also stay local. No source geometry is fetched during preparation;
the fixture is read from the exported tag. Rights-source metadata were checked
separately, with URLs/date/response identities retained in the rights review.

Sierra shows PASS/0/0, all 52 unchanged relationships, 40 assigned to `69` at
both states and 12 unassigned at both. Empty regression GeoJSON is valid; it
never removes the original point inventory. The park geometry is modified.
Equipment is fixed at 2026-10-05, not a pair of historical inventories; Gate 8
retains its original research MODIFY conclusion. Attribution remains visible.

## Interactions and integrity

Select a list row (Enter/Space) or point; BASE and CANDIDATE highlight the
recorded primary IDs. The evidence panel displays original arrays, predicate,
change type and existing regression evidence ID, with its JSON pointer. No ID
is invented for an unchanged row. Search, status and before→after filters only
select displayed rows; they do not change totals, classifications or policy.

Shared zoom/pan/fit controls retain the same camera on both maps. Arrow keys
pan only while a map has focus; +/− zoom; Tab leaves it; Escape clears selection
and returns focus to its row. Mouse dragging the map background pans; pan
buttons provide the pointer/touch alternative. On narrow screens the snapshot
buttons swap one map without moving the fixed points. A selection link jumps
to evidence. Sources/versions/config/downloads are under Provenance.

The viewer verifies catalog → manifest → raw files, then checks V5 input
identities, supported schema, complete composite joins and report/export
evidence agreement. Malformed/missing/mixed/tampered data hide the entire
scientific view and display a **load/integrity ERROR**, independently of an
analysis ERROR and completed PASS/BLOCK. It never re-evaluates a threshold.

The retained trust module is a byte-identity anchor, not a signature: someone
who replaces both app code and manifests can replace it. Source rights and
dates are curated metadata, not V5 output or proof of publisher authenticity.

## Automated verification

Keep the local static server running in another terminal. From this directory:

```powershell
npm ci
npx playwright install chromium
npm test
npm run test:browser
```

`STUDIO_URL` can select another loopback URL. To use an already installed
Chromium, set `STUDIO_CHROMIUM_EXECUTABLE` to its executable before running the
tests. No machine-specific browser path is required by the project. Playwright
is a pinned **development-only** dependency; runtime has no npm dependencies.

Browser tests run an actual Chromium process at 1440×900, 1440×1000, 834×1112,
375×812, 390×844 and 320×812. They also exercise 200% **CSS zoom emulation**.
These are viewport/layout checks, not physical tablet/phone or screen-reader
tests. Real captures of synthetic cases are in [qa/screenshots](qa/screenshots/).
Sierra captures/results are generated locally under ignored `qa/local/`.

To repeat scientific qualification from the exported release, put the venv's
Scripts/bin directory on PATH for the installed `geoimpact` command, then run
from `work/release-engine`:

```text
python -m pytest -q
python scripts/verify_ci_contract.py pass
python scripts/verify_ci_contract.py block
python scripts/verify_ci_contract.py error
python scripts/verify_ci_contract.py hashes
python scripts/verify_madrid_benchmark.py
python scripts/verify_gate8_case.py
```

Madrid's analysis verifier is permitted as scientific regression verification;
its outputs stay under ignored release `ci-output/`, never in the static root.
To verify the current checkout too, run its existing `python -m pytest -q` at
repository root. [VALIDATION](VALIDATION.md) records executed checks and limits.

## Architecture and deliberate limits

`prepare.py` calls the frozen CLI outside the browser and copies allowlisted
exact bytes. `web/reader.js` validates identities/joins. `web/app.js` renders
and filters records. `serve.py` serves only `web/` on 127.0.0.1, with no directory
listing, remote Host access or mutation API. Generated data/catalog/trust and
local logs are ignored. No application code imports `src/geoimpact`.

The native SVG renderer uses an affine CRS84 longitude/latitude display with
inverted y. It supports original Polygon/MultiPolygon rings and holes, with
no simplification, topology, metric accuracy or area-preservation claim.
Extents are computed only to frame the view. There is no geographic basemap,
metric scale bar or reprojection of the EPSG:25830 report footprint. Scientific
scalars are shown exactly as recorded, not measured from the displayed shapes.
The renderer is qualified only for the retained small cases, not arbitrary GIS
files. This is the scoped alternative to the proposed OpenLayers dependency.

No external user/adoption study, screen-reader assessment, full security audit,
WCAG certification, physical-device qualification or production SLA is claimed.
The local prototype does not validate data quality, real effects, administrative
intent or historical equipment operation. None of those are inferred by Studio.

The only blocker to adding Madrid/the full two-real-case viewer is **R1 OPEN**.
Publication/deployment remains outside the authorized scope. No INE query sent.
