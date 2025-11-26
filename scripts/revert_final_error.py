file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert: Center<span class="token punctuation">"</span> -> Center<span class="token punctuation">"</span></span>
target = 'Center<span class="token punctuation">"</span>'
replacement = 'Center<span class="token punctuation">"</span></span>'

# Be careful not to double replace if I run it multiple times or on other occurrences.
# But "Center" is specific enough?
# Let's check context.
if target in content and replacement not in content:
     # This logic is flawed if replacement is already there elsewhere.
     # But I only replaced ONE occurrence.
     # So I should find ONE occurrence of target that is NOT followed by </span>.
     pass

# Better: just replace back.
# I know I replaced it.
if 'Center<span class="token punctuation">"</span>' in content:
    # Check if it is followed by </span>
    # If not, replace.
    # But string replace is global.
    # I should use the same logic as before but reversed.
    print("Reverting...")
    content = content.replace('Center<span class="token punctuation">"</span>', 'Center<span class="token punctuation">"</span></span>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
