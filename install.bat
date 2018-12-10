@echo off
SET bat_path=%~dp0
echo CTAS Debugger Command Line Tool
echo Copyright Dalvik Shen 2018. All Rights Reserved. Prohibition of distribution
echo.

set "PYTHON_VERSION=3.7.1"

python -V && echo Installation Detected && echo. || goto py
goto pip


:py
  echo Installing Python
  echo REMEMBER TO CHECK THE BOX 'ADD TO PATH'
  %bat_path:~0,-1%\python-%PYTHON_VERSION%.exe
  echo Rerun this script to continue
  pause
  exit /B 1

:pip
echo Installing dependents
pip install %bat_path:~0,-1%\whl\pyperclip-1.7.0.tar.gz
pip install %bat_path:~0,-1%\whl\websockets-7.0-cp37-cp37m-win32.whl
echo.
echo Done.
REM type index.min.js | clip
REM echo Code copied, paste it to Chrome Console
echo Just double click __main__.pyw to run debugger
echo.
pause
exit /B 0