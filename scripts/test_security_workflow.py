#!/usr/bin/env python3
"""Offline regression tests for the professional secret-scan workflow."""

from pathlib import Path
import re
import unittest


CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
GITLEAKS_SHA = "e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e"
UPLOAD_PAGES_SHA = "fc324d3547104276b827a68afc52ff2a11cc49c9"
DEPLOY_PAGES_SHA = "368f82528645a54fb793d4d04e342629a3f51346"
ROOT = Path(__file__).resolve().parents[1]
SECURITY_WORKFLOW = ROOT / ".github/workflows/review-security.yml"
PAGES_WORKFLOW = ROOT / ".github/workflows/review-pages.yml"
EXPECTED_PAGES_WORKFLOW = f"""name: Secure site review and Pages
on:
  pull_request:
    branches: [master]
  push:
    branches: [master]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: review-pages-${{{{ github.ref }}}}
  cancel-in-progress: false
jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@{CHECKOUT_SHA} # v7
        with:
          persist-credentials: false
      - name: Security workflow policy
        run: python3 -m unittest scripts.test_security_workflow -v
      - run: node --check site-assets/site.js
      - run: python3 scripts/stage_review.py _review
      - name: Stage all domain previews from the reviewed source commit
        run: bash scripts/stage_domain_previews.sh _review/domain-previews
      - run: python3 scripts/check_review.py _review
      - uses: actions/upload-pages-artifact@{UPLOAD_PAGES_SHA} # v5
        with:
          path: _review
  deploy:
    if: github.event_name == 'push' || github.event_name == 'workflow_dispatch'
    needs: validate
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    steps:
      - id: deploy
        uses: actions/deploy-pages@{DEPLOY_PAGES_SHA} # v5
"""


class SecurityWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = SECURITY_WORKFLOW.read_text()

    def test_trusted_triggers_and_read_only_permissions(self) -> None:
        self.assertIn("pull_request:\n    branches: [master]", self.workflow)
        self.assertIn("push:\n    branches: [master]", self.workflow)
        self.assertIn("workflow_dispatch:", self.workflow)
        self.assertIn("schedule:\n    - cron: '41 1 * * 2'", self.workflow)
        self.assertNotIn("pull_request_target", self.workflow)
        self.assertEqual(self.workflow.count("permissions:\n  contents: read"), 1)
        self.assertNotRegex(self.workflow, r"\bwrite(?:-all)?\b")

    def test_actions_are_exactly_pinned(self) -> None:
        self.assertEqual(
            self.workflow.count(f"actions/checkout@{CHECKOUT_SHA}"), 1
        )
        self.assertEqual(
            self.workflow.count(f"gitleaks/gitleaks-action@{GITLEAKS_SHA}"), 1
        )
        uses = re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)", self.workflow)
        self.assertEqual(len(uses), 2)
        for action in uses:
            with self.subTest(action=action):
                self.assertRegex(action, r"^[^@\s]+@[0-9a-f]{40}$")

    def test_scan_is_bounded_and_cancels_superseded_runs(self) -> None:
        self.assertEqual(self.workflow.count("timeout-minutes: 10"), 1)
        self.assertIn(
            "concurrency:\n"
            "  group: professional-security-${{ github.ref }}\n"
            "  cancel-in-progress: true",
            self.workflow,
        )

    def test_checkout_and_gitleaks_keep_output_boundaries(self) -> None:
        self.assertEqual(self.workflow.count("fetch-depth: 0"), 1)
        self.assertEqual(self.workflow.count("persist-credentials: false"), 1)
        self.assertEqual(
            self.workflow.count("GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"), 1
        )
        self.assertEqual(
            self.workflow.count("GITLEAKS_ENABLE_COMMENTS: 'false'"), 1
        )
        self.assertEqual(
            self.workflow.count("GITLEAKS_ENABLE_UPLOAD_ARTIFACT: 'false'"), 1
        )

    def test_pages_validation_runs_policy_test(self) -> None:
        pages = PAGES_WORKFLOW.read_text()
        self.assertEqual(
            pages.count("python3 -m unittest scripts.test_security_workflow -v"),
            1,
        )
        validate = pages.split("\n  validate:\n", 1)[1].split("\n  deploy:\n", 1)[0]
        self.assertIn(
            "name: Security workflow policy\n"
            "        run: python3 -m unittest scripts.test_security_workflow -v",
            validate,
        )

    def test_complete_pages_workflow_contract_is_exact(self) -> None:
        self.assertEqual(
            PAGES_WORKFLOW.read_bytes(),
            EXPECTED_PAGES_WORKFLOW.encode("utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
