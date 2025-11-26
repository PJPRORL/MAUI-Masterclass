file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

if len(lines) >= 5:
    line5 = lines[4] # 0-indexed
    print(f"Line 5 length: {len(line5)}")
    if len(line5) > 323:
        print(f"Char at 323: {line5[323]}")
        print(f"Context around 323: {line5[300:350]}")
    else:
        print("Line 5 is shorter than 323 chars.")
else:
    print("File has fewer than 5 lines.")
