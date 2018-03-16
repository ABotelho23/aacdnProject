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

class DiscoveryThread(threading.Thread):
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
            print('\n')

class CoapNode():
    def __init__(self, ip_address, hostname, device_type):
        self.ip_address = ip_address
        self.hostname = hostname
        self.device_type = device_type


class FlaskThread(threading.Thread):
    def __init__(self, loop, protocol):
        self.loop = loop
        self.protocol = protocol
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


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/temperatureCheck/")
def tempstatus():
    return render_template('temperature.html')

@app.route("/tempbackground_proc")
def checkTemp():
    currentTemp = asyncio.run_coroutine_threadsafe(createRequest('GET', '10.0.0.103', '/thermo/temp',protocol), loop).result()
    print(currentTemp)
    return jsonify(result=currentTemp)

async def createRequest(request_type, node_address, node_resource,protocol):
    print("COAP THREAD DEBUG, SENDING REQUEST START: ",threading.current_thread())
    targetURI = 'coap://' + node_address + node_resource

    request = Message(code=GET, uri=targetURI)

    """We don't technically care if the GUI thread blocks, only that the coap thread does"""
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


"""def discoveryThread():
    print("DISCOVERY THREAD DEBUG #1: ",threading.current_thread())
    Prints here to be dumped into the main section of the GUI, maybe via queues?
    zeroconfDiscover.main()
    print("DISCOVERY THREAD DEBUG #2: ",threading.current_thread())"""


def testThread(loop,protocol):
    """This thread emulates what would be the GUI in the final product"""
    print("TEST THREAD DEBUG #1: ",threading.current_thread())

    counter = 0
    while True:
        counter += 1
        time.sleep(1)
        packet = asyncio.run_coroutine_threadsafe(createRequest('GET', '10.0.0.101', '/bulb/colours',protocol), loop).result()

        print("\n\n!==========REPONSE #",counter," FROM NODE: ",packet,"==========!\n\n")

        print("COAP THREAD DEBUG #3: ",threading.current_thread())


def main():

    print('DEBUG: STARTING DISCVOERY THREAD...')
    discoverNodes = DiscoveryThread()
    discoverNodes.start()
    print('DEBUG: FINISHED STARTING DISCOVERY THREAD...')

    coap_loop = asyncio.get_event_loop()
    #coap_loop.set_debug()

    root = resource.Site()
    root.add_resource(('.well-known', 'core'),
        resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('test',), TestResource())

    print('DEBUG: STARTING AIOCOAP THREAD...')
    aiocoapWorker = threading.Thread(target=aiocoapThread, args=(coap_loop,))
    aiocoapWorker.start()
    print('DEBUG: FINISHED STARTING AIOCOAP THREAD...\n')

    protocol = asyncio.run_coroutine_threadsafe(aiocoap.Context.create_server_context(root),coap_loop).result()

    """print('DEBUG: STARTING DISCOVERY THREAD...')
    discoverNodes = threading.Thread(target=discoveryThread)
    discoverNodes.start()
    print('DEBUG: FINISHED STARTING DISCOVERY THREAD...\n')"""

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
