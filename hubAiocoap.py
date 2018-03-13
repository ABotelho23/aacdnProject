import datetime
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

class FlaskThread(threading.Thread):

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
	currentTemp = coapTemp.main()
    print(currentTemp)
    return jsonify(result=currentTemp)

async def createRequest(request_type, node_address, node_resource):
	print("COAP THREAD DEBUG, SENDING REQUEST START: ",threading.current_thread())
	targetURI = 'coap://' + node_address + node_resource

    request = Message(code=request_type, uri=targetURI)

	"""Will response.payload be returned prior to the request being fulfilled?"""
	"""We don't technically care if the GUI thread blocks, only that the coap thread does"""
    try:
        response = await protocol.request(request).response
    except Exception as e:
        return e
    else:
        return response.payload

def aiocoapThread(loop):

	root = resource.Site()
	root.add_resource(('.well-known', 'core'),
		resource.WKCResource(root.get_resources_as_linkheader))
	root.add_resource(('test',), TestResource())

	print("COAP THREAD DEBUG #1, setting event loop: ",threading.current_thread())
    asyncio.set_event_loop(loop)

	print("COAP THREAD DEBUG #2, creating context: ",threading.current_thread())
	await protocol.create_server_context(root)

	print("COAP THREAD DEBUG #3, making loop run forever: ",threading.current_thread())
	loop.run_forever()

	print("COAP THREAD DEBUG #4, should this be seen?: ",threading.current_thread())

def discoveryThread():
    print("DISCOVERY THREAD DEBUG #1: ",threading.current_thread())
	"""Prints here to be dumped into the main section of the GUI, maybe via queues?"""
	zeroconfDiscover.main()
	print("DISCOVERY THREAD DEBUG #2 (SHOULDN'T SEE THIS): ",threading.current_thread())

def testThread(loop):
	"""This thread emulates what would be the GUI in the final product"""
	print("TEST THREAD DEBUG #1: ",threading.current_thread())

	"""this might return a future before it is available, CHECK THIS"""
	packet = asyncio.run_coroutine_threadsafe(createRequest('GET', '10.0.0.101', '/bulb/colours'), loop)

    print("\n\n!==========REPONSE FROM NODE: ",packet,"==========!\n\n")

    print("COAP THREAD DEBUG #3: ",threading.current_thread())

def main():

	print('DEBUG: STARTING FLASK THREAD...')
 	flaskServer = FlaskThread()
 	flaskServer.start()
 	print('DEBUG: FINISHED STARTING FLASK THREAD...')

	coap_loop = asyncio.new_event_loop()
	coap_loop.set_debug()

  	print('DEBUG: STARTING AIOCOAP THREAD...')
  	aiocoapWorker = threading.Thread(target=aiocoapThread, args=(coap_loop))
  	aiocoapWorker.start()
  	print('DEBUG: FINISHED STARTING AIOCOAP THREAD...\n')

  	print('DEBUG: STARTING DISCOVERY THREAD...')
  	discoverNodes = threading.Thread(target=discoveryThread)
  	discoverNodes.start()
  	print('DEBUG: FINISHED STARTING DISCOVERY THREAD...\n')

	print('ALL THREADS STARTED!\n')

	while True:
		counter = 0
		time.sleep(1)
		print('MAIN THREAD DEBUG #:',counter, ', PRINTING FROM END OF MAIN\n')

if __name__ == "__main__":
    main()
