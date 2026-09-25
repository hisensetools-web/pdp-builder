@echo off
title PDP builder
cd /d "%~dp0"
set PY=py
where py >nul 2>nul || set PY=python
%PY% pdp.py batch %*
echo.
if errorlevel 1 (
  echo  Something went wrong - see the last lines above. If a store showed a puzzle in a browser window,
  echo  solve it next time and the run carries on by itself.
) else (
  echo  Done. The images are in the pdp_output folder, one folder per product.
)
echo.
pause
