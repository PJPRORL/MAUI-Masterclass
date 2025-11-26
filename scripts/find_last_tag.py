file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

end = 29001
# Search backwards for &lt;/
last_tag = content.rfind('&lt;/', 20000, end)

if last_tag != -1:
    print(f"Found last tag at: {last_tag}")
    print(f"Context: {content[last_tag:end]}")
