import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

import capturePicture
import captureVideo

class TakePicture(resource.Resource):
    """This is our first resource defined from scratch to test functionality."""

    def __init__(self):
        super().__init__()
        self.set_content(b"If you perform a PUT on this URI, camera will take a picture.")

    def set_content(self, content):
        self.content = content
           
    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
    
    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        """print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)"""
        #Call Take picture function
        takePicture(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Picture captured.')
    
class TakeVideo(resource.Resource):
    """This is our first resource defined from scratch to test functionality."""

    def __init__(self):
        super().__init__()
        self.set_content(b"If you perform a PUT on this URI, camera will take a video of the amount of seconds you send.")

    def set_content(self, content):
        self.content = content
           
    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
    
    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        """print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)"""
        captureVideo.main()
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Video captured.')
# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def takePicture(hubRequest):
    
    print(hubRequest)
    hubRequeststr = hubRequest.decode()
    capturePicture.main(hubRequeststr)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('camera','capture'), TakePicture())
    root.add_resource(('camera','captureVideo'), TakeVideo())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
