import RPi.GPIO as GPIO
import os
import time

ONKYO_PIN = 23
EVENT_FIFO_NAME = "/opt/onkyo/event_fifo"
VOLUME_FIFO_NAME = "/opt/onkyo/volume_fifo"

## fifo setup
try:
    os.unlink(EVENT_FIFO_NAME)
    os.unlink(VOLUME_FIFO_NAME)
except (IOError, OSError):
    pass

os.mkfifo(EVENT_FIFO_NAME)
os.chmod(EVENT_FIFO_NAME, 0o777)
os.mkfifo(VOLUME_FIFO_NAME)
os.chmod(VOLUME_FIFO_NAME, 0o777)

## IO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ONKYO_PIN, GPIO.OUT)
def _send_header():
    GPIO.output(ONKYO_PIN, GPIO.HIGH)
    time.sleep(0.003)
    GPIO.output(ONKYO_PIN, GPIO.LOW)
    time.sleep(0.001)

def _send_trailer():
    GPIO.output(ONKYO_PIN, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(ONKYO_PIN, GPIO.LOW)
    time.sleep(0.020)

# Send the 12 LSB of the command parameter
# each bit duration is 1ms
def _send_command(command):
    for i in range(12):
        if command & (1 << i):
            GPIO.output(ONKYO_PIN, GPIO.HIGH)
        else:
            GPIO.output(ONKYO_PIN, GPIO.LOW)
        time.sleep(0.001)

def send(command):
    _send_header()
    _send_command(command)
    _send_trailer()


# program loop
with open(EVENT_FIFO_NAME, "r") as fifo:
    while True:
        event = fifo.read().strip()
        if len(event) == 0:
            time.sleep(0.1)
            continue
 
        print("Event received: " + event)

        if event == "started":
            send(0x02f) # trun on
            send(0x020) # set source to line1
            send(0x0d5) # next source (line2)
        #elif event == "playing":
        #    send(47)
        elif event == "stopped":
            send(0x0d6) # reset to line1
            send(0x0da) # turn off
        elif event == "volume_set":
            with open(VOLUME_FIFO_NAME, "r") as vol_fifo:
                vol = vol_fifo.read().strip()
                print("Volume set to: " + vol)
        #elif event == "paused":
