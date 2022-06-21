import socket, cv2, pickle, struct
from decouple import config

HOST_IP = config('HOST_IP')
PORT = config('SOCKET_PORT', cast=int)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, PORT))

data = b''
payload_size = struct.calcsize('!I')

while True:
    while len(data) < payload_size:
        data += client_socket.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack('!I', packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow('Received video stream', frame)
    cv2.waitKey(1)
    # print(frame)