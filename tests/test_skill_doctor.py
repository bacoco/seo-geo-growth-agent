#!/usr/bin/env python3
"""Tests for installed skill doctor tooling."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillDoctorTest(unittest.TestCase):
    def test_skill_doctor_passes_on_runtime_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install_dir = Path(tmp) / "seo-geo-growth-agent"
            install = subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), str(install_dir)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(install.returncode, 0, install.stderr)

            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "skill_doctor.py"), str(install_dir)],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OK: installed skill doctor passed", result.stdout)

    def test_sync_and_doctor_dry_run_lists_codex_and_claude_targets(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "sync_and_doctor.py"),
                "--target",
                "all",
                "--dry-run",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("codex", result.stdout)
        self.assertIn("claude", result.stdout)
        self.assertIn("dry-run", result.stdout)


if __name__ == "__main__":
    unittest.main()
