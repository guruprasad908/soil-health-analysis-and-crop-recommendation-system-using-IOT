import os
import sys
from sqlalchemy import create_engine, inspect
from app.models.db_model import Base, Prediction
from app.utils.database import DATABASE_URL

def reset_database():
    print(f"🔄 Resetting database at {DATABASE_URL}...")
    
    # 1. Delete existing database file if it exists (SQLite only)
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"✅ Deleted existing database file: {db_path}")
            except Exception as e:
                print(f"❌ Could not delete database file: {e}")
                return False
    
    # 2. Recreate tables (Drop and Create)
    try:
        engine = create_engine(DATABASE_URL)
        print("💥 Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        print("✨ Creating new tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Created new database tables.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
        
    # 3. Verify Schema
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('predictions')]
        print(f"🔎 'predictions' table columns: {columns}")
        
        if 'model_used' in columns:
            print("✅ Column 'model_used' exists!")
            return True
        else:
            print("❌ Column 'model_used' is MISSING!")
            return False
    except Exception as e:
        print(f"❌ Error verifying schema: {e}")
        return False

if __name__ == "__main__":
    # Add current directory to path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    if reset_database():
        print("🚀 Database reset successful!")
    else:
        print("💀 Database reset FAILED!")
