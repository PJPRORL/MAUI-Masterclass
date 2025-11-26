file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Error 1: Unexpected closing tag 'button' at 19336
offset1 = 19336
print(f"--- Context around {offset1} ---")
start1 = max(0, offset1 - 100)
end1 = min(len(content), offset1 + 100)
print(content[start1:end1])

# Error 2: Unclosed tag '' at 23538
offset2 = 23538
print(f"--- Context around {offset2} ---")
start2 = max(0, offset2 - 100)
end2 = min(len(content), offset2 + 100)
print(content[start2:end2])

# Fix 1: Remove </button> if no <button>
# Check if <button> is nearby?
# If not, remove it.
chunk1 = content[offset1:offset1+20]
if chunk1.startswith('</button>'):
    print("Removing unexpected </button>")
    content = content[:offset1] + content[offset1+9:]

# Fix 2: Unclosed tag ''
# Context: HorizontalOptions<","/span>
# It seems to be <",/span> or similar?
# The output showed: HorizontalOptions<","/span>
# Wait, the error is at 23538.
# The context printed: <span class="token attr-name">HorizontalOptions<","/span><span class="token attr-value"><span cl
# It looks like `HorizontalOptions<"` is the issue?
# Or `HorizontalOptions<` followed by `"/span>`?
# Maybe it should be `HorizontalOptions` and then `</span>`?
# But `HorizontalOptions` is inside `attr-name`.
# `HorizontalOptions="Center"` usually.
# Here it seems `HorizontalOptions` is the text content of the span?
# `<span ...>HorizontalOptions</span>`?
# But we see `HorizontalOptions<","/span>`.
# This implies `HorizontalOptions` is followed by `<"` and then `/span>`.
# This is definitely garbage.
# I will replace `<","/span>` with `</span>`?
# Or just remove `<"`?
# Let's try to find `<",` and replace with nothing or `</span>` if it looks like a closing tag.
# Actually, `HorizontalOptions` is an attribute name.
# So it should be `<span class="token attr-name">HorizontalOptions</span>`.
# If we have `<span class="token attr-name">HorizontalOptions<","/span>`, it means `</span>` is corrupted to `<","/span>`.
# So I will replace `<","/span>` with `</span>`.

if '<","/span>' in content:
    print("Fixing <\",/span> -> </span>")
    content = content.replace('<","/span>', '</span>')
elif '<",/span>' in content:
    print("Fixing <\",/span> -> </span>")
    content = content.replace('<",/span>', '</span>')
else:
    # Fallback: check what is at offset2
    chunk2 = content[offset2:offset2+10]
    print(f"Chunk at offset2: {repr(chunk2)}")
    if chunk2.startswith('<"'):
        print("Removing <\"")
        content = content[:offset2] + content[offset2+2:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
