@echo off
title PDP builder - one-time setup
cd /d "%~dp0"
echo.
echo  PDP builder - one-time setup
echo  ============================
echo.
where py >nul 2>nul || where python >nul 2>nul
if errorlevel 1 (
  echo  Python is not installed yet.
  echo  1. Open https://www.python.org/downloads/  and click the big Download button.
  echo  2. Run the installer and TICK "Add python.exe to PATH" on the first screen, then Install Now.
  echo  3. Close this window and double-click SETUP.bat again.
  echo.
  pause
  exit /b 1
)
set PY=py
where py >nul 2>nul || set PY=python
echo  Installing the tool's parts (a few minutes, needs internet) ...
echo.
%PY% -m pip install --upgrade pip >nul 2>nul
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo  Something failed above. Take a screenshot of this window and send it to whoever gave you the tool.
  pause
  exit /b 1
)
echo.
echo  Installing the browser the tool uses to read product pages ...
%PY% -m playwright install chromium
if errorlevel 1 (
  echo.
  echo  The browser install failed. Take a screenshot of this window and send it to whoever gave you the tool.
  pause
  exit /b 1
)
echo.
echo  Setup finished. From now on, double-click RUN.bat whenever you want to pull the sheet.
echo.
pause
