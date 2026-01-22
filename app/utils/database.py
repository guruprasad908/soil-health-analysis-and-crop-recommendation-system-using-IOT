import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

# FORCE SQLITE - IGNORE POSTGRESQL
DATABASE_URL = "sqlite:///./app.db"
logger.info("🔧 FORCED SQLite database connection")

# Enhanced engine configuration for Supabase (PostgreSQL)
# Works with SQLite too, but optimized for PostgreSQL
try:
    if DATABASE_URL and "postgresql" in DATABASE_URL.lower():
        # Check if psycopg2 is available
        try:
            import psycopg2
        except ImportError:
            logger.warning("⚠️ PostgreSQL URL detected but psycopg2 not installed. Falling back to SQLite.")
            DATABASE_URL = "sqlite:///./app.db"
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
            logger.info(f"✅ Connected to SQLite database: {DATABASE_URL}")
        else:
            # Supabase/PostgreSQL configuration with connection pooling
            engine = create_engine(
                DATABASE_URL,
                pool_size=10,           # Number of connections to keep open
                max_overflow=20,        # Max connections beyond pool_size
                pool_pre_ping=True,     # Verify connections before using (important for Supabase)
                echo=False              # Set to True to see SQL queries in console
            )
            logger.info("✅ Connected to PostgreSQL database")
    else:
        # SQLite configuration (fallback)
        # Default to SQLite if DATABASE_URL is not set
        DATABASE_URL = DATABASE_URL or "sqlite:///./app.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info(f"✅ Connected to SQLite database: {DATABASE_URL}")
    
    # Test the connection
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        conn.commit()
    
except SQLAlchemyError as e:
    logger.error(f"❌ Database connection error: {e}")
    # Fallback to SQLite if PostgreSQL fails
    if DATABASE_URL and "postgresql" in DATABASE_URL.lower():
        logger.warning("⚠️ Falling back to SQLite due to PostgreSQL connection error")
        DATABASE_URL = "sqlite:///./app.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info(f"✅ Connected to SQLite database: {DATABASE_URL}")
    else:
        raise RuntimeError(f"Failed to connect to database: {e}")
except Exception as e:
    logger.error(f"❌ Unexpected error during database setup: {e}")
    # Final fallback to SQLite
    try:
        DATABASE_URL = "sqlite:///./app.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info(f"✅ Connected to SQLite database (fallback): {DATABASE_URL}")
    except Exception as fallback_error:
        logger.error(f"❌ Even SQLite fallback failed: {fallback_error}")
        raise RuntimeError(f"Failed to connect to database: {e}")

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
