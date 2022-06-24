import numpy as np
import multiprocessing as mp
import imagezmq
from decouple import config


class VideoStreamClient:
    def __init__(self):
        (self.frame, self.frame_pipe) = mp.Pipe(False)

        self.image_hub = imagezmq.ImageHub(open_port=f'tcp://*:{config("HOST_PORT")}')

        self.get_frame_loop_process = mp.Process(target=self.get_frame_loop)
        self.get_frame_loop_process.start()

    def get_frame_loop(self):
        while True:
            rpi_name, frame = self.image_hub.recv_image()
            self.image_hub.send_reply(b"K")
            self.frame_pipe.send(frame)

    def get_frame(self) -> np.ndarray:
        self.frame.poll(None)
        return self.frame.recv()
