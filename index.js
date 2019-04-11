const proto_ver = 2;

class Client {
  websocket = null;
  // Counts questions passed.
  prect_counter = 0;
  // Is websocket or program is alive?
  alive = false;
  // Whether override message by closed or disconnected
  leaveMessage = false;
  display = null;

  constructor(display) {
    this._init();
    this.connect();
    this.display = display;
  }

  /**
   * This function will initialize hooks and render essential components.
   */
  _init() {
    // Bind question counter
    let me = this;
    $("#ProgramContent").bind("DOMSubtreeModified", function() {
      // Triggers twice
      me.prect_counter++;
      me.sendQuestion();
    });

    // Keep comprehensive hint for wrong answer
    try {
      $("#cAnswerSummary").bind("DOMSubtreeModified", function() {
        $("#ctas-msg2").text("解析：" + $("#cAnswerSummary").text());
      });
    } catch (ignored) {}
    // Inject Status Bar
    $("#divProgram").append(
      '<div id="ctas-inject" ctas-panel-expanded=false>\
          <p id="ctas-msg">🚴‍Loading</p>\
          <div class="ctas-setting-panel">\
              <a class="ctas-href-action" href="javascript:display.toggleDarkMode();">切换暗黑模式</a>\
          </div>\
          <p id="ctas-msg2"></p>\
      </div>'
    );
  }

  /**
   * To get whether the service is running correctly
   */
  get isAlive() {
    return this.alive;
  }

  disconnect() {
    if (this.isAlive) {
      this.websocket.close();
      this.alive = false;
      this.leaveMessage = true;
      display.printMessage("∥", "已暂停", "▹ 开始", "connect");
    }
  }

  runProgram() {
    if (!this.isAlive) return;
    display.printMessage("√", "已提交运行");

    let me = this;
    this.websocket.send(
      JSON.stringify({
        req: "runProgram",
        seq: me.getPrecticeDone(),
        proto: proto_ver
      })
    );
  }

  connect() {
    if (!this.isAlive) {
      let me = this;
      const wsUri = "ws://[::1]:12345/";
      this.websocket = new WebSocket(wsUri);
      this.websocket.onopen = function(evt) {
        me.alive = true;
        me.sendQuestion();
      };
      this.websocket.onclose = function(evt) {
        me.alive = false;
        if (me.leaveMessage) return;
        switch (evt.code) {
          case 1006:
            display.printError("已断开");
            break;
          case 1000:
            display.printError("已关闭");
            break;
          default:
            display.printError("未知错误");
        }
      };

      this.websocket.onmessage = function(evt) {
        me.handleMessage(evt);
      };
      this.websocket.onerror = function(evt) {
        me.alive = false;
        display.printError("无法连接到解析器");
      };
    }
  }

  handleMessage(evt) {
    this.leaveMessage = false;
    const serverResponse = JSON.parse(evt.data);
    if (serverResponse.seq && serverResponse.seq != this.getPrecticeDone())
      return;
    switch (serverResponse.req) {
      case "question":
        switch (serverResponse.status) {
          case 200:
            display.printMessage("√", "已复制", "运行", "runProgram");
            break;
          case 500:
            display.printError("无法解析本题");
            break;
          default:
            display.printError("无效回应");
        }
        break;
      case "compile":
        switch (serverResponse.status) {
          case 200:
            display.printMessage("√", "正在运行", "重新运行", "runProgram");
            break;
          case 500:
            display.printMessage(
              "×",
              "编译时出现错误",
              "重新运行",
              "runProgram"
            );
            break;
          case 503:
            display.printMessage("×", "平台不受支持");
            break;
          default:
            display.printError("无效回应");
        }
        break;
      case "answer":
        $(
          ".chosenItem:nth-child(" + (serverResponse.content + 1) + ")"
        ).click();
        break;

      case "action":
        switch (serverResponse.content) {
          case "run":
            client.runProgram();
            break;

          case "to_top":
            window.scrollTo(0, 0);
            break;

          case "to_bottom":
            window.scrollTo(0, document.body.scrollHeight);
            break;

          case "previous":
            previousQuestion();
            break;

          case "next":
            nextQuestion();
            break;
        }
        break;

      case "error":
        this.leaveMessage = true;
        printError(serverResponse["reason"]);
    }
  }

  sendQuestion() {
    const data = $("#ProgramContent").html();
    if (!this.isAlive) {
      if (!this.leaveMessage) display.printError("未连接");
      return;
    }
    if (data.length == 0) return;
    display.printMessage("", "正在载入...");
    let me = this;
    this.websocket.send(
      JSON.stringify({
        req: "question",
        length: me.getByteCount(data),
        content: data,
        seq: me.getPrecticeDone(),
        proto: proto_ver
      })
    );
  }

  getPrecticeDone() {
    return this.prect_counter % 2 == 0
      ? this.prect_counter / 2
      : (this.prect_counter + 1) / 2;
  }

  getByteCount(s) {
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
}

console.log(
  "%cCTAS Debugger Client\n(C) Dalvik Shen 2018. All Rights Reserved. Prohibition of distribution.",
  "color:grey;"
);

/**
 * This class will handle user interactions
 */
class Interaction {
  constructor() {
    this.bindShortcuts();
  }
  /**
   * This function binds keyboard shortcuts.
   */
  bindShortcuts() {
    document.onkeypress = function(e) {
      // Ignore if user is editing code
      e = e || window.event;
      if ($("#ProgramContent").is(":focus")) return;
      var charCode = typeof e.which == "number" ? e.which : e.keyCode;
      if (charCode) {
        switch (charCode) {
          // Q
          case 113:
            $(".chosenItem:nth-child(1)").click();
            break;
          // W
          case 119:
            $(".chosenItem:nth-child(2)").click();
            break;
          // E
          case 101:
            $(".chosenItem:nth-child(3)").click();
            break;
          // R
          case 114:
            $(".chosenItem:nth-child(4)").click();
            break;
          // A
          case 97:
            previousQuestion();
            break;
          // S
          case 115:
            nextQuestion();
            break;
          // T
          case 116:
            client.runProgram();
            break;

          // G which is to-bottom action in vim
          case 71:
            window.scrollTo(0, document.body.scrollHeight);
            break;

          // gg is to-top action in vim. We recognize it by once.
          case 103:
            window.scrollTo(0, 0);

          default:
            console.log(charCode);
        }
      }
    };
  }
}
/**
 * This is basically a toolkit class, which provides subsidiary functions
 */
class Display {
  constructor() {
    this.clearPageLimits();
    this.toggleEditMode();
    this.appendStyles();
  }

  toggleDarkMode() {
    $("html").attr(
      "ctas-darkmode",
      $("html").attr("ctas-darkmode") == "false" ? "true" : "false"
    );
  }

  /**
   * To unlock most of features like copying and selecting on page.
   */
  clearPageLimits() {
    var el = document.body;
    var listOfEvents = [];
    var attributes = [].slice.call(el.attributes);

    for (var i = 0; i < attributes.length; i++) {
      var att = attributes[i].name;

      if (att.indexOf("on") === 0) {
        var eventHandlers = {};
        eventHandlers.attribute = attributes[i].name;
        eventHandlers.value = attributes[i].value;
        listOfEvents.push(eventHandlers);
        el.attributes.removeNamedItem(att);
      }
    }
  }

  /**
   * To make the contents in showcase can be edited.
   */
  toggleEditMode() {
    document.getElementById("ProgramContent").designMode = "on";
    document.getElementById("ProgramContent").contentEditable = "true";
  }

  /**
   * This function will append necessary styles which CTAS-Client depends on..
   */
  appendStyles() {
    $(".page").append(
      '<style>\
  .glLineNumber {\
      user-select: none !important;\
  } \
  /** Setting Panel **/\
  #ctas-inject[ctas-panel-expanded=false] > .ctas-setting-panel {\
      display: none;\
  }\
  .ctas-href-action {\
      color: rgba(233, 39, 100, 1.000) !important;\
      border: solid rgba(25,25,25, .1) 1px;\
      border-radius: 3px;\
      padding: .6vmin 1.5vmin !important;\
      background: rgba(255,255,255,.5) !important;\
  }\
  .ctas-href-action:hover {\
      opacity: .7 !important;\
  }\
  tr > :first-child > div > div {\
      position: fixed;\
  }\
  #ctas-msg {\
      display: flex;\
      flex-flow: row;\
      align-items: baseline;\
  }\
  #ctas-msg :nth-child(3) {\
      margin-left: auto;\
  }\
  #ctas-inject { \
      background: rgba(0,0,0,.04);\
      border-radius: 6px;\
      margin: 2vmin 0;\
      box-shadow: 0 3px 1px -2px rgba(0,0,0,.2), 0 2px 2px 0 rgba(0,0,0,.14), 0 1px 5px 0 rgba(0,0,0,.12);\
  } \
  #ctas-inject > * {\
      padding: 1vmin 2vmin;\
      color: #666666;\
  }\
  #ctas-inject > :last-child {\
      background: rgba(0,0,0, .1);\
      margin-top: 0px;\
      padding-top: .5vmin;\
      border-radius: 0 0 6px 6px;\
      padding-bottom: .5vmin;\
      color: #444444;\
  }\
  #ctas-inject > :not(:last-child) {\
      padding-bottom: 0;\
      margin-bottom: 1vmin;\
  }\
  td:last-child:after { \
      content: "© Dalvik Shen 2018 | CTAS-Debugger v1.2.41";\
      opacity: .3;font-size: .8em;\
  }\
  /** Dark Mode **/\
  html[ctas-darkmode=true] {\
     filter: invert(1);\
     background-color: #000;\
  }\
  @keyframes tip {\
      0% {\
          opacity: 1;\
      }\
      25% {\
          opacity: 0;\
      }\
      50% {\
          opacity: 1;\
          font-size: 1.2em;\
      }\
      75% {\
          opacity: 0;\
      }\
      100% {\
          opacity: 1;\
      }\
  }\
  </style>'
    );
  }

  // UI Features
  printError(message) {
    this.printMessage("×", message, "重试", "connect");
  }

  printMessage(icon, message, action = false, func = "") {
    $("#ctas-msg").text(
      icon + " " + message + " 💀已做：" + client.getPrecticeDone() + "题"
    );
    $("#ctas-msg2").text("");
    if (client.isAlive)
      $("#ctas-msg").append(
        '&nbsp;&nbsp;&nbsp;<a class="ctas-href-action" onclick="client.disconnect()" href="javascript:;">∥ 暂停</a>'
      );
    if (action) {
      $("#ctas-msg").append(
        `&nbsp;&nbsp;<a class=\"ctas-href-action\" onclick=\"client.${func}()\" href=\"javascript:;\">${action}</a>`
      );
    }
    $("#ctas-msg").append(
      `&nbsp;&nbsp;<a class=\"ctas-href-action\" href=\"javascript:display.toggleSetPanel();\">设置</a>`
    );
  }

  toggleSetPanel() {
    $("#ctas-inject").attr(
      "ctas-panel-expanded",
      $("#ctas-inject").attr("ctas-panel-expanded") == "true"
        ? "false"
        : "true"
    );
  }
}

// Controllers
let display = new Display();
let client = new Client(display);
let interaction = new Interaction();
