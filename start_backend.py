import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add the current directory to sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("🌾 Starting Soil Crop Recommender Backend...")
    print("🚀 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["app"])
