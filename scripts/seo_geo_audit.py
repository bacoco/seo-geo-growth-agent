#!/usr/bin/env python3
"""Simple workspace CLI for SEO/GEO visual audits."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Target URL to audit.")
    parser.add_argument("--output-dir", type=Path, help="Audit workspace directory.")
    parser.add_argument("--lang", default="en", help="Report language, for example en or fr.")
    parser.add_argument("--environment", choices=["preprod", "production"], default="production")
    parser.add_argument("--plan-only", action="store_true", help="Only create the audit plan; do not launch browser capture.")
    parser.add_argument("--skip-browser", action="store_true", help="Create the workspace without browser capture.")
    return parser.parse_args()


def normalize_url(url: str) -> str:
    if url.startswith(("http://", "https://")):
        return url
    return f"https://{url}"


def site_slug(url: str) -> str:
    parsed = urlparse(normalize_url(url))
    host = parsed.netloc or parsed.path
    slug = re.sub(r"[^a-zA-Z0-9.-]+", "-", host).strip("-").lower()
    return slug or "site"


def default_output_dir(url: str) -> Path:
    return ROOT / "reports" / site_slug(url) / datetime.now(timezone.utc).strftime("%Y-%m-%d")


def command_strings(target_url: str, output_dir: Path, language: str) -> list[str]:
    screenshots = output_dir / "site-screenshots"
    return [
        f"node scripts/capture_site_screenshots.mjs --url {target_url} --output-dir {screenshots} --evidence-out {output_dir / 'site-visual-evidence.json'} --study-out {output_dir / 'responsive-study.json'} --evidence-engine-out {output_dir / 'evidence-engine.json'}",
        f"python3 scripts/generate_owner_data_request.py --site {target_url} --output-dir {output_dir / 'owner-data'} --language {language if language in ('en', 'fr') else 'en'}",
        f"python3 scripts/check_ard_readiness.py --url {target_url} --output {output_dir / 'ard-readiness.json'}",
        f"python3 scripts/generate_ai_layer_package.py --input {output_dir / 'audit.json'} --output-dir {output_dir} --update-audit",
        f"python3 scripts/generate_html_audit_report.py --input {output_dir / 'audit.json'} --output-dir {output_dir}",
        f"python3 scripts/serve_report.py --dir {output_dir} --port 8766 --open",
    ]


def write_plan(target_url: str, output_dir: Path, language: str, environment: str, mode: str) -> dict:
    plan = {
        "target_url": target_url,
        "site_slug": site_slug(target_url),
        "language": language,
        "environment": environment,
        "mode": mode,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "expected_outputs": [
            str(output_dir / "audit.json"),
            str(output_dir / "index.html"),
            str(output_dir / "LATEST-SEO-GEO-REPORT.md"),
            str(output_dir / "site-screenshots" / "desktop.png"),
            str(output_dir / "site-screenshots" / "mobile.png"),
            str(output_dir / "responsive-study.json"),
            str(output_dir / "evidence-engine.json"),
            str(output_dir / "owner-data" / "owner-data-request.md"),
        ],
        "next_commands": command_strings(target_url, output_dir, language),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return plan


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    args = parse_args()
    target_url = normalize_url(args.url)
    output_dir = args.output_dir or default_output_dir(target_url)
    mode = "plan_only" if args.plan_only else ("workspace_only" if args.skip_browser else "capture_started")
    plan = write_plan(target_url, output_dir, args.lang, args.environment, mode)
    print(f"Wrote {output_dir / 'audit-plan.json'}")
    if args.plan_only or args.skip_browser:
        print("Next commands:")
        for command in plan["next_commands"]:
            print(f"- {command}")
        return
    run(
        [
            "node",
            str(ROOT / "scripts" / "capture_site_screenshots.mjs"),
            "--url",
            target_url,
            "--output-dir",
            str(output_dir / "site-screenshots"),
            "--evidence-out",
            str(output_dir / "site-visual-evidence.json"),
            "--study-out",
            str(output_dir / "responsive-study.json"),
            "--evidence-engine-out",
            str(output_dir / "evidence-engine.json"),
        ]
    )
    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_owner_data_request.py"),
            "--site",
            target_url,
            "--output-dir",
            str(output_dir / "owner-data"),
            "--language",
            args.lang if args.lang in ("en", "fr") else "en",
        ]
    )


if __name__ == "__main__":
    main()
