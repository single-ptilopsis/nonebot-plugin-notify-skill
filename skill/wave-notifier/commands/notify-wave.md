# notify-wave

Request webhook notifications for each completed Prometheus TaskPlan wave, plus the final completion notification when all requested work is complete.

## Instructions

1. Confirm that the user explicitly requested notification for each TaskPlan wave.
2. Confirm that `WEBHOOK_URL` and `BEARER_TOKEN` are already configured in the current shell environment.
3. For each completed wave, use the `wave-notifier` skill to send exactly one notification.
4. After the entire TaskPlan is complete, also send one final completion notification.
5. Build the payload with these fields only:
   - `task_name`
   - `status`
   - `summary`
   - `finished_at`
6. Use `task_name` values like `TaskPlan wave 1`, `TaskPlan wave 2`, and `TaskPlan final`.
7. Keep each wave `summary` short and limited to the work completed in that wave.
8. Do not retry delivery failures.

## Wave notification rules

- Notify only after a wave is actually complete.
- Do not notify for partial progress inside a wave.
- Do not notify at all unless the user explicitly requested per-wave notifications.

## Final notification rule

After all waves and requested checks are complete, send one final notification in addition to the wave notifications.

## Safety rule

Do not hardcode webhook credentials or pass them as inline arguments; read them from `WEBHOOK_URL` and `BEARER_TOKEN` in the environment.
