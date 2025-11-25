# Bug Fixes - K-Means Voting System v2.1.1

**Release Date:** 25 November 2024

## 🐛 Bug Fixes

### 1. Database Initialization Error - Foreign Key Constraint

**Problem:**
```
Error initializing database: (1005, 'Can\'t create table `voting`.`penilaian` (errno: 150 "Foreign key constraint is incorrectly formed")')
```

**Root Cause:**
Tabel `penilaian` dibuat sebelum tabel `user`, sehingga foreign key `user_id` tidak bisa dibuat karena tabel referensi belum ada.

**Solution:**
Mengubah urutan pembuatan tabel di `db.py`:
1. `admin` (tidak ada foreign key)
2. `user` (tidak ada foreign key)
3. `anggota` (tidak ada foreign key)
4. `penilaian` (foreign key ke `user` dan `anggota`)
5. `voting_periods` (tidak ada foreign key)
6. `voting` (foreign key ke `user`, `anggota`, dan `voting_periods`)

**Files Changed:**
- `db.py` - Reorder table creation

---

### 2. Template Error - Column Not Found

**Problem:**
```
TypeError: can only concatenate str (not "int") to str
Database error: (1054, "Unknown column 'a.keaktifan' in 'field list'")
```

**Root Cause:**
Template dan query masih menggunakan struktur tabel lama yang memiliki kolom `keaktifan`, `kepemimpinan`, `pengalaman`, `disiplin`, `usia` langsung di tabel `anggota`. Struktur baru menggunakan tabel `penilaian` untuk menyimpan rating.

**Solution:**

#### A. Update Template `voting.html`
Mengubah tampilan kandidat dari menampilkan nilai kriteria langsung menjadi menampilkan:
- Nama
- Pendidikan
- Cluster (jika ada)
- Visi & Misi (preview 100 karakter)

**Before:**
```html
<h4>{{ candidate[1] }}</h4>
<span>Keaktifan: {{ candidate[2] }}</span>
<span>Kepemimpinan: {{ candidate[3] }}</span>
<span>Usia: {{ candidate[7] }} tahun</span>
<div>Skor Total: {{ (candidate[2] + ... + candidate[7]) / 6 }}</div>
```

**After:**
```html
<h4>{{ candidate[1] }}</h4>
<span>Pendidikan: {{ candidate[2] }}</span>
<span>Cluster: {{ candidate[4] }}</span>
<div>Visi & Misi: {{ candidate[3][:100] }}...</div>
```

#### B. Update Query di `hasil()` Function
Mengubah query untuk mengambil rata-rata penilaian dari tabel `penilaian` menggunakan JOIN.

**Before:**
```sql
SELECT a.id, a.nama, COUNT(v.id) as vote_count,
       a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
FROM anggota a
LEFT JOIN voting v ON a.id = v.kandidat_id
WHERE a.status = 'kandidat'
GROUP BY a.id, a.nama, a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
```

**After:**
```sql
SELECT a.id, a.nama, COUNT(v.id) as vote_count,
       a.pendidikan, a.cluster,
       AVG(p.keaktifan) as avg_keaktifan,
       AVG(p.kepemimpinan) as avg_kepemimpinan,
       AVG(p.pengalaman) as avg_pengalaman,
       AVG(p.disiplin) as avg_disiplin,
       AVG(p.komunikasi) as avg_komunikasi
FROM anggota a
LEFT JOIN voting v ON a.id = v.kandidat_id
LEFT JOIN penilaian p ON a.id = p.anggota_id
WHERE a.status = 'kandidat'
GROUP BY a.id, a.nama, a.pendidikan, a.cluster
```

#### C. Update Cluster Results Query
Mengubah query untuk mendapatkan hasil clustering dengan rata-rata penilaian.

**Before:**
```sql
SELECT nama, keaktifan, kepemimpinan, pengalaman, disiplin, pendidikan, usia, cluster
FROM anggota 
WHERE cluster IS NOT NULL
```

