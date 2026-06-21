#!/usr/bin/env python3
"""Tests for stronger pre-audit judgment without pretending autonomy."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OraclePreAuditTest(unittest.TestCase):
    def test_validate_report_accepts_real_screenshot_files_without_screenshot_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "report"
            screenshots = report_dir / "site-screenshots"
            screenshots.mkdir(parents=True)
            (screenshots / "desktop.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            (screenshots / "mobile.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            (report_dir / "index.html").write_text("<!doctype html><title>Report</title>", encoding="utf-8")
            (report_dir / "LATEST-SEO-GEO-REPORT.md").write_text("# Report\n", encoding="utf-8")
            (report_dir / "audit.json").write_text(
                json.dumps(
                    {
                        "site": "example.com",
                        "audited_url": "https://example.com/",
                        "generated_at": "2026-06-21T10:00:00+02:00",
                        "report_language": "en",
                        "summary": {"headline": "Fixture", "status": "partial"},
                        "findings": [],
                        "sources": [{"label": "Homepage", "url": "https://example.com/"}],
                        "responsive_study": {
                            "summary": {"status": "pass", "verdict": "Screenshots were captured."}
                        },
                        "ai_layer_current_state": {
                            "llms_txt": True,
                            "for_ai": True,
                            "for_ai_json": True,
                            "for_ai_txt": True,
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_audit_report.py"),
                    "--report-dir",
                    str(report_dir),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_draft_audit_marks_fragment_url_and_preprod_gates(self) -> None:
        run_full_audit = load_script("run_full_audit")
        with tempfile.TemporaryDirectory() as tmp:
            audit = run_full_audit.draft_audit(
                "https://swing.appmiweb.com/#page-1",
                Path(tmp),
                "fr",
                "preprod",
                True,
                {"llms_txt": True, "for_ai": True, "for_ai_json": True, "for_ai_txt": True},
                [],
                {},
            )

        self.assertEqual(audit["summary"]["status"], "production_gated")
        self.assertEqual(audit["url_scope"]["canonical_without_fragment"], "https://swing.appmiweb.com/")
        self.assertTrue(audit["url_scope"]["has_fragment"])
        self.assertTrue(any(finding["title"] == "Fragment URL should not become the canonical SEO URL" for finding in audit["findings"]))
        gate_areas = {gate["area"] for gate in audit["production_gates"]}
        self.assertIn("Final domain", gate_areas)
        self.assertIn("Measurement", gate_areas)
        self.assertEqual(audit["preproduction_assessment"]["status"], "production_gated")

    def test_ai_layer_package_includes_diff_when_ai_layer_already_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            audit_path = tmp_path / "audit.json"
            output_dir = tmp_path / "report"
            audit_path.write_text(
                json.dumps(
                    {
                        "site": "example.com",
                        "audited_url": "https://example.com/",
                        "report_language": "en",
                        "generated_at": "2026-06-21T10:00:00+02:00",
                        "summary": {"headline": "Existing AI layer needs review.", "status": "ok"},
                        "findings": [],
                        "sources": [{"label": "Homepage", "url": "https://example.com/"}],
                        "ai_layer_current_state": {
                            "llms_txt": True,
                            "for_ai": True,
                            "for_ai_json": True,
                            "for_ai_txt": True,
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_ai_layer_package.py"),
                    "--input",
                    str(audit_path),
                    "--output-dir",
                    str(output_dir),
                    "--update-audit",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_dir / "ai-layer-package" / "AI_LAYER_DIFF.md").is_file())
            updated = json.loads(audit_path.read_text(encoding="utf-8"))
            package = updated["ai_layer_package"]
            self.assertEqual(package["publication_status"], "already_present")
            self.assertEqual(package["comparison_status"], "compare_existing_before_change")
            self.assertTrue(any(item["path"] == "ai-layer-package/AI_LAYER_DIFF.md" for item in package["files"]))


if __name__ == "__main__":
    unittest.main()
