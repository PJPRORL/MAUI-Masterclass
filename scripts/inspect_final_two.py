file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Error 1: Unexpected closing tag 'button' at 19336
offset1 = 19336
print(f"--- Context around {offset1} ---")
start1 = max(0, offset1 - 100)
end1 = min(len(content), offset1 + 100)
print(content[start1:end1])

# Error 2: Unexpected closing tag 'span' at 23766
offset2 = 23766
print(f"--- Context around {offset2} ---")
start2 = max(0, offset2 - 100)
end2 = min(len(content), offset2 + 100)
print(content[start2:end2])
