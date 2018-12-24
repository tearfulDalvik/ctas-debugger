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

import signal
import sys
import os
import api
import mserver
from queue import Queue
from threading import Thread

global __DEBUG__ 
__DEBUG__ = True

_API_SERVER = True

global __SERVER_PORT__
__SERVER_PORT__ = 12345

global __API_SERVER_PORT__
__API_SERVER_PORT__ = 12346


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
    sys.exit(0)

def setupServer():
    os.system('cls')
    os.system('clear')
    print(bcolors.OKBLUE + "CTAS Debugger Server\n(C) Dalvik Shen 2018. All Rights Reserved. Prohibition of distribution.\n")
    print(bcolors.WARNING)
    print("\
	    ___      _       _ _        __ _                \n\
	   /   \\__ _| |_   ___) | __   / _\\ |__   ___ _ __  \n\
	  / /\\ / _` | \\ \\ / / | |/ /   \\ \\| '_ \\ / _ \\ '_ \\ \n\
	 / /_// (_| | |\\ V /| |   <    _\\ \\ | | |  __/ | | |\n\
	/___,' \\__,_|_| \\_/ |_|_|\\_\\   \\__/_| |_|\\___|_| |_|\n\
			")
    print(bcolors.ENDC)
    queue = Queue()
    # Main Server
    Thread(target=mserver.start_server, args=[queue, __DEBUG__]).start()
    # API Server
    if(_API_SERVER):
        Thread(target=api.start_api_server, args=[queue, __DEBUG__]).start()

signal.signal(signal.SIGINT, signal_handler)
print("正在关闭学生端...")
os.system('taskkill /f /im studentMain.exe')
print("正在启动服务...")
setupServer()