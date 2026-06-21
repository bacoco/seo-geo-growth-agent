#!/usr/bin/env python3
"""Check whether a site exposes ARD / ai-catalog discovery signals."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from validate_ard_catalog import validate_catalog


LINK_PATTERN = re.compile(r"<link\b[^>]*>", re.IGNORECASE)
ATTR_PATTERN = re.compile(r"([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(['\"])(.*?)\2", re.DOTALL)
AGENTMAP_PATTERN = re.compile(r"^\s*Agentmap:\s*(\S+)", re.IGNORECASE | re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Homepage or page URL to inspect.")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path for ard_readiness.")
    return parser.parse_args()


def normalize_url(url: str) -> str:
    if url.startswith(("http://", "https://")):
        return url
    return f"https://{url}"


def origin_for(url: str) -> str:
    parsed = urlparse(normalize_url(url))
    if not parsed.netloc:
        raise ValueError(f"invalid URL: {url}")
    return f"{parsed.scheme}://{parsed.netloc}"


def fetch(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "seo-geo-growth-agent/1.2"})
    try:
        with urlopen(request, timeout=10) as response:
            body = response.read()
            return {
                "status_code": response.status,
                "body": body.decode("utf-8", errors="replace"),
                "content_type": response.headers.get("content-type", ""),
                "error": "",
            }
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"status_code": exc.code, "body": body, "content_type": "", "error": f"HTTP {exc.code}"}
    except URLError as exc:
        return {"status_code": None, "body": "", "content_type": "", "error": str(exc.reason)}


def attrs(tag: str) -> dict[str, str]:
    return {match.group(1).lower(): match.group(3).strip() for match in ATTR_PATTERN.finditer(tag)}


def html_ai_catalog_link(html: str, base_url: str) -> str:
    for tag_match in LINK_PATTERN.finditer(html):
        values = attrs(tag_match.group(0))
        rel_values = {item.strip().lower() for item in values.get("rel", "").split()}
        if "ai-catalog" in rel_values and values.get("href"):
            return urljoin(base_url, values["href"])
    return ""


def robots_agentmap(robots_txt: str, base_url: str) -> str:
    match = AGENTMAP_PATTERN.search(robots_txt)
    if not match:
        return ""
    return urljoin(base_url + "/", match.group(1).strip())


def signal_status(url: str, response: dict[str, Any] | None = None) -> dict[str, str]:
    if not url:
        return {"status": "missing", "url": ""}
    if response is None:
        return {"status": "present", "url": url}
    if response.get("status_code") == 200:
        return {"status": "present", "url": url}
    if response.get("status_code") == 404:
        return {"status": "missing", "url": url}
    return {"status": "error", "url": url, "error": str(response.get("error") or response.get("status_code"))}


def build_readiness(url: str) -> dict[str, Any]:
    target_url = normalize_url(url)
    origin = origin_for(target_url)
    well_known_url = f"{origin}/.well-known/ai-catalog.json"
    robots_url = f"{origin}/robots.txt"

    homepage = fetch(target_url)
    well_known = fetch(well_known_url)
    robots = fetch(robots_url)

    link_url = html_ai_catalog_link(homepage["body"], target_url) if homepage.get("body") else ""
    agentmap_url = robots_agentmap(robots["body"], origin) if robots.get("body") else ""

    signals = {
        "well_known": signal_status(well_known_url, well_known),
        "html_link": signal_status(link_url),
        "robots_agentmap": signal_status(agentmap_url),
    }

    catalog_url = ""
    catalog_response = None
    if well_known.get("status_code") == 200:
        catalog_url = well_known_url
        catalog_response = well_known
    elif link_url:
        catalog_url = link_url
        catalog_response = fetch(link_url)
    elif agentmap_url:
        catalog_url = agentmap_url
        catalog_response = fetch(agentmap_url)

    validation = {"status": "not_checked", "errors": []}
    entries: list[Any] = []
    observed: list[str] = []
    recommended: list[str] = []

    if signals["well_known"]["status"] == "present":
        observed.append("ARD catalog is published at /.well-known/ai-catalog.json.")
    if signals["html_link"]["status"] == "present":
        observed.append("Homepage exposes a rel=ai-catalog discovery link.")
    if signals["robots_agentmap"]["status"] == "present":
        observed.append("robots.txt exposes an Agentmap discovery pointer.")

    status = "missing"
    if catalog_url and catalog_response:
        try:
            catalog = json.loads(catalog_response.get("body") or "{}")
        except json.JSONDecodeError as exc:
            validation = {"status": "fail", "errors": [f"catalog is invalid JSON: {exc}"]}
            status = "invalid"
        else:
            errors = validate_catalog(catalog)
            validation = {"status": "pass" if not errors else "fail", "errors": errors}
            entries = catalog.get("entries", []) if isinstance(catalog, dict) and not errors else []
            status = "present" if not errors else "invalid"
    else:
        observed.append("No ARD ai-catalog discovery signal was found.")
        recommended.append(
            "If the site exposes a skill, MCP server, A2A agent, or callable AI service, publish an owner-reviewed ai-catalog draft."
        )

    if validation["status"] == "fail":
        recommended.append("Fix the ARD catalog before using it as a discovery signal.")

    return {
        "status": status,
        "checked_url": target_url,
        "catalog_url": catalog_url or well_known_url,
        "signals": signals,
        "validation": validation,
        "entries": entries,
        "observed": observed,
        "recommended": recommended,
    }


def main() -> None:
    args = parse_args()
    try:
        readiness = build_readiness(args.url)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(readiness, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    raise SystemExit(0 if readiness["status"] in {"present", "missing"} else 1)


if __name__ == "__main__":
    main()
