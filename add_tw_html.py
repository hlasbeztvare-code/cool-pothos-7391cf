import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add tw-text to hero-title and subtitle
html = html.replace('class="hero-title"', 'class="hero-title tw-text"')
html = html.replace('class="hero-subtitle"', 'class="hero-subtitle tw-text"')

# Add tw-text to accordion
html = html.replace('<h3>Kaleidoskop</h3>', '<h3 class="tw-text">Kaleidoskop</h3>')
html = html.replace('<h3>Fog</h3>', '<h3 class="tw-text">Fog</h3>')
html = html.replace('<h3>Halo</h3>', '<h3 class="tw-text">Halo</h3>')
html = html.replace('<p>Geometrická exploze', '<p class="tw-text">Geometrická exploze')
html = html.replace('<p>Zjemněte kontrast', '<p class="tw-text">Zjemněte kontrast')
html = html.replace('<p>Magický prstenec', '<p class="tw-text">Magický prstenec')

# Add tw-text to about
html = html.replace('class="about-title"', 'class="about-title tw-text"')
html = html.replace('<p>Fotofiltry.cz vznikly', '<p class="tw-text">Fotofiltry.cz vznikly')
html = html.replace('<p>Naším cílem není sterilní', '<p class="tw-text">Naším cílem není sterilní')
html = html.replace('<p><strong>Světlo je všechno.</strong>', '<p class="tw-text"><strong>Světlo je všechno.</strong>')

# Add tw-text to section titles
html = html.replace('class="section-title"', 'class="section-title tw-text"')
html = html.replace('class="section-subtitle"', 'class="section-subtitle tw-text"')

# Add tw-text to contact
html = html.replace('class="contact-title"', 'class="contact-title tw-text"')
html = html.replace('class="contact-desc"', 'class="contact-desc tw-text"')


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("tw-text classes added to index.html")
