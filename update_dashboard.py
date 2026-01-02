with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the K-Means card description
content = content.replace(
    '<p class="text-gray-600 mb-4">Jalankan algoritma K-Means untuk menentukan kandidat terbaik</p>',
    '<p class="text-gray-600 mb-4">Analisis clustering opsional untuk visualisasi kelayakan kandidat</p>'
)

# Update the workflow steps
old_workflow = '''            <h4 class="font-semibold text-gray-700 mb-2">Alur Kerja Sistem:</h4>
            <ol class="list-decimal list-inside text-gray-600 space-y-1">
                <li>Tambahkan data anggota karang taruna</li>
                <li>Jalankan analisis K-Means untuk clustering</li>
                <li>Pilih kandidat terbaik dari hasil analisis</li>
                <li>Buat akun user untuk voting</li>
                <li>Lakukan proses voting</li>
                <li>Lihat hasil dan pemenang</li>
            </ol>'''

new_workflow = '''            <h4 class="font-semibold text-gray-700 mb-2">Alur Kerja Sistem:</h4>
            <ol class="list-decimal list-inside text-gray-600 space-y-1">
                <li>Tambahkan data anggota karang taruna</li>
                <li>Pilih kandidat dari daftar anggota</li>
                <li>Buat akun user untuk voting</li>
                <li>Buat dan kelola periode voting</li>
                <li>Voters memberikan penilaian ke kandidat</li>
                <li>Lihat hasil dan pemenang</li>
                <li>(Opsional) Jalankan analisis K-Means untuk clustering</li>
            </ol>'''

content = content.replace(old_workflow, new_workflow)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dashboard.html workflow steps")
