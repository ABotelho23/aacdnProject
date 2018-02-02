import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

import RPi.GPIO as GPIO

import turnOn
import turnOff
import RED
import BLUE
import GREEN
import YELLOW
import CYAN
import MAGENTA

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

# 1 = off, 0 = on
def turnOnLight(onOrOff):
    
    print(onOrOff)
    onOrOffstr = onOrOff.decode()
  
    if (onOrOffstr == 'on'):
        turnOn.lightOn()
    elif (onOrOffstr == 'off'):
        turnOff.lightOff()
    elif (onOrOffstr == 'red'):
        RED.redOn()
    elif (onOrOffstr == 'green'):
        GREEN.greenOn()
    elif (onOrOffstr == 'blue'):
        BLUE.blueOn()
    elif (onOrOffstr == 'yellow'):
        YELLOW.yellowOn()
    elif (onOrOffstr == 'cyan'):
        CYAN.cyanOn()
    elif (onOrOffstr == 'magenta'):
        MAGENTA.magentaOn()
    else:
        print("nothing")
        
  #  if (onOrOffstr == '1'):
   #     GPIO.output(RED,1)
    #    GPIO.output(GREEN,1)
     #   GPIO.output(BLUE,1)
    
    #else:
     #   GPIO.output(RED,0)
      #  GPIO.output(GREEN,0)
       # GPIO.output(BLUE,0)

def main():

        # Resource tree creation
        root = resource.Site()

        root.add_resource(('.well-known', 'core'),
                resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(('bulb','colours'), TestResource())

        asyncio.Task(aiocoap.Context.create_server_context(root))

        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
