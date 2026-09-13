import logging
import os

from slack_log_handler import SlackHandler

logger = logging.getLogger(__name__)
# アプリ全体の最低レベル(デバッグまで取得)
logger.setLevel(logging.DEBUG)

# コンソールハンドラ
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(console_handler)

# Slack ハンドラ
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "")

# 実際に利用する際はどちらか一方だけ設定してください
# slack_handler = SlackHandler(webhook_url=SLACK_WEBHOOK_URL)
slack_handler = SlackHandler(bot_token=SLACK_BOT_TOKEN, channel=SLACK_CHANNEL_ID)
# エラーレベル以上だけ Slack に送信
slack_handler.setLevel(logging.INFO)
logger.addHandler(slack_handler)

# デモログ
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("致命的エラー")
