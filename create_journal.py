html_content = """<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>Fotofiltry.cz - Kniha Objevů</title>
    <link rel="stylesheet" href="journal.css">
</head>
<body>
    <!-- Astrolabe Background -->
    <canvas id="canvas3d"></canvas>

    <div class="desk">
        <div class="book" id="book">
            <!-- Přebal knihy -->
            <div class="page cover" style="z-index: 10;">
                <div class="front">
                    <div class="cover-design">
                        <img src="Fotofiltry.cz LOGO, ICON/Fotofiltry.cz/Logos/Primary logo/ff-logo-vertical.png" alt="Logo" class="cover-logo">
                        <h2>SVAZEK I.</h2>
                        <p>Ztracené optické artefakty</p>
                    </div>
                </div>
                <div class="back cover-inside">
                    <!-- Vnitřní strana přebalu -->
                </div>
            </div>

            <!-- Strana 1: Úvod -->
            <div class="page" style="z-index: 9;">
                <div class="front paper">
                    <div class="page-content">
                        <h1 class="ink-title">Přelomový objev.</h1>
                        <p class="typewriter-text">Našli jsme způsob, jak zachytit světlo přesně tak, jak ho vidí oko. Nebo spíš... jak si ho přeje vidět duše.</p>
                        <p class="typewriter-text">Následující stránky obsahují nákresy a specifikace optických relikvií. Zacházejte s nimi opatrně.</p>
                    </div>
                    <div class="page-number">1</div>
                </div>
                <div class="back paper">
                    <div class="page-content center-content">
                        <img src="images/kaledo_transparent.png" class="blueprint-img" alt="Kaleidoskop Blueprint">
                    </div>
                    <div class="page-number-left">2</div>
                </div>
            </div>

            <!-- Strana 2: Kolekce - Kaleidoskop -->
            <div class="page" style="z-index: 8;">
                <div class="front paper">
                    <div class="page-content">
                        <h2 class="ink-title">Kaleidoskop</h2>
                        <div class="polaroid">
                            <div class="polaroid-img placeholder-1"></div>
                            <p class="polaroid-caption">Lom světla do tisíců střípků.</p>
                        </div>
                        <p class="handwritten">Fascinující úkaz. Světlo se tříští o hrany Schott B270 skla.</p>
                        <button class="buy-btn">Získat Artefakt</button>
                    </div>
                    <div class="page-number">3</div>
                </div>
                <div class="back paper">
                     <div class="page-content center-content">
                        <img src="images/fog_transparent.png" class="blueprint-img" alt="Fog Blueprint">
                    </div>
                    <div class="page-number-left">4</div>
                </div>
            </div>

            <!-- Strana 3: Kolekce - Fog -->
            <div class="page" style="z-index: 7;">
                <div class="front paper">
                    <div class="page-content">
                        <h2 class="ink-title">Fog Filter</h2>
                        <div class="polaroid">
                            <div class="polaroid-img placeholder-2"></div>
                            <p class="polaroid-caption">Závoj snové mlhy.</p>
                        </div>
                        <p class="handwritten">Ideální pro změkčení digitální ostrosti.</p>
                        <button class="buy-btn">Získat Artefakt</button>
                    </div>
                    <div class="page-number">5</div>
                </div>
                <div class="back paper">
                    <div class="page-content">
                        <h2 class="ink-title">Konec svazku.</h2>
                    </div>
                    <div class="page-number-left">6</div>
                </div>
            </div>

        </div>
        
        <!-- Ovládání listování -->
        <div class="controls">
            <button id="prev-btn" class="nav-btn">← Předchozí strana</button>
            <button id="next-btn" class="nav-btn">Další strana →</button>
        </div>
    </div>

    <script src="journal.js"></script>
    <script src="IndianaJonesEngine.js"></script>
</body>
</html>
"""

css_content = """@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Caveat:wght@400;700&family=Special+Elite&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background: #050302;
    overflow: hidden;
    font-family: 'Special Elite', monospace;
    color: #333;
}

#canvas3d {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0;
    opacity: 0.3;
}

.desk {
    position: relative;
    width: 100vw; height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1;
    perspective: 2500px; /* Crucial for 3D effect */
}

.book {
    position: relative;
    width: 40vw; /* Width of ONE page */
    height: 75vh;
    /* Move book slightly to the right so when closed it looks centered */
    transform: translateX(20vw) rotateX(15deg);
    transform-style: preserve-3d;
    transition: transform 1s ease;
}

/* When book is opened, center it */
.book.opened {
    transform: translateX(0) rotateX(5deg);
}

.page {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    transform-origin: left center;
    transform-style: preserve-3d;
    transition: transform 1.2s cubic-bezier(0.645, 0.045, 0.355, 1);
    cursor: pointer;
}

.page.turned {
    transform: rotateY(-180deg);
}

/* Front and Back of each page */
.front, .back {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 3px 15px 15px 3px;
    box-shadow: inset 0 0 30px rgba(0,0,0,0.1), 3px 5px 15px rgba(0,0,0,0.4);
    overflow: hidden;
}

.back {
    transform: rotateY(180deg);
    border-radius: 15px 3px 3px 15px;
}

/* Textures */
.cover .front {
    background: #2b1d12 url('https://www.transparenttextures.com/patterns/leather.png');
    border: 2px solid #1a100a;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #cfb18f;
}

.cover-inside {
    background: #1f140c url('https://www.transparenttextures.com/patterns/leather.png');
}

.paper {
    background: #e6d8c3 url('https://www.transparenttextures.com/patterns/cream-paper.png');
    color: #2a2018;
}

/* Content Styling */
.cover-design {
    text-align: center;
    border: 2px solid #cfb18f;
    padding: 40px;
    border-radius: 10px;
}
.cover-logo { width: 100px; margin-bottom: 20px; filter: drop-shadow(0 0 5px rgba(207, 177, 143, 0.5)); }
.cover-design h2 { font-family: 'Cinzel', serif; font-size: 2rem; margin-bottom: 10px; }
.cover-design p { font-family: 'Cinzel', serif; font-size: 1rem; opacity: 0.8; }

.page-content {
    padding: 50px;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.center-content { align-items: center; justify-content: center; }

.ink-title {
    font-family: 'Cinzel', serif;
    font-size: 2.5rem;
    margin-bottom: 30px;
    border-bottom: 2px solid rgba(0,0,0,0.2);
    padding-bottom: 10px;
}

.typewriter-text {
    font-size: 1.2rem;
    line-height: 1.6;
    margin-bottom: 20px;
    opacity: 0.8;
}

.handwritten {
    font-family: 'Caveat', cursive;
    font-size: 1.8rem;
    color: #1b1464; /* Blue ink */
    transform: rotate(-2deg);
    margin: 20px 0;
}

.blueprint-img {
    width: 80%;
    filter: invert(1) opacity(0.8) sepia(1) hue-rotate(180deg);
}

.polaroid {
    background: white;
    padding: 10px 10px 30px 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    transform: rotate(3deg);
    margin-bottom: 20px;
    width: 80%;
    align-self: center;
}
.polaroid-img {
    width: 100%;
    height: 200px;
    background: #333;
}
.placeholder-1 { background: url('images/kaleidoskop1.jpg') center/cover; }
.placeholder-2 { background: url('images/fog1.jpg') center/cover; }

.polaroid-caption {
    font-family: 'Caveat', cursive;
    font-size: 1.4rem;
    text-align: center;
    margin-top: 10px;
}

.buy-btn {
    margin-top: auto;
    background: transparent;
    border: 2px solid #2a2018;
    padding: 15px;
    font-family: 'Cinzel', serif;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
}
.buy-btn:hover {
    background: #2a2018;
    color: #e6d8c3;
}

.page-number, .page-number-left {
    position: absolute;
    bottom: 20px;
    font-family: 'Cinzel', serif;
    opacity: 0.5;
}
.page-number { right: 20px; }
.page-number-left { left: 20px; }

.controls {
    position: absolute;
    bottom: 30px;
    width: 100%;
    display: flex;
    justify-content: space-around;
    z-index: 100;
}
.nav-btn {
    background: rgba(0,0,0,0.5);
    color: #cfb18f;
    border: 1px solid #cfb18f;
    padding: 10px 20px;
    font-family: 'Cinzel', serif;
    cursor: pointer;
    backdrop-filter: blur(5px);
}
.nav-btn:hover { background: rgba(207, 177, 143, 0.2); }
"""

js_content = """document.addEventListener('DOMContentLoaded', () => {
    const pages = document.querySelectorAll('.page');
    const book = document.getElementById('book');
    let currentPageIndex = 0;

    // Update z-indexes dynamically so pages stack correctly
    function updateZIndexes() {
        pages.forEach((page, index) => {
            if (page.classList.contains('turned')) {
                // Pages on the left: lower index = higher z-index (closest to user)
                page.style.zIndex = index + 1;
            } else {
                // Pages on the right: higher index = lower z-index
                page.style.zIndex = pages.length - index;
            }
        });
    }

    function turnNext() {
        if (currentPageIndex < pages.length) {
            if (currentPageIndex === 0) {
                book.classList.add('opened'); // Center the book when cover is opened
            }
            pages[currentPageIndex].classList.add('turned');
            currentPageIndex++;
            setTimeout(updateZIndexes, 300); // Update z-index halfway through the flip
        }
    }

    function turnPrev() {
        if (currentPageIndex > 0) {
            currentPageIndex--;
            pages[currentPageIndex].classList.remove('turned');
            if (currentPageIndex === 0) {
                book.classList.remove('opened'); // Shift book back to right when closed
            }
            setTimeout(updateZIndexes, 300);
        }
    }

    document.getElementById('next-btn').addEventListener('click', turnNext);
    document.getElementById('prev-btn').addEventListener('click', turnPrev);

    // Allow clicking on pages to turn them
    pages.forEach((page, index) => {
        page.addEventListener('click', () => {
            if (page.classList.contains('turned')) {
                turnPrev();
            } else {
                turnNext();
            }
        });
    });

    // Initialize Astrolabe background (from existing IndianaJonesEngine)
    if (typeof IndianaJonesEngine !== 'undefined') {
        const engine = new IndianaJonesEngine('canvas3d');
    }
});
"""

with open('journal.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
with open('journal.css', 'w', encoding='utf-8') as f:
    f.write(css_content)
with open('journal.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Journal files created successfully.")
