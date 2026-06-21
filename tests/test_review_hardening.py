#!/usr/bin/env python3
"""Regression tests for code-review hardening items."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class ReviewHardeningTest(unittest.TestCase):
    def write_minimal_report(self, report_dir: Path, visual_path: str | None = None) -> None:
        report_dir.mkdir(parents=True, exist_ok=True)
        (report_dir / "index.html").write_text("<!doctype html><title>Report</title>", encoding="utf-8")
        (report_dir / "LATEST-SEO-GEO-REPORT.md").write_text("# Report\n", encoding="utf-8")
        audit = {
            "site": "example.test",
            "audited_url": "https://example.test/",
            "generated_at": "2026-06-21T10:00:00+02:00",
            "report_language": "en",
            "summary": {"headline": "Fixture report.", "status": "partial"},
            "findings": [],
            "sources": [{"label": "Fixture", "url": "https://example.test/"}],
            "responsive_study": {
                "summary": {
                    "status": "unavailable",
                    "verdict": "Browser evidence was not captured for this fixture.",
                }
            },
            "ai_layer_current_state": {
                "llms_txt": True,
                "for_ai": True,
                "for_ai_json": True,
                "for_ai_txt": True,
            },
        }
        if visual_path:
            audit["visual_evidence"] = [{"label": "External path", "source_path": visual_path}]
        else:
            audit["screenshot_status"] = "unavailable: fixture"
        (report_dir / "audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    def test_validate_audit_report_rejects_visual_evidence_outside_report_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            outside = tmp_path / "outside.png"
            outside.write_bytes(b"not really a png")
            report_dir = tmp_path / "report"
            self.write_minimal_report(report_dir, visual_path=str(outside))

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

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("site screenshots are missing", result.stderr)

    def test_serve_report_rejects_invalid_bind_host_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "report"
            self.write_minimal_report(report_dir)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "serve_report.py"),
                    "--dir",
                    str(report_dir),
                    "--host",
                    "256.256.256.256",
                    "--port",
                    "8766",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("Could not bind report server", result.stderr)

    def test_serve_report_warns_on_non_loopback_host(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "report"
            self.write_minimal_report(report_dir)
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "serve_report.py"),
                    "--dir",
                    str(report_dir),
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "0",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                time.sleep(1)
            finally:
                process.terminate()
                stdout, stderr = process.communicate(timeout=5)

            self.assertIn("Serving report:", stdout)
            self.assertIn("WARNING: serving on non-loopback host", stderr)

    def test_check_ard_readiness_marks_homepage_fetch_failure_as_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "ard-readiness.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "check_ard_readiness.py"),
                    "--url",
                    "http://127.0.0.1:9/",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )

            self.assertNotEqual(result.returncode, 0)
            readiness = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(readiness["status"], "error")
            self.assertIn("homepage", readiness["recommended"][0].lower())

    def test_compare_audit_reports_keeps_untitled_findings_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            before = tmp_path / "before.json"
            after = tmp_path / "after.json"
            output_dir = tmp_path / "comparison"
            before.write_text(
                json.dumps(
                    {
                        "site": "example.test",
                        "scorecards": [{"label": "SEO", "score": 7.25}],
                        "findings": [{"priority": "P1", "evidence": "A"}, {"priority": "P2", "evidence": "B"}],
                    }
                ),
                encoding="utf-8",
            )
            after.write_text(
                json.dumps(
                    {
                        "site": "example.test",
                        "scorecards": [{"label": "SEO", "score": 7.5}],
                        "findings": [{"priority": "P2", "evidence": "B"}],
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
            data = json.loads((output_dir / "audit-comparison.json").read_text(encoding="utf-8"))
            markdown = (output_dir / "audit-comparison.md").read_text(encoding="utf-8")
            self.assertEqual(data["resolved_findings"], ["P1: A"])
            self.assertIn("SEO: +0.25", markdown)

    def test_install_accepts_plain_relative_custom_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), "tmp-install/seo-geo-growth-agent"],
                cwd=tmp,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((Path(tmp) / "tmp-install" / "seo-geo-growth-agent" / "SKILL.md").is_file())

    def test_skill_doctor_reports_missing_node_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install_dir = Path(tmp) / "seo-geo-growth-agent"
            install = subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), str(install_dir)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(install.returncode, 0, install.stderr)

            env = {**os.environ, "PATH": tmp}
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "skill_doctor.py"), str(install_dir)],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("required command not found: node", result.stderr)

    def test_sync_and_doctor_reports_missing_bash_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = {**os.environ, "PATH": tmp}
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "sync_and_doctor.py"),
                    "--target",
                    "codex",
                ],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("required command not found: bash", result.stderr)


if __name__ == "__main__":
    unittest.main()
