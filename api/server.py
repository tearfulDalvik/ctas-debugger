from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import api
import asyncio

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/handshake':
            self.send_response(200)
            self.send_header("Server", "Dalvik\'s CTAS API Server")
            self.end_headers()
            self.wfile.write(json.dumps({"version": api.__API_PROTOCOL__, "status": "ok", "message": "hello from the CTAS server"}, sort_keys=True).encode("utf-8"))
        elif self.path == '/answer/a':
            self.send_websocket_message(json.dumps({"req": "answer", "content": "A"} , sort_keys=True))
            api.__WEBSOCKET_CALLBACK__.close()
            self.send_response(200 if api.__WEBSOCKET_ALIVE__  else 503)
            self.send_header("Server", "Dalvik\'s CTAS API Server")
            self.end_headers()
            self.wfile.write(json.dumps({"version": api.__API_PROTOCOL__, "status": "ok", "message": ""}, sort_keys=True).encode("utf-8"))
        else :
            self.send_response(400)
            self.end_headers()
            self.wfile.write("400 Bad Request".encode('utf-8'))

    async def send_websocket_message(self, message):
        if (api.__WEBSOCKET_ALIVE__):
            await api.__WEBSOCKET_CALLBACK__.send(message);

    def log_message(self, format, *args):
        if(api.__DEBUG__):
            print(format % args)
        return

def run():
    httpd = HTTPServer(('0.0.0.0', api.__SERVER_PORT__), RequestHandler)
    while(True):
        httpd.handle_request()