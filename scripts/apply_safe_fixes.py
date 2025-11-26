file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Inspect Duplicate Class (around 71926)
print("--- Context around 71926 (Duplicate Class) ---")
start = max(0, 71926 - 100)
end = min(len(content), 71926 + 100)
print(content[start:end])

# Inspect v3 (around 72263 - polygon error)
print("--- Context around 72263 (Polygon/v3) ---")
start = max(0, 72263 - 100)
end = min(len(content), 72263 + 100)
print(content[start:end])

# Fix 1: sdpan -> span
if 'sdpan' in content:
    print("Fixing sdpan -> span")
    content = content.replace('sdpan', 'span')

# Fix 2: cusable -> " focusable
# "22cusable="false"" -> "22" focusable="false""
if '22cusable="false"' in content:
    print("Fixing 22cusable -> 22\" focusable")
    content = content.replace('22cusable="false"', '22" focusable="false"')

# Fix 3: v3 -> 51.3
if 'v3,54.3' in content:
    print("Fixing v3 -> 51.3")
    content = content.replace('v3,54.3', '51.3,54.3')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
