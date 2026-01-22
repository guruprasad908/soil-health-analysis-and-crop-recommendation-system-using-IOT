"""
Script to manually create database tables (FORCED SQLITE)
"""
import os
# Force SQLite before any imports
os.environ['DATABASE_URL'] = 'sqlite:///./app.db'

from app.models.db_model import Base
from app.utils.database import engine

print("Creating database tables in SQLite...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")

# Verify
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables in database: {tables}")
