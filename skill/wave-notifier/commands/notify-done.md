# notify-done

Request a final webhook notification when all explicitly requested work is complete.

## Instructions

1. Confirm that the user explicitly requested notification for this task.
2. Confirm that `WEBHOOK_URL` and `BEARER_TOKEN` are already configured in the current shell environment.
3. Confirm that all requested work is complete, including any promised checks for this run.
4. Use the `wave-notifier` skill to send exactly one final completion notification.
5. Build the payload with these fields only:
   - `task_name`
   - `status`
   - `summary`
   - `finished_at`
6. Use a concise `summary`.
7. Do not send any wave-level notification from this command.
8. Do not retry delivery failures.

## Payload guidance

- `task_name`: describe the overall completed work, or use `TaskPlan final` when the workflow is centered on a Prometheus TaskPlan.
- `status`: usually `completed`
- `summary`: 1-2 short sentences describing the completed work
- `finished_at`: ISO 8601 timestamp when available

## Safety rule

Do not use this command unless the user explicitly asked to be notified.
Do not hardcode webhook credentials or pass them as inline arguments; read them from `WEBHOOK_URL` and `BEARER_TOKEN` in the environment.
