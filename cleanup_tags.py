import os
import re

def find_split_tags(directory):
    # Regex to find split Django template tags {{ ... }} or {% ... %}
    # We look for a start brace, then any characters including newlines, until the end brace.
    # However, we only care if there is at least one newline inside.
    tag_pattern = re.compile(r'(\{\{.*?\}\}|\{%.*?%\})', re.DOTALL)
    
    findings = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    content = "".join(lines)
                    matches = tag_pattern.finditer(content)
                    
                    file_modified = False
                    new_content = content
                    
                    for match in matches:
                        tag = match.group(0)
                        if '\n' in tag:
                            # Found a split tag
                            clean_tag = re.sub(r'\s+', ' ', tag).strip()
                            # Ensure we don't accidentally remove required spaces after {{ or {%
                            if clean_tag.startswith('{{'):
                                clean_tag = '{{ ' + clean_tag[2:-2].strip() + ' }}'
                            elif clean_tag.startswith('{%'):
                                clean_tag = '{% ' + clean_tag[2:-2].strip() + ' %}'
                            
                            new_content = new_content.replace(tag, clean_tag)
                            findings.append(f"Fixed split tag in {path}: {tag.strip()} -> {clean_tag}")
                            file_modified = True
                    
                    if file_modified:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    findings.append(f"Error in {path}: {e}")
                    
    return findings

if __name__ == "__main__":
    results = find_split_tags('templates')
    with open('cleanup_log.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(results))
    print(f"Processed template files. Found {len(results)} issues.")
