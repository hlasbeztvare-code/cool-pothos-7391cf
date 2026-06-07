import re

with open('scripts.js', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"(// Vložení kompletního HTML\n        wrapper\.innerHTML =\n)(.*?)(        // ── AKCE A INTERAKCE NA DETAILU PRODUKTU ──)"

new_html = """            '<!-- Left Visual Gallery (Smaller) -->' +
            '<div class="product-detail-visual" style="max-width: 450px; width: 100%;">' +
            '<div class="product-detail-main-image-wrap">' +
            '<img src="' + activeImage + '" alt="' + product.name + '" class="product-detail-main-img" id="main-detail-img" fetchpriority="high" style="transform: scale(1.0);">' +
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
            '<div class="premium-editorial-section" style="margin-top: 30px;">' +
            '<div class="editorial-block">' +
            '<h3 class="editorial-title tw-text">Příběh produktu</h3>' +
            '<div class="editorial-content tw-text" style="font-size: 16px; line-height: 1.6; opacity: 0.8;">' + product.description + '</div>' +
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
            '</div>' +

            '<!-- Variant Selection -->' +
            (product.variants && product.variants.length > 0 ?
                '<div class="product-option-group">' +
                '<span class="product-option-label tw-text">Volba verze / efektu:</span>' +
                '<div class="product-variant-pills" id="detail-variants-container">' +
                variantsHtml +
                '</div>' +
                '</div>' : '') +

            '<!-- Size Selection -->' +
            (product.sizes && product.sizes.length > 0 ?
                '<div class="product-option-group">' +
                '<span class="product-option-label tw-text">Velikost (průměr závitu objektivu):</span>' +
                '<div class="product-size-grid" id="detail-sizes-container">' +
                sizesHtml +
                '</div>' +
                '</div>' : '') +

            '<!-- Stock Level -->' +
            '<div class="stock-status-wrapper">' +
            '<span class="stock-status-dot ' + initialStockClass + '" id="detail-stock-dot"></span>' +
            '<span id="detail-stock-text" style="font-size: 13px; font-weight: 800;">' + initialStockLabel + '</span>' +
            '</div>' +

            '<!-- Quantity and Add to Cart -->' +
            '<div class="product-add-to-cart-wrapper">' +
            '<div class="quantity-stepper">' +
            '<button class="stepper-btn" id="stepper-minus" style="font-weight:900;">-</button>' +
            '<input type="text" class="stepper-input" id="stepper-val" value="1" readonly>' +
            '<button class="stepper-btn" id="stepper-plus" style="font-weight:900;">+</button>' +
            '</div>' +
            '<button class="detail-add-btn ' + (selectedSizeObj.stock === 0 ? 'disabled' : '') + '" id="detail-add-to-cart-btn" ' + (selectedSizeObj.stock === 0 ? 'disabled' : '') + ' style="width:100%;">Do košíku</button>' +
            '</div>' +
            '</div>';

        if (typeof TypewriterEngine !== 'undefined') {
            TypewriterEngine.init();
            TypewriterEngine.playSection(wrapper);
        }

"""

new_content = re.sub(pattern, r"\1" + new_html + r"\3", content, flags=re.DOTALL)

with open('scripts.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated scripts.js product layout via regex")
