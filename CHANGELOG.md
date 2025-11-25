# Changelog - K-Means Voting System

## [2.0.0] - Sistem Penilaian Berbasis User

### 🎯 Perubahan Besar

#### Sistem Lama:
- Admin menambahkan anggota dengan nilai kriteria lengkap
- Admin langsung menjalankan analisis K-Means
- User hanya melakukan voting terhadap kandidat

#### Sistem Baru:
- **Admin** menambahkan anggota dengan data dasar (nama, pendidikan, visi misi)
- **User** memberikan penilaian terhadap setiap anggota
- **Admin** menjalankan analisis K-Means berdasarkan rata-rata penilaian user
- **User** melakukan voting terhadap kandidat hasil analisis

### ✨ Fitur Baru

#### 1. Manajemen Anggota (Admin)
- Formulir sederhana: nama, pendidikan (SD-S3), visi & misi
- Tidak lagi memasukkan nilai kriteria secara manual
- Fokus pada data profil anggota

#### 2. Penilaian Anggota (User)
- **Route baru**: `/user_penilaian`
- User dapat menilai semua anggota
- 5 kriteria penilaian (skala 1-100):
  - Keaktifan
  - Kepemimpinan
  - Pengalaman
  - Disiplin
  - Komunikasi (kriteria baru)
- Interface slider untuk kemudahan penilaian
- User dapat mengubah penilaian yang sudah diberikan
- Indikator status: sudah/belum dinilai

#### 3. Analisis K-Means (Admin)
- Menggunakan rata-rata penilaian dari semua user
- Menampilkan jumlah penilai untuk setiap anggota
- Hasil lebih objektif karena berbasis penilaian kolektif
- Clustering tetap 3 kelompok:
  - Sangat Layak
  - Cukup Layak
  - Kurang Layak

#### 4. Voting (User)
- Menampilkan kandidat dengan rata-rata penilaian
- User dapat melihat visi & misi kandidat
- Menampilkan jumlah penilai untuk transparansi
- Skor rata-rata dari 5 kriteria

### 🗄️ Perubahan Database

#### Tabel `anggota` (Diubah)
```sql
-- Struktur Lama
id, nama, keaktifan, kepemimpinan, pengalaman, disiplin, pendidikan, usia, cluster, status

-- Struktur Baru
id, nama, pendidikan (ENUM), visi_misi (TEXT), cluster, status, created_at
```

#### Tabel `penilaian` (Baru)
```sql
CREATE TABLE penilaian (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    anggota_id INT NOT NULL,
    keaktifan INT NOT NULL (1-100),
    kepemimpinan INT NOT NULL (1-100),
    pengalaman INT NOT NULL (1-100),
    disiplin INT NOT NULL (1-100),
    komunikasi INT NOT NULL (1-100),
    created_at TIMESTAMP,
    UNIQUE KEY (user_id, anggota_id)
)
```

### 🔄 Migrasi Database

File `migrate_db.py` disediakan untuk migrasi otomatis:

```bash
python migrate_db.py
```

**Catatan Penting:**
- Data lama akan di-backup ke tabel `anggota_backup`
- Anggota harus ditambahkan ulang dengan format baru
- User perlu memberikan penilaian untuk semua anggota

### 📝 Perubahan Route

#### Route Baru:
- `GET /user_penilaian` - Halaman penilaian anggota
- `POST /submit_penilaian` - Submit penilaian anggota

#### Route Dimodifikasi:
- `POST /anggota/add` - Formulir sederhana (nama, pendidikan, visi misi)
- `POST /anggota/edit/<id>` - Edit data dasar anggota
- `POST /run_kmeans` - Analisis berdasarkan rata-rata penilaian user
- `GET /hasil_analisis` - Menampilkan hasil dengan data penilaian
- `GET /user_vote` - Menampilkan kandidat dengan penilaian

### 🎨 Perubahan Template

#### Template Baru:
- `templates/user_penilaian.html` - Interface penilaian anggota

#### Template Dimodifikasi:
- `templates/anggota.html` - Formulir sederhana untuk admin
- `templates/hasil_analisis.html` - Menampilkan rata-rata penilaian
- `templates/user_voting.html` - Menampilkan visi misi dan penilaian

### 🔧 Cara Penggunaan Baru

#### Untuk Admin:

1. **Tambah Anggota**
   - Login sebagai admin
   - Menu "Data Anggota"
   - Klik "Tambah Anggota"
   - Isi: Nama, Pendidikan, Visi & Misi
   - Simpan

2. **Tunggu Penilaian User**
   - Instruksikan user untuk login dan memberikan penilaian
   - Monitor jumlah penilaian yang masuk

3. **Jalankan Analisis**
   - Menu "Analisis K-Means"
   - Klik "Jalankan Analisis K-Means"
   - Sistem akan menggunakan rata-rata penilaian dari user
   - Minimal 3 anggota dengan penilaian

4. **Tetapkan Kandidat**
   - Pilih anggota dari hasil clustering
   - Klik "Tetapkan Kandidat"

5. **Buat Periode Voting**
   - Menu "Periode Voting"
   - Buat periode baru dengan jadwal
   - Mulai periode voting

#### Untuk User:

1. **Login**
   - Akses `/user_login`
   - Masukkan username dan password

2. **Berikan Penilaian**
   - Otomatis diarahkan ke halaman penilaian
   - Klik "Beri Penilaian" pada setiap anggota
   - Geser slider untuk memberikan nilai (1-100)
   - Simpan penilaian

3. **Voting**
   - Klik menu "Voting" di header
   - Pilih kandidat saat periode voting aktif
   - Konfirmasi pilihan

### ⚠️ Breaking Changes

1. **Struktur Database Berubah Total**
   - Tabel `anggota` memiliki struktur berbeda
   - Data lama tidak kompatibel dengan sistem baru
   - Perlu migrasi dan input ulang data

2. **Flow Aplikasi Berubah**
   - Admin tidak lagi input nilai kriteria
   - User harus memberikan penilaian sebelum analisis
   - Analisis memerlukan minimal 3 anggota dengan penilaian

3. **Template Berubah**
   - Formulir anggota lebih sederhana
   - Tampilan hasil analisis berbeda
   - Tampilan voting menampilkan data berbeda

### 🐛 Bug Fixes

- Fixed: Analisis K-Means sekarang menggunakan data yang lebih objektif
- Fixed: User experience lebih baik dengan pemisahan penilaian dan voting
- Fixed: Admin tidak perlu menebak nilai kriteria anggota

### 📚 Dokumentasi

- Ditambahkan `CHANGELOG.md` untuk tracking perubahan
- Ditambahkan `migrate_db.py` untuk migrasi database
- Updated README dengan informasi sistem baru

### 🔮 Rencana Kedepan

- [ ] Dashboard statistik penilaian
- [ ] Export hasil penilaian ke Excel/PDF
- [ ] Notifikasi email untuk user yang belum memberikan penilaian
- [ ] Grafik visualisasi penilaian per kriteria
- [ ] Sistem komentar untuk penilaian

---

## [2.1.0] - 2024-11-24

### ✨ Fitur Baru

#### 1. Ganti Password untuk User
- **Route baru**: `GET/POST /user_change_password`
- User dapat mengganti password sendiri tanpa bantuan admin
- Validasi password lama sebelum mengubah
- Password baru minimal 6 karakter
- Konfirmasi password untuk menghindari kesalahan input
- Tips keamanan password di halaman ganti password

**Fitur:**
- Form ganti password dengan validasi client-side dan server-side
- Verifikasi password lama menggunakan hash
- Link "Ganti Password" di semua halaman user (penilaian, voting, vote success)
- Pesan sukses/error yang jelas

#### 2. Hapus User untuk Admin
- **Route baru**: `GET /user/delete/<id>`
- Admin dapat menghapus user dari halaman "Voting & User"
- Tombol hapus dengan ikon trash di setiap user
- Konfirmasi sebelum menghapus dengan peringatan
- Cascade delete: menghapus user akan otomatis menghapus penilaian dan voting terkait

**Fitur:**
- Tombol hapus dengan hover effect
- Konfirmasi dialog dengan nama user dan peringatan
- Flash message sukses dengan nama user yang dihapus
- UI yang konsisten dengan desain sistem

### 🎨 Perubahan UI

#### Template yang Dimodifikasi:
- `templates/user_penilaian.html` - Tambah link "Ganti Password"
- `templates/user_voting.html` - Tambah link "Ganti Password" dan "Penilaian"
- `templates/vote_success.html` - Tambah link "Ganti Password" dan "Penilaian"
- `templates/user_login.html` - Update informasi tentang fitur ganti password
- `templates/voting.html` - Tambah tombol hapus user

#### Template Baru:
- `templates/user_change_password.html` - Halaman ganti password untuk user

### 🛠️ Utilitas Command Line

#### 1. Script Tambah Admin (`add_admin.py`)
- Script Python untuk menambahkan admin baru via terminal
- Input username dan password dengan validasi
- Hidden password input menggunakan `getpass`
- Validasi username tidak duplikat
- Validasi password minimal 6 karakter
- Menampilkan daftar admin yang ada
- Konfirmasi sebelum menyimpan

#### 2. Script Kelola Admin (`manage_admin.py`)
- Menu interaktif untuk kelola admin
- Fitur: lihat daftar, tambah, hapus, ganti password
- Safety feature: tidak bisa hapus admin terakhir
- Verifikasi password lama untuk ganti password
- User-friendly dengan emoji dan formatting

**Cara Menggunakan:**
```bash
# Tambah admin baru
python add_admin.py

# Kelola admin (menu lengkap)
python manage_admin.py
```

### 📝 Perubahan Dokumentasi

#### USER_GUIDE.md
- Tambah section "Mengganti Password" untuk user
- Tambah section "Menghapus User" untuk admin
- Tambah section "Utilitas Command Line" untuk kelola admin
- Update FAQ dengan pertanyaan tentang kelola admin
- Tips keamanan password

#### ADMIN_SCRIPTS.md (Baru)
- Dokumentasi lengkap untuk skrip admin
- Panduan troubleshooting
- Best practices
- Contoh output dan workflow

### 🔒 Keamanan

- Password di-hash menggunakan `werkzeug.security`
- Validasi password lama sebelum mengubah
- Minimal panjang password 6 karakter
- Session tetap aktif setelah ganti password

### 🐛 Bug Fixes

- Fixed: User sekarang dapat mengelola password sendiri
- Fixed: Admin dapat menghapus user yang tidak aktif
- Fixed: Cascade delete mencegah orphaned data
- Fixed: K-Means normalisasi error saat semua nilai sama (division by zero)
- Fixed: Urutan pembuatan tabel database untuk foreign key constraint
- Fixed: PyMySQL compatibility untuk Windows (pengganti MySQLdb)

### ⚠️ Catatan Penting

**Menghapus User:**
- Menghapus user akan menghapus semua penilaian yang telah diberikan
- Menghapus user akan menghapus voting yang telah dilakukan
- Hal ini dapat mempengaruhi hasil analisis K-Means dan hasil voting
- Rekomendasi: Jangan hapus user setelah periode penilaian atau voting dimulai

**Ganti Password:**
- User tetap login setelah mengganti password
- Password baru akan digunakan untuk login berikutnya
- Jika lupa password baru, hubungi admin untuk reset

---

## [1.0.0] - Rilis Awal

### Fitur Awal
- Sistem login admin dan user
- Manajemen anggota dengan nilai kriteria
- Analisis K-Means clustering
- Sistem voting dengan periode
- Dashboard dan laporan hasil
