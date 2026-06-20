#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-codex}"
SKILL_DIR_NAME="seo-geo-growth-agent"

usage() {
  echo "Usage: ./scripts/install.sh [codex|claude|/custom/path/seo-geo-growth-agent]" >&2
}

case "$TARGET" in
  codex)
    DEST="${CODEX_HOME:-$HOME/.codex}/skills/$SKILL_DIR_NAME"
    ;;
  claude)
    DEST="$HOME/.claude/skills/$SKILL_DIR_NAME"
    ;;
  /*|.*)
    DEST="$TARGET"
    ;;
  *)
    usage
    exit 2
    ;;
esac

DEST_BASE="$(basename "$DEST")"
DEST_PARENT="$(dirname "$DEST")"

if [[ "$DEST_BASE" != "$SKILL_DIR_NAME" ]]; then
  echo "Refusing custom destination: path must end with $SKILL_DIR_NAME" >&2
  usage
  exit 2
fi

mkdir -p "$DEST_PARENT"
DEST_PARENT_REAL="$(cd "$DEST_PARENT" && pwd -P)"

if [[ "$DEST_PARENT_REAL" == "/" ]]; then
  echo "Refusing to install directly under filesystem root" >&2
  exit 2
fi

DEST="$DEST_PARENT_REAL/$DEST_BASE"

if [[ "$DEST" == "$ROOT" ]]; then
  echo "Refusing to install over the source repository" >&2
  exit 2
fi

if [[ -e "$DEST" ]]; then
  BACKUP="$DEST.backup-$(date +%Y%m%d-%H%M%S)"
  if [[ -e "$BACKUP" ]]; then
    BACKUP="$BACKUP.$$"
  fi
  mv "$DEST" "$BACKUP"
  echo "Previous install moved to: $BACKUP"
fi

mkdir -p "$DEST"

cp "$ROOT/SKILL.md" "$DEST/"
cp "$ROOT/INSTALL_FOR_AGENTS.md" "$DEST/"
cp "$ROOT/LICENSE" "$DEST/"
cp "$ROOT/manifest.json" "$DEST/"
cp -R "$ROOT/references" "$DEST/"
cp -R "$ROOT/templates" "$DEST/"
cp -R "$ROOT/runbooks" "$DEST/"
cp -R "$ROOT/evals" "$DEST/"
mkdir -p "$DEST/scripts"
cp "$ROOT/scripts/generate_html_audit_report.py" "$DEST/scripts/"
cp "$ROOT/scripts/serve_report.py" "$DEST/scripts/"
cp "$ROOT/scripts/capture_site_screenshots.mjs" "$DEST/scripts/"
cp "$ROOT/scripts/skill_doctor.py" "$DEST/scripts/"

echo "Installed seo-geo-growth-agent skill to: $DEST"
echo "Restart your agent session if it does not auto-refresh installed skills."
