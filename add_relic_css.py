import os

css = """
/* ── MUSEUM RELICS COLLECTION ── */
.relic-museum-section {
    padding: 100px 0;
    background: transparent;
}

.relic-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 40px;
    margin-top: 60px;
}

.relic-card {
    display: flex;
    flex-direction: column;
    perspective: 1000px;
    position: relative;
}

.relic-frame {
    position: relative;
    background: #0f0805;
    padding: 20px;
    border: 3px solid #8b1515;
    border-radius: 8px;
    box-shadow: 
        0 20px 40px rgba(0,0,0,0.6), 
        inset 0 0 20px rgba(0,0,0,0.8),
        0 0 0 10px #1a100c, /* Outer dark wood */
        0 0 0 12px rgba(207, 177, 143, 0.2); /* Gold trim */
    transform-style: preserve-3d;
    transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.5s ease;
    margin-bottom: 30px;
    height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.relic-frame::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='1.5' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.08'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 1;
}

.relic-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
    filter: sepia(0.3) contrast(1.1) brightness(0.9);
    transition: transform 0.5s ease, filter 0.5s ease;
}

.relic-glass-glare {
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: linear-gradient(135deg, rgba(255,255,255,0) 30%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 70%);
    transform: rotate(30deg) translateY(-100%);
    transition: transform 0.6s ease;
    pointer-events: none;
    z-index: 2;
}

.relic-card:hover .relic-frame {
    transform: rotateX(5deg) rotateY(-5deg) translateZ(30px);
    box-shadow: 
        15px 30px 50px rgba(0,0,0,0.8), 
        inset 0 0 20px rgba(0,0,0,0.8),
        0 0 0 10px #1a100c,
        0 0 0 12px rgba(207, 177, 143, 0.5);
}

.relic-card:hover .relic-img {
    transform: scale(1.05);
    filter: sepia(0) contrast(1) brightness(1.1);
}

.relic-card:hover .relic-glass-glare {
    transform: rotate(30deg) translateY(100%);
}

.relic-info {
    position: relative;
    padding: 20px;
    background: rgba(15, 8, 5, 0.8);
    border: 1px solid rgba(207, 177, 143, 0.15);
    border-radius: 4px;
}

.relic-seal {
    position: absolute;
    top: -20px;
    right: 20px;
    width: 40px;
    height: 40px;
    background: #8b1515;
    border-radius: 50%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5), inset 0 0 5px rgba(0,0,0,0.8);
    z-index: 3;
}

.relic-seal::after {
    content: '★';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    color: rgba(255,255,255,0.3);
    font-size: 16px;
}

.relic-title {
    font-size: 24px;
    font-weight: 800;
    color: var(--color-accent);
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.relic-desc {
    color: var(--color-text-muted);
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.relic-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: center;
}

.relic-actions .price {
    font-family: var(--font-display);
    font-size: 20px;
    font-weight: 900;
    color: var(--color-text);
}

@media (max-width: 900px) {
    .relic-grid {
        grid-template-columns: 1fr;
    }
}
"""

with open('styles.css', 'a', encoding='utf-8') as f:
    f.write(css)
print("Museum relic CSS added")
