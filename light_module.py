import time
import board
import neopixel
from digitalio import DigitalInOut
from sam32lib import sam32

light_warning = {1: (50, 50, 50), 'two': 2, 'three': 3}

def light_up(snooze):
    for i in range(7): # to be updated with
        pixels[i] = (50, 50, 50) #to be updated with corresponding value with snooze

    pixels.show()

def light_off():
    for i in range(7):
        pixels[i] = (0, 0, 0)
    pixels.show()


def flicker():
    start_time = time.time()
    end_time = start_time+15
    while time.time() < end_time:

        light_off()
        time.sleep(0.1)
        light_up(1)
        time.sleep(0.1)

pixels = neopixel.NeoPixel(board.D41, 8, pixel_order = neopixel.RGB)
pixels.auto_write = False

alarm_time = 1 # input, should match alarm

#light_up(1)
#light_off()
#flicker()
#print(light_warning[1])
