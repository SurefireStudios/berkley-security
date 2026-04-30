import os
import glob
import re

def fix_image_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace object-cover with object-contain for the city image.
    # The image is usually <img src="../src/img/cities/... " class="absolute inset-0 w-full h-full object-cover"...>
    # Wait, some might just be <img src="..." class="w-full h-full object-cover"...>
    
    # Let's replace 'object-cover' with 'object-contain' on any img that has src="../src/img/cities/"
    def replace_cover(match):
        img_tag = match.group(0)
        new_tag = img_tag.replace('object-cover', 'object-contain')
        return new_tag

    content = re.sub(r'<img[^>]+src="\.\./src/img/cities/[^>]+>', replace_cover, content)
    
    # We also want to remove shadow from the container.
    # The container usually looks like: <div class="fade-up relative ... shadow-2xl"> or <div class="... rounded-2xl overflow-hidden shadow-2xl">
    # We can regex for any div that contains the img, but an easier way is to just look for the typical container classes
    # e.g. "rounded-2xl overflow-hidden shadow-2xl" -> "rounded-2xl overflow-hidden"
    
    content = content.replace('overflow-hidden shadow-2xl', 'overflow-hidden')
    content = content.replace('overflow-hidden shadow-xl', 'overflow-hidden')
    content = content.replace('overflow-hidden shadow-lg', 'overflow-hidden')
    content = content.replace('overflow-hidden shadow-md', 'overflow-hidden')
    content = content.replace('overflow-hidden shadow', 'overflow-hidden')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    base_dir = r"c:\Users\Haz\Desktop\Berkley Security\city"
    for filepath in glob.glob(os.path.join(base_dir, "*.html")):
        fix_image_in_file(filepath)
        print(f"Processed {os.path.basename(filepath)}")
