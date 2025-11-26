file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 19800
end = 19900
print(f"Content {start}-{end}: {content[start:end]}")
