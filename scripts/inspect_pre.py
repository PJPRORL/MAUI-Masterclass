file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

offset = 19970
print(f"--- Context around {offset} (Unclosed pre) ---")
start = max(0, offset - 200)
end = min(len(content), offset + 200)
print(content[start:end])
