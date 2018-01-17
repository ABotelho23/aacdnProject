import RPi.GPIO as GPIO
import sys

from time import sleep

#Motor Variables for easier management
Motor1A = 16
Motor1B = 18
Motor1E = 22

#Amount of time to fully open/close
fullTime = 5
#Step incrememter 
stepCounter = 10
#What user sent
movement = sys.argv[1]
#Adjust time accordinly
finalTime = 0

GPIO.setmode(GPIO.BOARD)

pwmtest = GPIO.PWM(Motor1E,100)

def openStart(time):

  print ("Opening Blinds...")
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor1B,GPIO.HIGH)
  GPIO.output(Motor1E,GPIO.HIGH)

  pwmtest.start(2.5)

  sleep(time)

  print ("Stopping...")
  GPIO.output(Motor1E,GPIO.LOW)
  GPIO.cleanup()

def closeStart(time):

  print ("Closing Blinds...")
  GPIO.output(Motor1A,GPIO.HIGH)
  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor1E,GPIO.HIGH)

  pwmtest.start(2.5)

  sleep(time)

  print ("Stopping...")
  GPIO.output(Motor1E,GPIO.LOW)
  GPIO.cleanup()
  
def writeStatus(num):

  #Update Status File
  print ("Writting status to file")
  writePath = '/home/pi/BlindStatus.txt'
  statusFile = open(writePath, 'w')
  statusFile.write(num)
  statusFile.close()
  
def main():

  #Check what is the argument
  print(movement)
  if (movement == '0'):
    openStart(fullTime)
    writeStatus(movement)
  elif (movement == '10'):
    closeStart(fullTime)
    writeStatus(movement)


if __name__ == "__main__":
    main()