file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

source_idx = content.find('Source', 21558)
# Find end of Source line
source_end = content.find('\n', source_idx)
fontsize_idx = content.find('FontSize', source_end)

print(f"Source end at {source_end}, FontSize at {fontsize_idx}")
print(f"--- Garbage Content ---")
print(content[source_end:fontsize_idx])
