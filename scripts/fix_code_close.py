file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: "></div><div class="line-number"> -> </code></div><div class="line-number">
# We match the specific sequence around 27971
target = '"></div><div class="line-number">'
replacement = '</code></div><div class="line-number">'

if target in content:
    print("Fixing unclosed code tag...")
    content = content.replace(target, replacement)
else:
    print("Target sequence not found!")
    # Debug
    start = 27971 - 20
    end = 27971 + 50
    print(f"Context: {content[start:end]}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
