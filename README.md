# nonebot-plugin-notify-skill

## 项目简介
`nonebot-plugin-notify-skill` 是一个基于 NoneBot2 的插件，用于接收外部 Webhook 通知，并通过已连接的 OneBot V11 Bot 转发给指定的 QQ 用户或群组。

## 功能特性
- 提供标准 Webhook 接口接收通知。
- 支持 Bearer Token 身份验证，确保接口安全。
- 支持转发通知至多个 QQ 用户和群组。
- 转发消息会包含任务名、状态、摘要和完成时间。
- 提供配套的辅助脚本用于测试和手动触发。

## 项目结构
```text
.
├── nonebot_plugin_notify_skill/
│   └── notify_webhook.py      # 插件核心逻辑
├── skill/
│   └── wave-notifier/
│       ├── scripts/
│       │   └── send_webhook.py # Webhook 发送辅助脚本
│       └── SKILL.md           # 技能详细说明
├── pyproject.toml             # 项目配置与依赖管理
└── README.md                  # 项目说明文档
```

## 环境要求
- Python >=3.10, <4.0
- 已安装 [uv](https://github.com/astral-sh/uv) 依赖管理工具。
- 运行时需有一个已连接的 OneBot V11 Bot。

## 安装与配置

### 安装
使用 `uv` 同步依赖：
```bash
uv sync --dev --frozen
```

### 配置
在项目的 `.env` 文件或环境变量中配置以下项：
| 配置项 | 类型 | 描述 |
| :--- | :--- | :--- |
| `NOTIFY_WEBHOOK_TOKEN` | `str` | 必填。Webhook 验证所需的 Bearer Token。 |
| `NOTIFY_WEBHOOK_PATH` | `str` | 可选。接口路径，默认为 `/notify`。 |
| `NOTIFY_WEBHOOK_USER_IDS` | `set[int]` | 通知接收者的 QQ 号集合。 |
| `NOTIFY_WEBHOOK_GROUP_IDS` | `set[int]` | 通知接收群组的 QQ 群号集合。 |

> 注意：`NOTIFY_WEBHOOK_USER_IDS` 和 `NOTIFY_WEBHOOK_GROUP_IDS` 必须至少配置其中之一。

NoneBot 会通过 `pyproject.toml` 中的 `plugin_dirs = ["nonebot_plugin_notify_skill"]` 加载本地插件目录。

## 运行方式
启动 NoneBot 实例：
```bash
uv run nb run --reload
```

## Webhook 接口说明

### 接口地址
`POST <bot-url>/notify` (路径可由 `NOTIFY_WEBHOOK_PATH` 自定义)

### 认证方式
请求头需包含：

- `Authorization: Bearer <NOTIFY_WEBHOOK_TOKEN>`
- `Content-Type: application/json`

### 请求 Payload (JSON)
| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_name` | `str` | 任务名称。 |
| `status` | `str` | 执行状态（如 Success, Failure）。 |
| `summary` | `str` | 执行摘要或详细说明。 |
| `finished_at` | `str` | 完成时间字符串。 |

以上四个字段都要求为非空字符串，`finished_at` 推荐使用 ISO 8601 格式。

### 响应示例
成功响应：
```json
{"ok": true}
```

常见失败场景包括：

- 未提供或提供了错误的 Bearer Token，接口会返回 `401`。
- 当前没有已连接的 OneBot V11 Bot，接口会返回 `503`。

## 代码质量检查
项目提供了完整的质量检查工具，在提交代码前建议运行：
- **格式检查**：`uv run ruff format --check .`
- **Lint 检查**：`uv run ruff check .`
- **类型检查**：`uv run pyright`

## 辅助脚本
项目内置了发送 Webhook 的测试脚本，位于 `skill/wave-notifier/scripts/send_webhook.py`。
使用方法：
```bash
uv run python skill/wave-notifier/scripts/send_webhook.py --help
```

该脚本会向 Webhook 地址发送包含 `task_name`、`status`、`summary`、`finished_at` 的 JSON 请求体，并使用 Bearer Token 完成认证。

## 安装 wave-notifier skill

`skill/wave-notifier/` 可以安装到 OpenCode 或 Claude 的 skill 目录中，并可同时安装配套命令 `/notify-done` 和 `/notify-wave`。

### 给人类看的

复制并粘贴下面这段提示词给你的 LLM Agent（OpenCode、Claude Code 等）：

```text
Install and configure the wave-notifier skill in by following the instructions here:
https://raw.githubusercontent.com/single-ptilopsis/nonebot-plugin-notify-skill/refs/heads/main/skill/wave-notifier/references/agent-install.md
```

### 给 LLM Agent 看的

读取安装指南并照做：

```bash
curl -s https://raw.githubusercontent.com/single-ptilopsis/nonebot-plugin-notify-skill/refs/heads/main/skill/wave-notifier/references/agent-install.md
```

### 手动安装

#### 自动脚本安装

仓库已提供安装脚本：

```bash
cd skill/wave-notifier
./install.sh --help
```

常见用法：

```bash
./install.sh --project
./install.sh --user
./install.sh --opencode --project
./install.sh --opencode --user
./install.sh --claude --project
./install.sh --claude --user
```

脚本会完成以下操作：

- 安装 `skills/wave-notifier/`
- 安装 `commands/notify-done.md`
- 安装 `commands/notify-wave.md`
- 在可能时自动识别当前是 OpenCode 还是 Claude

#### 手动复制安装

如果你不想运行脚本，也可以手动复制文件。

##### 安装到 Claude

- 当前项目范围：`./.claude/`
- 全局范围：`~/.claude/`

```bash
mkdir -p ./.claude/skills ./.claude/commands
rm -rf ./.claude/skills/wave-notifier
cp -R ./skill/wave-notifier ./.claude/skills/wave-notifier
cp ./skill/wave-notifier/commands/notify-done.md ./.claude/commands/
cp ./skill/wave-notifier/commands/notify-wave.md ./.claude/commands/
```

##### 安装到 OpenCode

- 当前项目范围：`./.opencode/`
- 全局范围：`~/.config/opencode/`

```bash
mkdir -p ./.opencode/skills ./.opencode/commands
rm -rf ./.opencode/skills/wave-notifier
cp -R ./skill/wave-notifier ./.opencode/skills/wave-notifier
cp ./skill/wave-notifier/commands/notify-done.md ./.opencode/commands/
cp ./skill/wave-notifier/commands/notify-wave.md ./.opencode/commands/
```

> 如果你要安装到全局目录，请把上面的 `./.claude` 替换成 `~/.claude`，或把 `./.opencode` 替换成 `~/.config/opencode`。
>
> 上面的 `rm -rf` 会覆盖已有安装。执行前请先确认目标目录中的旧版本是否可以被替换。

安装完成后，如当前 agent 会话没有自动刷新，请重启或重新加载会话。

## 技能目录说明
`skill/` 目录包含了针对特定场景的优化说明和资源。例如 `wave-notifier` 提供了在 `oh-my-opencode` 环境下的最佳实践，详见其子目录下的 `SKILL.md`。

## 开发注意事项
- 核心插件代码位于 `nonebot_plugin_notify_skill/notify_webhook.py`，不要随意在插件目录添加 `__init__.py`。
- 本项目目前没有自动化测试套件。
- 运行时必须确保有一个已连接的 OneBot V11 Bot。
- 代码需遵循 Python 3.9 兼容性基准线（由 Ruff 和 Pyright 强制执行）。

## 相关文档
- [NoneBot2 官方文档](https://nonebot.dev/)
- [OneBot V11 协议规范](https://11.onebot.dev/)
