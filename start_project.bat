@echo off
echo Starting Soil & Crop Recommender System...

:: Start Backend
echo Launching Backend Server...
start "Soil_Crop_Backend" cmd /k "call venv\Scripts\activate.bat && python start_backend.py"

:: Wait a moment to let backend initialize
timeout /t 3 /nobreak >nul

:: Start Frontend
echo Launching Frontend...
cd frontend
start "Soil_Crop_Frontend" cmd /k "npm run dev"

echo System Started!
