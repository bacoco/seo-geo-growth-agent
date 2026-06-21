#!/usr/bin/env python3
"""Compare two SEO/GEO audit JSON files and write narrative outputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, type=Path, help="Older audit JSON.")
    parser.add_argument("--after", required=True, type=Path, help="Newer audit JSON.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for audit-comparison outputs.")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing audit JSON: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Audit JSON must be an object: {path}")
    return data


def score_value(item: dict[str, Any]) -> float | None:
    raw = item.get("score")
    if isinstance(raw, (int, float)):
        return float(raw)
    if isinstance(raw, str):
        try:
            return float(raw.split("/", 1)[0].strip())
        except ValueError:
            return None
    return None


def score_map(audit: dict[str, Any]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for item in audit.get("scorecards", []):
        if not isinstance(item, dict):
            continue
        label = str(item.get("label") or "").strip()
        value = score_value(item)
        if label and value is not None:
            scores[label] = value
    return scores


def finding_identity(item: dict[str, Any], index: int) -> str:
    title = str(item.get("title") or "").strip()
    if title:
        return title
    priority = str(item.get("priority") or item.get("severity") or "").strip()
    evidence = str(item.get("evidence") or item.get("issue") or item.get("recommendation") or "").strip()
    if priority and evidence:
        return f"{priority}: {evidence}"
    if priority:
        return priority
    if evidence:
        return evidence
    return f"untitled finding #{index + 1}"


def finding_keys(findings: list[dict[str, Any]]) -> set[str]:
    return {finding_identity(item, index) for index, item in enumerate(findings)}


def compare(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_scores = score_map(before)
    after_scores = score_map(after)
    score_deltas = []
    for label in sorted(set(before_scores) | set(after_scores)):
        old = before_scores.get(label)
        new = after_scores.get(label)
        if old is None or new is None:
            continue
        score_deltas.append(
            {
                "label": label,
                "before": old,
                "after": new,
                "delta": round(new - old, 2),
            }
        )
    before_findings = [item for item in before.get("findings", []) if isinstance(item, dict)]
    after_findings = [item for item in after.get("findings", []) if isinstance(item, dict)]
    return {
        "site": after.get("site") or before.get("site") or "unknown",
        "before_generated_at": before.get("generated_at"),
        "after_generated_at": after.get("generated_at"),
        "before_status": (before.get("summary") or {}).get("status"),
        "after_status": (after.get("summary") or {}).get("status"),
        "score_deltas": score_deltas,
        "finding_delta": len(after_findings) - len(before_findings),
        "resolved_findings": sorted(finding_keys(before_findings) - finding_keys(after_findings)),
    }


def format_score(value: float) -> str:
    formatted = f"{value:.2f}".rstrip("0").rstrip(".")
    if "." not in formatted:
        formatted = f"{formatted}.0"
    return formatted


def markdown_report(data: dict[str, Any]) -> str:
    lines = [
        f"# SEO/GEO Audit Comparison - {data['site']}",
        "",
        "## Score changes",
        "",
    ]
    if data["score_deltas"]:
        for item in data["score_deltas"]:
            sign = "+" if item["delta"] >= 0 else ""
            lines.append(
                f"- {item['label']}: {sign}{format_score(item['delta'])} "
                f"({format_score(item['before'])} -> {format_score(item['after'])})"
            )
    else:
        lines.append("- No comparable scorecards supplied.")
    lines.extend(
        [
            "",
            "## Findings",
            "",
            f"- Finding count delta: {data['finding_delta']:+d}",
        ]
    )
    if data["resolved_findings"]:
        lines.append(f"- Resolved findings: {', '.join(data['resolved_findings'])}")
    lines.extend(
        [
            "",
            "## Narrative conclusion",
            "",
            narrative(data),
            "",
        ]
    )
    return "\n".join(lines)


def narrative(data: dict[str, Any]) -> str:
    positive = [item for item in data["score_deltas"] if item["delta"] > 0]
    negative = [item for item in data["score_deltas"] if item["delta"] < 0]
    if positive and not negative and data["finding_delta"] <= 0:
        return "The newer report is directionally better: scores improved and open findings did not increase. Keep the current fixes and focus on the next unresolved production gates."
    if negative:
        labels = ", ".join(item["label"] for item in negative)
        return f"The newer report regressed on {labels}. Review the underlying evidence before adding new recommendations."
    return "The two reports are broadly stable. Use the finding delta and evidence notes to decide the next action."


def main() -> None:
    args = parse_args()
    before = load_json(args.before)
    after = load_json(args.after)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    data = compare(before, after)
    (args.output_dir / "audit-comparison.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "audit-comparison.md").write_text(markdown_report(data), encoding="utf-8")
    print(f"Wrote {args.output_dir / 'audit-comparison.md'}")


if __name__ == "__main__":
    main()
