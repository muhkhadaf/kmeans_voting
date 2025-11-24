"""
Update Database Script
Updates existing database to new schema (user-based ratings)
"""
import MySQLdb
from werkzeug.security import generate_password_hash

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'kmeans_voting'
}

def update_database():
    try:
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            db=DB_CONFIG['database'],
            charset='utf8'
        )
        cursor = conn.cursor()
        
        print("=" * 60)
        print("Updating K-Means Voting Database Schema")
        print("=" * 60)
        
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 1. Backup existing anggota table
        print("\n1. Backing up existing anggota table...")
        try:
            cursor.execute("DROP TABLE IF EXISTS anggota_backup_old")
            cursor.execute("CREATE TABLE anggota_backup_old AS SELECT * FROM anggota")
            cursor.execute("SELECT COUNT(*) FROM anggota_backup_old")
            count = cursor.fetchone()[0]
            print(f"   ✓ Backed up {count} records to 'anggota_backup_old'")
        except Exception as e:
            print(f"   Note: {e}")
        
        # 2. Drop foreign key constraints first
        print("\n2. Removing foreign key constraints...")
        try:
            # Drop penilaian table if exists (it has FK to anggota)
            cursor.execute("DROP TABLE IF EXISTS penilaian")
            print("   ✓ Dropped penilaian table")
        except Exception as e:
            print(f"   Note: {e}")
        
        # 3. Drop old anggota table
        print("\n3. Dropping old anggota table...")
        cursor.execute("DROP TABLE IF EXISTS anggota")
        print("   ✓ Old table dropped")
        
        # 4. Create new anggota table
        print("\n4. Creating new anggota table...")
        cursor.execute("""
            CREATE TABLE anggota (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                pendidikan ENUM('SD','SMP','SMA','D3','S1','S2','S3') NOT NULL,
                visi_misi TEXT,
                cluster INT DEFAULT NULL,
                status ENUM('anggota','kandidat') DEFAULT 'anggota',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✓ New anggota table created")
        
        # 5. Create penilaian table
        print("\n5. Creating penilaian table...")
        cursor.execute("DROP TABLE IF EXISTS penilaian")
        cursor.execute("""
            CREATE TABLE penilaian (
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
                FOREIGN KEY (anggota_id) REFERENCES anggota(id) ON DELETE CASCADE,
                UNIQUE KEY unique_rating (user_id, anggota_id)
            )
        """)
        print("   ✓ Penilaian table created")
        
        # 6. Update voting table to remove old unique constraint
        print("\n6. Updating voting table...")
        try:
            cursor.execute("ALTER TABLE voting DROP INDEX unique_vote")
            print("   ✓ Removed old unique constraint")
        except:
            print("   Note: Unique constraint already removed or doesn't exist")
        
        # Add new unique constraint for voting per period
        try:
            cursor.execute("""
                ALTER TABLE voting 
                ADD UNIQUE KEY unique_vote_per_period (user_id, voting_period_id)
            """)
            print("   ✓ Added new unique constraint per period")
        except:
            print("   Note: Constraint already exists")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✓ Database update completed successfully!")
        print("=" * 60)
        
        print("\n📋 Next Steps:")
        print("1. Start the application: python app.py")
        print("2. Login as admin")
        print("3. Add members with new format (nama, pendidikan, visi misi)")
        print("4. Add users if not already added")
        print("5. Instruct users to login and rate members")
        print("6. Run K-Means analysis after sufficient ratings")
        
        print("\n💾 Old Data:")
        print("Your old anggota data is backed up in 'anggota_backup_old' table")
        print("You can view it with: SELECT * FROM anggota_backup_old;")
        
        cursor.close()
        conn.close()
        
    except MySQLdb.Error as e:
        print(f"\n✗ Database Error: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database 'kmeans_voting' exists")
        print("3. Database credentials in this script are correct")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("\n⚠️  WARNING: This will modify your database structure!")
    print("Make sure you have a backup of your database before proceeding.")
    print("\nTo backup your database, run:")
    print("mysqldump -u root -p kmeans_voting > backup_before_update.sql")
    
    response = input("\nHave you backed up your database? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Update cancelled. Please backup your database first.")
        exit()
    
    response = input("\nDo you want to continue with the update? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        success = update_database()
        if success:
            print("\n✅ You can now run the application!")
    else:
        print("\n❌ Update cancelled.")
