from .server import run
import mserver
import asyncio

global __PROTOCOL_VER__
__PROTOCOL_VER__ = 2
global __SERVER_PORT__
__SERVER_PORT__ = 12345

global __DEBUG__

def start_server(debug = False, port = __SERVER_PORT__):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    mserver.__DEBUG__ = debug
    mserver.__SERVER_PORT__ = port
    run()