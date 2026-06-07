/**
 * KNIHA OBJEVŮ — Interactive 3D Journal Engine
 * Handles: page flipping, z-index management, scroll/keyboard/click navigation,
 *          cinematic intro, ambient particle canvas, page indicators.
 */

(function () {
    'use strict';

    // ── STATE ──
    const pages = [];
    let currentPage = 0;
    let isAnimating = false;
    let bookReady = false;

    // ── DOM REFS ──
    const book = document.getElementById('book');
    const introOverlay = document.getElementById('intro-overlay');
    const introEnter = document.getElementById('intro-enter');
    const deskScene = document.getElementById('desk-scene');
    const indicatorDots = document.querySelectorAll('.indicator-dot');
    const canvas = document.getElementById('ambient-canvas');

    // ══════════════════════════════════════════════════
    // AMBIENT PARTICLE CANVAS (Astrolabe-lite: gold dust)
    // ══════════════════════════════════════════════════
    function initAmbientCanvas() {
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let w = window.innerWidth;
        let h = window.innerHeight;
        canvas.width = w;
        canvas.height = h;

        const particles = [];
        const NUM = 80;

        for (let i = 0; i < NUM; i++) {
            particles.push({
                x: Math.random() * w,
                y: Math.random() * h,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3 - 0.15,
                size: Math.random() * 1.5 + 0.3,
                alpha: Math.random() * 0.4 + 0.1,
                phase: Math.random() * Math.PI * 2
            });
        }

        let time = 0;

        function draw() {
            time++;
            ctx.globalCompositeOperation = 'source-over';
            ctx.fillStyle = 'rgba(5, 3, 2, 0.15)';
            ctx.fillRect(0, 0, w, h);

            ctx.globalCompositeOperation = 'screen';

            particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;
                if (p.x < 0) p.x = w;
                if (p.x > w) p.x = 0;
                if (p.y < 0) p.y = h;

                const twinkle = 0.15 + Math.abs(Math.sin(time * 0.01 + p.phase)) * 0.5;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(207, 177, 143, ${twinkle * p.alpha})`;
                ctx.fill();
            });

            // Subtle central glow
            const glow = ctx.createRadialGradient(w * 0.6, h * 0.5, 50, w * 0.6, h * 0.5, 500);
            glow.addColorStop(0, 'rgba(207, 177, 143, 0.04)');
            glow.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = glow;
            ctx.fillRect(0, 0, w, h);

            requestAnimationFrame(draw);
        }

        draw();

        window.addEventListener('resize', () => {
            w = window.innerWidth;
            h = window.innerHeight;
            canvas.width = w;
            canvas.height = h;
        });
    }

    // ══════════════════════════════════════════════════
    // CINEMATIC INTRO
    // ══════════════════════════════════════════════════
    function initIntro() {
        if (!introEnter || !introOverlay) return;

        // Spawn floating particles in intro
        const particlesContainer = document.getElementById('intro-particles');
        if (particlesContainer) {
            for (let i = 0; i < 30; i++) {
                const dot = document.createElement('div');
                dot.style.cssText = `
                    position: absolute;
                    width: ${Math.random() * 3 + 1}px;
                    height: ${Math.random() * 3 + 1}px;
                    background: rgba(207, 177, 143, ${Math.random() * 0.3 + 0.05});
                    border-radius: 50%;
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    animation: introFloat ${Math.random() * 10 + 10}s ease-in-out infinite ${Math.random() * 5}s;
                `;
                particlesContainer.appendChild(dot);
            }

            // Add float animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes introFloat {
                    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
                    25% { transform: translate(${Math.random() * 30 - 15}px, -${Math.random() * 40 + 10}px) scale(1.2); opacity: 0.6; }
                    50% { transform: translate(${Math.random() * 20 - 10}px, -${Math.random() * 60 + 20}px) scale(0.8); opacity: 0.2; }
                    75% { transform: translate(${Math.random() * 30 - 15}px, -${Math.random() * 30 + 5}px) scale(1.1); opacity: 0.5; }
                }
            `;
            document.head.appendChild(style);
        }

        introEnter.addEventListener('click', () => {
            introOverlay.classList.add('hidden');
            deskScene.classList.add('visible');
            bookReady = true;
        });
    }

    // ══════════════════════════════════════════════════
    // PAGE FLIP ENGINE
    // ══════════════════════════════════════════════════
    function initBook() {
        const pageElements = book.querySelectorAll('.page');
        pageElements.forEach((el, index) => {
            pages.push(el);
            // Set initial z-index: first page on top
            el.style.zIndex = pageElements.length - index;

            // Click to flip
            el.addEventListener('click', (e) => {
                // Don't flip if clicking a button or link
                if (e.target.closest('button, a')) return;
                if (!bookReady || isAnimating) return;

                const rect = el.getBoundingClientRect();
                const clickX = e.clientX - rect.left;
                const midX = rect.width / 2;

                // If the page is already flipped, clicking unflips it (go back)
                if (el.classList.contains('flipped')) {
                    goToPage(currentPage - 1);
                } else {
                    goToPage(currentPage + 1);
                }
            });
        });

        updateIndicators();
    }

    function goToPage(targetPage) {
        if (isAnimating) return;
        if (targetPage < 0 || targetPage > pages.length) return;

        isAnimating = true;

        if (targetPage > currentPage) {
            // Flip forward
            for (let i = currentPage; i < targetPage; i++) {
                flipForward(i, (targetPage - currentPage - 1 - (i - currentPage)) * 150);
            }
        } else if (targetPage < currentPage) {
            // Flip backward
            for (let i = currentPage - 1; i >= targetPage; i--) {
                flipBack(i, (currentPage - 1 - i) * 150);
            }
        }

        currentPage = targetPage;

        setTimeout(() => {
            updateZIndexes();
            updateIndicators();
            isAnimating = false;
        }, 1200);
    }

    function flipForward(index, delay) {
        setTimeout(() => {
            pages[index].classList.add('flipping');
            pages[index].classList.add('flipped');
            setTimeout(() => pages[index].classList.remove('flipping'), 800);
        }, delay);
    }

    function flipBack(index, delay) {
        setTimeout(() => {
            pages[index].classList.add('flipping');
            pages[index].classList.remove('flipped');
            setTimeout(() => pages[index].classList.remove('flipping'), 800);
        }, delay);
    }

    function updateZIndexes() {
        pages.forEach((page, index) => {
            if (page.classList.contains('flipped')) {
                page.style.zIndex = index + 1;
            } else {
                page.style.zIndex = pages.length - index;
            }
        });
    }

    function updateIndicators() {
        indicatorDots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentPage);
        });
    }

    // ── KEYBOARD NAVIGATION ──
    document.addEventListener('keydown', (e) => {
        if (!bookReady || isAnimating) return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            goToPage(currentPage + 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            goToPage(currentPage - 1);
        }
    });

    // ── SCROLL NAVIGATION (mousewheel turns pages) ──
    let scrollAccumulator = 0;
    const SCROLL_THRESHOLD = 80;

    document.addEventListener('wheel', (e) => {
        if (!bookReady || isAnimating) return;
        e.preventDefault();

        scrollAccumulator += e.deltaY;

        if (Math.abs(scrollAccumulator) > SCROLL_THRESHOLD) {
            if (scrollAccumulator > 0) {
                goToPage(currentPage + 1);
            } else {
                goToPage(currentPage - 1);
            }
            scrollAccumulator = 0;
        }
    }, { passive: false });

    // ── TOUCH NAVIGATION (swipe) ──
    let touchStartX = 0;
    let touchStartY = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
        if (!bookReady || isAnimating) return;
        const dx = e.changedTouches[0].clientX - touchStartX;
        const dy = e.changedTouches[0].clientY - touchStartY;

        // Horizontal swipe must be dominant
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
            if (dx < 0) {
                goToPage(currentPage + 1);
            } else {
                goToPage(currentPage + 1 > pages.length ? currentPage : currentPage - 1);
            }
        }
    }, { passive: true });

    // ── INDICATOR CLICK ──
    indicatorDots.forEach(dot => {
        dot.addEventListener('click', () => {
            if (!bookReady || isAnimating) return;
            const target = parseInt(dot.dataset.target, 10);
            goToPage(target);
        });
    });

    // ══════════════════════════════════════════════════
    // INIT
    // ══════════════════════════════════════════════════
    document.addEventListener('DOMContentLoaded', () => {
        initAmbientCanvas();
        initIntro();
        initBook();
    });

})();
