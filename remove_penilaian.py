import re

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Comment out the user_penilaian route and related routes
routes_to_comment = [
    '@app.route(\'/user_penilaian\')',
    '@app.route(\'/submit_penilaian\', methods=[\'POST\'])'
]

lines = content.split('\n')
new_lines = []
in_route = False
route_indent = 0

for i, line in enumerate(lines):
    # Check if this line starts a route we want to comment
    if any(route in line for route in routes_to_comment):
        in_route = True
        route_indent = len(line) - len(line.lstrip())
        new_lines.append('# ' + line)
        continue
    
    # If we're in a route, check if we've reached the next route or end
    if in_route:
        current_indent = len(line) - len(line.lstrip())
        # If line is not indented more than route def, we've left the route
        if line.strip() and current_indent <= route_indent and line.strip()[0] != '#':
            in_route = False
            new_lines.append(line)
        else:
            # Comment this line too
            if line.strip():
                new_lines.append('# ' + line)
            else:
                new_lines.append(line)
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Commented out user_penilaian and submit_penilaian routes")
