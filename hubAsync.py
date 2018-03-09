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
      print("In thread",threading.current_thread())
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

async def createAllContexts():

    root = resource.Site()
    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('test',), TestResource())

    protocol = await Context.create_client_context()
    await protocol.create_server_context(root)

    print("DEBUG: In thread #3")

    request = Message(code=GET, uri='coap://10.0.0.101/bulb/colours')

    print("DEBUG: In thread #4")

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

def aiocoapThread():

    print("In thread",threading.current_thread())
    print("DEBUG: In thread #1")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("DEBUG: In thread #2")

    loop.run_until_complete(createAllContexts())

    loop.run_forever()

def discoveryThread():
    print("In thread",threading.current_thread())
    zeroconfDiscover.main()

def main():

  print('DEBUG: STARTING FLASK THREAD...')
  flaskServer = FlaskThread()
  flaskServer.start()
  print('DEBUG: FINISHED STARTING FLASK THREAD...')

  print('DEBUG: STARTING AIOCOAP THREAD...')
  aiocoapWorker = threading.Thread(target=aiocoapThread)
  aiocoapWorker.start()
  print('DEBUG: FINISHED STARTING AIOCOAP THREAD...\n')

  print('DEBUG: STARTING DISCOVERY THREAD...')
  discoverNodes = threading.Thread(target=discoveryThread)
  discoverNodes.start()
  print('DEBUG: FINISHED STARTING DISCOVERY THREAD...\n')

  print('DEBUG: PRINTING FROM MAIN\n')

if __name__ == "__main__":
    main()



#contextClient = await Context.create_client_context() #context for sending PUTs and GETs

#contextServer = await Context. create_server_context() #context for receiving PUTs and GETs
