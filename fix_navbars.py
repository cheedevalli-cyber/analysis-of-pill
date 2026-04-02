import os
import re

# Directory containing templates
template_dir = r"c:\Users\kukka\Desktop\Detection_and_Analysis_of_Pill\templates"

# Slicknav-compatible navbar structure
def get_navbar(app_type, active_page):
    links = []
    if app_type == 'public':
        links = [
            ('Home', "{% url 'index' %}", active_page == 'home'),
            ('Login', "{% url 'loginForm' %}", active_page == 'login'),
            ('Register', "{% url 'userRegisterForm' %}", active_page == 'register'),
        ]
        brand_text = "Reliable & Accurate Identification"
    elif app_type == 'user':
        links = [
            ('Home', "{% url 'userHome' %}", active_page == 'home'),
            ('Prediction', "{% url 'prediction' %}", active_page == 'prediction'),
            ('Classification View', "{% url 'classificationView' %}", active_page == 'classification'),
            ('Logout', "{% url 'index' %}", False),
        ]
        brand_text = "Reliable & Accurate Identification"
    elif app_type == 'admin':
        links = [
            ('Home', "{% url 'adminHome' %}", active_page == 'home'),
            ('User Details', "{% url 'userDetails' %}", active_page == 'users'),
            ('Classification View', "{% url 'adminclassificationView' %}", active_page == 'classification'),
            ('Logout', "{% url 'index' %}", False),
        ]
        brand_text = "Reliable Identification"

    links_html = ""
    for name, url, active in links:
        active_class = ' class="active"' if active else ''
        links_html += f'                                        <li{active_class}><a href="{url}" style="color: #fff; font-weight: 600; text-transform: uppercase;">{name}</a></li>\n'

    return f"""        <!-- Bottom Header / Menu with Black Background -->
        <style>
            @media (min-width: 768px) {{
                .custom-desktop-menu {{ display: flex !important; list-style: none; margin: 0; padding: 0; gap: 20px; justify-content: flex-end; align-items: center; }}
                .custom-main-menu-wrapper {{ display: block !important; }}
                .mobile-nav-wrapper {{ display: none !important; }}
            }}
            @media (max-width: 767px) {{
                .custom-main-menu-wrapper {{ display: none !important; }}
                .mobile-nav-wrapper {{ display: block !important; }}
            }}
        </style>
        <div class="header_bottom" style="background: #1a1a1a; padding: 15px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div class="container">
                <div class="inner">
                    <div class="row align-items-center">
                        <div class="col-lg-4 col-md-3 col-sm-12 col-12">
                            <!-- Logo / Brand -->
                            <div class="navbar-brand">
                                <h2 style="color: #00e5ff; font-size: 1.6rem; font-weight: 700; margin: 0; letter-spacing: 1px;">{brand_text}</h2>
                            </div>
                            <!-- Mobile Nav -->
                            <div class="mobile-nav mobile-nav-wrapper"></div>
                            <!-- End Mobile Nav -->
                        </div>
                        <div class="col-lg-8 col-md-9 col-sm-12 col-12">
                            <!-- Main Menu -->
                            <div class="main-menu custom-main-menu-wrapper">
                                <nav class="navigation">
                                    <ul class="nav menu custom-desktop-menu">
{links_html.rstrip()}
                                    </ul>
                                </nav>
                            </div>
                            <!--/ End Main Menu -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>"""

# Map files to their types and active pages
file_map = {
    'index.html': ('public', 'home'),
    'login.html': ('public', 'login'),
    'register.html': ('public', 'register'),
    'base.html': ('public', 'home'),
    'users/userHome.html': ('user', 'home'),
    'users/classificationView.html': ('user', 'classification'),
    'users/predictionForm.html': ('user', 'prediction'),
    'admin/adminHome.html': ('admin', 'home'),
    'admin/userDetails.html': ('admin', 'users'),
    'admin/adminClassificationView.html': ('admin', 'classification'),
}

for rel_path, (app_type, active_page) in file_map.items():
    full_path = os.path.join(template_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"Skipping {rel_path} - Not found")
        continue

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the entire header_bottom div and the closing header tag
    # This is more robust than exact string matching
    pattern = re.compile(r'<!-- Bottom Header / Menu.*?class="header_bottom".*?header_bottom".*?</header>', re.DOTALL)
    
    # Also handle the cases where ID might be different or missing
    if not pattern.search(content):
        pattern = re.compile(r'<div class="header_bottom".*?</header>', re.DOTALL)

    new_nav = get_navbar(app_type, active_page)
    
    if pattern.search(content):
        new_content = pattern.sub(new_nav, content)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {rel_path}")
    else:
        print(f"Could not find navbar pattern in {rel_path}")

print("Done.")
