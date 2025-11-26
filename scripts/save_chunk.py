file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 21685
end = 23328
chunk = content[start:end]

with open('corrupted_chunk.txt', 'w', encoding='utf-8') as f:
    f.write(chunk)
