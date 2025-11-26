file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

offsets = [8404, 19970, 20020, 23367, 24274, 28910, 36028, 71926, 72263]

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    target_line_index = 3
    if len(lines) > target_line_index:
        content = lines[target_line_index]
        for offset in offsets:
            idx = offset - 1
            start = max(0, idx - 150)
            end = min(len(content), idx + 150)
            print(f"--- Offset {offset} ---")
            print(f"Context: {content[start:end]}")
    else:
        print("File does not have 4 lines?")
