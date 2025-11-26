import os

file_path = 'temp_chunks/part3.json'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

if lines:
    if lines[0].strip().startswith('```'):
        print("Removing first line")
        lines = lines[1:]
    
    if lines and lines[-1].strip().startswith('```'):
        print("Removing last line")
        lines = lines[:-1]

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Cleaned part3.json")
