#Client 1

import socket
import RPi.GPIO as GPIO
import time
import datetime

serverMACAddress = 'B8:27:EB:7C:B2:22' #Found from using hciconfig
port = 7
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress, port))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)
GPIO.setup(35, GPIO.IN)
GPIO.setup(33, GPIO.IN)
GPIO.setup(31, GPIO.IN)
while 1:
    while GPIO.input(37) == GPIO.HIGH and GPIO.input(35) == GPIO.HIGH and GPIO.input(33) == GPIO.HIGH and GPIO.input(31) == GPIO.HIGH:
        time.sleep(.01)
    print('detected light' + str(datetime.datetime.now().time()))
    text = "Hello"
    s.send(bytes(text, 'UTF-8'))
    time.sleep(.5)
s.close()
GPIO.cleanup()
