let prect_counter = 0;
let alive = false;
let websocket = null;
const proto_ver = 2;

// Whether override message by closed or disconnected
let leaveMessage = false;

connect();

$("#ProgramContent").bind("DOMSubtreeModified", function () {
    // Triggered Twice
    prect_counter++;
    sendQuestion();
})
$('#divProgram').append("<div id=\"ctas-inject\"><p id=\"ctas-msg\">🚴‍Loading</p></div>")

document.getElementById("ProgramContent").designMode = "on"
document.getElementById("ProgramContent").contentEditable = "true"

$('.page').append("<style>\
.glLineNumber {\
    user-select: none !important;\
} \
.ctas-href-action \{\
    color: rgba(233, 39, 100, 1.000) !important;\
}\
.ctas-href-action:hover {\
    opacity: .7 !important;\
}\
#ctas-inject { \
    background: rgba(0,0,0,.04);\
    border-radius: 20px;\
} \
#ctas-msg {\
    padding: 1vmin 2vmin;\
}\
td:last-child:after { \
    content: \"© Dalvik Shen 2018 | CTAS-Debugger v1.2.41\";\
    opacity: .3;font-size: .8em;\
}\
</style>");

function getPrecticeDone() {
    console.log(prect_counter);
    return prect_counter % 2 == 0 ? prect_counter / 2 : (prect_counter + 1) / 2;
}

function getByteCount(s) {
    var count = 0,
        stringLength = s.length,
        i;
    s = String(s || "");
    for (i = 0; i < stringLength; i++) {
        var partCount = encodeURI(s[i]).split("%").length;
        count += partCount == 1 ? 1 : partCount - 1;
    }
    return count;
}

function printError(message) {
    printMessage("×", message, "重试", "connect");
}

function printMessage(icon, message, action= false, func = "") {
    $('#ctas-msg').text(icon + " " + message + " 💀已做：" + getPrecticeDone() + "题")
    if(action) {
        $('#ctas-msg').append(`&nbsp;&nbsp;<a class=\"ctas-href-action\" onclick=\"${func}()\" href=\"javascript:;\">${action}</a>`);
    }
}

function runProgram() {
    if(!alive)  return;
    printMessage("√", "已提交运行");

    websocket.send(JSON.stringify({
        'req': "runProgram",
        'proto': proto_ver
    }));
}

function connect() {
    if(!alive) {
        const wsUri = "ws://[::1]:12345/";
        websocket = new WebSocket(wsUri);
        websocket.onopen = function(evt) { 
            alive = true;
            sendQuestion()
        };
        websocket.onclose = function(evt) {
            alive = false;
            if (leaveMessage) return;
            switch (evt.code) {
                case 1006:
                    printError("已断开")
                    break;
                case 1000:
                    printError("已关闭")
                    break;
                default:
                    printError("未知错误")
            }
        };
        
        websocket.onmessage = function(evt) {
            handleMessage(evt)
        };
        websocket.onerror = function(evt) {
            alive = false;
            printError("无法连接到解析器")
        };
    }
}

function handleMessage(evt) {
    leaveMessage = false;
    const serverResponse = JSON.parse(evt.data);
    if (serverResponse.seq != getPrecticeDone()) return;
    switch (serverResponse.req) {
        case "question":
            switch(serverResponse.status) {
                case 200:
                    printMessage("√", "已复制", "运行", "runProgram");
                    break;
                case 500:
                    printError("无法解析本题");
                    break;
                default:
                    printError("无效回应");
            }
            break;
        case "compile":
            switch(serverResponse.status) {
                case 200:
                    printMessage("√", "正在运行", "重新运行", "runProgram");
                    break;
                case 500:
                    printMessage("×", "编译时出现错误", "重新运行", "runProgram");
                    break;
                case 503:
                    printMessage("×", "平台不受支持");
                    break;
                default:
                    printError("无效回应");
            }
            break;
        case "error":
            leaveMessage = true;
            printError(serverResponse['reason']);
    }
}

function sendQuestion() {
    const data = $("#ProgramContent").html()
    if(!alive) {
        printError("未连接");
        return;
    }
    if(data.length == 0)  return;
    printMessage("", "正在载入...");

    websocket.send(JSON.stringify({
        'req': "question",
        'length': getByteCount(data),
        'content': data,
        'seq': getPrecticeDone(),
        'proto': proto_ver
    }));
}

var el = document.body;
var listOfEvents=[];  
var attributes = [].slice.call(el.attributes);  

for (i = 0; i < attributes.length; i++){
    var att= attributes[i].name; 

   if(att.indexOf("on")===0){
     var eventHandlers={};
     eventHandlers.attribute=attributes[i].name;
     eventHandlers.value=attributes[i].value;
     listOfEvents.push(eventHandlers);
     el.attributes.removeNamedItem(att);             
   }     
} 