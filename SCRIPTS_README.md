# 🛠️ Utilitas Scripts - K-Means Voting System

Kumpulan skrip Python untuk memudahkan pengelolaan sistem.

## 📋 Daftar Scripts

| Script | Fungsi | Dokumentasi |
|--------|--------|-------------|
| `add_admin.py` | Tambah admin baru via terminal | [ADMIN_SCRIPTS.md](ADMIN_SCRIPTS.md) |
| `manage_admin.py` | Kelola admin (menu lengkap) | [ADMIN_SCRIPTS.md](ADMIN_SCRIPTS.md) |
| `migrate_db.py` | Migrasi database v1.0 ke v2.0 | [CHANGELOG.md](CHANGELOG.md) |
| `update_database.py` | Update struktur database | - |

---

## 🚀 Quick Start

### 1. Tambah Admin Baru

```bash
python add_admin.py
```

**Output:**
```
==================================================
  TAMBAH ADMIN BARU - K-Means Voting System
==================================================

📋 Daftar Admin yang Ada:
----------------------------------------
  ID: 1 | Username: admin
----------------------------------------

➕ Tambah Admin Baru
--------------------------------------------------

Username admin baru: admin2
Password admin baru: ******
Konfirmasi password: ******

✅ ADMIN BERHASIL DITAMBAHKAN!
```

---

### 2. Kelola Admin (Menu)

```bash
python manage_admin.py
```

**Menu:**
```
==================================================
  KELOLA ADMIN - K-Means Voting System
==================================================

📋 Menu:
  [1] Lihat Daftar Admin
  [2] Tambah Admin Baru
  [3] Hapus Admin
  [4] Ganti Password Admin
  [0] Keluar
--------------------------------------------------

Pilih menu: 
```

---

### 3. Migrasi Database (v1.0 → v2.0)

```bash
python migrate_db.py
```

**Fungsi:**
- Backup data lama ke `anggota_backup`
- Update struktur tabel `anggota`
- Buat tabel `penilaian` baru
- Migrasi aman dengan rollback

---

## 📖 Dokumentasi Lengkap

### Admin Management
- **[ADMIN_SCRIPTS.md](ADMIN_SCRIPTS.md)** - Dokumentasi lengkap untuk `add_admin.py` dan `manage_admin.py`
  - Cara penggunaan
  - Fitur dan validasi
  - Troubleshooting
  - Best practices

### User Guide
- **[USER_GUIDE.md](USER_GUIDE.md)** - Panduan penggunaan aplikasi
  - Untuk admin
  - Untuk user
  - FAQ

### Installation
- **[INSTALLATION.md](INSTALLATION.md)** - Panduan instalasi
  - Requirements
  - Setup database
  - Konfigurasi

### Changelog
- **[CHANGELOG.md](CHANGELOG.md)** - Riwayat perubahan
  - Fitur baru
  - Bug fixes
  - Breaking changes

---

## 🔧 Requirements

Semua skrip memerlukan:

```bash
pip install pymysql werkzeug
```

**Catatan:** Jika sudah install requirements aplikasi, dependencies sudah tersedia.

---

## 💡 Tips

### 1. Jalankan dari Root Directory
```bash
# Benar
cd kmeans_voting
python add_admin.py

# Salah
cd kmeans_voting/templates
python ../add_admin.py  # Bisa error path
```

### 2. Pastikan MySQL Running
```bash
# Windows
net start MySQL

# Linux/Mac
sudo service mysql start
```

### 3. Backup Sebelum Operasi Penting
```bash
# Backup database
mysqldump -u root -p kmeans_voting > backup.sql

# Restore jika ada masalah
mysql -u root -p kmeans_voting < backup.sql
```

### 4. Konfigurasi Database
Edit `DB_CONFIG` di setiap skrip jika perlu:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Ganti dengan password MySQL Anda
    'database': 'kmeans_voting'
}
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pymysql'"
```bash
pip install pymysql
```

### Error: "Error koneksi database"
1. Pastikan MySQL running
2. Cek kredensial di `DB_CONFIG`
3. Pastikan database `kmeans_voting` sudah dibuat

### Error: "Permission denied"
```bash
# Linux/Mac - tambahkan execute permission
chmod +x add_admin.py
chmod +x manage_admin.py
```

---

## 📞 Support

Jika mengalami masalah:

1. Baca dokumentasi terkait
2. Cek troubleshooting di [ADMIN_SCRIPTS.md](ADMIN_SCRIPTS.md)
3. Periksa log error
4. Hubungi administrator sistem

---

## 🔄 Update Scripts

Jika ada update pada skrip:

```bash
# Pull latest version
git pull origin main

# Atau download manual dari repository
```

---

**K-Means Voting System v2.1.0**  
**Last Updated:** 24 November 2024

