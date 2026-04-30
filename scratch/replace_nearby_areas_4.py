import os
import re

def fix_last_5():
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
            
        new_content, count = re.subn(r'<section[^>]*>[\s\S]*?<div class="flex flex-wrap justify-center gap-3">[\s\S]*?</section>', lambda m: service_areas_block, content, count=1)
        
        if count == 0:
            print(f"Failed again: {filename}")
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")

if __name__ == '__main__':
    fix_last_5()
