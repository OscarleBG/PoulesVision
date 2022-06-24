# from gpiozero import Buzzer

# bip = Buzzer(26)

# button commands:
DOOR_OPEN, DOOR_CLOSE, ALARM = "door-open", "door-close", "alarm"
BUTTON_COMMANDS = [
    ("Open Door", DOOR_OPEN, "primary"),
    ("Close Door", DOOR_CLOSE, "primary"),
    ("Alarm", ALARM, "danger"),
]
COMMANDS_ACTIONS = {DOOR_OPEN: open_door, DOOR_CLOSE: close_door, ALARM: ring_alarm}

def open_door():
    print("door opened")


def close_door():
    print("door closed")


def ring_alarm():
    pass
