import picamera
from time import sleep
import datetime as dt
import os
import subprocess

def main():
    #File path 
    filePath = "/mnt/captures/"
    fileName = os.path.join(filePath, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S'))
    fileWithExtension = fileName
    fileWithExtension += '.h264'
    # Motion detection 
    def captureTestImage(settings, width, height):
    command = "raspistill %s -w %s -h %s -t 200 -e bmp -n -o -" %  (settings, width, height)
    #imageData = StringIO.StringIO()
    imageData = io.BytesIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer

    #Camera Setup
    with picamera.PiCamera() as camera:
        camera.start_recording(fileWithExtension)
        sleep(5)
        camera.stop_recording()

    print("convert the video.")

    command = "MP4Box -add {f}.h264 {f}.mp4".format(f=str(fileName))
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))
    print("Video converted.")
