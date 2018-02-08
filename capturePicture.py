
import picamera
import picammotion
from subprocess import call
from datetime import datetime
from time import sleep
from picamera import Color
 
 
def main(fromServer):
 # File path
   filePath = "/mnt/captures/"
   picTotal = fromServer
   intpicTotal = int(picTotal)
   picCount = 0
 
   while picCount < intpicTotal:
     #Current time
      cTime = datetime.now()
     
      picT = cTime.strftime("%Y-%m-%d %H:%M:%S")
     # picName = cTime + '.jpg'
      picName = picT + '.jpg'
      FilePathPic = filePath + picName
      
   while True:
    motionState = picammotion.motion()
    print(motionState)
    if motionState:
        currentTime = getTime()  
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
   sleep(3)

"""
import picamera
from subprocess import call
from datetime import datetime
from time import sleep
from picamera import Color
import io 
#import P3picam

 

motionState = False
picPath = "/mnt/captures"
 
def main(fromServer):  
# File path
  filePath = "/mnt/captures/"
  picTotal = fromServer
  intpicTotal = int(picTotal)
  picCount = 0
   
while picCount < intpicTotal:
  #Current time
  cTime = datetime.now()
  
  picT = cTime.strftime("%Y-%m-%d %H:%M:%S")
  picName = picT + '.jpg'
  FilePathPic = filePath + picName

  # Take picture
  with picamera.PiCamera() as camera:
    camera.resolution = (1280,720)
     
      #Timestamp
    camera.annotate_foreground = Color('black')
    camera.annotate_background = Color('white')
    camera.annotate_text = picT
    camera.capture(FilePathPic)
    print("picture taken.")
      
      

while True:
    motionState = p3picamera.motion()
    print(motionState)
    if motionState:
        cTime = getTime()
        picName = captureImage(cTime, picPath)
        timeStamp(currentTime, picPath, picName)

picCount += 1
sleep(3)
"""
