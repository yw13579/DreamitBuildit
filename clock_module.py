import board
import adafruit_pcf8523
import bitbangio
import time

i2c = bitbangio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(i2c)

#rtc.datetime = time.struct_time(tm_year = 2021, tm_mon = 10, tm_mday = 16, tm_hour = 14, tm_min = 85, tm_sec = 25, tm_wday = 3, tm_yday = 259, tm_isdst = -1)
#t = time.struct_time((2021, 9, 16, 14, 11, 0, 0, -1, -1))
#rtc.datetime = t
#time.sleep(1)

def check_time():
    hour = rtc.datetime.tm_hour
    minu = rtc.datetime.tm_min

    return hour, minu

def read_time_on_sd():

    hour = 0
    minu = 0

    with open("/sd/alarm.txt", "r") as f:

        line1 = f.readline()
        print('clock:' + line1)
        line1 = line1.strip()
        line2 = f.readline()
        print('clock:' + line2)
        line2 = line2.strip()

        print("sd1:" + line1)
        print("sd2:" + line2)

    return line1, line2
