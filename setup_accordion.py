import os

css_styles = """
/* ── PREMIUM ACCORDION PRODUCTS ── */
.premium-accordion-section {
    padding: 0 !important;
    margin: 0;
    overflow: hidden !important;
}

.accordion-container {
    display: flex;
    width: 100vw;
    height: 100vh;
    padding-top: 100px; /* Leave space for top nav */
}

.accordion-panel {
    position: relative;
    flex: 1;
    height: 100%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    transition: flex 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.8s ease;
    cursor: pointer;
    overflow: hidden;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
}

.accordion-panel:first-child {
    border-left: none;
}

.accordion-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, rgba(15, 8, 5, 0.9) 0%, rgba(15, 8, 5, 0.4) 50%, rgba(15, 8, 5, 0.2) 100%);
    backdrop-filter: blur(4px);
    transition: backdrop-filter 0.5s ease, background 0.5s ease;
}

.accordion-panel:hover .accordion-overlay {
    backdrop-filter: blur(0px);
    background: linear-gradient(to top, rgba(15, 8, 5, 0.95) 0%, rgba(15, 8, 5, 0.1) 60%, transparent 100%);
}

.accordion-content {
    position: absolute;
    bottom: 50px;
    left: 40px;
    right: 40px;
    color: #fff;
    z-index: 2;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    height: 100%;
}

.accordion-header {
    display: flex;
    align-items: baseline;
    gap: 15px;
    margin-bottom: 0;
    transition: transform 0.5s ease;
}

.accordion-header h2 {
    font-family: var(--font-display);
    font-size: 24px;
    font-weight: 300;
    opacity: 0.6;
    margin: 0;
}

.accordion-header h3 {
    font-family: var(--font-display);
    font-size: 32px;
    font-weight: 600;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 2px;
    white-space: nowrap;
}

.accordion-body {
    max-height: 0;
    opacity: 0;
    overflow: hidden;
    transition: max-height 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.5s ease;
    padding-top: 0;
}

.accordion-body p {
    font-family: var(--font-body);
    font-size: 16px;
    line-height: 1.6;
    margin: 15px 0 25px 0;
    color: rgba(255, 255, 255, 0.8);
    max-width: 400px;
}

.accordion-actions {
    display: flex;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
}

.accordion-actions .price {
    font-family: var(--font-display);
    font-size: 20px;
    font-weight: 600;
    color: #fff;
}

.accordion-actions .add-to-cart-btn {
    background: #fff;
    color: #0f0805;
    border: none;
    padding: 12px 24px;
    border-radius: 4px;
    font-family: var(--font-display);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
}

.accordion-actions .add-to-cart-btn:hover {
    background: var(--color-accent);
    color: #fff;
    transform: translateY(-2px);
}

.accordion-actions .detail-link {
    color: rgba(255, 255, 255, 0.6);
    text-decoration: none;
    font-family: var(--font-display);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 14px;
    transition: color 0.3s ease;
}

.accordion-actions .detail-link:hover {
    color: #fff;
}

/* Hover State */
.accordion-panel:hover {
    flex: 3;
}

.accordion-panel:hover .accordion-header {
    transform: translateY(-10px);
}

.accordion-panel:hover .accordion-header h3 {
    font-size: 48px;
}

.accordion-panel:hover .accordion-body {
    max-height: 300px;
    opacity: 1;
    padding-top: 10px;
}

/* Mobile Responsive */
@media (max-width: 992px) {
    .accordion-container {
        flex-direction: column;
        padding-top: 80px;
    }
    
    .accordion-panel {
        flex: 1;
        border-left: none;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .accordion-panel:hover {
        flex: 2;
    }
    
    .accordion-content {
        left: 20px;
        right: 20px;
        bottom: 30px;
    }
    
    .accordion-panel:hover .accordion-header h3 {
        font-size: 32px;
    }
}
"""

with open('styles.css', 'a', encoding='utf-8') as f:
    f.write(css_styles)
print("Accordion styles added.")
