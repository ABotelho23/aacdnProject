#Library Imports
import RPi.GPIO as GPIO
from time import sleep

def writeStatus(num):

  #Update Status File
  print ("Writting status to file")
  writePath = '/home/pi/BlindStatus.txt'
  statusFile = open(writePath, 'w')
  statusFile.write(num)
  statusFile.close()

def main():

    setBlind = input("Enter Value...")
    writeStatus(str(setBlind))

if __name__ == "__main__":
    main()
