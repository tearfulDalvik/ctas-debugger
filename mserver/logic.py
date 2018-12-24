
import platform
from urllib.parse import urlparse
import pyperclip
import json
import html
import os
import re
import subprocess
import mserver

run_dir = os.getcwd()
async def processData(websocket, path):
    while True:
        data = json.loads(await websocket.recv())
        mserver.__MESSAGE_POOL__.put(websocket)
        try:
            if(data['proto'] != mserver.__PROTOCOL_VER__) :
                raise Exception('Protocol Version Mismatch')
        except Exception as e:
            await websocket.send(json.dumps({"req": "error", "status": 400, "seq": data['seq'], "reason": repr(e)}, sort_keys=True))
            websocket.close()
            return
        if (data['req'] == 'question'):
            postvars = data['content']
            # 更换莫名的空格成空格
            postvars = postvars.encode("utf-8").replace(b'\xe3\x80\x80', b'\x20').decode("utf-8")

            if(mserver.__DEBUG__):
                print(postvars)
            # 删掉行号
            postvars = re.sub(r"<div *class= *\" *glLineNumber *\">\d+\D+ *?<\/div>(\d{,3})?(\)|）|\.)?", "" , postvars)
            # 处理用户编辑
            postvars = postvars.replace("<div>", "\n")
            postvars = postvars.replace("</div>", "")
            # 处理换行
            postvars = postvars.replace("<br>", "\n")
            # 替换中文符号
            postvars = re.sub(r"(“|”)", r"\"" , postvars)
            postvars = re.sub(r"(‘|’)", r"\'" , postvars)
            postvars = postvars.replace("（", "(")
            postvars = postvars.replace("；", ";")
            postvars = postvars.replace("）", ")")
            # 取消 HTML 实体
            postvars = html.unescape(postvars)
            # 更正 main 函数签名
            postvars = postvars.replace("void main(", "int main(")
            postvars = postvars.replace("#include \"stdafx.h\"\n", "")
            pyperclip.copy(postvars)
            if(mserver.__DEBUG__):
                print("\n============= 已复制 =============\n")

            # 清理运行环境
            try:
                if not os.path.exists("{}/cache".format(run_dir)):
                    os.makedirs("{}/cache".format(run_dir))
                for file in os.scandir("{}/cache".format(run_dir)):
                    os.unlink(file.path)
            except OSError:
                pass

            # 判断是否是多文件
            matcher = re.compile(r'\w+\.(h|cpp)(?!")')
            files = []
            fileNames = []
            fileParts = []
            startPos = 0
            endPos = 0
            for fileMatch in matcher.finditer(postvars):
                fileNames.append(fileMatch.group())
                # 每次循环都将开始指针重定向到上次结束的地方
                startPos = endPos
                endPos = 0
                lineStart = postvars[0: fileMatch.start()].rfind("\n")
                if (lineStart == -1):
                    # 找不到上一个换行符，则此时在第一行
                    startPos = 0
                else:
                    # 找到了上一个换行符，这就是上一个文件的所有代码
                    endPos = postvars[0: fileMatch.start()].rfind("\n")
                if (startPos < endPos):
                    # 仅当开始指针小于结束指针时写入缓冲区，此时数据已经准备完毕
                    fileParts.append(postvars[startPos: endPos])
                if(mserver.__DEBUG__):
                    print(str(startPos)+ "|"+str(endPos))
            # 将剩余部分写入
            fileParts.append(postvars[endPos: len(postvars)])

            # 现在将文件名和内容对应起来，上面只是做好了内容分割，但是可能会过度分割
            if (fileNames):
                # 多文件
                namePos = 0
                tempBody = ""
                for part in fileParts:
                    if (namePos >= len(fileNames)):
                        break
                    haveKeyword = matcher.search(part)
                    tempBody = tempBody + part
                    if (haveKeyword is not None):
                        files.append({"fileName": fileNames[namePos], "content": tempBody})
                        namePos = namePos + 1
                        tempBody = ''
                for fileContent in files:
                    f = open("{}/cache/{}".format(run_dir, fileContent["fileName"]), "w")
                    f.write(fileContent["content"])
                    f.flush()
            else:
                # 单文件，全部写入
                f = open("{}/cache/problem.cpp".format(run_dir), "w")
                f.write(postvars)
                f.flush()
            await websocket.send(json.dumps({"req": "question", "status": 200, "seq": data['seq']}, sort_keys=True))
        elif(data['req'] == "runProgram"):
            try:
                if(platform.system() == "Darwin"):
                    state = subprocess.run("chmod +x {}/scripts/run-Darwin && open {}/scripts/run-Darwin".format(run_dir, run_dir), shell=True).returncode == 0
                    await websocket.send(json.dumps({"req": "compile", "seq": data['seq'], "status": 200 if state else 500}, sort_keys=True))
                elif(platform.system() == "Windows"):
                    state = subprocess.run("start cmd /c {}/scripts/run-Windows".format(run_dir), shell=True).returncode == 0
                    await websocket.send(json.dumps({"req": "compile", "seq": data['seq'], "status": 200 if state else 500}, sort_keys=True))
                else:
                    await websocket.send(json.dumps({"req": "compile", "seq": data['seq'], "status": 503}, sort_keys=True))
            except Exception as e:
                print("error occurred: %s" % str(e))
                exit(0)