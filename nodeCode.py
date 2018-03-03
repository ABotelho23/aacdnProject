import datetime
import logging
import asyncio
import aiocoap.resource as resource
from aiocoap import *
import aiocoap
import threading
import capturePicture
import captureVideo

class MotionThread(resource.Resource):
    def __init__(self):
        
        async def motionLoop(self):
            while True:
                await asyncio.sleep(1)
                if self.toggleMotion:
                    return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Motion Toggle on.')
                    while self.toggleMotion:
                        print('sending payload')
                        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Motion Detected.')
                        if request.payload == b'0':
                            takePicture(b'10')
                        else:
                            takeVideo(b'10')        
                    return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Motion Toggle off.')
                    
        super().__init__()
        self.set_content(b"If you perform a PUT on this URI, motion detection will be toggled.")
        self.toggleMotion = False
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(motionLoop)
        #self.loop.close()
        
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
        if len(request.payload) > 0:
            self.toggleMotion = not self.toggleMotion
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Motion detection toggled')


    def run(self):

        targetURI = 'coap://10.0.0.100/cameras/capture'

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        _await = asyncio.get_event_loop().run_until_complete
        ctx = _await(Context.create_client_context())

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
                
        async def render_put(self, request):
            return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Motion Detected.')

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

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def takePicture(hubRequest):

    print(hubRequest)
    hubRequeststr = hubRequest.decode()
    capturePicture.main(hubRequeststr)

def takeVideo(hubRequest):
    print(hubRequest)
    hubRequeststr = hubRequest.decode()
    captureVideo.main(hubRequeststr)
    
def main():

    #start motion detection thread

    #moDetectionThread = MotionThread()
    #moDetectionThread.start()

    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('camera','capture'), TakePicture())
    root.add_resource(('camera','captureVideo'), TakeVideo())
    root.add_resource(('camera', 'motionToggle'), MotionThread())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()



