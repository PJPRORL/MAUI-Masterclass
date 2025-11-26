file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: >alse" -> focusable="false"
if '>alse"' in content:
    print("Fixing >alse\" -> focusable=\"false\"")
    content = content.replace('>alse"', ' focusable="false"')

# Also check for "22.9">alse" specifically if the above is too broad
# But >alse" is pretty specific and likely wrong anywhere.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
