#Client 1

import socket
import RPi.GPIO as GPIO
import time

serverMACAddress = 'B8:27:EB:FC:C1:76' #Found from using hciconfig
port = 7
#s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
#s.connect((serverMACAddress, port))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)
while 1:
    while GPIO.input(37) == GPIO.HIGH:
        time.sleep(.01)
    print('detected light')
    text = "Hello"
    #s.send(bytes(text, 'UTF-8'))
    time.sleep(.5)
s.close()
GPIO.cleanup()
