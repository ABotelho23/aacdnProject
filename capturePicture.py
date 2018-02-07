import picamera
from subprocess import call
from datetime import datetime
from time import sleep
from picamera import Color
import io 

def captureTestImage(fromserver):
##def main(fromServer):
#import P3picam

 
 
#motionState = False
    picPath = "/mnt/captures"
# File path
    filePath = "/mnt/captures/"
    picTotal = fromServer
    intpicTotal = int(picTotal)
    ##picCount = 0
    threshold = 10
    sensitivity = 20
    forceCapture = True
    #forceCaptureTime = 60 * 60 # Once an hour

# File settings
saveWidth = 1280
saveHeight = 960
diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk

# Capture a small test image (for motion detection)

    command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (100, 75)
    imageData = StringIO.StringIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer
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
