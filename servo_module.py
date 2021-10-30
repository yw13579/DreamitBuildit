import time
import board
import pwmio
from adafruit_motor import servo

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.D60, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

def servo_turn():

    for i in range(10):

        my_servo.angle = 90
        time.sleep(0.4)
        my_servo.angle = 0
        time.sleep(0.4)

