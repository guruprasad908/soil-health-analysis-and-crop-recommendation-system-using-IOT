# 🚀 Quick Start Guide - Start Backend & Frontend

## ⚠️ Connection Refused Error Fix

If you see `ERR_CONNECTION_REFUSED`, the backend server is not running. Follow these steps:

---

## 📋 Method 1: Using Batch File (Easiest)

**Double-click or run:**
```bash
start_project.bat
```

This will start both backend and frontend automatically in separate windows.

---

## 📋 Method 2: Manual Start (Step by Step)

### Step 1: Start Backend Server

**Open a new terminal/PowerShell window:**

```powershell
# Navigate to project directory
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend server
python start_backend.py
```

**OR use uvicorn directly:**
```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**You should see:**
```
✅ Loaded Stacking Classifier
✅ Loaded Random Forest
...
Starting FastAPI server...
Server will be accessible from network on http://0.0.0.0:8000
Access locally at http://localhost:8000
```

**Keep this terminal window open!**

---

### Step 2: Start Frontend Server

**Open a NEW terminal/PowerShell window:**

```powershell
# Navigate to project directory
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender

# Navigate to frontend
cd frontend

# Start frontend server
npm run dev
```

**OR if npm is not in PATH:**
```powershell
"C:\Program Files\nodejs\npm.cmd" run dev
```

**You should see:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Keep this terminal window open too!**

---

## ✅ Verify Servers Are Running

### Check Backend:
Open browser and go to: **http://localhost:8000**

You should see:
```json
{"message": "🌾 Soil Health & Crop Recommendation API is running!"}
```

### Check API Docs:
Open browser and go to: **http://localhost:8000/docs**

You should see the Swagger API documentation.

### Check Frontend:
Open browser and go to: **http://localhost:5173**

You should see the application homepage.

---

## 🔧 Troubleshooting

### Port 8000 Already in Use

If you get an error that port 8000 is already in use:

**Option 1: Kill the process using port 8000**
```powershell
# Find process ID
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Option 2: Use a different port**
```powershell
# Set environment variable
$env:PORT=8001

# Start server
python start_backend.py
```

Then update frontend `.env` file:
```
VITE_API_BASE_URL=http://localhost:8001
```

---

### Backend Won't Start

**Check if virtual environment is activated:**
```powershell
# Should show (venv) in prompt
.\venv\Scripts\Activate.ps1
```

**Check if dependencies are installed:**
```powershell
pip install -r requirements.txt
```

**Check for errors in terminal:**
- Look for import errors
- Check if models are loaded
- Verify database connection

---

### Frontend Won't Start

**Check if Node.js is installed:**
```powershell
node --version
npm --version
```

**Check if dependencies are installed:**
```powershell
cd frontend
npm install
```

**Check for errors in terminal:**
- Look for port conflicts (5173)
- Check for missing dependencies
- Verify API base URL in `.env`

---

## 📝 Quick Commands Reference

### Start Backend Only:
```powershell
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend Only:
```powershell
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender\frontend
npm run dev
```

### Start Both (Batch File):
```powershell
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender
.\start_project.bat
```

---

## 🎯 Expected URLs

Once both servers are running:

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend App**: http://localhost:5173
- **Weather Page**: http://localhost:5173/weather
- **Prediction Page**: http://localhost:5173/predict

---

## ⚡ Quick Fix for Current Issue

**Right now, to fix the connection refused error:**

1. **Open PowerShell/Terminal**
2. **Run:**
   ```powershell
   cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender
   .\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. **Wait for "Application startup complete"**
4. **Open browser to http://localhost:8000**
5. **Then go to http://localhost:5173/weather**

---

**The backend server is now starting in the background. Wait a few seconds, then try accessing the weather page again!**

