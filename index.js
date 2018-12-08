let prect_counter = 0;
$("#ProgramContent").bind("DOMSubtreeModified", function () {
    // Triggered Twice
    call()
})
$('#divProgram').append("<p id='inject'>Dalvik's Here</p>")
$('.page').append("<style>.glLineNumber {user-select: none !important;} .href-retry {color: blue !important;} .href-retry:hover {opacity: .7 !important;}</style>");
call();

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
        $('#inject').append("&nbsp;&nbsp;<a class=\"href-retry\" onclick=\"call()\" href=\"javascript:;\">重试</a>");
    }
}

function call() {
    printMessage("", "正在载入...");
    const data = $("#ProgramContent").html()
    if (data.length == 0) return;
    $.ajax({
        type: "POST",
        url: 'http://localhost:12345',
        data: data,
        beforeSend: function (request) {
            request.setRequestHeader("x-content-length", getByteCount(data));
        },
        statusCode: {
            200: function () {
                printMessage("√", "已复制");
            },
            500: function () {
                printMessage("×", "无法解析本题", true);
            }
        },
        error: function () {
            printMessage("×", "无法连接到解析器", true)
        }
    });
}