#Library Imports
import RPi.GPIO as GPIO
from time import sleep
#Script Imports
import blindStatus

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
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
  
  #Check current blind status
  currentStatus = blindStatus.checkStatus()
  print("Current Blind Status:")
  print(currentStatus)
  
  #Convert to ints
  currentStatus = int(currentStatus)
  hubRequeststr = int(hubRequeststr)
  
  #Convert request into intervals of 0.5
  hubRequestTime = (hubRequeststr * 0.5)
  
  if (currentStatus == hubRequeststr):
    #If current status = whats requested form hub, no movement nessecary
    print("Blinds Already At Current Level")
    
  elif (currentStatus < hubRequeststr):
    #If current status less than whats requested from hub, close appropraitely
    adjustBlinds = (currentStatus * 0.5)
    adjustBlindsTime = (hubRequestTime - adjustBlinds)
    #Debugging
    print("Closing blinds for ")
    print(adjustBlindsTime)
    print("Seconds")
    #Close Blinds
    closeStart(adjustBlindsTime)
    #Might fail here
    writeStatus(str(hubRequeststr))
    
  elif (currentStatus > hubRequeststr):
    #If current status greater than whats requested from hub, move appropraitely
    adjustBlinds = (currentStatus * 0.5)
    adjustBlindsTime = (adjustBlinds - hubRequestTime)
    #Debugging
    print("Openning blinds for ")
    print(adjustBlindsTime)
    print("Seconds")
    #Open Blinds
    openStart(adjustBlindsTime)
    writeStatus(str(hubRequeststr))

if __name__ == "__main__":
    main()