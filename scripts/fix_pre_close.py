file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: </div></div></div><p> -> </div></pre></div></div><p>
target = '</div></div></div><p>'
replacement = '</div></pre></div></div><p>'

if target in content:
    print("Fixing unclosed pre tag...")
    content = content.replace(target, replacement)
else:
    print("Target sequence not found!")
    # Debug around 29000
    start = 29000 - 50
    end = 29000 + 50
    print(f"Context: {content[start:end]}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
