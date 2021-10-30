import time
import board
import clock_module
import adafruit_pcf8523
import bitbangio
import servo_module
import pwmio
from adafruit_motor import servo
import light_module
import neopixel
from digitalio import DigitalInOut
from sam32lib import sam32


from adafruit_bluefruitspi import BluefruitSPI
import busio

#clock_module
#i2c = bitbangio.I2C(board.SCL, board.SDA)
#rtc = adafruit_pcf8523.PCF8523(i2c)

#light_module
#pixels = neopixel.NeoPixel(board.D41, 8, pixel_order = neopixel.RGB)#
#pixels.auto_write = False

#bluetooth_module
ADVERT_NAME = b'wakeup'

#spi_bus = busio.SPI(sam32._spi, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.D35)
irq = DigitalInOut(board.D36)
rst = DigitalInOut(board.D37)
bluefruit = BluefruitSPI(sam32._spi, cs, irq, rst, debug=False)

connection_timestamp = None
is_connected = None

#servo_module
#pwm = pwmio.PWMOut(board.D60, duty_cycle=2 ** 15, frequency=50)
#my_servo = servo.Servo(pwm)

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
        resp = resp.strip()
        print('first two chars' + str(resp[0:2]) + str(len(resp[0:2])))
        f.write(resp[0:2]+'\n')
        print('second two chars' + str(resp[2:4]) + str(len(resp[2:4])))
        f.write(resp[2:4] +'\n')


while True:
    # Initialize the module
    try:        # Wireless connections can have corrupt data or other runtime failures
                # This try block will reset the module if that happens
        init_bluefruit()
        wait_for_connection()
        print("\n *Connected!*")

        # Once connected, check for incoming BLE UART data
        while check_connection(3):  # Check our connection status every 3 seconds
            # OK we're still connected, see if we have any data waiting
            #resp = bluefruit.read_packet()
            resp = bluefruit.uart_rx()
            if not resp:
                continue  # nothin'
            print("alarm_time", resp)
            print(resp)
            # Look for a 'C'olor packet
            #if resp[0] != 'C':
            #    continue
            # Set the neopixels to the three bytes in the packet
            print("hello")
            parse_and_store_alarm(resp)

            current_hour, current_minu = clock_module.check_time()
            target_hour, target_minu = clock_module.read_time_on_sd()

            time.sleep(3)

            while True:

                time.sleep(1)

                #value = (target_hour == str(current_hour))
                #print("boolean:" + str(value))

                #value1 = type(current_hour)
                #value2 = type(target_hour)

                #print(len(str(current_hour)))
                #print(len(target_hour))


                #print(value1)
                #print(value2)


                current_hour, current_minu = clock_module.check_time()
                print(str(current_minu))
                print(target_minu)
                print(str(current_hour))
                print(target_hour)
                time.sleep(5)

                if current_hour == int(target_hour) and current_minu == int(target_minu):
                    print('condition met')
                    #light_module.flicker()
                    servo_module.servo_turn()

            #print("alarm time writen")
        print("Connection lost.")

    except RuntimeError as e:
        print(e)  # Print what happened
        continue  # retry!


