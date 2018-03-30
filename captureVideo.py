
import picamera
import picammotion
from  time import sleep
import datetime as dt
from datetime import timedelta
import os
import subprocess

def main(fromServer):
	#File path
	filePath = "/mnt/captures/videos/"
	#fileName = os.path.join(filePath, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S'))
	#fileWithExtension = fileName
	#fileWithExtension += '.h264'
	picTotal = fromServer
	intpicTotal = int(picTotal)


	cTime = dt.datetime.now()
	dTime = cTime + timedelta(seconds=10)  # constant time for motion detection to stay on
	#while cTime < dTime:

	cTime = dt.datetime.now()
	fileName = os.path.join(filePath, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S'))
	#motionState = picammotion.motion()
	#print(motionState)
#	if motionState:
		#Camera Setup
	with picamera.PiCamera() as camera:
		camera.start_recording(fileName + '.h264')
		sleep(intpicTotal)  # payload specfying how long to record in seconds
		camera.stop_recording()

		print("convert the video.")

		command = "MP4Box -add {f}.h264 {f}.mp4".format(f=str(fileName))
		try:
			output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
		except subprocess.CalledProcessError as e:
			print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))
			print("Video converted.")
            		os.remove('/mnt/captures/videos/*.h264')
