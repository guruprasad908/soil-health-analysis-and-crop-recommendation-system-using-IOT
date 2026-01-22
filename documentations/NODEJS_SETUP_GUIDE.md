# 🔧 Node.js Setup Guide

## Issue: Node.js Not Recognized After Adding to PATH

If you just added Node.js to your environment variables, you need to **restart your terminal/PowerShell** for the changes to take effect.

---

## ✅ Quick Fix Steps

### Step 1: Close and Restart Your Terminal
1. **Close** the current PowerShell/Command Prompt window
2. **Open a new** PowerShell or Command Prompt window
3. Navigate back to your project:
   ```bash
   cd C:\Users\wwwgu\OneDrive\Desktop\soil_crop_recommender
   ```

### Step 2: Verify Node.js is Working
```bash
node --version
npm --version
```

You should see version numbers like:
```
v20.11.0
10.2.4
```

---

## 🔍 If Node.js Still Doesn't Work

### Option A: Check if Node.js is Installed

1. **Check common installation locations:**
   - `C:\Program Files\nodejs\`
   - `C:\Program Files (x86)\nodejs\`
   - `%APPDATA%\npm\`

2. **If Node.js is installed but not in PATH:**
   - Find where `node.exe` is located
   - Add that folder to your PATH environment variable

### Option B: Install Node.js (If Not Installed)

1. **Download Node.js:**
   - Go to: https://nodejs.org/
   - Download the **LTS version** (recommended)
   - Run the installer

2. **During Installation:**
   - ✅ Check "Add to PATH" option
   - ✅ Complete the installation

3. **After Installation:**
   - **Restart your terminal**
   - Verify with: `node --version`

---

## 📝 How to Add Node.js to PATH Manually

If Node.js is installed but not in PATH:

1. **Find Node.js Installation:**
   - Usually: `C:\Program Files\nodejs\`
   - Or search for `node.exe` on your computer

2. **Add to PATH:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Go to **Advanced** tab → **Environment Variables**
   - Under **System Variables**, find **Path**
   - Click **Edit** → **New**
   - Add: `C:\Program Files\nodejs\` (or your Node.js path)
   - Click **OK** on all windows

3. **Restart Terminal:**
   - Close all terminal windows
   - Open a new terminal
   - Test: `node --version`

---

## ✅ Once Node.js is Working

### Install Frontend Dependencies:
```bash
cd frontend
npm install
```

### Start Frontend Server:
```bash
npm run dev
```

---

## 🎯 Current Status

- ✅ **Python Backend:** Ready
- ✅ **Database:** Initialized
- ⚠️ **Node.js:** Needs terminal restart or installation

---

## 💡 Pro Tip

After adding to PATH, always:
1. **Close** the current terminal
2. **Open a new** terminal window
3. Test the command again

Environment variable changes only apply to **new** terminal sessions!

---

**Next Steps:**
1. Restart your terminal
2. Run `node --version` to verify
3. Run `cd frontend && npm install` to install frontend dependencies
4. Run `npm run dev` to start the frontend server

