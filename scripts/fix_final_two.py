file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Remove </button> around 19336
# Context: ... </p><div class="copy-icon"></div></button> ...
if '</p><div class="copy-icon"></div></button>' in content:
    print("Removing unexpected </button>")
    content = content.replace('</p><div class="copy-icon"></div></button>', '</p><div class="copy-icon"></div>')

# Fix 2: Remove </span> around 23766
# Context: als">=</span>
if 'als">=</span>' in content:
    print("Removing unexpected </span> after als\">=")
    content = content.replace('als">=</span>', 'als">')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
