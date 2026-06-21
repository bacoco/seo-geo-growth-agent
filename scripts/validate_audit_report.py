#!/usr/bin/env python3
"""Validate a generated SEO/GEO audit report directory."""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from typing import Any


AI_LAYER_KEYS = ("llms_txt", "for_ai", "for_ai_json", "for_ai_txt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-dir", required=True, type=Path, help="Report directory containing audit.json and index.html.")
    parser.add_argument("--output", type=Path, help="Optional JSON validation result path.")
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"missing JSON file: {path.name}"
    except json.JSONDecodeError as exc:
        return None, f"{path.name} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return None, f"{path.name} must contain a JSON object"
    return data, ""


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def report_member_path(report_dir: Path, value: Any) -> Path | None:
    if not value:
        return None
    raw = Path(str(value))
    candidate = raw if raw.is_absolute() else report_dir / raw
    resolved = candidate.resolve()
    if not is_within(resolved, report_dir):
        return None
    return resolved


def has_visual_evidence(audit: dict[str, Any], report_dir: Path) -> bool:
    for key in ("site_visual_evidence", "visual_evidence"):
        visuals = audit.get(key)
        if not isinstance(visuals, list):
            continue
        for item in visuals:
            if not isinstance(item, dict):
                continue
            report_path = item.get("path")
            source_path = item.get("source_path")
            report_member = report_member_path(report_dir, report_path)
            source_member = report_member_path(report_dir, source_path)
            if report_member and report_member.is_file():
                return True
            if source_member and source_member.is_file():
                return True
    return False


def missing_ai_layer(current: dict[str, Any]) -> bool:
    return any(current.get(key) is False for key in AI_LAYER_KEYS)


def validate_package(audit: dict[str, Any], report_dir: Path, errors: list[str]) -> None:
    package = audit.get("ai_layer_package")
    if not isinstance(package, dict):
        errors.append("ai_layer_package is required when AI-readable files are missing")
        return
    files = package.get("files")
    if not isinstance(files, list) or not files:
        errors.append("ai_layer_package.files must list generated files")
        return

    listed_paths: list[str] = []
    for item in files:
        if not isinstance(item, dict) or not item.get("path"):
            errors.append("ai_layer_package.files entries must include path")
            continue
        relative = str(item["path"])
        listed_paths.append(relative)
        member = report_member_path(report_dir, relative)
        if member is None:
            errors.append(f"ai_layer_package file path escapes report directory: {relative}")
            continue
        if not member.is_file():
            errors.append(f"ai_layer_package file is missing: {relative}")

    zip_path = package.get("zip_path")
    if zip_path:
        zip_file = report_member_path(report_dir, zip_path)
        if zip_file is None:
            errors.append(f"ai_layer_package zip path escapes report directory: {zip_path}")
            return
        if not zip_file.is_file():
            errors.append(f"ai_layer_package zip is missing: {zip_path}")
            return
        try:
            with zipfile.ZipFile(zip_file) as archive:
                names = set(archive.namelist())
        except zipfile.BadZipFile:
            errors.append(f"ai_layer_package zip is invalid: {zip_path}")
            return
        for relative in listed_paths:
            if relative not in names:
                errors.append(f"ai_layer_package zip does not contain: {relative}")


def validate_report(report_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    report_dir = report_dir.resolve()

    if not report_dir.is_dir():
        return {"status": "fail", "errors": [f"report directory does not exist: {report_dir}"], "warnings": []}

    required_files = ("audit.json", "index.html", "LATEST-SEO-GEO-REPORT.md")
    for relative in required_files:
        if not (report_dir / relative).is_file():
            errors.append(f"missing required report file: {relative}")

    audit, load_error = load_json(report_dir / "audit.json")
    if load_error:
        errors.append(load_error)
        return {"status": "fail", "errors": errors, "warnings": warnings}
    assert audit is not None

    for field in ("site", "audited_url", "generated_at", "report_language", "summary", "findings", "sources"):
        if field not in audit:
            errors.append(f"audit.json missing required field: {field}")
    if not isinstance(audit.get("summary"), dict):
        errors.append("audit.summary must be an object")
    if not isinstance(audit.get("findings"), list):
        errors.append("audit.findings must be an array")
    if not isinstance(audit.get("sources"), list) or not audit.get("sources"):
        errors.append("audit.sources must be a non-empty array")

    if not has_visual_evidence(audit, report_dir) and not audit.get("screenshot_status"):
        errors.append("site screenshots are missing and screenshot_status does not explain why")

    responsive = audit.get("responsive_study")
    if not isinstance(responsive, dict):
        errors.append("responsive_study is required, or must explicitly mark browser evidence unavailable")
    else:
        summary = responsive.get("summary")
        if not isinstance(summary, dict) or not summary.get("status") or not summary.get("verdict"):
            errors.append("responsive_study.summary must include status and verdict")

    current = audit.get("ai_layer_current_state")
    if isinstance(current, dict) and missing_ai_layer(current):
        validate_package(audit, report_dir, errors)
    elif audit.get("ai_layer_package"):
        validate_package(audit, report_dir, errors)
    else:
        warnings.append("no ai_layer_package supplied")

    result = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "report_dir": str(report_dir),
    }
    return result


def main() -> None:
    args = parse_args()
    result = validate_report(args.report_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if result["status"] == "pass":
        print(f"OK: audit report validation passed for {args.report_dir}")
        raise SystemExit(0)
    print("ERROR: audit report validation failed", file=sys.stderr)
    for error in result["errors"]:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
