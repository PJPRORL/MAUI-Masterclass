file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: cusable="false" -> focusable="false"
# It looked like "...22cusable="false"..."
# It should probably be "...22" focusable="false"..."
# Revert bad fix
if 'fo focusable="false"' in content:
    print("Reverting bad fix...")
    content = content.replace('fo focusable="false"', 'focusable="false"')

# Fix 1: cusable="false" -> focusable="false" (only if not preceded by fo)
# We use regex to find it
import re
# Find 'cusable="false"' not preceded by 'fo'
# (?<!fo)cusable="false"
matches = list(re.finditer(r'(?<!fo)cusable="false"', content))
if matches:
    print(f"Found {len(matches)} real corruptions of 'cusable=\"false\"'")
    for m in matches:
        print(f"Context: {content[m.start()-10:m.end()+10]}")
    
    # Replace
    content = re.sub(r'(?<!fo)cusable="false"', ' focusable="false"', content)

# Fix 2: view3 -> viewBox
# Regex for view3
matches = list(re.finditer(r'view3', content))
if matches:
    print(f"Found {len(matches)} 'view3'")
    for m in matches:
        print(f"Context: {content[m.start()-10:m.end()+10]}")
        
    # If it looks like "view3,54.3", it might be "viewBox" corrupted.
    # But "viewBox" takes 4 numbers. "0 0 100 100".
    # "view3" might be "viewBox" where "Box" became "3"? Unlikely.
    # Maybe "viewBox" -> "viewB" -> "view3"?
    # Let's see the context.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

