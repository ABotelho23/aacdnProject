import RPi.GPIO as GPIO

def testOn():
  
  GPIO.setmode(GPIO.BCM)
  
  RUNNING = True
  
  RED = 17
  GREEN = 18
  BLUE = 27
  
  GPIO.setup(RED,GPIO.OUT)
  GPIO.setup(GREEN,GPIO.OUT)
  GPIO.setup(BLUE,GPIO.OUT)
  
  Freq = 100
  
  red = GPIO.PWN(RED, Freq)
  green = GPIO.PWN(GREEN, Freq)
  blue = GPIO.PWN(BLUE, Freq)
  
  try:
    while RUNNING:
      red.start(1)
      green.start(100)
      blue.start(100)
        
        for x in range(1,101):
          red.ChangeDutyCycle(101-x)
          
          time.sleep(0.05)
        for x in range(1,101):
          green.ChangeDutyCycle(101-x)
          blue.ChangeDutyCycle(x)
          time.sleep(0.025)
        for x in range (1,101):
          red.ChangeDutyCycle(x)
          time.sleep(0.025)
          
  except KeyboardInterrupt:
  RUNNING = False
  GPIO.cleanup()
          

  
 
  
if __name__ == "__main__":
  testOn()
