import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

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
    
    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        turnOnLight(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

#1 = off, 0 = on
def turnOnLight(onOrOff):
    
    if (onOrOff == '1'):
        GPIO.output(RED,1)
        GPIO.output(GREEN,1)
        GPIO.output(BLUE,1)
    
    else:
        GPIO.output(RED,0)
        GPIO.output(GREEN,0)
        GPIO.output(BLUE,0)

        
def initializeGPIO ():
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    RED = 17
    GREEN = 18
    BLUE = 27

    GPIO.setup(RED,GPIO.OUT)
    GPIO.setup(GREEN,GPIO.OUT)
    GPIO.setup(BLUE,GPIO.OUT)

def main():
    
    try:
        initializeGPIO()

        # Resource tree creation
        root = resource.Site()

        root.add_resource(('.well-known', 'core'),
                resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(('test',), TestResource())

        asyncio.Task(aiocoap.Context.create_server_context(root))

        asyncio.get_event_loop().run_forever()
    
    except KeyboardInterrupt:
        RPi.GPIO.cleanup()

if __name__ == "__main__":
    main()
