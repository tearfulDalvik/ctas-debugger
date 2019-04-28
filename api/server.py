from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import api
import asyncio


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_header("Server", "Dalvik\'s CTAS API Server")
        if self.path == '/handshake':
            self.send_response(200)
            self.send_header("Server", "Dalvik\'s CTAS API Server")
            self.end_headers()
            self.wfile.write(json.dumps({"version": api.__API_PROTOCOL__, "status": "ok",
                                         "message": "hello from the CTAS server"}, sort_keys=True).encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("400 Bad Request".encode('utf-8'))
    def do_HEAD(self):
        self.send_header("Server", "Dalvik\'s CTAS API Server")
        if self.path == '/answer/a':
            self.send_anwser(0)
        elif self.path == '/answer/b':
            self.send_anwser(1)
        elif self.path == '/answer/c':
            self.send_anwser(2)
        elif self.path == '/answer/d':
            self.send_anwser(3)
        elif self.path == '/action/previous':
            self.send_action("previous")
        elif self.path == '/action/to_top':
            self.send_action("to_top")
        elif self.path == '/action/to_bottom':
            self.send_action("to_bottom")
        elif self.path == '/action/next':
            self.send_action("next")
        elif self.path == '/action/run':
            self.send_action("run")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("400 Bad Request".encode('utf-8'))

    async def send_websocket_message(self, message):
        if (api.__WEBSOCKET_ALIVE__):
            await api.__WEBSOCKET_CALLBACK__.send(message)

    def log_message(self, format, *args):
        if(api.__DEBUG__):
            print(format % args)
        return

    def send_anwser(self, which):
        asyncio.get_event_loop().run_until_complete(self.send_websocket_message(
            json.dumps({"req": "answer", "content": which}, sort_keys=True)))
        self.send_response(200 if api.__WEBSOCKET_ALIVE__ else 503)
        self.send_header("Server", "Dalvik\'s CTAS API Server")
        self.end_headers()

    def send_action(self, which):
        asyncio.get_event_loop().run_until_complete(self.send_websocket_message(
            json.dumps({"req": "action", "content": which}, sort_keys=True)))
        self.send_response(200 if api.__WEBSOCKET_ALIVE__ else 503)
        self.send_header("Server", "Dalvik\'s CTAS API Server")
        self.end_headers()


def run():
    httpd = HTTPServer(('0.0.0.0', api.__SERVER_PORT__), RequestHandler)
    while(True):
        httpd.handle_request()
