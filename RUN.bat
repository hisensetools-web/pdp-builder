@echo off
title imageGrabber
cd /d "%~dp0"
set PY=py
where py >nul 2>nul || set PY=python
findstr /b /c:"CLICKUP_TOKEN=pk_" .env >nul 2>nul
if errorlevel 1 (
  echo  The ClickUp key is not set up on this computer yet. It starts with pk_ and whoever gave you the tool has it.
  set /p TOKEN=  Paste the ClickUp key here and press Enter: 
)
if defined TOKEN (
  >>.env echo CLICKUP_TOKEN=%TOKEN%
  echo  Saved.
  echo.
)
%PY% imageGrabber.py batch %*
echo.
if errorlevel 1 (
  echo  Something went wrong - see the last lines above. If a store showed a puzzle in a browser window,
  echo  solve it next time and the run carries on by itself.
) else (
  echo  Done. The images are in the pdp_output folder, one folder per product. Pulled tasks are ticked in ClickUp.
)
echo.
pause
