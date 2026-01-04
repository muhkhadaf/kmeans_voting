
import os

path = r'c:\program_freelance\kmeans_voting\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """        execute_query(
            "UPDATE user SET password = %s WHERE id = %s",
            (hashed_password, session['user_id'])
        )"""

replacement = """        execute_query(
            "UPDATE user SET password = %s WHERE id = %s",
            (hashed_password, session['user_id'])
        )
        
        flash('Password berhasil diubah!', 'success')
        return redirect(url_for('user_vote'))
    
    return render_template('user_change_password.html')"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced content")
else:
    print("Target content not found")
    # Debug: print surrounding content
    idx = content.find('hashed_password = generate_password_hash(new_password)')
    if idx != -1:
        print("Found anchor, surrounding content:")
        print(content[idx:idx+200])
