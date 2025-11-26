import json
import glob
import os

def process():
    chunks = []
    # Sort ensures part1, part2, ... part9 are in order
    files = sorted(glob.glob('temp_chunks/part*.json'))
    print(f"Found {len(files)} chunk files.")
    
    for f in files:
        print(f"Processing {f}...")
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                chunks.extend(data)
            elif isinstance(data, dict):
                if 'chunks' in data:
                    chunks.extend(data['chunks'])
                elif 'chunk' in data:
                    chunks.append(data['chunk'])
    
    full_html = "".join(chunks)
    # Unescape quotes
    full_html = full_html.replace('\\"', '"')
    
    print(f"Total HTML length: {len(full_html)}")
    print(f"HTML Tail: {repr(full_html[-500:])}")
    
    start_marker = '<div class="theme-hope-content">'
    end_marker = '<footer class="page-meta">'
    
    start_index = full_html.find(start_marker)
    if start_index == -1:
        print("Start marker not found! Searching for h1...")
        start_index = full_html.find('<h1 id="introductie-en-installatie"')
    else:
        start_index += len(start_marker) # Skip the div tag itself

    end_marker = '<footer class="page-meta">'
    end_index = full_html.find(end_marker, start_index)
    
    if end_index == -1:
        print("Footer not found, trying <nav class=\"page-nav\">")
        end_marker = '<nav class="page-nav">'
        end_index = full_html.find(end_marker, start_index)
        
    if end_index == -1:
        print("Nav not found, trying <div class=\"contributors\">")
        end_marker = '<div class="contributors">'
        end_index = full_html.find(end_marker, start_index)
        
    if end_index == -1:
        print("Contributors not found, trying last </div>")
        # This is risky, but maybe just take everything?
        # Let's try to find the last </div> that matches the indentation? No.
        pass
    
    if start_index != -1 and end_index != -1:
        content = full_html[start_index:end_index]
        print(f"Extracted content length: {len(content)}")
        
        # Cleanup: remove trailing </div> if present (it closes theme-hope-content)
        # The content might end with </div><!----> or just </div>
        # We'll strip whitespace and check
        content = content.strip()
        if content.endswith('<!---->'):
            content = content[:-7]
        if content.endswith('</div>'):
            content = content[:-6]
            
        # Escape @ symbols for Razor
        content = content.replace('@', '&#64;')
        
        # Wrap in Razor component
        razor_content = f"""@namespace MauiLearningPlatform.Components.Course

<div class="prose max-w-none p-6">
{content}
</div>
"""
        
        output_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(razor_content)
        print(f"Successfully written to {output_path}")
    else:
        print("Could not extract content boundaries.")
        print(f"Start index: {start_index}")
        print(f"End index: {end_index}")

if __name__ == '__main__':
    process()
