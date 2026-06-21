#!/usr/bin/env python3
"""Tests for committed reference audit examples."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReferenceExamplesTest(unittest.TestCase):
    def test_reference_audit_example_is_complete_and_valid(self) -> None:
        example_dir = ROOT / "examples" / "reference-audit"
        expected = [
            "audit.json",
            "index.html",
            "LATEST-SEO-GEO-REPORT.md",
            "ai-layer-package.zip",
            "ai-layer-package/llms.txt",
            "ai-layer-package/for-ai/index.html",
            "ai-layer-package/for-ai.json",
            "ai-layer-package/for-ai.txt",
            "ai-layer-package/schema-webpage.jsonld",
            "ai-layer-package/AI_LAYER_INSTALL.md",
            "ai-layer-package/manifest.json",
        ]
        for relative in expected:
            self.assertTrue((example_dir / relative).exists(), relative)

        audit = json.loads((example_dir / "audit.json").read_text(encoding="utf-8"))
        self.assertEqual(audit["site"], "reference.example")
        self.assertEqual(audit["report_language"], "en")
        self.assertEqual(audit["ai_layer_package"]["status"], "generated")

        with zipfile.ZipFile(example_dir / "ai-layer-package.zip") as archive:
            names = set(archive.namelist())
        self.assertIn("ai-layer-package/llms.txt", names)
        self.assertIn("ai-layer-package/for-ai/index.html", names)

        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_audit_report.py"),
                "--report-dir",
                str(example_dir),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
