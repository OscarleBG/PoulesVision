from socket import gethostname
from time import sleep
from decouple import config
from imagezmq import ImageSender
from imutils.video import VideoStream


def main():
    sender = ImageSender(connect_to=f'tcp://{config("HOST_IP")}:{config("HOST_PORT")}')
    rpi_name = gethostname()
    picam = VideoStream(
        resolution=(config("IMAGE_WIDTH"), config("IMAGE_HEIGHT"))
    ).start()
    sleep(2)

    while True:
        image = picam.read()
        sender.send_image(rpi_name, image)


if __name__ == "__main__":
    main()
