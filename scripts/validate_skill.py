#!/usr/bin/env python3
"""Validate the SEO + GEO Growth Agent Skill repository."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "INSTALL_FOR_AGENTS.md",
    "LICENSE",
    "manifest.json",
]

INTERNAL_PATH_PATTERN = re.compile(
    r"(?<![\w./-])((?:references|templates|runbooks|evals|scripts)/[A-Za-z0-9][A-Za-z0-9._/-]*\.[A-Za-z0-9]+)"
)
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".py", ".sh", ".mjs"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def warn(message: str) -> None:
    print(f"WARN: {message}")


def repo_files() -> list[tuple[Path, str]]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        files.append((path, rel))
    return files


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


def check_skill_description() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    try:
        frontmatter = text.split("---", 2)[1]
    except IndexError:
        fail("SKILL.md is missing YAML frontmatter")
    description_lines: list[str] = []
    in_description = False
    for line in frontmatter.splitlines():
        if line.startswith("description:"):
            in_description = True
            continue
        if in_description and line and not line.startswith(" "):
            break
        if in_description:
            description_lines.append(line.strip())
    description = "\n".join(line for line in description_lines if line)
    if not description:
        fail("SKILL.md description is missing")
    if len(description) > 1024:
        fail(f"SKILL.md description exceeds 1024 characters: {len(description)}")
    if not description.startswith("Use when"):
        fail('SKILL.md description must start with "Use when"')


def check_manifest_paths(manifest: dict) -> None:
    entrypoint = manifest.get("entrypoint")
    if not isinstance(entrypoint, str) or not entrypoint:
        fail("manifest.entrypoint must be a non-empty string")
    if not (ROOT / entrypoint).is_file():
        fail(f"manifest entrypoint not found: {entrypoint}")

    install_protocol = manifest.get("install_protocol")
    if not isinstance(install_protocol, str) or not install_protocol:
        fail("manifest.install_protocol must be a non-empty string")
    if not (ROOT / install_protocol).is_file():
        fail(f"manifest install_protocol not found: {install_protocol}")

    runbooks = manifest.get("runbooks", {})
    if not isinstance(runbooks, dict):
        fail("manifest.runbooks must be an object")
    bootstrap = runbooks.get("bootstrap")
    if not isinstance(bootstrap, str) or not bootstrap:
        fail("manifest.runbooks.bootstrap must be a non-empty string")
    if not (ROOT / bootstrap).is_file():
        fail(f"manifest runbooks.bootstrap not found: {bootstrap}")

    for key in ("templates", "references", "routing_evals"):
        values = manifest.get(key, [])
        if not isinstance(values, list):
            fail(f"manifest.{key} must be a list")
        for rel in values:
            if not isinstance(rel, str):
                fail(f"manifest.{key} contains a non-string path: {rel!r}")
            if not (ROOT / rel).is_file():
                fail(f"manifest.{key} path not found: {rel}")

    scripts = manifest.get("scripts", {})
    if not isinstance(scripts, dict):
        fail("manifest.scripts must be an object")
    for name, rel in scripts.items():
        if not isinstance(name, str) or not name:
            fail(f"manifest.scripts contains an invalid key: {name!r}")
        if not isinstance(rel, str) or not rel:
            fail(f"manifest.scripts.{name} must be a non-empty string path")
        if not (ROOT / rel).is_file():
            fail(f"manifest.scripts.{name} path not found: {rel}")


def check_manifest_directory_sync(manifest: dict) -> None:
    manifest_runbooks = manifest.get("runbooks", {})
    declared_runbooks = set(manifest_runbooks.values()) if isinstance(manifest_runbooks, dict) else set()

    sync_targets = (
        ("templates", "templates", set(manifest.get("templates", []))),
        ("references", "references", set(manifest.get("references", []))),
        ("routing_evals", "evals", set(manifest.get("routing_evals", []))),
        ("runbooks", "runbooks", declared_runbooks),
    )

    for key, dirname, declared_raw in sync_targets:
        declared = {Path(p).as_posix() for p in declared_raw}
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


def check_json_files() -> None:
    for path, rel in repo_files():
        if path.suffix != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{rel} is invalid JSON: {exc}")


def check_jsonl_files() -> None:
    for path, rel in repo_files():
        if path.suffix != ".jsonl":
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines:
            fail(f"{rel} is empty")
        is_routing_eval = rel.startswith("evals/")
        saw_true = False
        saw_false = False
        for index, line in enumerate(lines, start=1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"{rel}:{index} is invalid JSONL: {exc}")
            if not isinstance(data, dict):
                fail(f"{rel}:{index} JSONL entry must be an object")
            if not is_routing_eval:
                continue
            for key in ("input", "should_trigger", "expected_mode"):
                if key not in data:
                    fail(f"{rel}:{index} is missing required key: {key}")
            if not isinstance(data["input"], str) or not data["input"].strip():
                fail(f"{rel}:{index} input must be a non-empty string")
            if not isinstance(data["should_trigger"], bool):
                fail(f"{rel}:{index} should_trigger must be boolean")
            if not isinstance(data["expected_mode"], str) or not data["expected_mode"].strip():
                fail(f"{rel}:{index} expected_mode must be a non-empty string")
            saw_true = saw_true or data["should_trigger"]
            saw_false = saw_false or not data["should_trigger"]
        if not is_routing_eval:
            continue
        if len(lines) < 8:
            fail(f"{rel} must contain at least 8 routing cases")
        if not saw_true or not saw_false:
            fail(f"{rel} must include both positive and negative routing cases")


def check_internal_file_references() -> None:
    broken = []
    for path, rel in repo_files():
        if path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in INTERNAL_PATH_PATTERN.finditer(text):
            target = match.group(1).rstrip(".,;:)]}\"'")
            if not (ROOT / target).is_file():
                broken.append(f"{rel}: {target}")
    if broken:
        fail("broken internal file references:\n  " + "\n  ".join(sorted(set(broken))))


def check_reference_heading_numbers() -> None:
    mismatches = []
    for path in (ROOT / "references").glob("[0-9][0-9]-*.md"):
        expected = path.name.split("-", 1)[0]
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        match = re.match(r"^#\s+(\d{2})\b", first_line)
        if not match:
            mismatches.append(f"{path.relative_to(ROOT).as_posix()}: missing numbered H1")
            continue
        actual = match.group(1)
        if actual != expected:
            mismatches.append(
                f"{path.relative_to(ROOT).as_posix()}: H1 starts with {actual}, expected {expected}"
            )
    if mismatches:
        fail("reference heading number mismatch:\n  " + "\n  ".join(mismatches))


def check_install_script() -> None:
    script = ROOT / "scripts" / "install.sh"
    syntax = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
    if syntax.returncode != 0:
        fail(f"scripts/install.sh has invalid shell syntax:\n{syntax.stderr.strip()}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        safe_dest = tmp_path / "seo-geo-growth-agent"
        result = subprocess.run(
            ["bash", str(script), str(safe_dest)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            fail(f"install smoke test failed:\n{result.stderr.strip() or result.stdout.strip()}")

        for rel in (
            "SKILL.md",
            "INSTALL_FOR_AGENTS.md",
            "LICENSE",
            "manifest.json",
            "references",
            "templates",
            "runbooks",
            "evals",
            "examples/reference-audit/audit.json",
            "examples/reference-audit/index.html",
            "examples/reference-audit/LATEST-SEO-GEO-REPORT.md",
            "examples/reference-audit/report-validation.json",
            "examples/reference-audit/ai-layer-package.zip",
            "scripts/seo_geo_audit.py",
            "scripts/run_full_audit.py",
            "scripts/validate_audit_report.py",
            "scripts/generate_html_audit_report.py",
            "scripts/generate_ai_layer_package.py",
            "scripts/generate_owner_data_request.py",
            "scripts/generate_ard_catalog.py",
            "scripts/validate_ard_catalog.py",
            "scripts/check_ard_readiness.py",
            "scripts/compare_audit_reports.py",
            "scripts/generate_geo_citation_panel.py",
            "scripts/runtime_config.py",
            "scripts/serve_report.py",
            "scripts/capture_site_screenshots.mjs",
            "scripts/skill_demo.py",
            "scripts/skill_doctor.py",
        ):
            if not (safe_dest / rel).exists():
                fail(f"install smoke test did not copy expected path: {rel}")
        for rel in (".github", ".gitignore", "assets", "scripts/install.sh", "scripts/validate_skill.py"):
            if (safe_dest / rel).exists():
                fail(f"install smoke test copied maintenance path unexpectedly: {rel}")

        sentinel = safe_dest / "LOCAL_SENTINEL.txt"
        sentinel.write_text("preserve previous install", encoding="utf-8")
        reinstall = subprocess.run(
            ["bash", str(script), str(safe_dest)],
            capture_output=True,
            text=True,
        )
        if reinstall.returncode != 0:
            fail(f"install reinstall smoke test failed:\n{reinstall.stderr.strip() or reinstall.stdout.strip()}")
        backups = list(tmp_path.glob("seo-geo-growth-agent.backup-*"))
        if not backups:
            fail("install reinstall smoke test did not create a timestamped backup")
        if not any((backup / "LOCAL_SENTINEL.txt").is_file() for backup in backups):
            fail("install reinstall smoke test did not preserve previous install contents")

        unsafe_dest = tmp_path / "unsafe-destination"
        unsafe = subprocess.run(
            ["bash", str(script), str(unsafe_dest)],
            capture_output=True,
            text=True,
        )
        if unsafe.returncode == 0:
            fail("install script accepted a custom destination not named seo-geo-growth-agent")


def check_runtime_script_syntax(manifest: dict) -> None:
    scripts = manifest.get("scripts", {})
    for rel in scripts.values():
        path = ROOT / rel
        if path.suffix == ".py":
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError as exc:
                fail(f"{rel} has invalid Python syntax:\n{exc}")
        if path.suffix == ".mjs":
            result = subprocess.run(
                ["node", "--check", str(path)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                fail(f"{rel} has invalid JavaScript syntax:\n{result.stderr.strip()}")


def check_no_obvious_secrets() -> None:
    # Deliberately conservative patterns to avoid false positives such as `risk-red-team.md`.
    suspicious_patterns = {
        "GitHub classic token": re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
        "GitHub fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
        "OpenAI-style API key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        "private key block": re.compile(r"BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY"),
    }
    for path, rel in repo_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in suspicious_patterns.items():
            if pattern.search(text):
                fail(f"possible secret pattern {name!r} found in {rel}")


def main() -> None:
    check_required_files()
    check_skill_description()
    manifest = read_manifest()
    check_manifest_paths(manifest)
    check_manifest_directory_sync(manifest)
    check_json_files()
    check_jsonl_files()
    check_internal_file_references()
    check_reference_heading_numbers()
    check_runtime_script_syntax(manifest)
    check_install_script()
    check_no_obvious_secrets()
    print("OK: skill repository validation passed")


if __name__ == "__main__":
    main()
