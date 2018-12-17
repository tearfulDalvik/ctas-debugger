@echo off
echo CTAS Debugger Runtime Tool

echo (C) Dalvik Shen 2018. All Rights Reserved. Prohibition of distribution

echo.


echo Compiling...

SET BASEDIR=%~dp0


g++ %BASEDIR:~0,-1%\..\cache\problem.cpp -o %BASEDIR:~0,-1%\..\cache\problem.exe
if %ERRORLEVEL% == 0 GOTO run
pause
exit /b 1

:run
echo Done\nRunning...\n
cls
%BASEDIR:~0,-1%\..\cache\problem.exe
echo.
echo.
echo Done! Cleaning...
DEL %BASEDIR:~0,-1%\..\cache\problem.exe
pause