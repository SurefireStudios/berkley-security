import os
import re

workspace = r"C:\Users\Haz\Desktop\Berkley Security"
base_url = "https://berkleysecurity.com"
default_image = f"{base_url}/src/img/Berkley-Security-Logo.png"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if head not found
    if '<head>' not in content.lower() or '</head>' not in content.lower():
        return

    # Extract existing title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    existing_title = title_match.group(1).strip() if title_match else "Berkley Security Inc."

    # Decide on real title
    is_blog = 'blog\\' in filepath.lower() or 'blog/' in filepath.lower()
    is_blog_index = 'blog.html' in filepath.lower()
    
    if is_blog and not is_blog_index:
        # Extract h1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            real_title = h1_match.group(1).strip()
            # Clean up the h1 if it has span tags inside
            real_title = re.sub(r'<[^>]+>', '', real_title)
            
            new_title_tag = f"<title>{real_title} | Berkley Security Inc.</title>"
            if title_match:
                content = content[:title_match.start()] + new_title_tag + content[title_match.end():]
            else:
                content = content.replace('</head>', f"  {new_title_tag}\n</head>")
            og_title = real_title
        else:
            og_title = existing_title.replace(' | Berkley Security Inc.', '')
    else:
        og_title = existing_title.split(' | ')[0]

    # Clean existing og: and twitter: tags to prevent duplicates
    content = re.sub(r'\s*<meta\s+property=["\']og:.*?["\'][^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*<meta\s+name=["\']twitter:.*?["\'][^>]*>', '', content, flags=re.IGNORECASE)

    # Extract description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', content, re.IGNORECASE | re.DOTALL)
    if not desc_match:
         desc_match = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']\s*/?>', content, re.IGNORECASE | re.DOTALL)
         
    if desc_match:
        desc = desc_match.group(1).strip()
    else:
        # Fallback to first p tag
        p_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        if p_match:
             desc = re.sub(r'<[^>]+>', '', p_match.group(1).strip())[:150] + "..."
        else:
             desc = "Berkley Security Inc. providing excellent service."

    # URL
    rel_path = os.path.relpath(filepath, workspace).replace('\\', '/')
    if rel_path == 'index.html':
        url = f"{base_url}/"
    else:
        url = f"{base_url}/{rel_path}"

    type_str = "article" if (is_blog and not is_blog_index) else "website"

    tags = f"""
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="{type_str}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{default_image}">
  <meta property="og:site_name" content="Berkley Security Inc.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{default_image}">
"""
    content = content.replace("</head>", f"{tags}</head>")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

count = 0
for root, dirs, files in os.walk(workspace):
    if '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))
            count += 1
print(f"Processed {count} files.")
