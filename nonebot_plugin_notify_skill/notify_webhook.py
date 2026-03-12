from __future__ import annotations

import hmac

import nonebot
from fastapi import HTTPException, Request, status
from nonebot import get_plugin_config, logger
from nonebot.adapters.onebot.v11 import Bot as OneBotV11Bot
from nonebot.plugin import PluginMetadata
from pydantic import BaseModel, Field, field_validator, model_validator


class NotifyWebhookConfig(BaseModel):
    notify_webhook_token: str = Field(min_length=1)
    notify_webhook_path: str = "/notify"
    notify_webhook_user_ids: set[int] = Field(default_factory=set)
    notify_webhook_group_ids: set[int] = Field(default_factory=set)

    @field_validator("notify_webhook_token")
    @classmethod
    def validate_notify_webhook_token(cls, value: str) -> str:
        normalized_value = value.strip()
        if normalized_value == "change-me":
            msg = "NOTIFY_WEBHOOK_TOKEN must be replaced before startup."
            raise ValueError(msg)

        return normalized_value

    @field_validator("notify_webhook_path")
    @classmethod
    def validate_notify_webhook_path(cls, value: str) -> str:
        if value.startswith("/"):
            return value

        msg = "NOTIFY_WEBHOOK_PATH must start with '/'."
        raise ValueError(msg)

    @model_validator(mode="after")
    def validate_notify_targets(self) -> "NotifyWebhookConfig":
        if self.notify_webhook_user_ids or self.notify_webhook_group_ids:
            return self

        msg = (
            "At least one notify target must be configured in "
            "NOTIFY_WEBHOOK_USER_IDS or NOTIFY_WEBHOOK_GROUP_IDS."
        )
        raise ValueError(msg)


class NotifyWebhookPayload(BaseModel):
    task_name: str = Field(min_length=1)
    status: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    finished_at: str = Field(min_length=1)


__plugin_meta__ = PluginMetadata(
    name="notify_webhook",
    description="Receive notify webhooks and forward them through OneBot V11.",
    usage="POST /notify with Bearer auth and the webhook-spec payload.",
    config=NotifyWebhookConfig,
    supported_adapters={"~onebot.v11"},
)

plugin_config = get_plugin_config(NotifyWebhookConfig)
app = nonebot.get_app()


def build_notify_message(payload: NotifyWebhookPayload) -> str:
    return "\n".join(
        (
            "【Notify】",
            f"任务: {payload.task_name}",
            f"状态: {payload.status}",
            f"摘要: {payload.summary}",
            f"完成时间: {payload.finished_at}",
        )
    )


def require_bearer_token(request: Request) -> None:
    authorization = request.headers.get("Authorization")
    expected_authorization = f"Bearer {plugin_config.notify_webhook_token}"

    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header.",
        )

    if hmac.compare_digest(authorization, expected_authorization):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid bearer token.",
    )


def get_connected_onebot_bot() -> OneBotV11Bot:
    for bot in nonebot.get_bots().values():
        if isinstance(bot, OneBotV11Bot):
            return bot

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="No connected OneBot V11 bot is available.",
    )


async def send_notify_message(bot: OneBotV11Bot, message: str) -> None:
    for user_id in plugin_config.notify_webhook_user_ids:
        await bot.call_api("send_private_msg", user_id=user_id, message=message)

    for group_id in plugin_config.notify_webhook_group_ids:
        await bot.call_api("send_group_msg", group_id=group_id, message=message)


@app.post(plugin_config.notify_webhook_path)
async def notify_webhook(
    request: Request, payload: NotifyWebhookPayload
) -> dict[str, bool]:
    require_bearer_token(request)
    bot = get_connected_onebot_bot()
    message = build_notify_message(payload)
    await send_notify_message(bot, message)
    return {"ok": True}


logger.info("Notify webhook registered at {}", plugin_config.notify_webhook_path)
