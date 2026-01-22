
import sqlite3
import os
from datetime import datetime

DB_PATH = "app.db"

def check_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database file not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check NPK readings
        cursor.execute("SELECT COUNT(*) FROM npk_readings")
        npk_count = cursor.fetchone()[0]
        print(f"NPK Readings Count: {npk_count}")

        if npk_count > 0:
            cursor.execute("SELECT * FROM npk_readings ORDER BY timestamp DESC LIMIT 1")
            print("Latest NPK:", cursor.fetchone())

        # Check UNO readings
        cursor.execute("SELECT COUNT(*) FROM uno_readings")
        uno_count = cursor.fetchone()[0]
        print(f"UNO Readings Count: {uno_count}")

        if uno_count > 0:
            cursor.execute("SELECT * FROM uno_readings ORDER BY timestamp DESC LIMIT 1")
            print("Latest UNO:", cursor.fetchone())
            
    except Exception as e:
        print(f"❌ Error querying database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_db()
