@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Antigravity Smart RTL Patcher

:: Locate patcher scripts (support both root and src\ folder)
set "PATCH_PY=%~dp0src\patcher.py"
if not exist "%PATCH_PY%" set "PATCH_PY=%~dp0patcher.py"

set "PATCH_JS=%~dp0src\patcher.js"
if not exist "%PATCH_JS%" set "PATCH_JS=%~dp0patcher.js"

:: 1. Try Python (live interpreter test to avoid Windows Store execution alias stubs)
python -c "import sys" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python "%PATCH_PY%" %*
    goto :end
)

:: Try Python launcher (py -3 or py)
py -3 -c "import sys" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py "%PATCH_PY%" %*
    goto :end
)

py -c "import sys" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py "%PATCH_PY%" %*
    goto :end
)

:: 2. Try Node.js
node -v >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    node "%PATCH_JS%" %*
    goto :end
)

:: 3. Try Antigravity Built-in Node Engine (Zero external dependencies)
set "ANTIGRAVITY_EXE=%LOCALAPPDATA%\Programs\antigravity\Antigravity.exe"
if exist "%ANTIGRAVITY_EXE%" (
    set "ELECTRON_RUN_AS_NODE=1"
    "%ANTIGRAVITY_EXE%" "%PATCH_JS%" %*
    goto :end
)

if exist "%ProgramFiles%\Antigravity\Antigravity.exe" (
    set "ELECTRON_RUN_AS_NODE=1"
    "%ProgramFiles%\Antigravity\Antigravity.exe" "%PATCH_JS%" %*
    goto :end
)

if exist "%ProgramFiles(x86)%\Antigravity\Antigravity.exe" (
    set "ELECTRON_RUN_AS_NODE=1"
    "%ProgramFiles(x86)%\Antigravity\Antigravity.exe" "%PATCH_JS%" %*
    goto :end
)

echo [ERROR] Neither Python nor Node.js was found on this system.
echo Please install Python (https://www.python.org) or Node.js (https://nodejs.org).
pause
exit /b 1

:end
exit /b %ERRORLEVEL%
