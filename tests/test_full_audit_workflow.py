#!/usr/bin/env python3
"""Tests for the one-command audit workflow and report validation gate."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
import zipfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class FullAuditWorkflowTest(unittest.TestCase):
    def run_fixture_server(self, site_dir: Path) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            lambda *args, **kwargs: QuietHandler(*args, directory=site_dir, **kwargs),
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread, f"http://127.0.0.1:{server.server_port}/"

    def test_run_full_audit_generates_report_package_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            site_dir = tmp_path / "site"
            site_dir.mkdir()
            (site_dir / "index.html").write_text(
                """<!doctype html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reference fixture</title>
  <meta name="description" content="A fixture page used to test the SEO GEO audit workflow.">
</head>
<body>
  <main>
    <h1>Reference fixture</h1>
    <p>This page intentionally omits /llms.txt and /for-ai files so the audit workflow can generate owner-review improvement files.</p>
    <a href="/contact">Contact</a>
  </main>
</body>
</html>""",
                encoding="utf-8",
            )
            server, thread, base_url = self.run_fixture_server(site_dir)
            output_dir = tmp_path / "report"
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts" / "run_full_audit.py"),
                        base_url,
                        "--output-dir",
                        str(output_dir),
                        "--lang",
                        "en",
                        "--skip-browser",
                        "--no-serve",
                        "--allow-local",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=25,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)

            self.assertEqual(result.returncode, 0, result.stderr)
            for relative in (
                "audit.json",
                "index.html",
                "LATEST-SEO-GEO-REPORT.md",
                "owner-data/owner-data-request.md",
                "owner-data/owner-data-checklist.json",
                "owner-data/owner-data-intake.csv",
                "ard-readiness.json",
                "ai-layer-package.zip",
                "report-validation.json",
            ):
                self.assertTrue((output_dir / relative).exists(), relative)

            audit = json.loads((output_dir / "audit.json").read_text(encoding="utf-8"))
            self.assertEqual(audit["report_language"], "en")
            self.assertEqual(audit["summary"]["status"], "partial")
            self.assertEqual(audit["screenshot_status"], "unavailable: browser capture skipped by --skip-browser")
            self.assertEqual(audit["ai_layer_current_state"]["llms_txt"], False)
            self.assertEqual(audit["ai_layer_package"]["status"], "generated")
            self.assertTrue(any(finding["title"] == "Missing AI-readable publication layer" for finding in audit["findings"]))

            validation = json.loads((output_dir / "report-validation.json").read_text(encoding="utf-8"))
            self.assertEqual(validation["status"], "pass")
            with zipfile.ZipFile(output_dir / "ai-layer-package.zip") as archive:
                names = set(archive.namelist())
            self.assertIn("ai-layer-package/llms.txt", names)
            self.assertIn("ai-layer-package/for-ai/index.html", names)

    def test_validate_audit_report_fails_when_missing_ai_layer_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "bad-report"
            report_dir.mkdir()
            (report_dir / "index.html").write_text("<!doctype html><title>Bad report</title>", encoding="utf-8")
            (report_dir / "LATEST-SEO-GEO-REPORT.md").write_text("# Latest SEO/GEO Report\n", encoding="utf-8")
            (report_dir / "audit.json").write_text(
                json.dumps(
                    {
                        "site": "example.test",
                        "audited_url": "https://example.test/",
                        "generated_at": "2026-06-21T10:00:00+02:00",
                        "report_language": "en",
                        "summary": {"headline": "Missing AI layer.", "status": "partial"},
                        "findings": [],
                        "sources": [{"label": "Fixture", "url": "https://example.test/"}],
                        "screenshot_status": "unavailable: fixture",
                        "responsive_study": {
                            "summary": {
                                "status": "unavailable",
                                "verdict": "Browser evidence was not captured for this fixture.",
                            }
                        },
                        "ai_layer_current_state": {
                            "llms_txt": False,
                            "for_ai": False,
                            "for_ai_json": False,
                            "for_ai_txt": False,
                        },
                    },
                    indent=2,
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

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ai_layer_package", result.stderr)


if __name__ == "__main__":
    unittest.main()
