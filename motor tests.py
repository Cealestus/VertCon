import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, intitial=GPIO.LOW)

GPIO.output(36, GPIO.HIGH)
time.sleep(.75)
GPIO.output(36, GPIO.LOW)
time.sleep(1)
GPIO.output(32, GPIO.HIGH)
time.sleep(.75)
GPIO.output(32, GPIO.LOW)

time.sleep(1)

GPIO.output(13, GPIO.HIGH)
time.sleep(.75)
GPIO.output(13, GPIO.LOW)
time.sleep(1)
GPIO.output(11, GPIO.HIGH)
time.sleep(.75)
GPIO.output(11, GPIO.LOW)

time.sleep(1)



GPIO.cleanup()
