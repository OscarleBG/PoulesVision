from time import sleep
from decouple import config
from imagezmq import ImageSender
from imutils.video import VideoStream


def main():
    sender = ImageSender(connect_to=f'tcp://{config("HOST_IP")}:{config("HOST_PORT")}')
    resolution = (config("IMAGE_WIDTH"), config("IMAGE_HEIGHT"))

    picam = VideoStream(resolution=resolution).start()

    sleep(2)

    while True:
        sender.send_image('', picam.read())


if __name__ == "__main__":
    main()
