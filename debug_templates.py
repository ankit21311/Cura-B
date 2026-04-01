import os

search_folders = ['templates']
results = []

for folder in search_folders:
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if '{{' in line:
                                results.append(f"{path}:{i+1}:{line.strip()}")
                except Exception as e:
                    results.append(f"Error reading {path}: {e}")

with open('full_search_results.txt', 'w', encoding='ascii', errors='replace') as f:
    f.write('\n'.join(results))
