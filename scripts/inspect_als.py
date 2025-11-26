file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all indices of als">
import re
indices = [m.start() for m in re.finditer('als">', content)]

print(f"Found {len(indices)} occurrences.")

for i in indices[:5]: # Print first 5
    print(f"--- Context around {i} ---")
    start = max(0, i - 50)
    end = min(len(content), i + 50)
    print(content[start:end])
