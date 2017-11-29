import datetime
import logging
import asyncio
import aiocoap

async def main():
  
  protocol = await Context.create_client_context()

  request = Message(code=GET, uri='coap://10.0.0.104/test')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
  
  
  
#contextClient = await Context.create_client_context() #context for sending PUTs and GETs

#contextServer = await Context. create_server_context() #context for receiving PUTs and GETs

