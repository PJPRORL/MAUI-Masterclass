file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 20100
end = 34125
next_pre = content.find('<pre', start, end)

if next_pre != -1:
    print(f"Found another <pre at: {next_pre}")
    print(f"Context: {content[next_pre-50:next_pre+50]}")
else:
    print("No <pre found between 20100 and 34125")
