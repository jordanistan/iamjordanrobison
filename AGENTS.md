# iamjordanrobison.com site agents

Read `.github/portfolio/STATUS.md` first. Company-wide operating instructions, task claims, roles, decisions and expert prompt live in `jordanistan/illnetwork` under `AGENTS.md` and `.github/portfolio/`. Fetch that state and inspect current PRs before editing. Preserve repository history and existing source assets. No private client data or secrets in GitHub.

The current root is a static **design review** with no inquiry capture or checkout. `site-assets/` is its frontend code; `scripts/stage_review.py` publishes an explicit allowlist, and `scripts/check_review.py` checks the artifact. Production source lives in `illnetwork/portfolio`, buildable for `iamjordanrobison.com`. Do not add live commerce to GitHub Pages. Do not invent transactions, health claims, inventory, accreditation, testimonials, or insurance.

Validate with `node --check site-assets/site.js`, run `python3 scripts/stage_review.py <output>`, add the pinned domain mirror with `bash scripts/stage_domain_previews.sh <output>/domain-previews`, then run `python3 scripts/check_review.py <output>`. Use a fresh output directory. Keep pinned Actions and least privilege. Record actual CI/deploy evidence. Checkpoint branch, commit, tests, remaining work, and blockers before context exhaustion.
