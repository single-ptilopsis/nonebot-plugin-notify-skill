# agent-executable installation guide

Use the packaged installer from the unpacked skill directory.

## Project-local install

Run this from the unpacked `opencode-wave-notifier/` directory while your shell is in the target repository root:

```bash
./install.sh
```

This installs:

- the skill into `./.claude/skills/opencode-wave-notifier/`
- the commands into `./.claude/commands/`

## User-level install

Run this from the unpacked `opencode-wave-notifier/` directory:

```bash
./install.sh --user
```

This installs:

- the skill into `~/.claude/skills/opencode-wave-notifier/`
- the commands into `~/.claude/commands/`

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
ls ./.claude/skills/opencode-wave-notifier/SKILL.md
ls ./.claude/commands/notify-done.md
ls ./.claude/commands/notify-wave.md
```

For a user-level install, replace `./.claude` with `~/.claude`.

## Notes for agents

- Run the installer from the unpacked skill directory.
- For project installs, set the current working directory to the target repository root before running `./install.sh`.
- The installer copies the packaged commands into a command loader directory because oh-my-opencode does not load slash commands from inside the skill directory itself.
- If `WEBHOOK_URL` or `BEARER_TOKEN` is missing, do not attempt notification until the environment is configured.
