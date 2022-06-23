import socket, pickle, struct

import numpy as np
from decouple import config
import threading as th


class VideoStreamClient:
    def __init__(self):
        self.frame = None
        self.new_frame = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((config('HOST_IP'), config('SOCKET_PORT', cast=int)))

        self.data = b''
        self.payload_size = struct.calcsize('!I')

        self.get_frame_thread = th.Thread(target=self.get_frame_loop)
        self.get_frame_thread.start()

    def get_frame_loop(self):
        while True:
            while len(self.data) < self.payload_size:
                self.data += self.client_socket.recv(4096)
            packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            msg_size = struct.unpack('!I', packed_msg_size)[0]

            while len(self.data) < msg_size:
                self.data += self.client_socket.recv(4096)
            frame_data = self.data[:msg_size]
            self.data = self.data[msg_size:]
            self.frame = pickle.loads(frame_data)
            self.new_frame = True

    def get_frame(self) -> (bool, np.ndarray):
        new_frame = self.new_frame
        self.new_frame = False
        return new_frame, self.frame
