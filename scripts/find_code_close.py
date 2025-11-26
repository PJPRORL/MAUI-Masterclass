file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 20100
end = 30667
code_close = content.find('</code>', start, end)

if code_close != -1:
    print(f"Found </code> at: {code_close}")
    print(f"Context: {content[code_close-50:code_close+50]}")
else:
    print("No </code> found between 20100 and 30667")
