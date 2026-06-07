import re

# ==========================================
# 1. HTML MODIFICATIONS
# ==========================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tomb_html = """
    <!-- ── ULTIMATE WOW: TOMB FLASHLIGHT & OPTICAL LOUPE ── -->
    <div id="tomb-darkness"></div>
    <div id="optical-loupe">
        <div class="loupe-glass"></div>
        <div class="loupe-ring"></div>
        <div class="loupe-crosshair"></div>
    </div>
"""

# Insert the tomb and loupe right after body
if 'id="tomb-darkness"' not in html:
    html = html.replace('<body>', f'<body>\n{tomb_html}')

exploded_view_html = """
    <!-- ── APPLE EXPLODED VIEW SECTION ── -->
    <section class="exploded-section rotary-section" id="inzenyrstvi">
        <div class="exploded-container">
            <div class="exploded-text reveal-up">
                <span class="sub-label">OPTIKA & MECHANIKA</span>
                <h2 class="section-title tw-text">Mistrovství v každém detailu</h2>
                <p class="section-subtitle tw-text">Každý filtr je precizně vysoustružený z leteckého hliníku a osazený prémiovým optickým sklem Schott B270.</p>
            </div>
            
            <div class="exploded-3d-scene" id="exploded-scene">
                <div class="filter-layer ring-top"></div>
                <div class="filter-layer glass-pane">
                    <div class="glass-glare-anim"></div>
                </div>
                <div class="filter-layer ring-bottom"></div>
                
                <div class="exploded-labels">
                    <div class="exp-label label-1">CNC Anodizovaný hliník</div>
                    <div class="exp-label label-2">Optické sklo Schott B270</div>
                    <div class="exp-label label-3">Ultra-slim závit</div>
                </div>
            </div>
        </div>
    </section>
"""

# Insert Exploded View between products and about
if 'class="exploded-section' not in html:
    html = html.replace('<!-- ── ABOUT SECTION (O NÁS) ── -->', exploded_view_html + '\n    <!-- ── ABOUT SECTION (O NÁS) ── -->')

# Hide existing standard nav and use a "Turn on Flashlight" overlay instead of entrance
entrance_overlay_html = """
    <div id="tomb-entrance-overlay">
        <div class="tomb-entrance-content">
            <h2 class="tomb-title">Vstupte do temnoty</h2>
            <p>Tento web prozkoumáte vlastní rukou.</p>
            <button id="ignite-flashlight-btn" class="ignite-btn">Zažehnout světlo</button>
        </div>
    </div>
"""
if 'id="tomb-entrance-overlay"' not in html:
    html = html.replace('<body>', f'<body>\n{entrance_overlay_html}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# ==========================================
# 2. CSS MODIFICATIONS
# ==========================================
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

ultimate_css = """
/* ── ULTIMATE WOW: TOMB FLASHLIGHT & LOUPE ── */
body.tomb-mode-active {
    cursor: none !important;
}
body.tomb-mode-active a, body.tomb-mode-active button, body.tomb-mode-active input {
    cursor: none !important;
}

#tomb-entrance-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: #000;
    z-index: 9999999;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: opacity 1.5s cubic-bezier(0.16, 1, 0.3, 1), visibility 1.5s;
}

.tomb-entrance-content {
    text-align: center;
    color: #fff;
    opacity: 0;
    transform: translateY(20px);
    animation: tombFadeIn 2s ease forwards 0.5s;
}

@keyframes tombFadeIn {
    to { opacity: 1; transform: translateY(0); }
}

.tomb-title {
    font-size: 3rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 20px;
    text-shadow: 0 0 20px rgba(207, 177, 143, 0.5);
    font-family: var(--font-title);
}

.ignite-btn {
    margin-top: 40px;
    background: transparent;
    border: 1px solid rgba(207, 177, 143, 0.5);
    color: #cfb18f;
    padding: 15px 40px;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 40px;
}

.ignite-btn:hover {
    background: rgba(207, 177, 143, 0.1);
    box-shadow: 0 0 30px rgba(207, 177, 143, 0.3);
    transform: scale(1.05);
}

#tomb-darkness {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.95);
    z-index: 90000;
    pointer-events: none;
    transition: opacity 2s ease;
    /* Mask follows mouse */
    -webkit-mask-image: radial-gradient(circle 350px at var(--mouse-x, 50%) var(--mouse-y, 50%), transparent 0%, rgba(0,0,0,0.9) 60%, black 100%);
    mask-image: radial-gradient(circle 350px at var(--mouse-x, 50%) var(--mouse-y, 50%), transparent 0%, rgba(0,0,0,0.9) 60%, black 100%);
    opacity: 0; /* Hidden until ignite */
}

body.tomb-mode-active #tomb-darkness {
    opacity: 1;
}

#optical-loupe {
    position: fixed;
    top: 0; left: 0;
    width: 250px;
    height: 250px;
    pointer-events: none;
    z-index: 90001;
    transform: translate(calc(var(--mouse-x, 50vw) - 125px), calc(var(--mouse-y, 50vh) - 125px));
    border-radius: 50%;
    /* Smooth trailing transition applied via JS requestAnimationFrame for better perf, or CSS if preferred */
    opacity: 0;
    transition: opacity 1s ease;
}

body.tomb-mode-active #optical-loupe {
    opacity: 1;
}

.loupe-glass {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 50%;
    backdrop-filter: brightness(1.3) contrast(1.1) saturate(1.2) blur(1px);
    -webkit-backdrop-filter: brightness(1.3) contrast(1.1) saturate(1.2) blur(1px);
    box-shadow: inset 0 0 40px rgba(255, 255, 255, 0.2), 0 20px 50px rgba(0, 0, 0, 0.5);
}

.loupe-ring {
    position: absolute;
    top: -5px; left: -5px; right: -5px; bottom: -5px;
    border-radius: 50%;
    border: 4px solid #111;
    box-shadow: 
        inset 0 0 10px rgba(0,0,0,1), 
        0 0 0 2px rgba(207, 177, 143, 0.4),
        0 10px 20px rgba(0,0,0,0.5);
    background: transparent;
}

.loupe-crosshair {
    position: absolute;
    top: 50%; left: 50%;
    width: 10px; height: 10px;
    background: rgba(207, 177, 143, 0.8);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 15px rgba(207, 177, 143, 1);
}

.loupe-crosshair::before, .loupe-crosshair::after {
    content: '';
    position: absolute;
    background: rgba(207, 177, 143, 0.4);
}
.loupe-crosshair::before {
    top: 50%; left: -20px; right: -20px; height: 1px;
    transform: translateY(-50%);
}
.loupe-crosshair::after {
    left: 50%; top: -20px; bottom: -20px; width: 1px;
    transform: translateX(-50%);
}

/* ── ULTIMATE WOW: APPLE EXPLODED VIEW ── */
.exploded-section {
    padding: 120px 0;
    background: #080504;
    position: relative;
    overflow: hidden;
    min-height: 100vh;
    display: flex;
    align-items: center;
}

.exploded-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 24px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
}

.exploded-text {
    color: #fff;
    z-index: 10;
}

.exploded-text .section-subtitle {
    color: rgba(255,255,255,0.6);
}

.exploded-3d-scene {
    position: relative;
    height: 600px;
    perspective: 1500px;
    transform-style: preserve-3d;
}

.filter-layer {
    position: absolute;
    top: 50%; left: 50%;
    width: 300px; height: 300px;
    border-radius: 50%;
    transform-style: preserve-3d;
    /* Default stacked state */
    transform: translate(-50%, -50%) rotateX(60deg) rotateZ(0deg) translateZ(0px);
    transition: transform 0.1s ease-out; /* Driven by JS Scroll */
}

/* Base transform driven by scroll:
   var(--exp-rotZ) controls rotation as you scroll
   var(--exp-tz) controls layer separation (explosion)
*/
.ring-top {
    border: 15px solid #111;
    box-shadow: inset 0 0 10px rgba(255,255,255,0.1), 0 5px 15px rgba(0,0,0,0.8), 0 0 0 2px rgba(207, 177, 143, 0.5);
    background: transparent;
    transform: translate(-50%, -50%) rotateX(60deg) rotateZ(var(--exp-rotZ, 0deg)) translateZ(var(--exp-tz-top, 0px));
}

.glass-pane {
    background: radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, rgba(207, 177, 143, 0.05) 100%);
    backdrop-filter: blur(5px) contrast(1.2);
    -webkit-backdrop-filter: blur(5px) contrast(1.2);
    border: 2px solid rgba(255,255,255,0.2);
    box-shadow: inset 0 0 30px rgba(255,255,255,0.1);
    transform: translate(-50%, -50%) rotateX(60deg) rotateZ(0deg) translateZ(var(--exp-tz-mid, 0px));
    overflow: hidden;
}

.glass-glare-anim {
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: linear-gradient(135deg, rgba(255,255,255,0) 40%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0) 60%);
    transform: rotate(30deg) translateY(calc(var(--exp-progress, 0) * 200% - 100%));
}

.ring-bottom {
    border: 10px solid #222;
    background: transparent;
    box-shadow: 0 20px 40px rgba(0,0,0,0.9);
    transform: translate(-50%, -50%) rotateX(60deg) rotateZ(0deg) translateZ(var(--exp-tz-bot, 0px));
}

.exploded-labels {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
}

.exp-label {
    position: absolute;
    color: rgba(207, 177, 143, 0.8);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 800;
    opacity: var(--exp-label-op, 0);
    transition: opacity 0.3s;
    white-space: nowrap;
}

.exp-label::before {
    content: '';
    position: absolute;
    background: rgba(207, 177, 143, 0.5);
}

.label-1 {
    top: 15%; right: 0;
    transform: translateX(50px);
}
.label-1::before {
    top: 50%; right: 100%; width: 100px; height: 1px; margin-right: 15px;
}

.label-2 {
    top: 50%; left: 0;
    transform: translateX(-50px) translateY(-50%);
}
.label-2::before {
    top: 50%; left: 100%; width: 120px; height: 1px; margin-left: 15px;
}

.label-3 {
    bottom: 15%; right: 0;
    transform: translateX(50px);
}
.label-3::before {
    top: 50%; right: 100%; width: 80px; height: 1px; margin-right: 15px;
}

@media (max-width: 992px) {
    .exploded-container {
        grid-template-columns: 1fr;
        text-align: center;
    }
    .exploded-3d-scene {
        height: 400px;
    }
}
"""

if "ULTIMATE WOW" not in css:
    css += "\n" + ultimate_css

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)


# ==========================================
# 3. JS MODIFICATIONS
# ==========================================
with open('scripts.js', 'r', encoding='utf-8') as f:
    js = f.read()

ultimate_js = """
// ── ULTIMATE WOW: COMBINED LOGIC ──
document.addEventListener('DOMContentLoaded', () => {
    // 1. Tomb Ignite Sequence
    const igniteBtn = document.getElementById('ignite-flashlight-btn');
    const overlay = document.getElementById('tomb-entrance-overlay');
    
    if (igniteBtn && overlay) {
        igniteBtn.addEventListener('click', () => {
            // "Flash" effect on click
            overlay.style.background = '#fff';
            
            setTimeout(() => {
                overlay.style.opacity = '0';
                overlay.style.visibility = 'hidden';
                document.body.classList.add('tomb-mode-active');
            }, 150);
        });
    }

    // 2. Tomb Mask & Optical Loupe Tracking
    const tombMask = document.getElementById('tomb-darkness');
    const loupe = document.getElementById('optical-loupe');
    
    if (tombMask && loupe) {
        let tMouseX = window.innerWidth / 2;
        let tMouseY = window.innerHeight / 2;
        let lMouseX = tMouseX;
        let lMouseY = tMouseY;
        
        window.addEventListener('mousemove', (e) => {
            tMouseX = e.clientX;
            tMouseY = e.clientY;
        });
        
        const renderLoupe = () => {
            // Smooth trailing for loupe
            lMouseX += (tMouseX - lMouseX) * 0.15;
            lMouseY += (tMouseY - lMouseY) * 0.15;
            
            // Apply coordinates to CSS variables
            tombMask.style.setProperty('--mouse-x', `${lMouseX}px`);
            tombMask.style.setProperty('--mouse-y', `${lMouseY}px`);
            loupe.style.setProperty('--mouse-x', `${lMouseX}px`);
            loupe.style.setProperty('--mouse-y', `${lMouseY}px`);
            
            requestAnimationFrame(renderLoupe);
        };
        requestAnimationFrame(renderLoupe);
        
        // Disable Tomb mode on hover of certain sections if you want, 
        // or keep it everywhere. Let's keep it everywhere for maximum immersion.
    }

    // 3. Apple Exploded View Scroll Logic
    const explodedSection = document.getElementById('inzenyrstvi');
    const explodedScene = document.getElementById('exploded-scene');
    
    if (explodedSection && explodedScene) {
        // We calculate how far the section is scrolled into view
        window.addEventListener('scroll', () => {
            const rect = explodedSection.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            
            // When rect.top is at windowHeight, progress is 0.
            // When rect.top is at 0 (or centered), progress is 0.5.
            // When rect.bottom is at 0, progress is 1.
            
            const totalDistance = windowHeight + rect.height;
            const currentScrolled = windowHeight - rect.top;
            
            let progress = currentScrolled / totalDistance;
            
            // Clamp progress between 0 and 1
            progress = Math.max(0, Math.min(1, progress));
            
            // We want the explosion to peak when progress is exactly 0.5 (section centered)
            // distance from center (0 = center, 1 = edge)
            const distanceFromCenter = Math.abs(progress - 0.5) * 2;
            
            // Explosion factor (1 = fully exploded, 0 = completely flat)
            // Smooth bell curve
            const explosionFactor = Math.pow(1 - distanceFromCenter, 2);
            
            // Maximum explosion distances
            const topMax = 180;
            const midMax = 0;
            const botMax = -180;
            
            explodedScene.style.setProperty('--exp-tz-top', `${topMax * explosionFactor}px`);
            explodedScene.style.setProperty('--exp-tz-mid', `${midMax * explosionFactor}px`);
            explodedScene.style.setProperty('--exp-tz-bot', `${botMax * explosionFactor}px`);
            
            // Rotate as we scroll
            explodedScene.style.setProperty('--exp-rotZ', `${progress * 180}deg`);
            explodedScene.style.setProperty('--exp-progress', progress);
            
            // Fade in labels when exploded
            if (explosionFactor > 0.6) {
                explodedScene.style.setProperty('--exp-label-op', '1');
            } else {
                explodedScene.style.setProperty('--exp-label-op', '0');
            }
        });
    }
});
"""

if "ULTIMATE WOW: COMBINED LOGIC" not in js:
    js += "\n" + ultimate_js

with open('scripts.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("ULTIMATE WOW EFFECTS (Tomb + Loupe + Exploded) injected successfully!")

