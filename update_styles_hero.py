import os

css_styles = """
/* ── HERO ARTIFACTS DESK (Indiana Jones style) ── */
.hero-artifacts-desk {
    position: relative;
    width: 100%;
    height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.artifact-item {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.4s ease;
    cursor: pointer;
    z-index: 10;
}

.artifact-img {
    width: 280px;
    height: auto;
    filter: drop-shadow(0 25px 35px rgba(20, 10, 5, 0.3)) drop-shadow(0 5px 15px rgba(20, 10, 5, 0.2));
    transition: filter 0.4s ease, transform 0.4s ease;
}

.artifact-label {
    margin-top: 15px;
    font-family: 'Shadows Into Light', 'Caveat', 'Just Another Hand', cursive, sans-serif;
    font-size: 22px;
    color: rgba(43, 24, 16, 0.85);
    background: rgba(255, 255, 255, 0.4);
    padding: 4px 12px;
    border-radius: 4px;
    transform: rotate(-2deg);
    opacity: 0.8;
    transition: opacity 0.3s ease, transform 0.3s ease;
    border: 1px solid rgba(43, 24, 16, 0.1);
    box-shadow: 1px 2px 4px rgba(0,0,0,0.05);
}

.artifact-item:hover {
    z-index: 20;
    transform: scale(1.05) translateY(-10px) !important;
}

.artifact-item:hover .artifact-img {
    filter: drop-shadow(0 35px 45px rgba(20, 10, 5, 0.4)) drop-shadow(0 15px 25px rgba(20, 10, 5, 0.3));
}

.artifact-item:hover .artifact-label {
    opacity: 1;
    transform: rotate(0deg) scale(1.1);
}

/* Specific placements for the Indiana Jones scattered look */
.artifact-kaledo {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-8deg);
    z-index: 12;
}

.artifact-fog {
    top: 20%;
    left: 10%;
    transform: rotate(15deg);
    z-index: 11;
}

.artifact-halo {
    top: 35%;
    right: 5%;
    transform: rotate(-20deg);
    z-index: 13;
}

@media (max-width: 992px) {
    .hero-artifacts-desk {
        height: 600px;
    }
    .artifact-img {
        width: 200px;
    }
    .artifact-fog {
        top: 0;
        left: 5%;
    }
    .artifact-kaledo {
        top: 40%;
    }
    .artifact-halo {
        top: 75%;
        right: 15%;
    }
}
"""

with open('styles.css', 'a', encoding='utf-8') as f:
    f.write(css_styles)
print("Styles added.")
