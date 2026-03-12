# agent installation guide for OpenCode and Claude

Use the packaged installer from the unpacked skill directory. The installer can now detect whether the current target is OpenCode or Claude and choose the matching install path automatically.

## Runtime detection rules for agents

Before installing, detect the active runtime in this order:

1. If `OPENCODE_CONFIG_DIR` is set, treat the target as OpenCode.
2. If the target repository contains `.opencode/` or `opencode.json`, treat it as OpenCode.
3. If the target repository contains `.claude/` or `CLAUDE.md`, treat it as Claude.
4. For user-level installs, if `~/.config/opencode/` exists, prefer OpenCode.
5. For user-level installs, if `~/.claude/` exists, use Claude.
6. If the path for the detected runtime is not documented here, use web search to find the official or highest-confidence install path before proceeding.

If detection is ambiguous, pass an explicit runtime flag to the installer.

Prefer official references first:

- OpenCode skills: `https://opencode.ai/docs/skills/`
- OpenCode commands: `https://opencode.ai/docs/commands/`
- Claude skills and command compatibility: `https://docs.claude.com/en/docs/claude-code/skills`

Good web search queries when local docs are incomplete:

- `OpenCode skills path SKILL.md`
- `OpenCode commands directory`
- `Claude Code skills path`
- `Claude Code .claude commands`

## Project-local install

Run this from the unpacked skill directory while your shell is in the target repository root.

```bash
./install.sh
```

This installs into one of these path sets:

- OpenCode: `./.opencode/skills/wave-notifier/` and `./.opencode/commands/`
- Claude: `./.claude/skills/wave-notifier/` and `./.claude/commands/`

To force a specific runtime:

```bash
./install.sh --opencode
./install.sh --claude
```

## User-level install

Run this from the unpacked skill directory:

```bash
./install.sh --user
```

This installs into one of these path sets:

- OpenCode: `~/.config/opencode/skills/wave-notifier/` and `~/.config/opencode/commands/`
- Claude: `~/.claude/skills/wave-notifier/` and `~/.claude/commands/`

If `OPENCODE_CONFIG_DIR` is set, treat `$OPENCODE_CONFIG_DIR/` as the OpenCode user-level base instead of `~/.config/opencode/`.

To force a specific runtime:

```bash
./install.sh --opencode --user
./install.sh --claude --user
```

## Required runtime environment

Before using `/notify-done`, `/notify-wave`, or the underlying skill, configure these environment variables in the current shell:

```bash
export WEBHOOK_URL="https://localhost:55003/notify"
export BEARER_TOKEN="your-token"
```

The skill now requires these values to come from the environment. Do not pass them as inline script arguments.

## Verification

After installation, verify the expected files exist:

```bash
ls ./.opencode/skills/wave-notifier/SKILL.md
ls ./.opencode/commands/notify-done.md
ls ./.opencode/commands/notify-wave.md
```

For Claude installs, replace `./.opencode` with `./.claude`. For user-level installs, replace the project-local base with either `~/.config/opencode`, `$OPENCODE_CONFIG_DIR`, or `~/.claude`.

## Notes for agents

- Run the installer from the unpacked skill directory.
- For project installs, set the current working directory to the target repository root before running `./install.sh`.
- The installer copies the packaged commands into a command loader directory because neither OpenCode nor Claude loads slash commands from inside the skill directory itself.
- If runtime detection fails, use web search against the official docs to confirm the current path and then re-run the installer with `--opencode` or `--claude`.
- If `WEBHOOK_URL` or `BEARER_TOKEN` is missing, do not attempt notification until the environment is configured.
