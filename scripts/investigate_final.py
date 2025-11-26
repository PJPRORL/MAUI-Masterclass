file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Inspect Duplicate Class (around 71926)
print("--- Context around 71926 (Duplicate Class) ---")
start = max(0, 71926 - 300)
end = min(len(content), 71926 + 300)
print(content[start:end])

# Search for viewBox
import re
matches = list(re.finditer(r'viewBox', content))
if matches:
    print(f"Found {len(matches)} viewBox")
    for m in matches:
        print(f"Context: {content[m.start()-20:m.end()+20]}")
else:
    print("No viewBox found")

# Search for v3
matches = list(re.finditer(r'v3', content))
if matches:
    print(f"Found {len(matches)} v3")
    for m in matches:
        print(f"Context: {content[m.start()-20:m.end()+20]}")
