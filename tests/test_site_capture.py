#!/usr/bin/env python3
"""Tests for audited-site screenshot and responsive-study capture."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import threading
import unittest
from base64 import b64decode
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PNG_1X1 = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


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
    <a href="#contact">Start now</a>
    <p>Trusted by research teams and public institutions.</p>
  </main>
</body>
</html>"""
            url = f"data:text/html;charset=utf-8,{quote(html)}"
            evidence_path = tmp_path / "site-visual-evidence.json"
            study_path = tmp_path / "responsive-study.json"
            evidence_engine_path = tmp_path / "evidence-engine.json"

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
                    "--evidence-engine-out",
                    str(evidence_engine_path),
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
            self.assertTrue(evidence_engine_path.is_file())

            study = json.loads(study_path.read_text(encoding="utf-8"))
            self.assertEqual(study["summary"]["status"], "pass")
            self.assertEqual(len(study["viewports"]), 2)
            self.assertFalse(study["viewports"][0]["metrics"]["horizontalOverflow"])
            self.assertEqual(study["viewports"][0]["metrics"]["imageLoadStates"]["missing_after_scroll"], 0)

            evidence_engine = json.loads(evidence_engine_path.read_text(encoding="utf-8"))
            self.assertEqual(evidence_engine["url"], url)
            self.assertIn("console_watch", evidence_engine)
            self.assertIn("network_watch", evidence_engine)
            self.assertIn("cache_cdn_watch", evidence_engine)
            self.assertIn("design_watch_metrics", evidence_engine)
            self.assertEqual(evidence_engine["console_watch"]["summary"]["total"], 0)
            self.assertEqual(evidence_engine["network_watch"]["summary"]["failed_requests"], 0)
            self.assertTrue(evidence_engine["design_watch_metrics"]["desktop"]["cta_visible"])

    def test_capture_distinguishes_lazy_loaded_images_from_broken_images(self) -> None:
        if not chrome_available():
            self.skipTest("Chrome/Chromium not available")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            site_dir = tmp_path / "site"
            site_dir.mkdir()
            (site_dir / "pixel.png").write_bytes(PNG_1X1)
            (site_dir / "index.html").write_text(
                """<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lazy image fixture</title>
  <style>
    body{font-family:sans-serif;margin:0;padding:24px;max-width:720px}
    .spacer{height:5200px}
    img{display:block;width:32px;height:32px;margin:16px 0}
  </style>
</head>
<body>
  <main>
    <h1>Lazy image fixture</h1>
    <p>This fixture has enough visible text for the responsive study and places lazy images below the fold.</p>
    <div class="spacer"></div>
    <img loading="lazy" src="/pixel.png" alt="valid lazy image">
    <img loading="lazy" src="/missing.png" alt="broken lazy image">
  </main>
</body>
</html>""",
                encoding="utf-8",
            )

            class Handler(SimpleHTTPRequestHandler):
                def log_message(self, format: str, *args: object) -> None:
                    return

            server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *args, **kwargs: Handler(*args, directory=site_dir, **kwargs))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                study_path = tmp_path / "responsive-study.json"
                result = subprocess.run(
                    [
                        "node",
                        str(ROOT / "scripts" / "capture_site_screenshots.mjs"),
                        "--url",
                        f"http://127.0.0.1:{server.server_port}/index.html",
                        "--output-dir",
                        str(tmp_path / "screenshots"),
                        "--study-out",
                        str(study_path),
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
            study = json.loads(study_path.read_text(encoding="utf-8"))
            desktop_states = study["viewports"][0]["metrics"]["imageLoadStates"]
            self.assertGreaterEqual(desktop_states["loaded_after_scroll"], 1)
            self.assertEqual(desktop_states["broken"], 1)
            self.assertEqual(desktop_states["missing_after_scroll"], 1)
            self.assertIn("1 image(s) are broken after scroll.", study["viewports"][0]["issues"])


if __name__ == "__main__":
    unittest.main()
