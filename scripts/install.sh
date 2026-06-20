#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-codex}"

case "$TARGET" in
  codex)
    DEST="${CODEX_HOME:-$HOME/.codex}/skills/seo-geo-growth-agent"
    ;;
  claude)
    DEST="$HOME/.claude/skills/seo-geo-growth-agent"
    ;;
  /*|.*)
    DEST="$TARGET"
    ;;
  *)
    echo "Usage: ./scripts/install.sh [codex|claude|/custom/skill/path]" >&2
    exit 2
    ;;
esac

rm -rf "$DEST"
mkdir -p "$DEST"

cp "$ROOT/SKILL.md" "$DEST/"
cp "$ROOT/LICENSE" "$DEST/"
cp "$ROOT/manifest.json" "$DEST/"
cp -R "$ROOT/references" "$DEST/"
cp -R "$ROOT/templates" "$DEST/"

echo "Installed seo-geo-growth-agent skill to: $DEST"
echo "Restart your agent session if it does not auto-refresh installed skills."
