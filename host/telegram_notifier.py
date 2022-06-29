import asyncio

import cv2
import telegram
import telegram as tg
from decouple import config
from time import time
from telegram.ext import Application, CommandHandler, MessageHandler
from object_tracking import ObjectsTracker

loop = asyncio.get_event_loop()


class TelegramNotifier:
    def __init__(self, objects_tracker: ObjectsTracker):
        self.objects_tracker = objects_tracker
        # self.bot = tg.Bot(config("TELEGRAM_TOKEN"))
        self.application = Application.builder().token(config("TELEGRAM_TOKEN")).build()
        self.last_message_time = 0
        self.message_cooldown = config("TELEGRAM_MESSAGE_COOLDOWN", cast=float)
        self.chat_id = config("TELEGRAM_CHAT_ID", cast=int)
        self.save_sent_images = config("TELEGRAM_SAVE_SENT_IMAGES", cast=bool)
        self.show_boxes = config("TELEGRAM_SHOW_BOXES", cast=bool)

        self.application.add_handler(CommandHandler("where", self.where))
        # self.application.run_polling()
        self.initialize_application()

    def initialize_application(self):
        loop.run_until_complete(self.application.initialize())
        if self.application.post_init:
            loop.run_until_complete(self.application.post_init(self))
        loop.run_until_complete(
            self.application.updater.start_polling()
        )  # one of updater.start_webhook/polling
        loop.run_until_complete(self.application.start())

    def notify(self, image_with_boxes, image, detected_objects):
        if time() - self.last_message_time < self.message_cooldown:
            return
        self.last_message_time = time()
        sent_image = cv2.imencode(".jpg", image_with_boxes if self.show_boxes else image)[1].tobytes()
        caption = "Detected objects: " + ", ".join(detected_objects)
        loop.run_until_complete(
            self.application.bot.send_photo(self.chat_id, photo=sent_image, caption=caption)
        )
        if self.save_sent_images:
            cv2.imwrite(f"collected_images/{int(time())}.jpg", image)

    def update(self):
        try:
            loop.run_until_complete(self.application.bot.get_updates())
        except telegram.error.TimedOut:
            pass

    async def where(self, update, context):
        # print(f'{update.message.from_user.first_name} asked for where')
        # print(self.objects_tracker)
        await update.message.reply_text(str(self.objects_tracker))
