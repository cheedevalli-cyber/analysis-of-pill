import os
import re

# Directory containing templates
template_dir = r"c:\Users\kukka\Desktop\Detection_and_Analysis_of_Pill\templates"

# Responsive Native HTML/CSS/JS navbar structure
def get_navbar(app_type, active_page):
    links = []
    if app_type == 'public':
        links = [
            ('Home', "{% url 'index' %}", active_page == 'home'),
            ('Login', "{% url 'loginForm' %}", active_page == 'login'),
            ('Register', "{% url 'userRegisterForm' %}", active_page == 'register'),
        ]
        brand_text = "Accurate Identification"
    elif app_type == 'user':
        links = [
            ('Home', "{% url 'userHome' %}", active_page == 'home'),
            ('Prediction', "{% url 'prediction' %}", active_page == 'prediction'),
            ('Classification', "{% url 'classificationView' %}", active_page == 'classification'),
            ('Logout', "{% url 'index' %}", False),
        ]
        brand_text = "Accurate Identification"
    elif app_type == 'admin':
        links = [
            ('Home', "{% url 'adminHome' %}", active_page == 'home'),
            ('Users', "{% url 'userDetails' %}", active_page == 'users'),
            ('Classification', "{% url 'adminclassificationView' %}", active_page == 'classification'),
            ('Logout', "{% url 'index' %}", False),
        ]
        brand_text = "Reliable Identification"

    links_html = ""
    for name, url, active in links:
        active_class = ' class="active"' if active else ''
        links_html += f'                                        <li{active_class}><a href="{url}" style="color: #fff; font-weight: 600; text-transform: uppercase;">{name}</a></li>\n'

    mobile_links_html = ""
    for name, url, active in links:
        active_class = ' class="active"' if active else ''
        mobile_links_html += f'                                <li{active_class}><a href="{url}">{name}</a></li>\n'

    return f"""        <!-- Responsive Header Bottom -->
        <style>
            /* Desktop Menu Styles */
            @media (min-width: 768px) {{
                .custom-desktop-menu {{ display: flex !important; list-style: none; margin: 0; padding: 0; gap: 20px; justify-content: flex-end; align-items: center; }}
                .custom-main-menu-wrapper {{ display: block !important; margin-left: auto; }}
                .hamburger-btn {{ display: none !important; }}
                .mobile-dropdown-menu {{ display: none !important; }}
                .nav-header-flex {{ display: flex; align-items: center; justify-content: space-between; width: 100%; }}
            }}
            /* Mobile Menu Styles */
            @media (max-width: 767px) {{
                .custom-main-menu-wrapper {{ display: none !important; }}
                .nav-header-flex {{ display: flex; align-items: center; justify-content: space-between; width: 100%; }}
                .hamburger-btn {{ 
                    display: block !important; 
                    background: none; 
                    border: none; 
                    color: #00e5ff; 
                    font-size: 30px; 
                    cursor: pointer;
                    padding: 5px 10px;
                    border-radius: 4px;
                    border: 1px solid #00e5ff;
                }}
                .hamburger-btn:hover {{ background: rgba(0, 229, 255, 0.1); }}
                .mobile-dropdown-menu {{
                    display: none;
                    flex-direction: column;
                    background: #222;
                    width: 100%;
                    padding: 10px 0;
                    margin-top: 15px;
                    border-radius: 5px;
                }}
                .mobile-dropdown-menu.show {{ display: flex !important; }}
                .mobile-dropdown-menu li {{ list-style: none; text-align: center; padding: 12px 0; border-bottom: 1px solid #333; }}
                .mobile-dropdown-menu li:last-child {{ border-bottom: none; }}
                .mobile-dropdown-menu li a {{ color: #fff; font-weight: 600; text-transform: uppercase; display: block; text-decoration: none; letter-spacing: 1px; }}
                .mobile-dropdown-menu li a:hover {{ color: #00e5ff; }}
            }}
        </style>
        <div class="header_bottom" style="background: #1a1a1a; padding: 15px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div class="container">
                <div class="inner">
                    <div class="row align-items-center">
                        <div class="col-12 nav-header-flex">
                            <!-- Logo / Brand -->
                            <div class="navbar-brand">
                                <h2 style="color: #00e5ff; font-size: 1.4rem; font-weight: 700; margin: 0; letter-spacing: 1px;">{brand_text}</h2>
                            </div>
                            
                            <!-- Main Menu (Desktop) -->
                            <div class="main-menu custom-main-menu-wrapper">
                                <nav class="navigation">
                                    <ul class="nav menu custom-desktop-menu">
{links_html.rstrip()}
                                    </ul>
                                </nav>
                            </div>

                            <!-- Hamburger Icon (Mobile) -->
                            <button class="hamburger-btn" onclick="toggleMobileMenu()">&#9776;</button>
                        </div>
                        
                        <!-- Mobile Dropdown Menu -->
                        <div class="col-12">
                            <ul class="mobile-dropdown-menu" id="mobileMenu">
{mobile_links_html.rstrip()}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            function toggleMobileMenu() {{
                var menu = document.getElementById("mobileMenu");
                if (menu.classList.contains("show")) {{
                    menu.classList.remove("show");
                }} else {{
                    menu.classList.add("show");
                }}
            }}
        </script>
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
        print(f"Skipping {{rel_path}} - Not found")
        continue

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the entire header_bottom div and the closing header tag
    pattern = re.compile(r'<!-- Bottom Header / Menu.*?class="header_bottom".*?header_bottom".*?</header>|<!-- Responsive Header Bottom -->.*?</header>|<div class="header_bottom".*?</header>', re.DOTALL)

    new_nav = get_navbar(app_type, active_page)
    
    if pattern.search(content):
        new_content = pattern.sub(new_nav, content)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {{rel_path}}")
    else:
        print(f"Could not find navbar pattern in {{rel_path}}")

print("Responsive templates updating finished.")
