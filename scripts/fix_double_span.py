file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix double spans introduced by previous fix
# als">=</span>=</span> -> als">=</span>
if 'als">=</span>=</span>' in content:
    print(f"Found {content.count('als\">=</span>=</span>')} double spans. Fixing...")
    content = content.replace('als">=</span>=</span>', 'als">=</span>')
else:
    print("No double spans found.")

# Also check for als">=</span></span> just in case
if 'als">=</span></span>' in content:
     print(f"Found {content.count('als\">=</span></span>')} double closing spans. Fixing...")
     # Be careful, maybe the second span closes something else?
     # But if it follows als">=, it's likely the duplicate.
     # However, in the error case, we saw </span></span>.
     # One closed attr-equals, one closed attr-value.
     # If we have als">=</span></span>, and attr-value closes immediately...
     # Then it is valid.
     # But if we have als">=</span>=</span>, that is definitely invalid.
     pass

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
