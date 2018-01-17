import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RED = 17
GREEN = 18
BLUE = 27

GPIO.setup(RED,GPIO.OUT)
GPIO.output(RED,GPIO.LOW)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.output(GREEN,GPIO.HIGH)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.output(BLUE,GPIO.HIGH)

except KeyboardInterrupt:
        GPIO.cleanup()
