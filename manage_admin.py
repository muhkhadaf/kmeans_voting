#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk mengelola admin di database
K-Means Voting System

Usage:
    python manage_admin.py
"""

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
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
        sys.exit(1)

def list_admins(cursor):
    """List all admins"""
    cursor.execute("SELECT id, username FROM admin ORDER BY id")
    admins = cursor.fetchall()
    
    if admins:
        print("\n📋 Daftar Admin:")
        print("-" * 40)
        for admin in admins:
            print(f"  [{admin[0]}] {admin[1]}")
        print("-" * 40)
        return admins
    else:
        print("\n⚠️  Belum ada admin di database")
        return []

def add_admin(conn, cursor):
    """Add new admin"""
    print("\n➕ TAMBAH ADMIN BARU")
    print("-" * 50)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username tidak boleh kosong!")
        return
    
    # Check if exists
    cursor.execute("SELECT COUNT(*) FROM admin WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        print(f"❌ Username '{username}' sudah digunakan!")
        return
    
    password = getpass.getpass("Password: ")
    if len(password) < 6:
        print("❌ Password minimal 6 karakter!")
        return
    
    password_confirm = getpass.getpass("Konfirmasi password: ")
    if password != password_confirm:
        print("❌ Password tidak cocok!")
        return
    
    hashed_password = generate_password_hash(password)
    
    try:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        print(f"✅ Admin '{username}' berhasil ditambahkan!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")

def delete_admin(conn, cursor):
    """Delete admin"""
    admins = list_admins(cursor)
    if not admins:
        return
    
    print("\n🗑️  HAPUS ADMIN")
    print("-" * 50)
    
    try:
        admin_id = int(input("Masukkan ID admin yang akan dihapus: "))
    except ValueError:
        print("❌ ID harus berupa angka!")
        return
    
    # Get admin info
    cursor.execute("SELECT username FROM admin WHERE id = %s", (admin_id,))
    admin = cursor.fetchone()
    
    if not admin:
        print(f"❌ Admin dengan ID {admin_id} tidak ditemukan!")
        return
    
    username = admin[0]
    
    # Count total admins
    cursor.execute("SELECT COUNT(*) FROM admin")
    total_admins = cursor.fetchone()[0]
    
    if total_admins <= 1:
        print("❌ Tidak bisa menghapus admin terakhir!")
        return
    
    confirm = input(f"Yakin ingin menghapus admin '{username}'? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Dibatalkan")
        return
    
    try:
        cursor.execute("DELETE FROM admin WHERE id = %s", (admin_id,))
        conn.commit()
        print(f"✅ Admin '{username}' berhasil dihapus!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")

def change_password(conn, cursor):
    """Change admin password"""
    admins = list_admins(cursor)
    if not admins:
        return
    
    print("\n🔑 GANTI PASSWORD ADMIN")
    print("-" * 50)
    
    try:
        admin_id = int(input("Masukkan ID admin: "))
    except ValueError:
        print("❌ ID harus berupa angka!")
        return
    
    # Get admin info
    cursor.execute("SELECT username, password FROM admin WHERE id = %s", (admin_id,))
    admin = cursor.fetchone()
    
    if not admin:
        print(f"❌ Admin dengan ID {admin_id} tidak ditemukan!")
        return
    
    username = admin[0]
    current_hash = admin[1]
    
    print(f"\nGanti password untuk: {username}")
    
    # Verify current password
    current_password = getpass.getpass("Password lama: ")
    if not check_password_hash(current_hash, current_password):
        print("❌ Password lama salah!")
        return
    
    # Get new password
    new_password = getpass.getpass("Password baru: ")
    if len(new_password) < 6:
        print("❌ Password minimal 6 karakter!")
        return
    
    password_confirm = getpass.getpass("Konfirmasi password baru: ")
    if new_password != password_confirm:
        print("❌ Password tidak cocok!")
        return
    
    hashed_password = generate_password_hash(new_password)
    
    try:
        cursor.execute(
            "UPDATE admin SET password = %s WHERE id = %s",
            (hashed_password, admin_id)
        )
        conn.commit()
        print(f"✅ Password admin '{username}' berhasil diubah!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")

def show_menu():
    """Show main menu"""
    print("\n" + "=" * 50)
    print("  KELOLA ADMIN - K-Means Voting System")
    print("=" * 50)
    print("\n📋 Menu:")
    print("  [1] Lihat Daftar Admin")
    print("  [2] Tambah Admin Baru")
    print("  [3] Hapus Admin")
    print("  [4] Ganti Password Admin")
    print("  [0] Keluar")
    print("-" * 50)

def main():
    """Main function"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        while True:
            show_menu()
            choice = input("\nPilih menu: ").strip()
            
            if choice == '1':
                list_admins(cursor)
            elif choice == '2':
                add_admin(conn, cursor)
            elif choice == '3':
                delete_admin(conn, cursor)
            elif choice == '4':
                change_password(conn, cursor)
            elif choice == '0':
                print("\n👋 Terima kasih!")
                break
            else:
                print("❌ Pilihan tidak valid!")
            
            input("\nTekan Enter untuk melanjutkan...")
    
    except KeyboardInterrupt:
        print("\n\n❌ Dibatalkan oleh user")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
