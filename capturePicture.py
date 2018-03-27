
import picamera
import picammotion
from subprocess import call
from datetime import datetime
from datetime import timedelta
from time import sleep
from picamera import Color


def main(fromServer):
    # File path
    filePath = "/mnt/captures/pictures/"
    picTotal = fromServer
    intpicTotal = int(picTotal)
    picCount = 0

    #Current time
    cTime = datetime.now()
    dTime = cTime + timedelta(seconds=intpicTotal)
    
    while picCount < intpicTotal:

        cTime = datetime.now()
        picT = cTime.strftime("%Y-%m-%d %H-%M-%S")
        # picName = cTime + '.jpg'
        picName = picT + '.jpg'
        FilePathPic = filePath + picName
        
        #motionState = picammotion.motion()
        #print(motionState)
        #if motionState:
            # Take picture
        with picamera.PiCamera() as camera:
            camera.resolution = (1280,720)

            #Timestamp
            #camera.annotate = 700+650
            camera.annotate_foreground = Color('black')
            camera.annotate_background = Color('white')
            camera.annotate_text = picT
            camera.capture(FilePathPic)
            print("picture taken.")

            picCount += 1
            sleep(2)


