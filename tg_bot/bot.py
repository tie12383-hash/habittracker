import logging
from telegram import Bot
from telegram.error import TelegramError
from django.conf import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


def send_telegram_message(chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        logging.error(f"Ошибка отправки сообщения: {e}")
