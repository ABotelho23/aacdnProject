import RPi.GPIO as GPIO

import time

import turnOn
import turnOff
import RED
import BLUE
import GREEN
import YELLOW
import CYAN
import MAGENTA
import WHITE

def rainbowOn():

        turnOn.lightOn()
        time.sleep(0.5)
        RED.redOn()
        time.sleep(0.5)
        GREEN.greenOn()
        time.sleep(0.5)
        BLUE.blueOn()
        time.sleep(0.5)
        YELLOW.yellowOn()
        time.sleep(0.5)
        CYAN.cyanOn()
        time.sleep(0.5)
        MAGENTA.magentaOn()
        time.sleep(0.5)
        WHITE.whiteOn()
 
 if __name__ == "__main__":
  rainbowOn()
