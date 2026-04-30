import os

def fix_county_newellton():
    filepath = r"c:\Users\Haz\Desktop\Berkley Security\city\newellton-la.html"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("company Tensas Parish", "Tensas Parish")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_county_newellton()
