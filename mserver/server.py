from .logic import processData
import websockets
import asyncio
import mserver

def run():
    # Websocket Parse Server
    mserver.__WEBSOCKET_SERVER__ = websockets.serve(processData, 'localhost', mserver.__SERVER_PORT__)
    mserver.__SERVER_AVAILABLE__ = True
    asyncio.get_event_loop().run_until_complete(mserver.__WEBSOCKET_SERVER__)
    asyncio.get_event_loop().run_forever()