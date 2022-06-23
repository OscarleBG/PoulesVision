import socket, cv2, pickle, struct, imutils
from decouple import config

PORT = config('SOCKET_PORT',cast=int)
IMAGE_WIDTH = config('IMAGE_WIDTH',cast=int)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = config('HOST_IP')
host_ip = socket.gethostbyname(hostname)

print(f'[+] Server IP: {host_ip}')

socket_address = (host_ip, PORT)
server_socket.bind(socket_address)
server_socket.listen()

print(f'[+] Listening on {host_ip}:{PORT}')

while True:

    client_socket, client_address = server_socket.accept()

    print(f'[+] Accepted connection from {client_address}')

    if client_socket:

        video_stream = cv2.VideoCapture(0)

        while video_stream.isOpened():
            ret, frame = video_stream.read()
            if not ret:
                continue

            frame = imutils.resize(frame, width=IMAGE_WIDTH)
            frame = pickle.dumps(frame)
            frame_size = len(frame)
            try:
                client_socket.send(struct.pack('!I', frame_size))
                client_socket.send(frame)
            except BrokenPipeError or ConnectionResetError as e:
                print('[-] Client disconnected')
                break
