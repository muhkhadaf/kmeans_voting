# Panduan Instalasi - K-Means Voting System v2.0

## 📋 Prasyarat

Sebelum memulai instalasi, pastikan sistem Anda memiliki:

- Python 3.7 atau lebih tinggi
- MySQL Server 5.7 atau lebih tinggi
- pip (Python package manager)
- Git (opsional, untuk clone repository)

## 🚀 Instalasi Baru (Fresh Install)

### 1. Download/Clone Project

```bash
# Menggunakan Git
git clone https://github.com/muhkhadaf/kmeans_voting.git
cd kmeans_voting

# Atau download ZIP dan extract
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies yang akan diinstall:
- Flask (web framework)
- MySQLdb (database connector)
- numpy (untuk K-Means algorithm)
- pytz (timezone handling)
- werkzeug (security utilities)

### 3. Setup Database

#### a. Buat Database

Buka MySQL client dan jalankan:

```sql
CREATE DATABASE kmeans_voting CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### b. Konfigurasi Database

Edit file `db.py` sesuai dengan konfigurasi MySQL Anda:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Ganti dengan username MySQL Anda
    'password': '',           # Ganti dengan password MySQL Anda
    'database': 'kmeans_voting'
}
```

### 4. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan:
- Otomatis membuat tabel-tabel yang diperlukan
- Membuat akun admin default (username: admin, password: admin123)
- Berjalan di `http://127.0.0.1:5000`

### 5. Login Pertama Kali

#### Admin:
- URL: `http://127.0.0.1:5000/login`
- Username: `admin`
- Password: `admin123`

**⚠️ PENTING:** Segera ganti password admin setelah login pertama!

## 🔄 Migrasi dari Versi Lama (v1.0 ke v2.0)

Jika Anda sudah menggunakan versi lama sistem ini, ikuti langkah berikut:

### 1. Backup Database Lama

```bash
mysqldump -u root -p kmeans_voting > backup_kmeans_voting_v1.sql
```

### 2. Update File Aplikasi

```bash
# Backup file lama
cp app.py app.py.backup
cp db.py db.py.backup

# Download/copy file baru
# Ganti dengan file app.py dan db.py versi baru
```

### 3. Jalankan Script Migrasi

```bash
python migrate_db.py
```

Script ini akan:
- Membuat struktur tabel baru
- Backup data lama ke tabel `anggota_backup`
- Membuat tabel `penilaian` untuk sistem penilaian user

### 4. Input Ulang Data Anggota

Karena struktur data berubah, Anda perlu:

1. Login sebagai admin
2. Buka menu "Data Anggota"
3. Tambahkan anggota dengan format baru:
   - Nama
   - Pendidikan (SD/SMP/SMA/D3/S1/S2/S3)
   - Visi & Misi

### 5. Instruksikan User untuk Memberikan Penilaian

Setelah anggota ditambahkan:
1. User login ke sistem
2. Berikan penilaian untuk setiap anggota
3. Setelah cukup penilaian terkumpul, admin dapat menjalankan analisis

## 🔧 Konfigurasi Lanjutan

### Mengubah Port Server

Edit file `app.py` bagian bawah:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Ganti 5001 dengan port yang diinginkan
```

### Mengubah Secret Key

Edit file `app.py`:

```python
app.secret_key = 'ganti-dengan-random-string-yang-aman'
```

Generate secret key yang aman:

```python
import secrets
print(secrets.token_hex(32))
```

### Mengubah Timezone

Edit file `app.py`:

```python
SERVER_TIMEZONE = pytz.timezone('Asia/Jakarta')  # Ganti sesuai timezone Anda
```

Daftar timezone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## 📝 Setup Awal Setelah Instalasi

### 1. Tambah User

Login sebagai admin, kemudian:
1. Menu "Voting & User"
2. Tab "Manajemen User"
3. Klik "Tambah User"
4. Isi data user (nama, username, password)

### 2. Tambah Anggota

1. Menu "Data Anggota"
2. Klik "Tambah Anggota"
3. Isi:
   - Nama lengkap
   - Pendidikan terakhir
   - Visi & Misi (opsional)

### 3. Instruksikan User Memberikan Penilaian

Berikan instruksi kepada user:
1. Login ke sistem
2. Akan otomatis diarahkan ke halaman penilaian
3. Beri penilaian untuk setiap anggota (5 kriteria)
4. Penilaian dapat diubah kapan saja

### 4. Jalankan Analisis K-Means

Setelah cukup penilaian terkumpul:
1. Menu "Analisis K-Means"
2. Klik "Jalankan Analisis K-Means"
3. Sistem akan mengelompokkan anggota menjadi 3 cluster
4. Pilih anggota untuk dijadikan kandidat

### 5. Buat Periode Voting

1. Menu "Periode Voting"
2. Klik "Buat Periode Baru"
3. Isi:
   - Nama periode
   - Deskripsi
   - Waktu mulai
   - Waktu berakhir
4. Klik "Mulai Voting" saat siap

### 6. User Melakukan Voting

User dapat:
1. Login ke sistem
2. Klik menu "Voting" di header
3. Pilih kandidat
4. Konfirmasi pilihan

### 7. Lihat Hasil

Admin dapat melihat hasil:
1. Menu "Hasil Voting"
2. Pilih periode voting
3. Lihat hasil dan statistik

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

```bash
# Install ulang dependencies
pip install -r requirements.txt
```

### Error: Can't connect to MySQL server

1. Pastikan MySQL server berjalan:
   ```bash
   # Windows
   net start MySQL80
   
   # Linux
   sudo systemctl start mysql
   ```

2. Periksa konfigurasi di `db.py`

### Error: Access denied for user

Periksa username dan password MySQL di `db.py`

### Error: Database doesn't exist

Buat database terlebih dahulu:
```sql
CREATE DATABASE kmeans_voting;
```

### Error: Port already in use

Ganti port di `app.py` atau hentikan aplikasi yang menggunakan port 5000

### Data Anggota Lama Hilang Setelah Migrasi

Data lama tersimpan di tabel `anggota_backup`. Anda dapat melihatnya dengan:

```sql
SELECT * FROM anggota_backup;
```

Namun, data harus diinput ulang dengan format baru karena struktur berbeda.

## 📞 Bantuan

Jika mengalami masalah:

1. Periksa log error di terminal
2. Pastikan semua dependencies terinstall
3. Periksa konfigurasi database
4. Baca dokumentasi troubleshooting di README.md

## ✅ Checklist Instalasi

- [ ] Python 3.7+ terinstall
- [ ] MySQL Server berjalan
- [ ] Dependencies terinstall (`pip install -r requirements.txt`)
- [ ] Database `kmeans_voting` dibuat
- [ ] Konfigurasi database di `db.py` sudah benar
- [ ] Aplikasi berjalan tanpa error
- [ ] Bisa login sebagai admin
- [ ] Password admin sudah diganti
- [ ] User sudah ditambahkan
- [ ] Anggota sudah ditambahkan
- [ ] User sudah memberikan penilaian
- [ ] Analisis K-Means berhasil dijalankan
- [ ] Kandidat sudah ditetapkan
- [ ] Periode voting sudah dibuat

---

**Selamat! Sistem K-Means Voting sudah siap digunakan! 🎉**
