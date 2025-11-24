# Panduan Penggunaan - K-Means Voting System v2.0

## 📖 Daftar Isi

1. [Untuk Admin](#untuk-admin)
2. [Untuk User](#untuk-user)
3. [Alur Kerja Sistem](#alur-kerja-sistem)
4. [FAQ](#faq)

---

## 👨‍💼 Untuk Admin

### 1. Login Admin

1. Buka browser dan akses: `http://127.0.0.1:5000/login`
2. Masukkan kredensial admin:
   - Username: `admin`
   - Password: `admin123` (ganti setelah login pertama)
3. Klik "Masuk"

### 2. Dashboard

Setelah login, Anda akan melihat dashboard dengan statistik:
- Total Anggota
- Total Kandidat
- Total User
- Total Votes

### 3. Manajemen Anggota

#### Menambah Anggota Baru

1. Klik menu **"Data Anggota"**
2. Klik tombol **"Tambah Anggota"**
3. Isi formulir:
   - **Nama Lengkap**: Nama anggota
   - **Pendidikan**: Pilih dari dropdown (SD, SMP, SMA, D3, S1, S2, S3)
   - **Visi & Misi**: Tuliskan visi dan misi anggota (opsional)
4. Klik **"Simpan"**

#### Mengedit Anggota

1. Di halaman Data Anggota, klik ikon **pensil (edit)** pada anggota yang ingin diedit
2. Ubah data yang diperlukan
3. Klik **"Update"**

#### Menghapus Anggota

1. Klik ikon **tempat sampah (delete)** pada anggota yang ingin dihapus
2. Konfirmasi penghapusan
3. **Perhatian**: Menghapus anggota akan menghapus semua penilaian terkait

### 4. Manajemen User

#### Menambah User Baru

1. Klik menu **"Voting & User"**
2. Scroll ke bagian **"User Terdaftar"**
3. Klik tombol **"Tambah User"** (hijau, pojok kanan atas)
4. Isi formulir:
   - **Nama Lengkap**: Nama lengkap user
   - **Username**: Username untuk login (unik)
   - **Password**: Password untuk login
5. Klik **"Tambah User"**

**Tips**: Berikan username dan password yang mudah diingat user

#### Menghapus User

1. Di halaman **"Voting & User"**, lihat bagian **"User Terdaftar"**
2. Klik ikon **tempat sampah (delete)** pada user yang ingin dihapus
3. Konfirmasi penghapusan
4. **Perhatian**: Menghapus user akan menghapus semua penilaian dan voting yang telah dilakukan user tersebut

**Kapan Menghapus User:**
- User sudah tidak aktif atau keluar dari organisasi
- User duplikat atau salah input
- Sebelum periode voting dimulai (untuk menghindari kehilangan data voting)

**Rekomendasi**: Jangan hapus user setelah mereka melakukan penilaian atau voting, karena akan mempengaruhi hasil analisis dan voting

### 5. Menunggu Penilaian dari User

Setelah anggota ditambahkan:

1. Instruksikan semua user untuk login
2. User akan otomatis diarahkan ke halaman penilaian
3. Minta user memberikan penilaian untuk setiap anggota
4. Monitor jumlah penilaian yang masuk

**Catatan**: Minimal 3 anggota harus memiliki penilaian sebelum analisis dapat dijalankan

### 6. Analisis K-Means

#### Menjalankan Analisis

1. Klik menu **"Analisis K-Means"**
2. Pastikan minimal 3 anggota sudah memiliki penilaian
3. Klik tombol **"Jalankan Analisis K-Means"**
4. Sistem akan memproses dan mengelompokkan anggota menjadi 3 cluster:
   - **Sangat Layak** (cluster dengan skor tertinggi)
   - **Cukup Layak** (cluster dengan skor menengah)
   - **Kurang Layak** (cluster dengan skor terendah)

#### Melihat Hasil Analisis

Setelah analisis selesai, Anda akan melihat:
- Ringkasan setiap cluster (jumlah anggota, rata-rata skor)
- Daftar anggota per cluster dengan detail penilaian:
  - Nama dan pendidikan
  - Rata-rata nilai per kriteria (Keaktifan, Kepemimpinan, dll)
  - Jumlah penilai
  - Skor rata-rata keseluruhan
- Visualisasi grafik distribusi cluster

### 7. Menetapkan Kandidat

1. Di halaman **"Hasil Analisis"**
2. Centang checkbox pada anggota yang ingin dijadikan kandidat
   - **Rekomendasi**: Pilih dari cluster "Sangat Layak"
   - Anda dapat memilih dari cluster mana saja
3. Lihat jumlah kandidat terpilih di bagian bawah
4. Klik tombol **"Tetapkan Kandidat"**
5. Kandidat siap untuk periode voting

**Tips**: 
- Pilih 3-5 kandidat untuk hasil voting yang optimal
- Pertimbangkan keseimbangan dari berbagai cluster jika diperlukan

### 8. Membuat Periode Voting

#### Membuat Periode Baru

1. Klik menu **"Periode Voting"**
2. Klik tombol **"Buat Periode Baru"**
3. Isi formulir:
   - **Nama Periode**: Contoh: "Pemilihan Ketua 2024"
   - **Deskripsi**: Keterangan periode voting
   - **Waktu Mulai**: Tanggal dan jam mulai voting
   - **Waktu Berakhir**: Tanggal dan jam berakhir voting
4. Klik **"Buat Periode"**

**Catatan**: 
- Waktu mulai tidak boleh lebih dari 1 menit yang lalu
- Waktu berakhir harus setelah waktu mulai
- Tidak boleh ada periode yang bertabrakan

#### Memulai Periode Voting

Jika periode dibuat dengan waktu mulai di masa depan:
1. Tunggu hingga waktu mulai tiba (otomatis), atau
2. Klik tombol **"Mulai Sekarang"** untuk memulai manual

#### Menghentikan Periode Voting

Untuk menghentikan periode sebelum waktunya:
1. Klik tombol **"Hentikan Voting"**
2. Konfirmasi penghentian
3. Periode akan berakhir dan user tidak dapat voting lagi

#### Memperpanjang Periode Voting

Jika perlu memperpanjang waktu:
1. Klik tombol **"Perpanjang"**
2. Pilih durasi perpanjangan (dalam jam)
3. Konfirmasi perpanjangan

### 9. Melihat Hasil Voting

#### Hasil Real-time

1. Klik menu **"Hasil Voting"**
2. Pilih periode voting dari dropdown (jika ada multiple periode)
3. Lihat:
   - Jumlah total suara
   - Persentase partisipasi (total votes / total users)
   - Ranking kandidat berdasarkan jumlah suara
   - Detail penilaian setiap kandidat

#### Filter Hasil

- Gunakan dropdown **"Pilih Periode"** untuk melihat hasil periode tertentu
- Hasil akan otomatis update saat periode dipilih

### 10. Logout

Klik tombol **"Logout"** di pojok kanan atas untuk keluar dari sistem

---

## 👥 Untuk User

### 1. Login User

1. Buka browser dan akses: `http://127.0.0.1:5000/user_login`
2. Masukkan kredensial yang diberikan admin:
   - Username: (diberikan oleh admin)
   - Password: (diberikan oleh admin)
3. Klik **"Masuk untuk Voting"**

### 2. Memberikan Penilaian Anggota

Setelah login, Anda akan diarahkan ke halaman **Penilaian Anggota**.

#### Cara Memberikan Penilaian

1. Lihat daftar semua anggota
2. Untuk setiap anggota:
   - Klik tombol **"Beri Penilaian"** atau **"Edit Penilaian"** (jika sudah dinilai)
   - Modal penilaian akan muncul menampilkan:
     - Nama dan pendidikan anggota
     - Visi & Misi (jika ada)
   - Geser slider untuk memberikan nilai (1-100) pada 5 kriteria:
     - **Keaktifan**: Seberapa aktif dalam kegiatan organisasi
     - **Kepemimpinan**: Kemampuan memimpin dan mengambil keputusan
     - **Pengalaman**: Pengalaman organisasi dan kepanitiaan
     - **Disiplin**: Kedisiplinan dan tanggung jawab
     - **Komunikasi**: Kemampuan berkomunikasi dan bersosialisasi
   - Klik **"Simpan Penilaian"**

#### Tips Memberikan Penilaian

- **Objektif**: Berikan penilaian berdasarkan pengamatan nyata
- **Adil**: Jangan terpengaruh hubungan personal
- **Konsisten**: Gunakan standar yang sama untuk semua anggota
- **Lengkap**: Usahakan menilai semua anggota

**Skala Penilaian**:
- 1-20: Sangat Kurang
- 21-40: Kurang
- 41-60: Cukup
- 61-80: Baik
- 81-100: Sangat Baik

#### Mengubah Penilaian

Anda dapat mengubah penilaian kapan saja:
1. Klik **"Edit Penilaian"** pada anggota yang sudah dinilai
2. Ubah nilai yang diinginkan
3. Klik **"Simpan Penilaian"**

### 3. Melakukan Voting

Setelah admin menetapkan kandidat dan memulai periode voting:

#### Cara Voting

1. Klik menu **"Voting"** di header
2. Lihat status periode voting:
   - **Aktif**: Voting sedang berlangsung (ada countdown timer)
   - **Belum Dimulai**: Voting belum dibuka
   - **Berakhir**: Voting sudah ditutup
3. Jika voting aktif, Anda akan melihat daftar kandidat dengan:
   - Nama dan pendidikan
   - Visi & Misi
   - Rata-rata penilaian per kriteria
   - Skor rata-rata keseluruhan
   - Jumlah penilai
4. Klik tombol **"Pilih Kandidat"** pada kandidat pilihan Anda
5. Modal konfirmasi akan muncul
6. **Perhatian**: Keputusan tidak dapat diubah setelah dikonfirmasi!
7. Klik **"Konfirmasi Vote"**

#### Setelah Voting

- Anda akan diarahkan ke halaman sukses
- Anda tidak dapat voting lagi pada periode yang sama
- Hasil akan diumumkan setelah periode berakhir

### 4. Mengganti Password

Untuk keamanan akun, Anda dapat mengganti password:

#### Cara Ganti Password

1. Klik menu **"Ganti Password"** di header (ikon kunci)
2. Isi formulir:
   - **Password Lama**: Masukkan password saat ini
   - **Password Baru**: Masukkan password baru (minimal 6 karakter)
   - **Konfirmasi Password Baru**: Masukkan ulang password baru
3. Klik **"Simpan Password Baru"**

#### Tips Password Aman

- Gunakan kombinasi huruf besar dan kecil
- Tambahkan angka dan simbol
- Jangan gunakan password yang mudah ditebak (tanggal lahir, nama, dll)
- Jangan bagikan password kepada siapapun
- Ganti password secara berkala

**Catatan**: 
- Setelah password diubah, Anda tetap login dengan sesi saat ini
- Gunakan password baru untuk login berikutnya
- Jika lupa password baru, hubungi admin untuk reset

### 5. Logout

Klik tombol **"Keluar"** di pojok kanan atas untuk logout

---

## 🔄 Alur Kerja Sistem

### Alur Lengkap dari Awal hingga Akhir

```
1. ADMIN: Login
   ↓
2. ADMIN: Tambah Anggota (nama, pendidikan, visi misi)
   ↓
3. ADMIN: Tambah User
   ↓
4. USER: Login
   ↓
5. USER: Beri Penilaian untuk semua anggota
   ↓
6. ADMIN: Jalankan Analisis K-Means
   ↓
7. ADMIN: Lihat Hasil Clustering
   ↓
8. ADMIN: Tetapkan Kandidat dari hasil clustering
   ↓
9. ADMIN: Buat Periode Voting
   ↓
10. ADMIN: Mulai Periode Voting
    ↓
11. USER: Login dan Voting
    ↓
12. ADMIN: Monitor hasil voting real-time
    ↓
13. ADMIN: Periode berakhir (otomatis/manual)
    ↓
14. ADMIN: Lihat hasil akhir dan pemenang
```

### Timeline Rekomendasi

**Minggu 1-2**: Persiapan
- Admin menambahkan semua anggota
- Admin menambahkan semua user
- Sosialisasi sistem kepada user

**Minggu 3**: Penilaian
- User login dan memberikan penilaian
- Admin monitor progress penilaian
- Reminder untuk user yang belum menilai

**Minggu 4**: Analisis
- Admin jalankan analisis K-Means
- Review hasil clustering
- Tetapkan kandidat

**Minggu 5**: Voting
- Buat dan mulai periode voting
- User melakukan voting
- Monitor partisipasi

**Minggu 6**: Hasil
- Periode voting berakhir
- Pengumuman hasil
- Dokumentasi

---

## ❓ FAQ (Frequently Asked Questions)

### Untuk Admin

**Q: Berapa minimal anggota yang harus ada?**
A: Minimal 3 anggota dengan penilaian untuk menjalankan analisis K-Means.

**Q: Berapa minimal user yang harus menilai?**
A: Tidak ada minimal, tapi semakin banyak user yang menilai, hasil akan semakin objektif. Rekomendasi minimal 5 user.

**Q: Apakah bisa mengubah data anggota setelah ada penilaian?**
A: Ya, tapi hanya data profil (nama, pendidikan, visi misi). Penilaian dari user tidak terpengaruh.

**Q: Apakah bisa menjalankan analisis K-Means berkali-kali?**
A: Ya, Anda dapat menjalankan analisis ulang jika ada penilaian baru. Hasil clustering akan diupdate.

**Q: Bagaimana jika ada periode voting yang bertabrakan?**
A: Sistem tidak mengizinkan periode yang bertabrakan. Anda harus mengubah jadwal salah satu periode.

**Q: Apakah bisa melihat siapa yang voting kandidat tertentu?**
A: Tidak, sistem menjaga kerahasiaan voting. Admin hanya bisa melihat jumlah total suara per kandidat.

**Q: Bagaimana cara mengganti password admin?**
A: Saat ini harus dilakukan manual di database. Fitur change password akan ditambahkan di versi mendatang.

### Untuk User

**Q: Apakah harus menilai semua anggota?**
A: Tidak wajib, tapi sangat disarankan untuk menilai semua anggota agar hasil analisis lebih akurat.

**Q: Apakah bisa mengubah penilaian setelah disimpan?**
A: Ya, Anda dapat mengubah penilaian kapan saja sebelum admin menjalankan analisis.

**Q: Apakah penilaian saya dilihat orang lain?**
A: Tidak, penilaian individual bersifat rahasia. Yang ditampilkan hanya rata-rata dari semua penilai.

**Q: Apakah bisa voting lebih dari satu kandidat?**
A: Tidak, setiap user hanya dapat memilih satu kandidat per periode voting.

**Q: Apakah bisa mengubah pilihan voting?**
A: Tidak, setelah dikonfirmasi, pilihan tidak dapat diubah. Pastikan pilihan Anda sudah tepat sebelum konfirmasi.

**Q: Bagaimana cara mengganti password?**
A: Setelah login, klik menu "Ganti Password" di header, lalu ikuti petunjuk untuk mengubah password Anda.

**Q: Bagaimana jika lupa password?**
A: Hubungi admin untuk reset password. Setelah login dengan password baru dari admin, segera ganti password Anda sendiri.

**Q: Apakah bisa melihat hasil voting sebelum periode berakhir?**
A: Tidak, hasil hanya dapat dilihat oleh admin. User akan melihat hasil setelah periode berakhir dan admin mengumumkan.

### Teknis

**Q: Bagaimana cara backup data?**
A: Backup database MySQL secara berkala menggunakan mysqldump:
```bash
mysqldump -u root -p kmeans_voting > backup.sql
```

**Q: Bagaimana cara restore data?**
A: Restore dari backup:
```bash
mysql -u root -p kmeans_voting < backup.sql
```

**Q: Apakah sistem bisa diakses dari jaringan lain?**
A: Ya, ganti `host='0.0.0.0'` di app.py dan akses menggunakan IP server.

**Q: Bagaimana cara menambah kriteria penilaian?**
A: Perlu modifikasi kode di app.py dan database schema. Hubungi developer.

---

## 📞 Bantuan Lebih Lanjut

Jika mengalami masalah atau memiliki pertanyaan:

1. Baca dokumentasi lengkap di README.md
2. Periksa INSTALLATION.md untuk masalah instalasi
3. Lihat CHANGELOG.md untuk informasi perubahan
4. Hubungi administrator sistem

---

**Terima kasih telah menggunakan K-Means Voting System! 🗳️**
