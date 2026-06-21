#!/usr/bin/env python3
"""Generate an ARD/ai-catalog draft manifest for agentic resources."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_QUERIES = [
    "audit my website for SEO and AI search readiness",
    "generate an AI-readable /for-ai package for my site",
    "check whether my site can be cited safely by AI assistants",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publisher-domain", required=True, help="Authority domain for the urn:air publisher segment.")
    parser.add_argument("--display-name", required=True, help="Human-readable host/resource display name.")
    parser.add_argument("--resource-name", required=True, help="Short resource name, for example seo-geo-growth-agent.")
    parser.add_argument("--resource-url", required=True, help="URL where the resource can be retrieved.")
    parser.add_argument("--output", required=True, type=Path, help="Output ai-catalog.json path.")
    parser.add_argument("--description", default="SEO/GEO skill for evidence-led search and AI-answer readiness audits.")
    parser.add_argument("--version", default="")
    parser.add_argument("--query", action="append", default=[], help="Representative query; provide 2 to 5. Defaults are used if omitted.")
    return parser.parse_args()


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-").lower()
    return normalized or "resource"


def publisher(value: str) -> str:
    clean = value.replace("https://", "").replace("http://", "").strip().strip("/")
    clean = clean.split("/", 1)[0]
    if not re.match(r"^[a-zA-Z0-9.-]+$", clean):
        raise SystemExit("publisher domain must contain only letters, numbers, dots, and hyphens")
    return clean.lower()


def representative_queries(values: list[str]) -> list[str]:
    queries = [item.strip() for item in values if item and item.strip()] or DEFAULT_QUERIES
    if len(queries) < 2 or len(queries) > 5:
        raise SystemExit("representative queries must contain between 2 and 5 items")
    return queries


def catalog(args: argparse.Namespace) -> dict:
    publisher_domain = publisher(args.publisher_domain)
    resource_name = slug(args.resource_name)
    entry = {
        "identifier": f"urn:air:{publisher_domain}:skill:{resource_name}",
        "displayName": args.display_name,
        "type": "application/ai-skill+md",
        "url": args.resource_url,
        "description": args.description,
        "tags": ["seo", "geo", "ai-search", "skill"],
        "capabilities": ["SEOAudit", "GEOAudit", "ForAIPackage", "EvidenceEngine"],
        "representativeQueries": representative_queries(args.query),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "spec_status": "ARD v0.9 draft",
            "publication_path": "/.well-known/ai-catalog.json",
        },
    }
    if args.version:
        entry["version"] = args.version
    return {
        "specVersion": "1.0",
        "host": {
            "displayName": args.display_name,
            "identifier": f"https://{publisher_domain}",
            "documentationUrl": args.resource_url,
        },
        "entries": [entry],
    }


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalog(args), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
