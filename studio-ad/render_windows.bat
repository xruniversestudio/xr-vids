@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === XR Universe Studio - render ===
if not exist node_modules\three (
  echo Installing libraries, first time only...
  call npm install || goto :err
  call npx playwright install chromium || goto :err
)
call npm run render || goto :err
echo.
echo Done. The videos are in the "out" folder.
start "" "%~dp0out"
pause
exit /b 0
:err
echo.
echo Something went wrong - see the messages above.
pause
exit /b 1
