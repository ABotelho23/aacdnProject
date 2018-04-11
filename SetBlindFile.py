#Library Imports
import RPi.GPIO as GPIO
from time import sleep
import blindStatus

def main():

    setBlind = input("Enter Value...")
    blindStatus.writeStatus(str(setBlind))

if __name__ == "__main__":
    main()
