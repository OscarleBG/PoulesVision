import cv2
import numpy as np
from decouple import config
import threading as th
import imagezmq


class VideoStreamClient:
    def __init__(self):
        self.frame = None
        self.new_frame = False

        self.image_hub = imagezmq.ImageHub()

        self.get_frame_thread = th.Thread(target=self.get_frame_loop)
        self.get_frame_thread.start()

    def get_frame_loop(self):
        while True:
            rpi_name, self.frame = self.image_hub.recv_image()
            self.image_hub.send_reply(b'K')
            self.new_frame = True


def get_frame(self) -> (bool, np.ndarray):
    new_frame = self.new_frame
    self.new_frame = False
    return new_frame, self.frame
