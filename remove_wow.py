import re

# 1. Revert index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Tomb Darkness & Loupe
html = re.sub(r'<!-- ── ULTIMATE WOW: TOMB FLASHLIGHT & OPTICAL LOUPE ── -->.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<div id="tomb-darkness"></div>\s*<div id="optical-loupe">.*?</div>', '', html, flags=re.DOTALL)

# Remove Exploded Section
html = re.sub(r'<!-- ── APPLE EXPLODED VIEW SECTION ── -->.*?</section>', '', html, flags=re.DOTALL)

# Remove Tomb Entrance Overlay
html = re.sub(r'<div id="tomb-entrance-overlay">.*?</div>\s*</div>', '', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Revert styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'/\* ── ULTIMATE WOW: TOMB FLASHLIGHT & LOUPE ── \*/.*', '', css, flags=re.DOTALL)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Revert scripts.js
with open('scripts.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r'// ── ULTIMATE WOW: COMBINED LOGIC ──.*', '', js, flags=re.DOTALL)

with open('scripts.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Reverted WOW effects.")
