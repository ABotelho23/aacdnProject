import datetime
import logging
import asyncio
import dbus
#import avahi
import threading
import aiocoap.resource as resource
from aiocoap import *
import aiocoap

async def main():
    targetURI = 'coap://10.0.0.103/thermo/temp'
    #_await = asyncio.get_event_loop().run_until_complete

    _await = asyncio.new_event_loop()
    asyncio.set_event_loop(_await)

    ctx = _await(Context.create_client_context())
    asyncio.get_event_loop().run_forever()

    request = Message(code=GET, uri=targetURI)
    print('Test')
    
    try:
     response = _await(ctx.request(...).response)
    except Exception as e:
      print('Failed to fetch resource:')
      print(e)
      return "ERROR BLAHHHHHHH"
    else:
      print('Result: %s\n%r'%(response.code, response.payload))

      return response.payload
