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
      --ink: #161719;
      --muted: #62666d;
      --faint: #8b9098;
      --line: #e1e5ec;
      --paper: #f6f7f9;
      --panel: #ffffff;
      --soft: #f0f3f7;
      --blue: #135dd8;
      --blue-soft: #edf4ff;
      --red: #b42318;
      --red-soft: #fff1f0;
      --amber: #a15c07;
      --amber-soft: #fff7e6;
      --green: #067647;
      --green-soft: #ecfdf3;
      --shadow: 0 1px 2px rgba(16, 24, 40, .06);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      overflow-x: hidden;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
      font-size: 14px;
      line-height: 1.48;
    }
    a { color: var(--blue); overflow-wrap: anywhere; text-underline-offset: 3px; }
    code {
      padding: 2px 5px;
      border-radius: 5px;
      background: var(--soft);
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: .92em;
      overflow-wrap: anywhere;
    }
    .wrap { width: calc(100% - 36px); max-width: 1180px; margin: 0 auto; }
    header {
      border-bottom: 1px solid var(--line);
      background: rgba(255, 255, 255, .96);
    }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 28px;
      align-items: end;
      padding: 26px 0 22px;
    }
    .eyebrow {
      margin: 0 0 8px;
      color: var(--blue);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0;
      text-transform: uppercase;
    }
    h1 {
      max-width: 780px;
      margin: 0;
      font-size: clamp(24px, 2.6vw, 34px);
      line-height: 1.08;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }
    .subtitle {
      max-width: 780px;
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 15px;
    }
    .meta-box {
      justify-self: end;
      width: 100%;
      padding: 13px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      box-shadow: var(--shadow);
    }
    .meta-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      padding: 6px 0;
      border-bottom: 1px solid #eef1f5;
    }
    .meta-row:last-child { border-bottom: 0; }
    .meta-row span:first-child { color: var(--faint); }
    main { padding: 22px 0 56px; }
    section { margin: 16px 0; }
    .panel, .metric, .finding, .visual-card, .score-card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }
    .panel { padding: 18px; }
    .grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
    .grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .grid.sidebar { grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); align-items: start; }
    .metric { padding: 14px; min-height: 92px; }
    .metric strong { display: block; margin-bottom: 5px; font-size: 19px; line-height: 1.12; }
    .metric span { color: var(--muted); font-size: 12px; font-weight: 750; text-transform: uppercase; }
    .metric p { margin-top: 7px; }
    .score-card { padding: 14px; }
    .score-top { display: flex; justify-content: space-between; align-items: center; gap: 10px; }
    .score-card strong { font-size: 24px; line-height: 1; }
    .score-card progress { width: 100%; height: 7px; margin: 10px 0 6px; accent-color: var(--blue); }
    h2 { margin: 0 0 12px; font-size: 18px; line-height: 1.2; letter-spacing: 0; }
    h3 { margin: 0 0 7px; font-size: 15px; line-height: 1.3; letter-spacing: 0; }
    p { margin: 0 0 10px; overflow-wrap: anywhere; }
    ul, ol { margin: 8px 0 0; padding-left: 20px; }
    li { margin: 5px 0; overflow-wrap: anywhere; }
    .badge {
      display: inline-flex;
      align-items: center;
      min-height: 22px;
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      line-height: 1;
      white-space: nowrap;
    }
    .p0, .missing, .critical, .failed, .error { color: var(--red); background: var(--red-soft); }
    .p1, .partial, .warning, .medium { color: var(--amber); background: var(--amber-soft); }
    .p2, .ok, .pass, .passed, .good, .public { color: var(--green); background: var(--green-soft); }
    .unknown, .owner_only, .private { color: #344054; background: var(--soft); }
    .finding {
      border-left: 4px solid var(--blue);
      padding: 14px 16px;
      margin: 10px 0;
    }
    .finding.p0-border { border-left-color: var(--red); }
    .finding.p1-border { border-left-color: var(--amber); }
    .finding.p2-border { border-left-color: var(--green); }
    .label {
      display: block;
      margin-top: 10px;
      color: #344054;
      font-size: 11px;
      font-weight: 850;
      text-transform: uppercase;
    }
    .toolbar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
      margin: 0 0 10px;
    }
    .toolbar h2 { margin: 0 8px 0 0; }
    button {
      border: 1px solid var(--line);
      border-radius: 7px;
      background: #fff;
      color: var(--ink);
      cursor: pointer;
      font: inherit;
      font-size: 13px;
      font-weight: 750;
      padding: 7px 10px;
    }
    button.active { color: #fff; background: var(--blue); border-color: var(--blue); }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; table-layout: fixed; }
    th, td { padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; overflow-wrap: anywhere; }
    th { color: #344054; background: var(--soft); font-weight: 850; }
    tr:last-child td { border-bottom: 0; }
    .verdict {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 12px;
      align-items: start;
    }
    .verdict-score {
      display: inline-flex;
      min-width: 68px;
      min-height: 68px;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      background: var(--blue-soft);
      color: var(--blue);
      font-size: 20px;
      font-weight: 850;
    }
    .visual-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }
    .visual-card { overflow: hidden; }
    .visual-card img {
      display: block;
      width: 100%;
      max-height: 460px;
      object-fit: cover;
      object-position: top center;
      background: var(--soft);
      border-bottom: 1px solid var(--line);
    }
    .visual-card div { padding: 12px; }
    .screenshot-missing { padding: 18px; color: var(--muted); background: var(--soft); border-bottom: 1px solid var(--line); }
    .small { color: var(--muted); font-size: 12px; }
    .empty { color: var(--muted); font-style: italic; }
    .callout {
      border-left: 4px solid var(--blue);
      background: #fbfdff;
      padding: 12px 14px;
      border-radius: 7px;
    }
    @media (max-width: 900px) {
      .hero, .grid, .grid.two, .grid.four, .grid.sidebar, .visual-grid { grid-template-columns: 1fr; }
      .meta-box { justify-self: stretch; }
    }
    @media (max-width: 640px) {
      .wrap { width: calc(100% - 28px); }
      .hero { padding: 22px 0 18px; }
      h1 { font-size: 24px; line-height: 1.1; }
      .subtitle { font-size: 14px; }
      .panel { padding: 15px; }
      th { display: none; }
      td { display: block; width: 100%; padding: 8px 0; }
      tr { display: block; padding: 9px 0; border-bottom: 1px solid var(--line); }
      .visual-card img { max-height: 360px; }
    }
  </style>
</head>
<body>
  <header>
    <div class="wrap hero">
      <div>
        <p class="eyebrow" id="eyebrow"></p>
        <h1 id="headline"></h1>
        <p class="subtitle" id="subtitle"></p>
      </div>
      <aside class="meta-box" id="report-meta"></aside>
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

    function asArray(value) {
      if (Array.isArray(value)) return value;
      if (value === undefined || value === null || value === '') return [];
      return [value];
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
      const values = asArray(items);
      if (!values.length) return el('p', { class: 'empty', text: 'No data provided.' });
      return el('ul', {}, values.map(item => el('li', { text: text(item) })));
    }

    function badge(value) {
      const normalized = text(value, 'unknown').toLowerCase().replaceAll(' ', '_');
      let klass = `badge ${normalized}`;
      if (['p0', 'error', 'missing', 'failed', 'critical'].includes(normalized)) klass = 'badge p0';
      if (['p1', 'warning', 'partial', 'medium'].includes(normalized)) klass = 'badge p1';
      if (['p2', 'ok', 'pass', 'passed', 'good', 'public'].includes(normalized)) klass = 'badge p2';
      if (['owner_only', 'owner_only_free', 'public_if_enough_traffic', 'public_partial', 'unknown'].includes(normalized)) klass = `badge ${normalized}`;
      return el('span', { class: klass, text: text(value, 'unknown') });
    }

    function section(title, children, className = 'panel') {
      return el('section', { class: className }, [el('h2', { text: title }), ...children]);
    }

    function metaRow(label, value) {
      return el('div', { class: 'meta-row' }, [el('span', { text: label }), el('strong', { text: text(value, 'unknown') })]);
    }

    function renderHeader() {
      const generated = text(audit.generated_at, new Date().toISOString());
      const site = text(audit.site, 'unknown site');
      document.title = `Audit SEO/GEO — ${site}`;
      document.getElementById('eyebrow').textContent = 'SEO/GEO audit';
      document.getElementById('headline').textContent = `Audit SEO/GEO — ${site}`;
      document.getElementById('subtitle').textContent = text(
        audit.summary?.headline,
        'Evidence-led audit for search engines, AI answer engines, and browser agents.'
      );
      document.getElementById('report-meta').replaceChildren(
        metaRow('Status', text(audit.summary?.status, 'unknown')),
        metaRow('Confidence', text(audit.summary?.data_confidence, 'unknown')),
        metaRow('Generated', generated)
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
          el('span', { text: text(metric.label, '') }),
          el('strong', { text: text(metric.value, 'unknown') }),
          metric.detail ? el('p', { class: 'small', text: metric.detail }) : null
        ])
      ));
    }

    function renderExecutiveBrief() {
      const brief = asArray(audit.executive_brief);
      return section('Executive brief', [
        el('p', { text: text(audit.summary?.decision, audit.summary?.headline || 'Prioritize evidence-led fixes before content scale.') }),
        brief.length ? el('div', { class: 'callout' }, [list(brief)]) : null,
        el('p', { class: 'small', text: `Missing analytics or logs are marked unknown. Data confidence: ${text(audit.summary?.data_confidence, 'unknown')}.` })
      ].filter(Boolean));
    }

    function renderScorecards() {
      const scorecards = Array.isArray(audit.scorecards) ? audit.scorecards : [];
      if (!scorecards.length) return null;
      return section('Readiness scores', [
        el('div', { class: 'grid four' }, scorecards.map(scorecard => {
          const score = Number(scorecard.score ?? 0);
          const max = Number(scorecard.max ?? 10) || 10;
          const clamped = Math.max(0, Math.min(score, max));
          return el('article', { class: 'score-card' }, [
            el('div', { class: 'score-top' }, [
              el('span', { class: 'small', text: text(scorecard.label, 'Score') }),
              el('strong', { text: `${clamped}/${max}` })
            ]),
            el('progress', { value: clamped, max }),
            el('p', { class: 'small', text: text(scorecard.note, '') })
          ]);
        }))
      ]);
    }

    function renderCohorts() {
      const cohorts = Array.isArray(audit.analysis_cohorts || audit.cohorts)
        ? (audit.analysis_cohorts || audit.cohorts)
        : [];
      if (!cohorts.length) return null;
      return section('Analysis cohorts', [
        el('table', {}, [
          el('thead', {}, [el('tr', {}, [
            el('th', { text: 'Cohort' }),
            el('th', { text: 'Score' }),
            el('th', { text: 'Verdict' }),
            el('th', { text: 'Next action' })
          ])]),
          el('tbody', {}, cohorts.map(item => el('tr', {}, [
            el('td', {}, [
              el('strong', { text: text(item.name, 'Cohort') }),
              item.status ? el('p', {}, [badge(item.status)]) : null,
              item.what_it_checks ? el('p', { class: 'small', text: text(item.what_it_checks) }) : null
            ]),
            el('td', { text: text(item.score, 'n/a') }),
            el('td', {}, [
              el('p', { text: text(item.verdict, '') }),
              item.evidence ? el('p', { class: 'small', text: text(item.evidence) }) : null
            ]),
            el('td', { text: text(item.next_action, '') })
          ])))
        ])
      ]);
    }

    function visualCards(items) {
      const visuals = Array.isArray(items) ? items : [];
      if (!visuals.length) return el('p', { class: 'empty', text: 'No site screenshots supplied.' });
      return el('div', { class: 'visual-grid' }, visuals.map(item => {
        const image = item.path ? el('img', { src: item.path, alt: text(item.label, 'Site screenshot') }) : null;
        if (image) {
          image.addEventListener('error', () => {
            image.replaceWith(el('div', { class: 'screenshot-missing', text: `Screenshot file: ${item.path}` }));
          });
        }
        return el('article', { class: 'visual-card' }, [
          image,
          el('div', {}, [
            el('h3', { text: text(item.label, 'Site screenshot') }),
            el('p', { class: 'small', text: `Viewport: ${text(item.viewport, 'unknown')}` }),
            list(item.notes)
          ])
        ]);
      }));
    }

    function renderFirstImpression() {
      const first = audit.design_watch || audit.first_impression || audit.visual_verdict || {};
      const visuals = audit.site_visual_evidence || audit.visual_evidence || [];
      if (!Object.keys(first).length && !visuals.length) return null;
      return section('Design Watch', [
        el('div', { class: 'grid sidebar' }, [
          el('article', { class: 'panel' }, [
            el('div', { class: 'verdict' }, [
              el('div', { class: 'verdict-score', text: text(first.score, 'n/a') }),
              el('div', {}, [
                el('h3', { text: text(first.verdict, 'Visual verdict unavailable') }),
                el('p', { text: text(first.summary, 'No visual analysis supplied.') }),
                first.confidence ? badge(`confidence: ${first.confidence}`) : null
              ])
            ]),
            el('span', { class: 'label', text: 'Observed from screenshots' }),
            list(first.observed),
            el('span', { class: 'label', text: 'Implication' }),
            list(first.inferred || first.implications),
            el('span', { class: 'label', text: 'Recommended' }),
            list(first.recommended)
          ]),
          visualCards(visuals)
        ])
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
        const button = el('button', { text: value === 'all' ? 'All' : value });
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

    function renderTechnicalSnapshot() {
      const checks = Array.isArray(audit.technical_checks) ? audit.technical_checks : [];
      if (!checks.length) return null;
      return section('Technical snapshot', [
        el('table', {}, [
          el('thead', {}, [el('tr', {}, [
            el('th', { text: 'Area' }),
            el('th', { text: 'Status' }),
            el('th', { text: 'Observed evidence' }),
            el('th', { text: 'Implication' })
          ])]),
          el('tbody', {}, checks.map(item => el('tr', {}, [
            el('td', { text: text(item.area, '') }),
            el('td', {}, [badge(text(item.status, 'unknown'))]),
            el('td', { text: text(item.observed, '') }),
            el('td', { text: text(item.implication, '') })
          ])))
        ])
      ]);
    }

    function renderPublicMeasurements() {
      const measurements = Array.isArray(audit.public_measurements) ? audit.public_measurements : [];
      if (!measurements.length) return section('Measurement access', [
        el('p', { class: 'empty', text: 'No measurement access checks supplied.' })
      ]);
      const rows = measurements.map(item => el('tr', {}, [
        el('td', { text: text(item.source, '') }),
        el('td', {}, [badge(text(item.access, 'unknown'))]),
        el('td', { text: text(item.metric, '') }),
        el('td', { text: text(item.limit, '') })
      ]));
      return section('Measurement access', [
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
        renderCohorts(),
        renderExecutiveBrief(),
        renderFirstImpression(),
        renderFindings(),
        renderTechnicalSnapshot(),
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


def copy_visual_sources(audit: dict, output_dir: Path) -> None:
    for key in ("site_visual_evidence", "visual_evidence"):
        for visual in audit.get(key, []):
            source_path = visual.get("source_path")
            report_path = visual.get("path")
            if not source_path or not report_path:
                continue
            source = Path(source_path)
            destination = output_dir / report_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_file() and source.resolve() != destination.resolve():
                shutil.copy2(source, destination)


def main() -> None:
    args = parse_args()
    audit = load_audit(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    copied_audit = args.output_dir / "audit.json"
    copied_audit.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    html = HTML_TEMPLATE.replace("__AUDIT_JSON__", safe_json_for_script(audit))
    html_path = args.output_dir / "index.html"
    html_path.write_text(html, encoding="utf-8")

    copy_visual_sources(audit, args.output_dir)

    print(f"Wrote {html_path}")


if __name__ == "__main__":
    main()
