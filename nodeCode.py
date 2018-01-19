import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

import opencloseBlinds
import initializeMotor
import blindStatus

class TestResource(resource.Resource):
    """This is our first resource defined from scratch to test functionality."""

    def __init__(self):
        super().__init__()
        initializeMotor.initialize()
        currentStatus = blindStatus.checkStatus()
        #print(currentStatus)
        bcurrentStatus = currentStatus.encode()
        self.set_content(bcurrentStatus)
        #print(bcurrentStatus)

    def set_content(self, content):
        self.content = content
           
    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
    
    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        activateMotor(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
# logging setup

#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)

#Activate Motor
def activateMotor(testRequest):
    
    print(testRequest)
    testRequeststr = testRequest.decode()
    
    opencloseBlinds.main(testRequeststr)


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('node4','blinds','status'), TestResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
