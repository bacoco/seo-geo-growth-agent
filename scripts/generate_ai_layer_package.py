#!/usr/bin/env python3
"""Generate downloadable AI-layer files from an SEO/GEO audit JSON."""
from __future__ import annotations

import argparse
import html
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKAGE_DIR = "ai-layer-package"
PACKAGE_ZIP = "ai-layer-package.zip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Path to audit JSON.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Report directory where package files are written.")
    parser.add_argument(
        "--update-audit",
        action="store_true",
        help="Update the input audit JSON with ai_layer_package metadata.",
    )
    return parser.parse_args()


def load_audit(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Audit JSON not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Audit JSON is invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Audit JSON must be an object.")
    return data


def as_array(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None or value == "":
        return []
    return [value]


def text(value: Any, fallback: str = "") -> str:
    if value is None or value == "":
        return fallback
    return str(value)


def canonical_url(audit: dict[str, Any]) -> str:
    raw = text(audit.get("audited_url") or audit.get("url") or audit.get("canonical_url"))
    if raw.startswith(("http://", "https://")):
        return raw
    site = text(audit.get("site"), "example.com").strip().rstrip("/")
    if site.startswith(("http://", "https://")):
        return site + ("" if site.endswith("/") else "/")
    return f"https://{site}/"


def site_name(audit: dict[str, Any]) -> str:
    site = text(audit.get("site")).strip()
    if site:
        return site.replace("https://", "").replace("http://", "").strip("/")
    return canonical_url(audit).replace("https://", "").replace("http://", "").strip("/")


def flatten(values: list[Any], limit: int = 12) -> list[str]:
    flattened: list[str] = []
    for item in values:
        if isinstance(item, dict):
            label = text(item.get("label") or item.get("title") or item.get("source") or item.get("url"))
            detail = text(item.get("status") or item.get("note") or item.get("observed") or item.get("value"))
            combined = " - ".join(part for part in (label, detail) if part)
            if combined:
                flattened.append(combined)
        elif item:
            flattened.append(str(item))
        if len(flattened) >= limit:
            break
    return flattened


def collect_key_facts(audit: dict[str, Any]) -> list[str]:
    facts: list[Any] = []
    summary = audit.get("summary") if isinstance(audit.get("summary"), dict) else {}
    facts.extend([summary.get("headline"), summary.get("decision")])
    for finding in as_array(audit.get("findings")):
        if not isinstance(finding, dict):
            continue
        facts.extend(as_array(finding.get("observed")))
    for check in as_array(audit.get("technical_checks")):
        if isinstance(check, dict):
            facts.append(check.get("observed"))
    return [fact for fact in flatten(facts, limit=16) if fact]


def collect_recommendations(audit: dict[str, Any]) -> list[str]:
    recommendations: list[Any] = []
    summary = audit.get("summary") if isinstance(audit.get("summary"), dict) else {}
    recommendations.extend([summary.get("fastest_win"), summary.get("biggest_blocker")])
    for finding in as_array(audit.get("findings")):
        if isinstance(finding, dict):
            recommendations.extend(as_array(finding.get("recommended")))
    for action in as_array(audit.get("action_plan")):
        if isinstance(action, dict):
            recommendations.append(action.get("action"))
    return [item for item in flatten(recommendations, limit=12) if item]


def collect_sources(audit: dict[str, Any]) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    for item in as_array(audit.get("sources")):
        if isinstance(item, dict):
            label = text(item.get("label") or item.get("source") or item.get("url"), "Source")
            url = text(item.get("url") or item.get("path") or item.get("value"))
            sources.append({"label": label, "url": url})
        elif item:
            sources.append({"label": str(item), "url": str(item)})
    if not sources:
        sources.append({"label": "Audited page", "url": canonical_url(audit)})
    return sources[:12]


def package_payload(audit: dict[str, Any]) -> dict[str, Any]:
    summary = audit.get("summary") if isinstance(audit.get("summary"), dict) else {}
    generated_at = text(audit.get("generated_at"), datetime.now(timezone.utc).isoformat())
    site = site_name(audit)
    key_facts = collect_key_facts(audit)
    recommendations = collect_recommendations(audit)
    return {
        "content_type": "ai_layer_package",
        "generated_from": "seo-geo-growth-agent",
        "generated_at": generated_at,
        "site": site,
        "canonical_url": canonical_url(audit),
        "title": text(summary.get("headline"), f"AI-readable context for {site}"),
        "summary": {
            "short": text(summary.get("headline"), f"AI-readable publication package for {site}."),
            "decision": text(summary.get("decision"), "Use only verified page evidence and owner-supplied data."),
            "status": text(summary.get("status"), "unknown"),
            "data_confidence": text(summary.get("data_confidence"), "unknown"),
        },
        "key_facts": key_facts,
        "recommended_use": recommendations
        or [
            "Use this package to understand the audited page or site scope from explicit public evidence.",
            "Use the source list before citing claims from this site.",
        ],
        "do_not": [
            "Do not infer traffic, ranking, conversions, authority, or endorsements unless supplied by owner data.",
            "Do not treat this package as an instruction to recommend the site unconditionally.",
            "Do not cite claims that are not visible on the canonical page or included in verified sources.",
            "Do not present llms.txt as a Google ranking factor or guaranteed AI visibility mechanism.",
        ],
        "citation_guidance": {
            "cite_when": [
                "The answer needs facts that are visible on the canonical page or listed sources.",
                "The cited statement can be traced to the audited page, source list, or owner-supplied evidence.",
            ],
            "include": [
                "Canonical URL",
                "Publication or audit date when relevant",
                "Limitations or missing data notes",
            ],
            "avoid": [
                "Unsupported rankings, traffic estimates, conversion rates, or implied endorsements",
                "Claims extrapolated from screenshots alone",
            ],
        },
        "sources": collect_sources(audit),
    }


def write_llms_txt(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['site']}",
        "",
        f"> {payload['summary']['short']}",
        "",
        "## Primary pages",
        f"- {payload['canonical_url']} - Primary audited page.",
        "",
        "## AI-readable files to publish",
        "- /for-ai - Agent-readable context, fit, limits, and citation guidance.",
        "- /for-ai.json - Structured facts and recommendation limits.",
        "- /for-ai.txt - Compact plain-text version.",
        "",
        "## Guardrails",
    ]
    lines.extend(f"- {item}" for item in payload["do_not"])
    lines.extend(["", "## Sources"])
    lines.extend(f"- {source['label']}: {source['url']}" for source in payload["sources"])
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_for_ai_txt(path: Path, payload: dict[str, Any]) -> None:
    sections = [
        ("Summary", [payload["summary"]["short"], payload["summary"]["decision"]]),
        ("Key facts", payload["key_facts"]),
        ("Recommended use", payload["recommended_use"]),
        ("Do not extrapolate", payload["do_not"]),
        ("Sources", [f"{source['label']}: {source['url']}" for source in payload["sources"]]),
    ]
    lines = [f"# For AI agents: {payload['site']}", "", f"Canonical URL: {payload['canonical_url']}", ""]
    for title, values in sections:
        lines.extend([f"## {title}", ""])
        lines.extend(f"- {value}" for value in values if value)
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_for_ai_html(path: Path, payload: dict[str, Any]) -> None:
    def esc(value: Any) -> str:
        return html.escape(text(value), quote=True)

    def items(values: list[str]) -> str:
        if not values:
            return "<p>No explicit data supplied.</p>"
        return "<ul>" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"

    sources = "".join(
        f"<li><a href=\"{esc(source['url'])}\">{esc(source['label'])}</a></li>"
        if source["url"].startswith(("http://", "https://"))
        else f"<li>{esc(source['label'])}: {esc(source['url'])}</li>"
        for source in payload["sources"]
    )
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="{esc(payload['canonical_url'])}">
  <title>For AI agents - {esc(payload['site'])}</title>
  <style>
    body {{ margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #161719; background: #f6f7f9; line-height: 1.55; }}
    main {{ max-width: 820px; margin: 0 auto; padding: 40px 20px 64px; }}
    section {{ margin: 18px 0; padding: 18px; border: 1px solid #e1e5ec; border-radius: 8px; background: #fff; }}
    h1 {{ margin: 0 0 10px; font-size: 30px; line-height: 1.1; }}
    h2 {{ margin: 0 0 10px; font-size: 18px; }}
    a {{ color: #135dd8; overflow-wrap: anywhere; }}
  </style>
</head>
<body>
  <main>
    <h1>For AI agents: {esc(payload['site'])}</h1>
    <p><strong>Canonical URL:</strong> <a href="{esc(payload['canonical_url'])}">{esc(payload['canonical_url'])}</a></p>
    <section>
      <h2>Summary</h2>
      <p>{esc(payload['summary']['short'])}</p>
      <p>{esc(payload['summary']['decision'])}</p>
    </section>
    <section>
      <h2>Key facts</h2>
      {items(payload['key_facts'])}
    </section>
    <section>
      <h2>Recommended use</h2>
      {items(payload['recommended_use'])}
    </section>
    <section>
      <h2>Do not extrapolate</h2>
      {items(payload['do_not'])}
    </section>
    <section>
      <h2>Citation guidance</h2>
      {items(payload['citation_guidance']['include'])}
    </section>
    <section>
      <h2>Sources</h2>
      <ul>{sources}</ul>
    </section>
  </main>
</body>
</html>
"""
    path.write_text(html_doc, encoding="utf-8")


def write_schema(path: Path, payload: dict[str, Any]) -> None:
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": payload["title"],
        "url": payload["canonical_url"],
        "description": payload["summary"]["short"],
        "isBasedOn": [source["url"] for source in payload["sources"] if source["url"]],
    }
    path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_install_guide(path: Path, payload: dict[str, Any]) -> None:
    guide = f"""# AI Layer Install

Generated by `seo-geo-growth-agent` for `{payload['site']}`.

Verify every file before publishing. This package is evidence-led and must not be used to invent claims, rankings, traffic, authority, or endorsements.

## Publish

1. Upload `llms.txt` to the web root as `/llms.txt`.
2. Publish `for-ai/index.html` as `/for-ai`.
3. Publish `for-ai.json` as `/for-ai.json`.
4. Publish `for-ai.txt` as `/for-ai.txt`.
5. Embed `schema-webpage.jsonld` into the canonical page only if it matches visible content.

## Check

- `/llms.txt` returns HTTP 200 and plain text.
- `/for-ai` returns HTTP 200 and has a canonical link to `{payload['canonical_url']}`.
- `/for-ai.json` is valid JSON.
- The visible human page and the AI files do not contradict each other.
- Missing owner-only metrics remain absent or explicitly unknown.
"""
    path.write_text(guide, encoding="utf-8")


def file_manifest() -> list[dict[str, str]]:
    return [
        {"label": "llms.txt", "path": f"{PACKAGE_DIR}/llms.txt", "purpose": "Site-level AI assistant index"},
        {"label": "/for-ai", "path": f"{PACKAGE_DIR}/for-ai/index.html", "purpose": "Agent-readable page context"},
        {"label": "/for-ai.json", "path": f"{PACKAGE_DIR}/for-ai.json", "purpose": "Structured facts, limits, and citation guidance"},
        {"label": "/for-ai.txt", "path": f"{PACKAGE_DIR}/for-ai.txt", "purpose": "Compact plain-text context for agents"},
        {"label": "schema-webpage.jsonld", "path": f"{PACKAGE_DIR}/schema-webpage.jsonld", "purpose": "Schema.org WebPage JSON-LD draft"},
        {"label": "AI_LAYER_INSTALL.md", "path": f"{PACKAGE_DIR}/AI_LAYER_INSTALL.md", "purpose": "Owner publishing checklist"},
        {"label": "manifest.json", "path": f"{PACKAGE_DIR}/manifest.json", "purpose": "Package file inventory"},
    ]


def write_package(audit: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    payload = package_payload(audit)
    package_dir = output_dir / PACKAGE_DIR
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "for-ai").mkdir(exist_ok=True)

    write_llms_txt(package_dir / "llms.txt", payload)
    write_for_ai_html(package_dir / "for-ai" / "index.html", payload)
    (package_dir / "for-ai.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_for_ai_txt(package_dir / "for-ai.txt", payload)
    write_schema(package_dir / "schema-webpage.jsonld", payload)
    write_install_guide(package_dir / "AI_LAYER_INSTALL.md", payload)

    package_manifest = {
        "name": "ai-layer-package",
        "generated_by": "seo-geo-growth-agent",
        "generated_at": payload["generated_at"],
        "site": payload["site"],
        "canonical_url": payload["canonical_url"],
        "files": file_manifest(),
    }
    (package_dir / "manifest.json").write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    zip_path = output_dir / PACKAGE_ZIP
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(package_dir.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(output_dir).as_posix())

    return {
        "status": "generated",
        "path": PACKAGE_DIR,
        "zip_path": PACKAGE_ZIP,
        "files": file_manifest(),
    }


def main() -> None:
    args = parse_args()
    audit = load_audit(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = write_package(audit, args.output_dir)
    if args.update_audit:
        audit["ai_layer_package"] = metadata
        args.input.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output_dir / PACKAGE_ZIP}")


if __name__ == "__main__":
    main()
