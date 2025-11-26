file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Find polygon tag
# <polygon ... >
matches = list(re.finditer(r'<polygon[^>]*>', content))
if matches:
    print(f"Found {len(matches)} polygon tags")
    for m in matches:
        tag = m.group(0)
        print(f"Tag: {tag}")
        if not tag.endswith('/>') and '</polygon>' not in content[m.end():m.end()+20]:
            print("Polygon tag might be unclosed!")
else:
    print("No polygon tags found")
