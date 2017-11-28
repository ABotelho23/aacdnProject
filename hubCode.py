import datetime
import logging
import asyncio
import aiocoap

contextClient = await Context.create_client_context() #context for sending PUTs and GETs

contextServer = await Context. create_server_context() #context for receiving PUTs and GETs

