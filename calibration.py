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

def main():
    while 1:
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

      function = input("Open(o) or Close(c)?")
      value = input("What Amount?")

      #Convert to int
      value = int(value)

      #Convert request into intervals of 0.5
      if(function == 'o'):
          print("Openning blinds for ")
          print(value)
          print("Seconds")
          #Open Blinds
          openStart(value)
      elif(function == 'c'):
          print("Closing blinds for ")
          print(value)
          print("Seconds")
          #Open Blinds
          closeStart(value)
      else:
          print("Invalid Option")

if __name__ == "__main__":
    main()
