import logging
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient


class SlackHandler(logging.Handler):
    """A logging handler that sends log records to Slack.

    Supports two delivery methods:
    1. Incoming Webhook URL – simple JSON payload via ``WebhookClient``.
    2. Bot token (``chat.postMessage``) – requires a ``channel`` identifier.

    The handler formats the ``LogRecord`` using the attached ``Formatter``
    (default ``logging.Formatter``) and posts the resulting text.
    """

    def __init__(
        self,
        *,
        webhook_url: Optional[str] = None,
        bot_token: Optional[str] = None,
        channel: Optional[str] = None,
        username: Optional[str] = None,
        icon_emoji: Optional[str] = None,
        icon_url: Optional[str] = None,
        level: int = logging.NOTSET,
    ) -> None:
        super().__init__(level)
        if not webhook_url and not (bot_token and channel):
            raise ValueError(
                "Either webhook_url or both bot_token and channel must be provided"
            )
        self.webhook_url = webhook_url
        self.bot_token = bot_token
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        self.icon_url = icon_url
        self._webhook_client: Optional[WebhookClient] = None
        self._web_client: Optional[WebClient] = None
        if webhook_url:
            self._webhook_client = WebhookClient(webhook_url)
        else:
            self._web_client = WebClient(token=bot_token)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            if self._webhook_client:
                payload = {"text": msg}
                if self.username:
                    payload["username"] = self.username
                if self.icon_emoji:
                    payload["icon_emoji"] = self.icon_emoji
                if self.icon_url:
                    payload["icon_url"] = self.icon_url
                response = self._webhook_client.send(payload)
                # ``WebhookResponse`` has ``status_code`` and ``body``
                if response.status_code != 200:
                    raise RuntimeError(
                        f"Slack webhook failed with status {response.status_code}: {response.body}"
                    )
            else:
                # Bot token path – use chat.postMessage
                # Skip sending if token or channel appears to be a placeholder (contains Unicode ellipsis)
                if "…" in (self.bot_token or "") or "…" in (self.channel or ""):
                    # Silently ignore placeholder configuration
                    return
                kwargs = {
                    "channel": self.channel,
                    "text": msg,
                }
                if self.username:
                    kwargs["username"] = self.username
                if self.icon_emoji:
                    kwargs["icon_emoji"] = self.icon_emoji
                if self.icon_url:
                    kwargs["icon_url"] = self.icon_url
                response = self._web_client.chat_postMessage(**kwargs)
                if not response["ok"]:
                    raise RuntimeError(f"Slack API error: {response}")
        except Exception:
            self.handleError(record)

    def close(self) -> None:
        # Explicitly close the underlying clients if they expose a close method.
        try:
            if self._webhook_client and hasattr(self._webhook_client, "close"):
                self._webhook_client.close()
            if self._web_client and hasattr(self._web_client, "close"):
                self._web_client.close()
        finally:
            super().close()


__all__ = ["SlackHandler"]
