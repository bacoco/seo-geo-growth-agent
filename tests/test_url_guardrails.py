#!/usr/bin/env python3
"""Regression tests for network URL guardrails."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class UrlGuardrailsTest(unittest.TestCase):
    def test_seo_geo_audit_rejects_non_http_scheme(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "seo_geo_audit.py"),
                    "file:///tmp/index.html",
                    "--output-dir",
                    tmp,
                    "--plan-only",
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Only http:// and https:// URLs are supported", result.stderr)

    def test_local_targets_require_allow_local_but_can_be_planned_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            blocked = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "seo_geo_audit.py"),
                    "http://127.0.0.1:8765/",
                    "--output-dir",
                    str(Path(tmp) / "blocked"),
                    "--plan-only",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn("--allow-local", blocked.stderr)

            allowed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "seo_geo_audit.py"),
                    "http://127.0.0.1:8765/",
                    "--output-dir",
                    str(Path(tmp) / "allowed"),
                    "--plan-only",
                    "--allow-local",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
            plan = json.loads((Path(tmp) / "allowed" / "audit-plan.json").read_text(encoding="utf-8"))
            self.assertIn("--allow-local", "\n".join(plan["next_commands"]))

    def test_validate_ard_catalog_rejects_file_url_and_requires_allow_local_for_private_http(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_url = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_ard_catalog.py"),
                    f"file://{Path(tmp) / 'ai-catalog.json'}",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(file_url.returncode, 0)
            self.assertIn("Only http:// and https:// URLs are supported", file_url.stderr)

            site_dir = Path(tmp) / "site"
            site_dir.mkdir()
            (site_dir / "ai-catalog.json").write_text(
                json.dumps(
                    {
                        "specVersion": "1.0",
                        "entries": [
                            {
                                "identifier": "urn:air:example.com:skill:test",
                                "type": "application/ai-skill+md",
                                "url": "https://example.com",
                                "representativeQueries": ["audit my site", "generate an AI layer"],
                            }
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *args, **kwargs: QuietHandler(*args, directory=site_dir, **kwargs))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}/ai-catalog.json"
                blocked = subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "validate_ard_catalog.py"), url],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertNotEqual(blocked.returncode, 0)
                self.assertIn("--allow-local", blocked.stderr)

                allowed = subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "validate_ard_catalog.py"), url, "--allow-local"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)

            self.assertEqual(allowed.returncode, 0, allowed.stderr)

    def test_check_ard_readiness_rejects_local_without_allow_local(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "ard.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "check_ard_readiness.py"),
                    "--url",
                    "http://127.0.0.1:8765/",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--allow-local", result.stderr)

    def test_capture_site_screenshots_rejects_data_and_local_without_allow_local_before_browser_launch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_url = subprocess.run(
                [
                    "node",
                    str(ROOT / "scripts" / "capture_site_screenshots.mjs"),
                    "--url",
                    "data:text/html,<h1>Fixture</h1>",
                    "--output-dir",
                    str(Path(tmp) / "screenshots"),
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(data_url.returncode, 0)
            self.assertIn("Only http:// and https:// URLs are supported", data_url.stderr)

            local_url = subprocess.run(
                [
                    "node",
                    str(ROOT / "scripts" / "capture_site_screenshots.mjs"),
                    "--url",
                    "http://127.0.0.1:8765/",
                    "--output-dir",
                    str(Path(tmp) / "screenshots"),
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(local_url.returncode, 0)
            self.assertIn("--allow-local", local_url.stderr)


if __name__ == "__main__":
    unittest.main()
