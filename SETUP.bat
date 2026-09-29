@echo off
title imageGrabber - one-time setup
cd /d "%~dp0"
echo.
echo  imageGrabber - one-time setup
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
echo.
findstr /b /c:"CLICKUP_TOKEN=pk_" .env >nul 2>nul
if errorlevel 1 (
  echo  Last thing: the ClickUp key. Whoever gave you this tool has it - it starts with pk_
  echo  ^(they get it in ClickUp: click their avatar ^> Settings ^> Apps ^> API Token^).
  set /p TOKEN=  Paste the ClickUp key here and press Enter: 
)
if defined TOKEN (
  >>.env echo CLICKUP_TOKEN=%TOKEN%
  echo  Saved.
)
echo.
rem ---- images straight into the shared Google Drive folder (needs Google Drive for Desktop)
findstr /b /c:"PDP_OUTPUT_DIR=" .env >nul 2>nul
if not errorlevel 1 goto :outputdone
set GDRIVE=
for %%D in (G H I J K L M N O P Q R S T U V W X Y Z) do if not defined GDRIVE if exist "%%D:\My Drive\" set GDRIVE=%%D:\My Drive
if not defined GDRIVE if exist "%USERPROFILE%\My Drive\" set GDRIVE=%USERPROFILE%\My Drive
if not defined GDRIVE if exist "%USERPROFILE%\Google Drive\My Drive\" set GDRIVE=%USERPROFILE%\Google Drive\My Drive
if not defined GDRIVE (
  echo.
  echo  Google Drive for Desktop is not installed, so images will stay on this computer (in pdp_output).
  echo  To have them land in the team's Drive folder automatically: install https://www.google.com/drive/download/
  echo  sign in, open the shared imageGrabber folder in your browser, right-click it ^> Organise ^> Add shortcut ^> My Drive,
  echo  then double-click SETUP.bat again.
  goto :outputdone
)
if not exist "%GDRIVE%\imageGrabber\" (
  echo.
  echo  Google Drive for Desktop found at %GDRIVE%, but no imageGrabber folder in it yet.
  echo  Open the shared imageGrabber folder in your browser, right-click it ^> Organise ^> Add shortcut ^> My Drive,
  echo  wait a minute for Drive to sync, then double-click SETUP.bat again. Until then images stay in pdp_output.
  goto :outputdone
)
>>.env echo PDP_OUTPUT_DIR=%GDRIVE%\imageGrabber
echo.
echo  Images will be saved straight into Google Drive: %GDRIVE%\imageGrabber
:outputdone
echo.
echo  Setup finished. From now on, double-click RUN.bat whenever you want to pull the products.
echo.
pause
