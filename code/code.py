"""
DDS 2022 PumpkinBot Tutorial
"""

import board # needed for everything
import analogio # needed to read analog input
import digitalio # needed for audio

import time # needed for sleep
import neopixel # Needed for LEDs
import random # needed for debugging

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# Colors used by the LEDs
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
ORANGE = (255, 69, 0)
YELLOW = (255, 255, 0)
GOLD = (218, 165, 32)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)

# Setup for Neopixel LEDs
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.1, auto_write=True)
pixels.fill(BLACK)

# Setup analog input
analogin = analogio.AnalogIn(board.A6)

# distance variables
avgDistance = 0
triggerDistance = 0

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True
audio = AudioOut(board.SPEAKER)


def initial_setup():
    # global pixels
    pixels.fill(BLUE)
    updateDistance()
    pixels.fill(ORANGE)

# resets the distance calcs
def updateDistance():
    global avgDistance, triggerDistance

    pixels.fill(WHITE)

    rangeStore = []

    for i in range(10):
        rangeStore.append(getDistance(analogin))
        time.sleep(0.1)

    avgDistance = (rangeStore[0] + rangeStore[1] + rangeStore[2] + rangeStore[3] + rangeStore[4] + rangeStore[5] + rangeStore[6] + rangeStore[7] + rangeStore[8] + rangeStore[9]) / 10

    triggerDistance = (avgDistance / 4) * 3

    print("Average Distance (in): %f" % avgDistance)
    print("Trigger Distance (in): %f" % triggerDistance)

# seperate out the distance calc
def getDistance(pin):

    voltage = (pin.value * 3.3) / 65536

    return (voltage / 0.0064)

def sonicRead():
    global avgDistance, triggerDistance

    #print("Analog Voltage: %f" % getDistance(analogin))
    #print(triggerDistance)

    if float(getDistance(analogin)) <= float(triggerDistance):
        print("triggered")
        play_file()

    time.sleep(.1)

#play a random wav file
def play_file():


    choice = random.randint(1,4)
    if choice == 1:
        file = open("audio\s1.wav", "rb")
    elif choice == 2:
        file = open("audio\s2.wav", "rb")
    elif choice == 3:
        file = open("audio\s3.wav", "rb")
    else:
        file = open("audio\s4.wav", "rb")

    wave = WaveFile(file)
    audio.play(wave)

    for i in range(50):
        pixels.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        time.sleep(0.1)

    pixels.fill(ORANGE)

def main():
    initial_setup()
    while True:
        sonicRead()


if __name__ == "__main__":
    main()
