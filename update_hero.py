import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace hero-visual with hero-artifacts-desk
hero_visual_pattern = re.compile(r'<!-- Right: Prism visual -->.*?</div>\s*</div>\s*</div>', re.DOTALL)

artifacts_html = """<!-- Right: Artifacts Desk -->
            <div class="hero-artifacts-desk reveal-up delay-1">
                <!-- Artifact 1: KALEIDOSKOP -->
                <a href="product.html?id=kaleidoscope" class="artifact-item artifact-kaledo" aria-label="Kaleidoskop filtr">
                    <img src="images/kaledo_transparent.png" alt="Kaleidoskop Filtr" class="artifact-img">
                    <div class="artifact-label">Kaleidoskop</div>
                </a>
                
                <!-- Artifact 2: FOG -->
                <a href="product.html?id=fog" class="artifact-item artifact-fog" aria-label="Fog filtr">
                    <img src="images/fog_transparent.png" alt="Fog Filtr" class="artifact-img">
                    <div class="artifact-label">Fog</div>
                </a>
                
                <!-- Artifact 3: HALO -->
                <a href="product.html?id=halo" class="artifact-item artifact-halo" aria-label="Halo filtr">
                    <img src="images/halo_transparent.png" alt="Halo Filtr" class="artifact-img">
                    <div class="artifact-label">Halo</div>
                </a>
            </div>
        </div>"""

html = hero_visual_pattern.sub(artifacts_html, html)

# Hide the Kolekce section
html = html.replace('<section class="products-section" id="kolekce">', '<section class="products-section" id="kolekce" style="display: none;">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")
