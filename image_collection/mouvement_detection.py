from itertools import chain
import cv2
from cv2 import threshold
from cv2 import CHAIN_APPROX_NONE
from cv2 import CHAIN_APPROX_SIMPLE
from matplotlib.pyplot import contour
from time import time_ns,sleep
import telegram
import threading

PATH = '/home/pi/image-collection/captured_images'

TELEGRAM_BOT_TOKEN = '5344733165:AAF0Wzl6y0U03iQGXjHjwAfOqMhjbxltN5Q' 
TELEGRAM_CHAT_ID = -646055502
TELEGRAM_COOLDOWN = 60 * 10**9 #in nanoseconds
TELEGRAM_NOTIFICATION_SILENT = True

class MouvementDetector:
    def __init__(self,cam,FPS=1):
        self.cam = cam
        self.sleep_time = 1/FPS
        self.last_message = 0
        self.bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
     #   self.ioloop = asyncio.get_event_loop()

    def start_checking(self):
        threading.Thread(target=self.check_loop).start()

    def check_loop(self):
        while True:
            self.motion_check()
            sleep(self.sleep_time)

    def motion_check(self):
        _, frame = self.cam.read()
        _, frame1 = self.cam.read()
        diff = cv2.absdiff(frame,frame1)
        gray = cv2.cvtColor(diff,cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh,None,iterations=3)
        contours,_= cv2.findContours(dilated,cv2.RETR_TREE,CHAIN_APPROX_SIMPLE)
#        cv2.drawContours(frame1,contours,-1,(0,255,0),2)
        motion = False
        for c in contours:
            if cv2.contourArea(c) < 3000:
                continue
#            x,y,w,h = cv2.boundingRect(c)
#            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
            motion = True
        if motion:
            impath = f'{PATH}/{time_ns()}.png'
            cv2.imwrite(impath,frame)
            self.send_telegram_notif(impath)

    def send_telegram_notif(self,impath):
        if self.last_message + TELEGRAM_COOLDOWN > time_ns():
            return

        self.last_message = time_ns()
        self.bot.send_photo(TELEGRAM_CHAT_ID,open(impath,'rb'),disable_notification=TELEGRAM_NOTIFICATION_SILENT)
