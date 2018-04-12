import datetime
import time
import logging
import asyncio
import dbus
#import avahi
import threading
import aiocoap.resource as resource
from aiocoap import *
import aiocoap
import zeroconfDiscover
import flask
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from os import *
import os

global app
app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/gallery/")
def galleryPage():
    pics = os.listdir('static/images/camera/pictures')
    picSort = sorted(pics, reverse=True)
    vids = os.listdir('static/images/camera/videos')
    vidSort = sorted(vids, reverse=True)
    return render_template('gallery.html', pics=picSort, vids=vidSort)

@app.route("/multidevice/")
def multiPage():
    return render_template('multidevice.html')

@app.route("/credit/")
def creditPage():
    return render_template('credits.html')

@app.route("/tempbackground_proc")
def checkTemp():
    currentTemp = asyncio.run_coroutine_threadsafe(createRequest('GET', '10.0.0.103', '/thermo/temp','0', flaskProtocol), flaskLoop).result()
    return jsonify(result=currentTemp)

@app.route("/bulbbackground_proc")
def checkBulb():
    currentBulb = asyncio.run_coroutine_threadsafe(createRequest('GET', '10.0.0.101', '/bulb/colours','0', flaskProtocol), flaskLoop).result()
    return jsonify(result=currentBulb)

@app.route("/bulbsetbackground_proc")
def setBulb():
    onoff = request.args.get('onoffVal')
    colour = request.args.get('colourVal')
    print(onoff)
    print(colour)
    if(onoff == 'Off'):
        asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.101', '/bulb/colours', 'Off', flaskProtocol), flaskLoop)
    else:
        asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.101', '/bulb/colours', colour, flaskProtocol), flaskLoop)

    return jsonify('done')

@app.route("/blindbackground_proc")
def checkBlind():
    currentBlind = asyncio.run_coroutine_threadsafe(createRequest('GET', '10.0.0.104', '/blinds/move','0', flaskProtocol), flaskLoop).result()
    currentBlindstr = currentBlind.decode();

    if(currentBlindstr == '0'):
        currentBlindstr = 'Fully Open'
    elif(currentBlindstr == '10'):
        currentBlindstr = 'Fully Closed'
    else:
        currentBlindstr += '0% Closed'

    return jsonify(result=currentBlindstr)

@app.route("/blindsetbackground_proc")
def setBlind():
    userPayload = request.args.get('blindVal')
    setBlind = asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.104', '/blinds/move', userPayload, flaskProtocol), flaskLoop).result()
    return jsonify(result2=setBlind)

@app.route("/picturebackground_proc")
def setPicture():
    userPayload = request.args.get('picVal')
    setPic = asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.102', '/picture', userPayload, flaskProtocol), flaskLoop).result()
    return jsonify(result2=setPic)

@app.route("/videobackground_proc")
def setVideo():
    userPayload = request.args.get('vidVal')
    setVid = asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.102', '/video', userPayload, flaskProtocol), flaskLoop).result()
    return jsonify(result2=setVid)

@app.route("/lastpicbackground_proc")
def checkPic():
    listPic = os.listdir('static/images/camera/pictures/')
    paths = [os.path.join('static/images/camera/pictures/', basename) for basename in listPic]
    lastPic = max(paths, key=os.path.getctime)
    newLP = lastPic.replace('static/images/camera/pictures/','')

    return jsonify(result=newLP)

"""class DiscoveryThread(threading.Thread):
    def run(self):
        zeroconf = Zeroconf()
        print("\n+++++Discovering services...+++++\n")
        browser = ServiceBrowser(zeroconf, "_coap._udp.local.", handlers=[on_service_state_change])

        sleep(30)
        print("\n+++++Ending services discovery...+++++\n")
        zeroconf.close()

    def on_service_state_change(zeroconf, service_type, name, state_change):
        print("Service %s of type %s state changed: %s" % (name, service_type, state_change))

        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                print("  Address: %s" % (socket.inet_ntoa(info.address)))
                print("  Hostname: %s" % (info.server,))
                if info.properties:
                    print("  Properties are:")
                    for key, value in info.properties.items():
                        print("    %s: %s" % (key, value))
                else:
                    print("  No properties")
            else:
                print("  No info")
            print('\n')"""

class CoapNode():
    def __init__(self, ip_address, hostname, device_type):
        self.ip_address = ip_address
        self.hostname = hostname
        self.device_type = device_type


class FlaskThread(threading.Thread):
    def __init__(self, loop, protocol):
        threading.Thread.__init__(self)
        global flaskLoop
        global flaskProtocol
        flaskLoop = loop
        flaskProtocol = protocol

    def run(self):
        print("FLASK THREAD DEBUG #1: ",threading.current_thread())
        app.run()

class CameraCapture(resource.Resource):
    """For receiving notifications from camera."""

    def __init__(self):
        super().__init__()
        self.set_content(b"No notifications from camera yet.")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        print('\nReceived notification from a camera: %s' % request.payload)
        print('\n')
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Notification received.')

class Notifications(resource.Resource):
    """This is our first resource defined from scratch to test functionality."""
    def __init__(self):
        super().__init__()
        self.set_content(b"No notifications.")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('\nReceived notification from a camera: %s' % request.payload)
        print('\n')
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Notification received.')

class TestResource(resource.Resource):
    """This is our first resource defined from scratch to test functionality."""
    def __init__(self):
        super().__init__()
        self.set_content(b"This is the default TEST content.")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('\nTest content has be re-set: %s' % request.payload)
        print('\n')
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Confirmed changed test content.')

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def createRequest(request_type, node_address, node_resource, userPayload, protocol):
    if (request_type == 'GET'):
        print("COAP THREAD DEBUG, SENDING GET REQUEST START: ",threading.current_thread())
        targetURI = 'coap://' + node_address + node_resource

        request = Message(code=GET, uri=targetURI)

        """We don't technically care if the GUI thread blocks, only that the coap thread does"""
        try:
            response = await protocol.request(request).response
        except Exception as e:
            return e
        else:
            return response.payload
    else:
        print("COAP THREAD DEBUG, SENDING PUT REQUEST START: ",threading.current_thread())
        targetURI = 'coap://' + node_address + node_resource
        payload1 = userPayload.encode()
        request = Message(code=PUT, uri=targetURI, payload=payload1)

        try:
            response = await protocol.request(request).response
        except Exception as e:
            return e
        else:
            return response.payload

def aiocoapThread(loop):

    print("COAP THREAD DEBUG #1, setting event loop: ",threading.current_thread())
    asyncio.set_event_loop(loop)

    print("COAP THREAD DEBUG #3, making loop run forever: ",threading.current_thread())
    loop.run_forever()

    print("COAP THREAD DEBUG #4, should this be seen?: ",threading.current_thread())


def discoveryThread():
    print("DISCOVERY THREAD DEBUG #1: ",threading.current_thread())
    zeroconfDiscover.main()
    print("DISCOVERY THREAD DEBUG #2: ",threading.current_thread())


def testThread(loop,protocol):
    """This thread emulates what would be the GUI in the final product"""
    print("TEST THREAD DEBUG #1: ",threading.current_thread())

    packet = asyncio.run_coroutine_threadsafe(createRequest('GET', '10.0.0.101', '/bulb/colours','0', protocol), loop).result()

    print("\n\n!==========REPONSE FROM NODE: ",packet,"==========!\n\n")

    print("COAP THREAD DEBUG #3: ",threading.current_thread())


def main():

    """print('DEBUG: STARTING DISCVOERY THREAD...')
    discoverNodes = DiscoveryThread()
    discoverNodes.start()
    print('DEBUG: FINISHED STARTING DISCOVERY THREAD...')"""

    coap_loop = asyncio.get_event_loop()
    #coap_loop.set_debug()

    root = resource.Site()
    root.add_resource(('.well-known', 'core'),
        resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('test',), TestResource())
    root.add_resource(('notifications',), Notifications())

    print('DEBUG: STARTING AIOCOAP THREAD...')
    aiocoapWorker = threading.Thread(target=aiocoapThread, args=(coap_loop,))
    aiocoapWorker.start()
    print('DEBUG: FINISHED STARTING AIOCOAP THREAD...\n')

    protocol = asyncio.run_coroutine_threadsafe(aiocoap.Context.create_server_context(root),coap_loop).result()

    print('DEBUG: STARTING DISCOVERY THREAD...')
    discoverNodes = threading.Thread(target=discoveryThread)
    discoverNodes.start()
    print('DEBUG: FINISHED STARTING DISCOVERY THREAD...\n')

    print('DEBUG: STARTING FLASK THREAD...')
    flaskServer = FlaskThread(coap_loop,protocol)
    flaskServer.start()
    print('DEBUG: FINISHED STARTING FLASK THREAD...')

    print('DEBUG: STARTING TEST THREAD...')
    testInstance = threading.Thread(target=testThread, args=(coap_loop,protocol,))
    testInstance.start()
    print('DEBUG: FINISHED STARTING TEST THREAD...')
    print('DEBUG: FINISHED STARTING TEST THREAD...')

    print('ALL THREADS STARTED!\n')

    counter = 0
    while True:
        counter += 1
        time.sleep(3)
        print('MAIN THREAD DEBUG #:',counter, ', PRINTING FROM END OF MAIN\n')

if __name__ == "__main__":
    main()
