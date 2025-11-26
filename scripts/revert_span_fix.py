file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert: "&gt;</span>" -> "&gt;</span></span>"
# But wait, I replaced "&gt;</span></span>" with "&gt;</span>".
# So I should replace "&gt;</span>" with "&gt;</span></span>"
# BUT "&gt;</span>" might be correct in some places!
# I only want to revert the ones I changed.
# Since I did a global replace, I probably broke valid ones too?
# Or maybe all "&gt;</span></span>" were valid and I broke them.
# I'll assume I should revert all "&gt;</span>" to "&gt;</span></span>" IF they were originally double.
# But I can't know which ones were double.
# However, the errors suggest I have too many OPEN spans now.
# So I need MORE closing spans.
# So adding </span> back seems correct.
# But blindly replacing all "&gt;</span>" with "&gt;</span></span>" might add too many.

# Let's check if I can find where I made changes.
# I don't have a backup.
# But I know the pattern was `&gt;</span></span>`.
# If I search for `&gt;</span>` now, I will find them.
# The question is: are there any `&gt;</span>` that SHOULD be single?
# Probably.
# This is bad.

# Alternative:
# I can re-run `process_chapter01.py`!
# This will regenerate `Chapter01.razor` from the chunks.
# The chunks are still there (and I fixed `part4.json` manually).
# The `process_chapter01.py` script is fine.
# This is the safest way to get back to a clean state (with the original errors).
# Then I can apply the `sdpan` fix and `focusable` fix again, but CAREFULLY.

print("Regenerating Chapter01.razor from chunks...")
