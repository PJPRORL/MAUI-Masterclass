file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'alse"', content))
if matches:
    print(f"Found {len(matches)} 'alse\"'")
    for m in matches:
        print(f"Context: {content[m.start()-10:m.end()+10]}")
