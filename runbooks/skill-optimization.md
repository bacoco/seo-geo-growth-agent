# Skill Optimization Runbook

Use this when improving routing, prompts, or report quality after real SEO/GEO audit sessions.

## Inputs

- user prompt;
- selected mode;
- files generated;
- validation output;
- user feedback;
- missed triggers or wrong triggers;
- whether report output was useful.

## Loop

1. Add or update routing evals in `evals/routing-eval.jsonl`.
2. Add a small regression test for deterministic scripts.
3. Update only the narrowest instruction, template, or script needed.
4. Run:

```bash
python3 tests/test_visual_html_audit.py
python3 tests/test_skill_doctor.py
python3 scripts/validate_skill.py
git diff --check
```

5. Record a short note in the next changelog entry.

## Review Questions

- Did the skill choose the right mode?
- Did the output separate `Observed`, `Inferred`, and `Recommended`?
- Did it avoid inventing metrics?
- Did screenshots come from the audited site, and did Design Watch translate them into a scored verdict?
- Did the global report include clear analysis cohorts when several lenses were used?
- Did it produce files the next agent can reuse?
- Did the report help a human make decisions faster?
