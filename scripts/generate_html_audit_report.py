#!/usr/bin/env python3
"""Generate a self-contained dynamic HTML report from SEO/GEO audit JSON."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SEO/GEO Audit Report</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #1d1d1f;
      --muted: #6e6e73;
      --line: #d2d2d7;
      --paper: #f5f5f7;
      --panel: #ffffff;
      --blue: #0057d9;
      --blue-soft: #edf4ff;
      --red: #b42318;
      --red-soft: #fff1f0;
      --amber: #a15c07;
      --amber-soft: #fff7e6;
      --green: #067647;
      --green-soft: #ecfdf3;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      overflow-x: hidden;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.5;
    }
    a { color: var(--blue); overflow-wrap: anywhere; text-underline-offset: 3px; }
    code {
      padding: 2px 5px;
      border-radius: 5px;
      background: #eef1f6;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: .92em;
      overflow-wrap: anywhere;
    }
    .wrap { width: calc(100% - 32px); max-width: 1120px; margin: 0 auto; }
    header { border-bottom: 1px solid var(--line); background: rgba(255, 255, 255, .92); }
    .hero { padding: 30px 0 24px; }
    .eyebrow {
      margin: 0 0 12px;
      color: var(--blue);
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0;
      text-transform: uppercase;
    }
    h1 {
      max-width: 760px;
      margin: 0;
      font-size: clamp(30px, 3.4vw, 44px);
      line-height: 1.06;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }
    .subtitle { max-width: 760px; margin: 12px 0 0; color: var(--muted); font-size: 17px; }
    .report-meta {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 18px;
    }
    main { padding: 28px 0 56px; }
    section { margin: 22px 0; }
    .grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
    .grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .panel, .metric, .finding, .visual-card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    .panel { padding: 22px; }
    .metric { padding: 16px; }
    .metric strong { display: block; margin-bottom: 6px; font-size: 21px; line-height: 1.12; }
    .metric span { color: var(--muted); font-size: 14px; }
    .score {
      display: flex;
      flex-direction: column;
      gap: 10px;
      min-height: 136px;
      padding: 16px;
    }
    .score strong { font-size: 34px; line-height: 1; }
    .score progress { width: 100%; height: 8px; accent-color: var(--blue); }
    h2 { margin: 0 0 14px; font-size: 22px; line-height: 1.2; letter-spacing: 0; }
    h3 { margin: 0 0 8px; font-size: 18px; line-height: 1.3; letter-spacing: 0; }
    p { margin: 0 0 12px; overflow-wrap: anywhere; }
    ul, ol { margin: 10px 0 0; padding-left: 22px; }
    li { margin: 6px 0; overflow-wrap: anywhere; }
    .badge {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      line-height: 1;
      white-space: nowrap;
    }
    .p0, .missing { color: var(--red); background: var(--red-soft); }
    .p1, .partial { color: var(--amber); background: var(--amber-soft); }
    .p2, .ok { color: var(--green); background: var(--green-soft); }
    .finding { border-left: 4px solid var(--blue); padding: 16px 18px; margin: 12px 0; }
    .finding.p0-border { border-left-color: var(--red); }
    .finding.p1-border { border-left-color: var(--amber); }
    .finding.p2-border { border-left-color: var(--green); }
    .label {
      display: block;
      margin-top: 12px;
      color: #344054;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .toolbar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
      margin: 0 0 14px;
    }
    button {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: var(--ink);
      cursor: pointer;
      font: inherit;
      font-weight: 750;
      padding: 8px 12px;
    }
    button.active { color: #fff; background: var(--blue); border-color: var(--blue); }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; table-layout: fixed; }
    th, td { padding: 10px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; overflow-wrap: anywhere; }
    th { color: #344054; background: #f2f4f7; font-weight: 800; }
    .visual-card { overflow: hidden; }
    .visual-card img { display: block; width: 100%; height: auto; background: #f2f4f7; border-bottom: 1px solid var(--line); }
    .visual-card div { padding: 14px; }
    .screenshot-missing { padding: 18px; color: var(--muted); background: #f2f4f7; border-bottom: 1px solid var(--line); }
    .small { color: var(--muted); font-size: 13px; }
    .empty { color: var(--muted); font-style: italic; }
    @media (max-width: 820px) {
      .wrap { width: calc(100% - 28px); }
      .hero { padding: 34px 0 26px; }
      h1 { font-size: 27px; line-height: 1.08; }
      .subtitle { font-size: 16px; }
      .grid, .grid.two, .grid.four { grid-template-columns: 1fr; }
      th { display: none; }
      td { display: block; width: 100%; padding: 9px 0; }
      tr { display: block; padding: 10px 0; border-bottom: 1px solid var(--line); }
    }
  </style>
</head>
<body>
  <header>
    <div class="wrap hero">
      <p class="eyebrow" id="eyebrow"></p>
      <h1 id="headline"></h1>
      <p class="subtitle" id="subtitle"></p>
      <div class="report-meta" id="report-meta"></div>
    </div>
  </header>
  <main class="wrap" id="app"></main>
  <script id="audit-data" type="application/json">__AUDIT_JSON__</script>
  <script>
    const audit = JSON.parse(document.getElementById('audit-data').textContent);
    const app = document.getElementById('app');
    const priorityState = { value: 'all' };

    function text(value, fallback = '') {
      if (value === undefined || value === null || value === '') return fallback;
      return String(value);
    }

    function el(tag, attrs = {}, children = []) {
      const node = document.createElement(tag);
      for (const [key, value] of Object.entries(attrs)) {
        if (key === 'class') node.className = value;
        else if (key === 'text') node.textContent = value;
        else if (key === 'html') node.innerHTML = value;
        else if (key === 'href') {
          node.href = value;
          node.rel = 'noopener noreferrer';
        } else if (key === 'src') node.src = value;
        else if (value !== undefined && value !== null) node.setAttribute(key, value);
      }
      for (const child of children) {
        if (child === undefined || child === null) continue;
        node.append(child.nodeType ? child : document.createTextNode(String(child)));
      }
      return node;
    }

    function list(items) {
      const values = Array.isArray(items) ? items : (items ? [items] : []);
      if (!values.length) return el('p', { class: 'empty', text: 'No data provided.' });
      return el('ul', {}, values.map(item => el('li', { text: text(item) })));
    }

    function badge(value) {
      const normalized = text(value, 'unknown').toLowerCase();
      let klass = 'badge partial';
      if (['p0', 'error', 'missing', 'failed', 'critical'].includes(normalized)) klass = 'badge p0';
      if (['p1', 'warning', 'partial'].includes(normalized)) klass = 'badge p1';
      if (['p2', 'ok', 'pass', 'passed', 'good'].includes(normalized)) klass = 'badge p2';
      return el('span', { class: klass, text: text(value, 'unknown') });
    }

    function section(title, children, className = 'panel') {
      return el('section', { class: className }, [el('h2', { text: title }), ...children]);
    }

    function renderHeader() {
      const generated = text(audit.generated_at, new Date().toISOString());
      const site = text(audit.site, 'unknown site');
      document.title = `Audit SEO/GEO — ${site}`;
      document.getElementById('eyebrow').textContent = 'SEO + GEO audit';
      document.getElementById('headline').textContent = `Audit SEO/GEO — ${site}`;
      document.getElementById('subtitle').textContent = text(
        audit.summary?.headline,
        'Evidence-led audit report for search engines, AI answer engines, and browser agents.'
      );
      document.getElementById('report-meta').replaceChildren(
        badge(text(audit.summary?.status, 'unknown')),
        el('span', { class: 'badge partial', text: `Confidence: ${text(audit.summary?.data_confidence, 'unknown')}` }),
        el('span', { class: 'badge partial', text: generated })
      );
    }

    function renderMetrics() {
      const metrics = Array.isArray(audit.metrics) ? audit.metrics : [];
      const defaults = [
        { label: 'Status', value: text(audit.summary?.status, 'unknown'), detail: 'Overall readiness from supplied evidence.' },
        { label: 'Biggest blocker', value: text(audit.summary?.biggest_blocker, 'unknown'), detail: 'Highest-impact issue found.' },
        { label: 'Fastest win', value: text(audit.summary?.fastest_win, 'unknown'), detail: 'Best next action.' }
      ];
      return el('section', { class: 'grid' }, (metrics.length ? metrics : defaults).map(metric =>
        el('div', { class: 'metric' }, [
          el('strong', { text: text(metric.value, 'unknown') }),
          el('span', { text: text(metric.label, '') }),
          metric.detail ? el('p', { class: 'small', text: metric.detail }) : null
        ])
      ));
    }

    function renderDecision() {
      return section('Decision', [
        el('p', { text: text(audit.summary?.decision, audit.summary?.headline || 'Prioritize evidence-led fixes before content scale.') }),
        el('p', { class: 'small', text: `Data confidence: ${text(audit.summary?.data_confidence, 'unknown')}. Missing analytics or logs must remain unknown.` })
      ]);
    }

    function renderScorecards() {
      const scorecards = Array.isArray(audit.scorecards) ? audit.scorecards : [];
      if (!scorecards.length) return null;
      return section('Readiness scores', [
        el('div', { class: 'grid four' }, scorecards.map(scorecard => {
          const score = Number(scorecard.score ?? 0);
          const max = Number(scorecard.max ?? 10) || 10;
          const clamped = Math.max(0, Math.min(score, max));
          return el('article', { class: 'metric score' }, [
            el('span', { text: text(scorecard.label, 'Score') }),
            el('strong', { text: `${clamped}/${max}` }),
            el('progress', { value: clamped, max }),
            el('p', { class: 'small', text: text(scorecard.note, '') })
          ]);
        }))
      ]);
    }

    function evidenceTable(items) {
      const values = Array.isArray(items) ? items : [];
      if (!values.length) return el('p', { class: 'empty', text: 'No evidence links provided.' });
      const rows = values.map(item => el('tr', {}, [
        el('td', {}, [text(item.label, 'Evidence')]),
        el('td', {}, item.url ? [el('a', { href: item.url, text: item.url })] : [text(item.path || item.value || '')]),
        el('td', {}, [item.status ? badge(item.status) : text(item.note || '')])
      ]));
      return el('table', {}, [
        el('thead', {}, [el('tr', {}, [el('th', { text: 'Label' }), el('th', { text: 'Source' }), el('th', { text: 'Status / note' })])]),
        el('tbody', {}, rows)
      ]);
    }

    function renderFindings() {
      const findings = Array.isArray(audit.findings) ? audit.findings : [];
      const buttons = ['all', 'P0', 'P1', 'P2'].map(value => {
        const button = el('button', { text: value === 'all' ? 'All priorities' : value });
        button.classList.toggle('active', priorityState.value === value);
        button.addEventListener('click', () => {
          priorityState.value = value;
          render();
        });
        return button;
      });
      const filtered = findings.filter(f => priorityState.value === 'all' || text(f.priority).toUpperCase() === priorityState.value);
      return el('section', {}, [
        el('div', { class: 'toolbar' }, [el('h2', { text: 'Priority findings' }), ...buttons]),
        ...(filtered.length ? filtered.map(finding => {
          const priority = text(finding.priority, 'P1').toUpperCase();
          return el('article', { class: `finding ${priority.toLowerCase()}-border` }, [
            el('h3', {}, [badge(priority), ' ', text(finding.title, 'Untitled finding')]),
            el('span', { class: 'label', text: 'Observed' }),
            list(finding.observed),
            el('span', { class: 'label', text: 'Inferred' }),
            list(finding.inferred),
            el('span', { class: 'label', text: 'Recommended' }),
            list(finding.recommended),
            finding.evidence ? el('details', {}, [el('summary', { text: 'Evidence' }), evidenceTable(finding.evidence)]) : null
          ]);
        }) : [el('p', { class: 'empty', text: 'No findings match this filter.' })])
      ]);
    }

    function renderVisualEvidence() {
      const visuals = Array.isArray(audit.visual_evidence) ? audit.visual_evidence : [];
      if (!visuals.length) return section('Visual evidence', [el('p', { class: 'empty', text: 'No screenshots supplied.' })]);
      return section('Visual evidence', [
        el('div', { class: 'grid two' }, visuals.map(item =>
          {
            const image = item.path ? el('img', { src: item.path, alt: text(item.label, 'Screenshot') }) : null;
            if (image) {
              image.addEventListener('error', () => {
                image.replaceWith(el('div', { class: 'screenshot-missing', text: `Screenshot file: ${item.path}` }));
              });
            }
            return el('article', { class: 'visual-card' }, [
              image,
            el('div', {}, [
              el('h3', { text: text(item.label, 'Screenshot') }),
              el('p', { class: 'small', text: `Viewport: ${text(item.viewport, 'unknown')}` }),
              list(item.notes)
            ])
            ]);
          }
        ))
      ], 'panel');
    }

    function renderActionPlan() {
      const actions = Array.isArray(audit.action_plan) ? audit.action_plan : [];
      if (!actions.length) return section('Action plan', [el('p', { class: 'empty', text: 'No action plan supplied.' })]);
      const rows = actions.map(item => el('tr', {}, [
        el('td', { text: text(item.when || item.day || item.priority, '') }),
        el('td', { text: text(item.action, '') }),
        el('td', { text: text(item.outcome || item.metric, '') })
      ]));
      return section('Action plan', [
        el('table', {}, [
          el('thead', {}, [el('tr', {}, [el('th', { text: 'When' }), el('th', { text: 'Action' }), el('th', { text: 'Expected evidence' })])]),
          el('tbody', {}, rows)
        ])
      ]);
    }

    function renderPublicMeasurements() {
      const measurements = Array.isArray(audit.public_measurements) ? audit.public_measurements : [];
      if (!measurements.length) return section('Public measurements', [
        el('p', { class: 'empty', text: 'No public measurement checks supplied.' })
      ]);
      const rows = measurements.map(item => el('tr', {}, [
        el('td', { text: text(item.source, '') }),
        el('td', {}, [badge(text(item.access, 'unknown'))]),
        el('td', { text: text(item.metric, '') }),
        el('td', { text: text(item.limit, '') })
      ]));
      return section('Public measurements', [
        el('table', {}, [
          el('thead', {}, [el('tr', {}, [
            el('th', { text: 'Source' }),
            el('th', { text: 'Access' }),
            el('th', { text: 'Metric' }),
            el('th', { text: 'Limit' })
          ])]),
          el('tbody', {}, rows)
        ])
      ]);
    }

    function renderSources() {
      const sources = Array.isArray(audit.sources) ? audit.sources : [];
      return section('Sources consulted', [
        sources.length ? el('ul', {}, sources.map(source =>
          el('li', {}, [source.url ? el('a', { href: source.url, text: text(source.label, source.url) }) : text(source.label || source)])
        )) : el('p', { class: 'empty', text: 'No source list supplied.' })
      ]);
    }

    function render() {
      app.replaceChildren(...[
        renderMetrics(),
        renderScorecards(),
        renderDecision(),
        renderFindings(),
        renderVisualEvidence(),
        renderPublicMeasurements(),
        renderActionPlan(),
        renderSources()
      ].filter(Boolean));
    }

    renderHeader();
    render();
  </script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Path to audit JSON.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for index.html and audit.json.")
    return parser.parse_args()


def load_audit(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit("Audit JSON must be an object.")
    data.setdefault("generated_at", datetime.now(timezone.utc).isoformat())
    data.setdefault("summary", {})
    data.setdefault("findings", [])
    data.setdefault("sources", [])
    return data


def safe_json_for_script(data: dict) -> str:
    raw = json.dumps(data, ensure_ascii=False, indent=2)
    return raw.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def main() -> None:
    args = parse_args()
    audit = load_audit(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    copied_audit = args.output_dir / "audit.json"
    copied_audit.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    html = HTML_TEMPLATE.replace("__AUDIT_JSON__", safe_json_for_script(audit))
    html_path = args.output_dir / "index.html"
    html_path.write_text(html, encoding="utf-8")

    for visual in audit.get("visual_evidence", []):
      source_path = visual.get("source_path")
      report_path = visual.get("path")
      if source_path and report_path:
          source = Path(source_path)
          destination = args.output_dir / report_path
          destination.parent.mkdir(parents=True, exist_ok=True)
          if source.is_file() and source.resolve() != destination.resolve():
              shutil.copy2(source, destination)

    print(f"Wrote {html_path}")


if __name__ == "__main__":
    main()
