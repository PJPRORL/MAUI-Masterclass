file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Context: Center<span class="token punctuation">"</span></span>
# Replace with: Center<span class="token punctuation">"</span>
target = 'Center<span class="token punctuation">"</span></span>'
replacement = 'Center<span class="token punctuation">"</span>'

if target in content:
    print(f"Found target. Replacing...")
    content = content.replace(target, replacement)
else:
    print("Target not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
