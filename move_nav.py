import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# We want to find the <nav class="desktop-nav">...</nav> inside the <header>
# and move it right after the <body> tag or outside the header.
nav_pattern = re.compile(r'(<nav class="desktop-nav".*?</nav>)', re.DOTALL)
header_pattern = re.compile(r'(<header class="main-header".*?>)', re.DOTALL)

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # If desktop-nav is found
    match = nav_pattern.search(content)
    if match:
        nav_html = match.group(1)
        
        # Check if nav is currently inside header
        # Actually, let's just remove it from its current position
        new_content = content.replace(nav_html, '')
        
        # And place it right before the </header> ? No, outside the header completely.
        # Let's place it right before the <header class="main-header"
        new_content = new_content.replace('<header class="main-header"', nav_html + '\n    <header class="main-header"', 1)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Moved nav in {file}")
