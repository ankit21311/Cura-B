"""
Fix all split Django template tags across the project.
A split tag is one where {{ or {% starts on one line and }} or %} ends on another.
Django's template engine does NOT support multi-line tags.
"""
import os
import re

def fix_split_tags(directory):
    fixed_files = []
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if not filename.endswith('.html'):
                continue
            
            filepath = os.path.join(root, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # Fix split {{ ... }} tags (variable tags)
                # Match {{ followed by anything (including newlines) until }}
                # Only fix if there's a newline inside
                def fix_var_tag(m):
                    inner = m.group(1)
                    if '\n' in inner or '\r' in inner:
                        # Collapse whitespace (including newlines) to single space
                        inner = re.sub(r'\s+', ' ', inner).strip()
                        return '{{ ' + inner + ' }}'
                    return m.group(0)
                
                content = re.sub(r'\{\{(.*?)\}\}', fix_var_tag, content, flags=re.DOTALL)
                
                # Fix split {% ... %} tags (block tags)
                def fix_block_tag(m):
                    inner = m.group(1)
                    if '\n' in inner or '\r' in inner:
                        inner = re.sub(r'\s+', ' ', inner).strip()
                        return '{% ' + inner + ' %}'
                    return m.group(0)
                
                content = re.sub(r'\{%(.*?)%\}', fix_block_tag, content, flags=re.DOTALL)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_files.append(filepath)
                    print(f"Fixed: {filepath}")
            
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
    
    return fixed_files

if __name__ == '__main__':
    fixed = fix_split_tags('templates')
    print(f"\nTotal files fixed: {len(fixed)}")
    for f in fixed:
        print(f"  - {f}")
