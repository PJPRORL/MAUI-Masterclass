file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'
file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

offset = 23553
print(f"--- Context around {offset} ---")
start = max(0, offset - 100)
end = min(len(content), offset + 100)
print(content[start:end])
