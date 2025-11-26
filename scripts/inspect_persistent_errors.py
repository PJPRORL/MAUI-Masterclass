file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

offsets = [5939, 10861, 24195]

for offset in offsets:
    print(f"--- Context around {offset} ---")
    start = max(0, offset - 50)
    end = min(len(content), offset + 50)
    print(content[start:end])
