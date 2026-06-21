#!/usr/bin/env python3
"""Tests for owner-data mode and the simple audit CLI."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliOwnerAndEvidenceTest(unittest.TestCase):
    def test_generate_owner_data_request_writes_markdown_json_and_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "owner-data"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_owner_data_request.py"),
                    "--site",
                    "example.com",
                    "--output-dir",
                    str(output_dir),
                    "--language",
                    "en",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            markdown = (output_dir / "owner-data-request.md").read_text(encoding="utf-8")
            checklist = json.loads((output_dir / "owner-data-checklist.json").read_text(encoding="utf-8"))
            with (output_dir / "owner-data-intake.csv").open(encoding="utf-8") as handle:
                intake_rows = list(csv.DictReader(handle))
            self.assertIn("example.com", markdown)
            self.assertIn("Google Search Console", markdown)
            self.assertIn("GA4", markdown)
            self.assertIn("Bing Webmaster Tools", markdown)
            self.assertIn("Cloudflare Analytics", markdown)
            self.assertIn("server logs", markdown)
            self.assertTrue(any(item["source"] == "gsc" for item in checklist["requested_sources"]))
            self.assertTrue(any(item["source"] == "cloudflare" for item in checklist["requested_sources"]))
            self.assertEqual(checklist["paid_tools"]["default_policy"], "ask_before_use")
            self.assertTrue(any(row["source_key"] == "gsc" for row in intake_rows))
            self.assertTrue(any(row["source_key"] == "cloudflare" for row in intake_rows))

    def test_seo_geo_audit_plan_only_creates_workspace_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "audit-workspace"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "seo_geo_audit.py"),
                    "https://example.com/",
                    "--output-dir",
                    str(output_dir),
                    "--lang",
                    "fr",
                    "--plan-only",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads((output_dir / "audit-plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["target_url"], "https://example.com/")
            self.assertEqual(plan["language"], "fr")
            self.assertEqual(plan["mode"], "plan_only")
            self.assertIn("capture_site_screenshots.mjs", " ".join(plan["next_commands"]))
            self.assertIn("generate_html_audit_report.py", " ".join(plan["next_commands"]))
            self.assertIn("generate_owner_data_request.py", " ".join(plan["next_commands"]))
            self.assertIn("check_ard_readiness.py", " ".join(plan["next_commands"]))
            self.assertIn("validate_audit_report.py", " ".join(plan["next_commands"]))
            self.assertTrue(any("owner-data-intake.csv" in item for item in plan["expected_outputs"]))

    def test_generate_ard_catalog_writes_ai_catalog_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "ai-catalog.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_ard_catalog.py"),
                    "--publisher-domain",
                    "example.com",
                    "--display-name",
                    "SEO GEO Growth Agent",
                    "--resource-name",
                    "seo-geo-growth-agent",
                    "--resource-url",
                    "https://github.com/bacoco/seo-geo-growth-agent",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            catalog = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(catalog["specVersion"], "1.0")
            self.assertEqual(catalog["host"]["displayName"], "SEO GEO Growth Agent")
            self.assertEqual(len(catalog["entries"]), 1)
            entry = catalog["entries"][0]
            self.assertEqual(entry["identifier"], "urn:air:example.com:skill:seo-geo-growth-agent")
            self.assertEqual(entry["type"], "application/ai-skill+md")
            self.assertEqual(entry["url"], "https://github.com/bacoco/seo-geo-growth-agent")
            self.assertNotIn("data", entry)
            self.assertGreaterEqual(len(entry["representativeQueries"]), 2)
            self.assertLessEqual(len(entry["representativeQueries"]), 5)


if __name__ == "__main__":
    unittest.main()
