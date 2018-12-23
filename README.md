# ctas-debugger

A Debug Tool for [CTAS Student System](http://172.20.2.205.cqu.pt/ctas/). This tool includes support of MacOS and Windows, ready to install in a offline environment.

[![pipeline status](https://git.ifengge.me/Dalvik/ctas-debugger/badges/master/pipeline.svg)](https://git.ifengge.me/Dalvik/ctas-debugger/commits/master)



### License

This program is made by [Dalvik Shen](https://ifengge.me/about/). All rights reserved and commercial use is prohibited. 

This program is a crack of the CTAS Student System. As such, it is subject to the CTAS System's user license. Subject to the university regulations and local law. Use at your own risk.



## Features

- Edit codes directly in the webpage
- Run instantly
- Compile/Link error outputs
- Hide everything on Windows, neither a Taskbar icon nor a console window will be displayed
- Save your outputs for 5 seconds after a successfully run, then everything will disappear again
- Copy your codes automatically
- Fix page control bar
- Multple file problems support
- Unlock copying, selecting and context menu in every CTAS pages
- Use shortcut keys to complete your homework!
- APIs available and iOS remote client is included, you can also custom your remote control on other platforms.

## Installation

### Windows
Run install.bat and follow the instructions to install.

> Be aware! Offline installation is only available on Windows.



### MacOS
If you are MacOS user, make sure [Python 3](https://www.python.org/download/releases/3.0/) is installed on your system, then run the command below in the terminal.
```
$ pip3 install -r requirements.txt
```



## Getting Started

This is a guide only tested on [Google Chrome](https://dl.google.com).

- ** Before you logged in, turn on Developer Tools ( ⌥⌘I or Ctrl+Shift+I ) **

- Follow the regular steps and load a question.
- Run \_\_main\_\_.pyw 
  - Windows: Double click, and a black window will flashing past
  - MacOS: Run ```pyhton3 __main__.pyw``` in the terminal
- Switch to the ```Console``` Tab 
- Change the Javascript contexts dropdown to ```IFrame - main (CPractice.aspx)```
- Paste everything in index.min.js then press ```Enter```
- Awala! You are a cheater now !



## Usage


#### Keymaps
Key 		  	| Function
------------ 	| ---------------------
`Q`   			| Select answer A
`W`   			| Select answer B
`E`   			| Select answer C
`R`   			| Select answer D
`T`   			| Run code
`A`   			| Previous question
`S`   			| Subsequent question


#### Select and debug

You can just copy or select something as usual,  then run and debug with Visual Studio, LLDB or something else you like.



#### Edit
You can edit codes in the webpage by just click on the code section.

CTAS-Debugger will handle your modification and write it to your clipboard automatically.



#### Run (Beta)

Follow the injected message and you'll see a ```run``` button when your code is ready.