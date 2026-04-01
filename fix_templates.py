import os
import re

def fix_html_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                modified = False
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Fix truncated {% endif
                    new_content = re.sub(r'{%\s*endif\s*(?!%})', '{% endif %}', content)
                    if new_content != content:
                        content = new_content
                        modified = True
                    
                    # Fix truncated {% endfor
                    new_content = re.sub(r'{%\s*endfor\s*(?!%})', '{% endfor %}', content)
                    if new_content != content:
                        content = new_content
                        modified = True

                    # Fix truncated {% block ...
                    new_content = re.sub(r'{%\s*block\s+([\w_]+)\s*(?!%})', r'{% block \1 %}', content)
                    if new_content != content:
                        content = new_content
                        modified = True

                    # Fix truncated {% endblock
                    new_content = re.sub(r'{%\s*endblock\s*(?!%})', '{% endblock %}', content)
                    if new_content != content:
                        content = new_content
                        modified = True

                    # Also check for split braces that I might have missed
                    # (This is harder to regex safely, but let's try to find common ones)
                    
                    if modified:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Fixed truncated tags in {path}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    fix_html_files('templates')
