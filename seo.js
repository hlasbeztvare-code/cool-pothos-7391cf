export default async (request, context) => {
    const url = new URL(request.url);

    const isProduct = url.pathname.includes('/product.html');
    const isIndex = url.pathname === '/' || url.pathname === '/index.html';

    // Middleware běží pro produkty i blogové články na homepage
    if (!isProduct && !isIndex) {
        return context.next();
    }

    const productId = isProduct ? url.searchParams.get('id') : null;
    const articleId = isIndex ? url.searchParams.get('article') : null;

    if (!productId && !articleId) return context.next();

    // Získání původního (prázdného) HTML ze serveru Netlify
    const response = await context.next();
    let html = await response.text();

    try {
        if (isProduct && productId) {
            const productsUrl = new URL('/products.json', request.url);
            const productsRes = await fetch(productsUrl);
            const products = await productsRes.json();

            const product = products.find(p => p.id === productId);
            if (product) {
                const plainTextDesc = product.description.replace(/<[^>]+>/g, '').trim().substring(0, 155) + '...';
                const ogImage = product.images && product.images.length > 0 ? product.images[0] : (product.localImg || '');
                const fullOgImage = ogImage.startsWith('http') ? ogImage : `${url.origin}/${ogImage}`;

                html = html.replace('<title>Detail produktu | Fotofiltry.cz</title>', `<title>${product.name} — Premium Filtr | Fotofiltry.cz</title>`);
                html = html.replace('<meta name="description" content="Detail kreativního optického filtru s možností výběru rozměru a varianty. Navrženo pro nekompromisní filmový look.">', `<meta name="description" content="${plainTextDesc}">`);

                const ogTags = `
    <meta property="og:title" content="${product.name} | Fotofiltry.cz" />
    <meta property="og:description" content="${plainTextDesc}" />
    <meta property="og:image" content="${fullOgImage}" />
    <meta property="og:url" content="${request.url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${product.name} | Fotofiltry.cz" />
    <meta name="twitter:image" content="${fullOgImage}" />\n`;
                html = html.replace('</head>', `${ogTags}</head>`);
            }
        } else if (isIndex && articleId) {
            let posts = [];
            try {
                const blogUrl = new URL('/.netlify/functions/blog', request.url);
                const blogRes = await fetch(blogUrl);
                if (blogRes.ok) posts = await blogRes.json();
            } catch (e) {
                const fallbackUrl = new URL('/blog.json', request.url);
                const fallbackRes = await fetch(fallbackUrl);
                if (fallbackRes.ok) posts = await fallbackRes.json();
            }

            const post = posts.find(p => p.slug === articleId || p.id === articleId);
            if (post) {
                const plainTextDesc = post.text.replace(/<[^>]+>/g, '').trim().substring(0, 155) + '...';
                const fullOgImage = post.image.startsWith('http') ? post.image : `${url.origin}/${post.image}`;

                html = html.replace('<title>Fotofiltry.cz — Prémiové optické filtry pro moderní tvůrce</title>', `<title>${post.title} | Studio Journal</title>`);
                html = html.replace('<meta name="description" content="Filmový look a nekompromisní optická kvalita. Objevte kreativní fotofiltry PRISM, FOG a HALO navržené pro profesionální fotografy a filmaře.">', `<meta name="description" content="${plainTextDesc}">`);

                const ogTags = `
<meta property="og:title" content="${post.title} | Studio Journal" />
<meta property="og:description" content="${plainTextDesc}" />
<meta property="og:image" content="${fullOgImage}" />
<meta property="og:url" content="${request.url}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${post.title} | Studio Journal" />
<meta name="twitter:image" content="${fullOgImage}" />\n`;
                html = html.replace('</head>', `${ogTags}</head>`);
            }
        }
    } catch (error) {
        console.error("SEO Edge Function Error:", error);
    }

    // Vrácení modifikovaného HTML, které už bot dokáže zpracovat
    return new Response(html, {
        headers: { 'content-type': 'text/html;charset=UTF-8' }
    });
};

// Middleware zachytává product detail i úvodní stranu
export const config = { path: ["/product.html", "/", "/index.html"] };