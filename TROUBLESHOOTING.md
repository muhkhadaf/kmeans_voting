# Troubleshooting Guide - K-Means Voting System

## 🔧 Panduan Mengatasi Masalah Umum

### 1. Error Database

#### Error: "Can't create table (errno: 150 Foreign key constraint)"

**Penyebab:** Urutan pembuatan tabel salah. Foreign key dibuat sebelum tabel referensi ada.

**Solusi:**
1. Drop database dan buat ulang:
   ```sql
   DROP DATABASE kmeans_voting;
   CREATE DATABASE kmeans_voting;
   ```
2. Restart aplikasi untuk inisialisasi ulang database

**Pencegahan:** Pastikan urutan tabel di `db.py`:
1. admin
2. user
3. anggota
4. penilaian (referensi user & anggota)
5. voting_periods
6. voting (referensi user, anggota, voting_periods)

---

#### Error: "Access denied for user 'root'@'localhost'"

**Penyebab:** Password MySQL salah atau user tidak memiliki akses.

**Solusi:**
1. Buka `db.py`
2. Update konfigurasi database:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_mysql_password',  # Ganti dengan password Anda
       'database': 'kmeans_voting'
   }
   ```

---

#### Error: "Unknown database 'kmeans_voting'"

**Penyebab:** Database belum dibuat.

**Solusi:**
1. Buka MySQL command line atau phpMyAdmin
2. Jalankan:
   ```sql
   CREATE DATABASE kmeans_voting;
   ```
3. Restart aplikasi

---

### 2. Error K-Means Clustering

#### Error: "decimal.InvalidOperation: DivisionUndefined"

**Penyebab:** Pembagian dengan nol saat normalisasi data (semua nilai dalam satu kriteria sama).

**Solusi:** Sudah diperbaiki di v2.1.0 dengan safe division.

**Jika masih terjadi:**
1. Pastikan ada variasi nilai penilaian
2. Minta user memberikan penilaian yang berbeda-beda
3. Minimal 3 anggota dengan penilaian yang bervariasi

---

#### Error: "Minimal 3 anggota dengan penilaian diperlukan"

**Penyebab:** Tidak cukup data untuk clustering.

**Solusi:**
1. Tambahkan minimal 3 anggota
2. Minta user memberikan penilaian untuk anggota tersebut
3. Pastikan setiap anggota memiliki minimal 1 penilaian

---

### 3. Error Instalasi

#### Error: "ModuleNotFoundError: No module named 'flask'"

**Penyebab:** Dependencies belum diinstall.

**Solusi:**
```bash
pip install Flask numpy Werkzeug pytz pymysql
```

---

#### Error: "Microsoft Visual C++ 14.0 or greater is required"

**Penyebab:** Mencoba install `mysqlclient` yang memerlukan compiler C++.

**Solusi:** Gunakan PyMySQL sebagai pengganti:
```bash
pip install pymysql
```

Tambahkan di `db.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

### 4. Error Login

#### Error: "Username atau password salah" (Admin)

**Solusi:**
1. Pastikan menggunakan kredensial default:
   - Username: `admin`
   - Password: `admin123`

2. Jika lupa password, reset via MySQL:
   ```sql
   USE kmeans_voting;
   UPDATE admin SET password = 'scrypt:32768:8:1$...' WHERE username = 'admin';
   ```

3. Atau jalankan script reset:
   ```python
   from werkzeug.security import generate_password_hash
   print(generate_password_hash('admin123'))
   ```

---

#### Error: "Username atau password salah" (User)

**Solusi:**
1. Hubungi admin untuk cek username
2. Minta admin reset password
3. Setelah login, segera ganti password sendiri

---

### 5. Error Ganti Password

#### Error: "Password lama salah"

**Penyebab:** Password yang dimasukkan tidak sesuai dengan password saat ini.

**Solusi:**
1. Pastikan memasukkan password yang benar
2. Jika lupa, hubungi admin untuk reset
3. Coba logout dan login ulang untuk memastikan password

---

#### Error: "Password baru minimal 6 karakter"

**Penyebab:** Password terlalu pendek.

**Solusi:** Gunakan password minimal 6 karakter.

---

### 6. Error Voting

#### Error: "Voting tidak diizinkan saat ini"

**Penyebab:** Periode voting belum dimulai atau sudah berakhir.

**Solusi:**
1. Cek status periode voting di halaman admin
2. Tunggu hingga periode voting aktif
3. Hubungi admin untuk memulai periode voting

---

#### Error: "Anda sudah melakukan voting pada periode ini"

**Penyebab:** User sudah voting sebelumnya.

**Solusi:** Setiap user hanya dapat voting sekali per periode. Tidak dapat diubah.

---

### 7. Error Hapus User

#### Error: "User tidak ditemukan"

**Penyebab:** User ID tidak valid atau sudah dihapus.

**Solusi:** Refresh halaman dan coba lagi.

---

#### Warning: "Menghapus user akan menghapus semua penilaian dan voting"

**Bukan Error:** Ini adalah peringatan normal.

**Catatan:**
- Cascade delete akan menghapus semua data terkait
- Pastikan backup data jika diperlukan
- Jangan hapus user setelah periode penilaian/voting dimulai

---

### 8. Error Server

#### Error: "Address already in use"

**Penyebab:** Port 5000 sudah digunakan aplikasi lain.

**Solusi 1:** Matikan aplikasi yang menggunakan port 5000

**Solusi 2:** Ubah port di `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Ganti ke port lain
```

---

#### Error: "Connection refused"

**Penyebab:** Server tidak berjalan atau firewall memblokir.

**Solusi:**
1. Pastikan server berjalan: `python app.py`
2. Cek firewall Windows
3. Akses menggunakan `http://127.0.0.1:5000` bukan `localhost`

---

### 9. Error Template

#### Error: "TemplateNotFound"

**Penyebab:** File template tidak ditemukan.

**Solusi:**
1. Pastikan struktur folder:
   ```
   kmeans_voting/
   ├── app.py
   ├── db.py
   └── templates/
       ├── base.html
       ├── login.html
       ├── user_login.html
       ├── user_change_password.html
       └── ...
   ```
2. Pastikan nama file template sesuai dengan yang dipanggil di route

---

### 10. Error Session

#### Error: "Please log in to access this page"

**Penyebab:** Session expired atau belum login.

**Solusi:**
1. Login ulang
2. Jika sering terjadi, tingkatkan session timeout di `app.py`:
   ```python
   from datetime import timedelta
   app.permanent_session_lifetime = timedelta(hours=2)
   ```

---

## 🐛 Debug Mode

### Mengaktifkan Debug Mode

Di `app.py`, pastikan:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Melihat Error Detail

1. Buka browser
2. Akses halaman yang error
3. Lihat traceback di terminal
4. Atau lihat di browser jika debug mode aktif

---

## 📊 Cek Status Sistem

### Cek Database Connection

```python
python -c "from db import init_db; init_db(); print('✓ Database OK')"
```

### Cek Import Modules

```python
python -c "from app import app; print('✓ App OK')"
```

### Cek MySQL Service

**Windows:**
```bash
net start MySQL
```

**Linux/Mac:**
```bash
sudo systemctl status mysql
```

---

## 🔍 Log Files

### Melihat Error Log

Jika menggunakan production server (gunicorn/uwsgi), cek log:

```bash
tail -f /var/log/kmeans_voting/error.log
```

### Flask Development Log

Error akan muncul di terminal tempat menjalankan `python app.py`

---

## 💾 Backup & Restore

### Backup Database

```bash
mysqldump -u root -p kmeans_voting > backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
mysql -u root -p kmeans_voting < backup_20241124.sql
```

---

## 🆘 Bantuan Lebih Lanjut

Jika masalah tidak teratasi:

1. **Cek Dokumentasi:**
   - README.md
   - USER_GUIDE.md
   - INSTALLATION.md

2. **Cek Versi:**
   - Python: `python --version` (minimal 3.7)
   - MySQL: `mysql --version` (minimal 5.7)
   - Flask: `pip show flask`

3. **Reset Sistem:**
   ```bash
   # Backup data
   mysqldump -u root -p kmeans_voting > backup.sql
   
   # Drop dan buat ulang database
   mysql -u root -p -e "DROP DATABASE kmeans_voting; CREATE DATABASE kmeans_voting;"
   
   # Restart aplikasi
   python app.py
   ```

4. **Hubungi Administrator**

---

## 📝 Melaporkan Bug

Gunakan template ini:

```
**Bug Title:** [Judul singkat]

**Error Message:**
[Copy paste error lengkap]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected:** [Yang seharusnya terjadi]
**Actual:** [Yang sebenarnya terjadi]

**Environment:**
- OS: Windows/Linux/Mac
- Python: 3.x.x
- MySQL: 5.x.x
- Browser: Chrome/Firefox/etc

**Screenshots:** [Jika ada]
```

---

**Last Updated:** 24 November 2024  
**Version:** 2.1.0

