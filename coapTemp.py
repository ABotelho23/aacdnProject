import datetime
import logging
import asyncio
import dbus
#import avahi
import threading
import aiocoap.resource as resource
from aiocoap import *
import aiocoap

def main():
    targetURI = 'coap://10.0.0.103/thermo/temp'
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri=targetURI)

    try:
      response = await protocol.request(request).response
    except Exception as e:
      print('Failed to fetch resource:')
      print(e)
      return "ERROR BLAHHHHHHH"
    else:
      print('Result: %s\n%r'%(response.code, response.payload))

      return response.payload
