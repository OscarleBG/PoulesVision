import time
from flask import Flask, render_template, Response
from button_actions import *
from TensorflowBoxDrawer import BoxDrawer
from VideoStreamClient import VideoStreamClient
import cv2
from decouple import config

app = Flask(__name__)

pi_camera = VideoStreamClient()
box_drawer = BoxDrawer()
FRAME_PREPROCESSORS = [
    # box_drawer.draw_boxes
]

# button commands:
DOOR_OPEN, DOOR_CLOSE, ALARM = "door-open", "door-close", "alarm"
BUTTON_COMMANDS = [
    ('Open Door', DOOR_OPEN, 'primary'),
    ('Close Door', DOOR_CLOSE, 'primary'),
    ('Alarm', ALARM, 'danger'),
]
COMMANDS_ACTIONS = {
    DOOR_OPEN: open_door,
    DOOR_CLOSE: close_door,
    ALARM: ring_alarm
}


@app.route('/')
def index():
    return render_template('index.html', commands=BUTTON_COMMANDS)


def preprocess_frame(frame):
    for f in FRAME_PREPROCESSORS:
        frame = f(frame)
    return frame


def gen(camera):
    fps_limit = config('FPS_LIMIT', cast=int)
    sleep_time = 1 / fps_limit
    while True:
        if fps_limit > 0:
            time.sleep(sleep_time)
        frame = camera.get_frame()
        frame = preprocess_frame(frame)
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera), mimetype='multipart/x-mixed-replace; boundary=frame')


# Button commands
@app.route('/<cmd>')
def command(cmd=None):
    COMMANDS_ACTIONS.get(cmd, lambda: None)()
    return 'OK', 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=80)


def create_app():
    return app
