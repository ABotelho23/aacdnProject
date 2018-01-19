import picamera
from subprocess import call
from datetime import datetime
from time import sleep


def main():
# File path
  filePath = "/mnt/captures/"
  picTotal = 3
  picCount = 0

  while picCount < picTotal:
    # Grab the current time
    cTime = datetime.now()
   
    picT = cTime.strftime("%Y.%m.%d-%H%M%S")
    picName = picT + '.jpg'
    FilePathPic = filePath + picName

    # Take picture
    with picamera.PiCamera() as camera:
      camera.resolution = (1280,720)
      camera.capture(FilePathPic)
          print("picture taken.")

    #currenttime variable
    timestampMessage = cTime.strftime("%Y.%m.%d - %H:%M:%S")

    #time stamp command 
    timestampCommand = "/mnt/captures/convert/ " + FilePathPic + " -pointsize 36 \
      -fill blue -annotate +700+650 '" + timestampMessage + "' " + FilePathPic
    
    call([timestampCommand], shell=True)
    print("  picture captured")


    picCount += 1
    sleep(3)
