file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total length: {len(content)}")

# Count spans
open_spans = content.count('<span')
close_spans = content.count('</span>')
print(f"Open spans: {open_spans}")
print(f"Close spans: {close_spans}")
print(f"Diff: {open_spans - close_spans}")

# Find occurrences of als">
print(f"Occurrences of 'als\">': {content.count('als\">')}")
# Find occurrences of </button>
print(f"Occurrences of '</button>': {content.count('</button>')}")

# Find first unclosed span (naive)
balance = 0
for i in range(len(content)):
    if content.startswith('<span', i):
        balance += 1
    elif content.startswith('</span>', i):
        balance -= 1
    
    if balance < 0:
        print(f"Negative balance (unexpected closing) at {i}")
        print(content[max(0, i-50):min(len(content), i+50)])
        break
