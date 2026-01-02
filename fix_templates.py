# Remove Penilaian link from user_voting.html
with open('templates/user_voting.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the Penilaian link from navigation
old_nav = """                    <a href="{{ url_for('user_penilaian') }}" 
                       class="text-blue-600 hover:text-blue-800 transition-colors">
                        <i class="fas fa-star mr-1"></i>
                        Penilaian
                    </a>"""

content = content.replace(old_nav, '')

with open('templates/user_voting.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed Penilaian link from user_voting.html")
