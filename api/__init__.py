global __API_PROTOCOL__
global __SERVER_PORT__
global __WEBSOCKET_CALLBACK__
global __WEBSOCKET_ALIVE__
global __DEBUG__
global __MESSAGE_POOL__

__API_PROTOCOL__ = 1

import api
import asyncio
from threading import Thread
from .server import run
from .utils import get_host_ip

def start_api_server(queue, debug, port = 12346):
    api.__SERVER_PORT__ = port
    api.__DEBUG__ = debug
    api.__WEBSOCKET_ALIVE__ = False
    api.__MESSAGE_POOL__ = queue
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if(debug):
        print("API Server Enabled")
        print("API is now serving on http://%s:%d\n" % (get_host_ip(), __SERVER_PORT__))
    
    Thread(target=wait_websocket_info, args=[api.__MESSAGE_POOL__]).start()
    run()

def wait_websocket_info(queue):
    while True:
        websocket = queue.get()
        api.__WEBSOCKET_CALLBACK__ = websocket
        api.__WEBSOCKET_ALIVE__ = True
