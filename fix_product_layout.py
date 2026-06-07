import re

with open('scripts.js', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to change how wrapper.innerHTML is built.
# I will replace the large wrapper.innerHTML assignment with a new one.

old_html_start = "        // Vložení kompletního HTML\n        wrapper.innerHTML ="
# Let's find the end of the innerHTML assignment. It ends with:
#             '</div>' +
#             '</div>';
# Because after sizes HTML there is a buy block and closing divs.
# I will just write a regex to replace everything from "wrapper.innerHTML =" up to the end of the function renderProductDetail(product)

# Let's use string operations instead.
split1 = content.split("        // Vložení kompletního HTML\n        wrapper.innerHTML =\n")
if len(split1) > 1:
    before = split1[0]
    rest = split1[1]
    
    # We want to replace the rest until `        // 1) Hlavní obrázek switch`
    split2 = rest.split("        // 1) Hlavní obrázek switch\n")
    if len(split2) > 1:
        after = "        // 1) Hlavní obrázek switch\n" + split2[1]
        
        new_html = """            '<!-- Left Visual Gallery -->' +
            '<div class="product-detail-visual" style="max-width: 400px; margin: 0 auto;">' +
            '<div class="product-detail-main-image-wrap">' +
            '<img src="' + activeImage + '" alt="' + product.name + '" class="product-detail-main-img" id="main-detail-img" fetchpriority="high">' +
            '</div>' +
            '<div class="product-detail-thumbs" id="detail-thumbs-container">' +
            thumbsHtml +
            '</div>' +
            '</div>' +

            '<!-- Right Info Block -->' +
            '<div class="product-detail-info">' +
            '<div class="product-detail-badge tw-text">Prémiová kvalita</div>' +
            '<span class="product-detail-category tw-text">Optické fotografické filtry</span>' +
            '<h1 class="product-detail-title tw-text">' + product.name + '</h1>' +
            '<div class="product-detail-price-wrap tw-text" id="detail-price">' + initialPriceText + '</div>' +

            '<!-- Premium Editorial Section (Description typing out) -->' +
            '<div class="premium-editorial-section">' +
            '<div class="editorial-block">' +
            '<h3 class="editorial-title tw-text">Příběh produktu</h3>' +
            '<div class="editorial-content tw-text">' + product.description + '</div>' +
            '</div>' +
            '<div class="editorial-block">' +
            '<h3 class="editorial-title tw-text">Technická specifikace</h3>' +
            '<ul class="premium-specs-list tw-text">' +
            '<li><span>Optické sklo</span><strong>Schott B270 (vysoká propustnost)</strong></li>' +
            '<li><span>Konstrukce</span><strong>Slim hliníková slitina, anodizováno</strong></li>' +
            '<li><span>Mechanika</span><strong>Otočná obroučka pro plynulé natáčení</strong></li>' +
            '<li><span>Závit</span><strong>Standardní vnitřní fotografický</strong></li>' +
            '</ul>' +
            '</div>' +
            '<div class="editorial-block shipping-block tw-text">' +
            '<h3 class="editorial-title">Doprava a servis</h3>' +
            '<p>Každý filtr je ručně kontrolován před odesláním. Odesíláme expresně přes Zásilkovnu. <strong>Doprava zdarma nad 2 000 Kč.</strong> Součástí je prémiové balení a dvouletá záruka.</p>' +
            '</div>' +
            '</div>' +

            '<!-- Variant Selection -->' +
            (product.variants && product.variants.length > 0 ?
                '<div class="product-option-group">' +
                '<span class="product-option-label">Volba verze / efektu:</span>' +
                '<div class="product-variant-pills" id="detail-variants-container">' +
                variantsHtml +
                '</div>' +
                '</div>' : '') +

            '<!-- Size Selection -->' +
            (product.sizes && product.sizes.length > 0 ?
                '<div class="product-option-group">' +
                '<div class="product-option-header">' +
                '<span class="product-option-label">Velikost závitu:</span>' +
                '<a href="#" class="size-guide-link">Jak zjistit velikost?</a>' +
                '</div>' +
                '<div class="product-size-grid" id="detail-sizes-container">' +
                sizesHtml +
                '</div>' +
                '</div>' : '') +

            '<!-- Buy Block -->' +
            '<div class="product-buy-block">' +
            '<div class="quantity-selector">' +
            '<button class="qty-btn" id="qty-minus">-</button>' +
            '<input type="number" id="qty-input" value="1" min="1" max="10" readonly>' +
            '<button class="qty-btn" id="qty-plus">+</button>' +
            '</div>' +
            '<button class="add-to-cart-btn large-btn" id="detail-add-cart" ' +
            (selectedSizeObj.stock === 0 ? 'disabled' : '') + '>' +
            (selectedSizeObj.stock === 0 ? 'Vyprodáno' : 'Přidat do košíku') +
            '</button>' +
            '</div>' +
            '<div class="stock-status-label ' + initialStockClass + '" id="detail-stock-status">' + initialStockLabel + '</div>' +
            '</div>';

        // Spuštění typewriter efektu na nově vloženém obsahu
        if (typeof TypewriterEngine !== 'undefined') {
            TypewriterEngine.init();
            TypewriterEngine.playSection(wrapper);
        }

"""
        
        with open('scripts.js', 'w', encoding='utf-8') as f:
            f.write(before + "        // Vložení kompletního HTML\n        wrapper.innerHTML =\n" + new_html + after)
        print("Updated scripts.js product layout")
    else:
        print("Failed to find '1) Hlavní obrázek switch'")
else:
    print("Failed to find 'Vložení kompletního HTML'")
