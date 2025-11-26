file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Search for <span class="token punctuation">&lt;</span>Label
target = '<span class="token punctuation">&lt;</span>Label'
idx = content.find(target, 23000) # Start searching around 23000

if idx != -1:
    print(f"Found target at {idx}")
    print(f"--- Context around {idx} ---")
    print(content[idx-100:idx+100])
else:
    print("Target not found.")
