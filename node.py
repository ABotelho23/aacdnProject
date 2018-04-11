import datetime
import logging
import asyncio
from aiocoap import *
import aiocoap.resource as resource
import aiocoap
import threading
import time
import capturePicture
import captureVideo
import picammotion

logging.basicConfig(level=logging.DEBUG)

"""Please keep this resource for testing purposes"""
class TestResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b"TEST CONTENT!")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Test put set.')

class TakePicture(resource.Resource):
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
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        #Call Take picture function
        capturePicture.main(request.payload)
        #takePicture(request.payload)
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
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        captureVideo.main(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Video captured.')
# logging setup

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

async def motion(loop,protocol):
        await asyncio.sleep(0)
        motionState = picammotion.motion()
        return motionState

def backgroundTask(loop,protocol):
        #self.toggleMotion = False
        #self.mode = b'0'
    time.sleep(1)
    while True:
            motionYesOrNo = asyncio.run_coroutine_threadsafe(motion(loop,protocol), loop).result()
            if motionYesOrNo == False:
                print("BACKGROUND THREAD, no motion: ",threading.current_thread())
            else:
            #packet = await createRequest('PUT', '10.0.0.100', '/notifications','Motion Detected',protocol)
                packet = asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.100', '/notifications','Motion Detected',protocol), loop).result()
                print("BACKGROUND THREAD, motion: ",threading.current_thread())
                capturePicture.main(1)
                time.sleep(5)

def main():

    coap_loop = asyncio.get_event_loop()

    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'),
        resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('test',), TestResource())
    root.add_resource(('picture',), TakePicture())
    root.add_resource(('video',), TakeVideo())

    protocol = coap_loop.run_until_complete(aiocoap.Context.create_server_context(root))

    #detectMotion = backgroundTask(args=(protocol,coap_loop))
    #detectMotion.start()

    detectMotion = threading.Thread(target=backgroundTask, args=(coap_loop,protocol,))
    detectMotion.start()

    coap_loop.run_forever()


if __name__ == "__main__":
    main()
