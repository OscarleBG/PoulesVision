"""
utility to download all photos from telegram with a 👎
"""
import telegram as tg
from decouple import config


def main():
    bot = tg.Bot(config("TELEGRAM_TOKEN"))
    chat_id = config("TELEGRAM_CHAT_ID", cast=int)
    # retrieve all photos from telegram chat
    photos = tg.Chat(chat_id
