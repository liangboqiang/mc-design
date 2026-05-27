@echo off
setlocal

set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

if not exist "%ROOT%\install-state.json" (
  echo [mc-design] This directory is an extracted installer package.
  echo [mc-design] Run install.bat first.
  echo [mc-design] Example: install.bat E:\A0_Projects\A1_Dynamics_Design_LM\mc-design-client
  pause
  exit /b 2
)

set "CLIENT_DIR=%ROOT%\client"
set "CLIENT_APP=%CLIENT_DIR%\app\mc_design_client.pyz"
set "PYTHON_EXE=%CLIENT_DIR%\python\python.exe"

if not exist "%PYTHON_EXE%" goto no_python

:run
if not exist "%CLIENT_APP%" goto no_client
cd /d "%ROOT%"
echo [mc-design] Starting client...
"%PYTHON_EXE%" "%CLIENT_APP%" --root "%CLIENT_DIR%" start
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" pause
exit /b %EXIT_CODE%

:no_client
echo [mc-design] Client app not found: %CLIENT_APP%
pause
exit /b 1

:no_python
echo [mc-design] Missing bundled Python.
echo [mc-design] Expected: %CLIENT_DIR%\python\python.exe
pause
exit /b 1
