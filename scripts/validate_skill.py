#!/usr/bin/env python3
"""Validate the SEO + GEO Growth Agent Skill repository."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "manifest.json",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def warn(message: str) -> None:
    print(f"WARN: {message}")


def read_manifest() -> dict:
    path = ROOT / "manifest.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("manifest.json is missing")
    except json.JSONDecodeError as exc:
        fail(f"manifest.json is invalid JSON: {exc}")


def check_required_files() -> None:
    for rel in REQUIRED_ROOT_FILES:
        if not (ROOT / rel).is_file():
            fail(f"missing required root file: {rel}")


def check_manifest_paths(manifest: dict) -> None:
    entrypoint = manifest.get("entrypoint")
    if not isinstance(entrypoint, str) or not entrypoint:
        fail("manifest.entrypoint must be a non-empty string")
    if not (ROOT / entrypoint).is_file():
        fail(f"manifest entrypoint not found: {entrypoint}")

    for key in ("templates", "references"):
        values = manifest.get(key, [])
        if not isinstance(values, list):
            fail(f"manifest.{key} must be a list")
        for rel in values:
            if not isinstance(rel, str):
                fail(f"manifest.{key} contains a non-string path: {rel!r}")
            if not (ROOT / rel).is_file():
                fail(f"manifest.{key} path not found: {rel}")


def check_manifest_directory_sync(manifest: dict) -> None:
    for key, dirname in (("templates", "templates"), ("references", "references")):
        declared = {Path(p).as_posix() for p in manifest.get(key, [])}
        actual = {
            p.relative_to(ROOT).as_posix()
            for p in (ROOT / dirname).glob("**/*")
            if p.is_file()
        }
        missing_in_manifest = sorted(actual - declared)
        stale_in_manifest = sorted(declared - actual)
        if missing_in_manifest:
            warn(f"files present in {dirname}/ but missing from manifest.{key}: {missing_in_manifest}")
        if stale_in_manifest:
            fail(f"manifest.{key} has stale paths: {stale_in_manifest}")


def check_no_obvious_secrets() -> None:
    # Deliberately conservative patterns to avoid false positives such as `risk-red-team.md`.
    suspicious_patterns = {
        "GitHub classic token": re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
        "GitHub fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
        "OpenAI-style API key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        "private key block": re.compile(r"BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY"),
    }
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in suspicious_patterns.items():
            if pattern.search(text):
                fail(f"possible secret pattern {name!r} found in {rel}")


def main() -> None:
    check_required_files()
    manifest = read_manifest()
    check_manifest_paths(manifest)
    check_manifest_directory_sync(manifest)
    check_no_obvious_secrets()
    print("OK: skill repository validation passed")


if __name__ == "__main__":
    main()
