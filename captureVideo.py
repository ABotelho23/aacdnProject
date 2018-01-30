import picamera
from time import sleep
from subprocess import call
import datetime as dt
import os
import shlex
import subprocess

#File path 
filePath = "/mnt/captures/"
fileName = os.path.join(filePath, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.'))
fileWithExtension = fileName
fileWithExtension += 'h264'

#  camera Setup
with picamera.PiCamera() as camera:
    camera.start_recording(fileWithExtension)
    sleep(5)
    camera.stop_recording()

print("convert the video.")

command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=str(fileName)))
try:
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
except subprocess.CalledProcessError as e:
    print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

#call([command], shell=True)
# Video converted.
print("Video converted.")
