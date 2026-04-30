import os
import urllib.parse
from bs4 import BeautifulSoup

base_dir = r'c:\Users\Haz\Desktop\Berkley Security\city'
cities = [f for f in os.listdir(base_dir) if f.endswith('.html')]

print(f'Starting map injection for {len(cities)} files...')

for filename in cities:
    file_path = os.path.join(base_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check if map already exists
    if soup.find('section', class_='w-full h-64 md:h-80 lg:h-96'):
        if filename != 'edwards-ms.html':
            pass
        else:
            # We skip edwards since we just did it
            continue
            
    # Extract data
    title_tag = soup.find('title')
    title_text = title_tag.text if title_tag else ''
    city = 'Your City'
    if ' in ' in title_text:
        city = title_text.split(' in ')[1].split(',')[0].strip()
        
    state = 'MS' if '-ms' in filename else 'LA'
    
    query = f"{city}, {state}"
    encoded_query = urllib.parse.quote_plus(query)
    
    map_html = f"""
<!-- Location Map -->
<section class="w-full h-64 md:h-80 lg:h-96">
<iframe allowfullscreen="" height="100%" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={encoded_query}&amp;t=&amp;z=12&amp;ie=UTF8&amp;iwloc=&amp;output=embed" style="border:0;" width="100%"></iframe>
</section>
"""
    
    map_soup = BeautifulSoup(map_html, 'html.parser')
    
    main_tag = soup.find('main')
    if main_tag:
        main_tag.append(map_soup)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

print('Done injecting maps.')
