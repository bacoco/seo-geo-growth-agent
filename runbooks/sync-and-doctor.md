# Sync And Doctor

Use this after changing the source repository when the user has Codex and Claude skill copies installed.

## Command

From the source repository:

```bash
python3 scripts/sync_and_doctor.py --target all
```

Dry run:

```bash
python3 scripts/sync_and_doctor.py --target all --dry-run
```

The script installs the source package into the selected local skill folders and runs `scripts/skill_doctor.py` against each installed copy.

## Guardrail

Run this only from the source repository. Installed runtime copies do not include `scripts/install.sh`, so they are not the right place to synchronize other copies.
