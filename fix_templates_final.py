import os
import re

template_dir = r"c:\Users\kukka\Desktop\Detection_and_Analysis_of_Pill\templates"

def update_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    
    # 1. Ensure {% load static %} is at the top
    if '{% load static %}' not in content:
        content = '{% load static %}\n' + content
        modified = True

    # 2. Fix JS references: main.js -> custom.js and ensure {% static %}
    # We also check for jquery, slicknav, etc.
    scripts = {
        'js/jquery.min.js': 'js/jquery-3.3.1.min.js',
        'js/main.js': 'js/custom.js',
        'js/custom.js': 'js/custom.js',
    }
    
    for old, new in scripts.items():
        # Match both raw src="img/..." and existing {% static %} with wrong names
        pattern = re.compile(rf'src="([^"]*{old}[^"]*)"')
        if pattern.search(content):
            content = pattern.sub(f'src="{{% static \'{new}\' %}}"', content)
            modified = True
            
    # 3. Fix pill-identification image
    pill_pattern = re.compile(r"pill-identification1\.jpg\.jpg")
    if pill_pattern.search(content):
        content = pill_pattern.sub("pill-1.jpg", content)
        modified = True

    # 4. Wrap all raw image sources in static tag
    # src="img/..." -> src="{% static 'img/...' %}"
    img_pattern = re.compile(r'src="img/([^"]+)"')
    if img_pattern.search(content):
        content = img_pattern.sub(r'src="{% static \'img/\1\' %}"', content)
        modified = True

    # 5. Fix Slicknav structure (Double check)
    # Ensure <div class="mobile-nav"></div> is present if not already
    if 'header_bottom' in content and 'mobile-nav' not in content:
        # Insert before .main-menu or after .navbar-brand
        content = content.replace('<div class="navbar-brand">', '<div class="navbar-brand">\n                            <div class="mobile-nav"></div>')
        modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")

# Run on all templates
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            update_template(os.path.join(root, file))

print("Template fixing finished.")
