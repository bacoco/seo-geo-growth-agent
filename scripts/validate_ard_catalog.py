#!/usr/bin/env python3
"""Validate an ARD / ai-catalog JSON manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


IDENTIFIER_PATTERN = re.compile(r"^urn:air:[A-Za-z0-9.-]+(?::[A-Za-z0-9][A-Za-z0-9._-]*){2,}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Local ai-catalog.json path or http(s) URL.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation results.")
    return parser.parse_args()


def load_json(source: str) -> Any:
    if source.startswith(("http://", "https://")):
        request = Request(source, headers={"User-Agent": "seo-geo-growth-agent/1.2"})
        try:
            with urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ValueError(f"HTTP {exc.code} while fetching {source}") from exc
        except URLError as exc:
            raise ValueError(f"network error while fetching {source}: {exc.reason}") from exc
    path = Path(source)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_catalog(catalog: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(catalog, dict):
        return ["catalog root must be an object"]

    if catalog.get("specVersion") != "1.0":
        errors.append('specVersion must be "1.0"')

    host = catalog.get("host")
    if host is not None and not isinstance(host, dict):
        errors.append("host must be an object when supplied")

    entries = catalog.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries must be a non-empty array")
        return errors

    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue

        identifier = entry.get("identifier")
        if not _is_non_empty_string(identifier) or not IDENTIFIER_PATTERN.match(identifier):
            errors.append(f"{prefix}.identifier must match urn:air:<publisher>:<namespace>:<resource>")

        if not _is_non_empty_string(entry.get("type")):
            errors.append(f"{prefix}.type must be a non-empty string")

        has_url = "url" in entry and entry.get("url") not in (None, "")
        has_data = "data" in entry and entry.get("data") not in (None, "")
        if has_url == has_data:
            errors.append(f"{prefix} must contain exactly one of url or data")
        if has_url and not _is_non_empty_string(entry.get("url")):
            errors.append(f"{prefix}.url must be a non-empty string")

        queries = entry.get("representativeQueries")
        if queries is not None:
            if not isinstance(queries, list):
                errors.append(f"{prefix}.representativeQueries must be an array")
            else:
                if len(queries) < 2 or len(queries) > 5:
                    errors.append(f"{prefix}.representativeQueries must contain 2 to 5 items")
                for query_index, query in enumerate(queries):
                    if not _is_non_empty_string(query):
                        errors.append(f"{prefix}.representativeQueries[{query_index}] must be a non-empty string")

        trust_manifest = entry.get("trustManifest")
        if trust_manifest is not None:
            if not isinstance(trust_manifest, dict):
                errors.append(f"{prefix}.trustManifest must be an object")
            elif not trust_manifest.get("identity"):
                errors.append(f"{prefix}.trustManifest.identity is required when trustManifest is supplied")

    return errors


def main() -> None:
    args = parse_args()
    try:
        catalog = load_json(args.source)
    except ValueError as exc:
        if args.json:
            print(json.dumps({"status": "fail", "errors": [str(exc)]}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

    errors = validate_catalog(catalog)
    if args.json:
        print(json.dumps({"status": "pass" if not errors else "fail", "errors": errors}, indent=2))
    elif errors:
        print("ERROR: ARD catalog validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("OK: ARD catalog validation passed")
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
