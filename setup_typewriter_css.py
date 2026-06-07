import os

css = """
/* ── TYPEWRITER EFFECT ── */
.tw-text {
    visibility: hidden; /* Hide initially to prevent FOUC */
}
.tw-text.tw-ready {
    visibility: visible;
}

.tw-cursor {
    display: inline-block;
    width: 0.5em;
    height: 1em;
    background-color: var(--color-accent, rgba(43, 24, 16, 0.8));
    vertical-align: bottom;
    animation: blink-cursor 1s step-end infinite;
    margin-left: 2px;
}

@keyframes blink-cursor {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
"""

with open('styles.css', 'a', encoding='utf-8') as f:
    f.write(css)
print("Typewriter CSS added")
