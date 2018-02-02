import SocketServer
from zeroconf import *
import socket
import time
 
PORT = 7679
devices = [];
 
class ServiceListener(object):
    def __init__(self):
        self.r = Zeroconf()
 
    def removeService(self, zeroconf, type, name):
        print
        print "Service", name, "removed"
 
    def addService(self, zeroconf, type, name):
        print
        print "Service", name, "added"
        print "  Type is", type
        info = self.r.getServiceInfo(type, name)
        if info:
            #Currently only saving the ip address.
            devices.append(socket.inet_ntoa(info.getAddress()))
            print "  Address is %s:%d" % (socket.inet_ntoa(info.getAddress()),
                                          info.getPort())
            print "  Weight is %d, Priority is %d" % (info.getWeight(),
                                                      info.getPriority())
            print "  Server is", info.getServer()
            prop = info.getProperties()
            if prop:
                print "  Properties are"
                for key, value in prop.items():
                    print "    %s: %s" % (key, value)
 
def searchForDynamixServices():
    del devices[:] # Clear list.
    r = Zeroconf()
    type = "_dynamix._tcp.local."
    listener = ServiceListener()
    browser = ServiceBrowser(r, type, listener)
    #Will only be searching for 5 seconds. 
    time.sleep(5)
    r.close()
    return devices[0]
