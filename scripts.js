/* ==========================================================================
   FOTOFILTRY.CZ — STANDALONE ENGINE v1.0
   Logic: Shopping Cart, Interactive Canvas Prism Animation, Form Submissions
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    /* ── 0. HAMBURGER MENU & MOBILNÍ NAVIGACE ── */
    var hamburgerBtn = document.getElementById('mobile-menu-trigger');
    var mobileNav = document.getElementById('mobile-nav-overlay');
    var mobileNavLinks = document.querySelectorAll('.mobile-nav-links a');

    if (hamburgerBtn && mobileNav) {
        function toggleMenu() {
            hamburgerBtn.classList.toggle('is-active');
            mobileNav.classList.toggle('is-active');
            document.body.style.overflow = mobileNav.classList.contains('is-active') ? 'hidden' : '';
        }
        hamburgerBtn.addEventListener('click', toggleMenu);

        mobileNavLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                hamburgerBtn.classList.remove('is-active');
                mobileNav.classList.remove('is-active');
                document.body.style.overflow = '';
            });
        });
    }

    /* ── 0.5 SCROLL REVEAL ANIMACE ── */
    var revealElements = document.querySelectorAll('.reveal-up');
    if ('IntersectionObserver' in window) {
        var revealObserver = new IntersectionObserver(function (entries, obs) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-revealed');
                    obs.unobserve(entry.target);
                }
            });
        }, { root: null, rootMargin: '0px 0px -50px 0px', threshold: 0.1 });
        revealElements.forEach(function (el) { revealObserver.observe(el); });
    } else {
        revealElements.forEach(function (el) { el.classList.add('is-revealed'); });
    }

    /* ── 1. DYNAMICKÝ ROK V PATIČCE ── */
    var yearEl = document.getElementById('current-year');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    /* ── 2. STATE KOŠÍKU ── */
    var cart = [];
    var cartCounter = document.getElementById('cart-counter');
    var cartDrawer = document.getElementById('cart-drawer');
    var cartOverlay = document.getElementById('cart-overlay');
    var cartTrigger = document.getElementById('cart-trigger');
    var cartClose = document.getElementById('cart-close');
    var cartItemsContainer = document.getElementById('cart-items-container');
    var cartTotalPrice = document.getElementById('cart-total-price');
    var checkoutBtn = document.getElementById('cart-checkout');

    // Načtení z localStorage
    try {
        var savedCart = localStorage.getItem('fotofiltry_cart');
        if (savedCart) {
            cart = JSON.parse(savedCart);
            updateCartUI();
        }
    } catch (e) {
        console.error('Nelze načíst košík:', e);
    }

    // Otevření / zavření košíku
    function toggleCart(open) {
        if (open) {
            cartDrawer.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden'; // block scroll
        } else {
            cartDrawer.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }
    }

    cartTrigger.addEventListener('click', function () { toggleCart(true); });
    cartClose.addEventListener('click', function () { toggleCart(false); });
    cartOverlay.addEventListener('click', function () { toggleCart(false); });

    // Generalized Add to Cart helper supporting variants and sizes
    window.addToCart = function (id, name, price, img, variant, size, quantity) {
        quantity = quantity || 1;
        variant = variant || 'Classic';
        size = size || '77 mm';

        // Create a unique composite key for the variant/size combination
        var variantKey = variant.replace(/[^a-zA-Z0-9]/g, '');
        var sizeKey = size.replace(/[^a-zA-Z0-9]/g, '');
        var cartItemId = id + '-' + variantKey + '-' + sizeKey;

        var displayName = name + ' (' + variant + ', ' + size + ')';

        var existingItem = cart.find(function (item) { return item.id === cartItemId; });
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({
                id: cartItemId,
                productId: id,
                name: displayName,
                price: price,
                img: img,
                quantity: quantity,
                variant: variant,
                size: size
            });
        }

        saveCart();
        updateCartUI();
        toggleCart(true); // Open drawer on addition
    };

    // Přidání do košíku z úvodní strany (homepage fallback se 77mm a výchozí variantou)
    document.querySelectorAll('.add-to-cart-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.stopPropagation(); // prevent navigation on card click
            e.preventDefault();
            var id = this.getAttribute('data-id');
            var name = this.getAttribute('data-name');
            var price = parseInt(this.getAttribute('data-price'), 10);
            var img = this.getAttribute('data-img');

            // Map default variants for quick add
            var defaultVariant = 'Classic';
            if (id === 'kaleidoscope') defaultVariant = 'Classic (5-Prizma)';
            else if (id === 'fog') defaultVariant = 'Fog Classic (1/2)';
            else if (id === 'halo') defaultVariant = 'Halo Classic (Neutrální)';

            window.addToCart(id, name, price, img, defaultVariant, '77 mm', 1);
        });
    });

    // Povolení prokliku na detail z celé produktové karty na úvodní straně
    document.querySelectorAll('.product-card').forEach(function (card) {
        card.addEventListener('click', function (e) {
            // Ignorujeme navigaci, pokud uživatel klikl přímo na "Do košíku" tlačítko
            if (e.target.closest('.add-to-cart-btn')) return;

            var link = this.querySelector('a.product-card-link') || this.querySelector('a');
            if (link && link.href) {
                window.location.href = link.href;
            }
        });
    });

    function saveCart() {
        try {
            localStorage.setItem('fotofiltry_cart', JSON.stringify(cart));
        } catch (e) {
            console.error('Nelze uložit košík:', e);
        }
    }

    function updateCartUI() {
        // Počítadlo v hlavičce
        var totalItems = cart.reduce(function (acc, item) { return acc + item.quantity; }, 0);
        cartCounter.textContent = totalItems;

        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p class="cart-empty-message">Košík je prázdný.</p>';
            cartTotalPrice.textContent = '0 Kč';
            return;
        }

        // Vykreslení položek
        cartItemsContainer.innerHTML = '';
        var totalSum = 0;

        cart.forEach(function (item) {
            var itemTotal = item.price * item.quantity;
            totalSum += itemTotal;

            var itemEl = document.createElement('div');
            itemEl.className = 'cart-item';
            itemEl.innerHTML =
                '<img src="' + item.img + '" alt="' + item.name + '" class="cart-item-img" loading="lazy" onerror="this.src=\'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?auto=format&fit=crop&w=80&q=80\'">' +
                '<div class="cart-item-details">' +
                '<h4>' + item.name + '</h4>' +
                '<p>' + item.quantity + '× ' + item.price + ' Kč</p>' +
                '</div>' +
                '<button class="cart-item-remove" data-id="' + item.id + '">×</button>';

            // Tlačítko smazat
            itemEl.querySelector('.cart-item-remove').addEventListener('click', function () {
                removeItem(item.id);
            });

            cartItemsContainer.appendChild(itemEl);
        });

        cartTotalPrice.textContent = totalSum.toLocaleString() + ' Kč';
    }

    function removeItem(id) {
        cart = cart.filter(function (item) { return item.id !== id; });
        saveCart();
        updateCartUI();
    }

    // Prefill contact form from checkout redirect on page load
    if (window.location.hash === '#kontakt') {
        var prefillMsg = localStorage.getItem('checkout_prefill_msg');
        if (prefillMsg) {
            var msgInput = document.getElementById('form-message');
            if (msgInput) {
                msgInput.value = prefillMsg;
                localStorage.removeItem('checkout_prefill_msg');
                setTimeout(function () {
                    msgInput.focus();
                }, 500);
            }
        }
    }

    // Load Stripe.js dynamically
    var stripeScript = document.createElement('script');
    stripeScript.src = 'https://js.stripe.com/v3/';
    document.head.appendChild(stripeScript);

    /* ── 3. KONTAKTNÍ FORMULÁŘ (Úvodní strana) ── */
    var contactForm = document.getElementById('order-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var btn = document.getElementById('form-submit');
            var fb = document.getElementById('form-feedback');
            btn.textContent = 'Odesílám...';
            btn.disabled = true;

            // Prozatimní demo odeslání pro čistě kontaktní zprávy
            setTimeout(function () {
                fb.className = 'form-feedback success';
                fb.textContent = 'Zpráva byla úspěšně odeslána. Brzy se vám ozveme.';
                contactForm.reset();
                btn.textContent = 'Odeslat poptávku';
                btn.disabled = false;
            }, 1000);
        });
    }

    /* ── 3.5 CHECKOUT FORMULÁŘ PŘÍMO V KOŠÍKU (STRIPE PLATBA) ── */
    var checkoutSubmitBtn = document.getElementById('cart-checkout-submit');
    var checkoutFeedback = document.getElementById('checkout-feedback');

    if (checkoutSubmitBtn) {
        checkoutSubmitBtn.addEventListener('click', function (e) {
            e.preventDefault();
            var name = document.getElementById('checkout-name').value;
            var email = document.getElementById('checkout-email').value;
            var phone = document.getElementById('checkout-phone').value;
            var zasilkovnaId = document.getElementById('checkout-zasilkovna-id').value;
            var zasilkovnaName = document.getElementById('checkout-zasilkovna-name').value;
            var termsChecked = document.getElementById('checkout-terms').checked;

            if (cart.length === 0) {
                checkoutFeedback.className = 'form-feedback error';
                checkoutFeedback.style.color = 'var(--danger)';
                checkoutFeedback.textContent = 'Košík je prázdný.';
                return;
            }
            if (!name || !email || !phone) {
                checkoutFeedback.className = 'form-feedback error';
                checkoutFeedback.style.color = 'var(--danger)';
                checkoutFeedback.textContent = 'Vyplňte prosím všechny kontaktní údaje.';
                return;
            }
            if (!zasilkovnaId) {
                checkoutFeedback.className = 'form-feedback error';
                checkoutFeedback.style.color = 'var(--danger)';
                checkoutFeedback.textContent = 'Vyberte prosím pobočku Zásilkovny.';
                return;
            }
            if (!termsChecked) {
                checkoutFeedback.className = 'form-feedback error';
                checkoutFeedback.style.color = 'var(--danger)';
                checkoutFeedback.textContent = 'Musíte souhlasit s obchodními podmínkami.';
                return;
            }

            // Lock submit button
            checkoutSubmitBtn.disabled = true;
            checkoutSubmitBtn.textContent = 'Připravuji platbu...';
            checkoutFeedback.className = 'form-feedback';
            checkoutFeedback.textContent = '';

            var checkoutItems = cart.map(function (item) {
                return { id: item.id, quantity: item.quantity };
            });

            // Call Netlify checkout API
            fetch('/.netlify/functions/checkout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    phone: phone,
                    zasilkovnaId: zasilkovnaId,
                    message: 'Objednávka z pokladny',
                    shipping_info: zasilkovnaName,
                    items: checkoutItems
                })
            })
                .then(function (res) {
                    if (!res.ok) {
                        return res.json().then(function (err) { throw new Error(err.error || 'Checkout API error'); });
                    }
                    return res.json();
                })
                .then(function (data) {
                    if (!window.Stripe) {
                        throw new Error('Knihovna Stripe se nenačetla. Zkuste to prosím znovu.');
                    }

                    var stripe = Stripe(data.publishableKey);
                    var elements = stripe.elements();

                    // Build a premium minimalist card payment modal overlay
                    var modal = document.createElement('div');
                    modal.id = 'stripe-payment-modal';
                    modal.style.position = 'fixed';
                    modal.style.top = '0';
                    modal.style.left = '0';
                    modal.style.width = '100%';
                    modal.style.height = '100%';
                    modal.style.background = 'rgba(0, 0, 0, 0.85)';
                    modal.style.backdropFilter = 'blur(8px)';
                    modal.style.display = 'flex';
                    modal.style.justifyContent = 'center';
                    modal.style.alignItems = 'center';
                    modal.style.zIndex = '9999';
                    modal.style.fontFamily = "'Outfit', sans-serif";

                    modal.innerHTML =
                        '<div style="background:#121216; border:1px solid #22222a; border-radius:12px; padding:30px; width:100%; max-width:420px; box-shadow:0 20px 40px rgba(0,0,0,0.5); color:#f3f3f6; position:relative;">' +
                        '<button id="stripe-modal-close" style="position:absolute; top:20px; right:20px; background:none; border:none; color:#8e8e9f; font-size:1.5rem; cursor:pointer; line-height:1;">×</button>' +
                        '<h3 style="margin:0 0 10px 0; font-size:1.4rem; font-weight:700; color:#f3f3f6;">Dokončení platby</h3>' +
                        '<p style="margin:0 0 20px 0; font-size:0.9rem; color:#8e8e9f;">Celková částka: <strong style="color:#d68c3f;">' + data.totalAmountCzk + ' Kč</strong> (včetně poštovného 100 Kč)</p>' +
                        '<form id="stripe-card-form">' +
                        '<div style="margin-bottom:20px; text-align:left;">' +
                        '<label style="display:block; font-size:0.8rem; color:#8e8e9f; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.05em;">Platební karta</label>' +
                        '<div id="stripe-card-element" style="background:#1a1a22; border:1px solid #22222a; border-radius:6px; padding:12px 16px;"></div>' +
                        '<div id="stripe-card-errors" role="alert" style="color:#e65050; font-size:0.85rem; margin-top:8px;"></div>' +
                        '</div>' +
                        '<button type="submit" id="stripe-submit-payment" style="width:100%; background:#d68c3f; color:#000; border:none; border-radius:6px; padding:14px; font-weight:600; font-size:0.95rem; cursor:pointer; transition:all 0.2s ease;">Zaplatit a dokončit</button>' +
                        '</form>' +
                        '</div>';

                    document.body.appendChild(modal);

                    var style = {
                        base: {
                            color: '#f3f3f6',
                            fontFamily: "'Outfit', sans-serif",
                            fontSmoothing: 'antialiased',
                            fontSize: '16px',
                            '::placeholder': {
                                color: '#8e8e9f'
                            }
                        },
                        invalid: {
                            color: '#e65050',
                            iconColor: '#e65050'
                        }
                    };

                    var cardElement = elements.create('card', { style: style, hidePostalCode: true });
                    cardElement.mount('#stripe-card-element');

                    // Close Modal
                    document.getElementById('stripe-modal-close').addEventListener('click', function () {
                        document.body.removeChild(modal);
                        checkoutSubmitBtn.disabled = false;
                        checkoutSubmitBtn.textContent = 'Objednat a zaplatit';
                    });

                    // Form submit within modal
                    var cardForm = document.getElementById('stripe-card-form');
                    cardForm.addEventListener('submit', function (ev) {
                        ev.preventDefault();
                        var payBtn = document.getElementById('stripe-submit-payment');
                        payBtn.disabled = true;
                        payBtn.textContent = 'Zpracovávám platbu...';

                        stripe.confirmCardPayment(data.clientSecret, {
                            payment_method: {
                                card: cardElement,
                                billing_details: {
                                    name: name,
                                    email: email
                                }
                            }
                        })
                            .then(function (result) {
                                if (result.error) {
                                    document.getElementById('stripe-card-errors').textContent = result.error.message;
                                    payBtn.disabled = false;
                                    payBtn.textContent = 'Zaplatit a dokončit';
                                } else {
                                    if (result.paymentIntent.status === 'succeeded') {
                                        document.body.removeChild(modal);
                                        checkoutSubmitBtn.disabled = false;
                                        checkoutSubmitBtn.textContent = 'Objednat a zaplatit';

                                        checkoutFeedback.className = 'form-feedback success';
                                        checkoutFeedback.innerHTML = 'Děkujeme, ' + name + '! Objednávka byla zaplacena. Potvrzení a fakturu obdržíte e-mailem.';

                                        // Clear cart
                                        document.getElementById('cart-checkout-form').reset();
                                        cart = [];
                                        saveCart();
                                        updateCartUI();
                                    }
                                }
                            });
                    });
                })
                .catch(function (err) {
                    console.error(err);
                    checkoutSubmitBtn.disabled = false;
                    checkoutSubmitBtn.textContent = 'Objednat a zaplatit';
                    checkoutFeedback.className = 'form-feedback error';
                    checkoutFeedback.style.color = 'var(--danger)';
                    checkoutFeedback.textContent = 'Chyba při přípravě platby: ' + err.message;
                });
        });
    }

    /* ── 3.5 DYNAMICKÉ NAČÍTÁNÍ PRODUKTŮ A BLOGU Z DATABÁZE ── */
    function loadProductsData() {
        fetch('/products.json')
            .then(function (res) { return res.json(); })
            .then(function (products) {
                products.forEach(function (p) {
                    var card = null;
                    if (p.id === 'kaleidoscope') card = document.getElementById('card-kaleidoscope');
                    else if (p.id === 'fog') card = document.getElementById('card-fog');
                    else if (p.id === 'halo') card = document.getElementById('card-halo');

                    if (card) {
                        // 1. Nastavení ceny
                        var priceEl = card.querySelector('.product-price');
                        if (priceEl) priceEl.textContent = p.price;

                        // 2. Vstříknutí KOMPLETNÍHO plného HTML popisu ze starého Shoptetu
                        var descEl = card.querySelector('.product-desc');
                        if (descEl) {
                            descEl.innerHTML = p.description; // innerHTML, ať fungují odrážky a formátování!
                        }

                        // 3. Hlavní fotka
                        var imgEl = card.querySelector('.product-img');
                        if (imgEl && p.localImg) imgEl.src = p.localImg;

                        // 4. AUTOMATICKÉ VYTVOŘENÍ GALERIE (Pokud má produkt víc fotek)
                        if (p.images && p.images.length > 1) {
                            var imgWrap = card.querySelector('.card-image-wrap');

                            // Smažeme případnou starou lištu miniatur, ať se neduplikuje
                            var oldGallery = card.querySelector('.product-thumb-gallery');
                            if (oldGallery) oldGallery.remove();

                            // Vytvoříme flex kontejner pro miniatury pod hlavní fotkou
                            var galleryDiv = document.createElement('div');
                            galleryDiv.className = 'product-thumb-gallery';
                            galleryDiv.style.display = 'flex';
                            galleryDiv.style.gap = '5px';
                            galleryDiv.style.marginTop = '10px';
                            galleryDiv.style.overflowX = 'auto';

                            p.images.forEach(function (imgSrc) {
                                var thumb = document.createElement('img');
                                thumb.src = imgSrc;
                                thumb.style.width = '45px';
                                thumb.style.height = '45px';
                                thumb.style.objectFit = 'cover';
                                thumb.style.borderRadius = '4px';
                                thumb.style.cursor = 'pointer';
                                thumb.style.border = '1px solid #22222a';
                                thumb.loading = 'lazy';

                                // Interaktivní proklik - klik na miniaturu změní hlavní velkou fotku
                                thumb.addEventListener('click', function () {
                                    imgEl.src = imgSrc;
                                    var btn = card.querySelector('.add-to-cart-btn');
                                    if (btn) btn.setAttribute('data-img', imgSrc);
                                });

                                galleryDiv.appendChild(thumb);
                            });

                            imgWrap.appendChild(galleryDiv);
                        }

                        // 5. Update nákupního tlačítka
                        var btn = card.querySelector('.add-to-cart-btn');
                        if (btn) {
                            var priceVal = parseInt(p.price.replace(/[^0-9]/g, ''), 10) || 990;
                            btn.setAttribute('data-price', priceVal);
                            if (p.localImg) btn.setAttribute('data-img', p.localImg);

                            if (p.inStock === false) {
                                btn.disabled = true;
                                btn.textContent = 'Vyprodáno';
                                btn.style.background = '#22222a';
                                btn.style.color = '#8e8e9f';
                                btn.style.cursor = 'not-allowed';
                            } else {
                                btn.disabled = false;
                                btn.textContent = 'Do košíku';
                                btn.style.background = '';
                                btn.style.color = '';
                                btn.style.cursor = '';
                            }
                        }
                    }
                });
            })
            .catch(function (err) {
                console.error('Failed to load products.json:', err);
            });
    }

    // Packeta Widget v6 picker
    var zasilkovnaBtn = document.getElementById('zasilkovna-trigger-drawer');
    if (zasilkovnaBtn) {
        zasilkovnaBtn.addEventListener('click', function () {
            var apiKey = 'a90886c33e8b0a9c'; // Demo key or project apiKey
            Packeta.Widget.pick(apiKey, function (point) {
                if (point) {
                    document.getElementById('checkout-zasilkovna-id').value = point.id;
                    document.getElementById('checkout-zasilkovna-name').value = point.name + ', ' + point.street + ', ' + point.city;
                    document.getElementById('zasilkovna-info-drawer').textContent = 'Vybráno: ' + point.name + ' (' + point.street + ')';
                }
            }, {
                country: 'cz',
                language: 'cs'
            });
        });
    }

    // ── JOURNAL DETAIL MODAL LOGIC ──
    var journalModal = document.getElementById('journal-modal');
    var modalCloseBtn = document.getElementById('journal-modal-close');
    var modalImg = document.getElementById('modal-article-img');
    var modalMeta = document.getElementById('modal-article-meta');
    var modalTitle = document.getElementById('modal-article-title');
    var modalBody = document.getElementById('modal-article-body');

    function openArticleModal(post) {
        if (!journalModal) return;
        modalImg.src = post.image || '';
        modalImg.alt = post.title || '';
        modalMeta.textContent = post.date || '';
        modalTitle.textContent = post.title || '';
        modalBody.innerHTML = post.text || ''; // Full HTML content!

        journalModal.showModal();
        document.body.style.overflow = 'hidden'; // block page scroll

        // Přidání parametru do URL pro sdílení
        if (window.history.pushState) {
            var newUrl = new URL(window.location);
            newUrl.searchParams.set('article', post.slug || post.id);
            window.history.pushState({}, '', newUrl);
        }
    }

    if (modalCloseBtn && journalModal) {
        modalCloseBtn.addEventListener('click', function () {
            journalModal.close();
        });
    }

    if (journalModal) {
        // Unblock scroll when modal closes
        journalModal.addEventListener('close', function () {
            document.body.style.overflow = '';

            // Odstranění parametru article z URL při zavření
            if (window.history.pushState) {
                var newUrl = new URL(window.location);
                newUrl.searchParams.delete('article');
                window.history.pushState({}, '', newUrl);
            }
        });

        // Fallback for browsers without closedby support
        if (!('closedBy' in HTMLDialogElement.prototype)) {
            journalModal.addEventListener('click', function (event) {
                if (event.target !== journalModal) return;

                var rect = journalModal.getBoundingClientRect();
                var isDialogContent = (
                    rect.top <= event.clientY &&
                    event.clientY <= rect.top + rect.height &&
                    rect.left <= event.clientX &&
                    event.clientX <= rect.left + rect.width
                );

                if (!isDialogContent) {
                    journalModal.close();
                }
            });
        }
    }

    function loadBlogPosts() {
        var grid = document.querySelector('.journal-grid');
        if (!grid) return;

        fetch('/.netlify/functions/blog')
            .then(function (res) { return res.json(); })
            .then(function (posts) {
                if (!posts || posts.length === 0) return;

                grid.innerHTML = '';
                posts.forEach(function (post) {
                    // Extract plain text excerpt from HTML
                    var tempDiv = document.createElement('div');
                    tempDiv.innerHTML = post.text || '';
                    var plainText = tempDiv.textContent || tempDiv.innerText || '';
                    var excerpt = plainText;
                    if (excerpt.length > 140) {
                        excerpt = excerpt.substring(0, 137) + '...';
                    }

                    var card = document.createElement('article');
                    card.className = 'journal-card';
                    card.id = 'article-' + post.id;
                    card.style.cursor = 'pointer'; // Make entire card look clickable
                    card.innerHTML =
                        '<div class="journal-img-wrap">' +
                        '<img src="' + post.image + '" alt="' + post.title + '" class="journal-img" loading="lazy" onerror="this.src=\'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80\'">' +
                        '</div>' +
                        '<div class="journal-content">' +
                        '<span class="journal-meta">' + post.date + '</span>' +
                        '<h3 class="journal-card-title">' + post.title + '</h3>' +
                        '<p class="journal-excerpt">' + excerpt + '</p>' +
                        '<a href="#" class="read-more-link" onclick="event.preventDefault();">Číst dále →</a>' +
                        '</div>';

                    // Open modal on card click
                    card.addEventListener('click', function (e) {
                        e.preventDefault();
                        openArticleModal(post);
                    });

                    grid.appendChild(card);
                });

                // Otevření článku automaticky, pokud je v URL parametr
                var urlParams = new URLSearchParams(window.location.search);
                var articleParam = urlParams.get('article');
                if (articleParam) {
                    var postToOpen = posts.find(function (p) { return p.slug === articleParam || p.id === articleParam; });
                    if (postToOpen) {
                        // setTimeout zajišťuje, že se modal otevře až po správném vyrendrování
                        setTimeout(function () { openArticleModal(postToOpen); }, 100);
                    }
                }
            })
            .catch(function (err) {
                console.error('Failed to load blog posts:', err);
            });
    }

    // Run loaders
    loadProductsData();
    loadBlogPosts();

    /* ── 4. INTERAKTIVNÍ CANVAS PRISM ANIMACE ── */
    var canvas = document.getElementById('prism-canvas');
    if (canvas) {
        var ctx = canvas.getContext('2d');
        var mouse = { x: canvas.width / 2, y: canvas.height / 2, active: false };

        // Nastavení reálného rozlišení pro retina displeje
        function resizeCanvas() {
            var rect = canvas.getBoundingClientRect();
            canvas.width = rect.width * (window.devicePixelRatio || 1);
            canvas.height = rect.height * (window.devicePixelRatio || 1);
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        // Trackování myši
        canvas.addEventListener('mousemove', function (e) {
            var rect = canvas.getBoundingClientRect();
            mouse.x = (e.clientX - rect.left) * (window.devicePixelRatio || 1);
            mouse.y = (e.clientY - rect.top) * (window.devicePixelRatio || 1);
            mouse.active = true;
        });

        canvas.addEventListener('mouseleave', function () {
            mouse.active = false;
        });

        // Paprsky světla
        var particles = [];
        var numParticles = 40;

        for (var i = 0; i < numParticles; i++) {
            particles.push({
                x: 0,
                y: Math.random() * canvas.height,
                speed: 1.5 + Math.random() * 2,
                size: 1 + Math.random() * 1.5,
                angle: (Math.random() - 0.5) * 0.1
            });
        }

        // Kreslení scény
        function drawScene() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            var w = canvas.width;
            var h = canvas.height;
            var centerX = w / 2;
            var centerY = h / 2;
            var scale = w / 400; // měřítko podle velikosti canvasu

            // Výchozí bod pro světelný paprsek
            var lightSourceX = mouse.active ? mouse.x : centerX - 180 * scale;
            var lightSourceY = mouse.active ? mouse.y : centerY - 60 * scale;

            // 1. Nakreslit skleněný trojúhelník (Prism)
            var p1 = { x: centerX, y: centerY - 90 * scale };
            var p2 = { x: centerX - 90 * scale, y: centerY + 70 * scale };
            var p3 = { x: centerX + 90 * scale, y: centerY + 70 * scale };

            // Skleněné pozadí prismu
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.lineTo(p3.x, p3.y);
            ctx.closePath();

            var prismGrad = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
            prismGrad.addColorStop(0, 'rgba(255, 255, 255, 0.25)');
            prismGrad.addColorStop(1, 'rgba(214, 140, 63, 0.05)');
            ctx.fillStyle = prismGrad;
            ctx.fill();

            // 2. Kreslení světelných paprsků a refrakce
            // Vstupní bílé světlo
            ctx.beginPath();
            ctx.moveTo(lightSourceX, lightSourceY);
            ctx.lineTo(centerX - 30 * scale, centerY - 10 * scale);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.lineWidth = 3 * scale;
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#ffffff';
            ctx.stroke();
            ctx.shadowBlur = 0; // reset

            // Rozklad světla na spektrum za trojúhelníkem (refrakce)
            var colors = [
                'rgba(230, 80, 80, 0.65)',   // Červená
                'rgba(240, 160, 80, 0.65)',  // Oranžová
                'rgba(240, 240, 80, 0.65)',  // Žlutá
                'rgba(80, 200, 120, 0.65)',  // Zelená
                'rgba(80, 160, 240, 0.65)',  // Modrá
                'rgba(160, 80, 240, 0.65)'   // Fialová
            ];

            colors.forEach(function (color, index) {
                var offset = (index - 2.5) * 12 * scale;
                ctx.beginPath();
                ctx.moveTo(centerX - 30 * scale, centerY - 10 * scale);
                ctx.lineTo(centerX + 60 * scale, centerY + 20 * scale + offset * 0.3);
                ctx.lineTo(w, centerY + 40 * scale + offset * 2.5);
                ctx.strokeStyle = color;
                ctx.lineWidth = 4 * scale;
                ctx.stroke();
            });

            // Vykreslit obrysy prismy (skleněný lesk)
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.lineTo(p3.x, p3.y);
            ctx.closePath();
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.lineWidth = 2 * scale;
            ctx.stroke();

            // Světelné body v rozích
            ctx.beginPath();
            ctx.arc(p1.x, p1.y, 3 * scale, 0, Math.PI * 2);
            ctx.fillStyle = '#ffffff';
            ctx.fill();

            // Animování a kreslení prachových částic ve světle
            particles.forEach(function (p) {
                p.x += p.speed;
                p.y += Math.sin(p.x * 0.02) * 0.5 + p.angle;

                if (p.x > w) {
                    p.x = 0;
                    p.y = Math.random() * h;
                }

                // Vykreslit částici
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);

                // Částice svítí víc v oblasti spektra
                if (p.x > centerX) {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
                } else {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                }
                ctx.fill();
            });

            requestAnimationFrame(drawScene);
        }

        drawScene();
    }

    /* ── 5. DETAILEM PRODUKTU DYNAMICKÝ KONTROLER (product.html) ── */
    var productContentWrapper = document.getElementById('product-content-wrapper');
    if (productContentWrapper) {
        var urlParams = new URLSearchParams(window.location.search);
        var productId = urlParams.get('id') || 'kaleidoscope'; // Výchozí pokud chybí

        fetch('/products.json')
            .then(function (res) { return res.json(); })
            .then(function (products) {
                var currentProduct = products.find(function (p) { return p.id === productId; });
                if (!currentProduct) {
                    productContentWrapper.innerHTML =
                        '<div style="grid-column: 1 / -1; text-align: center; padding: 100px 0; color: var(--color-text-muted); font-family: var(--font-body);">' +
                        '<h2>Omlouváme se, produkt nebyl nalezen.</h2>' +
                        '<p style="margin-top: 10px;"><a href="index.html" class="back-link" style="color: var(--color-accent); font-weight: 800;">← Zpět na úvodní stranu</a></p>' +
                        '</div>';
                    return;
                }

                renderProductDetail(currentProduct);
            })
            .catch(function (err) {
                console.error('Nepodařilo se načíst data produktu:', err);
                productContentWrapper.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:100px 0; color: var(--color-text-muted);">Nepodařilo se načíst detail produktu. Zkuste to prosím znovu.</div>';
            });
    }

    function renderProductDetail(product) {
        var wrapper = document.getElementById('product-content-wrapper');
        if (!wrapper) return;

        // Nastavit název stránky a drobečkovou navigaci
        document.title = product.name + ' — Premium Filtr | Fotofiltry.cz';
        var breadcrumbCurrent = document.getElementById('breadcrumb-current');
        if (breadcrumbCurrent) breadcrumbCurrent.textContent = product.name;

        // Aktualizace SEO metadat (vyčištění HTML tagů pro čistý text)
        var metaDesc = document.querySelector('meta[name="description"]');
        var plainTextDesc = product.description.replace(/<[^>]+>/g, '').trim().substring(0, 155) + '...';
        if (metaDesc) metaDesc.setAttribute('content', plainTextDesc);

        // Helper funkce pro Open Graph tagy (sociální sítě)
        function setMetaTag(attr, attrValue, content) {
            var el = document.querySelector('meta[' + attr + '="' + attrValue + '"]');
            if (!el) {
                el = document.createElement('meta');
                el.setAttribute(attr, attrValue);
                document.head.appendChild(el);
            }
            el.setAttribute('content', content);
        }

        // Zajištění absolutní URL adresy pro obrázek (vyžadováno většinou sítí)
        var ogImage = product.images && product.images.length > 0 ? product.images[0] : (product.localImg || '');
        if (ogImage && !ogImage.startsWith('http')) ogImage = window.location.origin + '/' + ogImage;

        setMetaTag('property', 'og:title', product.name + ' | Fotofiltry.cz');
        setMetaTag('property', 'og:description', plainTextDesc);
        setMetaTag('property', 'og:image', ogImage);
        setMetaTag('property', 'og:url', window.location.href);

        // Výchozí hodnoty stavu
        var selectedVariant = product.variants && product.variants.length > 0 ? product.variants[0] : 'Classic';

        // Najít první velikost, která je skladem, případně vzít první v poli
        var selectedSizeObj = product.sizes && product.sizes.length > 0 ?
            (product.sizes.find(function (s) { return s.stock > 0; }) || product.sizes[0]) :
            { size: '77 mm', price: 990, stock: 5 };

        var selectedSize = selectedSizeObj.size;
        var selectedQuantity = 1;
        var activeImage = product.images && product.images.length > 0 ? product.images[0] : (product.localImg || 'images/kaleidoscope.png');

        // Sestavení galerie miniatur
        var thumbsHtml = '';
        if (product.images && product.images.length > 1) {
            product.images.forEach(function (img, index) {
                var activeClass = img === activeImage ? 'active' : '';
                thumbsHtml += '<img src="' + img + '" alt="' + product.name + ' náhled ' + (index + 1) + '" class="product-detail-thumb ' + activeClass + '" data-img="' + img + '">';
            });
        }

        // Sestavení výběru variant
        var variantsHtml = '';
        if (product.variants && product.variants.length > 0) {
            product.variants.forEach(function (v, index) {
                var activeClass = v === selectedVariant ? 'active' : '';
                variantsHtml += '<button class="variant-pill ' + activeClass + '" data-variant="' + v + '">' + v + '</button>';
            });
        }

        // Sestavení výběru velikostí
        var sizesHtml = '';
        if (product.sizes && product.sizes.length > 0) {
            product.sizes.forEach(function (s) {
                var activeClass = s.size === selectedSize ? 'active' : '';
                var disabledClass = s.stock === 0 ? 'disabled' : '';
                sizesHtml += '<button class="size-btn ' + activeClass + ' ' + disabledClass + '" data-size="' + s.size + '" data-price="' + s.price + '" data-stock="' + s.stock + '">' + s.size + '</button>';
            });
        }

        var initialPriceText = selectedSizeObj.price.toLocaleString() + ' Kč';

        var initialStockLabel = '';
        var initialStockClass = '';
        if (selectedSizeObj.stock > 3) {
            initialStockLabel = 'Skladem (' + selectedSizeObj.stock + ' ks)';
            initialStockClass = 'in-stock';
        } else if (selectedSizeObj.stock > 0) {
            initialStockLabel = 'Poslední kusy (' + selectedSizeObj.stock + ' ks)';
            initialStockClass = 'low-stock';
        } else {
            initialStockLabel = 'Dočasně vyprodáno (Dostupné na objednání)';
            initialStockClass = 'out-of-stock';
        }

        // Vložení kompletního HTML
        wrapper.innerHTML =
            '<!-- Left Visual Gallery (Smaller) -->' +
            '<div class="product-detail-visual" style="max-width: 450px; width: 100%;">' +
            '<div class="product-detail-main-image-wrap">' +
            '<img src="' + activeImage + '" alt="' + product.name + '" class="product-detail-main-img" id="main-detail-img" fetchpriority="high" style="transform: scale(1.0);">' +
            '</div>' +
            '<div class="product-detail-thumbs" id="detail-thumbs-container">' +
            thumbsHtml +
            '</div>' +
            '</div>' +

            '<!-- Right Info Block -->' +
            '<div class="product-detail-info">' +
            '<div class="product-detail-badge tw-text">Prémiová kvalita</div>' +
            '<span class="product-detail-category tw-text">Optické fotografické filtry</span>' +
            '<h1 class="product-detail-title tw-text">' + product.name + '</h1>' +
            '<div class="product-detail-price-wrap tw-text" id="detail-price">' + initialPriceText + '</div>' +

            '<!-- Premium Editorial Section (Description typing out) -->' +
            '<div class="premium-editorial-section" style="margin-top: 30px;">' +
            '<div class="editorial-block">' +
            '<h3 class="editorial-title tw-text">Příběh produktu</h3>' +
            '<div class="editorial-content" style="font-size: 16px; line-height: 1.6; opacity: 0.8;">' + product.description + '</div>' +
            '</div>' +
            '<div class="editorial-block">' +
            '<h3 class="editorial-title tw-text">Technická specifikace</h3>' +
            '<ul class="premium-specs-list">' +
            '<li><span>Optické sklo</span><strong>Schott B270 (vysoká propustnost)</strong></li>' +
            '<li><span>Konstrukce</span><strong>Slim hliníková slitina, anodizováno</strong></li>' +
            '<li><span>Mechanika</span><strong>Otočná obroučka pro plynulé natáčení</strong></li>' +
            '<li><span>Závit</span><strong>Standardní vnitřní fotografický</strong></li>' +
            '</ul>' +
            '</div>' +
            '</div>' +

            '<!-- Variant Selection -->' +
            (product.variants && product.variants.length > 0 ?
                '<div class="product-option-group">' +
                '<span class="product-option-label tw-text">Volba verze / efektu:</span>' +
                '<div class="product-variant-pills" id="detail-variants-container">' +
                variantsHtml +
                '</div>' +
                '</div>' : '') +

            '<!-- Size Selection -->' +
            (product.sizes && product.sizes.length > 0 ?
                '<div class="product-option-group">' +
                '<span class="product-option-label tw-text">Velikost (průměr závitu objektivu):</span>' +
                '<div class="product-size-grid" id="detail-sizes-container">' +
                sizesHtml +
                '</div>' +
                '</div>' : '') +

            '<!-- Stock Level -->' +
            '<div class="stock-status-wrapper">' +
            '<span class="stock-status-dot ' + initialStockClass + '" id="detail-stock-dot"></span>' +
            '<span id="detail-stock-text" style="font-size: 13px; font-weight: 800;">' + initialStockLabel + '</span>' +
            '</div>' +

            '<!-- Quantity and Add to Cart -->' +
            '<div class="product-add-to-cart-wrapper">' +
            '<div class="quantity-stepper">' +
            '<button class="stepper-btn" id="stepper-minus" style="font-weight:900;">-</button>' +
            '<input type="text" class="stepper-input" id="stepper-val" value="1" readonly>' +
            '<button class="stepper-btn" id="stepper-plus" style="font-weight:900;">+</button>' +
            '</div>' +
            '<button class="detail-add-btn ' + (selectedSizeObj.stock === 0 ? 'disabled' : '') + '" id="detail-add-to-cart-btn" ' + (selectedSizeObj.stock === 0 ? 'disabled' : '') + ' style="width:100%;">Do košíku</button>' +
            '</div>' +
            '</div>';

        if (typeof TypewriterEngine !== 'undefined') {
            TypewriterEngine.init();
            TypewriterEngine.playSection(wrapper);
        }

        // ── AKCE A INTERAKCE NA DETAILU PRODUKTU ──

        // 1. Přepínání miniatur v galerii
        var mainImg = document.getElementById('main-detail-img');
        var thumbs = wrapper.querySelectorAll('.product-detail-thumb');
        thumbs.forEach(function (thumb) {
            thumb.addEventListener('click', function () {
                thumbs.forEach(function (t) { t.classList.remove('active'); });
                this.classList.add('active');
                var newImg = this.getAttribute('data-img');
                mainImg.src = newImg;
                activeImage = newImg;
            });
        });

        // 2. Výběr varianty (pills)
        var varPills = wrapper.querySelectorAll('.variant-pill');
        varPills.forEach(function (pill) {
            pill.addEventListener('click', function () {
                varPills.forEach(function (p) { p.classList.remove('active'); });
                this.classList.add('active');
                selectedVariant = this.getAttribute('data-variant');
            });
        });

        // 3. Výběr velikosti
        var sizeBtns = wrapper.querySelectorAll('.size-btn');
        var priceDisplay = document.getElementById('detail-price');
        var stockDot = document.getElementById('detail-stock-dot');
        var stockText = document.getElementById('detail-stock-text');
        var addToCartBtn = document.getElementById('detail-add-to-cart-btn');

        sizeBtns.forEach(function (btn) {
            btn.addEventListener('click', function () {
                if (this.classList.contains('disabled')) return;

                sizeBtns.forEach(function (b) { b.classList.remove('active'); });
                this.classList.add('active');

                selectedSize = this.getAttribute('data-size');
                var price = parseInt(this.getAttribute('data-price'), 10);
                var stock = parseInt(this.getAttribute('data-stock'), 10);

                priceDisplay.textContent = price.toLocaleString() + ' Kč';

                // Update stavu skladu a tlačítka košíku
                stockDot.className = 'stock-status-dot';
                if (stock > 3) {
                    stockText.textContent = 'Skladem (' + stock + ' ks)';
                    stockDot.classList.add('in-stock');
                    addToCartBtn.disabled = false;
                    addToCartBtn.classList.remove('disabled');
                } else if (stock > 0) {
                    stockText.textContent = 'Poslední kusy (' + stock + ' ks)';
                    stockDot.classList.add('low-stock');
                    addToCartBtn.disabled = false;
                    addToCartBtn.classList.remove('disabled');
                } else {
                    stockText.textContent = 'Dočasně vyprodáno (Dostupné na objednání)';
                    stockDot.classList.add('out-of-stock');
                    addToCartBtn.disabled = true;
                    addToCartBtn.classList.add('disabled');
                }
            });
        });

        // 4. Stepper množství
        var stepperMinus = document.getElementById('stepper-minus');
        var stepperPlus = document.getElementById('stepper-plus');
        var stepperVal = document.getElementById('stepper-val');

        stepperMinus.addEventListener('click', function () {
            if (selectedQuantity > 1) {
                selectedQuantity--;
                stepperVal.value = selectedQuantity;
            }
        });

        stepperPlus.addEventListener('click', function () {
            selectedQuantity++;
            stepperVal.value = selectedQuantity;
        });

        // 6. Klik na přidání do košíku
        addToCartBtn.addEventListener('click', function () {
            var currentSizeObj = product.sizes.find(function (s) { return s.size === selectedSize; }) || { price: 990 };
            var currentPrice = currentSizeObj.price;

            window.addToCart(
                product.id,
                product.name,
                currentPrice,
                activeImage,
                selectedVariant,
                selectedSize,
                selectedQuantity
            );
        });
    }
    // --- Globální IndianaJonesEngine Blueprint Background ---
    if (!document.getElementById('indiana-background')) {
        var canvas = document.createElement('canvas');
        canvas.id = 'indiana-background';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.zIndex = '-1';
        canvas.style.pointerEvents = 'none';
        document.body.prepend(canvas);

        var script = document.createElement('script');
        script.type = 'module';
        script.textContent = "import { IndianaEngine } from './IndianaJonesEngine.js';\n" +
                             "const canvas = document.getElementById('indiana-background');\n" +
                             "new IndianaEngine(canvas);";
        document.body.appendChild(script);
    }
});

// ── ROTARY ENGINE ──
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.getElementById('rotary-wrapper');
    if (!wrapper) return;

    // Zapojení všech rotujících sekcí, včetně kolekce
    const sections = Array.from(document.querySelectorAll('.rotary-section'));
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
        TypewriterEngine.resetSection(currentSection);
        TypewriterEngine.playSection(nextSection);

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
            setTimeout(()=>TypewriterEngine.playSection(sec), 500);
        }
    });
});


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


