import picamera
from subprocess import call
from datetime import datetime
from time import sleep
from picamera import Color
import io 
#import P3picam

 
def main(fromServer): 
#motionState = False
    picPath = "/mnt/captures/"
 
# File path
    filePath = "/mnt/captures/"
    picTotal = fromServer
    intpicTotal = int(picTotal)
    picCount = 0
    
    #Current time
while picCount < intpicTotal:
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
      
      
 """"
while True:
    motionState = p3picamera.motion()
    print(motionState)
    if motionState:
        cTime = getTime()
        picName = captureImage(cTime, picPath)
        timeStamp(currentTime, picPath, picName)
 """
    picCount += 1
    sleep(3)
