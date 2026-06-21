#!/usr/bin/env python3
"""Sync the source skill into local Codex/Claude destinations and run doctors."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "seo-geo-growth-agent"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["codex", "claude", "all"], default="all")
    parser.add_argument("--dry-run", action="store_true", help="Print destinations without installing.")
    return parser.parse_args()


def targets(selection: str) -> list[tuple[str, Path]]:
    values = []
    if selection in ("codex", "all"):
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        values.append(("codex", codex_home / "skills" / SKILL_NAME))
    if selection in ("claude", "all"):
        values.append(("claude", Path.home() / ".claude" / "skills" / SKILL_NAME))
    return values


def run(command: list[str]) -> None:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise SystemExit(f"required command not found: {command[0]}") from exc
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip())
    if result.stdout.strip():
        print(result.stdout.strip())


def main() -> None:
    args = parse_args()
    install_script = ROOT / "scripts" / "install.sh"
    doctor_script = ROOT / "scripts" / "skill_doctor.py"
    if not install_script.is_file():
        raise SystemExit("sync_and_doctor.py must be run from the source repository; scripts/install.sh is missing.")
    for name, destination in targets(args.target):
        if args.dry_run:
            print(f"dry-run: {name} -> {destination}")
            continue
        run(["bash", str(install_script), str(destination)])
        run([sys.executable, str(doctor_script), str(destination)])
        print(f"synced: {name} -> {destination}")


if __name__ == "__main__":
    main()
