@echo off

title "%~nx0"

REM ~ set python=C:\Python27\python.exe
set python=C:\pypy-2.3.1-win32\pypy.exe
if NOT exist %python% (
    echo Error: '%python%' doesn't exists?!?
    pause
    exit 1
)

cd..

:loop
    cls
    echo on
    %python% DragonPy_CLI.py --machine=CoCo2b run
    @echo off
    pause
goto:loop