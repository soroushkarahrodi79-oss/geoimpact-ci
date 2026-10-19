# GeoImpact Review Studio — Private Academic Demo V1

Prepared from Draft PR #23 at
`4133c2262fb16546a0dd41f09dd5a6a92b64c100`. This is a deployment candidate,
not a deployment authorization. It does not change GeoImpact CI 1.2.0, Report
V5, the CLI, scientific fixtures, reference hashes, R1, or the local moderated
study in PR #24.

## Delivery decision

**GO to request the owner's publication approval; HOLD for any real upload,
resource creation, DNS change, invitation or email.** The static package and
local verification are ready. Authentication and direct-file denial remain
**PENDING** until an owner-approved hosting instance exists.

## Runtime architecture

The browser loads only static HTML, CSS, JavaScript, JSON, YAML, Markdown and
GeoJSON. It makes same-origin requests for the catalog and allowlisted evidence.
There is no analysis backend, Python runtime, Pages Function, map tile service,
analytics SDK, telemetry SDK, remote font, CDN asset, or browser-side policy
calculation. Python is used only before publication to run the frozen CLI and
assemble/verify the package.

The deployable directory is
`experiments/review-studio-local/academic-demo-dist/`. Its
`package-manifest.json` records SHA-256 and byte size for every payload. The
tracked `package-allowlist.json` is the complete positive file list; packaging
fails on any missing, extra or unsafe source, and verification fails on any
unexpected deployed file.

## Data isolation and rights assurance

Only these cases are admitted by the catalog, JavaScript reader, packager and
package verifier:

- `synthetic-block`: completed V5 analysis, BLOCK, two regressions, threshold 1.
- `synthetic-pass`: the same synthetic source geometry and two regressions,
  PASS under threshold 2.
- `synthetic-error`: controlled missing-configuration exit 2, with no report,
  geometry or invented verdict.

The package contains neither `research/` nor any file from it. The verifier
also rejects known real-data paths/identifiers, symlinks, hidden additions,
secret patterns, remote request targets and analytics markers. The source
repository continues to contain research materials outside the package; this
work neither deletes nor relicenses them.

Rights were assessed from the repository's actual licensing records, not from
GitHub visibility:

| Included material | Basis | Decision |
|---|---|---|
| Review Studio HTML/CSS/JS | Repository `LICENSE`, MIT, copyright 2026 Soroush Karahrodi | Include with `LICENSE.txt` |
| `tests/fixtures` synthetic geometries, configs and points | Repository MIT scope plus Gate 1's recorded mathematical synthetic construction | Include; label synthetic and non-official |
| V5 outputs generated from those fixtures | Mechanical output of the frozen MIT code over synthetic fixtures; exact hashes retained | Include with provenance and scientific limits |
| Fonts, icons and map presentation | System fonts, text glyphs and native SVG only | Include; no external asset licence needed |
| Third-party/research geometry | Repository `NOTICE.md` explicitly says `research/` is not relicensed by MIT | Exclude completely |

This is an engineering redistribution assessment, not a legal opinion. No
rights claim is made for excluded research data.

## Experience retained

The implementation retains ES/EN welcome, the eight-step tour, the real
`hotel_813` practice, Help and eleven-term glossary, synchronized BASE and
CANDIDATE maps, filters, selection, original evidence downloads, provenance,
scientific limitations, and PASS/BLOCK/ERROR states. The only product-facing
change is a quiet bilingual label that identifies a private academic demo using
synthetic data. Scientific values and outcomes are untouched.

Source citations remain visible as plain text. They are deliberately not
clickable, so the viewer does not initiate third-party navigation or requests.
The Content Security Policy permits only same-origin scripts, styles, data and
connections.

## Hosting comparison (checked 2026-10-19)

| Option | Guest access and all-path protection | Cost / account | Main risk | Fit |
|---|---|---|---|---|
| **Cloudflare Pages + Access OTP** | Exact email list; OTP to invited email. Access must cover the production `*.pages.dev` hostname, preview wildcard and any custom domain, so assets and direct data URLs are gated. | Pages static requests are free/unlimited; Free Pages allows 20,000 files, 25 MiB per file and 500 builds/month. Zero Trust Free is $0 for up to 50 users; pay-as-you-go is listed at $7/user/month above that. Requires Cloudflare account; custom domain strongly recommended. | A public custom domain or unprotected `pages.dev` alias would bypass the intended gate. Free Access retains limited authentication logs (up to 24 hours). | **Recommended** for a small invited cohort. |
| Azure Static Web Apps Free | `/*` can require a custom invited role, covering static files as well as the entry page. Built-in invitations support up to 25 users. | Free tier: $0, 250 MB per app/deployment, 100 GB included bandwidth per subscription; Azure subscription and GitHub/Entra identity required. | Using the built-in `authenticated` role would admit any signed-in user; every professor must instead receive the custom role. Invitation workflow is heavier and identity-provider dependent. | Good alternative for an Azure/Entra institution. |
| Vercel Deployment Protection | Vercel Authentication protects previews, but external guests generally need Vercel identities/team access or share links. Protecting all production URLs needs Pro/Enterprise plus the relevant protection capability. | Advanced Deployment Protection for Pro is documented at $150/month; Enterprise pricing is custom. | Hobby standard protection leaves the production domain public. Password sharing is not an email allowlist. | Not recommended for this cohort/cost profile. |
| Private GitHub Pages | Private Pages is available only to GitHub Enterprise Cloud organizations and readers need repository access. | Enterprise Cloud contract plus GitHub accounts. | Couples demo access to source-repository access and does not suit invited academics without enterprise membership. Public Pages is explicitly out of scope. | Reject for V1. |

Primary references:

- Cloudflare [Pages limits](https://developers.cloudflare.com/pages/platform/limits/),
  [static pricing](https://developers.cloudflare.com/pages/functions/pricing/),
  [Zero Trust pricing](https://www.cloudflare.com/plans/),
  [OTP allowlisting](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/),
  [Pages/Access hostname caveat](https://developers.cloudflare.com/pages/platform/known-issues/),
  [custom headers](https://developers.cloudflare.com/pages/configuration/headers/).
- Azure [route authorization](https://learn.microsoft.com/azure/static-web-apps/configuration),
  [authentication](https://learn.microsoft.com/azure/static-web-apps/authentication-authorization),
  [quotas](https://learn.microsoft.com/azure/static-web-apps/quotas).
- Vercel [Deployment Protection](https://vercel.com/docs/deployment-protection).
- GitHub [private Pages visibility](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site).

Prices and plan features must be rechecked immediately before approval and
purchase. No account or paid resource has been created.

## Recommended authentication plan

Use Cloudflare Pages static hosting plus Cloudflare Access with One-time PIN:

1. The owner provides the exact professor/researcher email allowlist. Do not
   use an open email-domain rule unless the owner explicitly approves it.
2. Create one Access application for the exact production hostname and another
   for preview hostnames. If a custom domain is added, create and test its own
   Access application. Protect the root and every subpath.
3. Require the OTP login method and the exact email selector. Keep session
   duration short for the study window and revoke users after it.
4. Do not add client secrets, service tokens, analytics, Zaraz, Pages Functions
   or authentication code to the package. Access owns authentication before
   static delivery.
5. Keep the supplied `X-Robots-Tag`, `robots.txt`, CSP, no-store and framing
   headers. Disable Cloudflare Web Analytics for the project.
6. Accept only the minimum authentication/security logs intrinsic to Access;
   document the retention and controller before inviting users.

## Deployment procedure — not executed

These steps require a new explicit owner authorization:

1. Rebuild and verify locally using the commands in
   `ACADEMIC_DEMO_VERIFICATION.md`; compare the package manifest in the PR.
2. Create a Cloudflare Pages **Direct Upload** project with no Functions and no
   repository build integration. Upload only `academic-demo-dist/`.
3. Before sharing any URL, enable Access on the production `pages.dev` hostname
   and preview wildcard. Add a protected custom domain if approved; either
   protect or redirect every alternate hostname.
4. Apply the exact email/OTP policy, disable analytics, and test while signed
   out. Direct requests to `/app.js`, `/catalog.json`,
   `/data/synthetic-block/report.json` and `/package-manifest.json` must never
   return content without authentication.
5. Test an allowed and a denied email, expired session, logout, deep links,
   mobile, cache clearing and the complete application flow. Record actual
   response status/redirect chains and a browser network trace.
6. Only after those checks pass may invitations be sent. This preparation does
   not authorize sending them.

No production secret is required by the client. Any deployment API token stays
outside the repository and browser bundle.

## Rollback and emergency closure

For immediate containment, change the Access policy to deny all and verify all
hostnames while signed out. Then use Pages deployment history to roll production
back to the prior successful deployment, or delete the unneeded demo project.
Cloudflare documents instant rollback to any prior successful production
deployment in [Pages rollbacks](https://developers.cloudflare.com/pages/configuration/rollbacks/).
Finally revoke guest policy entries and any short-lived deployment credential.

## Publication blockers

- **PENDING:** owner approval for provider, account, domain, cost and privacy/log
  handling.
- **PENDING:** exact guest email allowlist and invitation period.
- **PENDING:** real-host validation that every alias and direct asset path is
  denied before authentication.
- **PENDING:** owner acceptance of Cloudflare as authentication/data processor,
  including OTP email delivery and limited Access logs.
- **PENDING:** optional physical-device and screen-reader qualification if the
  owner requires claims beyond the existing engineering checks.

Until all required pending items are resolved, the verdict remains **HOLD for
publication**.
