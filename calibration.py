#Library Imports
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
#pwmtest = GPIO.PWM(Motor1E,1000)

def openStart(time):

  print ("Opening Blinds...")
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor1B,GPIO.HIGH)
  GPIO.output(Motor1E,GPIO.HIGH)

  #pwmtest.start(100)

  sleep(time)

  print ("Stopping...")
  GPIO.output(Motor1E,GPIO.LOW)
  GPIO.cleanup()

def closeStart(time):

  print ("Closing Blinds...")
  GPIO.output(Motor1A,GPIO.HIGH)
  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor1E,GPIO.HIGH)

  #pwmtest.start(100)

  sleep(time)

  print ("Stopping...")
  GPIO.output(Motor1E,GPIO.LOW)
  GPIO.cleanup()

def main(fromServer):
  # Step incrememter
  # 0 = fully open
  # 10 = full closed

  GPIO.setmode(GPIO.BOARD)

  Motor1A = 16
  Motor1B = 18
  Motor1E = 22

  GPIO.setup(Motor1A,GPIO.OUT)
  GPIO.setup(Motor1B,GPIO.OUT)
  GPIO.setup(Motor1E,GPIO.OUT)

  #Amount of time to fully open/close = 5 Seconds
  fullTime = 5

  pwmtest = GPIO.PWM(Motor1E,100)

  #Check what is the argument
  hubRequeststr = fromServer
  print("Request from Server:")
  print(hubRequeststr)

  hubRequeststr = int(hubRequeststr)

  #Convert request into intervals of 0.5
  hubRequestTime = (hubRequeststr * 1)

  print("Openning blinds for ")
  print(hubRequestTime)
  print("Seconds")
  #Open Blinds
  openStart(hubRequestTime)

if __name__ == "__main__":
    main()