# Release Notes - K-Means Voting System v2.1.0

**Release Date:** 24 November 2024

## 🎉 Apa yang Baru?

### 1. 🔐 Ganti Password untuk User

User sekarang dapat mengganti password mereka sendiri tanpa perlu bantuan admin!

**Fitur:**
- Form ganti password yang mudah digunakan
- Validasi password lama untuk keamanan
- Password baru minimal 6 karakter
- Konfirmasi password untuk menghindari kesalahan
- Tips keamanan password
- Link "Ganti Password" di semua halaman user

**Cara Menggunakan:**
1. Login sebagai user
2. Klik "Ganti Password" di header
3. Masukkan password lama, password baru, dan konfirmasi
4. Klik "Simpan Password Baru"

### 2. 🗑️ Hapus User untuk Admin

Admin sekarang dapat menghapus user yang tidak aktif atau tidak diperlukan lagi.

**Fitur:**
- Tombol hapus di setiap user di halaman "Voting & User"
- Konfirmasi sebelum menghapus dengan peringatan jelas
- Cascade delete: penilaian dan voting user ikut terhapus
- Flash message dengan nama user yang dihapus

**Cara Menggunakan:**
1. Login sebagai admin
2. Buka halaman "Voting & User"
3. Klik ikon trash pada user yang ingin dihapus
4. Konfirmasi penghapusan

**⚠️ Perhatian:** Menghapus user akan menghapus semua penilaian dan voting yang telah dilakukan user tersebut. Hal ini dapat mempengaruhi hasil analisis dan voting.

## 🔧 Perubahan Teknis

### Route Baru:
- `GET/POST /user_change_password` - Halaman ganti password untuk user
- `GET /user/delete/<id>` - Hapus user oleh admin

### Template Baru:
- `templates/user_change_password.html` - Form ganti password

### Template yang Dimodifikasi:
- `templates/user_penilaian.html` - Tambah link ganti password
- `templates/user_voting.html` - Tambah link ganti password dan penilaian
- `templates/vote_success.html` - Tambah link ganti password dan penilaian
- `templates/user_login.html` - Update informasi
- `templates/voting.html` - Tambah tombol hapus user

### Dokumentasi:
- `USER_GUIDE.md` - Update dengan panduan fitur baru
- `CHANGELOG.md` - Dokumentasi perubahan lengkap
- `TEST_FEATURES.md` - Panduan testing fitur baru
- `RELEASE_NOTES_v2.1.0.md` - Release notes ini

## 🔒 Keamanan

- Password di-hash menggunakan `werkzeug.security`
- Validasi password lama sebelum mengubah
- Minimal panjang password 6 karakter
- Session tetap aktif setelah ganti password
- Cascade delete mencegah orphaned data

## 📋 Upgrade Guide

### Untuk Admin:

1. **Update Kode:**
   ```bash
   git pull origin main
   # atau download versi terbaru
   ```

2. **Tidak Ada Perubahan Database:**
   - Tidak perlu migrasi database
   - Sistem langsung bisa digunakan

3. **Restart Server:**
   ```bash
   python app.py
   ```

4. **Informasikan User:**
   - Beritahu user tentang fitur ganti password
   - Anjurkan user untuk mengganti password default

### Untuk User:

1. **Login seperti biasa**
2. **Ganti password Anda:**
   - Klik "Ganti Password" di header
   - Ikuti petunjuk untuk mengganti password
3. **Gunakan password baru untuk login berikutnya**

## 🐛 Bug Fixes

- Fixed: User sekarang dapat mengelola password sendiri
- Fixed: Admin dapat menghapus user yang tidak aktif
- Fixed: Cascade delete mencegah orphaned data di database

## 📚 Dokumentasi

Dokumentasi lengkap tersedia di:
- `README.md` - Panduan instalasi dan overview
- `USER_GUIDE.md` - Panduan penggunaan lengkap
- `INSTALLATION.md` - Panduan instalasi detail
- `CHANGELOG.md` - Riwayat perubahan
- `TEST_FEATURES.md` - Panduan testing

## 🔮 Rencana Kedepan (v2.2.0)

- Dashboard statistik penilaian
- Export hasil ke Excel/PDF
- Notifikasi email
- Grafik visualisasi penilaian
- Fitur ganti password untuk admin
- Bulk import user dari CSV

## 💬 Feedback & Support

Jika menemukan bug atau memiliki saran:
1. Baca dokumentasi di `USER_GUIDE.md`
2. Cek `TEST_FEATURES.md` untuk panduan testing
3. Hubungi administrator sistem

## 🙏 Terima Kasih

Terima kasih telah menggunakan K-Means Voting System!

---

**Version:** 2.1.0  
**Release Date:** 24 November 2024  
**Compatibility:** Python 3.7+, MySQL 5.7+  
**License:** MIT

