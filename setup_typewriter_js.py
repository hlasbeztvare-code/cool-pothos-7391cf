import re

with open('scripts.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add TypewriterEngine
typewriter_code = """
// ── TYPEWRITER ENGINE ──
const TypewriterEngine = {
    init: function() {
        document.querySelectorAll('.tw-text').forEach(el => {
            if (!el.hasAttribute('data-tw-original')) {
                el.setAttribute('data-tw-original', el.innerHTML);
            }
            this.resetElement(el);
            el.classList.add('tw-ready');
        });
    },
    resetElement: function(el) {
        el.innerHTML = '';
        el.removeAttribute('data-tw-active');
    },
    resetSection: function(section) {
        if (!section) return;
        section.querySelectorAll('.tw-text').forEach(el => this.resetElement(el));
    },
    playSection: function(section) {
        if (!section) return;
        const elements = section.querySelectorAll('.tw-text');
        if (elements.length === 0) return;

        // Play sequentially with small delays based on index
        elements.forEach((el, index) => {
            setTimeout(() => {
                this.typeElement(el);
            }, index * 400 + 400); // 400ms delay between elements, plus initial 400ms delay for rotation
        });
    },
    typeElement: function(el) {
        if (el.hasAttribute('data-tw-active')) return;
        el.setAttribute('data-tw-active', 'true');
        
        const htmlContent = el.getAttribute('data-tw-original');
        el.innerHTML = '';
        
        const cursor = document.createElement('span');
        cursor.className = 'tw-cursor';
        el.appendChild(cursor);

        let i = 0;
        let isTag = false;
        let tagBuffer = '';

        const typeInterval = setInterval(() => {
            if (i >= htmlContent.length) {
                clearInterval(typeInterval);
                setTimeout(() => cursor.remove(), 1500); // Remove cursor after done
                return;
            }

            const char = htmlContent.charAt(i);
            
            if (char === '<') {
                isTag = true;
            }
            
            if (isTag) {
                tagBuffer += char;
                if (char === '>') {
                    isTag = false;
                    // insert tag before cursor
                    cursor.insertAdjacentHTML('beforebegin', tagBuffer);
                    tagBuffer = '';
                }
            } else {
                cursor.insertAdjacentText('beforebegin', char);
            }
            
            i++;
        }, 30); // 30ms per character
    }
};

document.addEventListener('DOMContentLoaded', () => {
    TypewriterEngine.init();
});
"""

content = content + "\n" + typewriter_code

# Inject TypewriterEngine into goToSection
# Find: `nextSection.classList.add('rotary-active');`
# Replace with: `nextSection.classList.add('rotary-active');\n        TypewriterEngine.resetSection(currentSection);\n        TypewriterEngine.playSection(nextSection);`

content = content.replace("nextSection.classList.add('rotary-active');", "nextSection.classList.add('rotary-active');\n        TypewriterEngine.resetSection(currentSection);\n        TypewriterEngine.playSection(nextSection);")

# Find: `sec.classList.add('rotary-active');` inside the `sections.forEach((sec, i) => {`
# Replace with: `sec.classList.add('rotary-active');\n            TypewriterEngine.playSection(sec);`
content = content.replace("sec.classList.add('rotary-active');", "sec.classList.add('rotary-active');\n            setTimeout(()=>TypewriterEngine.playSection(sec), 500);")


with open('scripts.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Typewriter JS added")
