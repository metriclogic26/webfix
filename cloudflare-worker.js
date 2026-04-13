// HttpFixer Headers Proxy Worker
// Deploy at: Cloudflare Dashboard → Workers → headers-proxy → Edit Code

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const target = url.searchParams.get('url');
    const nofollow = url.searchParams.get('nofollow') === '1';

    if (!target) {
      return new Response(JSON.stringify({ error: 'Missing url parameter' }), {
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }

    try {
      const resp = await fetch(target, {
        redirect: nofollow ? 'manual' : 'follow',
        headers: { 'User-Agent': 'HttpFixer/1.0 (httpfixer.dev)' }
      });

      const headers = {};
      resp.headers.forEach((v, k) => { headers[k] = v; });
      // Set-Cookie has multiple values — forEach only returns the last one
      // Use getAll() to capture all Set-Cookie headers as an array
      const setCookieAll = resp.headers.getAll('set-cookie');
      if (setCookieAll && setCookieAll.length > 0) {
        headers['set-cookie'] = setCookieAll;
      }

      const result = {
        status: resp.status,
        headers: headers,
      };

      // Include body for HTML parsing (mixed content tool)
      if (!nofollow && url.searchParams.get('body') === '1') {
        try {
          result.body = await resp.text();
        } catch(e) {}
      }

      return new Response(JSON.stringify(result), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET',
        }
      });
    } catch(e) {
      return new Response(JSON.stringify({ error: e.message }), {
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }
  }
};
