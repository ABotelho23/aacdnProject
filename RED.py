import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RED = 17
GREEN = 18
BLUE = 27

GPIO.setup(RED,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(BLUE,GPIO.OUT)

"""try:
        while(True):
                request = input("RGB ->")
                if (len(request) == 3):
                        GPIO.output(RED,int(request[0]))
                        GPIO.output(GREEN,int(request[1]))
                        GPIO.output(BLUE,int(request[2]))"""
try:
        while(True)
                flub = input("Will turn RED on any input")
                GPIO.output(RED,0)

except KeyboardInterrupt:
        GPIO.cleanup()
