#!/usr/bin/env python3
"""Tests for audited-site screenshot and responsive-study capture."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def chrome_available() -> bool:
    candidates = [
        os.environ.get("CHROME_PATH"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    return any(candidate and Path(candidate).exists() for candidate in candidates)


class SiteCaptureTest(unittest.TestCase):
    def test_capture_site_screenshots_can_emit_responsive_study(self) -> None:
        if not chrome_available():
            self.skipTest("Chrome/Chromium not available")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            html = """<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Responsive fixture</title>
  <style>body{font-family:sans-serif;margin:0;padding:24px;max-width:720px}</style>
</head>
<body>
  <main>
    <h1>Responsive fixture</h1>
    <p>This fixture has enough visible text to be measured by the responsive study script without
    depending on external network resources or browser-specific default content.</p>
  </main>
</body>
</html>"""
            url = f"data:text/html;charset=utf-8,{quote(html)}"
            evidence_path = tmp_path / "site-visual-evidence.json"
            study_path = tmp_path / "responsive-study.json"

            result = subprocess.run(
                [
                    "node",
                    str(ROOT / "scripts" / "capture_site_screenshots.mjs"),
                    "--url",
                    url,
                    "--output-dir",
                    str(tmp_path / "screenshots"),
                    "--evidence-out",
                    str(evidence_path),
                    "--study-out",
                    str(study_path),
                ],
                capture_output=True,
                text=True,
                timeout=20,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((tmp_path / "screenshots" / "desktop.png").is_file())
            self.assertTrue((tmp_path / "screenshots" / "mobile.png").is_file())
            self.assertTrue(evidence_path.is_file())
            self.assertTrue(study_path.is_file())

            study = json.loads(study_path.read_text(encoding="utf-8"))
            self.assertEqual(study["summary"]["status"], "pass")
            self.assertEqual(len(study["viewports"]), 2)
            self.assertFalse(study["viewports"][0]["metrics"]["horizontalOverflow"])


if __name__ == "__main__":
    unittest.main()
