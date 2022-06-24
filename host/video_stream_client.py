import numpy as np
import threading as th
import imagezmq
from decouple import config


class VideoStreamClient:
    def __init__(self, frame_preprocessors=[]):
        self.frame = None
        self.new_frame = False
        self.frame_preprocessors = frame_preprocessors

        self.image_hub = imagezmq.ImageHub(open_port=f'tcp://*:{config("HOST_PORT")}')

        self.get_frame_loop_process = th.Thread(target=self.get_frame_loop)
        self.get_frame_loop_process.start()

    def get_frame_loop(self):
        while True:
            rpi_name, self.frame = self.image_hub.recv_image()
            self.frame = self.preprocess_frame(self.frame)
            self.new_frame = True
            self.image_hub.send_reply(b'OK')

    def get_frame(self) -> (bool, np.ndarray):
        new_frame = self.new_frame
        self.new_frame = False
        return new_frame, self.frame

    def preprocess_frame(self, frame):
        for f in self.frame_preprocessors:
            frame = f(frame)
        return frame
