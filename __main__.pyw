# -*- coding: utf-8 -*-  

# Copyright 2018 Dalvik Shen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from http.server import *
from urllib.parse import urlparse
import signal
import sys
import re
import html
import os
import pyperclip

_SERVER_PORT = 12345
_DEBUG = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def signal_handler(sig, frame):
    log("SIGINT exit")
    httpd.server_close()
    sys.exit(0)
    
def log(packet):
    if _DEBUG:
        print(packet)

def processData(postvars):
    # 更换莫名的空格成空格
    postvars = postvars.replace(b'\xe3\x80\x80', b'\x20').decode("utf-8")
    # 删掉行号
    postvars = re.sub(r"<div *class= *\" *glLineNumber *\">\d+ *</div>(\d{,3})?(\))?", "" , postvars)
    # 处理换行
    postvars = postvars.replace("<br>", "\n")
    # 替换中文符号
    postvars = re.sub(r"(“|”)", r"\"" , postvars)
    postvars = re.sub(r"(‘|’)", r"\'" , postvars)
    postvars = postvars.replace("（", "(")
    postvars = postvars.replace("）", ")")
    # 取消 HTML 实体
    postvars = html.unescape(postvars)
    pyperclip.copy(postvars)
    log("\n======== 已复制 ========\n")
    log(postvars)
    if (_DEBUG):
        exit(0)

def setupServer():
    os.system('cls')
    print(bcolors.WARNING)
    print("\
	    ___      _       _ _        __ _                \n\
	   /   \\__ _| |_   ___) | __   / _\\ |__   ___ _ __  \n\
	  / /\\ / _` | \\ \\ / / | |/ /   \\ \\| '_ \\ / _ \\ '_ \\ \n\
	 / /_// (_| | |\\ V /| |   <    _\\ \\ | | |  __/ | | |\n\
	/___,' \\__,_|_| \\_/ |_|_|\\_\\   \\__/_| |_|\\___|_| |_|\n\
			")
    print(bcolors.ENDC)
    class RequestHandler(BaseHTTPRequestHandler):
        def do_OPTIONS(self):           
            self.send_response(200, "ok") 
            self.send_header('Access-Control-Allow-Origin', '*')                
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header("Access-Control-Allow-Headers", "x-content-length")
            self.end_headers()

        def do_GET(self):
            self.send_response(405)
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Access-Control-Allow-Headers", "x-content-length")
            self.end_headers()
            self.wfile.write("405 method not allowed".encode('utf-8'))

        def do_POST(self):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Access-Control-Allow-Headers", "x-content-length")
            self.end_headers()
            length = int(self.headers.get('x-content-length'))
            processData(self.rfile.read(length))
            return

        def log_message(self, format, *args):
            if (_DEBUG):
                print(format % args)
            return
        
    httpd = HTTPServer(('127.0.0.1', _SERVER_PORT), RequestHandler)
    while(True):
        httpd.handle_request()

signal.signal(signal.SIGINT, signal_handler)
print("正在关闭学生端...")
os.system('taskkill /f /im studentMain.exe')
print("正在启动服务...")
setupServer()