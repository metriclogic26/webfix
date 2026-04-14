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
  headers.forEach((value, key) => { out[key.toLowerCase()] = value; });
  const setCookieAll = headers.getAll('set-cookie');
  if (setCookieAll && setCookieAll.length > 0) out['set-cookie'] = setCookieAll;
  return out;
}
export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }
    const url = new URL(request.url);
    const target = url.searchParams.get('url');
    const nofollow = url.searchParams.get('nofollow') === '1';
    if (!target || (!target.startsWith('https://') && !target.startsWith('http://'))) {
      return jsonResponse({ error: 'Missing or invalid url' }, 400);
    }
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 5000);
      const res = await fetch(target, {
        method: 'HEAD',
        signal: controller.signal,
        redirect: nofollow ? 'manual' : 'follow',
      });
      clearTimeout(timeout);
      return jsonResponse({ status: res.status, headers: headersToObject(res.headers) });
    } catch(e) {
      return jsonResponse({ error: 'Upstream fetch failed' }, 502);
    }
  },
};
