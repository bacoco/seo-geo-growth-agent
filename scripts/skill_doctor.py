#!/usr/bin/env python3
"""Validate an installed seo-geo-growth-agent runtime package."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "SKILL.md",
    "INSTALL_FOR_AGENTS.md",
    "LICENSE",
    "manifest.json",
    "references",
    "templates",
    "runbooks",
    "evals",
    "scripts/generate_html_audit_report.py",
    "scripts/serve_report.py",
    "scripts/capture_site_screenshots.mjs",
    "scripts/skill_doctor.py",
]

FORBIDDEN_PATHS = [
    ".git",
    ".github",
    ".gitignore",
    "assets",
    "scripts/install.sh",
    "scripts/validate_skill.py",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("install_dir", type=Path, help="Installed seo-geo-growth-agent skill directory.")
    return parser.parse_args()


def check_paths(root: Path) -> None:
    if not root.is_dir():
        fail(f"install directory does not exist: {root}")
    if root.name != "seo-geo-growth-agent":
        fail("install directory must be named seo-geo-growth-agent")
    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            fail(f"missing required runtime path: {rel}")
    for rel in FORBIDDEN_PATHS:
        if (root / rel).exists():
            fail(f"maintenance path should not be installed: {rel}")


def check_manifest(root: Path) -> dict:
    manifest_path = root / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"manifest.json is invalid: {exc}")
    for section in ("templates", "references", "routing_evals"):
        values = manifest.get(section, [])
        if not isinstance(values, list):
            fail(f"manifest.{section} must be a list")
        for rel in values:
            if not (root / rel).is_file():
                fail(f"manifest.{section} path missing from install: {rel}")
    for rel in manifest.get("runbooks", {}).values():
        if not (root / rel).is_file():
            fail(f"manifest.runbooks path missing from install: {rel}")
    for rel in manifest.get("scripts", {}).values():
        if not (root / rel).is_file():
            fail(f"manifest.scripts path missing from install: {rel}")
    return manifest


def check_script_syntax(root: Path, manifest: dict) -> None:
    for rel in manifest.get("scripts", {}).values():
        path = root / rel
        if path.suffix == ".py":
            result = subprocess.run([sys.executable, "-m", "py_compile", str(path)], capture_output=True, text=True)
            if result.returncode != 0:
                fail(f"{rel} has invalid Python syntax:\n{result.stderr.strip()}")
        if path.suffix == ".mjs":
            result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
            if result.returncode != 0:
                fail(f"{rel} has invalid JavaScript syntax:\n{result.stderr.strip()}")


def main() -> None:
    args = parse_args()
    root = args.install_dir.resolve()
    check_paths(root)
    manifest = check_manifest(root)
    check_script_syntax(root, manifest)
    print(f"OK: installed skill doctor passed for {root}")


if __name__ == "__main__":
    main()
