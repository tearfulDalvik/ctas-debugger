let prect_counter = 0;
$("#ProgramContent").bind("DOMSubtreeModified", function () {
    // Triggered Twice
    sendQuestion()
})
$('#divProgram').append("<p id='inject'>🚴‍ &copy; Dalvik Shen 2018</p>")
$('.page').append("<style>.glLineNumber {user-select: none !important;} .href-retry { color: rgba(233, 39, 100, 1.000) !important;} .href-retry:hover {opacity: .7 !important;} #inject { background: rgba(0,0,0,.04);border-radius: 20px;padding: 1vmin 2vmin;}</style>");

let alive = false;
let websocket = null;
connect();

function getPrecticeDone() {
    return prect_counter++ % 2 == 0 ? (prect_counter + 1) / 2 : prect_counter / 2;
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

function printMessage(icon, message, retry = false) {
    $('#inject').text(icon + " " + message + " 💀已做：" + getPrecticeDone() + "题")
    if(retry) {
        $('#inject').append("&nbsp;&nbsp;<a class=\"href-retry\" onclick=\"connect()\" href=\"javascript:;\">重试</a>");
    }
}

function connect() {
    if(!alive) {
        const wsUri = "ws://localhost:12345/";
        websocket = new WebSocket(wsUri);
        websocket.onopen = function(evt) { 
            alive = true;
            sendQuestion()
        };
        websocket.onclose = function(evt) {
            alive = false;
            console.log(evt);
            switch (evt.code) {
                case 1006:
                    printMessage("×", "没有运行", true)
                    break;
                case 1000:
                    printMessage("×", "没有运行", true)
                    break;
                default:
                    printMessage("×", "未知错误", true)
            }
        };
        
        websocket.onmessage = function(evt) {
            handleMessage(evt)
        };
        websocket.onerror = function(evt) {
            alive = false;
            printMessage("×", "无法连接到解析器", true)
        };
    }
}

function handleMessage(evt) {
    const serverResponse = JSON.parse(evt.data);
    if (serverResponse.req === "question") {
        switch(serverResponse.status) {
            case 200:
                printMessage("√", "已复制");
                break;
            case 500:
                printMessage("×", "无法解析本题", true);
                break;
            default:
                printMessage("×", "无效回应", true);
        }
    }
}

function sendQuestion() {
    const data = $("#ProgramContent").html()
    if(!alive || data.length == 0)  return;
    printMessage("", "正在载入...");

    websocket.send(JSON.stringify({
        'req': "question",
        'length': getByteCount(data),
        'content': data,
    }));
}