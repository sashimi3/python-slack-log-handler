# Python Slack Log Handler

A tiny, framework‑agnostic Python logging handler that forwards log messages to Slack.

## Features

- Supports **Incoming Webhook** URLs and **Bot Token** (`chat.postMessage`).
- Thin wrapper around the official `slack-sdk` library.
- No framework dependencies – works with scripts, Flask, FastAPI, Celery, cron jobs, etc.
- Installable via a VCS URL:

```shell
pip install git+https://github.com/sashimi3/python-slack-log-handler
```

or

```shell
pipenv install git+https://github.com/sashimi3/python-slack-log-handler
```

or

```shell
uv add git+https://github.com/sashimi3/python-slack-log-handler
```

To specify tag:

```shell
uv add git+https://github.com/sashimi3/python-slack-log-handler@v0.2.2
```

## Installation (development)

```bash
uv init --lib slack-log-handler
cd slack-log-handler
uv add slack-sdk
uv add --dev pytest pytest-cov ruff
```

## Usage
```python
import logging
from slack_log_handler import SlackHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Example 1 – Incoming Webhook
handler = SlackHandler(webhook_url="https://hooks.slack.com/services/…")
logger.addHandler(handler)

# Example 2 – Bot token
# handler = SlackHandler(bot_token="xoxb-…", channel="#logs")
# logger.addHandler(handler)

logger.info("Application started")
```

## Configuration options
- ``webhook_url`` – Slack Incoming Webhook endpoint.
- ``bot_token`` – Bot user OAuth token (`xoxb-…`).
- ``channel`` – Channel name or ID when using a bot token.
- ``username`` – Override the displayed username.
- ``icon_emoji`` / ``icon_url`` – Custom avatar.

The handler respects the standard ``logging`` level hierarchy; set the handler's level to control which messages are sent.

## Testing

```bash
pytest --cov=slack_log_handler
```

