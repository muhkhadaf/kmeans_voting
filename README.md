# K-Means Voting System

Sistem voting berbasis web dengan analisis clustering menggunakan algoritma K-Means untuk mengelompokkan hasil voting berdasarkan preferensi pengguna.

## 📋 Deskripsi

Aplikasi ini adalah sistem voting online yang dilengkapi dengan fitur analisis clustering menggunakan K-Means algorithm. Sistem ini memungkinkan admin untuk membuat periode voting, mengelola kandidat, dan menganalisis pola voting pengguna.

## 🚀 Fitur Utama

### Untuk Admin
- **Manajemen Anggota**: Tambah, edit, hapus data anggota dengan informasi dasar
- **Manajemen User**: Tambah dan hapus user yang dapat memberikan penilaian dan voting
- **Analisis K-Means**: Clustering otomatis berdasarkan rata-rata penilaian dari user
- **Manajemen Periode Voting**: Membuat, memulai, menghentikan, dan memperpanjang periode voting
- **Dashboard Analytics**: Visualisasi hasil voting dan analisis cluster real-time
- **Hasil Voting**: Monitoring hasil voting per periode dengan statistik lengkap

### Untuk User
- **Penilaian Anggota**: Memberikan penilaian untuk setiap anggota berdasarkan 5 kriteria
- **Voting Kandidat**: Memilih kandidat terbaik dari hasil clustering
- **Ganti Password**: Mengganti password sendiri untuk keamanan akun
- **Riwayat Aktivitas**: Melihat status penilaian dan voting yang telah dilakukan

### Fitur Keamanan
- **Password Hashing**: Semua password di-hash menggunakan Werkzeug Security
- **Session Management**: Session timeout dan secure session handling
- **Role-based Access**: Pemisahan akses admin dan user
- **Cascade Delete**: Penghapusan data terkait secara otomatis untuk integritas database

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Machine Learning**: NumPy untuk implementasi K-Means
- **Timezone**: PyTZ untuk handling timezone Indonesia

## 📦 Instalasi dan Setup

### 1. Clone Repository

```bash
git clone https://github.com/muhkhadaf/kmeans_voting.git
cd kmeans_voting
```

### 2. Install Dependencies

Pastikan Python 3.7+ sudah terinstall, kemudian install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Setup Database

Aplikasi menggunakan MySQL. Pastikan MySQL server sudah berjalan, kemudian:

1. Buat database baru:
```sql
CREATE DATABASE kmeans_voting;
```

2. Update konfigurasi database di `db.py` jika diperlukan:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'database': 'kmeans_voting'
}
```

### 4. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di:
- Local: `http://127.0.0.1:5000`
- Network: `http://[IP_ADDRESS]:5000`

## 🔐 Login Default

### Admin
- **URL**: `http://127.0.0.1:5000/login`
- **Username**: `admin`
- **Password**: `admin123`

### User
- **URL**: `http://127.0.0.1:5000/user_login`
- User harus didaftarkan terlebih dahulu oleh admin

## 📱 Cara Penggunaan

### Untuk Admin

1. **Login** ke sistem menggunakan kredensial admin
2. **Dashboard**: Lihat overview sistem dan statistik
3. **Manajemen Anggota**: 
   - Tambah/edit/hapus anggota/kandidat
   - Kelola data anggota yang akan divoting
4. **Periode Voting**:
   - Buat periode voting baru dengan jadwal mulai dan berakhir
   - Mulai/hentikan periode voting secara manual
   - Monitor status periode voting aktif
5. **Hasil & Analisis**:
   - Lihat hasil voting real-time
   - Analisis clustering K-Means otomatis
   - Export atau print hasil analisis

### Untuk User

1. **Login** menggunakan akun yang sudah didaftarkan admin
2. **Voting**: Pilih kandidat pada periode voting yang aktif
3. **Konfirmasi**: Review pilihan sebelum submit
4. **Selesai**: Sistem akan mengkonfirmasi vote berhasil

## 🔧 Konfigurasi

### Database Configuration (`db.py`)
```python
DB_CONFIG = {
    'host': 'localhost',      # Host database
    'user': 'root',           # Username database
    'password': '',           # Password database
    'database': 'kmeans_voting'  # Nama database
}
```

### Server Configuration (`app.py`)
```python
SERVER_TIMEZONE = pytz.timezone('Asia/Jakarta')  # Timezone server
app.secret_key = 'your-secret-key-here'          # Ganti dengan secret key yang aman
```

## 📊 Struktur Database

Aplikasi akan otomatis membuat tabel-tabel berikut:

- `admin`: Data admin sistem
- `user`: Data user/voter
- `anggota`: Data anggota/kandidat
- `voting_periods`: Periode-periode voting
- `voting`: Record voting dari user

## 🐛 Troubleshooting

### Error Database Connection
```
Error: Can't connect to MySQL server
```
**Solusi**: 
- Pastikan MySQL server berjalan
- Periksa konfigurasi database di `db.py`
- Pastikan database `kmeans_voting` sudah dibuat

### Error Import Module
```
ModuleNotFoundError: No module named 'flask'
```
**Solusi**:
```bash
pip install -r requirements.txt
```

### Error Port Already in Use
```
Address already in use
```
**Solusi**:
- Hentikan aplikasi yang menggunakan port 5000
- Atau ubah port di `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Error Timezone
```
Error: Unknown timezone
```
**Solusi**:
```bash
pip install pytz
```

## 🔄 Development

### Menjalankan dalam Mode Development
```bash
python app.py
```
Mode debug sudah aktif secara default untuk development.

### Struktur Project
```
kmeans_voting/
├── app.py              # Main application file
├── db.py               # Database configuration and functions
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS)
│   ├── css/
│   └── js/
└── templates/         # HTML templates
    ├── base.html
    ├── dashboard.html
    ├── login.html
    ├── voting.html
    └── ...
```

## 📝 API Endpoints

### Admin Routes
- `GET /` - Dashboard admin
- `GET /login` - Halaman login admin
- `POST /login` - Proses login admin
- `GET /anggota` - Manajemen anggota
- `POST /anggota/add` - Tambah anggota
- `GET /voting_periods` - Manajemen periode voting
- `POST /voting_periods/add` - Tambah periode voting
- `GET /hasil` - Hasil dan analisis voting

### User Routes
- `GET /user_login` - Halaman login user
- `POST /user_login` - Proses login user
- `GET /voting` - Halaman voting
- `POST /vote` - Submit vote

## 🤝 Contributing

1. Fork repository
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 License

Project ini menggunakan MIT License. Lihat file `LICENSE` untuk detail lengkap.

## 👥 Author

- **Muhammad Khadafi** - [muhkhadaf](https://github.com/muhkhadaf)

## 📚 Dokumentasi Lengkap

Untuk informasi lebih detail, silakan baca dokumentasi berikut:

- **[QUICKSTART.md](QUICKSTART.md)** - Panduan cepat memulai dalam 5 menit
- **[INSTALLATION.md](INSTALLATION.md)** - Panduan instalasi lengkap step-by-step
- **[USER_GUIDE.md](USER_GUIDE.md)** - Panduan penggunaan untuk admin dan user
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solusi masalah umum dan debugging
- **[CHANGELOG.md](CHANGELOG.md)** - Riwayat perubahan dan update
- **[TEST_FEATURES.md](TEST_FEATURES.md)** - Panduan testing fitur-fitur baru
- **[RELEASE_NOTES_v2.1.0.md](RELEASE_NOTES_v2.1.0.md)** - Release notes versi terbaru

## 🆕 What's New in v2.1.0

### Fitur Baru
- ✨ **Ganti Password untuk User** - User dapat mengganti password sendiri
- ✨ **Hapus User untuk Admin** - Admin dapat menghapus user yang tidak aktif
- 🔒 **Enhanced Security** - Password validation dan safe deletion

### Bug Fixes
- 🐛 Fixed K-Means normalization error (division by zero)
- 🐛 Fixed database foreign key constraint issues
- 🐛 Fixed PyMySQL compatibility for Windows

[Lihat changelog lengkap](CHANGELOG.md)

## 📞 Support

Jika mengalami masalah atau memiliki pertanyaan:

1. **Baca Dokumentasi**: Cek [TROUBLESHOOTING.md](TROUBLESHOOTING.md) untuk solusi masalah umum
2. **Quick Start**: Ikuti [QUICKSTART.md](QUICKSTART.md) untuk setup cepat
3. **User Guide**: Baca [USER_GUIDE.md](USER_GUIDE.md) untuk panduan lengkap
4. **GitHub Issues**: Buka issue di GitHub repository
5. **Contact Admin**: Hubungi administrator sistem

## 🎯 Quick Links

- 📖 [Dokumentasi Lengkap](USER_GUIDE.md)
- 🚀 [Quick Start Guide](QUICKSTART.md)
- 🔧 [Troubleshooting](TROUBLESHOOTING.md)
- 📝 [Changelog](CHANGELOG.md)
- 🧪 [Testing Guide](TEST_FEATURES.md)

---

**Version:** 2.1.0  
**Last Updated:** 24 November 2024  
**Happy Voting! 🗳️**