# Quick Start Guide - K-Means Voting System

## 🚀 Mulai Cepat dalam 5 Menit

### Prasyarat
- Python 3.7+ terinstall
- MySQL/MariaDB terinstall dan berjalan
- Browser modern (Chrome, Firefox, Edge)

---

## 📦 Instalasi

### 1. Clone atau Download Project

```bash
cd C:\program_freelance\kmeans_voting
```

### 2. Install Dependencies

```bash
pip install Flask numpy Werkzeug pytz pymysql
```

### 3. Setup Database

**Buka MySQL:**
```bash
mysql -u root -p
```

**Buat Database:**
```sql
CREATE DATABASE kmeans_voting;
EXIT;
```

### 4. Konfigurasi Database

Edit `db.py` jika perlu:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Ganti dengan password MySQL Anda
    'database': 'kmeans_voting'
}
```

### 5. Jalankan Aplikasi

```bash
python app.py
```

**Output yang diharapkan:**
```
Database initialized successfully!
 * Running on http://127.0.0.1:5000
```

---

## 🎯 Penggunaan Pertama Kali

### Langkah 1: Login Admin

1. Buka browser: `http://127.0.0.1:5000`
2. Login dengan:
   - Username: `admin`
   - Password: `admin123`

### Langkah 2: Tambah Anggota

1. Klik menu **"Data Anggota"**
2. Klik **"Tambah Anggota"**
3. Isi data:
   - Nama: `John Doe`
   - Pendidikan: `S1`
   - Visi Misi: `Memajukan organisasi...`
4. Klik **"Simpan"**
5. Ulangi untuk minimal 3 anggota

### Langkah 3: Tambah User

1. Klik menu **"Voting & User"**
2. Klik **"Tambah User"**
3. Isi data:
   - Nama: `User Test`
   - Username: `user1`
   - Password: `user123`
4. Klik **"Tambah User"**
5. Ulangi untuk beberapa user

### Langkah 4: User Memberikan Penilaian

1. Buka tab baru: `http://127.0.0.1:5000/user_login`
2. Login sebagai user (`user1` / `user123`)
3. Akan otomatis masuk ke halaman **Penilaian**
4. Klik **"Beri Penilaian"** pada setiap anggota
5. Geser slider untuk memberikan nilai (1-100):
   - Keaktifan: 80
   - Kepemimpinan: 75
   - Pengalaman: 70
   - Disiplin: 85
   - Komunikasi: 90
6. Klik **"Simpan Penilaian"**
7. Ulangi untuk semua anggota

### Langkah 5: Jalankan Analisis K-Means

1. Kembali ke tab admin
2. Klik menu **"Analisis K-Means"**
3. Klik **"Jalankan Analisis K-Means"**
4. Lihat hasil clustering:
   - Sangat Layak
   - Cukup Layak
   - Kurang Layak

### Langkah 6: Tetapkan Kandidat

1. Di halaman **"Hasil Analisis"**
2. Centang anggota yang ingin dijadikan kandidat
3. Klik **"Tetapkan Kandidat"**

### Langkah 7: Buat Periode Voting

1. Klik menu **"Periode Voting"**
2. Klik **"Buat Periode Baru"**
3. Isi:
   - Nama: `Pemilihan Ketua 2024`
   - Deskripsi: `Pemilihan ketua periode 2024-2025`
   - Waktu Mulai: (pilih tanggal/jam)
   - Waktu Berakhir: (pilih tanggal/jam)
4. Klik **"Buat Periode"**
5. Klik **"Mulai Sekarang"** jika ingin mulai langsung

### Langkah 8: User Melakukan Voting

1. Kembali ke tab user
2. Klik menu **"Voting"**
3. Lihat daftar kandidat dengan penilaian
4. Klik **"Pilih Kandidat"** pada kandidat pilihan
5. Konfirmasi pilihan
6. Selesai!

### Langkah 9: Lihat Hasil Voting

1. Kembali ke tab admin
2. Klik menu **"Hasil Voting"**
3. Lihat hasil real-time:
   - Jumlah suara per kandidat
   - Persentase
   - Kandidat terdepan

---

## 🎓 Fitur Tambahan

### Ganti Password (User)

1. Login sebagai user
2. Klik **"Ganti Password"** di header
3. Isi password lama dan password baru
4. Klik **"Simpan Password Baru"**

### Hapus User (Admin)

1. Login sebagai admin
2. Buka **"Voting & User"**
3. Klik ikon **trash** pada user yang ingin dihapus
4. Konfirmasi penghapusan

---

## 📊 Contoh Data Testing

### Anggota (minimal 3):

| Nama | Pendidikan | Visi Misi |
|------|------------|-----------|
| Ahmad Rizki | S1 | Meningkatkan partisipasi pemuda |
| Siti Nurhaliza | S1 | Mengembangkan kreativitas anggota |
| Budi Santoso | SMA | Membangun solidaritas organisasi |

### User (minimal 2):

| Nama | Username | Password |
|------|----------|----------|
| User Satu | user1 | user123 |
| User Dua | user2 | user123 |

### Penilaian (contoh untuk Ahmad Rizki):

| Kriteria | Nilai |
|----------|-------|
| Keaktifan | 85 |
| Kepemimpinan | 80 |
| Pengalaman | 75 |
| Disiplin | 90 |
| Komunikasi | 85 |

---

## 🔧 Troubleshooting Cepat

### Error: "Can't connect to MySQL"
```bash
# Cek MySQL berjalan
net start MySQL

# Atau restart MySQL
net stop MySQL
net start MySQL
```

### Error: "ModuleNotFoundError"
```bash
# Install ulang dependencies
pip install Flask numpy Werkzeug pytz pymysql
```

### Error: "Port already in use"
```python
# Edit app.py, ganti port
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error: "Division by zero" saat K-Means
- Pastikan ada variasi nilai penilaian
- Jangan semua user memberikan nilai yang sama persis
- Minimal 3 anggota dengan penilaian berbeda

---

## 📚 Dokumentasi Lengkap

- **README.md** - Overview dan fitur
- **INSTALLATION.md** - Instalasi detail
- **USER_GUIDE.md** - Panduan lengkap untuk admin dan user
- **TROUBLESHOOTING.md** - Solusi masalah umum
- **CHANGELOG.md** - Riwayat perubahan

---

## 🎯 Checklist Setup

- [ ] Python 3.7+ terinstall
- [ ] MySQL terinstall dan berjalan
- [ ] Dependencies terinstall
- [ ] Database `kmeans_voting` dibuat
- [ ] Aplikasi berjalan di port 5000
- [ ] Login admin berhasil
- [ ] Minimal 3 anggota ditambahkan
- [ ] Minimal 2 user ditambahkan
- [ ] User memberikan penilaian
- [ ] Analisis K-Means berhasil
- [ ] Kandidat ditetapkan
- [ ] Periode voting dibuat
- [ ] User berhasil voting
- [ ] Hasil voting terlihat

---

## 🎉 Selamat!

Sistem K-Means Voting sudah siap digunakan!

**Tips:**
- Backup database secara berkala
- Ganti password admin default
- Instruksikan user untuk ganti password setelah login pertama
- Monitor hasil voting secara real-time
- Export hasil untuk dokumentasi

**Butuh Bantuan?**
- Baca USER_GUIDE.md untuk panduan lengkap
- Cek TROUBLESHOOTING.md jika ada masalah
- Hubungi administrator sistem

---

**Version:** 2.1.0  
**Last Updated:** 24 November 2024

