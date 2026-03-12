# command installation for OpenCode and Claude

This package includes companion slash command files:

- `commands/notify-done.md`
- `commands/notify-wave.md`

To make them available, copy them into a documented command loader directory for the active runtime:

- `~/.claude/commands/`
- `./.claude/commands/`
- `~/.config/opencode/commands/`
- `./.opencode/commands/`

Examples:

```bash
mkdir -p ./.claude/commands
cp commands/notify-done.md ./.claude/commands/
cp commands/notify-wave.md ./.claude/commands/
```

```bash
mkdir -p ./.opencode/commands
cp commands/notify-done.md ./.opencode/commands/
cp commands/notify-wave.md ./.opencode/commands/
```

Then restart or reload your current OpenCode or Claude session if needed.

If your current runtime uses a different command directory than the ones listed
here, use the web-search fallback in `references/agent-install.md` before
copying files.

For an agent-friendly one-step install, see `../install.sh` and `references/agent-install.md`.
