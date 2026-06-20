#!/usr/bin/env python3
"""Tests for generated AI-layer publication packages."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AiLayerPackageTest(unittest.TestCase):
    def test_generate_ai_layer_package_updates_audit_and_zip(self) -> None:
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
                        "generated_at": "2026-06-20T18:00:00+02:00",
                        "summary": {
                            "headline": "Example needs an AI-readable citation layer.",
                            "decision": "Publish llms.txt and a /for-ai package.",
                            "status": "partial",
                        },
                        "findings": [
                            {
                                "priority": "P1",
                                "title": "Missing /for-ai",
                                "observed": ["/for-ai returns 404"],
                                "recommended": ["Publish /for-ai and /for-ai.json"],
                            }
                        ],
                        "sources": [{"label": "Homepage", "url": "https://example.com/"}],
                    },
                    indent=2,
                ),
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
            package_dir = output_dir / "ai-layer-package"
            expected_files = [
                "llms.txt",
                "for-ai/index.html",
                "for-ai.json",
                "for-ai.txt",
                "schema-webpage.jsonld",
                "AI_LAYER_INSTALL.md",
                "manifest.json",
            ]
            for relative in expected_files:
                self.assertTrue((package_dir / relative).is_file(), relative)
            self.assertTrue((output_dir / "ai-layer-package.zip").is_file())

            generated_json = json.loads((package_dir / "for-ai.json").read_text(encoding="utf-8"))
            self.assertEqual(generated_json["canonical_url"], "https://example.com/")
            self.assertIn("do_not", generated_json)
            self.assertIn("citation_guidance", generated_json)

            updated_audit = json.loads(audit_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_audit["ai_layer_package"]["zip_path"], "ai-layer-package.zip")
            self.assertEqual(len(updated_audit["ai_layer_package"]["files"]), len(expected_files))

            with zipfile.ZipFile(output_dir / "ai-layer-package.zip") as archive:
                names = set(archive.namelist())
            self.assertIn("ai-layer-package/llms.txt", names)
            self.assertIn("ai-layer-package/for-ai/index.html", names)


if __name__ == "__main__":
    unittest.main()
