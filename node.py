import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap
import threading
import time


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
        takeVideo(request.payload)
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


def backgroundTask(loop,protocol):

    """This is where you would run background tasks, like motion detection or scheduling temperature checks"""
    while True:
            motionState = picammotion.motion()
            print(motionState)
             if motionState:
                 #DEFINE WHAT THE PAYLOAD IS
                 payload = b"PAYLOAD CONTENT"
                 request = Message(code=PUT, uri=targetURI, payload=payload)
                 print('Sending payload')
                 response = _await(ctx.request(request).response)
                 print('Result: %s\n%r'%(response.code, response.payload))
                 takeVideo(b'10')
     
         #async def render_put(self, request):
             #return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Motion Detected.')

    """packet = asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.100', '/notifications',protocol,'Motion Detected',), loop).result()"""

    while True:
        print("BACKGROUND THREAD: ",threading.current_thread())
        time.sleep(3)

def main():

    coap_loop = asyncio.get_event_loop()

    # Resource tree creation
    root = resource.Site()
    root.add_resource(('.well-known', 'core'),
        resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('picture'), TakePicture())
    root.add_resource(('video'), TakeVideo())

    protocol = coap_loop.run_until_complete(aiocoap.Context.create_server_context(root))

    Backgroundmotion = threading.Thread(target=backgroundTask, args=(coap_loop,protocol,))
    Backgroundmotion.start()

    coap_loop.run_forever()

if __name__ == "__main__":
    main()
