import cv2
import telegram as tg
from decouple import config
from time import time

class TelegramNotifier:
    def __init__(self):
        self.bot = tg.Bot(config('TELEGRAM_TOKEN'))
        self.last_message_time = 0
        self.message_cooldown = config('TELEGRAM_MESSAGE_COOLDOWN', cast=float)
        self.chat_id = config('TELEGRAM_CHAT_ID', cast=int)

    def notify(self, image, detected_objects):
        if time() - self.last_message_time < self.message_cooldown:
            return
        self.last_message_time = time()
        image = cv2.imencode('.jpg', image)[1].tobytes()
        caption = 'Detected objects: ' + ', '.join(detected_objects)
        self.bot.send_photo(self.chat_id, photo=image, caption=caption)
