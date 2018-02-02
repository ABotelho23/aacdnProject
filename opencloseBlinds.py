#Library Imports
import RPi.GPIO as GPIO
from time import sleep
#Script Imports
import blindStatus

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
  #5 Seconds
  fullTime = 5
  
  #Step incrememter 
  # 1 = fully open
  # 11 = full closed
  stepCounter = 11

  pwmtest = GPIO.PWM(Motor1E,100)

  #Check what is the argument
  hubRequeststr = fromServer
  print(hubRequeststr)
  
  #Check current blind status
  currentStatus = blindStatus.checkStatus()
  
  #Convert to ints
  currentStatus = int(currentStatus)
  hubRequeststr = int(hubRequeststr)
  
  if (currentStatus == hubRequeststr):
    #If current status = whats requested form hub, no movement nessecary
    print("Blinds Already At Current Level")
    
  elif (currentStatus < hubRequeststr):
    #If current status less than whats requested from hub, close appropraitely
    adjustBlinds = (((hubRequeststr - currentStatus)/stepCounter)* fullTime)
    #Debugging
    print("Closing blinds for " % adjustBlinds % " seconds")
    #Close Blinds
    closeStart(adjustBlinds)
    writeStatus(hubRequeststr)
    
  elif (currentStatus > hubRequeststr):
    #If current status greater than whats requested from hub, move appropraitely
    adjustBlinds = (((currentStatus - hubRequeststr)/stepCounter)* fullTime)
    #Debugging
    print("Openning blinds for " % adjustBlinds % " seconds")
    #Open Blinds
    openStart(adjustBlinds)
    writeStatus(hubRequeststr)

if __name__ == "__main__":
    main()
