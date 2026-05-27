@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
set "TARGET_ROOT=%ROOT%"
if exist "%ROOT%\payload\client\app\mc_design_client.pyz" set "TARGET_ROOT=%ROOT%\payload"
set "PYTHON_EXE=%TARGET_ROOT%\client\python\python.exe"
set "PYTHON_ARGS="

if exist "%PYTHON_EXE%" goto run
echo [mc-design] Missing bundled Python: %PYTHON_EXE%
exit /b 2

:run
"%PYTHON_EXE%" %PYTHON_ARGS% "%ROOT%\installer\tools\smoke_test.mcpy" --root "%TARGET_ROOT%" %*
exit /b %ERRORLEVEL%
