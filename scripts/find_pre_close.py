file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

offset = 19970
next_pre_close = content.find('</pre>', offset)
next_div_close = content.find('</div>', offset)

print(f"Next </pre> at: {next_pre_close}")
print(f"Next </div> at: {next_div_close}")

if next_pre_close != -1:
    print(f"Context around </pre>: {content[next_pre_close-50:next_pre_close+50]}")
