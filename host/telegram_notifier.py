import cv2
import telegram as tg
from decouple import config
from time import time
from telegram.ext import Application, CommandHandler, MessageHandler
from object_tracking import ObjectsTracker


class TelegramNotifier:
    def __init__(self, objects_tracker: ObjectsTracker):
        self.objects_tracker = objects_tracker
        # self.bot = tg.Bot(config("TELEGRAM_TOKEN"))
        self.application = Application.builder().token(config("TELEGRAM_TOKEN")).build()
        self.last_message_time = 0
        self.message_cooldown = config("TELEGRAM_MESSAGE_COOLDOWN", cast=float)
        self.chat_id = config("TELEGRAM_CHAT_ID", cast=int)

        self.application.add_handler(CommandHandler("where", self.where))

    def notify(self, image, detected_objects):
        if time() - self.last_message_time < self.message_cooldown:
            return
        self.last_message_time = time()
        image = cv2.imencode(".jpg", image)[1].tobytes()
        caption = "Detected objects: " + ", ".join(detected_objects)
        self.application.bot.send_photo(self.chat_id, photo=image, caption=caption)

    async def where(self, update, context):
        await update.message.reply_text(self.objects_tracker)
