#!/usr/bin/env python3
"""Run a deterministic demo/doctor check for seo-geo-growth-agent."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GOLDEN_AUDIT_DIR = ROOT / "examples" / "reference-audit"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for demo-result.json and validation output.")
    parser.add_argument("--install-dir", type=Path, help="Optional installed skill directory to check with skill_doctor.py.")
    parser.add_argument("--no-serve", action="store_true", help="Do not start the local report server.")
    parser.add_argument("--port", type=int, default=8766, help="Preferred local report server port when serving.")
    parser.add_argument("--open", action="store_true", help="Open the report if serving.")
    return parser.parse_args()


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or f"Command failed: {' '.join(command)}")
    return result


def load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def validate_golden_audit(output_dir: Path) -> dict[str, Any]:
    validation_path = output_dir / "golden-audit-validation.json"
    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_audit_report.py"),
            "--report-dir",
            str(GOLDEN_AUDIT_DIR),
            "--output",
            str(validation_path),
        ]
    )
    audit = load_json(GOLDEN_AUDIT_DIR / "audit.json", {})
    validation = load_json(validation_path, {})
    return {
        "site": audit.get("site", "unknown"),
        "audited_url": audit.get("audited_url", "unknown"),
        "index_html": str(GOLDEN_AUDIT_DIR / "index.html"),
        "validation_json": str(validation_path),
        "validation_status": validation.get("status", "unknown"),
        "ai_layer_package": audit.get("ai_layer_package", {}).get("zip_path", "not generated"),
    }


def run_install_doctor(install_dir: Path | None) -> dict[str, Any]:
    if install_dir is None:
        return {"status": "not_run", "reason": "--install-dir not supplied"}
    result = run(
        [sys.executable, str(ROOT / "scripts" / "skill_doctor.py"), str(install_dir)],
        check=False,
    )
    return {
        "status": "pass" if result.returncode == 0 else "fail",
        "install_dir": str(install_dir),
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def serve_report(port: int, open_report: bool) -> None:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "serve_report.py"),
        "--dir",
        str(GOLDEN_AUDIT_DIR),
        "--port",
        str(port),
    ]
    if open_report:
        command.append("--open")
    subprocess.run(command, cwd=ROOT, text=True)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    golden = validate_golden_audit(args.output_dir)
    doctor = run_install_doctor(args.install_dir)
    status = "pass" if golden["validation_status"] == "pass" and doctor["status"] in {"pass", "not_run"} else "fail"
    result = {
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "golden_audit": golden,
        "install_doctor": doctor,
        "next_commands": [
            "python3 scripts/run_full_audit.py [OWNED_SITE_URL] --output-dir reports/[site-slug]/latest --lang en",
            "python3 scripts/generate_owner_data_request.py --site [OWNED_SITE_URL] --output-dir reports/[site-slug]/latest/owner-data --language en",
            "python3 scripts/serve_report.py --dir examples/reference-audit --port 8766 --open",
        ],
    }
    output_path = args.output_dir / "demo-result.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    if not args.no_serve:
        serve_report(args.port, args.open)
    raise SystemExit(0 if status == "pass" else 1)


if __name__ == "__main__":
    main()
