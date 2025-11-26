file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Duplicate class
print("Searching for duplicate class...")
# <tag ... class="..." ... class="..." ... >
# We need to be careful not to match across tags.
# So [^>]* is important.
match = re.search(r'<[^>]+class="[^"]*"[^>]+class="[^"]*"[^>]*>', content)
if match:
    print("Found duplicate class!")
    print(f"Match: {match.group(0)}")
else:
    print("No duplicate class found by regex.")

# Unclosed polygon
print("Searching for unclosed polygon...")
# <polygon ... > (without / at end)
# And not followed by </polygon>
matches = list(re.finditer(r'<polygon[^>]*>', content))
if matches:
    for m in matches:
        tag = m.group(0)
        if not tag.endswith('/>') and not tag.endswith('</polygon>'):
            # Check if </polygon> follows immediately
            following = content[m.end():m.end()+10]
            if '</polygon>' not in following:
                print(f"Potential unclosed polygon: {tag}")
                print(f"Following: {following}")
