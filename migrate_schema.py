"""
Script to migrate PostgreSQL npk_readings table from uppercase to lowercase columns
"""
from app.utils.database import engine
from sqlalchemy import text

print("=" * 60)
print("🔄 Migrating NPK Readings Table Schema")
print("=" * 60)

try:
    with engine.connect() as conn:
        # Check if table exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'npk_readings'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            print("\n❌ Table 'npk_readings' does not exist!")
            print("Creating table with correct schema...")
            
            conn.execute(text("""
                CREATE TABLE npk_readings (
                    id SERIAL PRIMARY KEY,
                    n INTEGER,
                    p INTEGER,
                    k INTEGER,
                    device_id VARCHAR DEFAULT 'ESP8266',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX ix_npk_readings_device_id ON npk_readings(device_id);
                CREATE INDEX ix_npk_readings_timestamp ON npk_readings(timestamp);
            """))
            conn.commit()
            print("✅ Table created successfully!")
        else:
            print("\n✅ Table 'npk_readings' exists")
            
            # Check if old columns exist
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'npk_readings' 
                AND column_name IN ('N', 'P', 'K', 'n', 'p', 'k');
            """))
            columns = [row[0] for row in result]
            
            print(f"   Current columns: {columns}")
            
            if 'N' in columns or 'P' in columns or 'K' in columns:
                print("\n🔄 Migrating from uppercase to lowercase...")
                
                # Rename columns
                if 'N' in columns:
                    conn.execute(text('ALTER TABLE npk_readings RENAME COLUMN "N" TO n;'))
                    print("   ✅ Renamed N → n")
                
                if 'P' in columns:
                    conn.execute(text('ALTER TABLE npk_readings RENAME COLUMN "P" TO p;'))
                    print("   ✅ Renamed P → p")
                
                if 'K' in columns:
                    conn.execute(text('ALTER TABLE npk_readings RENAME COLUMN "K" TO k;'))
                    print("   ✅ Renamed K → k")
                
                conn.commit()
                print("\n✅ Migration completed successfully!")
            else:
                print("\n✅ Schema is already correct (lowercase columns)")
        
        # Verify final schema
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'npk_readings'
            ORDER BY ordinal_position;
        """))
        
        print("\n📋 Final Schema:")
        print("-" * 60)
        for row in result:
            print(f"   {row[0]}: {row[1]}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
