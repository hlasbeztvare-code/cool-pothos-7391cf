import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

entrance_html = """
    <!-- ── CINEMATIC ENTRANCE ── -->
    <div id="cinematic-entrance" class="cinematic-entrance">
        <div class="entrance-flash"></div>
    </div>
    
    <!-- ── CUSTOM CURSOR ── -->
    <div id="custom-cursor" class="custom-cursor">
        <div class="cursor-crosshair"></div>
    </div>
    <div id="custom-cursor-dot" class="custom-cursor-dot"></div>
"""

if 'id="cinematic-entrance"' not in html:
    html = html.replace('<body>', f'<body>\n{entrance_html}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add cursor and entrance CSS
wow_css = """

/* ── CUSTOM CURSOR ── */
body, a, button, input, textarea {
    cursor: none !important;
}

.custom-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 40px;
    height: 40px;
    border: 1px solid rgba(207, 177, 143, 0.4);
    border-radius: 50%;
    pointer-events: none;
    z-index: 99999;
    transform: translate(-50%, -50%);
    transition: width 0.3s, height 0.3s, background 0.3s;
    mix-blend-mode: screen;
}

.custom-cursor.is-hovering {
    width: 60px;
    height: 60px;
    background: rgba(207, 177, 143, 0.1);
    border-color: rgba(207, 177, 143, 0.8);
}

.cursor-crosshair {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 100%; height: 100%;
}
.cursor-crosshair::before, .cursor-crosshair::after {
    content: '';
    position: absolute;
    background: rgba(207, 177, 143, 0.6);
}
.cursor-crosshair::before {
    top: 50%; left: -5px; right: -5px; height: 1px;
    transform: translateY(-50%);
}
.cursor-crosshair::after {
    left: 50%; top: -5px; bottom: -5px; width: 1px;
    transform: translateX(-50%);
}

.custom-cursor-dot {
    position: fixed;
    top: 0;
    left: 0;
    width: 6px;
    height: 6px;
    background: #fff;
    border-radius: 50%;
    pointer-events: none;
    z-index: 100000;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 10px #fff, 0 0 20px rgba(207, 177, 143, 0.8);
}

/* ── CINEMATIC ENTRANCE ── */
.cinematic-entrance {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: #050302;
    z-index: 999999;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: opacity 2s ease, visibility 2s;
}

.cinematic-entrance.is-loaded {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}

.entrance-flash {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
    opacity: 0;
    transition: opacity 0.5s ease;
}

.entrance-flash.flash-active {
    opacity: 1;
}

/* ── DYNAMIC RELIC TILT OVERRIDES ── */
.relic-frame {
    /* We add transition for smooth return to 0 when mouse leaves */
    transition: transform 0.1s cubic-bezier(0.1, 0.9, 0.2, 1), box-shadow 0.1s ease;
    transform: rotateX(var(--rotate-x, 0deg)) rotateY(var(--rotate-y, 0deg)) translateZ(0px);
}

.relic-card.is-interacting .relic-frame {
    transform: rotateX(var(--rotate-x, 0deg)) rotateY(var(--rotate-y, 0deg)) translateZ(30px);
    box-shadow: 
        15px 30px 50px rgba(0,0,0,0.8), 
        inset 0 0 20px rgba(0,0,0,0.8),
        0 0 0 10px #1a100c,
        0 0 0 12px rgba(207, 177, 143, 0.5);
}

.relic-card.is-interacting .relic-img {
    transform: scale(1.05);
    filter: sepia(0) contrast(1) brightness(1.1);
}

.relic-card.is-interacting .relic-glass-glare {
    /* Dynamic glare positioning */
    opacity: 1;
    transform: translate(var(--glare-x, -50%), var(--glare-y, -50%)) rotate(30deg);
    background: radial-gradient(circle at center, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 60%);
    width: 200%; height: 200%;
}
.relic-glass-glare {
    opacity: 0;
    transition: opacity 0.3s ease;
}

"""

if "CUSTOM CURSOR" not in css:
    css += "\n" + wow_css

# Remove existing :hover effects on relic frames to prevent conflict with JS
css = re.sub(r'\.relic-card:hover \.relic-frame\s*\{[^}]+\}', '/* Removed pure CSS hover frame */', css)
css = re.sub(r'\.relic-card:hover \.relic-img\s*\{[^}]+\}', '/* Removed pure CSS hover img */', css)
css = re.sub(r'\.relic-card:hover \.relic-glass-glare\s*\{[^}]+\}', '/* Removed pure CSS hover glare */', css)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update scripts.js
with open('scripts.js', 'r', encoding='utf-8') as f:
    js = f.read()

wow_js = """
// ── WOW EFFECTS: ENTRANCE, CURSOR, 3D TILT ──
document.addEventListener('DOMContentLoaded', () => {
    // 1. Cinematic Entrance
    const entrance = document.getElementById('cinematic-entrance');
    const flash = entrance?.querySelector('.entrance-flash');
    if (entrance) {
        // Wait for Astrolabe to render briefly, then flash and fade
        setTimeout(() => {
            if (flash) flash.classList.add('flash-active');
            setTimeout(() => {
                if (flash) flash.classList.remove('flash-active');
                entrance.classList.add('is-loaded');
            }, 100);
        }, 800);
    }

    // 2. Custom Cursor Tracking
    const cursor = document.getElementById('custom-cursor');
    const cursorDot = document.getElementById('custom-cursor-dot');
    
    if (cursor && cursorDot) {
        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;
        let cursorX = mouseX;
        let cursorY = mouseY;
        
        window.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            // Dot follows instantly
            cursorDot.style.left = mouseX + 'px';
            cursorDot.style.top = mouseY + 'px';
        });
        
        // Smooth trailing for the main crosshair
        const renderCursor = () => {
            cursorX += (mouseX - cursorX) * 0.15;
            cursorY += (mouseY - cursorY) * 0.15;
            cursor.style.left = cursorX + 'px';
            cursor.style.top = cursorY + 'px';
            requestAnimationFrame(renderCursor);
        };
        requestAnimationFrame(renderCursor);
        
        // Hover states
        const hoverElements = document.querySelectorAll('a, button, .relic-card, .stepper-btn, .variant-pill, .size-btn');
        hoverElements.forEach(el => {
            el.addEventListener('mouseenter', () => cursor.classList.add('is-hovering'));
            el.addEventListener('mouseleave', () => cursor.classList.remove('is-hovering'));
        });
    }

    // 3. Dynamic 3D Relic Cards Tilt & Glare
    const relicCards = document.querySelectorAll('.relic-card');
    relicCards.forEach(card => {
        const frame = card.querySelector('.relic-frame');
        
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within the element.
            const y = e.clientY - rect.top;  // y position within the element.
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate rotation (max 10 degrees)
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            // Calculate glare position
            const glareX = (x / rect.width) * 100 - 50;
            const glareY = (y / rect.height) * 100 - 50;
            
            card.classList.add('is-interacting');
            
            if (frame) {
                frame.style.setProperty('--rotate-x', `${rotateX}deg`);
                frame.style.setProperty('--rotate-y', `${rotateY}deg`);
                frame.style.setProperty('--glare-x', `${glareX}%`);
                frame.style.setProperty('--glare-y', `${glareY}%`);
            }
        });
        
        card.addEventListener('mouseleave', () => {
            card.classList.remove('is-interacting');
            if (frame) {
                // Reset smoothly
                frame.style.setProperty('--rotate-x', '0deg');
                frame.style.setProperty('--rotate-y', '0deg');
            }
        });
    });
});
"""

if "WOW EFFECTS: ENTRANCE, CURSOR" not in js:
    js += "\n" + wow_js

with open('scripts.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("WOW effects applied successfully!")

