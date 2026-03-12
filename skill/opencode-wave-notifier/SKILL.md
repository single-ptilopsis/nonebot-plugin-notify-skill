---
name: opencode-wave-notifier
description: send explicit webhook notifications for oh-my-opencode workflows that use sisyphus orchestration and prometheus planning. use when the user clearly asks to be notified after all requested changes are finished, or after each taskplan or wave completes, such as "完成所有改动后，通知我" or "在taskplan各wave完成后，分别通知我，并给出简短summary". this skill is opt-in only, for agent-initiated notifications, reads webhook_url and bearer_token from environment variables, and should not be used unless the user explicitly requested notification.
---

# opencode wave notifier

Send one HTTP POST notification for a completed oh-my-opencode work unit when notification was explicitly requested by the user.

## Workflow

1. Confirm that the current task is running in an oh-my-opencode workflow and that the user explicitly asked for notification.
2. Confirm that `WEBHOOK_URL` and `BEARER_TOKEN` are available in the current shell environment.
3. Determine the completion scope:
   - entire requested work is complete
   - one Prometheus TaskPlan wave is complete
4. Build the four required payload fields:
   - `task_name`
   - `status`
   - `summary`
   - `finished_at`
5. Run `scripts/send_webhook.py` exactly once.
6. Report success or failure in the conversation.

## Strict notification policy

- Treat this skill as **explicit opt-in only**.
- Use it only when the user clearly asked for notification in the current task.
- Do not infer notification intent from general workflow context.
- Do not auto-listen, poll, hook, or monitor in the background.
- Do not retry failed deliveries.
- If delivery fails, report failure honestly and continue unless the user instructed otherwise.

## Required environment

This skill must read webhook configuration from environment variables, not from inline command arguments, command files, repository docs, or hardcoded values.

Required variables:

- `WEBHOOK_URL`
- `BEARER_TOKEN`

If either variable is missing, stop and report that the environment is not configured.

## Required inputs

Collect these values before running the script:

- `task_name`
- `status`
- `summary`
- `finished_at`

Use ISO 8601 for `finished_at` when possible.

## opencode-specific completion rules

### Final completion notification

Use this when the user asked for a notification after all requested work is complete.

Recommended values:

- `task_name`: describe the whole requested work, for example `finish requested repository changes`
- `status`: `completed`
- `summary`: 1-3 short sentences covering the highest-value completed work and validation

Only send the final notification after:

- requested implementation work is done
- relevant edits are complete
- any promised checks or validation for this run are complete

### TaskPlan wave notification

Use this when the user asked for a notification after each TaskPlan wave.

Recommended `task_name` format:

- `TaskPlan wave 1`
- `TaskPlan wave 2`
- `TaskPlan wave 3`

Wave `summary` guidance:

- Keep it short
- Mention only the work completed in that wave
- Mention validation only if it was part of that wave

Good examples:

- `Implemented the API changes for the first wave and updated the affected tests.`
- `Completed the refactor wave, fixed edge cases, and verified the touched modules.`

## Prometheus / Plan Builder guidance

When the workflow uses Prometheus-created plans or TaskPlan waves:

- Treat each completed wave as a separately notifiable milestone only if the user explicitly requested per-wave notifications.
- Otherwise, wait until all requested work is complete and send one final notification.
- Preserve the user's preferred language in `summary` when practical.

## Status guidance

Prefer these values unless the user specified another convention:

- `completed` for successful completion
- `failed` when the task outcome itself failed or when the user explicitly asked to notify failure states

A webhook delivery failure is not the same as a task failure. Report delivery failure in chat, but do not silently change the task's business status unless the user asked for that behavior.

## Command

Run this command from the skill directory after confirming `WEBHOOK_URL` and `BEARER_TOKEN` are present in the environment:

```bash
python scripts/send_webhook.py \
  --task-name "$TASK_NAME" \
  --status "$STATUS" \
  --summary "$SUMMARY" \
  --finished-at "$FINISHED_AT"
```

## Response behavior

After the script finishes:

- If the request succeeds, say that the notification was sent.
- If the request fails, say that the notification could not be delivered and include the script's error output when helpful.
- If required environment variables are missing, say that notification could not be sent because the environment is not configured.

## Companion slash commands

This package includes companion command files for oh-my-opencode:

- `commands/notify-done.md`
- `commands/notify-wave.md`

These files are packaged for convenience, but oh-my-opencode loads slash commands from command directories such as `~/.claude/commands/` or `./.claude/commands/`, not from inside the skill directory. See `references/command-install.md` for installation details.

## Reference

See `references/webhook-spec.md` for the request format and opencode-oriented examples.
