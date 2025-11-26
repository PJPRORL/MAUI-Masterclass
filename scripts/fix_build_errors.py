import re

file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'
error_file = 'MauiLearningPlatform/errors_14.txt'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse errors
errors = []
with open(error_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Parse: ...Chapter01.razor(Line,Column): error Code: Message
        match = re.search(r'Chapter01\.razor\((\d+),(\d+)\): error ([^:]+): (.*)', line)
        if match:
            line_num = int(match.group(1))
            col_num = int(match.group(2))
            code = match.group(3)
            msg = match.group(4)
            errors.append({'line': line_num, 'col': col_num, 'code': code, 'msg': msg})

# Sort errors by location descending
errors.sort(key=lambda x: (x['line'], x['col']), reverse=True)

# Calculate line offsets
lines = content.splitlines(keepends=True)
line_offsets = [0]
for i in range(len(lines)):
    line_offsets.append(line_offsets[-1] + len(lines[i]))

def get_offset(line, col):
    if line > len(lines): return -1
    return line_offsets[line-1] + col - 1

# Apply fixes
for err in errors:
    offset = get_offset(err['line'], err['col'])
    if offset == -1: continue
    
    msg = err['msg']
    print(f"Processing error at {offset}: {msg}")
    
    if "Unexpected closing tag" in msg:
        chunk = content[offset:offset+20]
        match = re.match(r'^</\w+>', chunk)
        if match:
            tag = match.group(0)
            print(f"Removing unexpected tag: {tag}")
            content = content[:offset] + content[offset+len(tag):]
        else:
            print(f"Could not find tag to remove at {offset}. Chunk: {repr(chunk)}")
            
    elif "Unclosed tag" in msg:
        # Read a larger chunk to handle long tags
        chunk = content[offset:offset+500]
        # Match <tag ... >
        # We use non-greedy match for attributes
        match = re.match(r'^<(\w+).*?>', chunk, re.DOTALL)
        if match:
            tag = match.group(0)
            print(f"Removing unclosed tag: {tag}")
            content = content[:offset] + content[offset+len(tag):]
        else:
            print(f"Could not find tag to remove at {offset}. Chunk start: {repr(chunk[:50])}")
            if "Unclosed tag ''" in msg:
                if chunk.startswith('<>'):
                    print("Removing <>")
                    content = content[:offset] + content[offset+2:]
                elif chunk.startswith('< '):
                    print("Removing < ")
                    content = content[:offset] + content[offset+2:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
