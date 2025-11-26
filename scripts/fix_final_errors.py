file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Fix 1: Duplicate class on svg
# <svg class="external-link-icon" ... class="icon outbound">
# We'll remove the second class attribute for now, or merge.
# Let's just remove the second one to be safe (or first).
# Actually, "icon outbound" seems to be the one associated with the "external-link-icon" usually.
# Let's replace 'class="icon outbound"' with '' if 'class="external-link-icon"' is present in the same tag?
# Regex: (<svg[^>]*class="external-link-icon"[^>]*)class="icon outbound"
# This is hard to match safely.
# Let's just find the specific string sequence if possible.
# The locate_errors.py output showed:
# <svg class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15" class="icon outbound">
# Wait, the output in Step 900 showed:
# <svg class="external-link-icon" ... viewBox="0 0 100 100" width="15" height="15">
# It didn't show "class="icon outbound"" in the match!
# But regex matched `class="[^"]*"[^>]+class="[^"]*"`.
# So "class="icon outbound"" MUST be there.
# Maybe it was truncated in the print output?
# Yes, output was truncated.
# So I will assume it's there.
# I will replace `class="icon outbound"` with `` inside that tag.
# Or better, replace `class="external-link-icon"` with `class="external-link-icon icon outbound"` and remove the second one.
# But simpler: just remove the second one.
content = re.sub(r'(<svg[^>]*class="external-link-icon"[^>]*)class="icon outbound"', r'\1', content)


# Fix 2: Unclosed polygon with garbage attributes
# <polygon fill="currentColor" points="..." focusable="false" x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15">
# We want to keep points and focusable="false".
# And close it with />.
# And remove x, y, viewBox, width, height.
# Regex: <polygon fill="currentColor" points="([^"]*)" focusable="false"[^>]*>
# Replace: <polygon fill="currentColor" points="\1" focusable="false" />
content = re.sub(r'<polygon fill="currentColor" points="([^"]*)" focusable="false"[^>]*>', r'<polygon fill="currentColor" points="\1" focusable="false" />', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
