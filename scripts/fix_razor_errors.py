import re

file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: sdpan -> span
if 'sdpan' in content:
    print("Found 'sdpan', replacing with 'span'")
    content = content.replace('sdpan', 'span')

# Fix 2: Duplicate class attributes
# Pattern: class="..." ... class="..."
# This is hard to regex safely globally, but let's look for specific instances
# The error was around offset 71927.
# Let's inspect that area specifically in the script
start = max(0, 71927 - 100)
end = min(len(content), 71927 + 100)
print(f"Context around 71927: {content[start:end]}")

# Regex to find tags with duplicate class
# <\w+[^>]*class="[^"]*"[^>]*class="[^"]*"
match = re.search(r'<(\w+)[^>]*class="[^"]*"[^>]*class="[^"]*"', content)
if match:
    print(f"Found duplicate class in tag <{match.group(1)}...>")
    print(f"Match: {match.group(0)}")
    
    # Simple fix: remove the second class attribute? Or merge?
    # Usually the second one is the intended one or they are duplicates.
    # Let's see what it looks like first.

# Fix 3: Unclosed tags
# <span class="token tag"><span class="token ...
# Maybe some spans are not closed.
# The error log said: Unclosed tag 'span' at 8404.
start = max(0, 8404 - 100)
end = min(len(content), 8404 + 100)
print(f"Context around 8404: {content[start:end]}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
