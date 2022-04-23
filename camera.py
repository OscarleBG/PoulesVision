#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2
import imutils
import time
import numpy as np
import importlib.machinery

loader = importlib.machinery.SourceFileLoader('report', '/home/pi/image-collection/mouvement_detection.py')
mouvement_detection = loader.load_module('report')

IMAGE_PROCESSOR = mouvement_detection.draw_mouvement

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = cv2.VideoCapture(0)
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        success = False
        while not success:
            success, frame = self.vs.read()
        #frame = self.flip_if_needed(frame)
        if(IMAGE_PROCESSOR):
            frame = IMAGE_PROCESSOR(frame,self.vs)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
