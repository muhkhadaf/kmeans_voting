# Testing Guide - Fitur Baru v2.1.0

## 🧪 Panduan Testing Fitur Baru

### 1. Testing Fitur Ganti Password (User)

#### Persiapan:
1. Pastikan ada minimal 1 user di database
2. Login sebagai user

#### Test Case 1: Ganti Password Berhasil
**Steps:**
1. Login sebagai user
2. Klik link "Ganti Password" di header
3. Isi form:
   - Password Lama: (password saat ini)
   - Password Baru: `newpass123`
   - Konfirmasi Password: `newpass123`
4. Klik "Simpan Password Baru"

**Expected Result:**
- ✅ Muncul pesan sukses "Password berhasil diubah!"
- ✅ Redirect ke halaman penilaian
- ✅ User tetap login
- ✅ Logout dan login lagi dengan password baru berhasil

#### Test Case 2: Password Lama Salah
**Steps:**
1. Klik "Ganti Password"
2. Isi password lama dengan password yang salah
3. Isi password baru dan konfirmasi
4. Submit form

**Expected Result:**
- ❌ Muncul pesan error "Password lama salah!"
- ❌ Password tidak berubah
- ✅ Form tetap di halaman ganti password

#### Test Case 3: Password Baru Tidak Cocok
**Steps:**
1. Klik "Ganti Password"
2. Isi password lama dengan benar
3. Password Baru: `newpass123`
4. Konfirmasi Password: `newpass456` (berbeda)
5. Submit form

**Expected Result:**
- ❌ Muncul pesan error "Password baru dan konfirmasi tidak cocok!"
- ❌ Password tidak berubah

#### Test Case 4: Password Terlalu Pendek
**Steps:**
1. Klik "Ganti Password"
2. Isi password lama dengan benar
3. Password Baru: `123` (kurang dari 6 karakter)
4. Konfirmasi Password: `123`
5. Submit form

**Expected Result:**
- ❌ Muncul pesan error "Password baru minimal 6 karakter!"
- ❌ Password tidak berubah

#### Test Case 5: Validasi Client-Side
**Steps:**
1. Klik "Ganti Password"
2. Isi password baru dan konfirmasi dengan nilai berbeda
3. Submit form

**Expected Result:**
- ❌ Alert JavaScript: "Password baru dan konfirmasi tidak cocok!"
- ❌ Form tidak di-submit

---

### 2. Testing Fitur Hapus User (Admin)

#### Persiapan:
1. Login sebagai admin
2. Pastikan ada minimal 2 user di database
3. Buka halaman "Voting & User"

#### Test Case 1: Hapus User Berhasil
**Steps:**
1. Di bagian "User Terdaftar", pilih user yang akan dihapus
2. Klik ikon trash (tempat sampah) pada user tersebut
3. Konfirmasi dialog yang muncul

**Expected Result:**
- ✅ Muncul dialog konfirmasi dengan nama user dan peringatan
- ✅ Setelah konfirmasi, user terhapus dari daftar
- ✅ Muncul pesan sukses "User '[nama]' berhasil dihapus!"
- ✅ Halaman refresh dan user tidak ada di daftar

#### Test Case 2: Cascade Delete - Penilaian Terhapus
**Steps:**
1. Pastikan user yang akan dihapus sudah memberikan penilaian
2. Catat jumlah penilaian di halaman "Analisis K-Means"
3. Hapus user tersebut
4. Cek kembali halaman "Analisis K-Means"

**Expected Result:**
- ✅ Jumlah penilaian berkurang
- ✅ Rata-rata penilaian anggota berubah (jika ada)
- ✅ Tidak ada error orphaned data

#### Test Case 3: Cascade Delete - Voting Terhapus
**Steps:**
1. Pastikan user yang akan dihapus sudah melakukan voting
2. Catat jumlah vote di halaman "Hasil Voting"
3. Hapus user tersebut
4. Cek kembali halaman "Hasil Voting"

**Expected Result:**
- ✅ Jumlah vote berkurang
- ✅ Persentase voting berubah
- ✅ Tidak ada error orphaned data

#### Test Case 4: Batal Hapus User
**Steps:**
1. Klik ikon trash pada user
2. Klik "Cancel" atau "Batal" pada dialog konfirmasi

**Expected Result:**
- ✅ User tidak terhapus
- ✅ Tetap ada di daftar
- ✅ Tidak ada perubahan data

#### Test Case 5: Hapus User yang Tidak Ada
**Steps:**
1. Akses URL langsung: `/user/delete/99999` (ID yang tidak ada)

**Expected Result:**
- ❌ Muncul pesan error "User tidak ditemukan!"
- ✅ Redirect ke halaman voting

---

### 3. Testing Integrasi

#### Test Case 1: User Ganti Password Lalu Login Ulang
**Steps:**
1. Login sebagai user
2. Ganti password
3. Logout
4. Login dengan password lama

**Expected Result:**
- ❌ Login gagal dengan password lama
- ✅ Login berhasil dengan password baru

#### Test Case 2: Admin Hapus User yang Sedang Login
**Steps:**
1. Login sebagai user di browser 1
2. Login sebagai admin di browser 2
3. Admin hapus user yang sedang login
4. User coba akses halaman lain di browser 1

**Expected Result:**
- ✅ User masih bisa akses dengan session yang ada
- ✅ Setelah logout, user tidak bisa login lagi

#### Test Case 3: Link Navigasi Ganti Password
**Steps:**
1. Login sebagai user
2. Cek link "Ganti Password" di:
   - Halaman Penilaian
   - Halaman Voting
   - Halaman Vote Success

**Expected Result:**
- ✅ Link "Ganti Password" muncul di semua halaman
- ✅ Klik link mengarah ke `/user_change_password`
- ✅ Icon key (🔑) muncul di sebelah link

---

### 4. Testing UI/UX

#### Test Case 1: Responsiveness Ganti Password
**Steps:**
1. Buka halaman ganti password
2. Resize browser ke ukuran mobile (375px)
3. Resize ke tablet (768px)
4. Resize ke desktop (1920px)

**Expected Result:**
- ✅ Form tetap readable di semua ukuran
- ✅ Button tidak overlap
- ✅ Padding dan margin sesuai

#### Test Case 2: Hover Effect Tombol Hapus
**Steps:**
1. Login sebagai admin
2. Buka halaman "Voting & User"
3. Hover mouse di atas tombol trash

**Expected Result:**
- ✅ Warna berubah ke merah lebih gelap
- ✅ Background berubah ke merah muda
- ✅ Cursor berubah jadi pointer
- ✅ Tooltip "Hapus User" muncul

#### Test Case 3: Flash Messages
**Steps:**
1. Test berbagai aksi yang menghasilkan flash message
2. Perhatikan styling dan posisi

**Expected Result:**
- ✅ Success message: hijau dengan icon check
- ✅ Error message: merah dengan icon exclamation
- ✅ Message muncul di atas konten
- ✅ Message readable dan jelas

---

### 5. Testing Keamanan

#### Test Case 1: Akses Ganti Password Tanpa Login
**Steps:**
1. Logout dari sistem
2. Akses URL: `/user_change_password`

**Expected Result:**
- ❌ Tidak bisa akses halaman
- ✅ Redirect ke `/user_login`

#### Test Case 2: Akses Hapus User Tanpa Login Admin
**Steps:**
1. Logout dari admin
2. Akses URL: `/user/delete/1`

**Expected Result:**
- ❌ Tidak bisa hapus user
- ✅ Redirect ke `/login`

#### Test Case 3: User Coba Akses Route Admin
**Steps:**
1. Login sebagai user (bukan admin)
2. Akses URL: `/user/delete/1`

**Expected Result:**
- ❌ Tidak bisa hapus user
- ✅ Redirect ke `/login`

#### Test Case 4: SQL Injection Prevention
**Steps:**
1. Coba input SQL injection di form ganti password:
   - Password Lama: `' OR '1'='1`
   - Password Baru: `'; DROP TABLE user; --`

**Expected Result:**
- ✅ Input di-escape dengan benar
- ✅ Tidak ada SQL injection
- ✅ Password tidak berubah (karena password lama salah)

---

## 📊 Checklist Testing

### Fitur Ganti Password
- [ ] Ganti password berhasil
- [ ] Password lama salah ditolak
- [ ] Password tidak cocok ditolak
- [ ] Password terlalu pendek ditolak
- [ ] Validasi client-side berfungsi
- [ ] Link muncul di semua halaman user
- [ ] Redirect setelah sukses
- [ ] Flash message muncul
- [ ] Session tetap aktif
- [ ] Login dengan password baru berhasil

### Fitur Hapus User
- [ ] Hapus user berhasil
- [ ] Konfirmasi dialog muncul
- [ ] Cascade delete penilaian
- [ ] Cascade delete voting
- [ ] Batal hapus berfungsi
- [ ] User tidak ada ditangani
- [ ] Flash message muncul
- [ ] Tombol trash visible
- [ ] Hover effect berfungsi
- [ ] Tidak ada orphaned data

### Keamanan
- [ ] Akses tanpa login ditolak
- [ ] User tidak bisa akses route admin
- [ ] Password di-hash dengan benar
- [ ] SQL injection prevention
- [ ] XSS prevention

### UI/UX
- [ ] Responsive di mobile
- [ ] Responsive di tablet
- [ ] Responsive di desktop
- [ ] Hover effects smooth
- [ ] Flash messages styled
- [ ] Icons muncul dengan benar
- [ ] Colors consistent
- [ ] Typography readable

---

## 🐛 Bug Report Template

Jika menemukan bug, gunakan template ini:

```
**Bug Title:** [Judul singkat bug]

**Severity:** [Critical / High / Medium / Low]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Result:**
[Apa yang seharusnya terjadi]

**Actual Result:**
[Apa yang sebenarnya terjadi]

**Screenshots:**
[Jika ada]

**Environment:**
- Browser: 
- OS: 
- Python Version: 
- MySQL Version: 

**Additional Notes:**
[Informasi tambahan]
```

---

## ✅ Testing Completion

Setelah semua test case di atas berhasil, fitur siap untuk production!

**Tested by:** _______________
**Date:** _______________
**Status:** [ ] Pass / [ ] Fail
**Notes:** _______________

