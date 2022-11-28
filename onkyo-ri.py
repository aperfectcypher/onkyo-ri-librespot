import pigpio
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
pi = pigpio.pi()
pi.set_mode(ONKYO_PIN, pigpio.OUTPUT)

def _create_header_wave():
    wf = []
    wf.append(pigpio.pulse(1 << ONKYO_PIN, 0, 3000))
    wf.append(pigpio.pulse(0, 1 << ONKYO_PIN, 1000))
    return wf

def _create_trailer_wave():
    wf = []
    wf.append(pigpio.pulse(1 << ONKYO_PIN, 0, 1000))
    wf.append(pigpio.pulse(0, 1 << ONKYO_PIN, 40000))
    return wf

def _create_command_wave(command):
    wf = []
    for x in range(0, 12):
        gap = 2000 if command & 2048 != 0 else 1000
        wf.append(pigpio.pulse(1 << ONKYO_PIN, 0, 1000))
        wf.append(pigpio.pulse(0, 1 << ONKYO_PIN, gap))
        command = command << 1
    return wf

def send(command):
    pi.wave_clear()

    wave_elements = _create_header_wave() + \
    _create_command_wave(command) + \
    _create_trailer_wave()

    pi.wave_add_generic(wave_elements)
    pi.wave_send_once(pi.wave_create())

    while pi.wave_tx_busy():
        time.sleep(0.1)


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
