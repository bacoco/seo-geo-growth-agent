#!/usr/bin/env python3
"""Tests for report receipts, comparison, and GEO citation panel tooling."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReportReceiptCompareAndPanelsTest(unittest.TestCase):
    def test_html_report_writes_latest_receipt_and_preprod_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            audit_path = tmp_path / "audit.json"
            output_dir = tmp_path / "report"
            audit_path.write_text(
                json.dumps(
                    {
                        "site": "example.com",
                        "audited_url": "https://preprod.example.com/",
                        "generated_at": "2026-06-21T09:00:00+02:00",
                        "environment": "preprod",
                        "summary": {
                            "headline": "Preproduction is ready for content QA, not production measurement.",
                            "status": "partial",
                            "data_confidence": "medium",
                        },
                        "production_gates": [
                            {
                                "area": "Measurement",
                                "next_now": "Keep public crawl checks green.",
                                "defer_until_prod": "Connect GA4/GSC after final domain launch.",
                                "proof_needed": "Owner access to GA4, GSC, and Bing Webmaster Tools.",
                            }
                        ],
                        "findings": [],
                        "sources": [{"label": "Preprod", "url": "https://preprod.example.com/"}],
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_html_audit_report.py"),
                    "--input",
                    str(audit_path),
                    "--output-dir",
                    str(output_dir),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = output_dir / "LATEST-SEO-GEO-REPORT.md"
            self.assertTrue(receipt.is_file())
            receipt_text = receipt.read_text(encoding="utf-8")
            self.assertIn("example.com", receipt_text)
            self.assertIn("index.html", receipt_text)
            self.assertIn("v1.3.0", receipt_text)
            self.assertIn("preprod", receipt_text)

            html = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn("Environment", html)
            self.assertIn("Preproduction", html)
            self.assertIn("Defer until production", html)
            self.assertIn("Connect GA4/GSC after final domain launch.", html)

    def test_compare_audit_reports_writes_narrative_markdown_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            before = tmp_path / "before.json"
            after = tmp_path / "after.json"
            output_dir = tmp_path / "comparison"
            before.write_text(
                json.dumps(
                    {
                        "site": "example.com",
                        "generated_at": "2026-06-20T09:00:00+02:00",
                        "summary": {"headline": "Older report", "status": "partial"},
                        "scorecards": [{"label": "SEO", "score": 6, "max": 10}],
                        "findings": [{"priority": "P1", "title": "Missing llms.txt"}],
                    }
                ),
                encoding="utf-8",
            )
            after.write_text(
                json.dumps(
                    {
                        "site": "example.com",
                        "generated_at": "2026-06-21T09:00:00+02:00",
                        "summary": {"headline": "Newer report", "status": "ok"},
                        "scorecards": [{"label": "SEO", "score": 8, "max": 10}],
                        "findings": [],
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "compare_audit_reports.py"),
                    "--before",
                    str(before),
                    "--after",
                    str(after),
                    "--output-dir",
                    str(output_dir),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            markdown = (output_dir / "audit-comparison.md").read_text(encoding="utf-8")
            data = json.loads((output_dir / "audit-comparison.json").read_text(encoding="utf-8"))
            self.assertIn("SEO: +2.0", markdown)
            self.assertIn("Narrative conclusion", markdown)
            self.assertEqual(data["score_deltas"][0]["delta"], 2.0)
            self.assertEqual(data["finding_delta"], -1)

    def test_generate_geo_citation_panel_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "geo-citation-panel.csv"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_geo_citation_panel.py"),
                    "--site",
                    "example.com",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            with output_path.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            families = {row["prompt_family"] for row in rows}
            self.assertIn("brand_discovery", families)
            self.assertIn("booking_boundary", families)
            self.assertIn("source_integrity", families)
            self.assertTrue(all(row["result_status"] == "ready_not_executed" for row in rows))
            self.assertTrue(all("example.com" in row["target_domain"] for row in rows))


if __name__ == "__main__":
    unittest.main()
