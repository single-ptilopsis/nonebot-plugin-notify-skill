#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Install wave-notifier into OpenCode or Claude directories.

Usage:
  ./install.sh                     # auto-detect runtime, install project-local
  ./install.sh --project           # auto-detect runtime, install project-local
  ./install.sh --user              # auto-detect runtime, install user-level
  ./install.sh --opencode          # force OpenCode paths
  ./install.sh --claude            # force Claude paths
  ./install.sh --opencode --user   # force OpenCode user-level paths
  ./install.sh --claude --user     # force Claude user-level paths
  ./install.sh --help
EOF
}

MODE="project"
RUNTIME="auto"
DETECTION_REASON=""

while (($# > 0)); do
  case "$1" in
    --project)
      MODE="project"
      ;;
    --user)
      MODE="user"
      ;;
    --opencode)
      RUNTIME="opencode"
      ;;
    --claude)
      RUNTIME="claude"
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
  shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="wave-notifier"

detect_runtime() {
  if [[ "$RUNTIME" != "auto" ]]; then
    DETECTION_REASON="runtime forced by command-line flag"
    return
  fi

  if [[ -n "${OPENCODE_CONFIG_DIR:-}" ]]; then
    DETECTION_REASON="OPENCODE_CONFIG_DIR is set"
    RUNTIME="opencode"
    return
  fi

  if [[ -d "$(pwd)/.opencode" || -f "$(pwd)/opencode.json" ]]; then
    DETECTION_REASON="found OpenCode project markers (.opencode/ or opencode.json)"
    RUNTIME="opencode"
    return
  fi

  if [[ "$MODE" == "user" && -d "$HOME/.config/opencode" ]]; then
    DETECTION_REASON="found user-level OpenCode config directory"
    RUNTIME="opencode"
    return
  fi

  if [[ -d "$(pwd)/.claude" || -f "$(pwd)/CLAUDE.md" ]]; then
    DETECTION_REASON="found Claude project markers (.claude/ or CLAUDE.md)"
    RUNTIME="claude"
    return
  fi

  if [[ "$MODE" == "user" && -d "$HOME/.claude" ]]; then
    DETECTION_REASON="found user-level Claude config directory"
    RUNTIME="claude"
    return
  fi

  echo "Could not detect whether to install for OpenCode or Claude from local markers." >&2
  echo "If the required path is not documented locally, use web search against the official OpenCode or Claude docs, then re-run with --opencode or --claude." >&2
  exit 1
}

detect_runtime

if [[ "$RUNTIME" == "opencode" ]]; then
  if [[ "$MODE" == "project" ]]; then
    BASE_DIR="$(pwd)/.opencode"
  elif [[ -n "${OPENCODE_CONFIG_DIR:-}" ]]; then
    BASE_DIR="$OPENCODE_CONFIG_DIR"
  else
    BASE_DIR="$HOME/.config/opencode"
  fi
else
  if [[ "$MODE" == "project" ]]; then
    BASE_DIR="$(pwd)/.claude"
  else
    BASE_DIR="$HOME/.claude"
  fi
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
echo "Detected runtime: $RUNTIME"
echo "Detection reason: $DETECTION_REASON"
echo "Available commands: /notify-done and /notify-wave"
