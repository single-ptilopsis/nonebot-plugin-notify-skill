# Agent Guide: nonebot-plugin-notify-skill
Use this file as the repository-specific guide for coding agents.
If this file and the code ever disagree, trust `pyproject.toml` and the current source tree.

## Repository Reality
This repo currently has two main parts:
- `nonebot_plugin_notify_skill/notify_webhook.py`: the actual NoneBot plugin
- `skill/wave-notifier/`: skill docs, references, commands, and a helper script

Important facts verified from the tree:
- There is no `bot.py`
- There is no `main.py`
- There is no `tests/` directory
- There is no `nonebot_plugin_notify_skill/plugins/` subdirectory
- There is no dedicated build/package workflow

## Layout
```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── uv.lock
├── nonebot_plugin_notify_skill/
│   └── notify_webhook.py
└── skill/
    └── wave-notifier/
        ├── SKILL.md
        ├── agents/
        ├── commands/
        ├── references/
        └── scripts/
            └── send_webhook.py
```

## Rules Files
The following were checked and are not present:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`
If any of them are added later, treat them as higher-priority instructions.

## Tooling Baseline
- Dependency manager: `uv`
- Runtime framework: `nonebot2` with FastAPI and OneBot V11
- Formatter/linter: `ruff`
- Type checker: `pyright`
- Declared Python requirement: `>=3.10, <4.0`
- Ruff target version: `py39`
- Pyright version: `3.9`
- Local `.python-version`: `3.14`
Even though the local interpreter is newer, keep code compatible with Python 3.9 semantics because Ruff and Pyright enforce that baseline.

## Setup and Run Commands
- Install/sync dev dependencies: `uv sync --dev --frozen`
- Show NoneBot CLI help: `uv run nb --help`
- Start local runtime: `uv run nb run --reload`
- Show helper script help: `uv run python skill/wave-notifier/scripts/send_webhook.py --help`
The NoneBot CLI command above is the only verified runtime entrypoint in this repo.

## Build / Package Commands
There is no build step today.
- No `[build-system]` section exists in `pyproject.toml`
- No `make`, `tox`, `nox`, `poetry`, or CI packaging workflow exists
- Do not invent `uv build`, wheel, or publish commands

## Lint / Format / Typecheck
Use `uv run ...` instead of global tools.

### Whole repository
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Format check: `uv run ruff format --check .`
- Typecheck: `uv run pyright`

### Single file
- Lint one file: `uv run ruff check path/to/file.py`
- Format one file: `uv run ruff format path/to/file.py`
- Format-check one file: `uv run ruff format --check path/to/file.py`
- Typecheck one file: `uv run pyright path/to/file.py`

## Test Commands
There is no automated test framework configured right now.
Verified current state:
- No `tests/` directory exists
- No `test_*.py`, `*_test.py`, or `conftest.py` files exist
- `pytest` is not installed in the environment
- `uv run python -m pytest` fails with `No module named pytest`
- Run all tests: not supported
- Run a single test file: not supported
- Run a single test case: not supported

If you add tests later, add the framework first and then document the exact single-file and single-test commands before claiming support.

## Practical Verification Strategy
Since there is no test suite, use the closest checks available:
1. `uv run ruff check ...`
2. `uv run ruff format --check ...`
3. `uv run pyright ...`
4. `uv run nb run --reload` when plugin behavior changes
5. `uv run python skill/wave-notifier/scripts/send_webhook.py --help` or a real webhook call for manual verification
At inspection time, `uv run pyright` passes, while `uv run ruff format --check .` and `uv run ruff check .` both report pre-existing issues in `skill/wave-notifier/scripts/send_webhook.py`. Separate those from anything you introduce.

## Code Style
### Imports and module structure
- Prefer `from __future__ import annotations`
- Keep imports grouped and Ruff/isort-compatible
- Prefer direct imports over wildcard imports
- Avoid adding `__init__.py` unless packaging work truly requires it
- Plugin discovery uses `plugin_dirs = ["nonebot_plugin_notify_skill"]`
- Keep plugin code in `nonebot_plugin_notify_skill/`, not a made-up `plugins/` subdirectory

### Formatting
- Maximum line length: `88`
- Line endings: `lf`
- Ruff is the formatter of record
- Follow standard Ruff formatting instead of custom alignment styles

### Types and typing
- Keep code compatible with Pyright `typeCheckingMode = "standard"`
- Prefer explicit return types on public functions where practical
- Prefer built-in generics like `set[int]`, `list[str]`, `dict[str, bool]`
- `pyupgrade.keep-runtime-typing = true` is enabled; avoid rewrites that break runtime typing behavior
- Avoid unnecessary `Any` even though Ruff tolerates `ANN401`

### Naming
- Use `snake_case` for functions, variables, and helpers
- Use `PascalCase` for classes and Pydantic models
- Prefer descriptive names tied to the webhook domain

### Data modeling
- Use `pydantic.BaseModel` for config and payload models
- Use `Field(...)` constraints such as `min_length=1`
- Prefer Pydantic v2 validators: `@field_validator` and `@model_validator`
- Validate and normalize input at the model boundary

### Error handling
- Use `fastapi.HTTPException` with `fastapi.status` for request-facing errors
- Use `ValueError` in validators for invalid config
- Use `hmac.compare_digest` for sensitive token comparison
- Avoid blind exception handling unless there is a clear boundary reason
- In helper scripts, return explicit exit codes and machine-readable output

### Logging and output
- Use `nonebot.logger` in plugin runtime code
- Do not use `print` in the NoneBot plugin module
- Helper scripts may use stdout/stderr intentionally for JSON output

### Async and framework conventions
- Keep webhook handlers `async def`
- Get config through `get_plugin_config(...)`
- Use `PluginMetadata` for plugin declaration
- Register routes on `nonebot.get_app()`
- Keep bot message sending on the async call path

### Message and payload conventions
- Build multi-line bot messages with `"\n".join(...)` or simple f-strings
- Preserve the current payload keys: `task_name`, `status`, `summary`, `finished_at`
- Keep those payload fields as non-empty strings unless a schema change is intentional

## Secrets and Environment
- Do not print, log, or commit real secrets
- `.env`, `.env.dev`, and `.env.prod` exist; treat them as sensitive
- `NOTIFY_WEBHOOK_TOKEN` must not remain `change-me`
- At least one of `NOTIFY_WEBHOOK_USER_IDS` or `NOTIFY_WEBHOOK_GROUP_IDS` must be configured
- The helper script reads `WEBHOOK_URL` and `BEARER_TOKEN` from environment variables

## Agent Notes
- Check `pyproject.toml` before assuming commands or project structure
- Prefer minimal diffs that match current NoneBot and Pydantic patterns
- When touching `nonebot_plugin_notify_skill/notify_webhook.py`, verify with Ruff and Pyright
- When touching webhook behavior, prefer manual end-to-end validation over invented tests
- Do not claim single-test support unless a real test framework is added
