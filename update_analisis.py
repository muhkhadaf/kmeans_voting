with open('templates/analisis.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the subtitle to clarify K-Means is optional
content = content.replace(
    '<p class="text-gray-600">Analisis kelayakan anggota berdasarkan penilaian user</p>',
    '<p class="text-gray-600">Analisis clustering opsional untuk visualisasi kelayakan kandidat berdasarkan penilaian voters</p>'
)

# Update the info section
old_info = '''            <h3 class="text-lg font-medium text-blue-800 mb-2">Tentang Analisis K-Means</h3>
            <div class="text-blue-700 space-y-2">
                <p>Algoritma K-Means akan mengelompokkan anggota menjadi 3 cluster berdasarkan rata-rata penilaian user pada kriteria:</p>'''

new_info = '''            <h3 class="text-lg font-medium text-blue-800 mb-2">Tentang Analisis K-Means (Opsional)</h3>
            <div class="text-blue-700 space-y-2">
                <p><strong>Catatan:</strong> Anda dapat langsung memilih kandidat di menu "Kelola Voting" tanpa menjalankan analisis ini.</p>
                <p class="mt-2">Analisis K-Means akan mengelompokkan kandidat menjadi 3 cluster berdasarkan rata-rata penilaian voters pada kriteria:</p>'''

content = content.replace(old_info, new_info)

# Update the note about ratings
content = content.replace(
    '<p class="mt-2 text-sm"><em>Catatan: Anggota harus memiliki penilaian dari user sebelum dapat dianalisis</em></p>',
    '<p class="mt-2 text-sm"><em>Catatan: Kandidat harus memiliki penilaian dari voters sebelum dapat dianalisis</em></p>'
)

# Update step 4 in instructions
content = content.replace(
    '<p>Lihat hasil clustering dan pilih kandidat terbaik untuk tahap voting</p>',
    '<p>Lihat hasil clustering sebagai referensi tambahan untuk evaluasi kandidat</p>'
)

with open('templates/analisis.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated analisis.html to show K-Means as optional")
