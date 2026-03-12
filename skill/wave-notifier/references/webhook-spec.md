# Webhook request format

## Configuration source

Read webhook configuration from environment variables:

- `WEBHOOK_URL`
- `BEARER_TOKEN`

Do not hardcode these values in the skill, slash commands, or repository documentation.

## Method

`POST`

## Headers

- `Authorization: Bearer <token from BEARER_TOKEN>`
- `Content-Type: application/json`

## JSON payload

```json
{
  "task_name": "string",
  "status": "completed",
  "summary": "short summary of what was finished",
  "finished_at": "2026-03-12T16:20:00+08:00"
}
```

## Notes

- This skill does not retry failed deliveries.
- A non-2xx response should be treated as delivery failure.
- `summary` should be concise and scoped to the completed task or wave.
- `finished_at` should preferably be in ISO 8601 format.
- For Prometheus TaskPlan waves, encode the wave identity in `task_name` rather than changing the payload schema.

## Example: final oh-my-opencode work complete

```json
{
  "task_name": "finish requested repository changes",
  "status": "completed",
  "summary": "Completed the requested implementation, updated the affected tests, and verified the final result.",
  "finished_at": "2026-03-12T18:30:00+08:00"
}
```

## Example: Prometheus TaskPlan wave complete

```json
{
  "task_name": "TaskPlan wave 2",
  "status": "completed",
  "summary": "Completed wave 2, including the refactor, edge-case fixes, and verification for the touched modules.",
  "finished_at": "2026-03-12T19:05:00+08:00"
}
```

## Example: Chinese summary

```json
{
  "task_name": "TaskPlan wave 3",
  "status": "completed",
  "summary": "已完成第 3 个 wave 的改动，补充了校验，并确认相关模块行为符合预期。",
  "finished_at": "2026-03-12T20:10:00+08:00"
}
```
