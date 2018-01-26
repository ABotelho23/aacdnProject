def checkStatus():

  readPath = '/home/pi/BlindStatus.txt'
  statusFile = open(readPath, 'r')
  currentStatus = statusFile.readline()
  statusFile.close()
  
  return currentStatus

if __name__ == "__main__":
    checkStatus()
