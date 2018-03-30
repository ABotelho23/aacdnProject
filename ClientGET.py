import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():

    addressIn = input("Target?")
    resourceIn = input ("Resource? (Include initial slash, and no ending slash.)")

    protocol = await Context.create_client_context()

    targetURI = 'coap://' + addressIn + resourceIn

    request = Message(code=GET, uri=targetURI)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
