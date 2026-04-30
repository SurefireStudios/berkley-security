import os
import glob
import re

def apply_full_coverage():
    base_dir = r"c:\Users\Haz\Desktop\Berkley Security"
    locations_path = os.path.join(base_dir, "locations.html")

    with open(locations_path, 'r', encoding='utf-8') as f:
        locations_content = f.read()

    # Extract the block from locations.html. It's the section with class="py-16 lg:py-20 bg-navy text-white"
    # that contains "Mississippi" and "Louisiana"
    match = re.search(r'(<section[^>]*bg-navy text-white[^>]*>[\s\S]*?Louisiana[\s\S]*?</section>)', locations_content)
    if not match:
        print("Could not find the coverage block in locations.html")
        return
        
    original_locations_block = match.group(1)
    
    # Check if it already has id="service-areas"
    if 'id="service-areas"' not in original_locations_block:
        base_service_block = original_locations_block.replace('<section', '<section id="service-areas"', 1)
        # Update locations.html
        locations_content = locations_content.replace(original_locations_block, base_service_block)
        with open(locations_path, 'w', encoding='utf-8') as f:
            f.write(locations_content)
    else:
        base_service_block = original_locations_block

    # Create the block for city/ pages
    city_service_block = base_service_block.replace('href="city/', 'href="')

    # Update root HTML files
    root_files = glob.glob(os.path.join(base_dir, "*.html"))
    for file in root_files:
        if file == locations_path:
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content, count = re.subn(r'<section[^>]*id="service-areas"[^>]*>[\s\S]*?</section>', lambda m: base_service_block, content)
        if count > 0:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(file)}")

    # Update city/ HTML files
    city_files = glob.glob(os.path.join(base_dir, "city", "*.html"))
    for file in city_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content, count = re.subn(r'<section[^>]*id="service-areas"[^>]*>[\s\S]*?</section>', lambda m: city_service_block, content)
        if count > 0:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(file)}")
            
    # Update scratch/template.html
    template_path = os.path.join(base_dir, "scratch", "template.html")
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content, count = re.subn(r'<section[^>]*id="service-areas"[^>]*>[\s\S]*?</section>', lambda m: base_service_block, content) # template expects the full base block, because update_cities replaces it
        if count > 0:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated template.html")

if __name__ == '__main__':
    apply_full_coverage()
