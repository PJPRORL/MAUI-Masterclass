file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Missing quote before focusable
# "22 focusable="false"" -> "22" focusable="false""
if '22 focusable="false"' in content:
    print("Fixing missing quote before focusable...")
    content = content.replace('22 focusable="false"', '22" focusable="false"')

# Fix 2: v3 -> 51.3
# "v3,54.3" -> "51.3,54.3"
if 'v3,54.3' in content:
    print("Fixing v3 -> 51.3...")
    content = content.replace('v3,54.3', '51.3,54.3')

# Fix 3: Extra closing spans
# "&gt;</span></span>" -> "&gt;</span>"
# Only if it's common.
if '&gt;</span></span>' in content:
    print("Fixing extra closing spans...")
    content = content.replace('&gt;</span></span>', '&gt;</span>')

# Fix 4: Unclosed tag 'span' at 8404
# The context was: on">&lt;/</span>ApplicationId</span><span class="token punctuation">&gt;</span></span>
# If I replace &gt;</span></span> with &gt;</span>, it might fix it.

# Fix 5: Unclosed tag 'pre' and 'code'
# These might be due to similar extra closing tags or missing opening tags.
# Let's see if the above fixes help.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
