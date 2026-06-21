#!/usr/bin/env python3
"""Run the SEO/GEO audit workflow end to end."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from seo_geo_audit import default_output_dir, normalize_url, site_slug, write_plan


ROOT = Path(__file__).resolve().parents[1]
AI_ENDPOINTS = {
    "llms_txt": "/llms.txt",
    "for_ai": "/for-ai",
    "for_ai_json": "/for-ai.json",
    "for_ai_txt": "/for-ai.txt",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Target URL to audit.")
    parser.add_argument("--output-dir", type=Path, help="Audit workspace directory.")
    parser.add_argument("--lang", default="en", help="Report language, for example en or fr.")
    parser.add_argument("--environment", choices=["preprod", "production", "unknown"], default="production")
    parser.add_argument("--audit-json", type=Path, help="Existing audit JSON to use as the analysis base.")
    parser.add_argument("--skip-browser", action="store_true", help="Skip screenshot/responsive browser capture.")
    parser.add_argument("--force-package", action="store_true", help="Generate the AI-layer package even if public checks do not prove missing files.")
    parser.add_argument("--no-serve", action="store_true", help="Do not start the local report server after generation.")
    parser.add_argument("--port", type=int, default=8766, help="Preferred local report server port.")
    parser.add_argument("--open", action="store_true", help="Open the served report in the system browser.")
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


def fetch_status(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "seo-geo-growth-agent/1.2"})
    try:
        with urlopen(request, timeout=10) as response:
            return {"url": url, "status_code": response.status, "present": 200 <= response.status < 400, "error": ""}
    except HTTPError as exc:
        return {"url": url, "status_code": exc.code, "present": False, "error": f"HTTP {exc.code}"}
    except URLError as exc:
        return {"url": url, "status_code": None, "present": False, "error": str(exc.reason)}


def ai_layer_state(target_url: str) -> tuple[dict[str, bool], list[dict[str, Any]]]:
    parsed = urlparse(target_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    checks: list[dict[str, Any]] = []
    current: dict[str, bool] = {}
    for key, path in AI_ENDPOINTS.items():
        url = urljoin(origin + "/", path.lstrip("/"))
        check = fetch_status(url)
        checks.append({"label": path, **check})
        current[key] = bool(check["present"])
    return current, checks


def endpoint_findings(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [check for check in checks if not check["present"]]
    if not missing:
        return []
    observed = [
        f"{check['label']} returned {check['status_code'] or check['error'] or 'unavailable'}"
        for check in missing
    ]
    return [
        {
            "priority": "P1",
            "title": "Missing AI-readable publication layer",
            "observed": observed,
            "inferred": [
                "Assistants have less explicit context for citation guidance, source limits, and do-not-extrapolate boundaries."
            ],
            "recommended": [
                "Review the generated AI-layer package, adapt it to owner-approved facts, and publish the selected files."
            ],
            "evidence": [{"label": check["label"], "url": check["url"], "status": str(check["status_code"])} for check in missing],
        }
    ]


def unavailable_responsive(skip_browser: bool) -> dict[str, Any]:
    reason = "Browser capture skipped by --skip-browser." if skip_browser else "Browser evidence unavailable."
    return {"method": "not_captured", "summary": {"status": "unavailable", "verdict": reason}, "viewports": []}


def draft_audit(
    target_url: str,
    output_dir: Path,
    language: str,
    environment: str,
    skip_browser: bool,
    ai_current: dict[str, bool],
    ai_checks: list[dict[str, Any]],
    base: dict[str, Any] | None = None,
) -> dict[str, Any]:
    base = dict(base or {})
    site = base.get("site") or site_slug(target_url)
    generated_at = base.get("generated_at") or datetime.now(timezone.utc).isoformat()
    findings = list(base.get("findings", [])) if isinstance(base.get("findings"), list) else []
    findings.extend(endpoint_findings(ai_checks))
    responsive = load_json(output_dir / "responsive-study.json", unavailable_responsive(skip_browser))
    visual_evidence = load_json(output_dir / "site-visual-evidence.json", [])
    evidence_engine = load_json(output_dir / "evidence-engine.json", {})
    ard_readiness = load_json(output_dir / "ard-readiness.json", {})
    screenshot_status = base.get("screenshot_status")
    if not visual_evidence:
        screenshot_status = screenshot_status or (
            "unavailable: browser capture skipped by --skip-browser" if skip_browser else "unavailable: no browser screenshot evidence was generated"
        )

    summary = base.get("summary") if isinstance(base.get("summary"), dict) else {}
    missing_ai = any(value is False for value in ai_current.values())
    summary = {
        "headline": summary.get("headline") or f"{site} needs owner-reviewed AI-readable publication files.",
        "status": summary.get("status") or ("partial" if missing_ai else "ok"),
        "biggest_blocker": summary.get("biggest_blocker") or ("Missing AI-readable files" if missing_ai else "No P0 blocker observed from public checks"),
        "fastest_win": summary.get("fastest_win") or ("Review and publish the generated AI-layer package" if missing_ai else "Validate owner data and monitor"),
        "data_confidence": summary.get("data_confidence") or "medium",
        "decision": summary.get("decision") or "Use generated files as owner-review drafts; do not treat unknown metrics as zero.",
    }

    audit = {
        **base,
        "site": site,
        "audited_url": target_url,
        "generated_at": generated_at,
        "environment": environment,
        "report_language": language,
        "summary": summary,
        "findings": findings,
        "sources": base.get("sources")
        if isinstance(base.get("sources"), list) and base.get("sources")
        else [{"label": "Audited page", "url": target_url}],
        "screenshot_status": screenshot_status,
        "site_visual_evidence": visual_evidence if isinstance(visual_evidence, list) else [],
        "responsive_study": responsive,
        "evidence_engine": evidence_engine if isinstance(evidence_engine, dict) else {},
        "ard_readiness": ard_readiness if isinstance(ard_readiness, dict) else {},
        "ai_layer_current_state": ai_current,
        "ai_layer_endpoint_checks": ai_checks,
        "public_measurements": base.get("public_measurements")
        if isinstance(base.get("public_measurements"), list)
        else [
            {
                "source": "Public HTTP checks",
                "access": "public",
                "metric": "AI-readable endpoint presence",
                "limit": "No visit counts, rankings, conversions, or AI citation metrics",
            }
        ],
    }
    return audit


def write_audit(path: Path, audit: dict[str, Any]) -> None:
    path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    target_url = normalize_url(args.url)
    output_dir = args.output_dir or default_output_dir(target_url)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_plan(target_url, output_dir, args.lang, args.environment, "full_audit")

    if not args.skip_browser:
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
    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_ard_readiness.py"),
            "--url",
            target_url,
            "--output",
            str(output_dir / "ard-readiness.json"),
        ],
        check=False,
    )

    ai_current, ai_checks = ai_layer_state(target_url)
    base = load_json(args.audit_json, {}) if args.audit_json else load_json(output_dir / "audit.json", {})
    audit_path = output_dir / "audit.json"
    write_audit(
        audit_path,
        draft_audit(target_url, output_dir, args.lang, args.environment, args.skip_browser, ai_current, ai_checks, base),
    )

    if args.force_package or any(value is False for value in ai_current.values()):
        run(
            [
                sys.executable,
                str(ROOT / "scripts" / "generate_ai_layer_package.py"),
                "--input",
                str(audit_path),
                "--output-dir",
                str(output_dir),
                "--update-audit",
            ]
        )

    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_html_audit_report.py"),
            "--input",
            str(audit_path),
            "--output-dir",
            str(output_dir),
        ]
    )
    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_audit_report.py"),
            "--report-dir",
            str(output_dir),
            "--output",
            str(output_dir / "report-validation.json"),
        ]
    )

    print(f"Report written to {output_dir / 'index.html'}")
    if not args.no_serve:
        command = [
            sys.executable,
            str(ROOT / "scripts" / "serve_report.py"),
            "--dir",
            str(output_dir),
            "--port",
            str(args.port),
        ]
        if args.open:
            command.append("--open")
        subprocess.run(command, cwd=ROOT, text=True)


if __name__ == "__main__":
    main()
