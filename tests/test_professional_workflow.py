#!/usr/bin/env python3
"""Tests for professional audit workflow utilities."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfessionalWorkflowTest(unittest.TestCase):
    def test_owner_data_request_writes_intake_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "owner-data"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_owner_data_request.py"),
                    "--site",
                    "https://github.com/bacoco/seo-geo-growth-agent",
                    "--output-dir",
                    str(output_dir),
                    "--language",
                    "en",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            intake_path = output_dir / "owner-data-intake.csv"
            self.assertTrue(intake_path.is_file())
            with intake_path.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertGreaterEqual(len(rows), 5)
            self.assertIn("Google Search Console", {row["source_label"] for row in rows})
            self.assertIn("Cloudflare Analytics", {row["source_label"] for row in rows})
            self.assertTrue(all(row["status"] == "requested" for row in rows))
            self.assertIn("owner-data-intake.csv", result.stdout)

    def test_skill_demo_validates_golden_audit_and_writes_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "demo"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "skill_demo.py"),
                    "--output-dir",
                    str(output_dir),
                    "--no-serve",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            demo_result = output_dir / "demo-result.json"
            self.assertTrue(demo_result.is_file())
            data = json.loads(demo_result.read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "pass")
            self.assertEqual(data["golden_audit"]["validation_status"], "pass")
            self.assertEqual(data["golden_audit"]["site"], "bacoco/seo-geo-growth-agent")
            self.assertTrue(Path(data["golden_audit"]["index_html"]).is_file())
            self.assertIn("run_full_audit", " ".join(data["next_commands"]))

    def test_installed_skill_demo_is_self_contained(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            install_dir = tmp_path / "skills" / "seo-geo-growth-agent"
            install = subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), str(install_dir)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(install.returncode, 0, install.stderr)

            output_dir = tmp_path / "demo"
            result = subprocess.run(
                [
                    sys.executable,
                    str(install_dir / "scripts" / "skill_demo.py"),
                    "--output-dir",
                    str(output_dir),
                    "--install-dir",
                    str(install_dir),
                    "--no-serve",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((output_dir / "demo-result.json").read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "pass")
            self.assertEqual(data["install_doctor"]["status"], "pass")
            self.assertTrue((install_dir / "examples" / "reference-audit" / "index.html").is_file())

    def test_runtime_manifest_installs_demo_script_and_owner_data_template(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.3.1")
        self.assertEqual(manifest["scripts"]["skill_demo"], "scripts/skill_demo.py")
        self.assertIn("templates/owner-data-intake.csv", manifest["templates"])


if __name__ == "__main__":
    unittest.main()
