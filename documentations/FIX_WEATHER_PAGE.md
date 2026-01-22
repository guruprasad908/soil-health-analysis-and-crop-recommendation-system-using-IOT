# 🔧 Fix: Weather Page Connection Refused

## ✅ Current Status

- ✅ **Backend Server**: Running on port 8000 (Working!)
- ⚠️ **Frontend Server**: Not fully started on port 5173

---

## 🚀 Solution: Start Frontend Server

The connection refused error is because the **frontend server is not running** or not fully started.

### Quick Fix:

**Open a NEW PowerShell window and run:**

```powershell
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender\frontend
npm run dev
```

**Wait for this message:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Then open browser to:**
```
http://localhost:5173/weather
```

---

## 📋 Complete Steps

### 1. Check Backend (Should be running)
Open: http://localhost:8000
- Should show: `{"message": "🌾 Soil Health & Crop Recommendation API is running!"}`

### 2. Start Frontend
```powershell
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender\frontend
npm run dev
```

### 3. Wait for Frontend to Start
Look for: `ready in xxx ms` and `Local: http://localhost:5173/`

### 4. Open Weather Page
Go to: http://localhost:5173/weather

---

## 🎯 Or Use Batch File (Easiest)

**Double-click:**
```
start_project.bat
```

This starts both servers automatically!

---

## ⚠️ If Frontend Won't Start

### Check Node.js:
```powershell
node --version
npm --version
```

### Install Dependencies:
```powershell
cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender\frontend
npm install
```

### Check for Port Conflicts:
If port 5173 is in use, Vite will automatically use the next available port (5174, 5175, etc.)

---

## ✅ Verification

**Both servers should be running:**

1. **Backend**: http://localhost:8000 ✅ (Confirmed working)
2. **Frontend**: http://localhost:5173 (Need to start)

**Once both are running, the weather page will work!**

