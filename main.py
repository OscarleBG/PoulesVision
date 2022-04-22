from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os
from button_actions import *

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)


#button commands:
DOOR_OPEN, DOOR_CLOSE, ALARM = "door-open","door-close","alarm"
COMMANDS = {
        'Open Door':DOOR_OPEN,
        'Close Door':DOOR_CLOSE,
        'Alarm':ALARM
}
COMMANDS_ACTIONS = {
        DOOR_OPEN:open_door,
        DOOR_CLOSE:close_door,
        ALARM:ring_alarm
}

@app.route('/')
def index():
    return render_template('index.html',commands=COMMANDS)

def gen(camera):
    #get camera frame
    while True:
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



