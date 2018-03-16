import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap


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


async def createRequest(request_type, node_address, node_resource,protocol):
    print("CREATING REQUEST IN THREAD: ",threading.current_thread())
    targetURI = 'coap://' + node_address + node_resource

    request = Message(code=PUT, uri=targetURI)

    """We don't technically care if this thread blocks, only that the coap thread does"""
    try:
        response = await protocol.request(request).response
    except Exception as e:
        return e
    else:
        return response.payload


def backgroundTask(loop,protocol):

    """This is where you would run background tasks, like motion detection or scheduling temperature checks"""

    """packet = asyncio.run_coroutine_threadsafe(createRequest('PUT', '10.0.0.100', '/notifications',protocol), loop).result()"""

    while true:
        print("BACKGROUND THREAD: ",threading.current_thread())
        sleep(3)

def main():

    coap_loop = asyncio.get_event_loop()

    # Resource tree creation
    root = resource.Site()
    root.add_resource(('.well-known', 'core'),
        resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('test',), TestResource())

    protocol = coap_loop.run_until_complete(aiocoap.Context.create_server_context(root))

    namedBackgroundTask = threading.Thread(target=backgroundTask, args=(coap_loop,protocol,))
    namedBackgroundTask.start()

    coap_loop.run_forever()

if __name__ == "__main__":
    main()
