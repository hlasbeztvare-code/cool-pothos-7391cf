const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async function(event, context) {
  // Webhooky musí být POST
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const sig = event.headers['stripe-signature'];
  let stripeEvent;

  try {
    // Ověření, že požadavek skutečně pochází od Stripe (pomocí tajného klíče z .env)
    stripeEvent = stripe.webhooks.constructEvent(
      event.body, 
      sig, 
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    console.error(`⚠️ Webhook Error: ${err.message}`);
    return { statusCode: 400, body: `Webhook Error: ${err.message}` };
  }

  // Zpracování úspěšné platby
  if (stripeEvent.type === 'payment_intent.succeeded') {
    const paymentIntent = stripeEvent.data.object;
    
    // Zde máme všechna data, která jsme si do metadata uložili v checkout.js
    const metadata = paymentIntent.metadata;
    const customerEmail = metadata.email;
    const customerName = metadata.name;
    const items = JSON.parse(metadata.items || '[]');

    console.log(`✅ Úspěšná platba přijata od: ${customerName} (${customerEmail})`);
    console.log('📦 Objednané položky:', items);
    console.log('🚚 Doprava:', metadata.Doprava);
    
    // ---------------------------------------------------------
    // TODO: Zde napojíme odeslání e-mailu majiteli e-shopu
    // TODO: Zde napojíme Fakturoid pro automatické vytvoření faktury
    // ---------------------------------------------------------
  }

  // Stripe vyžaduje odpověď 200 OK, jinak bude webhook opakovat
  return { 
    statusCode: 200, 
    body: JSON.stringify({ received: true }) 
  };
};