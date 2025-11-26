file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target: </span>\n\n            <span class="token punctuation">&lt;</span>Label
# Replace with: </span>\n\n            <span class="token tag"><span class="token punctuation">&lt;</span>Label

# Use regex to be safe about whitespace
import re
pattern = r'(</span>\s+<span class="token punctuation">&lt;</span>Label)'
match = re.search(pattern, content)

if match:
    print(f"Found match: {match.group(0)}")
    # We want to insert <span class="token tag"> after the whitespace and before <span class...
    # Actually, we can just replace the whole match string carefully.
    # The match includes the closing span of previous tag, whitespace, and start of Label.
    # We want to keep closing span and whitespace.
    # Then insert <span class="token tag">.
    # Then keep the rest.
    
    # Let's find the index of <span class="token punctuation"> in the match
    span_idx = match.group(0).find('<span class="token punctuation">')
    
    replacement = match.group(0)[:span_idx] + '<span class="token tag">' + match.group(0)[span_idx:]
    
    print(f"Replacement: {replacement}")
    
    content = content.replace(match.group(0), replacement)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Pattern not found.")
