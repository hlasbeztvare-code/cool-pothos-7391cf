import re

with open('scripts.js', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace all instances of tw-text in the product wrapper generation
# where it's unsafe (contains HTML tags).

# Unsafe:
# '<div class="product-detail-price-wrap tw-text" id="detail-price">' + initialPriceText + '</div>' -> safe, text only
# '<div class="editorial-content tw-text" style="font-size: 16px; line-height: 1.6; opacity: 0.8;">' -> unsafe, product.description contains HTML
# '<ul class="premium-specs-list tw-text">' -> unsafe, contains li/span/strong
# '<span class="product-option-label tw-text">Volba verze / efektu:</span>' -> safe, text only
# '<span class="product-option-label tw-text">Velikost (průměr závitu objektivu):</span>' -> safe, text only

content = content.replace('<div class="editorial-content tw-text"', '<div class="editorial-content"')
content = content.replace('<ul class="premium-specs-list tw-text">', '<ul class="premium-specs-list">')

with open('scripts.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed unsafe tw-text classes from scripts.js")
