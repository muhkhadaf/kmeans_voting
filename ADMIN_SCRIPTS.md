# Admin Management Scripts

Dokumentasi untuk skrip pengelolaan admin via command line.

## 📋 Daftar Skrip

### 1. `add_admin.py` - Tambah Admin Baru

Script untuk menambahkan admin baru ke sistem dengan mudah via terminal.

#### Cara Menggunakan:

```bash
python add_admin.py
```

#### Fitur:
- ✅ Menampilkan daftar admin yang sudah ada
- ✅ Input username dengan validasi
- ✅ Input password dengan konfirmasi (hidden input)
- ✅ Validasi username tidak duplikat
- ✅ Validasi password minimal 6 karakter
- ✅ Password di-hash dengan aman
- ✅ Konfirmasi sebelum menyimpan

#### Contoh Output:

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

==================================================
📝 Konfirmasi Data Admin Baru:
--------------------------------------------------
  Username: admin2
  Password: ******
--------------------------------------------------

Tambahkan admin ini? (y/n): y

==================================================
✅ ADMIN BERHASIL DITAMBAHKAN!
==================================================
  Username: admin2
  Password: (tersimpan dengan aman)

💡 Gunakan kredensial ini untuk login sebagai admin
   URL: http://127.0.0.1:5000/login
==================================================
```

---

### 2. `manage_admin.py` - Kelola Admin (Menu Lengkap)

Script untuk mengelola admin dengan berbagai fitur: lihat, tambah, hapus, dan ganti password.

#### Cara Menggunakan:

```bash
python manage_admin.py
```

#### Menu:

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
```

#### Fitur per Menu:

##### [1] Lihat Daftar Admin
- Menampilkan semua admin dengan ID dan username
- Berguna untuk melihat admin yang tersedia

##### [2] Tambah Admin Baru
- Input username dan password
- Validasi duplikat username
- Validasi password minimal 6 karakter
- Konfirmasi password

##### [3] Hapus Admin
- Pilih admin berdasarkan ID
- Konfirmasi sebelum menghapus
- **Tidak bisa menghapus admin terakhir** (safety feature)
- Menampilkan username yang akan dihapus

##### [4] Ganti Password Admin
- Pilih admin berdasarkan ID
- Verifikasi password lama
- Input password baru dengan konfirmasi
- Password minimal 6 karakter

---

## 🔒 Keamanan

### Password Hashing
- Semua password di-hash menggunakan `werkzeug.security`
- Menggunakan algoritma PBKDF2 dengan salt
- Password tidak pernah disimpan dalam bentuk plain text

### Input Validation
- Username: 3-50 karakter, tidak boleh duplikat
- Password: minimal 6 karakter
- Konfirmasi password harus cocok

### Safety Features
- Tidak bisa menghapus admin terakhir
- Perlu verifikasi password lama untuk ganti password
- Konfirmasi sebelum operasi destructive (hapus)
- Hidden input untuk password (tidak terlihat saat diketik)

---

## 🛠️ Troubleshooting

### Error: "Error koneksi database"

**Penyebab:**
- MySQL server tidak berjalan
- Database 'kmeans_voting' belum dibuat
- Kredensial database salah

**Solusi:**
1. Pastikan MySQL server berjalan:
   ```bash
   # Windows
   net start MySQL
   
   # Linux/Mac
   sudo service mysql start
   ```

2. Buat database jika belum ada:
   ```sql
   CREATE DATABASE kmeans_voting;
   ```

3. Periksa kredensial di `DB_CONFIG` dalam skrip:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': '',  # Sesuaikan dengan password MySQL Anda
       'database': 'kmeans_voting'
   }
   ```

### Error: "Username sudah digunakan"

**Penyebab:**
- Username yang diinput sudah ada di database

**Solusi:**
- Gunakan username yang berbeda
- Atau hapus admin lama dengan username tersebut terlebih dahulu

### Error: "Password minimal 6 karakter"

**Penyebab:**
- Password yang diinput kurang dari 6 karakter

**Solusi:**
- Gunakan password minimal 6 karakter
- Rekomendasi: gunakan kombinasi huruf, angka, dan simbol

### Error: "Tidak bisa menghapus admin terakhir"

**Penyebab:**
- Mencoba menghapus satu-satunya admin yang tersisa

**Solusi:**
- Tambahkan admin baru terlebih dahulu
- Baru kemudian hapus admin lama

---

## 📝 Best Practices

### 1. Backup Database Sebelum Menghapus Admin
```bash
mysqldump -u root -p kmeans_voting > backup_before_delete.sql
```

### 2. Gunakan Password yang Kuat
- Minimal 8 karakter (lebih baik dari minimal 6)
- Kombinasi huruf besar dan kecil
- Tambahkan angka dan simbol
- Jangan gunakan password yang mudah ditebak

### 3. Catat Kredensial Admin
- Simpan username dan password di tempat yang aman
- Jangan bagikan kredensial admin
- Ganti password secara berkala

### 4. Minimal 2 Admin
- Selalu miliki minimal 2 admin
- Jika satu admin lupa password, admin lain bisa membantu
- Backup jika terjadi masalah

---

## 🔄 Workflow Rekomendasi

### Setup Awal:
1. Install aplikasi dan database
2. Jalankan `python app.py` untuk inisialisasi database
3. Login dengan admin default (admin/admin123)
4. Gunakan `add_admin.py` untuk tambah admin baru
5. Ganti password admin default via `manage_admin.py`

### Maintenance:
1. Gunakan `manage_admin.py` untuk kelola admin
2. Backup database secara berkala
3. Ganti password admin secara berkala
4. Hapus admin yang tidak aktif

---

## 📚 Referensi

- **USER_GUIDE.md** - Panduan lengkap penggunaan aplikasi
- **INSTALLATION.md** - Panduan instalasi
- **CHANGELOG.md** - Riwayat perubahan
- **README.md** - Overview aplikasi

---

## 💡 Tips

### Menggunakan getpass
Script ini menggunakan `getpass` untuk input password yang aman:
- Password tidak terlihat saat diketik
- Lebih aman dari `input()` biasa
- Standard library Python, tidak perlu install

### Keyboard Interrupt
Tekan `Ctrl+C` kapan saja untuk membatalkan operasi:
```
^C
❌ Dibatalkan oleh user
```

### Database Configuration
Jika menggunakan konfigurasi database yang berbeda, edit `DB_CONFIG` di kedua skrip:
```python
DB_CONFIG = {
    'host': 'localhost',      # Ganti jika MySQL di server lain
    'user': 'root',           # Ganti dengan user MySQL Anda
    'password': 'mypass',     # Ganti dengan password MySQL Anda
    'database': 'kmeans_voting'
}
```

---

**Dibuat untuk K-Means Voting System v2.1.0**

