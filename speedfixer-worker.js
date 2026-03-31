// MetricLogic SpeedFixer PSI proxy — API key stored as Worker secret, never exposed.

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS },
  });
}

function clientIp(request) {
  return (
    request.headers.get('CF-Connecting-IP') ||
    request.headers.get('X-Forwarded-For')?.split(',')[0]?.trim() ||
    'unknown'
  );
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    if (request.method !== 'GET') {
      return jsonResponse({ error: 'Method not allowed' }, 405);
    }

    const url = new URL(request.url);
    const targetUrl = url.searchParams.get('url');

    if (!targetUrl || !targetUrl.startsWith('https://')) {
      return jsonResponse(
        { error: 'Missing or invalid url (must start with https://)' },
        400
      );
    }

    const site = targetUrl;
    const apiKey = env.PSI_API_KEY;
    if (!apiKey) {
      return new Response(JSON.stringify({ error: 'PSI_API_KEY not configured' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }
    console.log('API key present:', !!env.PSI_API_KEY);
    console.log('Fetching PSI for:', site);

    // const key = `ratelimit:${clientIP}`;
    // const last = await env.SPEEDFIXER_KV.get(key);
    // if (last) return new Response(JSON.stringify({ error: 'Rate limited' }), { status: 429, ... });
    // await env.SPEEDFIXER_KV.put(key, '1', { expirationTtl: 60 });

    const psiUrl = new URL('https://www.googleapis.com/pagespeedonline/v5/runPagespeed');
    psiUrl.searchParams.set('url', site);
    psiUrl.searchParams.set('strategy', 'mobile');
    psiUrl.searchParams.set('key', apiKey);

    try {
      const psiResponse = await fetch(psiUrl.toString());
      console.log('PSI response status:', psiResponse.status);
      const body = await psiResponse.text();
      let data;
      try {
        data = JSON.parse(body);
      } catch {
        data = null;
      }
      console.log('PSI data keys:', Object.keys(data || {}).join(', '));

      if (!psiResponse.ok) {
        return jsonResponse(
          { error: 'PageSpeed Insights API request failed', status: psiResponse.status },
          502
        );
      }

      const contentType =
        psiResponse.headers.get('Content-Type') || 'application/json; charset=utf-8';
      return new Response(body, {
        status: 200,
        headers: { ...CORS, 'Content-Type': contentType },
      });
    } catch (err) {
      console.log('PSI fetch error:', err.message);
      return jsonResponse(
        { error: 'PageSpeed Insights API unavailable or timed out' },
        502
      );
    }
  },
};
