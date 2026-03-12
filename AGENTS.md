# Agent Guide: nonebot-plugin-notify-skill

This guide provides repository-specific context and verified commands for coding agents.
Prior to this file's creation, no `AGENTS.md`, `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md` existed in this repository.

## Repository Overview
This is a Python/NoneBot project with two related but separate parts:
- the bot/plugin code under `bot.py` and `nonebot_plugin_notify_skill/plugins/`
- the skill subtree under `skill/wave-notifier/`

Treat `pyproject.toml` and the current source code as the source of truth if this guide and the code ever drift.

## Key Files & Roles
- `pyproject.toml`: source of truth for dependencies, Ruff, Pyright, and NoneBot plugin loading.
- `uv.lock`: locked dependency graph for the `uv` environment.
- `bot.py`: primary NoneBot entrypoint.
- `main.py`: stub script; not the main runtime path.
- `nonebot_plugin_notify_skill/plugins/notify_webhook.py`: main plugin implementation.
- `skill/wave-notifier/SKILL.md`: skill documentation.
- `skill/wave-notifier/scripts/send_webhook.py`: stdlib CLI helper for webhook delivery tests.
- `README.md`: short project bootstrap guidance.

## Structure Warning
- `nonebot_plugin_notify_skill/` and `nonebot_plugin_notify_skill/plugins/` currently do **not** contain `__init__.py`.
- Plugin discovery is configured through `plugin_dirs` in `pyproject.toml`.
- Do **not** add `__init__.py` files there unless packaging work explicitly requires it.
- Do not assume the `skill/` subtree is part of the runtime plugin package; it is a separate documentation/helper area.

## Environment & Setup
The project uses `uv` for environment and dependency management.

### Setup
- Sync dev environment: `uv sync --dev --frozen`

### Run the bot
- Reloading dev run: `uv run nb run --reload`
- Direct run: `uv run python bot.py`
- NoneBot CLI help: `uv run nb --help`
- NoneBot run help: `uv run nb run --help`

### Helper script
- Webhook sender help: `uv run python skill/wave-notifier/scripts/send_webhook.py --help`

## Build / Package Reality
- There is **no dedicated build or packaging command** configured in this repository today.
- There is no `[build-system]` section in `pyproject.toml`.
- Standard workflows rely on local `uv` execution, not package-building commands.
- Do not invent `make`, `poetry`, `pip install`, or `uv build` workflows here.

## Quality Gates
Run these commands before finishing coding work.

| Goal | Command |
| :--- | :--- |
| Lint all | `uv run ruff check .` |
| Lint main plugin | `uv run ruff check nonebot_plugin_notify_skill/plugins/notify_webhook.py` |
| Format all | `uv run ruff format .` |
| Format check all | `uv run ruff format --check .` |
| Format check plugin | `uv run ruff format --check nonebot_plugin_notify_skill/plugins/notify_webhook.py` |
| Typecheck all | `uv run pyright` |
| Typecheck plugin | `uv run pyright nonebot_plugin_notify_skill/plugins/notify_webhook.py` |

## Testing Reality
There is **no automated test suite** configured in this repository right now.

- `pytest` is not installed.
- `uv run python -m pytest` fails with `No module named pytest`.
- No `tests/` directory was found.
- No `test_*.py`, `*_test.py`, or `conftest.py` files were found.
- No CI or workflow files were found to run tests automatically.
- There is **no supported command today** for running all tests, one test file, or one test case.

### Verification strategy instead of tests
- Use the Ruff and Pyright commands above.
- Run the bot with `uv run nb run --reload` or `uv run python bot.py` when runtime verification is needed.
- Use `skill/wave-notifier/scripts/send_webhook.py` for manual webhook testing.

## Versioning & Tooling Baseline
There is a version tension that agents should respect:

- project metadata declares Python `>=3.10, <4.0`
- local `.python-version` is `3.14`
- Ruff and Pyright are configured to target Python `3.9`

Stay within the conservative Python 3.9 syntax and type-checking baseline so quality gates keep passing.

## Enforced by Tooling
These are grounded in `pyproject.toml`.

### Ruff
- line length: `88`
- line ending: `lf`
- target version: `py39`
- linting is intentionally strict and enables many rule families
- some ignores are deliberate framework accommodations, including `E402` and `B008`

### Pyright
- `pythonVersion = "3.9"`
- `typeCheckingMode = "standard"`

## Observed Code Conventions
These come from the current source files and should be treated as repository conventions.

- Prefer `from __future__ import annotations` in real modules.
- Prefer PEP 585 built-in generics such as `set[int]`, `list[str]`, and `dict[str, bool]`.
- Use `snake_case` for functions and variables.
- Use `PascalCase` for classes and Pydantic models.
- Use Pydantic v2 validators: `@field_validator` and `@model_validator`.
- Use `HTTPException` with `fastapi.status` for API failures.
- Use `hmac.compare_digest` for token or secret comparison.
- Use `nonebot.logger` for internal plugin logging.
- Build multiline user-facing messages with `"\n".join([...])` or f-strings.
- Keep async code async: route handlers and network-facing bot actions should stay in `async def` functions.
- For helper scripts, return explicit exit codes and emit structured JSON on stdout/stderr.

## NoneBot and Plugin Structure
`nonebot_plugin_notify_skill/plugins/notify_webhook.py` shows the main local pattern:

1. Define a config model with `pydantic.BaseModel`.
2. Define request payload models with Pydantic fields.
3. Declare plugin metadata with `__plugin_meta__ = PluginMetadata(...)`.
4. Load config through `get_plugin_config(...)`.
5. Retrieve the FastAPI app with `nonebot.get_app()`.
6. Register routes directly on that app.
7. Use `async` route handlers for webhook endpoints.
8. Raise `HTTPException` when validation or runtime prerequisites fail.

Follow this structure unless the existing codebase evolves away from it.

## Environment & Secrets
- Local development uses `.env` files.
- Do not print, log, or commit real secret values.
- Be careful with tracked environment variants such as `.env.dev` and `.env.prod`.
- The plugin config expects a real webhook token, not a placeholder.
- The plugin also requires at least one notification target.

## Agent Workflow Guidance
- Check `pyproject.toml` before inventing commands or assumptions.
- Prefer `uv run ...` commands over global tools.
- Do not assume a build step, test runner, or CI pipeline exists.
- Keep changes aligned with the current NoneBot plugin loading pattern.
- When editing plugin code, verify with Ruff and Pyright before stopping.
- When touching webhook behavior, do manual validation with the bot or helper script.

## Agent Do / Don't Checklist
- Do use `uv` for setup and command execution.
- Do treat `pyproject.toml` as the tooling source of truth.
- Do follow the Python 3.9-compatible syntax baseline.
- Do use `nonebot.logger` instead of `print` in plugin code.
- Do use `hmac.compare_digest` for sensitive comparisons.
- Do keep `main.py` as a stub unless explicitly asked to change runtime entrypoints.
- Don't add `__init__.py` to plugin directories casually.
- Don't attempt to run nonexistent tests.
- Don't invent CI, Makefile, Poetry, or package-build workflows.
- Don't commit or expose secrets from local environment files.
