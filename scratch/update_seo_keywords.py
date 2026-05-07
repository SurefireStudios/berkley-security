import os
import re

CITY_DIR = r"c:\Users\Haz\Desktop\Berkley Security\city"

# The keywords the client wants:
# Security Systems, Security Alarms, Camera Systems, Security Cameras, Alarm Systems, Fire Systems, Medical Alerts

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract City from the Title tag: <title>Security Systems in Madison, MS | Berkley Security</title>
    title_match = re.search(r'<title>.*? in (.*?), (MS|LA).*?</title>', content)
    if not title_match:
        print(f"Skipping {filepath} - could not find city in title.")
        return
    
    city = title_match.group(1)

    # 1. Update Meta Description
    new_desc = f"Top-rated security systems &amp; security cameras. {city}&apos;s trusted security provider since 1978. Custom alarm systems, fire systems &amp; medical alerts."
    
    # Replace name="description"
    content = re.sub(
        r'<meta content="[^"]*" name="description"\s*/>',
        f'<meta content="{new_desc}" name="description"/>',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace property="og:description"
    content = re.sub(
        r'<meta content="[^"]*" property="og:description"\s*/>',
        f'<meta content="{new_desc}" property="og:description"/>',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace name="twitter:description"
    content = re.sub(
        r'<meta content="[^"]*" name="twitter:description"\s*/>',
        f'<meta content="{new_desc}" name="twitter:description"/>',
        content,
        flags=re.IGNORECASE
    )

    # 2. Update Hero Paragraph
    # Find the H1 tag and the following paragraph
    # <h1 ...>...</h1>\n<p class="text-xl md:text-2xl text-gray-300 mb-8">...</p>
    
    hero_p_pattern = r'(<h1[^>]*>.*?</h1>\s*)<p class="text-xl md:text-2xl text-gray-300 mb-8">.*?</p>'
    
    new_hero_p = f'<p class="text-xl md:text-2xl text-gray-300 mb-8">Safeguard your {city} property with advanced <strong>security systems</strong> and <strong>security cameras</strong>. As {city}&apos;s trusted security provider since 1978, we install custom <strong>security alarms</strong>, high-definition <strong>camera systems</strong>, commercial <strong>fire systems</strong>, and reliable <strong>medical alerts</strong>. Experience complete protection with our 24/7 monitored <strong>alarm systems</strong> for homes and businesses.</p>'
    
    content = re.sub(hero_p_pattern, r'\1' + new_hero_p, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {os.path.basename(filepath)}")

def main():
    count = 0
    for filename in os.listdir(CITY_DIR):
        if filename.endswith(".html"):
            filepath = os.path.join(CITY_DIR, filename)
            process_html_file(filepath)
            count += 1
    print(f"Successfully processed {count} files.")

if __name__ == "__main__":
    main()
