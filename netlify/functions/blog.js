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

  if (event.httpMethod !== 'GET') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method Not Allowed' }) };
  }

  try {
    let posts = null;
    try {
      const store = getStore({ name: 'eshop-data', consistency: 'strong' });
      posts = await store.get('blog', { type: 'json' });

      if (!posts) {
        const blogPath = path.join(process.cwd(), 'blog.json');
        if (fs.existsSync(blogPath)) {
          posts = JSON.parse(fs.readFileSync(blogPath, 'utf8'));
        } else {
          posts = [];
        }
        await store.set('blog', JSON.stringify(posts));
      }
    } catch (blobError) {
      console.warn('Netlify Blobs not available, falling back to local files:', blobError.message);
      const blogPath = path.join(process.cwd(), 'blog.json');
      if (fs.existsSync(blogPath)) {
        posts = JSON.parse(fs.readFileSync(blogPath, 'utf8'));
      } else {
        posts = [];
      }
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(posts)
    };
  } catch (error) {
    console.error('Blog fetch error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal Server Error' })
    };
  }
};
