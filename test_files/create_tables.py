"""
Database Table Creation Script
Creates all required database tables for the Soil Crop Recommender System
"""

from app.models.db_model import Base
from app.utils.database import engine
import sys

def create_tables():
    """Create all database tables"""
    try:
        print("🔄 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        print("  - predictions (stores crop prediction history)")
        print("  - npk_readings (stores NPK sensor readings)")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your .env file has DATABASE_URL set")
        print("  2. For PostgreSQL: Ensure database server is running")
        print("  3. For SQLite: Ensure write permissions in project directory")
        print("  4. Check database connection in app/utils/database.py")
        return False

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)

