import urllib.request
import sys

if len(sys.argv) < 3:
    print("Usage: python fetch_chapter.py <url> <output_file>")
    sys.exit(1)

url = sys.argv[1]
output_file = sys.argv[2]

print(f"Downloading {url}...")

try:
    # Add a user agent to avoid 403 Forbidden on some sites
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"Successfully downloaded to {output_file}")
except Exception as e:
    print(f"Error downloading {url}: {e}")
    sys.exit(1)
