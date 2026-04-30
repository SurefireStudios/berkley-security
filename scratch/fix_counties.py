import os
import re

def fix_county(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace "cameras Copiah County" -> "Copiah County"
    # Replace "home security Pointe Coupee Parish" -> "Pointe Coupee Parish"
    
    content = re.sub(r'cameras\s+([A-Za-z]+(?:\s[A-Za-z]+)?\s(?:County|Parish))', r'\1', content)
    content = re.sub(r'home security\s+([A-Za-z]+(?:\s[A-Za-z]+)?\s(?:County|Parish))', r'\1', content)
    content = re.sub(r'security\s+([A-Za-z]+(?:\s[A-Za-z]+)?\s(?:County|Parish))', r'\1', content)
    
    # Also I need to make sure I don't leave double spaces if they exist
    content = content.replace('  ', ' ')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
if __name__ == '__main__':
    base_dir = r"c:\Users\Haz\Desktop\Berkley Security\city"
    files_to_process = [
        "wesson-ms.html", "waynesboro-ms.html", "forest-ms.html", "urania-la.html",
        "tullos-la.html", "prentiss-ms.html", "philadelphia-ms.html", "newton-ms.html",
        "mer-rouge-la.html", "batesville-ms.html", "olla-la.html", "oak-grove-la.html",
        "morton-ms.html", "monticello-ms.html", "new-roads-la.html"
    ]
    
    for filename in files_to_process:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            fix_county(filepath)
            print(f"Fixed {filename}")
