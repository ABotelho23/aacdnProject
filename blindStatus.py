
def checkStatus():

  print("Checking Status File")
  readPath = '/home/pi/BlindStatus.txt'
  statusFile = open(readPath, 'r')
  
  currentStatus = statusFile.readline()
  print("Current Status: ")
  print(currentStatus)


if __name__ == "__main__":
    checkStatus()
