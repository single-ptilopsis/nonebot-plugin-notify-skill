# agent installation guide for OpenCode and Claude

If you are an LLM agent, read this file and follow it.

Your job is to install `wave-notifier` correctly, with the least necessary back-and-forth, and without overwriting an existing install unless the user explicitly approves it.

The installation is complete only when both of these are present under the chosen target base directory:

- `skills/wave-notifier/`
- `commands/notify-done.md` and `commands/notify-wave.md`

Prefer the packaged installer first. Fall back to manual copy only when the installer cannot be used.

## Agent quick start

1. Ask the minimum required questions.
2. Resolve the target base directory.
3. Prefer `skill/wave-notifier/install.sh`.
4. If that is not suitable, use the manual copy procedure in this document.
5. Verify the installed files exist.
6. Report the exact installed paths and remind the user to restart or reload the current session if needed.

## What agents should ask before installing

Ask only the minimum questions required to avoid installing into the wrong place.

### Required questions

1. Should this be installed for **OpenCode** or **Claude**?
2. Should this be installed **globally** or for the **current project**?
3. If the target already contains `wave-notifier` or the same command files, is the agent allowed to **overwrite** them?

### Ask only when needed

Ask these follow-up questions only if the current context is insufficient:

- **Project directory**: ask only when the user chose a project-local install but the current project root cannot be determined reliably.
- **Partial install preference**: ask only if the user explicitly says they may want to install only the skill or only the commands. Otherwise, install both by default.

### Do not ask by default

Do **not** block installation on runtime usage configuration such as:

- `WEBHOOK_URL`
- `BEARER_TOKEN`
- webhook endpoint reachability

Those belong to **using** the skill, not **installing** it.

Unless the user explicitly approved overwrite, do not remove or replace existing files.

## Target path mapping

### Project-local install

- OpenCode: `./.opencode/`
- Claude: `./.claude/`

### Global install

- OpenCode: `~/.config/opencode/`
- Claude: `~/.claude/`

If `OPENCODE_CONFIG_DIR` is set for a global OpenCode install, use `$OPENCODE_CONFIG_DIR/` as the base directory.

## Preferred method: packaged installer

Run from the unpacked skill directory:

```bash
./install.sh --help
```

Common commands:

```bash
./install.sh --project
./install.sh --user
./install.sh --opencode --project
./install.sh --opencode --user
./install.sh --claude --project
./install.sh --claude --user
```

Behavior:

- installs `skills/wave-notifier/`
- installs `commands/notify-done.md`
- installs `commands/notify-wave.md`
- auto-detects OpenCode vs Claude when possible

Recommended choices:

- project-local install: `./install.sh --project`
- global install: `./install.sh --user`
- explicit OpenCode target: add `--opencode`
- explicit Claude target: add `--claude`

## Runtime detection rules

When the runtime was not explicitly chosen by the user, detect it in this order:

1. If `OPENCODE_CONFIG_DIR` is set, treat the target as OpenCode.
2. If the target repository contains `.opencode/` or `opencode.json`, treat it as OpenCode.
3. If this is a global install and `~/.config/opencode/` exists, prefer OpenCode.
4. If the target repository contains `.claude/` or `CLAUDE.md`, treat it as Claude.
5. If this is a global install and `~/.claude/` exists, use Claude.

If detection is still ambiguous, ask the user instead of guessing.

## How to speak to the user

Keep the install conversation short.

Ask the minimum required questions in one message when possible. For example:

```text
Before I install it, please confirm three things:
1. Install for OpenCode or Claude?
2. Install globally or only for the current project?
3. If wave-notifier or the same command files already exist at the target, may I overwrite them?
```

Only ask follow-up questions when the project root is unclear or when the user explicitly asks for a partial install.

## Fallback method: manual copy

### Claude

Project-local base:

```bash
mkdir -p ./.claude/skills ./.claude/commands
cp -R ./skill/wave-notifier ./.claude/skills/wave-notifier
cp ./skill/wave-notifier/commands/notify-done.md ./.claude/commands/
cp ./skill/wave-notifier/commands/notify-wave.md ./.claude/commands/
```

Global base: replace `./.claude` with `~/.claude`.

### OpenCode

Project-local base:

```bash
mkdir -p ./.opencode/skills ./.opencode/commands
cp -R ./skill/wave-notifier ./.opencode/skills/wave-notifier
cp ./skill/wave-notifier/commands/notify-done.md ./.opencode/commands/
cp ./skill/wave-notifier/commands/notify-wave.md ./.opencode/commands/
```

Global base: replace `./.opencode` with `~/.config/opencode`, or with `$OPENCODE_CONFIG_DIR` when that variable is intentionally being used.

If overwrite was explicitly approved, remove the old `skills/wave-notifier/` directory before copying the new one.

## Verification

After installation, verify these files exist under the chosen base directory:

- `skills/wave-notifier/SKILL.md`
- `commands/notify-done.md`
- `commands/notify-wave.md`

Example for a project-local OpenCode install:

```bash
ls ./.opencode/skills/wave-notifier/SKILL.md
ls ./.opencode/commands/notify-done.md
ls ./.opencode/commands/notify-wave.md
```

Adjust the base path for Claude or global installs.

## Suggested agent prompt pattern

If a user asks an agent to install this skill, the agent can follow this instruction shape:

```text
Install and configure the wave-notifier skill from this repository by following:
skill/wave-notifier/references/agent-install.md

Before making changes, ask only the minimum required questions:
- OpenCode or Claude
- global or current project
- whether overwrite is allowed if the target already exists

If project-local installation is selected and the project root is unclear, ask for the target project directory.

Prefer running skill/wave-notifier/install.sh first. If that is not suitable, fall back to manual copy.

Install all of the following together:
- skills/wave-notifier/
- commands/notify-done.md
- commands/notify-wave.md

After installation, verify the files exist, then report the exact installed paths and remind me to restart or reload the current session if needed.

Do not overwrite existing files unless I explicitly approve it.
```

## Notes for agents

- This document is the source of truth for the install flow.
- Run the installer from the unpacked skill directory.
- For project-local installs, make sure the working directory refers to the target repository root when that affects path resolution.
- OpenCode and Claude load commands from command directories, not from inside the skill directory itself, so installing the skill alone is incomplete.
- If the documented paths here ever become outdated, verify against official docs before inventing a new path.
