#!/usr/bin/env python3
"""Tests for visual HTML audit report tooling."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VisualHtmlAuditReportTest(unittest.TestCase):
    def test_generate_html_report_from_audit_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            audit_path = tmp_path / "audit.json"
            output_dir = tmp_path / "report"
            audit_path.write_text(
                json.dumps(
                    {
                        "site": "example.com",
                        "generated_at": "2026-06-20T18:00:00+02:00",
                        "summary": {
                            "headline": "Make example.com easier for agents to cite.",
                            "status": "partial",
                            "biggest_blocker": "No /llms.txt or /for-ai package",
                            "fastest_win": "Add structured summaries to key pages",
                            "data_confidence": "medium",
                            "decision": "Do not launch until owner evidence is reviewed.",
                        },
                        "executive_verdict": {
                            "status": "production_gated",
                            "can_launch": "no",
                            "launch_status": "not_ready",
                            "top_blocker": "No /llms.txt or /for-ai package",
                            "owner_decision_needed": "Approve AI publication policy.",
                            "evidence_confidence": "medium",
                        },
                        "human_review_required": [
                            {
                                "area": "AI publication policy",
                                "reason": "Generated files require owner approval.",
                                "decision": "Approve or adapt before publication.",
                            }
                        ],
                        "url_scope": {
                            "audited_url": "https://example.com/#page-1",
                            "canonical_without_fragment": "https://example.com/",
                            "fragment": "page-1",
                            "has_fragment": True,
                            "share_url_recommendation": "Use the fragment-free canonical URL for SEO, sharing, and production references.",
                        },
                        "metrics": [
                            {"label": "Crawl", "value": "OK", "detail": "Homepage returns 200"}
                        ],
                        "scorecards": [
                            {"label": "SEO", "score": 7, "max": 10, "note": "Crawlable but missing metadata"}
                        ],
                        "analysis_cohorts": [
                            {
                                "name": "Design Watch",
                                "score": "6/10",
                                "status": "partial",
                                "what_it_checks": "First impression, hierarchy, trust, and mobile readability",
                                "verdict": "Readable but visually under-positioned",
                                "evidence": "Desktop and mobile screenshots reviewed",
                                "next_action": "Replace generic imagery with topic-relevant editorial identity",
                            }
                        ],
                        "design_watch": {
                            "score": "6/10",
                            "verdict": "Clear content, weak first impression",
                            "summary": "The page is readable, but the visual identity does not match the expertise implied by the content.",
                            "confidence": "needs_human_review",
                            "limits": ["Screenshot review cannot confirm conversion intent alone."],
                            "first_impression_risk": "The first viewport does not prove the value proposition fast enough.",
                            "observed": ["Homepage screenshot is readable on mobile."],
                            "inferred": ["The site may lose trust before the article content is evaluated."],
                            "recommended": ["Replace generic visual assets with topic-relevant editorial identity."],
                        },
                        "findings": [
                            {
                                "priority": "P1",
                                "title": "Missing agent-readable package",
                                "observed": ["/llms.txt returns 404"],
                                "inferred": ["Agents must infer citation guidance"],
                                "recommended": ["Create /llms.txt and /for-ai pages"],
                                "evidence": [{"label": "llms.txt", "url": "https://example.com/llms.txt", "status": "404"}],
                            }
                        ],
                        "site_visual_evidence": [
                            {
                                "label": "Homepage mobile",
                                "path": "site-screenshots/mobile.png",
                                "viewport": "390x1400",
                                "notes": ["No horizontal overflow detected"],
                            }
                        ],
                        "responsive_study": {
                            "method": "Chrome DevTools fallback",
                            "summary": {
                                "status": "pass",
                                "verdict": "Homepage responds correctly on tested mobile and desktop viewports.",
                            },
                            "viewports": [
                                {
                                    "label": "Mobile",
                                    "viewport": "390x1400",
                                    "status": "pass",
                                    "issues": [],
                                    "metrics": {
                                        "title": "Example",
                                        "scrollWidth": 390,
                                        "documentHeight": 1400,
                                        "horizontalOverflow": False,
                                        "h1Text": ["Example"],
                                        "missingImages": 0,
                                        "imageLoadStates": {
                                            "loaded_initially": 8,
                                            "loaded_after_scroll": 26,
                                            "broken": 0,
                                            "still_deferred": 0,
                                            "initial_missing": 26,
                                            "missing_after_scroll": 0,
                                        },
                                    },
                                }
                            ],
                        },
                        "public_measurements": [
                            {
                                "source": "Chrome UX Report",
                                "access": "public",
                                "metric": "Core Web Vitals field data",
                                "limit": "No visit counts",
                            }
                        ],
                        "evidence_engine": {
                            "console_watch": {
                                "summary": {
                                    "total": 1,
                                    "errors": 1,
                                    "warnings": 0,
                                    "by_classification": {"first_party": 1},
                                },
                                "sample": [
                                    {
                                        "level": "error",
                                        "classification": "first_party",
                                        "text": "Fixture console error",
                                        "url": "https://example.com/app.js",
                                    }
                                ],
                            },
                            "network_watch": {
                                "summary": {
                                    "response_count": 12,
                                    "failed_requests": 1,
                                    "non_2xx_3xx": 1,
                                    "status_counts": {"200": 11, "404": 1},
                                },
                                "failed_sample": [
                                    {"type": "Image", "error_text": "net::ERR_ABORTED", "blocked_reason": ""}
                                ],
                            },
                            "cache_cdn_watch": {
                                "status": "headers_available",
                                "verdict": "Cache/CDN headers captured.",
                                "headers": {"cache-control": "max-age=3600", "cf-cache-status": "HIT"},
                            },
                            "design_watch_metrics": {
                                "desktop": {
                                    "cta_visible": True,
                                    "trust_signal_visible": True,
                                    "hero_height_ratio": 0.58,
                                    "next_section_visible": True,
                                }
                            },
                        },
                        "ard_readiness": {
                            "status": "draft_ready",
                            "catalog_url": "https://example.com/.well-known/ai-catalog.json",
                            "observed": ["No ai-catalog manifest is currently published."],
                            "recommended": ["Publish /.well-known/ai-catalog.json if the site exposes agentic resources."],
                            "entries": [
                                {
                                    "identifier": "urn:air:example.com:skill:seo-geo-growth-agent",
                                    "type": "application/ai-skill+md",
                                    "representativeQueries": ["audit my website for AI search", "generate a /for-ai package"],
                                }
                            ],
                        },
                        "ai_layer_package": {
                            "status": "generated",
                            "publication_status": "adapt_before_publish",
                            "status_reason": "Owner review required before publishing.",
                            "zip_path": "ai-layer-package.zip",
                            "files": [
                                {
                                    "label": "llms.txt",
                                    "path": "ai-layer-package/llms.txt",
                                    "purpose": "Site-level AI assistant index",
                                },
                                {
                                    "label": "/for-ai",
                                    "path": "ai-layer-package/for-ai/index.html",
                                    "purpose": "Agent-readable page context",
                                },
                            ],
                        },
                        "sources": [{"label": "Homepage", "url": "https://example.com/"}],
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_html_audit_report.py"),
                    "--input",
                    str(audit_path),
                    "--output-dir",
                    str(output_dir),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            html_path = output_dir / "index.html"
            copied_audit_path = output_dir / "audit.json"
            self.assertTrue(html_path.is_file())
            self.assertTrue(copied_audit_path.is_file())
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("Make example.com easier for agents to cite.", html)
            self.assertIn("Missing agent-readable package", html)
            self.assertIn("Design Watch", html)
            self.assertIn("Analysis cohorts", html)
            self.assertIn("tab-shell", html)
            self.assertIn("Readiness signal", html)
            self.assertIn("Executive Verdict", html)
            self.assertIn("Can launch?", html)
            self.assertIn("Human review required", html)
            self.assertIn("Approve AI publication policy.", html)
            self.assertIn("Canonical URL without fragment", html)
            self.assertIn("https://example.com/", html)
            self.assertIn("Visual judgment", html)
            self.assertIn("first viewport does not prove", html)
            self.assertIn("Readable but visually under-positioned", html)
            self.assertIn("Clear content, weak first impression", html)
            self.assertIn("site-screenshots/mobile.png", html)
            self.assertIn("Responsive study", html)
            self.assertIn("Homepage responds correctly", html)
            self.assertIn("Readiness scores", html)
            self.assertIn("Measurement access", html)
            self.assertIn("Chrome UX Report", html)
            self.assertIn("Evidence Engine", html)
            self.assertIn("Console Watch", html)
            self.assertIn("Cache/CDN Watch", html)
            self.assertIn("Fixture console error", html)
            self.assertIn("CTA visible", html)
            self.assertIn("ARD readiness", html)
            self.assertIn("ai-catalog", html)
            self.assertIn("AI layer package", html)
            self.assertIn("adapt_before_publish", html)
            self.assertIn("Owner review required before publishing.", html)
            self.assertIn("ai-layer-package.zip", html)
            self.assertIn("ai-layer-package/llms.txt", html)
            self.assertIn("Images loaded after scroll", html)
            self.assertIn("26", html)

    def test_serve_report_check_mode_validates_report_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "index.html").write_text("<!doctype html><title>Report</title>", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "serve_report.py"),
                    "--dir",
                    str(tmp_path),
                    "--check",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Report directory OK", result.stdout)

    def test_generate_html_report_uses_requested_language(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            audit_path = tmp_path / "audit.json"
            output_dir = tmp_path / "report"
            audit_path.write_text(
                json.dumps(
                    {
                        "site": "example.fr",
                        "report_language": "fr",
                        "summary": {
                            "headline": "Audit rédigé en français.",
                            "status": "partiel",
                            "data_confidence": "moyenne",
                        },
                        "analysis_cohorts": [
                            {
                                "name": "Design Watch",
                                "score": "6/10",
                                "status": "partiel",
                                "verdict": "Lisible mais perfectible",
                                "next_action": "Clarifier la première impression",
                            }
                        ],
                        "design_watch": {
                            "score": "6/10",
                            "verdict": "Première impression moyenne",
                            "summary": "La page est lisible.",
                        },
                        "responsive_study": {
                            "summary": {
                                "status": "pass",
                                "verdict": "La page d’accueil répond correctement en mobile et desktop.",
                            },
                            "viewports": [],
                        },
                        "findings": [],
                        "sources": [],
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_html_audit_report.py"),
                    "--input",
                    str(audit_path),
                    "--output-dir",
                    str(output_dir),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            html = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn('document.documentElement.lang = reportLanguage', html)
            self.assertIn("Synthèse exécutive", html)
            self.assertIn("Cohortes d’analyse", html)
            self.assertIn("Étude responsive", html)
            self.assertIn("Constats prioritaires", html)
            self.assertIn("Sources consultées", html)
            self.assertIn("Audit rédigé en français.", html)


if __name__ == "__main__":
    unittest.main()
