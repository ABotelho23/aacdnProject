import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RED = 17
GREEN = 18
BLUE = 27

GPIO.setup(RED,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.output(RED,False)
GPIO.output(GREEN,False)
GPIO.output(BLUE,False)

try:         
    while True:
        UserInput = raw_input()
	UserInput = str(UserInput)
        if UserInput == "red":
            GPIO.output(RED, True)
            GPIO.output(GREEN, False)
            GPIO.output(BLUE, False)
        elif UserInput == "green":
            GPIO.output(RED, False)
            GPIO.output(GREEN, True)
            GPIO.output(BLUE, False)
        elif UserInput == "blue":
            GPIO.output(RED, False)
            GPIO.output(GREEN, False)
            GPIO.output(BLUE, True)
	else:
		print("Only red, green, and blue are valid colors.")

except KeyboardInterrupt:
        GPIO.cleanup()
