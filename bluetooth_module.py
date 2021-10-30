import time
import busio
import board
from digitalio import DigitalInOut
from adafruit_bluefruitspi import BluefruitSPI
from sam32lib import sam32

ADVERT_NAME = b'wakeup'

#spi_bus = busio.SPI(sam32._spi, MOSI=board.MOSI, MISO=board.MISO)
# above is commented out twice
cs = DigitalInOut(board.D35)
irq = DigitalInOut(board.D36)
rst = DigitalInOut(board.D37)
bluefruit = BluefruitSPI(sam32._spi, cs, irq, rst, debug=False)

def init_bluefruit():
    # Initialize the device and perform a factory reset
    print("Initializing the Bluefruit LE SPI Friend module")
    bluefruit.init()
    bluefruit.command_check_OK(b'AT+FACTORYRESET', delay=1)
    # Print the response to 'ATI' (info request) as a string
    print(str(bluefruit.command_check_OK(b'ATI'), 'utf-8'))
    # Change advertised name
    bluefruit.command_check_OK(b'AT+GAPDEVNAME='+ADVERT_NAME)

def wait_for_connection():
    print("Waiting for a connection to Bluefruit LE Connect ...")
    # Wait for a connection ...
    dotcount = 0
    while not bluefruit.connected:
        print(".", end="")
        dotcount = (dotcount + 1) % 80
        if dotcount == 79:
            print("")
        time.sleep(0.5)

# This code will check the connection but only query the module if it has been
# at least 'n_sec' seconds. Otherwise it 'caches' the response, to keep from
# hogging the Bluefruit connection with constant queries
connection_timestamp = None
is_connected = None
def check_connection(n_sec):
    # pylint: disable=global-statement
    global connection_timestamp, is_connected
    if (not connection_timestamp) or (time.monotonic() - connection_timestamp > n_sec):
        connection_timestamp = time.monotonic()
        is_connected = bluefruit.connected
    return is_connected

def parse_and_store_alarm(resp):
    print(resp)

    with open("/sd/alarm.txt", "w") as f:
        f.write(resp[0:2]+'\n')
        f.write(resp[2:4]+'\n')



def alarm(sleep_in_mins):
    current_time = time.time()
    target_time = current_time + sleep_in_mins*60

    return target_time

#while time.time() <= target_time:



# Unlike most circuitpython code, this runs in two loops
# one outer loop manages reconnecting bluetooth if we lose connection
# then one inner loop for doing what we want when connected!
