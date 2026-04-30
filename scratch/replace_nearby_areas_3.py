import os
import re
from bs4 import BeautifulSoup

def fix_remaining():
    base_dir = r"c:\Users\Haz\Desktop\Berkley Security"
    city_dir = os.path.join(base_dir, "city")
    index_path = os.path.join(base_dir, "index.html")

    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    match = re.search(r'(<!-- Areas We Serve Section -->[\s\S]*?<section id="service-areas"[\s\S]*?</section>)', index_content)
    service_areas_block = match.group(1).replace('href="city/', 'href="')

    failed_files = ["hattiesburg-ms.html", "newellton-la.html", "rayville-la.html", "st-joseph-la.html", "waterproof-la.html"]
    
    for filename in failed_files:
        filepath = os.path.join(city_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        sections = soup.find_all('section')
        for section in sections:
            h2 = section.find('h2')
            if h2 and 'Serving' in h2.text:
                # We found the section
                pattern = r'<section[^>]*>[\s\S]*?' + re.escape(str(h2)) + r'[\s\S]*?</section>'
                new_content, count = re.subn(pattern, lambda m: service_areas_block, content, count=1)
                if count > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {filename}")
                break

if __name__ == '__main__':
    fix_remaining()
