file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target: <span class="token tag"><span class="token punctuation">&lt;</span>Label</span>\n                <span class="token attr-name">FontSize</span>
# Replace with: <span class="token tag"><span class="token punctuation">&lt;</span>Label\n                <span class="token attr-name">FontSize</span>

target = '<span class="token tag"><span class="token punctuation">&lt;</span>Label</span>\n                <span class="token attr-name">FontSize</span>'
replacement = '<span class="token tag"><span class="token punctuation">&lt;</span>Label\n                <span class="token attr-name">FontSize</span>'

if target in content:
    print("Found target. Replacing...")
    content = content.replace(target, replacement)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Target not found.")
    # Debug: print what IS there
    idx = content.find('FontSize', 23000)
    if idx != -1:
        print(f"Context around FontSize: {content[idx-50:idx+50]}")
