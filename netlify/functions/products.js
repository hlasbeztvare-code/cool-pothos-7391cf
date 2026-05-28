const { getStore } = require('@netlify/blobs');
const fs = require('fs');
const path = require('path');

exports.handler = async function(event, context) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    const store = getStore({ name: 'eshop-data', consistency: 'strong' });
    let products = await store.get('products', { type: 'json' });

    if (!products) {
      // Fallback to local file if Blobs is empty
      const productsPath = path.join(process.cwd(), 'products.json');
      const productsData = fs.readFileSync(productsPath, 'utf8');
      products = JSON.parse(productsData);
      // Initialize store
      await store.set('products', JSON.stringify(products));
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(products)
    };
  } catch (error) {
    console.error('Products fetch error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal Server Error' })
    };
  }
};
