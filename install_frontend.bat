@echo off
echo Installing Frontend Dependencies...
echo.

cd frontend

REM Try using npm directly first (if in PATH)
where npm >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Using npm from PATH...
    npm install
) else (
    echo Using npm from full path...
    "C:\Program Files\nodejs\npm.cmd" install
)

echo.
echo Frontend dependencies installation complete!
pause

