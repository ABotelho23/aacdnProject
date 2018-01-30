import picamera
from time import sleep
from subprocess import call
#File path 
    filePath = "/mnt/videocaptures/"
    
#  camera Setup
with picamera.PiCamera() as camera:
    camera.start_recording("pythonVideo.h264")
    sleep(5)
    camera.stop_recording()

print("convert the video.")

command = "MP4Box -add pythonVideo.h264 convertedVideo.mp4"
call([command], shell=True)
# Video converted.
print("Video converted.")
