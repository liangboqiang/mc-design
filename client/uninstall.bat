@echo off
setlocal EnableExtensions EnableDelayedExpansion

if /i not "%MC_DESIGN_UNINSTALL_CHILD%"=="1" (
  if "%~1"=="" (
    set "CLEANUP_INSTALL_DIR=%~dp0"
  ) else (
    set "CLEANUP_INSTALL_DIR=%~1"
  )
  for %%I in ("!CLEANUP_INSTALL_DIR!") do set "CLEANUP_INSTALL_DIR=%%~fI"
  if "!CLEANUP_INSTALL_DIR:~-1!"=="\" set "CLEANUP_INSTALL_DIR=!CLEANUP_INSTALL_DIR:~0,-1!"
  set "SELF_COPY=%TEMP%\mc-design-uninstall-%RANDOM%.bat"
  copy /Y "%~f0" "!SELF_COPY!" >nul
  if errorlevel 1 (
    echo [mc-design] Failed to prepare uninstall helper.
    echo [mc-design] Uninstall failed. Exit code: 5.
    if /i not "%MC_DESIGN_UNINSTALL_NO_PAUSE%"=="1" (
      echo [mc-design] Press any key to close.
      pause >nul
    )
    exit /b 5
  )
  set "MC_DESIGN_UNINSTALL_CHILD=1"
  call "!SELF_COPY!" "!CLEANUP_INSTALL_DIR!"
  set "RC=!ERRORLEVEL!"
  del /Q "!SELF_COPY!" >nul 2>nul
  if "!RC!"=="0" (
    call :remove_install_dir "!CLEANUP_INSTALL_DIR!"
    set "RC=!ERRORLEVEL!"
  )
  exit /b !RC!
)

if "%~1"=="" (
  set "INSTALL_DIR=%~dp0"
) else (
  set "INSTALL_DIR=%~1"
)
for %%I in ("%INSTALL_DIR%") do set "INSTALL_DIR=%%~fI"
if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"

echo [mc-design] Uninstall dir: %INSTALL_DIR%

set "PYTHON_EXE=%INSTALL_DIR%\client\python\python.exe"
set "HELPER=%INSTALL_DIR%\installer\tools\install_helper.mcpy"
if not exist "%PYTHON_EXE%" goto missing_runtime
if not exist "%HELPER%" goto missing_runtime

set "TEMP_RUNTIME=%TEMP%\mc-design-uninstall-runtime-%RANDOM%"
set "TEMP_PYTHON=%TEMP_RUNTIME%\python\python.exe"
set "TEMP_HELPER=%TEMP_RUNTIME%\install_helper.mcpy"
if exist "%TEMP_RUNTIME%" rmdir /S /Q "%TEMP_RUNTIME%" >nul 2>nul
xcopy "%INSTALL_DIR%\client\python" "%TEMP_RUNTIME%\python" /E /I /Y /Q >nul
if errorlevel 1 goto temp_runtime_failed
copy /Y "%HELPER%" "%TEMP_HELPER%" >nul
if errorlevel 1 goto temp_runtime_failed

"%TEMP_PYTHON%" "%TEMP_HELPER%" uninstall --install-dir "%INSTALL_DIR%"
set "HELPER_RC=%ERRORLEVEL%"
rmdir /S /Q "%TEMP_RUNTIME%" >nul 2>nul
if not "%HELPER_RC%"=="0" goto uninstall_failed

echo [mc-design] Uninstall succeeded.
if /i not "%MC_DESIGN_UNINSTALL_NO_PAUSE%"=="1" (
  echo [mc-design] Press any key to close and clean install directory.
  pause >nul
)

exit /b 0

:missing_runtime
echo [mc-design] Missing bundled Python or uninstall helper.
echo [mc-design] Uninstall failed. Exit code: 4.
if /i not "%MC_DESIGN_UNINSTALL_NO_PAUSE%"=="1" (
  echo [mc-design] Press any key to close.
  pause >nul
)
exit /b 4

:temp_runtime_failed
echo [mc-design] Failed to prepare temporary uninstall runtime.
echo [mc-design] Uninstall failed. Exit code: 6.
if /i not "%MC_DESIGN_UNINSTALL_NO_PAUSE%"=="1" (
  echo [mc-design] Press any key to close.
  pause >nul
)
exit /b 6

:uninstall_failed
echo [mc-design] Uninstall helper failed.
echo [mc-design] Uninstall failed. Exit code: %HELPER_RC%.
if /i not "%MC_DESIGN_UNINSTALL_NO_PAUSE%"=="1" (
  echo [mc-design] Press any key to close.
  pause >nul
)
exit /b %HELPER_RC%

:remove_install_dir
set "TARGET=%~1"
if "%TARGET%"=="" exit /b 8
for %%I in ("%TARGET%") do set "TARGET=%%~fI"
cd /d "%TEMP%" >nul 2>nul
for /L %%R in (1,1,20) do (
  rmdir /S /Q "%TARGET%" 2>nul
  if not exist "%TARGET%" (
    set "TARGET_REMOVED=1"
    goto remove_install_dir_done
  )
  "%SystemRoot%\System32\ping.exe" 127.0.0.1 -n 2 >nul
)
:remove_install_dir_done
if "%TARGET_REMOVED%"=="1" (
  echo [mc-design] Install directory removed.
  exit /b 0
)
echo [mc-design] Failed to remove install directory: %TARGET%
echo [mc-design] Close processes or consoles under that directory and run uninstall again.
exit /b 8
