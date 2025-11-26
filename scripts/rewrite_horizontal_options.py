file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target: HorizontalOptions...Center...
# We want to replace the whole mess with a clean version.
# Regex to match the block.
import re
# Match from HorizontalOptions to the closing span of Center
# Be careful with greedy matching.
pattern = r'<span class="token attr-name">HorizontalOptions="Center"</span>'
# We need to be sure we match the right one.
# There might be multiple HorizontalOptions="Center".
# But the error is at 23757.
# Let's find the one around 23757.

match = re.search(pattern, content[23000:25000], re.DOTALL)
if match:
    print(f"Found match: {match.group(0)}")
    # Construct clean version - no span, just text
    clean = 'HorizontalOptions="Center"'
    
    # Replace in content
    # We need to find the absolute position.
    start = 23000 + match.start()
    end = 23000 + match.end()
    
    print(f"Replacing at {start}-{end}")
    content = content[:start] + clean + content[end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Could not find the block with regex.")
