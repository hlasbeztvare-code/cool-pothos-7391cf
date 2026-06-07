(function () {
    const injectMasterDesign = () => {
        console.log("⚡ L-Code Dynamics: Odpaluji externí modul. Carousely drží, sklo svítí...");

        // 1. KROK: Čisté schování bočního panelu
        const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar') || document.querySelector('aside');
        if (sidebar) sidebar.style.setProperty('display', 'none', 'important');

        const contentBody = document.getElementById('content') || document.querySelector('.main-content') || document.querySelector('#content-wrapper');
        if (!contentBody) return;

        contentBody.style.setProperty('width', '100%', 'important');
        contentBody.style.setProperty('max-width', '100%', 'important');
        contentBody.style.setProperty('float', 'none', 'important');
        contentBody.style.setProperty('padding', '0', 'important');

        // 2. KROK: LCD CSS (Deep Glass & Animations)
        const styleHTML = `
        <style>
            .lcd-master-wrapper { width: 100% !important; box-sizing: border-box !important; font-family: system-ui, -apple-system, sans-serif !important; margin-bottom: 40px !important; clear: both !important; }
            .lcd-trust-row { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 30px !important; padding: 25px !important; background: rgba(255, 255, 255, 0.95) !important; border: 1px solid rgba(255, 107, 0, 0.25) !important; border-radius: 16px !important; box-shadow: 0 6px 30px rgba(255, 107, 0, 0.05) !important; width: 100% !important; box-sizing: border-box !important; }
            @media (max-width: 991px) { .lcd-trust-row { grid-template-columns: repeat(2, 1fr) !important; gap: 30px !important; } }
            @media (max-width: 575px) { .lcd-trust-row { grid-template-columns: 1fr !important; gap: 25px !important; } }
            .lcd-trust-item { display: flex !important; flex-direction: column !important; align-items: center !important; text-align: center !important; gap: 16px !important; }
            .lcd-trust-icon-box { width: 85px !important; height: 85px !important; display: flex !important; align-items: center !important; justify-content: center !important; transition: transform 0.4s ease !important; }
            .lcd-trust-item:hover .lcd-trust-icon-box { transform: translateY(-6px) scale(1.06) !important; }
            .lcd-trust-title { font-size: 16px !important; font-weight: 900 !important; color: #ff6b00 !important; text-transform: uppercase !important; margin: 0 0 6px 0 !important; letter-spacing: 1px !important; }
            .lcd-trust-desc { font-size: 13px !important; color: #363636 !important; line-height: 1.4 !important; margin: 0 !important; font-weight: 600 !important; }

            .lcd-marquee-wrapper { width: 100% !important; overflow: hidden !important; background: linear-gradient(90deg, rgba(0, 82, 148, 0.08) 0%, rgba(240, 246, 252, 0.4) 50%, rgba(0, 82, 148, 0.08) 100%) !important; backdrop-filter: blur(15px) !important; border-top: 1px solid rgba(0, 82, 148, 0.2) !important; border-bottom: 1px solid rgba(0, 82, 148, 0.2) !important; padding: 14px 0 !important; margin: 20px 0 35px 0 !important; box-sizing: border-box !important; display: flex !important; align-items: center !important; }
            .lcd-marquee-track { display: flex !important; width: max-content !important; animation: lcd-marquee-scroll 45s linear infinite !important; }
            .lcd-marquee-wrapper:hover .lcd-marquee-track { animation-play-state: paused !important; }
            .lcd-marquee-content { display: flex !important; align-items: center !important; gap: 60px !important; padding-right: 60px !important; white-space: nowrap !important; }
            .lcd-marquee-text { font-family: system-ui, -apple-system, sans-serif !important; font-size: 14px !important; font-weight: 700 !important; color: #005294 !important; letter-spacing: 0.5px !important; }
            .lcd-marquee-text stroke { color: #ff6b00 !important; font-weight: 900 !important; }
            @keyframes lcd-marquee-scroll { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }

            .lcd-integrated-container { display: flex !important; flex-direction: column !important; gap: 16px !important; width: 100% !important; }
            .lcd-grid-main { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 16px !important; width: 100% !important; }
            .lcd-grid-bottom { display: flex !important; justify-content: center !important; gap: 16px !important; width: 100% !important; }
            .lcd-grid-bottom .lcd-integrated-card { width: calc(25% - 12px) !important; }
            @media (max-width: 991px) { .lcd-grid-main { grid-template-columns: repeat(2, 1fr) !important; } .lcd-grid-bottom { flex-wrap: wrap !important; } .lcd-grid-bottom .lcd-integrated-card { width: calc(50% - 8px) !important; } }
            @media (max-width: 575px) { .lcd-grid-main { grid-template-columns: 1fr !important; } .lcd-grid-bottom .lcd-integrated-card { width: 100% !important; } }

            .lcd-integrated-card { text-decoration: none !important; box-sizing: border-box !important; display: block !important; padding: 35px 20px !important; border-radius: 14px !important; text-align: center !important; background: linear-gradient(135deg, rgba(255, 255, 255, 0.88) 0%, rgba(242, 247, 252, 0.6) 100%) !important; backdrop-filter: blur(25px) saturate(190%) !important; border: 1px solid rgba(0, 82, 148, 0.18) !important; box-shadow: 0 4px 25px rgba(0, 82, 148, 0.02) !important, inset 0 1px 1px rgba(255, 255, 255, 0.95) !important; transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important; }
            .lcd-integrated-card:hover { transform: translateY(-7px) !important; background: linear-gradient(135deg, rgba(242, 247, 252, 0.95) 0%, rgba(0, 82, 148, 0.07) 100%) !important; border-color: rgba(0, 82, 148, 0.55) !important; box-shadow: 0 24px 35px rgba(0, 82, 148, 0.14) !important; }
            .lcd-hub-icon { height: 60px !important; display: flex !important; align-items: center !important; justify-content: center !important; margin-bottom: 14px !important; }
            .lcd-hub-text { font-size: 15px !important; margin: 0 0 8px 0 !important; font-weight: 800 !important; line-height: 1.2 !important; color: #005294 !important; }
            .lcd-hub-sub { font-size: 11px !important; color: #363636 !important; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; }
        </style>
        `;

        document.querySelectorAll('.lcd-master-wrapper, .lcd-marquee-wrapper').forEach(el => el.remove());
        if (!document.getElementById('lcd-dynamic-styles')) {
            const styleTag = document.createElement('div');
            styleTag.id = 'lcd-dynamic-styles';
            styleTag.innerHTML = styleHTML;
            document.head.appendChild(styleTag);
        }

        const trustRowHTML = `
        <div class="lcd-trust-row">
            <div class="lcd-trust-item"><div class="lcd-trust-icon-box"><svg width="85" height="85" viewBox="0 0 64 64" fill="none" stroke="#ff6b00" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="32 2 58 16 58 48 32 62 6 48 6 16" /><polygon points="32 14 46 24 46 40 32 50 18 40 18 24" stroke-width="1.5" stroke-dasharray="2 2" /><line x1="32" y1="2" x2="32" y2="62" stroke-width="1.5" /><line x1="6" y1="16" x2="58" y2="48" stroke-width="1" /><line x1="6" y1="48" x2="58" y2="16" stroke-width="1" /></svg></div><div class="lcd-trust-content"><h4 class="lcd-trust-title">Ušetříte</h4><p class="lcd-trust-desc">Skvělé ceny a kvalitní produkty pro každého svářeče.</p></div></div>
            <div class="lcd-trust-item"><div class="lcd-trust-icon-box"><svg width="85" height="85" viewBox="0 0 64 64" fill="none" stroke="#ff6b00" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="26" /><circle cx="32" cy="32" r="14" stroke-width="1.5" stroke-dasharray="4 2" /><circle cx="32" cy="32" r="6" fill="#ff6b00" /><path d="M32 2 L32 12 M32 52 L32 62 M2 32 H12 M52 32 H62" stroke-width="4" /><path d="M12 12 L20 20 M44 44 L52 52 M12 52 L20 44 M44 20 L52 52" stroke-width="1.5" /></svg></div><div class="lcd-trust-content"><h4 class="lcd-trust-title">Efektivita</h4><p class="lcd-trust-desc">Ušetříte čas i energii díky technice, která nezklame.</p></div></div>
            <div class="lcd-trust-item"><div class="lcd-trust-icon-box"><svg width="85" height="85" viewBox="0 0 64 64" fill="none" stroke="#ff6b00" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M32 6 L60 22 L32 38 L4 22 Z" /><path d="M4 22 L4 44 L32 60 L32 38 Z" /><path d="M32 38 L32 60 L60 44 L60 22 Z" /><path d="M14 12 C24 4 40 4 50 12" stroke-width="2" stroke-dasharray="3 3" /><path d="M4 30 C12 38 12 48 32 54" stroke-width="1.5" /></svg></div><div class="lcd-trust-content"><h4 class="lcd-trust-title">Dostupnost</h4><p class="lcd-trust-desc">Rychlé delivery. Většinu sortimentu máme trvale skladem.</p></div></div>
            <div class="lcd-trust-item"><div class="lcd-trust-icon-box"><svg width="85" height="85" viewBox="0 0 64 64" fill="none" stroke="#ff6b00" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 10 L32 2 L52 10 L52 34 C52 48 32 60 32 60 C32 60 12 48 12 34 Z" /><path d="M22 14 H42 V24 H22 Z" stroke-width="2" fill="#ff6b00" fill-opacity="0.1" /><path d="M32 24 V44" stroke-width="4" /><path d="M24 36 L32 44 L44 28" stroke-width="5" /></svg></div><div class="lcd-trust-content"><h4 class="lcd-trust-title">Spolehlivost</h4><p class="lcd-trust-desc">Vybíráme pro Vás stroje, kterým sami plně důvěřujeme.</p></div></div>
        </div>`;

        const marqueeHTML = `
        <div class="lcd-marquee-wrapper">
            <div class="lcd-marquee-track">
                <div class="lcd-marquee-content">
                    <span class="lcd-marquee-text">⚡ <stroke>Svářečky a svářecí technika</stroke> ALFA IN, OMICRON, KÜHTREIBER</span>
                    <span class="lcd-marquee-text">📞 Telefon: <stroke>603 912 644</stroke> (Každý den 7-21 h)</span>
                    <span class="lcd-marquee-text">✉️ E-mail: <stroke>info@cznaradi.cz</stroke></span>
                    <span class="lcd-marquee-text">🔥 Většina mašin s <stroke>prodlouženou zárukou</stroke> a <stroke>dopravou ZDARMA</stroke> po ČR</span>
                    <span class="lcd-marquee-text">🛠️ <stroke>Servis svářeček</stroke> v rámci ČR zajištěn včetně svozu – vždy se postaráme!</span>
                </div>
                <div class="lcd-marquee-content">
                    <span class="lcd-marquee-text">⚡ <stroke>Svářečky a svářecí technika</stroke> ALFA IN, OMICRON, KÜHTREIBER</span>
                    <span class="lcd-marquee-text">📞 Telefon: <stroke>603 912 644</stroke> (Každý den 7-21 h)</span>
                    <span class="lcd-marquee-text">✉️ E-mail: <stroke>info@cznaradi.cz</stroke></span>
                    <span class="lcd-marquee-text">🔥 Většina mašin s <stroke>prodlouženou zárukou</stroke> a <stroke>dopravou ZDARMA</stroke> po ČR</span>
                    <span class="lcd-marquee-text">🛠️ <stroke>Servis svářeček</stroke> v rámci ČR zajištěn včetně svozu – vždy se postaráme!</span>
                </div>
            </div>
        </div>`;

        const categoriesHTML = `
        <div class="lcd-integrated-container">
            <div class="lcd-grid-main">
                <a href="/svareci-invertory-mma/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="10" y="18" width="44" height="32" rx="4" /><path d="M18 18v-4a2 2 0 0 1 2-2h24a2 2 0 0 1 2 2v4M18 28h6M18 38h6" /><circle cx="44" cy="30" r="3" fill="#005294" /><path d="M40 42h8" /></svg></div><div class="lcd-hub-text">Svářecí invertory (MMA)</div><div class="lcd-hub-sub">Vstoupit &rarr;</div></a>
                <a href="/co2-svarecky-mig-mag/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="14" width="34" height="40" rx="4" /><circle cx="25" cy="26" r="6" /><path d="M42 22h10M48 18v22" /><path d="M30 44l14 10M14 14v-4h14" /></svg></div><div class="lcd-hub-text">CO2 svářečky (MIG/MAG)</div><div class="lcd-hub-sub">Vstoupit &rarr;</div></a>
                <a href="/tig-svarecky/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 50l26-26M30 20l8-8M34 24l8-8" /><path d="M38 16l14-14M44 10l4-4M6 58l6-6M46 6l12 12" /></svg></div><div class="lcd-hub-text">TIG svářečky</div><div class="lcd-hub-sub">Vstoupit &rarr;</div></a>
                <a href="/plazmove-rezacky/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 52l25-25M32 22l10-10M42 12l6-6" /><path d="M44 8l12 12-4 4-12-12Z" fill="#005294" fill-opacity="0.1" /><path d="M12 52l-6 6M48 6l10 10" /></svg></div><div class="lcd-hub-text">Plazmové řezačky</div><div class="lcd-hub-sub">Vstoupit &rarr;</div></a>
            </div>
            <div class="lcd-grid-main">
                <a href="/co2-horaky/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 48L32 32M24 24l22-22" stroke-width="3" /><path d="M42 10l12 12-4 4-12-12Z" /><path d="M10 54c4-4 8-2 12 2" stroke-width="1.5" /></svg></div><div class="lcd-hub-text">Hořáky a náhradní díly</div><div class="lcd-hub-sub">Zobrazit &rarr;</div></a>
                <a href="/kabely-pro-elektrodu/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 32c8-10 18-10 24 0s16 10 24 0" stroke-width="3.5" /><rect x="26" y="24" width="12" height="16" rx="2" fill="#005294" /><line x1="32" y1="20" x2="32" y2="24" /></svg></div><div class="lcd-hub-text">Svářecí kabely a kleště</div><div class="lcd-hub-sub">Zobrazit &rarr;</div></a>
                <a href="/elektrody-a-draty/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="22" stroke-dasharray="4 3" /><line x1="16" y1="48" x2="48" y2="16" stroke-width="4.5" /><line x1="24" y1="48" x2="48" y2="24" stroke-width="2" /><line x1="16" y1="40" x2="40" y2="16" stroke-width="2" /></svg></div><div class="lcd-hub-text">Dráty a elektrody</div><div class="lcd-hub-sub">Zobrazit &rarr;</div></a>
                <a href="/tlakove-lahve/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M24 22v26c0 5 3 8 8 8s8-3 8-8V22c0-7-3-9-8-9s-8 2-8 9Z" /><rect x="29" y="4" width="6" height="9" rx="1" fill="#005294" /><circle cx="32" cy="8.5" r="1.5" stroke="none" fill="#fff" /><path d="M24 30h16M24 40h16" stroke-width="1.5" /></svg></div><div class="lcd-hub-text">Tlakové lahve a plyn</div><div class="lcd-hub-sub">Zobrazit &rarr;</div></a>
            </div>
            <div class="lcd-grid-bottom">
                <a href="/spreje-pasty-pro-svarovani/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="22" y="18" width="20" height="38" rx="3" /><path d="M26 18v-5h12v5M32 8v5" /><path d="M32 26l-4 8h8l-4 8" fill="#005294" stroke="none" /></svg></div><div class="lcd-hub-text">Spreje, pasty a chemie</div><div class="lcd-hub-sub">Zobrazit &rarr;</div></a>
                <a href="/svareci-kukly-a-masky/" class="lcd-integrated-card"><div class="lcd-hub-icon"><svg width="55" height="55" viewBox="0 0 64 64" fill="none" stroke="#005294" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 12c12-3 24 0 36 0v20c0 14-12 20-18 22 C26 52 14 46 14 32V12Z" /><rect x="24" y="22" width="16" height="10" rx="2" fill="#005294" fill-opacity="0.15" /><path d="M20 12v10M44 12v10" stroke-width="1.5" /></svg></div><div class="lcd-hub-text">Svářecí kukly a masky</div><div class="lcd-hub-sub">Vstoupit &rarr;</div></a>
            </div>
        </div>`;

        const trustWrapper = document.createElement('div');
        trustWrapper.className = 'lcd-master-wrapper';
        trustWrapper.innerHTML = trustRowHTML;
        contentBody.insertBefore(trustWrapper, contentBody.firstChild);

        trustWrapper.insertAdjacentHTML('afterend', marqueeHTML);

        const productGrid = document.querySelector('.products') || document.querySelector('.index-products') || document.querySelector('.homepage-box');
        if (productGrid) {
            const categoriesWrapper = document.createElement('div');
            categoriesWrapper.className = 'lcd-master-wrapper';
            categoriesWrapper.innerHTML = categoriesHTML;
            productGrid.parentNode.insertBefore(categoriesWrapper, productGrid);
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectMasterDesign);
    } else {
        injectMasterDesign();
    }
