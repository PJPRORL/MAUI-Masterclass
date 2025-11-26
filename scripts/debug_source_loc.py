file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 21558
print(f"--- Content at {start} ---")
print(content[start:start+200])

# Find Source manually in this chunk
chunk = content[start:start+200]
idx = chunk.find('Source')
if idx != -1:
    print(f"Found Source at relative {idx}, absolute {start+idx}")
else:
    print("Source NOT found in chunk")
