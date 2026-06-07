import os

css = """
/* ── SKEUOMORPHIC PAPER STACK (O NÁS) ── */
.paper-stack {
    position: relative;
    background: #fdfbf7;
    padding: 40px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2), inset 0 0 50px rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.05);
    z-index: 5;
    color: #2b1810;
    margin: 20px 0;
}

.paper-stack .sub-label,
.paper-stack .about-title,
.paper-stack p,
.paper-stack strong,
.paper-stack .tw-cursor {
    color: #2b1810 !important;
}

.paper-stack::before,
.paper-stack::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: #fdfbf7;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    border: 1px solid rgba(0,0,0,0.05);
    z-index: -1;
}

.paper-stack::before {
    transform: rotate(-3deg);
}

.paper-stack::after {
    transform: rotate(2deg);
    z-index: -2;
}

/* ── SKEUOMORPHIC ENVELOPE (KONTAKT) ── */
.envelope-container {
    position: relative;
    background: #cfb18f;
    padding: 50px 40px 70px 40px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    border: 1px solid rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 0 auto;
    overflow: hidden;
    color: #2b1810;
    background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
}

/* Envelope Flap */
.envelope-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    border-top: 80px solid rgba(0,0,0,0.05);
    border-left: 250px solid transparent;
    border-right: 250px solid transparent;
    z-index: 1;
    pointer-events: none;
}

.envelope-form {
    position: relative;
    z-index: 2;
}

.envelope-form .form-group label {
    color: #553a25;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 1px;
}

.envelope-form input,
.envelope-form textarea {
    background: rgba(255, 255, 255, 0.85) !important;
    border: 1px dashed rgba(0,0,0,0.3) !important;
    color: #2b1810 !important;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.05);
    border-radius: 0 !important;
    padding: 12px !important;
}

.envelope-form input:focus,
.envelope-form textarea:focus {
    background: #fff !important;
    border: 1px dashed rgba(0,0,0,0.6) !important;
    outline: none;
}

/* Stamp button */
.envelope-submit {
    background: transparent !important;
    border: 3px solid #8b1515 !important;
    color: #8b1515 !important;
    font-family: var(--font-display);
    font-weight: 800;
    letter-spacing: 2px;
    padding: 10px 20px;
    transform: rotate(-5deg);
    display: inline-block;
    transition: transform 0.2s, background 0.2s;
    cursor: pointer;
    margin-top: 10px;
    border-radius: 4px;
}

.envelope-submit:hover {
    transform: scale(1.1) rotate(-5deg);
    background: rgba(139, 21, 21, 0.05) !important;
}

/* Wax Seal */
.envelope-seal {
    position: absolute;
    bottom: 25px;
    right: 25px;
    width: 60px;
    height: 60px;
    background: #8b1515;
    border-radius: 50%;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.4), inset 0 0 10px rgba(0,0,0,0.6);
    z-index: 3;
}

.envelope-seal::after {
    content: '★';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    color: rgba(255,255,255,0.3);
    font-size: 24px;
}

/* Postmark */
.envelope-postmark {
    position: absolute;
    bottom: 45px;
    right: 95px;
    width: 80px;
    height: 80px;
    border: 2px solid rgba(0,0,0,0.15);
    border-radius: 50%;
    z-index: 2;
    pointer-events: none;
}

.envelope-postmark::before {
    content: '';
    position: absolute;
    top: 50%; left: -20px; right: -20px;
    height: 2px;
    background: rgba(0,0,0,0.15);
    transform: rotate(-15deg);
}

.envelope-postmark::after {
    content: '';
    position: absolute;
    top: 60%; left: -15px; right: -15px;
    height: 2px;
    background: rgba(0,0,0,0.15);
    transform: rotate(-15deg);
}
"""

with open('styles.css', 'a', encoding='utf-8') as f:
    f.write(css)
print("Skeuomorphic CSS added")
