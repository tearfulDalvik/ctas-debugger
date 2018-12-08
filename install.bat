@echo off

echo Copyright Dalvik Shen 2018
echo.

set "PYTHON_VERSION=3.7.1"

python -V && echo Installation Detected && echo. || goto py
goto pip

:py
  echo Installing Python
  python-%PYTHON_VERSION%.exe /quiet

:pip
pip download -d whl -r requirements.txt
exit /B 0