"""
Force SQLite and check sensor data
"""
import os
# Force SQLite before any imports
os.environ['DATABASE_URL'] = 'sqlite:///./app.db'

from app.utils.database import SessionLocal
from app.models.db_model import NPKReading
from datetime import datetime, timedelta

print("=" * 60)
print("🔍 Checking ESP8266 Sensor Data (FORCED SQLITE)")
print("=" * 60)

db = SessionLocal()

try:
    # Get total count
    total_count = db.query(NPKReading).count()
    print(f"\n📊 Total NPK readings in database: {total_count}")
    
    if total_count == 0:
        print("\n❌ No data found!")
        print("\n💡 Possible reasons:")
        print("   1. ESP8266 is not connected to WiFi")
        print("   2. ESP8266 IP address is incorrect in firmware")
        print("   3. Backend is not running")
        print("   4. ESP8266 hasn't sent data yet (press the button!)")
    else:
        print("\n✅ Data found! Here are the details:\n")
        
        # Get latest 5 readings
        latest_readings = db.query(NPKReading).order_by(NPKReading.timestamp.desc()).limit(5).all()
        
        print("📋 Latest 5 readings:")
        print("-" * 60)
        for i, reading in enumerate(latest_readings, 1):
            time_ago = datetime.utcnow() - reading.timestamp
            minutes_ago = int(time_ago.total_seconds() / 60)
            
            print(f"\n{i}. Reading ID: {reading.id}")
            print(f"   N: {reading.n} mg/kg | P: {reading.p} mg/kg | K: {reading.k} mg/kg")
            print(f"   Device: {reading.device_id}")
            print(f"   Time: {reading.timestamp} ({minutes_ago} minutes ago)")
        
        # Check if data is recent (within last 5 minutes)
        recent_cutoff = datetime.utcnow() - timedelta(minutes=5)
        recent_count = db.query(NPKReading).filter(NPKReading.timestamp >= recent_cutoff).count()
        
        print("\n" + "=" * 60)
        if recent_count > 0:
            print(f"✅ ESP8266 is ACTIVE! {recent_count} readings in last 5 minutes")
        else:
            print(f"⚠️  No recent data (last 5 min). ESP8266 might be idle.")
            print("   Try pressing the button on the ESP8266!")
        
finally:
    db.close()

print("\n" + "=" * 60)
