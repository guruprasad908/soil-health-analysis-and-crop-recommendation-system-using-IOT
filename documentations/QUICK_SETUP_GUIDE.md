# 🚀 Quick Setup Guide
## Soil Crop Recommender System

This is a quick reference guide to get your project running. For detailed analysis, see `PROJECT_ANALYSIS_README.md`.

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### Step 2: Create Environment File

Create a file named `.env` in the project root:

```env
DATABASE_URL=sqlite:///./app.db
OPENWEATHER_API_KEY=your_key_here
```

**Note:** Get free OpenWeather API key from: https://openweathermap.org/api

### Step 3: Initialize Database

```bash
python create_tables.py
```

### Step 4: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### Step 5: Start the Application

**Windows:**
```bash
start_project.bat
```

**Manual (Linux/Mac/Windows):**

Terminal 1 - Backend:
```bash
venv\Scripts\activate  # Windows
python start_backend.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### Step 6: Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 14+ installed
- [ ] Virtual environment created and activated
- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `DATABASE_URL`
- [ ] Database tables created (`python create_tables.py`)
- [ ] Frontend packages installed (`cd frontend && npm install`)
- [ ] Backend server running (http://localhost:8000)
- [ ] Frontend server running (http://localhost:5173)

---

## 🐛 Common Issues

### "Module not found"
**Fix:** Activate virtual environment and install dependencies:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### "Database connection failed"
**Fix:** Create `.env` file with:
```env
DATABASE_URL=sqlite:///./app.db
```

### "Port already in use"
**Fix:** Change port or kill the process:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "API key invalid"
**Fix:** Get free API key from https://openweathermap.org/api and add to `.env`

---

## 📚 Next Steps

1. Read `PROJECT_ANALYSIS_README.md` for detailed bug analysis
2. Test the API at http://localhost:8000/docs
3. Try making a prediction through the frontend
4. Check for any errors in the console

---

## 🆘 Need Help?

- Check `PROJECT_ANALYSIS_README.md` for detailed troubleshooting
- Review error messages in terminal
- Check that all services are running
- Verify `.env` file is correct

---

**Last Updated:** 2025-01-27

