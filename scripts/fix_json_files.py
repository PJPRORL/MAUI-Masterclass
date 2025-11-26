import os
import glob

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix invalid escape \'
    content = content.replace("\\'", "'")
    
    # Fix escaped quote before total key
    # This might happen if the previous string ended with \"
    # We want "total":24, not "total\":24
    content = content.replace('total\\":', 'total":')
    
    # Also fix "total\" :
    content = content.replace('total\\" :', 'total" :')

    # Fix specific issue in part2 where closing quote of chunk might be escaped
    # ...spa\",\"total -> ...spa","total
    content = content.replace('spa\\",\\"total', 'spa","total')
    
    # Fix escaped quote before total key after array end
    # ],\"total -> ],"total
    content = content.replace('],\\"total', '],"total')
    content = content.replace('], \\"total', '], "total')
    
    # Fix escaped quote before array end
    # \"] -> "]
    content = content.replace('\\\\"]', '"]')
    
    if content != original_content:
        print(f"Fixed {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"No changes in {filepath}")

def main():
    files = glob.glob('temp_chunks/part*.json')
    for filepath in files:
        fix_file(filepath)

if __name__ == "__main__":
    main()
