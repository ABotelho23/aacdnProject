import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

class Temperature(resource.Resource):
    """This URI is the value of the temperature"""

    def __init__(self):
        super().__init__()
        self.set_content(b"0")

    def set_content(self, content):
        self.content = content
           
    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        readPath = '/sys/bus/w1/devices/28-0316a078c2ff/w1_slave'
        statusFile = open(readPath, 'r')
        payloadtemp = statusFile.readline()
        statusFile.close()
        tempvalue = bytes(payloadtemp)
        #tempvalue = payloadtemp.encode()
        self.set_content(tempvalue)
        return aiocoap.Message(payload=self.content)
    
    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('node3','thermometer','temperature'), Temperature())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
