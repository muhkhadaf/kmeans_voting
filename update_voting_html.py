with open('templates/voting.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the "Belum Ada Kandidat" section
old_section = '''            {% else %}
                <div class="text-center py-8">
                    <i class="fas fa-user-tie text-4xl text-gray-400 mb-4"></i>
                    <h4 class="text-lg font-medium text-gray-900 mb-2">Belum Ada Kandidat</h4>
                    <p class="text-gray-600 mb-4">Jalankan analisis K-Means dan pilih kandidat terlebih dahulu</p>
                    <a href="{{ url_for('analisis') }}" 
                       class="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                        <i class="fas fa-chart-line mr-2"></i>
                        Mulai Analisis
                    </a>
                </div>
            {% endif %}'''

new_section = '''            {% else %}
                <div class="py-6">
                    <h4 class="text-lg font-medium text-gray-900 mb-4">Pilih Kandidat dari Daftar Anggota</h4>
                    {% if all_members %}
                    <form method="POST" action="{{ url_for('set_kandidat') }}" id="candidateForm">
                        <div class="space-y-2 max-h-96 overflow-y-auto mb-4">
                            {% for member in all_members %}
                            <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                                <input type="checkbox" name="selected_members" value="{{ member[0] }}" 
                                       class="mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                                <div class="flex-1">
                                    <span class="font-medium text-gray-900">{{ member[1] }}</span>
                                    <span class="text-sm text-gray-600 ml-2">({{ member[2] }})</span>
                                </div>
                            </label>
                            {% endfor %}
                        </div>
                        <button type="submit" 
                                class="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center justify-center">
                            <i class="fas fa-check-circle mr-2"></i>
                            Set sebagai Kandidat
                        </button>
                    </form>
                    {% else %}
                    <div class="text-center py-8">
                        <i class="fas fa-users text-4xl text-gray-400 mb-4"></i>
                        <p class="text-gray-600">Belum ada anggota. Tambahkan anggota terlebih dahulu di menu Data Anggota.</p>
                        <a href="{{ url_for('anggota') }}" 
                           class="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors mt-4">
                            <i class="fas fa-users mr-2"></i>
                            Kelola Anggota
                        </a>
                    </div>
                    {% endif %}
                </div>
            {% endif %}'''

content = content.replace(old_section, new_section)

with open('templates/voting.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated voting.html with candidate selection interface")
