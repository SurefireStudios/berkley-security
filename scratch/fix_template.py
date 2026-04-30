import re

def fix_template():
    with open('locations.html', 'r', encoding='utf-8') as f:
        locations = f.read()
        
    match = re.search(r'(<section[^>]*id="service-areas"[^>]*>[\s\S]*?</section>)', locations)
    if not match:
        print("Could not find base block")
        return
        
    base_block = match.group(1)
    
    with open('scratch/template.html', 'r', encoding='utf-8') as f:
        template = f.read()
        
    new_template, count = re.subn(r'<!-- NEARBY AREAS[\s\S]*?<section[^>]*>[\s\S]*?</section>', base_block, template)
    if count == 0:
        # Also try to match the section by id
        new_template, count = re.subn(r'<section[^>]*id="service-areas"[^>]*>[\s\S]*?</section>', base_block, template)
        
    with open('scratch/template.html', 'w', encoding='utf-8') as f:
        f.write(new_template)
        
    print("Fixed template")

if __name__ == '__main__':
    fix_template()
