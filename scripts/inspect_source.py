file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

source_idx = content.find('Source', 21558)
print(f"--- Source context ---")
print(content[source_idx:source_idx+200])

if 'dotnet_bot.png' in content[source_idx:source_idx+200]:
    print("Found dotnet_bot.png")
else:
    print("dotnet_bot.png NOT found in context")
