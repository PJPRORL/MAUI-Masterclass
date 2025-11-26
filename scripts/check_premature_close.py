file_path = 'MauiLearningPlatform/Components/Course/Chapter01.razor'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = 21558
end = 23553 + 100 # Look a bit past the error
chunk = content[start:end]

balance = 0
premature_index = -1

for i in range(len(chunk)):
    if chunk.startswith('<span', i):
        balance += 1
    elif chunk.startswith('</span>', i):
        balance -= 1
    
    if balance == 0 and i > 0:
        print(f"Balance reached 0 at relative index {i} (absolute {start+i})")
        print(f"Context: {chunk[i-20:i+20]}")
        premature_index = i
        # Don't break, see if it goes negative or stays 0
        
if premature_index != -1:
    print("Premature closure detected.")
else:
    print("No premature closure detected.")
