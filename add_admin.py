#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk menambahkan admin baru ke database
K-Means Voting System

Usage:
    python add_admin.py
"""

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from werkzeug.security import generate_password_hash
import getpass
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'database': 'kmeans_voting'
}

def connect_db():
    """Connect to database"""
    try:
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            db=DB_CONFIG['database'],
            charset='utf8'
        )
        return conn
    except Exception as e:
        print(f"❌ Error koneksi database: {e}")
        print("\nPastikan:")
        print("1. MySQL server sudah berjalan")
        print("2. Database 'kmeans_voting' sudah dibuat")
        print("3. Kredensial database di DB_CONFIG sudah benar")
        sys.exit(1)

def check_username_exists(cursor, username):
    """Check if username already exists"""
    cursor.execute("SELECT COUNT(*) FROM admin WHERE username = %s", (username,))
    count = cursor.fetchone()[0]
    return count > 0

def list_admins(cursor):
    """List all existing admins"""
    cursor.execute("SELECT id, username FROM admin ORDER BY id")
    admins = cursor.fetchall()
    
    if admins:
        print("\n📋 Daftar Admin yang Ada:")
        print("-" * 40)
        for admin in admins:
            print(f"  ID: {admin[0]} | Username: {admin[1]}")
        print("-" * 40)
    else:
        print("\n⚠️  Belum ada admin di database")

def add_admin():
    """Main function to add new admin"""
    print("=" * 50)
    print("  TAMBAH ADMIN BARU - K-Means Voting System")
    print("=" * 50)
    
    # Connect to database
    conn = connect_db()
    cursor = conn.cursor()
    
    # Show existing admins
    list_admins(cursor)
    
    print("\n➕ Tambah Admin Baru")
    print("-" * 50)
    
    # Get username
    while True:
        username = input("\nUsername admin baru: ").strip()
        
        if not username:
            print("❌ Username tidak boleh kosong!")
            continue
        
        if len(username) < 3:
            print("❌ Username minimal 3 karakter!")
            continue
        
        if len(username) > 50:
            print("❌ Username maksimal 50 karakter!")
            continue
        
        # Check if username exists
        if check_username_exists(cursor, username):
            print(f"❌ Username '{username}' sudah digunakan!")
            retry = input("Coba username lain? (y/n): ").lower()
            if retry != 'y':
                print("\n❌ Dibatalkan")
                cursor.close()
                conn.close()
                sys.exit(0)
            continue
        
        break
    
    # Get password
    while True:
        password = getpass.getpass("\nPassword admin baru: ")
        
        if not password:
            print("❌ Password tidak boleh kosong!")
            continue
        
        if len(password) < 6:
            print("❌ Password minimal 6 karakter!")
            continue
        
        # Confirm password
        password_confirm = getpass.getpass("Konfirmasi password: ")
        
        if password != password_confirm:
            print("❌ Password tidak cocok!")
            retry = input("Coba lagi? (y/n): ").lower()
            if retry != 'y':
                print("\n❌ Dibatalkan")
                cursor.close()
                conn.close()
                sys.exit(0)
            continue
        
        break
    
    # Confirmation
    print("\n" + "=" * 50)
    print("📝 Konfirmasi Data Admin Baru:")
    print("-" * 50)
    print(f"  Username: {username}")
    print(f"  Password: {'*' * len(password)}")
    print("-" * 50)
    
    confirm = input("\nTambahkan admin ini? (y/n): ").lower()
    
    if confirm != 'y':
        print("\n❌ Dibatalkan")
        cursor.close()
        conn.close()
        sys.exit(0)
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    # Insert to database
    try:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        
        print("\n" + "=" * 50)
        print("✅ ADMIN BERHASIL DITAMBAHKAN!")
        print("=" * 50)
        print(f"  Username: {username}")
        print(f"  Password: (tersimpan dengan aman)")
        print("\n💡 Gunakan kredensial ini untuk login sebagai admin")
        print(f"   URL: http://127.0.0.1:5000/login")
        print("=" * 50)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error menambahkan admin: {e}")
        cursor.close()
        conn.close()
        sys.exit(1)
    
    # Show updated admin list
    list_admins(cursor)
    
    # Close connection
    cursor.close()
    conn.close()

def main():
    """Entry point"""
    try:
        add_admin()
    except KeyboardInterrupt:
        print("\n\n❌ Dibatalkan oleh user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
