import os

path = r'c:\program_freelance\kmeans_voting\db.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """                created_by VARCHAR(100) NOT NULL
            )
        \"\"\")"""

replacement = """                created_by VARCHAR(100) NOT NULL,
                manually_stopped TINYINT DEFAULT 0,
                stopped_at DATETIME DEFAULT NULL,
                extended_count INT DEFAULT 0
            )
        \"\"\")"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated db.py schema")
else:
    print("Target content not found in db.py")
