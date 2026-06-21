#!/usr/bin/env python3
"""Generate a ready-not-executed GEO/Citation prompt panel CSV."""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


PROMPTS = [
    ("brand_discovery", "What is {site}, and what is it known for?"),
    ("category_discovery", "Which companies or websites should I compare when evaluating services like {site}?"),
    ("concept_explanation", "Explain the main topic covered by {site} and cite reliable sources."),
    ("project_discovery", "Find official information about projects, services, or content published by {site}."),
    ("booking_boundary", "Can I book, buy, subscribe, or contact {site}; what is the safest next step?"),
    ("source_integrity", "What facts about {site} can be cited safely, and which claims need verification?"),
]

FIELDNAMES = [
    "date",
    "target_domain",
    "engine",
    "prompt_family",
    "prompt",
    "brand_mentioned",
    "domain_cited",
    "cited_urls",
    "competitor_domains",
    "facts_reused",
    "errors_or_hallucinations",
    "result_status",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", required=True, help="Target domain or brand.")
    parser.add_argument("--output", required=True, type=Path, help="CSV output path.")
    return parser.parse_args()


def rows(site: str) -> list[dict[str, str]]:
    engines = ["ChatGPT", "Perplexity", "Claude"]
    output = []
    today = date.today().isoformat()
    clean_site = site.replace("https://", "").replace("http://", "").strip("/")
    for engine in engines:
        for family, prompt in PROMPTS:
            output.append(
                {
                    "date": today,
                    "target_domain": clean_site,
                    "engine": engine,
                    "prompt_family": family,
                    "prompt": prompt.format(site=clean_site),
                    "brand_mentioned": "",
                    "domain_cited": "",
                    "cited_urls": "",
                    "competitor_domains": "",
                    "facts_reused": "",
                    "errors_or_hallucinations": "",
                    "result_status": "ready_not_executed",
                    "notes": "Run manually or through an approved answer-engine measurement tool; do not treat blanks as zero visibility.",
                }
            )
    return output


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows(args.site))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
