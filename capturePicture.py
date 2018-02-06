import picamera
from subprocess import call
from datetime import datetime
from time import sleep
from picamera import Color

#import P3picam
import picamera



motionState = False
picPath = "/mnt/captures"

def captureImage(currentTime, picPath):
    # Generate the picture's name
    picName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picPath + picName)
    print("We have taken a picture.")
    return picName

def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime

def timeStamp(currentTime, picPath, picName):
    # Variable for file path
    filepath = picPath + picName
    # Create message to stamp on picture
    message = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    # Create command to execute
    timestampCommand = "/usr/bin/convert " + filepath + " -pointsize 36 \
    -fill red -annotate +700+650 '" + message + "' " + filepath
    # Execute the command
    call([timestampCommand], shell=True)
    print("We have timestamped our picture.")

while True:
    motionState = picamera.motion()
    print(motionState)
    if motionState:
        currentTime = getTime()
        picName = captureImage(currentTime, picPath)
        timeStamp(currentTime, picPath, picName)

#def main(fromServer):
# File path
  #filePath = "/mnt/captures/"
  #picTotal = fromServer
  #intpicTotal = int(picTotal)
  #picCount = 0

  #while picCount < intpicTotal:
    #Current time
    #cTime = datetime.now()
   
    #picT = cTime.strftime("%Y-%m-%d %H:%M:%S")
    #picName = picT + '.jpg'
   #FilePathPic = filePath + picName

    # Take picture
    #with picamera.PiCamera() as camera:
      #camera.resolution = (1280,720)
     
      #Timestamp
      #camera.annotate = 700+650
      #camera.annotate_foreground = Color('black')
      #camera.annotate_background = Color('white')
      #camera.annotate_text = picT
      #camera.capture(FilePathPic)
      #print("picture taken.")

    #picCount += 1
    #sleep(3)
