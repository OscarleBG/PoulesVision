from gpiozero import Buzzer

bip = Buzzer(26)

def open_door():
    print("door opened")


def close_door():
    print("door closed")


def ring_alarm():
    bip.beep(on_time=0.01,off_time=0.1,n=2)
