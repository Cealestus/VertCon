import socket
import RPi.GPIO as GPIO
import threading
import time

#Set GPIO mode to use board pin numbers
GPIO.setmode(GPIO.BOARD)

#Setup the GPIO pins used to control the system
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.output(36, GPIO.LOW)
GPIO.output(38, GPIO.LOW)
GPIO.output(40, GPIO.LOW)

#Setup global variables to be used
currentLED = 1
counter1 = 0
ping1 = 0
counter2 = 0
ping2 = 0
counter3 = 0
ping3 = 0

#Setup locks for concurrency
lock = threading.Lock()
pinglock = threading.Lock()

#Thread for incrementing the last time a floor request was pinged
def pingCounters():
    global ping1
    global ping2
    global ping3
    while 1:
        time.sleep(1)
        ping1 = ping1 + 1
        ping2 = ping2 + 1
        ping3 = ping3 + 1

#Thread for reseting the counters based on the ping value
def resetCounters():
    global counter1
    global counter2
    global counter3
    while 1:
        time.sleep(1)
        pinglock.acquire()
        if ping1 > 30:
            lock.acquire()
            if counter1 > 0:
                print("Counter1 Value was: " + str(counter1))
            counter1 = 0
            lock.release()
        pinglock.release()
        pinglock.acquire()
        if ping2 > 30:
            lock.acquire()
            if counter2 > 0:
                print("Counter2 Value was: " + str(counter2))
            counter2 = 0
            lock.release()
        pinglock.release()
        pinglock.acquire()
        if ping3 > 30:
            lock.acquire()
            if counter3 > 0:
                print("Counter3 Value was: " + str(counter3))
            counter3 = 0
            lock.release()
        pinglock.release()

#Thread to cycle the IR LEDs based on the current floor-detection state
def cycle_LEDs():
    global currentLED
    while 1:
        if currentLED == 1:
            print("Setting Floor 1 LED")
            GPIO.output(33, GPIO.LOW)
            GPIO.output(35, GPIO.HIGH)
            GPIO.output(37, GPIO.HIGH)
        elif currentLED == 2:
            print("Setting Floor 2 LED")
            GPIO.output(33, GPIO.HIGH)
            GPIO.output(35, GPIO.LOW)
            GPIO.output(37, GPIO.HIGH)
        else:
            print("Setting Floor 3 LED")

            GPIO.output(33, GPIO.HIGH)
            GPIO.output(35, GPIO.HIGH)
            GPIO.output(37, GPIO.LOW)
        time.sleep(15)
        if currentLED < 3:
            currentLED = currentLED + 1
        else:
            currentLED = 1

#Thread for running the bluetooth reception and indication of pings
def runPrimary():
    hostMACAddress = 'B8:27:EB:FC:C1:76' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
    port = 7   # 3 is an arbitrary choice. However, it must match the port used by the client.  
    backlog = 1
    size = 1024
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((hostMACAddress,port))
    s.listen(backlog)
    global counter1
    global counter2
    global counter3
    global ping1
    global ping2
    global ping3
    try:
        client, address = s.accept()
        while 1:
            print("Waiting to receive data")
            data = client.recv(size)
            if data:
                if data.decode("UTF-8") == "Hello":
                    if currentLED == 1:
                        lock.acquire()
                        counter1 = counter1 + 1
                        lock.release()
                        pinglock.acquire()
                        ping1 = 0
                        pinglock.release()
                        print("Received Signal for Floor One")
                        client.send(data)
                    elif currentLED == 2:
                        lock.acquire()
                        counter2 = counter2 + 1
                        lock.release()
                        pinglock.acquire()
                        ping2 = 0
                        pinglock.release()
                        print("Received Signal for Floor Two")
                        client.send(data)
                    elif currentLED == 3:
                        lock.acquire()
                        counter3 = counter3 + 1
                        lock.release()
                        pinglock.acquire()
                        ping3 = 0
                        pinglock.release()
                        print("Received Signal for Floor 3")
                        client.send(data)
                else:
                    print("Something went wrong")
    except Exception as e:
        logger.error("Closing socket: " + str(e))
        client.close()
        s.close()

#Thread for selecting the floor based on the current counter values
def floorSelection():
    global counter1
    global counter2
    global counter3
    while 1:
        lock.acquire()
        if counter1 >= 20:
            GPIO.output(36, GPIO.HIGH)
            print("Floor Select: 1")
            counter1 = 0
        if counter2 >= 20:
            GPIO.output(38, GPIO.HIGH)
            print("Floor Select: 2")
            counter2 = 0
        if counter3 >= 20:
            GPIO.output(40, GPIO.HIGH)
            print("Floor Select: 3")
            counter3 = 0
        lock.release()
        time.sleep(2)

#Start the PWM for 10kHz, 50% duty cycle
p = GPIO.PWM(31, 10000)
p.start(50.0)

#Set up threads for each of the five subsystems
t1 = threading.Thread(target=cycle_LEDs)
t2 = threading.Thread(target=runPrimary)
t3 = threading.Thread(target=resetCounters)
t4 = threading.Thread(target=floorSelection)
t5 = threading.Thread(target=pingCounters)
t1.daemon = True
t2.daemon = True
t3.daemon = True
t4.daemon = True
t5.daemon = True

#Start the subsystems
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
