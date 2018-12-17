global __API_PROTOCOL__
global __SERVER_PORT__
global __WEBSOCKET_CALLBACK__
global __WEBSOCKET_ALIVE__
global __DEBUG__

import api
from .server import run
from .utils import get_host_ip

api.__API_PROTOCOL__ = 1

def start_api_server(debug, port = 12346):
    api.__SERVER_PORT__ = port
    api.__DEBUG__ = debug
    api.__WEBSOCKET_ALIVE__ = False
    if(debug):
        print("API Server Enabled")
    print("API server listening on http://%s:%d" % (get_host_ip(), __SERVER_PORT__))
    run()

def update_websocket_info(websocket):
    api.__WEBSOCKET_CALLBACK__ = websocket
    api.__WEBSOCKET_ALIVE__ = True
