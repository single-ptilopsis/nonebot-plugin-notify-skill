# command installation for oh-my-opencode

This package includes companion slash command files:

- `commands/notify-done.md`
- `commands/notify-wave.md`

To make them available in oh-my-opencode, copy them into one of the command loader directories documented by oh-my-opencode, such as:

- `~/.claude/commands/`
- `./.claude/commands/`
- `~/.config/opencode/command/`
- `./.opencode/command/`

Example:

```bash
mkdir -p ./.claude/commands
cp commands/notify-done.md ./.claude/commands/
cp commands/notify-wave.md ./.claude/commands/
```

Then restart or reload your opencode session if needed.

For an agent-friendly one-step install, see `../install.sh` and `references/agent-install.md`.
