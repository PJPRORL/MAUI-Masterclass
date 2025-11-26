file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Restore attr-equals span
# als"> -> als">=</span>
# This restores <span class="... attr-equals">=</span>
if 'als">' in content:
    print(f"Restoring {content.count('als\">')} occurrences of als\">")
    content = content.replace('als">', 'als">=</span>')

# Fix 2: Remove remaining orphaned </button>
# Check context first
import re
# Find </button> not preceded by <button...>
# This is hard with regex on full file.
# Let's just find them and print context.
indices = [m.start() for m in re.finditer('</button>', content)]
for i in indices:
    print(f"--- </button> at {i} ---")
    print(content[max(0, i-50):min(len(content), i+20)])

# Based on previous knowledge, they are likely orphaned.
# I will remove them if they look like the copy button one.
# </p><div class="copy-icon"></div></button>
if '</p><div class="copy-icon"></div></button>' in content:
    print("Removing orphaned </button> (exact match)")
    content = content.replace('</p><div class="copy-icon"></div></button>', '</p><div class="copy-icon"></div>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
