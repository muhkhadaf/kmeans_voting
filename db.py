import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from flask import g
from werkzeug.security import generate_password_hash
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'votink'
}

def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            db=DB_CONFIG['database'],
            charset='utf8'
        )
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database with tables"""
    try:
        # Connect without database first to create it
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            charset='utf8'
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create admin table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        # Create user table FIRST (before penilaian)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                has_voted TINYINT DEFAULT 0
            )
        """)
        
        # Create anggota table (simplified - only basic info)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anggota (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                pendidikan ENUM('SD','SMP','SMA','D3','S1','S2','S3') NOT NULL,
                visi_misi TEXT,
                cluster INT DEFAULT NULL,
                status ENUM('anggota','kandidat') DEFAULT 'anggota',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create penilaian table (user ratings for members) - AFTER user and anggota
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
                FOREIGN KEY (anggota_id) REFERENCES anggota(id) ON DELETE CASCADE,
                UNIQUE KEY unique_rating (user_id, anggota_id)
            )
        """)
        
        # Add has_voted column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN has_voted TINYINT DEFAULT 0")
        except MySQLdb.Error:
            pass  # Column already exists
        
        # Create voting_periods table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS voting_periods (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                status ENUM('scheduled','active','ended') DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(100) NOT NULL,
                manually_stopped TINYINT DEFAULT 0,
                stopped_at DATETIME DEFAULT NULL,
                extended_count INT DEFAULT 0
            )
        """)

        # Create voting table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS voting (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                kandidat_id INT NOT NULL,
                voting_period_id INT NOT NULL,
                keaktifan INT DEFAULT 0,
                kepemimpinan INT DEFAULT 0,
                pengalaman INT DEFAULT 0,
                disiplin INT DEFAULT 0,
                komunikasi INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY (kandidat_id) REFERENCES anggota(id) ON DELETE CASCADE,
                FOREIGN KEY (voting_period_id) REFERENCES voting_periods(id) ON DELETE CASCADE,
                UNIQUE KEY unique_vote (user_id, kandidat_id, voting_period_id)
            )
        """)

        # Add rating columns to voting table if they don't exist (migration)
        try:
            cursor.execute("SELECT keaktifan FROM voting LIMIT 1")
        except:
            print("Adding rating columns to voting table...")
            alter_queries = [
                "ALTER TABLE voting ADD COLUMN keaktifan INT DEFAULT 0",
                "ALTER TABLE voting ADD COLUMN kepemimpinan INT DEFAULT 0",
                "ALTER TABLE voting ADD COLUMN pengalaman INT DEFAULT 0",
                "ALTER TABLE voting ADD COLUMN disiplin INT DEFAULT 0",
                "ALTER TABLE voting ADD COLUMN komunikasi INT DEFAULT 0"
            ]
            for query in alter_queries:
                try:
                    cursor.execute(query)
                except Exception as e:
                    print(f"Error executing migration: {e}")

        # Check if admin exists
        cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
        if not cursor.fetchone():
            hashed_password = generate_password_hash('admin123')
            cursor.execute(
                "INSERT INTO admin (username, password) VALUES (%s, %s)",
                ('admin', hashed_password)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def execute_query(query, params=None, fetch=False):
    """Execute database query"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            if fetch == 'one':
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        else:
            result = cursor.rowcount
            
        db.commit()
        cursor.close()
        return result
        
    except Exception as e:
        print(f"Database error: {e}")
        return None