import json

file_path = 'temp_chunks/part4.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"Content head: {repr(content[:100])}")
        print(f"Content tail: {repr(content[-100:])}")
        # Print around column 8955
        start = max(0, 8955 - 50)
        end = min(len(content), 8955 + 50)
        print(f"Context around 8955: {repr(content[start:end])}")
        
        json.loads(content)
        print("Valid JSON")
except Exception as e:
    print(f"Error: {e}")
