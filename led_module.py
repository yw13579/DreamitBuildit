import time
import board
from digitalio import DigitalInOut, Direction
from sam32lib import sam32

mosfet = DigitalInOut(board.D38)
mosfet.direction = Direction.OUTPUT
mosfet.value = False


def led_flicker():

    start_time = time.time()
    end_time = start_time+15

    while time.time() < end_time:
        mosfet.value = True
        time.sleep(0.05)
        mosfet.value = False
        time.sleep(0.05)
