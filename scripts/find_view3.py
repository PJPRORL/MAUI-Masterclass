file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'view3' in content:
    print("Found 'view3' string literal.")
    idx = content.find('view3')
    print(f"Context: {content[idx-20:idx+20]}")
else:
    print("Did not find 'view3' string literal.")

import re
match = re.search(r'view3', content)
if match:
    print("Regex found view3")
else:
    print("Regex did not find view3")
