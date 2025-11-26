file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 21685
end = 23328
chunk_size = 500

for i in range(start, end, chunk_size):
    print(f"--- Chunk {i} ---")
    print(content[i:min(end, i+chunk_size)])
