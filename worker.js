// MetricLogic HeadersFixer CORS proxy — stateless, discards all requests immediately. No logging.

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
};

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

function headersToObject(headers) {
  const out = {};
  headers.forEach((value, key) => {
    out[key.toLowerCase()] = value;
  });
  // Set-Cookie can have multiple values — forEach only captures the last
  const setCookieAll = headers.getAll('set-cookie');
  if (setCookieAll && setCookieAll.length > 0) {
    out['set-cookie'] = setCookieAll;
  }
  return out;
}

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const url = new URL(request.url);
    const target = url.searchParams.get('url');

    if (!target || !target.startsWith('https://')) {
      return jsonResponse({ error: 'Missing or invalid url (must be https://)' }, 400);
    }

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 5000);
      const res = await fetch(target, {
        method: 'HEAD',
        signal: controller.signal,
      });
      clearTimeout(timeout);
      return jsonResponse({ headers: headersToObject(res.headers) });
    } catch {
      return jsonResponse({ error: 'Upstream fetch failed' }, 502);
    }
  },
};
