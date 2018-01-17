import datetime
import logging
import asyncio
from aiocoap import *
      
class ThermoTemperature(resource.Resource): #/node3/thermometer/temperature
    """This could be for notifying hub of new temperature change every X mins?"""

    def __init__(self):
        super().__init__()
        self.set_content(b"This is the default content for this resource.")

    def set_content(self, content):
        self.content = content
           
    #this is the render for a GET. This returns the payload.
    async def render_get(self, request):
        readPath = '/sys/bus/w1/devices/28-0316a078c2ff/w1_slave.txt
        statusFile = open(readPath, 'r')
        payloadtemp = statusFile.readline()
        return aiocoap.Message(payload=payloadtemp)
    
    #this is the render for a PUT. This sets what the resource value is.
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
      

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
  
  targetIPAdd = input("What is the IP address of the target?")
  targetResource = input("What is the resource of the target? Include initial slash, and no ending slash")
  targetURI = 'coap://' + targetIPAdd + targetResource
  
  selection = input("1. GET\n2. PUT \n3. SERVER (not yet available)\n")
  
  if (selection == '1'):
    
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
    
    context = await Context.create_client_context()
    
    userInput = input("What is the paylod?")
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
    print('Starting server, creating resource tree...')  
      # Resource tree creation
      root = resource.Site()
        
      root.add_resource(('.well-known', 'core'),
        resource.WKCResource(root.get_resources_as_linkheader))
      root.add_resource(('node3', 'thermometer', 'temperature'), ThermoTemperature())
      
      asyncio.Task(aiocoap.Context.create_server_context(root))
 
      asyncio.get_event_loop().run_forever()
  
  else:
    print('Invalid selection. Re-run program to try again.')
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
  
