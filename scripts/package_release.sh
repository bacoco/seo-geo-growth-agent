#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="seo-geo-growth-agent"
VERSION="$(python3 - <<'PY'
import json
from pathlib import Path
manifest = json.loads(Path('manifest.json').read_text(encoding='utf-8'))
print(manifest.get('version', 'dev'))
PY
)"
OUT_DIR="$ROOT/dist"
ARCHIVE="$OUT_DIR/${NAME}-${VERSION}.zip"

cd "$ROOT"
python3 scripts/validate_skill.py
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
zip -r "$ARCHIVE" \
  SKILL.md README.md CHANGELOG.md RELEASE_NOTES.md LICENSE manifest.json \
  references templates docs scripts .github .gitignore .gitattributes CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md \
  -x '*/__pycache__/*' '*.pyc' '.git/*' 'dist/*'

echo "Created $ARCHIVE"
