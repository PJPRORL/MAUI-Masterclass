file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find Source
source_idx = content.find('Source', 21558)
# Find FontSize
fontsize_idx = content.find('FontSize', source_idx)

print(f"Source at {source_idx}, FontSize at {fontsize_idx}")
print(f"--- Content between ---")
print(content[source_idx:fontsize_idx])
