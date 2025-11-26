import sys
import os

def process_chapter(input_file, output_file):
    print(f"Processing {input_file} -> {output_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        full_html = f.read()

    start_marker = '<div class="theme-hope-content">'
    
    start_index = full_html.find(start_marker)
    if start_index == -1:
        print("Start marker not found! Searching for h1...")
        # Fallback: try to find the first h1
        start_index = full_html.find('<h1')
        if start_index != -1:
            # Backtrack to find the container if possible, or just start from h1
            print("Found h1, starting from there.")
        else:
            print("Could not find start of content.")
            return
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

    if start_index != -1 and end_index != -1:
        content = full_html[start_index:end_index]
        print(f"Extracted content length: {len(content)}")
        
        # Cleanup: remove trailing </div> if present (it closes theme-hope-content)
        content = content.strip()
        if content.endswith('<!---->'):
            content = content[:-7]
        if content.endswith('</div>'):
            content = content[:-6]
            
        # Escape @ symbols for Razor
        content = content.replace('@', '&#64;')
        
        # Fix images: The source uses relative paths or absolute paths. 
        # Since we are hotlinking or just copying text, we should check image tags.
        # But for now, let's just dump the content.
        
        # Wrap in Razor component
        razor_content = f"""@namespace MauiLearningPlatform.Components.Course

<div class="prose max-w-none p-6">
{content}
</div>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(razor_content)
        print(f"Successfully written to {output_file}")
    else:
        print("Could not extract content boundaries.")
        print(f"Start index: {start_index}")
        print(f"End index: {end_index}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python process_chapter_generic.py <input_html> <output_razor>")
        sys.exit(1)
        
    process_chapter(sys.argv[1], sys.argv[2])
