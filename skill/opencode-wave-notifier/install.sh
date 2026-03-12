#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Install opencode-wave-notifier into oh-my-opencode / Claude-compatible directories.

Usage:
  ./install.sh            # install into project-local .claude/
  ./install.sh --project  # same as default
  ./install.sh --user     # install into ~/.claude/
  ./install.sh --help
EOF
}

MODE="project"
case "${1:-}" in
  ""|--project)
    MODE="project"
    ;;
  --user)
    MODE="user"
    ;;
  --help|-h)
    usage
    exit 0
    ;;
  *)
    echo "Unknown option: ${1}" >&2
    usage >&2
    exit 2
    ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="$(basename "$SCRIPT_DIR")"

if [[ "$MODE" == "project" ]]; then
  BASE_DIR="$(pwd)/.claude"
else
  BASE_DIR="$HOME/.claude"
fi

SKILLS_DIR="$BASE_DIR/skills"
COMMANDS_DIR="$BASE_DIR/commands"
TARGET_SKILL_DIR="$SKILLS_DIR/$SKILL_NAME"

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR"
rm -rf "$TARGET_SKILL_DIR"
mkdir -p "$TARGET_SKILL_DIR"

# Copy the full skill directory except transient artifacts.
rsync -a \
  --exclude '.git' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.DS_Store' \
  "$SCRIPT_DIR/" "$TARGET_SKILL_DIR/"

cp "$SCRIPT_DIR/commands/notify-done.md" "$COMMANDS_DIR/notify-done.md"
cp "$SCRIPT_DIR/commands/notify-wave.md" "$COMMANDS_DIR/notify-wave.md"

echo "Installed skill to: $TARGET_SKILL_DIR"
echo "Installed commands to: $COMMANDS_DIR"
echo "Available commands: /notify-done and /notify-wave"
