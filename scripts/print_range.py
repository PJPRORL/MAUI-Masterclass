file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 19900
end = 20100
print(f"Content {start}-{end}: {content[start:end]}")
