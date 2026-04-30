import os
import re
import json
from bs4 import BeautifulSoup

def process_city_file(filepath, template_content):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract json-ld
    scripts = soup.find_all('script', type='application/ld+json')
    json_ld_local = None
    for script in scripts:
        if script.string:
            try:
                data = json.loads(script.string)
                if data.get('@type') == 'LocalBusiness':
                    json_ld_local = data
            except json.JSONDecodeError:
                pass
    
    if not json_ld_local:
        print(f"Skipping {filepath} - no LocalBusiness JSON-LD found.")
        return

    city = json_ld_local.get('address', {}).get('addressLocality', '')
    state = json_ld_local.get('address', {}).get('addressRegion', '')
    zipcode = json_ld_local.get('address', {}).get('postalCode', '')
    
    state_full = "Louisiana" if state == "LA" else "Mississippi" if state == "MS" else state
    
    # Extract county/parish from keywords or description
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    
    keywords = meta_keywords['content'] if meta_keywords and 'content' in meta_keywords.attrs else ''
    desc = meta_desc['content'] if meta_desc and 'content' in meta_desc.attrs else ''
    
    # Look for "County" or "Parish" in text
    county_match = re.search(r'([A-Za-z\s]+ (County|Parish))', keywords + " " + desc + " " + json.dumps(json_ld_local.get('areaServed', [])))
    county = county_match.group(1).strip() if county_match else ("County" if state == "MS" else "Parish")
    
    filename = os.path.basename(filepath)
    city_slug = filename.replace('.html', '')
    
    # Create the new JSON LD local business block nicely formatted
    # Update areaServed if it doesn't have the county
    area_served = json_ld_local.get('areaServed', [])
    if isinstance(area_served, list) and county not in area_served:
        if city not in area_served:
            area_served.insert(0, city)
        if county not in area_served:
            area_served.append(county)
        json_ld_local['areaServed'] = area_served
    
    json_ld_local_str = json.dumps(json_ld_local, indent=2)
    
    # Build FAQ JSON
    faq_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"How much does a security system cost in {city}, {state}?",
                "acceptedAnswer": { "@type": "Answer", "text": f"Security system costs in {city} typically range from $199 to $1,500+ depending on the size of your property and the features you need. A basic home alarm with door/window sensors and a keypad is on the lower end, while a full system with HD cameras covering a large commercial property falls on the higher end. Berkley Security offers free on-site assessments and custom quotes so you only pay for what your property actually needs. Flexible financing is available." }
            },
            {
                "@type": "Question",
                "name": f"What is the best security company in {city}, {state_full}?",
                "acceptedAnswer": { "@type": "Answer", "text": f"Berkley Security has been the most trusted security provider since 1978. Unlike national chains that push cookie-cutter packages, we custom-design every system for your specific property. Our technicians are fully licensed and understand the unique security needs of {city}'s diverse neighborhoods and properties." }
            },
            {
                "@type": "Question",
                "name": f"Does Berkley serve businesses in {city}?",
                "acceptedAnswer": { "@type": "Answer", "text": f"Yes. We design and install commercial security systems for {city} businesses of all sizes. This includes retail stores, medical facilities, restaurants, offices, warehouses, churches, and industrial sites throughout {county}. Our commercial solutions include access control, multi-camera surveillance, intrusion detection, and fire alarm systems." }
            },
            {
                "@type": "Question",
                "name": f"Does Berkley Security offer 24/7 monitoring in {city}?",
                "acceptedAnswer": { "@type": "Answer", "text": f"Yes. Berkley Security provides 24/7 professional monitoring for all alarm and fire systems in {city}. When your alarm is triggered, our monitoring center immediately verifies the event and dispatches local police, sheriff, or fire department as needed. We also provide 24/7 emergency service for system issues outside normal business hours." }
            },
            {
                "@type": "Question",
                "name": f"Can I view my {city} security cameras from my phone?",
                "acceptedAnswer": { "@type": "Answer", "text": f"Absolutely. All of our video surveillance systems include remote viewing through a free mobile app. You can watch live camera feeds from your {city} home or business, review recorded footage, and receive instant motion alerts directly on your smartphone from anywhere in the world. We offer both cloud-based and local NVR storage options depending on your preference." }
            },
            {
                "@type": "Question",
                "name": f"How long does security installation take in {city}?",
                "acceptedAnswer": { "@type": "Answer", "text": f"Most residential security system installations in {city} are completed in a single day, typically within 3 to 6 hours. Larger commercial installations for medical offices, retail centers, or multi-camera warehouse setups may require 2 to 3 days. Our licensed technicians handle everything from the initial assessment through installation and hands-on system training." }
            },
            {
                "@type": "Question",
                "name": f"Is Berkley Security licensed in {state_full}?",
                "acceptedAnswer": { "@type": "Answer", "text": f"Yes. Berkley Security is fully licensed in both Louisiana and Mississippi. Every technician is background-checked, insured, and highly trained. We have been serving communities since 1978, and {city} is a core part of our service area in {county}." }
            }
        ]
    }
    json_ld_faq_str = json.dumps(faq_json, indent=2)
    
    new_html = template_content
    new_html = new_html.replace('{CITY}', city)
    new_html = new_html.replace('{STATE}', state)
    new_html = new_html.replace('{STATEFULL}', state_full)
    new_html = new_html.replace('{COUNTY}', county)
    new_html = new_html.replace('{ZIPCODE}', zipcode)
    new_html = new_html.replace('{CITY_SLUG}', city_slug)
    new_html = new_html.replace('{JSON_LD_LOCAL}', json_ld_local_str)
    new_html = new_html.replace('{JSON_LD_FAQ}', json_ld_faq_str)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Successfully processed {filename} (City: {city}, County: {county})")

if __name__ == '__main__':
    base_dir = r"c:\Users\Haz\Desktop\Berkley Security\city"
    template_path = r"c:\Users\Haz\Desktop\Berkley Security\scratch\template.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
        
    files_to_process = [
        "wesson-ms.html", "waynesboro-ms.html", "forest-ms.html", "urania-la.html",
        "tullos-la.html", "prentiss-ms.html", "philadelphia-ms.html", "newton-ms.html",
        "mer-rouge-la.html", "batesville-ms.html", "olla-la.html", "oak-grove-la.html",
        "morton-ms.html", "monticello-ms.html", "new-roads-la.html"
    ]
    
    for filename in files_to_process:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            process_city_file(filepath, template_content)
        else:
            print(f"File not found: {filepath}")
