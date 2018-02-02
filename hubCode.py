import datetime
import logging
import asyncio
import dbus
import avahi
import threading
import aiocoap.resource as resource
from aiocoap import *
import aiocoap

class ServerThread(threading.Thread):
    def run(self):
      print('Starting server, creating resource tree...')
      # Resource tree creation
      root = resource.Site()

      root.add_resource(('.well-known', 'core'),
        resource.WKCResource(root.get_resources_as_linkheader))

      root.add_resource(('hub', 'bulbs', 'schedule'), BulbSchedule())
      root.add_resource(('hub', 'cameras', 'capture'), CameraCapture())
      root.add_resource(('hub', 'thermometers', 'temperature'), ThermoTemperature())
      root.add_resource(('hub', 'blinds', 'schedule'), BlindsSchedule())

      asyncio.Task(aiocoap.Context.create_server_context(root))

      asyncio.get_event_loop().run_forever()


class BulbSchedule(resource.Resource): #/hub/bulb/schedule
    """This could be for notifying hub that a scheduled colour change or on/off has occurred?"""

    def __init__(self):
        super().__init__()
        self.set_content(b"No messages have been posted by any bulbs yet.")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        print('Last message from a bulb being requested. Sending.')
        return aiocoap.Message(payload=self.content)

    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        #print('PUT payload: %s' % request.payload)
        print('Message from bulb: ' % request.payload) #to add avahi "name" to "bulb"?
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload='Notification received.')

class CameraCapture(resource.Resource): #/hub/camera/capture
    """This could be for notifying hub that the camera detected motion and took a picture?"""

    def __init__(self):
        super().__init__()
        self.set_content(b"No images have been transmitted to the hub yet.")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
        print('Sending number of pictures taken from camera last time.')

    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        #rint('PUT payload: %s' % request.payload)
        print('Camera took automated picture. Placing in samba share. Placed number of pictures taken in URI.')
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload='Aknowledged')

class ThermoTemperature(resource.Resource): #/hub/thermometer/temperature
    """This could be for notifying hub of new temperature change every X mins?"""

    def __init__(self):
        super().__init__()
        self.set_content(b"No temperature has been posted yet.")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
        print('Sending last received temperature.')

    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        #print('PUT payload: %s' % request.payload)
        print('Updating temperature to ' % request.payload)
        self.set_content(request.payload)
        returnMessage = 'Temperature recorded as ' % self.content
        return aiocoap.Message(code=aiocoap.CHANGED, payload=returnMessage)

class BlindsSchedule(resource.Resource): #/hub/blinds/schedule
    """This could be for notifying hub that a scheduled raising or lowering has occured?"""

    def __init__(self):
        super().__init__()
        self.set_content(b"This is the default content for this resource.")

    def set_content(self, content):
        self.content = content

    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
  serverRunning = '0'

  while True:

      selection = input("\n==========\n1. GET\n2. PUT \n3. SERVER (not yet available) \n4. MULTI-DEVICE\n==========\n")

      if (selection == '1'):
        targetIPAdd = input("\nWhat is the IP address of the target?")
        targetResource = input("\nWhat is the resource of the target?\n Include initial slash, and no ending slash. \n")
        targetURI = 'coap://' + targetIPAdd + targetResource
        protocol = await Context.create_client_context()

        request = Message(code=GET, uri=targetURI)

        try:
          response = await protocol.request(request).response
        except Exception as e:
          print('Failed to fetch resource:')
          print(e)
        else:
          print('Result: %s\n%r'%(response.code, response.payload))

      elif (selection == '2'):
        targetIPAdd = input("\nWhat is the IP address of the target?\n")
        targetResource = input("\nWhat is the resource of the target?\nInclude initial slash, and no ending slash.\n")
        targetURI = 'coap://' + targetIPAdd + targetResource
        context = await Context.create_client_context()

        userInput = input("\nWhat is the payload?")
        payload = userInput.encode()
        request = Message(code=PUT, uri=targetURI, payload=payload)
        # These direct assignments are an alternative to setting the URI like in
        # the GET example:
        #request.opt.uri_host = '10.0.0.101'
        #request.opt.uri_path = 'test'
        print(payload)
        response = await context.request(request).response

        print('Result: %s\n%r'%(response.code, response.payload))

      elif (selection == '3'):
        if (serverRunning == '0'):
            serverRunning = 1
            receiverThread = ServerThread()
            receiverThread.start()
        else:
            print('\nServer should already be running.')
      elif (selection == '4'):

        multiSelection = input("\nWhat is the command?\n")

        if (multiSelection == 'goodnight'):
            targetURI1 = 'coap://node1/bulb/colours'
            targetURI4 = 'coap://node4/blinds/move'

            context1 = await Context.create_client_context()
            context4 = await Context.create_client_context()

            request1 = Message(code=PUT, uri=targetURI1, payload=b'off')
            request4 = Message(code=PUT, uri=targetURI4, payload=b'10')

            response1 = await context1.request(request1).response
            response4 = await context4.request(request4).response

            print('Result: %s\n%r'%(response1.code, response1.payload))
            print('Result: %s\n%r'%(response4.code, response4.payload))

            print('\nResponses received!')

        else:
            print('\nThat is not a supported command!')

      else:
        print('\nInvalid selection.')

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())



#contextClient = await Context.create_client_context() #context for sending PUTs and GETs

#contextServer = await Context. create_server_context() #context for receiving PUTs and GETs
