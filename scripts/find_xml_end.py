file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 20100
end = 30667
# Search for </ContentPage> escaped
xml_end = content.find('&lt;/ContentPage&gt;', start, end)

if xml_end != -1:
    print(f"Found &lt;/ContentPage&gt; at: {xml_end}")
    print(f"Context: {content[xml_end-50:xml_end+50]}")
else:
    print("No &lt;/ContentPage&gt; found")
    # Try finding the start of the next text paragraph?
    # <p>
    next_p = content.find('<p>', start, end)
    if next_p != -1:
        print(f"Found <p> at: {next_p}")
        print(f"Context: {content[next_p-50:next_p+50]}")
