from .server import run
import asyncio
import mserver

global __SERVER_PORT__
__SERVER_PORT__ = 12345
global __MESSAGE_POOL__
global __PROTOCOL_VER__
__PROTOCOL_VER__ = 2

global __DEBUG__
global __WEBSOCKET_SERVER__
global __SERVER_AVAILABLE__
__SERVER_AVAILABLE__ = False

def start_server(queue, debug, port = __SERVER_PORT__):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    mserver.__DEBUG__ = debug
    mserver.__MESSAGE_POOL__ = queue
    mserver.__SERVER_PORT__ = port

    run()