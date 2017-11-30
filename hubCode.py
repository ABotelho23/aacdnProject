import datetime
import logging
import asyncio
from aiocoap import *

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
  
  selection = input("1. GET\n2. PUT \n3. SERVER (not yet available)\n")
  
  if (selection == '1'):
    
    protocol = await Context.create_client_context()
    
    request = Message(code=GET, uri='coap://10.0.0.101/test')
  
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
    request = Message(code=PUT, uri='coap://10.0.0.101/test', payload=payload)
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
      root.add_resource(('node3', 'temperature'), Temperature())
 
      asyncio.Task(aiocoap.Context.create_server_context(root))
 
      asyncio.get_event_loop().run_forever()
  
  else:
    print('Invalid selection. Re-run program to try again.')
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
  
  
  
#contextClient = await Context.create_client_context() #context for sending PUTs and GETs

#contextServer = await Context. create_server_context() #context for receiving PUTs and GETs

