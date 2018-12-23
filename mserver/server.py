from .logic import processData
import websockets
import asyncio
import mserver

def run():
    # Websocket Parse Server
    server = websockets.serve(processData, 'localhost', mserver.__SERVER_PORT__)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()