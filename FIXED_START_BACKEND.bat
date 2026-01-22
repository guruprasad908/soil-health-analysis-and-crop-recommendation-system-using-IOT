@echo off
echo Starting FastAPI Backend Server...
echo.

REM Activate virtual environment and run uvicorn
call venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
