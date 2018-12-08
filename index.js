let prect_counter = 0;
$("#ProgramContent").bind("DOMSubtreeModified", function () {
    // Triggered Twice
    $('#inject').text("正在载入... 💀已做：" + getPrecticeDone() + "题");
    call()
})
$('#divProgram').append("<p id='inject'>Dalvik's Here</p>")
$('#page').append("<style>.glLineNumber {user-select: none !important;} </style>");
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

function call() {
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
                $('#inject').text("√ 已复制 💀已做：" + getPrecticeDone() + "题")
            },
            500: function () {
                alert("× 无法解析本题 💀已做：" + getPrecticeDone() + "题");
            }
        },
        error: function () {
            $('#inject').text("× 无法连接到解析器 💀已做：" + getPrecticeDone() + "题")
        }
    });
}