import RPi.GPIO as GPIO
from time import sleep

def closeStart():
  
  GPIO.setmode(GPIO.BOARD)

  Motor1A = 16
  Motor1B = 18
  Motor1E = 22

  GPIO.setup(Motor1A,GPIO.OUT)
  GPIO.setup(Motor1B,GPIO.OUT)
  GPIO.setup(Motor1E,GPIO.OUT)

  pwmtest = GPIO.PWM(Motor1E,100)

  print ("Closing Blinds...")
  GPIO.output(Motor1A,GPIO.HIGH)
  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor1E,GPIO.HIGH)

  pwmtest.start(2.5)

  sleep(3)

  print ("Stopping...")
  GPIO.output(Motor1E,GPIO.LOW)
  GPIO.cleanup()
  
  #Update Status File
  print ("Writting status to file")
  writePath = '/home/pi/BlindStatus.txt'
  statusFile = open(writePath, 'w')
  statusFile.write("CLOSED")
  statusFile.close()
  
if __name__ == "__main__":
    closeStart()
  
