file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'rb') as f:
    content = f.read()

offset = 23757
print(f"--- Hex around {offset} ---")
start = max(0, offset - 20)
end = min(len(content), offset + 20)
chunk = content[start:end]
print(chunk)
print(chunk.hex())
