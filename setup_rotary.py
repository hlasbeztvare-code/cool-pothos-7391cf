import os

css_styles = """
/* ── ROTARY PRESENTATION SYSTEM ── */
body {
    overflow: hidden !important;
}

.rotary-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    perspective: 1500px;
    transform-style: preserve-3d;
    z-index: 10;
}

.rotary-section {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    background: transparent;
    opacity: 0;
    visibility: hidden;
    transform: rotateX(-30deg) translateY(-200px) scale(0.9);
    transition: transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), 
                opacity 0.6s ease,
                visibility 0.8s;
    transform-origin: center center;
    will-change: transform, opacity;
}

.rotary-section.rotary-active {
    opacity: 1;
    visibility: visible;
    transform: rotateX(0deg) translateY(0) scale(1);
    z-index: 50;
}

.rotary-section.rotary-out-up {
    transform: rotateX(30deg) translateY(200px) scale(0.9);
    opacity: 0;
    visibility: hidden;
}

.rotary-section.rotary-out-down {
    transform: rotateX(-30deg) translateY(-200px) scale(0.9);
    opacity: 0;
    visibility: hidden;
}

/* Fix padding for sections since they are full height now */
.rotary-section .section-container,
.rotary-section .hero-container {
    padding-top: 140px; /* Space for fixed header */
    padding-bottom: 60px;
    min-height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-section.rotary-section {
    overflow-y: hidden; /* Hero shouldn't scroll */
}

/* Scrollbar styling for inner scrolling */
.rotary-section::-webkit-scrollbar {
    width: 6px;
}
.rotary-section::-webkit-scrollbar-track {
    background: rgba(var(--color-bg-rgb), 0.5);
}
.rotary-section::-webkit-scrollbar-thumb {
    background: var(--color-accent);
    border-radius: 10px;
}
"""

with open('styles.css', 'a', encoding='utf-8') as f:
    f.write(css_styles)

js_logic = """
// ── ROTARY ENGINE ──
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.getElementById('rotary-wrapper');
    if (!wrapper) return;

    // We skip 'kolekce' because it's hidden.
    const sections = Array.from(document.querySelectorAll('.rotary-section')).filter(sec => sec.id !== 'kolekce');
    if (sections.length === 0) return;

    let currentIndex = 0;
    let isAnimating = false;

    // Helper to switch active section
    function goToSection(index) {
        if (isAnimating || index === currentIndex || index < 0 || index >= sections.length) return;
        
        isAnimating = true;
        const currentSection = sections[currentIndex];
        const nextSection = sections[index];

        // Direction check
        const goingDown = index > currentIndex;

        // Reset classes
        currentSection.classList.remove('rotary-active', 'rotary-out-up', 'rotary-out-down');
        nextSection.classList.remove('rotary-active', 'rotary-out-up', 'rotary-out-down');

        // Apply transition out
        if (goingDown) {
            currentSection.classList.add('rotary-out-up');
            // Before animation, next section should be at bottom
            nextSection.style.transition = 'none';
            nextSection.classList.add('rotary-out-down');
        } else {
            currentSection.classList.add('rotary-out-down');
            // Before animation, next section should be at top
            nextSection.style.transition = 'none';
            nextSection.classList.add('rotary-out-up');
        }

        // Force reflow
        void nextSection.offsetWidth;

        // Apply transition in
        nextSection.style.transition = '';
        nextSection.classList.remove('rotary-out-up', 'rotary-out-down');
        nextSection.classList.add('rotary-active');

        currentIndex = index;

        setTimeout(() => {
            isAnimating = false;
        }, 800); // match CSS transition duration
    }

    // Mouse wheel handling
    let wheelTimeout;
    window.addEventListener('wheel', (e) => {
        // Allow inner scrolling if the section overflows
        const activeSec = sections[currentIndex];
        const canScrollUp = activeSec.scrollTop > 0;
        const canScrollDown = activeSec.scrollHeight - activeSec.clientHeight > activeSec.scrollTop + 1;

        if (e.deltaY > 0 && canScrollDown) return; // let natural scroll happen
        if (e.deltaY < 0 && canScrollUp) return;

        e.preventDefault(); // Prevent default if at boundaries

        clearTimeout(wheelTimeout);
        wheelTimeout = setTimeout(() => {
            if (e.deltaY > 30) {
                goToSection(currentIndex + 1);
            } else if (e.deltaY < -30) {
                goToSection(currentIndex - 1);
            }
        }, 50); // debounce threshold
    }, { passive: false });

    // Touch handling
    let touchStartY = 0;
    window.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
        const activeSec = sections[currentIndex];
        const canScrollUp = activeSec.scrollTop > 0;
        const canScrollDown = activeSec.scrollHeight - activeSec.clientHeight > activeSec.scrollTop + 1;

        const touchEndY = e.touches[0].clientY;
        const diff = touchStartY - touchEndY;

        if (diff > 0 && canScrollDown) return;
        if (diff < 0 && canScrollUp) return;

        // Prevent body scroll bounce
        if (e.cancelable) e.preventDefault();
    }, { passive: false });

    window.addEventListener('touchend', (e) => {
        const touchEndY = e.changedTouches[0].clientY;
        const diff = touchStartY - touchEndY;
        
        if (Math.abs(diff) > 50) {
            if (diff > 0) goToSection(currentIndex + 1);
            else goToSection(currentIndex - 1);
        }
    });

    // Update Nav links
    const navLinks = document.querySelectorAll('.desktop-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href').replace('index.html', '').replace('#', '');
            const targetIndex = sections.findIndex(sec => sec.id === targetId);
            if (targetIndex !== -1) {
                e.preventDefault();
                goToSection(targetIndex);
            }
        });
    });

    // Force active on load
    sections.forEach((sec, i) => {
        if (i !== currentIndex) {
            sec.classList.remove('rotary-active');
            sec.classList.add('rotary-out-down');
        } else {
            sec.classList.add('rotary-active');
        }
    });
});
"""

with open('scripts.js', 'a', encoding='utf-8') as f:
    f.write(js_logic)

print("Styles and Scripts added.")
