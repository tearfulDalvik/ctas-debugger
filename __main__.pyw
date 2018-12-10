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
import platform
import pyperclip
import asyncio
import json
import websockets

_SERVER_PORT = 12345
_DEBUG = False

server = False

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
    sys.exit(0)
    
def log(packet):
    if _DEBUG:
        print(packet)

async def processData(websocket, path):
    while True:
        data = json.loads(await websocket.recv())
        if (data['req'] == 'question'):
            postvars = data['content']
            # 更换莫名的空格成空格
            postvars = postvars.encode("utf-8").replace(b'\xe3\x80\x80', b'\x20').decode("utf-8")
            # 删掉行号
            postvars = re.sub(r"<div *class= *\" *glLineNumber *\">\d+ *</div>(\d{,3})?(\))?", "" , postvars)
            postvars = postvars.replace("<div>", "\n")
            postvars = postvars.replace("</div>", "")
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
            f = open("cache/problem.cpp", "w")
            f.write(postvars)
            await websocket.send(json.dumps({"req": "question", "status": 200}, sort_keys=True))
        elif(data['req'] == "runProgram"):
            try:
                state = os.system("g++ cache/problem.cpp -o cache/problem") == 0
                await websocket.send(json.dumps({"req": "compile", "status": 200 if state else 500}, sort_keys=True))
                if(platform.system() == "Darwin"):
                    os.system('open cache/problem')
            except:
                
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
    server = websockets.serve(processData, 'localhost', 12345)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

signal.signal(signal.SIGINT, signal_handler)
print("正在关闭学生端...")
os.system('taskkill /f /im studentMain.exe')
print("正在启动服务...")
setupServer()