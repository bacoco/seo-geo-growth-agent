#!/usr/bin/env python3
"""Generate owner-data collection requests for SEO/GEO audits."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SOURCES = [
    {
        "source": "gsc",
        "label": "Google Search Console",
        "requested_export": "Performance export for the audited property covering queries, pages, countries, devices, CTR, clicks, impressions, and average position.",
        "why": "Search visibility, query fit, CTR, and page-level opportunities cannot be proven from public HTML alone.",
    },
    {
        "source": "ga4",
        "label": "GA4",
        "requested_export": "Landing page, source/medium, conversion, engagement, and AI-assistant referral reports for the same audit window.",
        "why": "Public tools cannot verify visits, conversions, or business impact.",
    },
    {
        "source": "bing_webmaster_tools",
        "label": "Bing Webmaster Tools",
        "requested_export": "Search performance, crawl/indexing issues, IndexNow status, and AI Performance data if available.",
        "why": "Bing/Copilot and IndexNow evidence requires owner access or explicit exports.",
    },
    {
        "source": "server_logs",
        "label": "server logs",
        "requested_export": "Bot/user-agent logs for Googlebot, Bingbot, OAI-SearchBot, GPTBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot, and Perplexity-User.",
        "why": "Crawler access, WAF blocks, and fetch behavior need log evidence.",
    },
    {
        "source": "cloudflare",
        "label": "Cloudflare Analytics",
        "requested_export": "Traffic, cache, WAF/firewall, bot, and response status analytics for audited URLs.",
        "why": "Cache/CDN behavior and blocked crawlers should be verified by owner-side telemetry, not bypass attempts.",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", required=True, help="Domain or URL being audited.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for owner-data request files.")
    parser.add_argument("--language", default="en", choices=["en", "fr"], help="Output language.")
    return parser.parse_args()


def clean_site(site: str) -> str:
    return site.replace("https://", "").replace("http://", "").strip("/")


def markdown(site: str, language: str) -> str:
    if language == "fr":
        intro = (
            f"# Demande de données propriétaire - {site}\n\n"
            "Ces données servent à distinguer ce qui est observable publiquement de ce qui nécessite un accès propriétaire. "
            "Ne pas utiliser d’outil payant ou crédité sans validation explicite.\n"
        )
        paid = "## Consentement outils payants\n\nPar défaut : demander avant d’utiliser Haloscan, Semrush, Ahrefs, DataForSEO, Similarweb, SerpApi ou tout outil consommant des crédits.\n"
        sections = ["## Données demandées", ""]
        for item in SOURCES:
            sections.extend(
                [
                    f"### {item['label']}",
                    f"- Export demandé : {item['requested_export']}",
                    f"- Utilité : {item['why']}",
                    "",
                ]
            )
        return intro + "\n".join(sections).rstrip() + "\n\n" + paid

    intro = (
        f"# Owner Data Request - {site}\n\n"
        "Use this request to separate public evidence from owner-only proof. "
        "Do not call paid or credit-based tools without explicit approval.\n"
    )
    paid = "## Paid Tool Consent\n\nDefault policy: ask before using Haloscan, Semrush, Ahrefs, DataForSEO, Similarweb, SerpApi, or any credit-consuming tool.\n"
    sections = ["## Requested Data", ""]
    for item in SOURCES:
        sections.extend(
            [
                f"### {item['label']}",
                f"- Requested export: {item['requested_export']}",
                f"- Why it matters: {item['why']}",
                "",
            ]
        )
    return intro + "\n".join(sections).rstrip() + "\n\n" + paid


def checklist(site: str, language: str) -> dict:
    return {
        "site": site,
        "language": language,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "requested_sources": SOURCES,
        "paid_tools": {
            "default_policy": "ask_before_use",
            "examples": ["Haloscan", "Semrush", "Ahrefs", "DataForSEO", "Similarweb", "SerpApi"],
        },
        "cloudflare_policy": "Use owner analytics, logs, cache headers, and WAF events. Do not bypass Cloudflare protections.",
    }


def main() -> None:
    args = parse_args()
    site = clean_site(args.site)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "owner-data-request.md").write_text(markdown(site, args.language), encoding="utf-8")
    (args.output_dir / "owner-data-checklist.json").write_text(
        json.dumps(checklist(site, args.language), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {args.output_dir / 'owner-data-request.md'}")
    print(f"Wrote {args.output_dir / 'owner-data-checklist.json'}")


if __name__ == "__main__":
    main()
