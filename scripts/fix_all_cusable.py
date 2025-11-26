file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Fix 1: ">cusable -> " focusable
if '">cusable="false"' in content:
    print("Fixing \">cusable -> \" focusable")
    content = content.replace('">cusable="false"', '" focusable="false"')

# Fix 2: Any other cusable not preceded by fo
# (?<!fo)cusable="false"
matches = list(re.finditer(r'(?<!fo)cusable="false"', content))
if matches:
    print(f"Found {len(matches)} other corruptions of 'cusable=\"false\"'")
    for m in matches:
        print(f"Context: {content[m.start()-10:m.end()+10]}")
    
    # Replace
    content = re.sub(r'(?<!fo)cusable="false"', ' focusable="false"', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
