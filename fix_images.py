import os
import re

template_dir = r"c:\Users\kukka\Desktop\Detection_and_Analysis_of_Pill\templates"
img_dir = r"c:\Users\kukka\Desktop\Detection_and_Analysis_of_Pill\templates\assets\img"

# Get all images from the filesystem
images_on_disk = os.listdir(img_dir)
image_map = {img.lower(): img for img in images_on_disk}

def fix_image_paths(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    
    # Regex to find static tags for images
    # Example: {% static 'img/Admin.jpg' %}
    static_pattern = re.compile(r"\{% static 'img/([^']+)' %\}")
    
    def replace_img(match):
        nonlocal modified
        current_name = match.group(1)
        if current_name.lower() in image_map:
            correct_name = image_map[current_name.lower()]
            if correct_name != current_name:
                modified = True
                print(f"Fixed {current_name} -> {correct_name} in {file_path}")
                return f"{{% static 'img/{correct_name}' %}}"
        return match.group(0)

    new_content = static_pattern.sub(replace_img, content)
    
    # Also handle src="img/..." if NOT in static tag (though we should ideally wrap them)
    src_pattern = re.compile(r'src="img/([^"]+)"')
    def replace_src(match):
        nonlocal modified
        name = match.group(1)
        # If it's not wrapped in static, wrap it
        if name.lower() in image_map:
            correct_name = image_map[name.lower()]
            modified = True
            print(f"Fixed and wrapped img/{name} in {file_path}")
            return f'src="{{% static \'img/{correct_name}\' %}}"'
        return match.group(0)
    
    new_content = src_pattern.sub(replace_src, new_content)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Traverse templates
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            fix_image_paths(os.path.join(root, file))

print("Image path fixing done.")
