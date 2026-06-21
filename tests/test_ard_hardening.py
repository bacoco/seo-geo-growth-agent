#!/usr/bin/env python3
"""Tests for ARD catalog validation and readiness tooling."""
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


class ArdHardeningTest(unittest.TestCase):
    def write_valid_catalog(self, path: Path) -> dict:
        catalog = {
            "specVersion": "1.0",
            "host": {
                "displayName": "SEO GEO Growth Agent",
                "identifier": "https://example.com",
                "documentationUrl": "https://example.com/docs",
            },
            "entries": [
                {
                    "identifier": "urn:air:example.com:skill:seo-geo-growth-agent",
                    "displayName": "SEO GEO Growth Agent",
                    "type": "application/ai-skill+md",
                    "url": "https://github.com/bacoco/seo-geo-growth-agent",
                    "representativeQueries": [
                        "audit my website for AI search readiness",
                        "generate a citation-safe for-ai package",
                    ],
                }
            ],
        }
        path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
        return catalog

    def test_validate_ard_catalog_accepts_valid_generated_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog_path = Path(tmp) / "ai-catalog.json"
            self.write_valid_catalog(catalog_path)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_ard_catalog.py"),
                    str(catalog_path),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OK", result.stdout)

    def test_validate_ard_catalog_rejects_invalid_catalog_shapes(self) -> None:
        invalid_variants = {
            "bad-version": {"specVersion": "0.9"},
            "bad-identifier": {
                "specVersion": "1.0",
                "entries": [{"identifier": "not-a-urn", "type": "application/ai-skill+md", "url": "https://example.com"}],
            },
            "url-and-data": {
                "specVersion": "1.0",
                "entries": [
                    {
                        "identifier": "urn:air:example.com:skill:test",
                        "type": "application/ai-skill+md",
                        "url": "https://example.com",
                        "data": {"inline": True},
                    }
                ],
            },
            "too-few-queries": {
                "specVersion": "1.0",
                "entries": [
                    {
                        "identifier": "urn:air:example.com:skill:test",
                        "type": "application/ai-skill+md",
                        "url": "https://example.com",
                        "representativeQueries": ["one query"],
                    }
                ],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            for name, data in invalid_variants.items():
                path = Path(tmp) / f"{name}.json"
                path.write_text(json.dumps(data) + "\n", encoding="utf-8")
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts" / "validate_ard_catalog.py"),
                        str(path),
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(result.returncode, 0, name)
                self.assertIn("ERROR", result.stderr)

    def test_check_ard_readiness_detects_well_known_link_and_agentmap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            site_dir = Path(tmp) / "site"
            site_dir.mkdir()
            well_known = site_dir / ".well-known"
            well_known.mkdir()
            catalog = self.write_valid_catalog(well_known / "ai-catalog.json")

            server = ThreadingHTTPServer(
                ("127.0.0.1", 0),
                lambda *args, **kwargs: QuietHandler(*args, directory=site_dir, **kwargs),
            )
            port = server.server_port
            base_url = f"http://127.0.0.1:{port}"
            (site_dir / "index.html").write_text(
                f"""<!doctype html>
<html>
<head>
  <link rel="ai-catalog" href="{base_url}/.well-known/ai-catalog.json">
  <title>ARD fixture</title>
</head>
<body><h1>ARD fixture</h1></body>
</html>""",
                encoding="utf-8",
            )
            (site_dir / "robots.txt").write_text(
                f"User-agent: *\nAllow: /\nAgentmap: {base_url}/.well-known/ai-catalog.json\n",
                encoding="utf-8",
            )

            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            output_path = Path(tmp) / "ard-readiness.json"
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts" / "check_ard_readiness.py"),
                        "--url",
                        f"{base_url}/",
                        "--output",
                        str(output_path),
                        "--allow-local",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)

            self.assertEqual(result.returncode, 0, result.stderr)
            readiness = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(readiness["status"], "present")
            self.assertEqual(readiness["signals"]["well_known"]["status"], "present")
            self.assertEqual(readiness["signals"]["html_link"]["status"], "present")
            self.assertEqual(readiness["signals"]["robots_agentmap"]["status"], "present")
            self.assertEqual(readiness["validation"]["status"], "pass")
            self.assertEqual(readiness["entries"][0]["identifier"], catalog["entries"][0]["identifier"])

    def test_readme_explains_why_ard_matters(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Why ARD Matters", readme)
        self.assertIn("not a ranking factor", readme.lower())
        self.assertIn("agentic resource", readme.lower())


if __name__ == "__main__":
    unittest.main()
