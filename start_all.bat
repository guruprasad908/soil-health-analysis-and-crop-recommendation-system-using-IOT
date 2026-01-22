@echo off
echo ========================================
echo   Soil Crop Recommender System
echo   Starting Backend and Frontend
echo ========================================
echo.

REM Change to project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Please create it first: python -m venv venv
    pause
    exit /b 1
)

REM Check if Node.js is installed
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    REM Try full path
    if not exist "C:\Program Files\nodejs\npm.cmd" (
        echo [ERROR] Node.js/npm not found!
        echo Please install Node.js from https://nodejs.org/
        pause
        exit /b 1
    )
    set NPM_CMD=C:\Program Files\nodejs\npm.cmd
) else (
    set NPM_CMD=npm
)

echo [1/2] Starting FastAPI Backend Server...
echo    URL: http://localhost:8000
echo    Docs: http://localhost:8000/docs
echo.
start "FastAPI Backend" cmd /k "cd /d %~dp0 && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul 2>&1

echo [2/2] Starting React Frontend Server...
echo    URL: http://localhost:5173
echo.

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo [WARNING] Frontend dependencies not installed!
    echo Installing dependencies first...
    cd frontend
    %NPM_CMD% install
    cd ..
)

start "React Frontend" cmd /k "cd /d %~dp0frontend && %NPM_CMD% run dev"

echo.
echo ========================================
echo   Servers Starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Two command windows will open - keep them open!
echo Close them when you're done.
echo.
echo Waiting 5 seconds for servers to initialize...
timeout /t 5 /nobreak >nul 2>&1

echo.
echo ========================================
echo   Opening Browser...
echo ========================================
start http://localhost:5173

echo.
echo Done! Check the command windows for any errors.
echo.
pause

