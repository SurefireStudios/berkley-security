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

    # Find the section using regex to keep the exact formatting
    match = re.search(r'(<!-- Areas We Serve Section -->[\s\S]*?<section id="service-areas"[\s\S]*?</section>)', index_content)
    if not match:
        print("Could not find service-areas in index.html")
        return
        
    service_areas_block = match.group(1)
    
    # Replace city/xxx.html with xxx.html
    service_areas_block = service_areas_block.replace('href="city/', 'href="')
    
    # Also adjust the id to maybe remove <!-- Areas We Serve Section -->
    # Actually it's fine. 

    # Loop over all city html files
    for filepath in glob.glob(os.path.join(city_dir, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Try to find the section to replace
        # It typically contains an h2 with "Serving [City] & Surrounding Areas" or "Communities"
        # Let's find the section that matches this.
        
        # We can look for <section ...>...Serving...Areas... </section> or ...Communities...
        # Wait, the newly created 15 pages have: <!-- NEARBY AREAS - Updated to link to general locations -->
        
        # Regex to find the nearby areas section:
        # It can be <!-- NEARBY AREAS... -->\n<section...>...Serving...</section>
        # Or just <section...>...Serving...Areas...</section>
        
        def replace_func(m):
            return service_areas_block
            
        new_content, count = re.subn(r'<!-- NEARBY AREAS[\s\S]*?<section[^>]*>[\s\S]*?Serving[\s\S]*?(?:Areas|Communities)[\s\S]*?</section>', replace_func, content, count=1)
        
        if count == 0:
            new_content, count = re.subn(r'<section[^>]*>[\s\S]*?<h2[^>]*>Serving[\s\S]*?(?:Areas|Communities)[\s\S]*?</section>', replace_func, content, count=1)
            
        if count == 0:
            print(f"Could not find nearby areas section in {os.path.basename(filepath)}")
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(filepath)}")

if __name__ == '__main__':
    replace_nearby_areas()
