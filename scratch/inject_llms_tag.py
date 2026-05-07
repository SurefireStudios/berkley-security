import os
import glob

# Paths to process
workspace_dir = r"c:\Users\Haz\Desktop\Berkley Security"
city_dir = os.path.join(workspace_dir, "city")

# Get all HTML files in root and city dir
html_files = glob.glob(os.path.join(workspace_dir, "*.html"))
html_files.extend(glob.glob(os.path.join(city_dir, "*.html")))

tag_to_inject = '<link href="/llms.txt" rel="llms-txt"/>'

updated_count = 0
already_present_count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'rel="llms-txt"' in content:
        already_present_count += 1
        continue # Already injected
        
    # Find the closing </head> tag and insert right before it
    if '</head>' in content:
        content = content.replace('</head>', f'{tag_to_inject}\n</head>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1

print(f"Successfully injected llms.txt link into {updated_count} files.")
if already_present_count > 0:
    print(f"Skipped {already_present_count} files that already had the tag.")
