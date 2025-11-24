"""
Database Migration Script
Migrates from old schema (admin-based ratings) to new schema (user-based ratings)
"""
import MySQLdb

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'kmeans_voting'
}

def migrate_database():
    try:
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            db=DB_CONFIG['database'],
            charset='utf8'
        )
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # 1. Create new anggota table structure
        print("1. Updating anggota table structure...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anggota_new (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                pendidikan ENUM('SD','SMP','SMA','D3','S1','S2','S3') NOT NULL,
                visi_misi TEXT,
                cluster INT DEFAULT NULL,
                status ENUM('anggota','kandidat') DEFAULT 'anggota',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Create penilaian table
        print("2. Creating penilaian table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS penilaian (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                anggota_id INT NOT NULL,
                keaktifan INT NOT NULL CHECK (keaktifan BETWEEN 1 AND 100),
                kepemimpinan INT NOT NULL CHECK (kepemimpinan BETWEEN 1 AND 100),
                pengalaman INT NOT NULL CHECK (pengalaman BETWEEN 1 AND 100),
                disiplin INT NOT NULL CHECK (disiplin BETWEEN 1 AND 100),
                komunikasi INT NOT NULL CHECK (komunikasi BETWEEN 1 AND 100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY (anggota_id) REFERENCES anggota_new(id) ON DELETE CASCADE,
                UNIQUE KEY unique_rating (user_id, anggota_id)
            )
        """)
        
        # 3. Check if old anggota table exists and has data
        cursor.execute("SHOW TABLES LIKE 'anggota'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM anggota")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"3. Found {count} records in old anggota table")
                print("   Note: Old data cannot be automatically migrated due to schema changes.")
                print("   Please manually re-add members with new format (nama, pendidikan, visi_misi)")
                
                # Backup old table
                cursor.execute("DROP TABLE IF EXISTS anggota_backup")
                cursor.execute("CREATE TABLE anggota_backup AS SELECT * FROM anggota")
                print("   Old data backed up to 'anggota_backup' table")
        
        # 4. Drop old anggota table and rename new one
        print("4. Replacing anggota table...")
        cursor.execute("DROP TABLE IF EXISTS anggota")
        cursor.execute("RENAME TABLE anggota_new TO anggota")
        
        # 5. Update penilaian foreign key
        cursor.execute("ALTER TABLE penilaian DROP FOREIGN KEY IF EXISTS penilaian_ibfk_2")
        cursor.execute("""
            ALTER TABLE penilaian 
            ADD CONSTRAINT penilaian_ibfk_2 
            FOREIGN KEY (anggota_id) REFERENCES anggota(id) ON DELETE CASCADE
        """)
        
        conn.commit()
        print("\n✓ Database migration completed successfully!")
        print("\nNext steps:")
        print("1. Add new members using the admin panel (Data Anggota)")
        print("2. Have users rate the members (User login -> Penilaian)")
        print("3. Run K-Means analysis based on user ratings")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n✗ Error during migration: {e}")
        print("Please check your database configuration and try again.")

if __name__ == '__main__':
    print("=" * 60)
    print("K-Means Voting System - Database Migration")
    print("=" * 60)
    print("\nThis will update your database schema to support user-based ratings.")
    print("WARNING: This will modify your database structure!")
    
    response = input("\nDo you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        migrate_database()
    else:
        print("Migration cancelled.")
