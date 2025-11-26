file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

offset = 23553
# Search backwards for <span class="token tag">
start_index = content.rfind('<span class="token tag">', 0, offset)

if start_index != -1:
    print(f"Found tag start at {start_index}")
    print(f"--- Context around {start_index} ---")
    print(content[start_index:start_index+200])
else:
    print("Tag start not found.")
