import picamera
from time import sleep
from subprocess import call
import datetime as dt
import os
import shlex

#File path 
filePath = "/mnt/captures/"
fileName = os.path.join(filePath, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))

#  camera Setup
with picamera.PiCamera() as camera:
    camera.start_recording(fileName)
    sleep(5)
    camera.stop_recording()

print("convert the video.")


command = shlex.split("MP4Box -add {} {}.mp4".format(filePath, os.path.splitext(fileName)[0]))
call([command], shell=True)
# Video converted.
print("Video converted.")
