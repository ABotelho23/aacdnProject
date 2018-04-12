#Library Imports
import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
#Script Imports
import opencloseBlinds
import blindStatus

class MovementResource(resource.Resource):
    """Resource used to move blinds based on Hub reqeust."""

    def __init__(self):
        super().__init__()
        #Check current status and set upon initialization of Resource
        currentStatus = blindStatus.checkStatus()
        bcurrentStatus = currentStatus.encode()
        self.set_content(bcurrentStatus)

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        await asyncio.sleep(0)
        activateMotor(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'Blinds Finished')

#logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

#Activate Motor
def activateMotor(hubRequest):

    print(hubRequest)
    hubRequeststr = hubRequest.decode()
    opencloseBlinds.main(hubRequeststr)


def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('blinds','move'), MovementResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
