#Library Imports
import RPi.GPIO as GPIO
from time import sleep
#Script Imports
import blindStatus

#Motor Variables for easier management
GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

#Amount of time to fully open/close
fullTime = 5
#Step incrememter 
stepCounter = 10
#Adjust time accordinly
finalTime = 0

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
  
def main(fromServer):
  
  GPIO.setmode(GPIO.BOARD)

  Motor1A = 16
  Motor1B = 18
  Motor1E = 22

  GPIO.setup(Motor1A,GPIO.OUT)
  GPIO.setup(Motor1B,GPIO.OUT)
  GPIO.setup(Motor1E,GPIO.OUT)

  #Amount of time to fully open/close
  fullTime = 5
  #Step incrememter 
  stepCounter = 10
  #Adjust time accordinly
  finalTime = 0

  pwmtest = GPIO.PWM(Motor1E,100)

  #Check what is the argument
  print(fromServer)
  if (fromServer == '0'):
    openStart(fullTime)
    writeStatus(fromServer)
  elif (fromServer == '10'):
    closeStart(fullTime)
    writeStatus(fromServer)

if __name__ == "__main__":
    main()
