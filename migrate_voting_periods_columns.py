import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'votings'
}

print("Connecting to database...")
conn = MySQLdb.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    passwd=DB_CONFIG['password'],
    db=DB_CONFIG['database'],
    charset='utf8'
)
cursor = conn.cursor()

print("Adding missing columns to voting_periods table...")

# Add manually_stopped column
try:
    cursor.execute("ALTER TABLE voting_periods ADD COLUMN manually_stopped TINYINT DEFAULT 0")
    print("✓ Added manually_stopped column")
except MySQLdb.Error as e:
    print(f"  manually_stopped: {e}")

# Add stopped_at column
try:
    cursor.execute("ALTER TABLE voting_periods ADD COLUMN stopped_at DATETIME DEFAULT NULL")
    print("✓ Added stopped_at column")
except MySQLdb.Error as e:
    print(f"  stopped_at: {e}")

# Add extended_count column
try:
    cursor.execute("ALTER TABLE voting_periods ADD COLUMN extended_count INT DEFAULT 0")
    print("✓ Added extended_count column")
except MySQLdb.Error as e:
    print(f"  extended_count: {e}")

conn.commit()
cursor.close()
conn.close()

print("\nMigration completed!")
