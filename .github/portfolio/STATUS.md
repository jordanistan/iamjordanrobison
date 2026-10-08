# iamjordanrobison.com checkpoint — 2026-10-04

- New responsive static review built, with original source/history preserved.
- Native Pages review uses a publish allowlist; no private docs or old application source are staged.
- Preview has no live lead capture. Production generator and launch guide: `jordanistan/illnetwork/portfolio` and `.github/portfolio/LAUNCH.md`.
- Added pinned build, Gitleaks, CodeQL Actions. Successful scans/deployment still need observed workflow evidence; native security settings are not verified.
- Browser QA is pending (no supported browser-control skill in this build session).
- Next task: inspect actual CI, then perform desktop/mobile/keyboard review; consult the central task board before writing.

## CI repair evidence

GitHub reported CodeQL default setup already enabled; its PR analysis passed. Removed the conflicting advanced CodeQL job while retaining the passing Gitleaks job and native default analysis. Native secret scanning/push protection are still unverified.

Archived unconfigured Snyk and labeler templates plus conflicting advanced CodeQL. Native default CodeQL and Gitleaks remain active; no failed scan is represented as passing.

## Portfolio review mirror

The central Pages deploy succeeded but ill.network returned a Cloudflare 403 from the managed workspace, with a GitHub redirect to HTTP. A review-only mirror is staged at `/domain-previews/review.html` on this working personal site using a specific reviewed central commit. No mutable remote branch is executed, no live commerce is enabled, and internal source/docs are excluded. Update the pinned source commit only after reviewing and testing a new central change. P001 remains the central domain HTTPS/access check.

## P006 recruiter-facing portfolio polish — October 6, 2026

Review branch `codex/p006-portfolio-polish-20261006` turns the landing page into an evidence-led recruiter brief using only the current `Jordan_Robison_2026-Resume.pdf`: role fit, selected verified experience, working approach, inspectable public projects, and a direct résumé download. The existing PDF is now included by the explicit Pages allowlist. Before publication, its two pages were structurally re-exported to remove the embedded Content Credentials attachment and model/timestamp provenance while preserving extracted text, tagged-document status, and pixel-identical rendering in the comparison test. The checker requires a non-empty PDF and landing-page link, rejects attachment/active-content/external-action markers, and excludes the legacy live-contact résumé page from the review artifact.

Local checks passed: JavaScript syntax; Python compilation; 39-page combined Pages artifact with 0 errors; sanitized PDF source/artifact SHA-256 parity; PDF text parity, 0 embedded files, no form or JavaScript, and pixel-identical two-page renders; current central production export for `iamjordanrobison.com` with 2 pages and 0 errors; `git diff --check`. Browser QA was attempted but skipped because the installed Playwright package had no browser executable. No form, email capture, scheduling, tracker, external script, checkout, customer claim, or private data was added.

This change affects the native GitHub Pages design review only. The separate central production source is unchanged because P009 currently owns the shared portfolio generator/assets. After that lease is released, a separate reviewed task may sync the recruiter content into the commercial production export. Do not claim the new review is deployed until PR checks and the post-merge Pages run succeed.


## Owner-requested design restoration — October 8, 2026

Restored `index.html`, robots and sitemap from `0b837e291252e666aac048ef0aa266b2a11b1286`, the state before PR #62 and PR #64 replaced the original design. The publication allowlist now includes the existing résumé and threat-detection pages, original CSS, imagery, fonts and navigation scripts. The sanitized résumé PDF and security workflows remain. Historical compatibility exceptions in the artifact checker are restricted to exact file hashes. The domain review mirror remains separate. Future work must preserve this design unless Jordan explicitly requests a redesign. Local artifact checks and deployment evidence are recorded in the restoration delivery.
