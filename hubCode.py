import datetime
import logging
import asyncio
from aiocoap import *

async def main():
  
  selection = input("1. GET\n2. PUT \n\n")
  
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
  
  else:
    
    context = await Context.create_client_context()
    
    payload = input("What is the paylod?")
    payload.encode()
    request = Message(code=PUT, payload=payload)
    # These direct assignments are an alternative to setting the URI like in
    # the GET example:
    request.opt.uri_host = '10.0.0.101'
    request.opt.uri_path = ("test")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
  
  
  
#contextClient = await Context.create_client_context() #context for sending PUTs and GETs

#contextServer = await Context. create_server_context() #context for receiving PUTs and GETs

