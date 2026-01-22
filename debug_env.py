import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Sys Path: {sys.path}")

try:
    import dotenv
    print(f"✅ dotenv imported: {dotenv.__file__}")
except ImportError as e:
    print(f"❌ dotenv import failed: {e}")

try:
    import uvicorn
    print(f"✅ uvicorn imported: {uvicorn.__file__}")
except ImportError as e:
    print(f"❌ uvicorn import failed: {e}")

try:
    import sqlalchemy
    print(f"✅ sqlalchemy imported: {sqlalchemy.__file__}")
except ImportError as e:
    print(f"❌ sqlalchemy import failed: {e}")
