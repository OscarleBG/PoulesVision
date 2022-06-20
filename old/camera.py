#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2
import imutils
import time
import numpy as np
from image_collection.mouvement_detection import MouvementDetector


class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = cv2.VideoCapture(0)
        self.flip = flip
        time.sleep(2.0)
        mouvement_detector = MouvementDetector(self.vs)
        mouvement_detector.start_checking()

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
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
