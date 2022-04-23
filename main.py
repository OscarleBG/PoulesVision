from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os
from button_actions import *

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

FPS_LIMIT = 5

#button commands:
DOOR_OPEN, DOOR_CLOSE, ALARM = "door-open","door-close","alarm"
# triplet list: (label, value, type from bootstrap)
BUTTON_COMMANDS = [
        ('Open Door',DOOR_OPEN,'primary'),
        ('Close Door',DOOR_CLOSE,'primary'),
        ('Alarm',ALARM,'danger'),
]
COMMANDS_ACTIONS = {
        DOOR_OPEN:open_door,
        DOOR_CLOSE:close_door,
        ALARM:ring_alarm
}

@app.route('/')
def index():
    return render_template('index.html',commands=BUTTON_COMMANDS)

def gen(camera):
    #get camera frame
    sleep_time = 1/ FPS_LIMIT
    while True:
        time.sleep(sleep_time)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera), mimetype='multipart/x-mixed-replace; boundary=frame')


#Button commands
@app.route('/<cmd>')
def command(cmd=None):
    COMMANDS_ACTIONS.get(cmd,lambda:None)()
    return 'OK', 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)


def create_app():
   return app
