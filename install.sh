#!/usr/bin/env bash
# Installs the fb-* skills into ~/.claude/skills and the state templates into
# ~/.claude/facebook (existing files are never overwritten).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
STATE_DIR="${CLAUDE_FB_STATE_DIR:-$HOME/.claude/facebook}"

command -v python3 >/dev/null 2>&1 || { echo "python3 (3.8+) is required for lint.py and beats.py" >&2; exit 1; }

mkdir -p "$SKILLS_DIR" "$STATE_DIR"

for d in "$HERE"/skills/fb-*; do
  name="$(basename "$d")"
  rm -rf "$SKILLS_DIR/$name"
  cp -R "$d" "$SKILLS_DIR/$name"
  echo "installed skill: $name"
done

copy_if_absent() {
  local src="$1" dst="$2"
  if [ -e "$dst" ]; then echo "kept existing:   $dst"; else cp "$src" "$dst"; echo "created:         $dst"; fi
}
copy_if_absent "$HERE/templates/config.template.md" "$STATE_DIR/config.md"
copy_if_absent "$HERE/templates/voice.template.md"  "$STATE_DIR/voice.md"
copy_if_absent "$HERE/templates/log.template.md"    "$STATE_DIR/log.md"

echo
echo "Done. Next: restart Claude Code and run /fb-start"
