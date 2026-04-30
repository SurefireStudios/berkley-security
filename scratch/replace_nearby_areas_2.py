import os
import glob
import re
from bs4 import BeautifulSoup

def replace_nearby_areas():
    base_dir = r"c:\Users\Haz\Desktop\Berkley Security"
    city_dir = os.path.join(base_dir, "city")
    index_path = os.path.join(base_dir, "index.html")

    # Extract the full service-areas block from index.html
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    match = re.search(r'(<!-- Areas We Serve Section -->[\s\S]*?<section id="service-areas"[\s\S]*?</section>)', index_content)
    if not match:
        print("Could not find service-areas in index.html")
        return
        
    service_areas_block = match.group(1)
    service_areas_block = service_areas_block.replace('href="city/', 'href="')

    failed_files = [
        "ferriday-la.html", "greenville-ms.html", "grenada-ms.html", "hattiesburg-ms.html",
        "indianola-ms.html", "jackson-ms.html", "mangham-la.html", "newellton-la.html",
        "petal-ms.html", "rayville-la.html", "rolling-fork-ms.html", "st-joseph-la.html",
        "tallulah-la.html", "waterproof-la.html", "west-monroe-la.html", "winnsboro-la.html"
    ]
    
    for filename in failed_files:
        filepath = os.path.join(city_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        def replace_func(m):
            return service_areas_block
            
        # Match <section>...</section> containing <h2>...Nearby Areas We Serve...</h2> or similar
        # Since we just want to match the section that has an <h2> with "Areas We Serve", "Serving ", etc.
        # Let's match ANY section that contains an h2 with "Areas" or "Serving"
        # We need to be careful not to match the whole file if there are multiple sections.
        
        # We can find the section by finding <!-- NEARBY --> or <!-- NEARBY AREAS -->
        new_content, count = re.subn(r'<!-- NEARBY[\s\S]*?<section[^>]*>[\s\S]*?</section>', replace_func, content, count=1)
        
        if count == 0:
            # Maybe just <section...> <h2> Nearby Areas We Serve </h2> ... </section>
            new_content, count = re.subn(r'<section[^>]*>[\s\S]*?<h2[^>]*>(?:Nearby Areas We Serve|Serving[\s\S]*?Areas)[\s\S]*?</section>', replace_func, content, count=1)
            
        if count == 0:
            # Let's try BeautifulSoup just to be safe
            soup = BeautifulSoup(content, 'html.parser')
            sections = soup.find_all('section')
            replaced = False
            for section in sections:
                h2 = section.find('h2')
                if h2 and ('Areas We Serve' in h2.text or 'Serving' in h2.text or 'Nearby Areas' in h2.text):
                    if 'Ready to Secure' not in h2.text and 'Why' not in h2.text and 'Services' not in h2.text and 'Questions' not in h2.text and 'Protecting' not in h2.text:
                        # Found it!
                        # We use regex to replace it in the original string to maintain formatting
                        pattern = r'<section[^>]*>[\s\S]*?' + re.escape(str(h2)) + r'[\s\S]*?</section>'
                        new_content, count = re.subn(pattern, replace_func, content, count=1)
                        if count > 0:
                            replaced = True
                        break
            if not replaced:
                print(f"Still could not find nearby areas section in {filename}")
                continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")

if __name__ == '__main__':
    replace_nearby_areas()
