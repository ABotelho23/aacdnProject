import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RED = 17
GREEN = 18
BLUE = 27

GPIO.setup(RED,GPIO.OUT)
GPIO.output(RED,0)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.output(GREEN,0)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.output(BLUE,0)

try:
        while(True):
                request = input("RGB ->")
                if (len(request) == 3):
                        GPIO.output(RED,int(request[0]))
                        GPIO.output(GREEN,int(request[1]))
                        GPIO.output(BLUE,int(request[2]))

except KeyboardInterrupt:
        GPIO.cleanup()
