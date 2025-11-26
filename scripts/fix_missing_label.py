file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target: <span class="token attr-name">FontSize</span>
# We want to insert <span class="token tag"><span class="token punctuation">&lt;</span>Label</span>\n                
# before it.

target = '<span class="token attr-name">FontSize</span>'
replacement = '<span class="token tag"><span class="token punctuation">&lt;</span>Label</span>\n                <span class="token attr-name">FontSize</span>'

# Find the specific occurrence around 23328
idx = content.find(target, 23000)
if idx != -1:
    print(f"Found target at {idx}")
    # Verify context
    print(f"Context: {content[idx-50:idx+50]}")
    
    # Replace
    content = content[:idx] + replacement + content[idx+len(target):]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Target not found.")
