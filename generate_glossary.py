#!/usr/bin/env python3
"""Generate glossary pages for webfix.dev. Run: python3 generate_glossary.py"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://webfix.dev{canonical}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="MetricLogic">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="https://webfix.dev{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">{schema}</script>
  <style>
    :root {{
      --bg: #0B0D14; --surface: #12151F; --border: #252836;
      --purple: #6C63FF; --green: #22C55E; --orange: #F97316;
      --red: #EF4444; --text: #E2E4F0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: "JetBrains Mono", monospace; font-size: 14px; line-height: 1.6; min-height: 100vh; }}
    nav {{ display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); background: var(--surface); }}
    nav .brand {{ font-weight: 600; color: var(--text); text-decoration: none; }}
    nav .brand span {{ color: var(--purple); }}
    nav .right {{ display: flex; gap: 1rem; align-items: center; }}
    nav a {{ color: var(--text); text-decoration: none; opacity: 0.6; font-size: 13px; }}
    nav a:hover {{ color: var(--purple); opacity: 1; }}
    main {{ max-width: 760px; margin: 0 auto; padding: 2.5rem 1.5rem 4rem; }}
    main.wide {{ max-width: 1000px; }}
    .breadcrumb {{ font-size: 12px; color: var(--text); opacity: 0.5; margin-bottom: 1.5rem; }}
    .breadcrumb a {{ color: var(--purple); text-decoration: none; }}
    h1 {{ font-size: 1.75rem; font-weight: 600; line-height: 1.3; margin-bottom: 1rem; }}
    h2 {{ font-size: 1.1rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--text); }}
    p {{ margin-bottom: 1rem; opacity: 0.9; line-height: 1.7; }}
    .lead {{ font-size: 1.05rem; opacity: 0.95; margin-bottom: 1.25rem; }}
    .tool-cta {{ display: inline-block; margin: 1.5rem 0; padding: 0.75rem 1.25rem; background: var(--purple); color: white; text-decoration: none; border-radius: 6px; font-weight: 500; font-size: 14px; }}
    .tool-cta:hover {{ filter: brightness(1.1); }}
    .code-block {{ background: #080a0f; border: 1px solid var(--border); border-radius: 6px; padding: 1rem; font-size: 12px; margin: 1rem 0; overflow-x: auto; white-space: pre-wrap; word-break: break-word; }}
    footer {{ border-top: 1px solid var(--border); padding: 2rem 1.5rem; font-size: 12px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; opacity: 0.6; }}
    footer a {{ color: var(--text); text-decoration: none; }}
    .glossary-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
    .glossary-grid a {{ display: block; padding: 1rem 1.1rem; background: var(--surface); border: 1px solid var(--border); border-radius: 6px; color: var(--text); text-decoration: none; }}
    .glossary-grid a:hover {{ border-color: var(--purple); }}
    .glossary-grid .term-title {{ color: var(--purple); font-weight: 600; font-size: 13px; margin-bottom: 0.4rem; }}
    .glossary-grid .term-d {{ font-size: 12px; opacity: 0.8; line-height: 1.5; }}
    article a {{ color: var(--purple); }}
    .related-links {{ font-size: 12px; opacity: 0.7; margin: 1.5rem 0; }}
    .related-links a {{ color: var(--purple); text-decoration: none; }}
    @media (max-width: 600px) {{ nav .right {{ display: none; }} footer {{ flex-direction: column; text-align: center; }} }}
  </style>
</head>
<body>
  <nav>
    <a href="/" class="brand">WebFix <span>/</span> {nav_section}</a>
    <div class="right">
      <a href="/headers/">Headers</a>
      <a href="/cors/">CORS</a>
      <a href="/oauth/">OAuth</a>
      <a href="/csp/">CSP</a>
      <a href="/edge/">Edge</a>
      <a href="/speedfixer/">Speed</a>
    </div>
  </nav>
  <main class="{main_class}">
    <div class="breadcrumb">{breadcrumb}</div>
    <h1>{h1}</h1>
    {content}
    {related}
    <a href="{tool_url}" class="tool-cta">{tool_cta_text}</a>
  </main>
  <footer>
    <span>WebFix by MetricLogic · <a href="https://configclarity.dev">configclarity.dev</a> · <a href="https://domainpreflight.dev">domainpreflight.dev</a> · <a href="https://packagefix.dev">packagefix.dev</a></span>
    <span>MIT · <a href="https://github.com/metriclogic26/webfix">GitHub →</a></span>
  </footer>
</body>
</html>'''


def ld_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False)


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    elements = []
    for i, (name, url) in enumerate(items, start=1):
        if url:
            elements.append(
                {
                    "@type": "ListItem",
                    "position": i,
                    "name": name,
                    "item": f"https://webfix.dev{url}",
                }
            )
        else:
            elements.append({"@type": "ListItem", "position": i, "name": name})
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def faq_ld(pairs: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }


def defined_term_ld(name: str, description: str, page_url: str) -> dict:
    return {
        "@type": "DefinedTerm",
        "name": name,
        "description": description,
        "url": page_url,
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "name": "WebFix Security Glossary",
            "url": "https://webfix.dev/glossary/",
        },
    }


def bc_html(parts: list[tuple[str, str | None]]) -> str:
    out = []
    for label, href in parts:
        if href:
            out.append(f'<a href="{href}">{label}</a>')
        else:
            out.append(label)
    return " → ".join(out)


def related_block(links: list[tuple[str, str]], *, include_vs: bool = True) -> str:
    pairs = list(links)
    if include_vs:
        pairs.append(("WebFix vs securityheaders.com", "/vs/webfix-vs-securityheaders/"))
    parts = [f'<a href="{h}">{t}</a>' for t, h in pairs]
    inner = " · ".join(parts)
    return f'<div class="related-links"><span>Related:</span> {inner}</div>'


def glossary_term_related(slug: str) -> str:
    m: dict[str, list[tuple[str, str]]] = {
        "content-security-policy": [
            ("Fix CSP (Nginx)", "/fix/csp/nginx/"),
            ("CSP refused error", "/error/csp-refused-to-load/"),
        ],
        "hsts": [
            ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ("HSTS missing error", "/error/hsts-missing/"),
        ],
        "cors": [
            ("Fix CORS (Nginx)", "/fix/cors/nginx/"),
            ("CORS blocked error", "/error/cors-blocked/"),
        ],
        "preflight-request": [
            ("Fix CORS (Express)", "/fix/cors/express/"),
            ("CORS blocked error", "/error/cors-blocked/"),
        ],
        "csp-nonce": [
            ("Fix CSP (Vercel)", "/fix/csp/vercel/"),
            ("Fix CSP (Nginx)", "/fix/csp/nginx/"),
        ],
        "unsafe-inline": [
            ("Fix CSP (Nginx)", "/fix/csp/nginx/"),
            ("CSP refused error", "/error/csp-refused-to-load/"),
        ],
        "x-frame-options": [
            ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ("X-Frame-Options missing", "/error/x-frame-options-missing/"),
        ],
        "referrer-policy": [
            ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ("Fix headers (Apache)", "/fix/headers/apache/"),
        ],
        "permissions-policy": [
            ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ("Fix headers (Express)", "/fix/headers/express/"),
        ],
        "pkce": [
            ("Fix OAuth (Auth0)", "/fix/oauth/auth0/"),
            ("PKCE required error", "/error/pkce-required/"),
        ],
        "oauth-grant-types": [
            ("Fix OAuth (Auth0)", "/fix/oauth/auth0/"),
            ("invalid_grant error", "/error/invalid-grant/"),
        ],
        "cache-control": [
            ("Fix cache (Nginx)", "/fix/cache/nginx/"),
            ("Auth response cached", "/error/cache-authenticated-response/"),
        ],
        "vary-header": [
            ("Fix cache (Cloudflare)", "/fix/cache/cloudflare/"),
            ("Fix CORS (Nginx)", "/fix/cors/nginx/"),
        ],
        "etag": [
            ("Fix cache (Nginx)", "/fix/cache/nginx/"),
            ("EdgeFix", "/edge/"),
        ],
        "core-web-vitals": [
            ("Fix PageSpeed (Nginx)", "/fix/pagespeed/nginx/"),
            ("Cache policy error", "/error/pagespeed-cache-policy/"),
        ],
        "largest-contentful-paint": [
            ("Fix PageSpeed (Nginx)", "/fix/pagespeed/nginx/"),
            ("Render-blocking error", "/error/pagespeed-render-blocking/"),
        ],
        "cumulative-layout-shift": [
            ("Fix PageSpeed (Vercel)", "/fix/pagespeed/vercel/"),
            ("Fix PageSpeed (WordPress)", "/fix/pagespeed/wordpress/"),
        ],
        "interaction-to-next-paint": [
            ("Fix PageSpeed (Nginx)", "/fix/pagespeed/nginx/"),
            ("No compression error", "/error/pagespeed-no-compression/"),
        ],
        "time-to-first-byte": [
            ("Fix PageSpeed (Nginx)", "/fix/pagespeed/nginx/"),
            ("Fix cache (Cloudflare)", "/fix/cache/cloudflare/"),
        ],
        "coop-coep": [
            ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ("Fix headers (Express)", "/fix/headers/express/"),
        ],
    }
    return related_block(m.get(slug, [("Fix guides", "/fix/"), ("Errors", "/error/")]))


def write_glossary_page(
    slug: str,
    *,
    title: str,
    description: str,
    h1: str,
    content: str,
    tool_url: str,
    tool_cta: str,
    term_name: str,
    term_desc_short: str,
    faqs: list[tuple[str, str]],
    main_class: str = "",
    related: str = "",
) -> Path:
    canonical = f"/glossary/{slug}/"
    page_url = f"https://webfix.dev{canonical}"
    graph = [
        defined_term_ld(term_name, term_desc_short, page_url),
        breadcrumb_ld([("WebFix", "/"), ("Glossary", "/glossary/"), (term_name, "")]),
        faq_ld(faqs),
    ]
    schema_str = ld_json({"@context": "https://schema.org", "@graph": graph})
    html = (
        TEMPLATE.replace("{schema}", "__SCHEMA__")
        .format(
            title=title,
            description=description,
            canonical=canonical,
            nav_section="Glossary",
            breadcrumb=bc_html([("WebFix", "/"), ("Glossary", "/glossary/"), (term_name, None)]),
            h1=h1,
            content=content,
            tool_url=tool_url,
            tool_cta_text=tool_cta,
            main_class=main_class,
            related=related,
        )
        .replace("__SCHEMA__", schema_str)
    )
    out = ROOT / "glossary" / slug
    out.mkdir(parents=True, exist_ok=True)
    path = out / "index.html"
    path.write_text(html, encoding="utf-8")
    return path


def main() -> None:
    paths: list[Path] = []

    TERMS: list[dict] = [
        {
            "slug": "content-security-policy",
            "term_name": "Content Security Policy (CSP)",
            "title": "What is Content Security Policy (CSP)? — WebFix Glossary",
            "description": "CSP restricts which scripts, styles, and other resources a page may load—your main defense against XSS when applied strictly.",
            "h1": "Content Security Policy (CSP)",
            "short": "A browser security mechanism that restricts which resources a page can load.",
            "tool_url": "/csp/",
            "tool_cta": "Generate a CSP with CSPFixer →",
            "content": """
<p class="lead">A browser security mechanism that restricts which resources a page can load.</p>
<p>Content Security Policy is delivered as an HTTP header (or, less ideally, a <code>&lt;meta&gt;</code> tag). The browser compares every script, stylesheet, font, image, and connection against directives such as <code>script-src</code>, <code>style-src</code>, and <code>default-src</code>. Anything not allowed is blocked, which is why you see “refused to load” in DevTools when a CDN or inline snippet is missing from the policy.</p>
<h2>Why developers care</h2>
<p>A missing or loose CSP is the biggest single XSS attack surface on modern sites. If <code>script-src</code> allows <code>'unsafe-inline'</code> or <code>*</code>, an injected script runs as first-party code. A tight CSP forces you to list real origins, use nonces or hashes for the inline bits you truly need, and think about <code>frame-ancestors</code> for clickjacking. Production apps increasingly face audits and enterprise buyers who ask for CSP by name.</p>
<h2>Example</h2>
<div class="code-block">Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'</div>
<h2>Spec</h2>
<p><a href="https://www.w3.org/TR/CSP3/">W3C Content Security Policy Level 3</a></p>
""",
            "faqs": [
                (
                    "What happens if CSP blocks a legitimate script?",
                    "The browser refuses to run or load it and logs a violation. Add the origin to the right directive (e.g. script-src), use a nonce/hash for inline code, or serve the script from an already-allowed host.",
                ),
                (
                    "Is unsafe-inline safe in CSP?",
                    "No. 'unsafe-inline' for scripts removes most XSS protection. Prefer nonces with templating, or hashes for static inline blocks.",
                ),
            ],
        },
        {
            "slug": "hsts",
            "term_name": "HTTP Strict Transport Security (HSTS)",
            "title": "What is HSTS? — WebFix Glossary",
            "description": "HSTS tells browsers to use HTTPS only for your host, closing the first-visit downgrade gap.",
            "h1": "HTTP Strict Transport Security (HSTS)",
            "short": "Tells browsers to only connect to your site over HTTPS for a set period.",
            "tool_url": "/headers/",
            "tool_cta": "Audit headers with HeadersFixer →",
            "content": """
<p class="lead">Tells browsers to only connect to your site over HTTPS for a set period.</p>
<p>HSTS is a simple response header. Once the browser has seen it over a trusted HTTPS connection, it will upgrade or reject plain HTTP for that host (and optionally subdomains) until <code>max-age</code> expires. Preload lists let new users get protection even on the first visit, but only after you meet the preload requirements.</p>
<h2>Why developers care</h2>
<p>Without HSTS, a user’s first request might go over HTTP (bookmark, typo, captive portal, or active attacker). TLS alone does not stop that downgrade. HSTS closes the gap for return visits immediately and, with preload, shrinks the first-visit window. Security scanners flag missing HSTS as a standard finding; fixing it is usually one header line at the edge or in your app server.</p>
<h2>Example</h2>
<div class="code-block">Strict-Transport-Security: max-age=31536000; includeSubDomains; preload</div>
<h2>Spec</h2>
<p><a href="https://www.rfc-editor.org/rfc/rfc6797">RFC 6797</a> · <a href="https://hstspreload.org/">HSTS Preload</a></p>
""",
            "faqs": [
                (
                    "Can HSTS break local development?",
                    "Usually not if you use different hostnames. If you set includeSubDomains on a parent domain used for dev, you can pin yourself to HTTPS in ways you did not intend—use separate zones or shorter max-age in tests.",
                ),
                (
                    "Do I need preload?",
                    "Preload is optional. Start with a conservative max-age, prove HTTPS everywhere, then add preload only if all subdomains are ready for long-lived HTTPS-only behavior.",
                ),
            ],
        },
        {
            "slug": "cors",
            "term_name": "Cross-Origin Resource Sharing (CORS)",
            "title": "What is CORS? — WebFix Glossary",
            "description": "CORS is how browsers decide whether your API may be called from another origin—misconfigurations break SPAs daily.",
            "h1": "Cross-Origin Resource Sharing (CORS)",
            "short": "The browser mechanism that controls which origins can call your API.",
            "tool_url": "/cors/",
            "tool_cta": "Debug CORS with CORSFixer →",
            "content": """
<p class="lead">The browser mechanism that controls which origins can call your API.</p>
<p>CORS is not enforced by curl or server-to-server calls. It applies when browser JavaScript on origin A reads a response from origin B. The server must opt in with <code>Access-Control-Allow-Origin</code> (and often other <code>Access-Control-*</code> headers). The browser blocks the response body from reaching your JS if the check fails—even when the server returned 200.</p>
<h2>Why developers care</h2>
<p>Every SPA, Auth redirect flow, and public API hit from a browser crosses this path. Mis-set origins, credentials mode, or missing preflight handlers show up as “CORS error” with no stack trace. Fixing the API response headers (or proxying through same-origin) is the real solution; disabling CORS in the browser is not.</p>
<h2>Example</h2>
<div class="code-block">Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Credentials: true
Vary: Origin</div>
<h2>Spec</h2>
<p><a href="https://fetch.spec.whatwg.org/">Fetch Living Standard (CORS)</a></p>
""",
            "faqs": [
                (
                    "Why does Postman work but the browser fails?",
                    "Postman is not a browser and does not enforce CORS. Only browsers apply the Same-Origin Policy and CORS checks to cross-origin XHR/fetch.",
                ),
                (
                    "Is Access-Control-Allow-Origin: * with cookies valid?",
                    "No. When credentials are included, the wildcard origin is not allowed. The server must echo a specific allowed origin.",
                ),
            ],
        },
        {
            "slug": "preflight-request",
            "term_name": "CORS Preflight Request",
            "title": "What is a CORS preflight (OPTIONS)? — WebFix Glossary",
            "description": "Browsers send an OPTIONS request before non-simple cross-origin requests; your API must answer it correctly.",
            "h1": "CORS Preflight Request",
            "short": "An OPTIONS request the browser sends before a cross-origin request to check permissions.",
            "tool_url": "/cors/",
            "tool_cta": "Test preflight with CORSFixer →",
            "content": """
<p class="lead">An OPTIONS request the browser sends before a cross-origin request to check permissions.</p>
<p>“Simple” GET/HEAD/POST with safelisted headers skips preflight. Anything with custom headers, JSON content types, PUT/PATCH/DELETE, or credentials in certain combinations triggers a preflight: the browser sends <code>OPTIONS</code> with <code>Access-Control-Request-Method</code> and sometimes <code>Access-Control-Request-Headers</code>. The server answers with allowed methods and headers plus max-age for caching the result.</p>
<h2>Why developers care</h2>
<p>If your framework returns 404 for OPTIONS, or your gateway strips CORS on OPTIONS only, every mutating API call from the browser fails before the real request fires. Many “works in curl” bugs are missing preflight handlers. You also need <code>Vary: Origin</code> when responses differ by caller so CDNs do not cache one user’s CORS headers for everyone.</p>
<h2>Example</h2>
<div class="code-block">OPTIONS /api/profile HTTP/1.1
Host: api.example.com
Origin: https://app.example.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: authorization, content-type

HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, PUT, OPTIONS
Access-Control-Allow-Headers: authorization, content-type
Access-Control-Max-Age: 86400</div>
<h2>Spec</h2>
<p><a href="https://fetch.spec.whatwg.org/#cors-preflight-fetch">Fetch — CORS-preflight fetch</a></p>
""",
            "faqs": [
                (
                    "Why do I see two requests in DevTools?",
                    "The first is the OPTIONS preflight; the second is your real request. Both must succeed for the browser to expose the response to your JavaScript.",
                ),
                (
                    "Can I disable preflight?",
                    "You cannot disable it from the client for non-simple requests. You can sometimes redesign APIs to use simple requests—often not worth it versus fixing OPTIONS on the server.",
                ),
            ],
        },
        {
            "slug": "csp-nonce",
            "term_name": "CSP Nonce",
            "title": "What is a CSP nonce? — WebFix Glossary",
            "description": "A one-time token lets one inline script run under a strict script-src without unsafe-inline.",
            "h1": "CSP Nonce",
            "short": "A random value that allows a specific inline script to run despite a strict CSP.",
            "tool_url": "/csp/",
            "tool_cta": "Build CSP with CSPFixer →",
            "content": """
<p class="lead">A random value that allows a specific inline script to run despite a strict CSP.</p>
<p>A nonce (“number used once”) is generated per response on the server, embedded in the <code>Content-Security-Policy</code> header as <code>script-src 'nonce-…'</code>, and repeated on the matching <code>&lt;script&gt;</code> tag as <code>nonce="…"</code>. Only scripts carrying that nonce may execute as inline script. Dynamic frameworks (Next.js middleware, SSR templates) can rotate the value every request so leaked nonces from old pages expire quickly.</p>
<h2>Why developers care</h2>
<p>Strict <code>script-src</code> without <code>'unsafe-inline'</code> blocks legacy analytics snippets and framework hydration unless you use nonces or hashes. Nonces are the practical path when inline script content changes per user or request. Hashes work for byte-stable inline blocks only.</p>
<h2>Example</h2>
<div class="code-block">Content-Security-Policy: script-src 'self' 'nonce-rAnDm8xK9pQ2'

&lt;script nonce="rAnDm8xK9pQ2"&gt;
  console.log('This inline script is allowed.');
&lt;/script&gt;</div>
<h2>Spec</h2>
<p><a href="https://www.w3.org/TR/CSP3/#framework-directive-source-list">CSP3 — source lists (nonce)</a></p>
""",
            "faqs": [
                (
                    "Can I reuse the same nonce on every page?",
                    "You can, but a fresh nonce per response is stronger: it narrows the window if markup leaks and matches how most modern stacks implement CSP.",
                ),
                (
                    "Do third-party scripts support nonces?",
                    "Only if you inject their script tag with the nonce attribute from your template. Async third-party loaders that inject their own scripts need different patterns (proxy, hash allowlists, or separate isolated origins).",
                ),
            ],
        },
        {
            "slug": "unsafe-inline",
            "term_name": "unsafe-inline (CSP)",
            "title": "What does unsafe-inline mean in CSP? — WebFix Glossary",
            "description": "unsafe-inline allows arbitrary inline script and style—convenient and dangerous.",
            "h1": "<code>unsafe-inline</code> (CSP directive)",
            "short": "A CSP keyword that allows all inline scripts or styles — effectively disabling XSS protection.",
            "tool_url": "/csp/",
            "tool_cta": "Tighten CSP with CSPFixer →",
            "content": """
<p class="lead">A CSP keyword that allows all inline scripts or styles — effectively disabling XSS protection.</p>
<p>In <code>script-src</code>, <code>'unsafe-inline'</code> tells the browser to execute any inline <code>&lt;script&gt;</code> block or event handler–style injections the page contains. In <code>style-src</code>, it permits inline <code>&lt;style&gt;</code> and style attributes. It exists for legacy sites, not as a security control.</p>
<h2>Why developers care</h2>
<p>Most “we added CSP but nothing works” stories end with <code>'unsafe-inline'</code> in <code>script-src</code>. That silences violations by letting the attack succeed: reflected or stored XSS runs like normal code. The fix is to remove it, add nonces/hashes for the few inline bits you need, and move the rest to files. Until then your CSP is mostly theater.</p>
<h2>Example</h2>
<div class="code-block"># Weak — any injected &lt;script&gt; runs:
Content-Security-Policy: script-src 'self' 'unsafe-inline'

# Stronger — inline only with a matching nonce:
Content-Security-Policy: script-src 'self' 'nonce-abc123'</div>
<h2>Spec</h2>
<p><a href="https://www.w3.org/TR/CSP3/#keyword-unsafe-inline">CSP3 — 'unsafe-inline'</a></p>
""",
            "faqs": [
                (
                    "Is unsafe-inline OK for style-src only?",
                    "It is less catastrophic than script-src, but inline style can still aid data exfiltration and UI redress. Prefer hashes or refactor CSS.",
                ),
                (
                    "Does unsafe-eval matter too?",
                    "Yes. script-src 'unsafe-eval' allows eval() and similar constructs—another XSS amplifier. Remove it unless a library truly requires it.",
                ),
            ],
        },
        {
            "slug": "x-frame-options",
            "term_name": "X-Frame-Options",
            "title": "What is X-Frame-Options? — WebFix Glossary",
            "description": "Controls iframe embedding; still widely used alongside CSP frame-ancestors.",
            "h1": "X-Frame-Options",
            "short": "A header that controls whether your page can be embedded in an iframe.",
            "tool_url": "/headers/",
            "tool_cta": "Check headers with HeadersFixer →",
            "content": """
<p class="lead">A header that controls whether your page can be embedded in an iframe.</p>
<p><code>X-Frame-Options</code> is an older response header with three effective values: <code>DENY</code> (no framing), <code>SAMEORIGIN</code> (only same site), or <code>ALLOW-FROM uri</code> (legacy, poor support). Modern guidance prefers CSP’s <code>frame-ancestors</code>, which is more expressive, but many scanners still look for XFO first.</p>
<h2>Why developers care</h2>
<p>Without it (and without a restrictive <code>frame-ancestors</code>), an attacker can load your logged-in app in a hidden iframe and trick users into clicking actions they cannot see—classic clickjacking. Banking and admin UIs treat this as mandatory. Setting <code>DENY</code> or <code>SAMEORIGIN</code> is usually a one-line change at the reverse proxy.</p>
<h2>Example</h2>
<div class="code-block">X-Frame-Options: SAMEORIGIN

# Modern complement:
Content-Security-Policy: frame-ancestors 'self'</div>
<h2>Spec</h2>
<p><a href="https://tools.ietf.org/html/rfc7034">RFC 7034</a></p>
""",
            "faqs": [
                (
                    "X-Frame-Options or frame-ancestors?",
                    "Use frame-ancestors in CSP for fine-grained control. Keep XFO for defense in depth and older user agents that ignore CSP framing rules.",
                ),
                (
                    "Can I allow one partner to iframe my site?",
                    "XFO cannot express allowlists. Use CSP: frame-ancestors https://partner.example.",
                ),
            ],
        },
        {
            "slug": "referrer-policy",
            "term_name": "Referrer-Policy",
            "title": "What is Referrer-Policy? — WebFix Glossary",
            "description": "Controls how much URL leaks when users follow links or load subresources.",
            "h1": "Referrer-Policy",
            "short": "Controls how much URL information is sent in the Referer header to other sites.",
            "tool_url": "/headers/",
            "tool_cta": "Audit headers with HeadersFixer →",
            "content": """
<p class="lead">Controls how much URL information is sent in the <code>Referer</code> header to other sites.</p>
<p>When your page loads third-party analytics, fonts, or users click outbound links, the browser may send a <code>Referer</code> showing the full path and query string of the page they came from. <code>Referrer-Policy</code> (note the historic spelling) shrinks or removes that signal—per document, or inherited by subresources depending on policy.</p>
<h2>Why developers care</h2>
<p>Internal URLs, reset tokens in query strings, and PII in paths routinely leak to vendors you did not mean to trust with that detail. Compliance teams care; so should you. A sane default like <code>strict-origin-when-cross-origin</code> keeps same-origin diagnostics while stripping paths on cross-origin requests.</p>
<h2>Example</h2>
<div class="code-block">Referrer-Policy: strict-origin-when-cross-origin

# Stricter — no referrer on downgrades:
Referrer-Policy: no-referrer-when-downgrade</div>
<h2>Spec</h2>
<p><a href="https://www.w3.org/TR/referrer-policy/">W3C Referrer Policy</a></p>
""",
            "faqs": [
                (
                    "Does Referrer-Policy break OAuth redirects?",
                    "Rarely. OAuth flows rely on explicit redirect_uri parameters, not Referer. If you strip everything with no-referrer, debug third-party integrations case by case.",
                ),
                (
                    "meta referrer vs header?",
                    "Prefer the HTTP header for the whole origin. HTML meta tags are per-document fallbacks.",
                ),
            ],
        },
        {
            "slug": "permissions-policy",
            "term_name": "Permissions-Policy",
            "title": "What is Permissions-Policy? — WebFix Glossary",
            "description": "Feature policy successor—deny camera, mic, geolocation by default for embeds.",
            "h1": "Permissions-Policy",
            "short": "Restricts which browser features (camera, microphone, geolocation) a page can use.",
            "tool_url": "/headers/",
            "tool_cta": "Audit headers with HeadersFixer →",
            "content": """
<p class="lead">Restricts which browser features (camera, microphone, geolocation) a page can use.</p>
<p>Formerly called Feature Policy, <code>Permissions-Policy</code> declares which powerful APIs (camera, microphone, geolocation, payment, fullscreen, etc.) are available to your document and to cross-origin iframes you embed. Denying by default and allowlisting only what you need shrinks the blast radius when a third-party script goes rogue.</p>
<h2>Why developers care</h2>
<p>Marketing tags and support widgets often request capabilities you never intended to grant globally. A tight policy surfaces misuse early and satisfies security questionnaires that ask for “least privilege” on browser features. You set it once at the edge like any other security header.</p>
<h2>Example</h2>
<div class="code-block">Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(self)</div>
<h2>Spec</h2>
<p><a href="https://www.w3.org/TR/permissions-policy-1/">W3C Permissions Policy</a></p>
""",
            "faqs": [
                (
                    "Will Permissions-Policy break Google Maps embeds?",
                    "If you deny geolocation or fullscreen globally, embedded maps may lose features. Scope allowlists to paths or origins that need them.",
                ),
                (
                    "Difference from Prompt API consent?",
                    "The policy is a hard gate: disallowed features throw or fail silently before user prompts. It is defense in depth, not a replacement for UX permission prompts.",
                ),
            ],
        },
        {
            "slug": "pkce",
            "term_name": "Proof Key for Code Exchange (PKCE)",
            "title": "What is PKCE? — WebFix Glossary",
            "description": "PKCE protects public OAuth clients from authorization code interception.",
            "h1": "Proof Key for Code Exchange (PKCE)",
            "short": "An OAuth extension that prevents authorization code interception attacks.",
            "tool_url": "/oauth/",
            "tool_cta": "Fix OAuth with OAuthFixer →",
            "content": """
<p class="lead">An OAuth extension that prevents authorization code interception attacks.</p>
<p>Public clients (SPAs, mobile apps) cannot hold a client secret in the binary. An attacker who steals the authorization code from a redirect could exchange it at the token endpoint unless you bind the exchange to a secret only the real app knows. PKCE does that with <code>code_verifier</code> (random, 43–128 chars) and <code>code_challenge</code> (S256 hash of the verifier) sent on the authorize request, then the plaintext verifier on the token request.</p>
<h2>Why developers care</h2>
<p>OAuth 2.1 requires PKCE for public clients. Auth servers reject flows or emit insecure grants if you skip it. Desktop loopback and mobile custom-URL redirects are especially exposed to interception without PKCE. Server-side apps with secrets use confidential client mode, but PKCE is still recommended for defense in depth.</p>
<h2>Example</h2>
<div class="code-block"># Authorization request (query or body):
code_challenge_method=S256
code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM

# Token request:
grant_type=authorization_code
code=...
redirect_uri=...
client_id=...
code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk</div>
<h2>Spec</h2>
<p><a href="https://www.rfc-editor.org/rfc/rfc7636">RFC 7636</a></p>
""",
            "faqs": [
                (
                    "Does PKCE replace client secret for SPAs?",
                    "For public clients, yes—you should not ship a secret to the browser. PKCE proves possession without a static secret.",
                ),
                (
                    "What if code_verifier does not match?",
                    "The token endpoint returns invalid_grant. Ensure the same verifier is stored client-side until the callback completes.",
                ),
            ],
        },
        {
            "slug": "oauth-grant-types",
            "term_name": "OAuth 2.0 Grant Types",
            "title": "OAuth 2.0 grant types explained — WebFix Glossary",
            "description": "Authorization Code with PKCE, Client Credentials, Device Flow—pick the right one.",
            "h1": "OAuth 2.0 Grant Types",
            "short": "The different flows OAuth supports for obtaining access tokens.",
            "tool_url": "/oauth/",
            "tool_cta": "Debug OAuth with OAuthFixer →",
            "content": """
<p class="lead">The different flows OAuth supports for obtaining access tokens.</p>
<p>Grant types define how a client proves identity and obtains tokens. The authorization code grant (today always paired with PKCE for public clients) drives browser and mobile login. Client credentials serve machine-to-machine APIs with a stored secret. Device flow covers input-constrained TVs and printers. Implicit and password grants are deprecated for new work because they cannot protect refresh tokens or codes the same way.</p>
<h2>Why developers care</h2>
<p>Using client credentials from a SPA, or enabling implicit flow because a tutorial said so, creates audit findings and real account takeover paths. The wrong grant type also produces confusing errors—<code>unsupported_grant_type</code>, silent failures in iframes, or refresh tokens where they are forbidden.</p>
<h2>Example</h2>
<div class="code-block">Authorization Code + PKCE — user login in browser/mobile; auth code redeemed server-side or in app with PKCE verifier.

Client Credentials — backend job calls API with client_id + client_secret (no user context).

Device Flow — user visits verification URL on phone while device polls token endpoint with device_code.</div>
<h2>Spec</h2>
<p><a href="https://www.rfc-editor.org/rfc/rfc6749">RFC 6749</a> · <a href="https://oauth.net/2/grant-types/">OAuth.net — grant types</a></p>
""",
            "faqs": [
                (
                    "Which grant for a Next.js app?",
                    "Authorization code with PKCE, usually via the BFF pattern or a secure server component—not implicit in the browser.",
                ),
                (
                    "Can I use refresh tokens in SPAs?",
                    "Only with strict rotation, secure storage, and provider support. Many teams use HTTP-only cookies on a same-site backend instead.",
                ),
            ],
        },
        {
            "slug": "cache-control",
            "term_name": "Cache-Control",
            "title": "What is the Cache-Control header? — WebFix Glossary",
            "description": "Controls freshness and privacy of cached HTTP responses across browsers and CDNs.",
            "h1": "Cache-Control",
            "short": "An HTTP header that tells browsers and CDNs how long to cache a response.",
            "tool_url": "/edge/",
            "tool_cta": "Audit caching with EdgeFix →",
            "content": """
<p class="lead">An HTTP header that tells browsers and CDNs how long to cache a response.</p>
<p><code>Cache-Control</code> combines directives: <code>max-age</code>, <code>s-maxage</code> (shared caches), <code>private</code>, <code>no-store</code>, <code>immutable</code>, <code>stale-while-revalidate</code>, and more. Browsers and CDNs each interpret the tuple; middleware that strips or overrides it changes production behavior even when origin looks correct.</p>
<h2>Why developers care</h2>
<p>Wrong caching means either angry users on stale dashboards or serious bugs where a CDN serves one user’s HTML to another after a <code>private</code> miss. APIs that return JSON with auth cookies must usually send <code>no-store</code> or <code>private</code> explicitly. Static hashed assets want long <code>max-age</code> with <code>immutable</code> so PSI and real users stop revalidating bytes that never change.</p>
<h2>Example</h2>
<div class="code-block"># Fingerprinted build asset:
Cache-Control: public, max-age=31536000, immutable

# Authenticated API:
Cache-Control: private, no-store</div>
<h2>Spec</h2>
<p><a href="https://www.rfc-editor.org/rfc/rfc7234">RFC 7234</a></p>
""",
            "faqs": [
                (
                    "What is the difference between private and no-store?",
                    "private allows the end-user’s browser to cache but not shared proxies; no-store asks for no caching anywhere.",
                ),
                (
                    "Does immutable mean forever?",
                    "It is a hint: if the URL never changes content, validators are unnecessary. You still change URLs when content changes.",
                ),
            ],
        },
        {
            "slug": "vary-header",
            "term_name": "Vary Header",
            "title": "What is the Vary header? — WebFix Glossary",
            "description": "Tell shared caches which request headers change the response body.",
            "h1": "Vary Header",
            "short": "Tells CDNs which request headers affect the response, so they cache separate versions.",
            "tool_url": "/edge/",
            "tool_cta": "Audit caching with EdgeFix →",
            "content": """
<p class="lead">Tells CDNs which request headers affect the response, so they cache separate versions.</p>
<p><code>Vary</code> lists request header names whose values select among different representations. A classic case is <code>Vary: Accept-Encoding</code> so gzip and brotli bodies are not mixed. CORS-aware APIs often need <code>Vary: Origin</code> when the server echoes different <code>Access-Control-Allow-Origin</code> values.</p>
<h2>Why developers care</h2>
<p>Without <code>Vary: Origin</code>, a CDN might cache the first user’s permissive CORS response and hand it to a different origin—security bug plus mysterious client failures. Adding <code>Vary</code> increases cache cardinality; you balance correctness vs hit ratio. EdgeFix surfaces what your edge actually returns after compression and CORS.</p>
<h2>Example</h2>
<div class="code-block">Vary: Accept-Encoding, Origin</div>
<h2>Spec</h2>
<p><a href="https://www.rfc-editor.org/rfc/rfc7231#section-7.1.4">RFC 7231 — Vary</a></p>
""",
            "faqs": [
                (
                    "Is Vary: * valid?",
                    "It means uncacheable for most shared caches—use explicit header names instead unless you truly cannot describe the dimensions.",
                ),
                (
                    "Do I need Vary for Authorization?",
                    "If responses differ by auth, either vary on it or mark responses private/no-store so shared caches do not serve cross-user data.",
                ),
            ],
        },
        {
            "slug": "etag",
            "term_name": "ETag",
            "title": "What is an ETag? — WebFix Glossary",
            "description": "Validators let caches revalidate without full downloads.",
            "h1": "ETag",
            "short": "A fingerprint of a response that lets browsers check if their cached copy is still valid.",
            "tool_url": "/edge/",
            "tool_cta": "Audit caching with EdgeFix →",
            "content": """
<p class="lead">A fingerprint of a response that lets browsers check if their cached copy is still valid.</p>
<p>An <code>ETag</code> is an opaque validator the server attaches (strong or weak). On later requests the client sends <code>If-None-Match</code>; if content unchanged, the server returns <code>304 Not Modified</code> and the browser reuses the cached body. This saves bandwidth compared to unconditional 200 responses on every navigation.</p>
<h2>Why developers care</h2>
<p>API gateways and CDNs sometimes strip ETags when compressing or transforming bodies, which forces full refetch. Dynamic apps that disable caching entirely miss free wins for semi-static JSON. Configuring ETags correctly pairs with <code>Cache-Control</code> freshness so users see updates when data changes without redownloading when it does not.</p>
<h2>Example</h2>
<div class="code-block">ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"

# Client conditional request:
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"

# If unchanged:
HTTP/1.1 304 Not Modified</div>
<h2>Spec</h2>
<p><a href="https://www.rfc-editor.org/rfc/rfc7232">RFC 7232</a></p>
""",
            "faqs": [
                (
                    "Strong vs weak ETag?",
                    "Strong ETags must change when any byte changes; weak (W/) allows semantic equivalence. Byte-range and caching behavior differ—pick one consistent with your CDN.",
                ),
                (
                    "ETag vs Last-Modified?",
                    "Both are validators; ETags work for dynamic content without filesystem timestamps. Either can drive 304 logic.",
                ),
            ],
        },
        {
            "slug": "core-web-vitals",
            "term_name": "Core Web Vitals",
            "title": "What are Core Web Vitals? — WebFix Glossary",
            "description": "LCP, INP, and CLS—Google’s field metrics for UX and ranking signals.",
            "h1": "Core Web Vitals",
            "short": "Google's three user-experience metrics: LCP, INP, and CLS.",
            "tool_url": "/speedfixer/",
            "tool_cta": "Measure with SpeedFixer →",
            "content": """
<p class="lead">Google’s three user-experience metrics: LCP, INP, and CLS.</p>
<p>Core Web Vitals summarize real-user experience: loading (Largest Contentful Paint), interactivity (Interaction to Next Paint), and visual stability (Cumulative Layout Shift). They are measured from the Chrome User Experience Report field data, not just lab Lighthouse runs, though lab tools approximate them.</p>
<h2>Why developers care</h2>
<p>Google has confirmed Core Web Vitals as ranking factors alongside page experience signals. Poor scores correlate with higher bounce and lower conversion even without SEO. The upside: many fixes are server and asset configuration—compression, cache lifetimes, image dimensions—not months of React refactor.</p>
<h2>Example</h2>
<div class="code-block">Good targets (field data, mobile):
  LCP  &lt; 2.5 s
  INP  &lt; 200 ms
  CLS  &lt; 0.1</div>
<h2>Spec</h2>
<p><a href="https://web.dev/articles/vitals">web.dev — Core Web Vitals</a></p>
""",
            "faqs": [
                (
                    "Lab vs field for Core Web Vitals?",
                    "Field (CrUX) is what search uses for URL-level signals; lab Lighthouse helps debug but may differ from real users.",
                ),
                (
                    "Do other search engines use CWV?",
                    "Signals differ by engine; CWV remain the clearest documented UX bar for Google.",
                ),
            ],
        },
        {
            "slug": "largest-contentful-paint",
            "term_name": "Largest Contentful Paint (LCP)",
            "title": "What is LCP? — WebFix Glossary",
            "description": "LCP tracks when the main visible content element finishes loading across navigations.",
            "h1": "Largest Contentful Paint (LCP)",
            "short": "How long it takes for the largest visible element to load.",
            "tool_url": "/speedfixer/",
            "tool_cta": "Improve LCP with SpeedFixer →",
            "content": """
<p class="lead">How long it takes for the largest visible element to load.</p>
<p>LCP measures the render time of the largest image, video poster, or text block in the viewport during page load. It stops when that element is painted and stable enough to count. Slow LCP usually means late discovery (HTML depth), slow server TTFB, unoptimized hero media, or render-blocking CSS/JS in front of the hero.</p>
<h2>Why developers care</h2>
<p>LCP is the most actionable Core Web Vital for many marketing and app shells: you can often win hundreds of milliseconds with <code>fetchpriority=&quot;high&quot;</code> on the hero, preloading the LCP image, shrinking image bytes, or moving blocking scripts. SpeedFixer ties failing Lighthouse audits to nginx or CDN snippets so you do not guess.</p>
<h2>Example</h2>
<div class="code-block">&lt;link rel="preload" as="image" href="/hero.webp" type="image/webp"&gt;
&lt;img src="/hero.webp" alt="..." width="1200" height="630" fetchpriority="high"&gt;</div>
<h2>Spec</h2>
<p><a href="https://w3c.github.io/largest-contentful-paint/">Largest Contentful Paint</a></p>
""",
            "faqs": [
                (
                    "Does lazy-loading the LCP image hurt?",
                    "Yes—never lazy-load your LCP candidate. Exclude it from lazy attributes and prioritize its download.",
                ),
                (
                    "Can fonts be LCP?",
                    "Text can be the LCP element; font swap and subsetting affect when text paints acceptably.",
                ),
            ],
        },
        {
            "slug": "cumulative-layout-shift",
            "term_name": "Cumulative Layout Shift (CLS)",
            "title": "What is CLS? — WebFix Glossary",
            "description": "CLS scores unexpected movement as content loads—bad for taps and trust.",
            "h1": "Cumulative Layout Shift (CLS)",
            "short": "Measures how much page elements move around while loading.",
            "tool_url": "/speedfixer/",
            "tool_cta": "Reduce CLS with SpeedFixer →",
            "content": """
<p class="lead">Measures how much page elements move around while loading.</p>
<p>CLS aggregates layout shift scores for unexpected movement during the session lifetime measurement window. Ads, web fonts, images without reserved space, and late-inserted iframes shove content users were about to click. Unlike LCP, CLS is not about speed—it is about stability.</p>
<h2>Why developers care</h2>
<p>High CLS produces mis-clicks, form errors, and accessibility failures. It is a Core Web Vital, so it affects search visibility where field data is poor. Fixes are often free: explicit width/height (or aspect-ratio) on media, skeleton placeholders for async regions, and reserving space for embeds before they load.</p>
<h2>Example</h2>
<div class="code-block">&lt;!-- Reserve space so the browser can paint layout before bytes arrive --&gt;
&lt;img src="/photo.jpg" alt="" width="800" height="600"&gt;
&lt;iframe src="https://..." width="560" height="315" title="..."&gt;&lt;/iframe&gt;</div>
<h2>Spec</h2>
<p><a href="https://w3c.github.io/layout-instability/">Layout Instability API</a></p>
""",
            "faqs": [
                (
                    "Do animations count as CLS?",
                    "Expected movement (user-initiated) is excluded; unexpected layout shifts from loading content count.",
                ),
                (
                    "Can infinite scroll hurt CLS?",
                    "Yes, if new items push content without stable min-heights; reserve space or virtualize carefully.",
                ),
            ],
        },
        {
            "slug": "interaction-to-next-paint",
            "term_name": "Interaction to Next Paint (INP)",
            "title": "What is INP? — WebFix Glossary",
            "description": "INP replaced FID as the responsiveness Core Web Vital in 2024.",
            "h1": "Interaction to Next Paint (INP)",
            "short": "Measures how long the browser takes to visually respond to user interactions.",
            "tool_url": "/speedfixer/",
            "tool_cta": "Improve INP with SpeedFixer →",
            "content": """
<p class="lead">Measures how long the browser takes to visually respond to user interactions.</p>
<p>INP captures the worst latency (or high percentile) from tap, click, or key until the next paint the user sees—after event handlers and scheduling settle. Long tasks on the main thread, hydration storms, and third-party tag soup inflate INP even when First Input Delay looked fine.</p>
<h2>Why developers care</h2>
<p>INP replaced FID in 2024 as a Core Web Vital because FID only measured first input and missed sluggish apps after load. High INP means the UI feels frozen. Mitigations include smaller JS bundles, yielding after chunks of work, moving analytics to web workers (e.g. Partytown), and deferring non-critical scripts.</p>
<h2>Example</h2>
<div class="code-block"># Patterns that help INP:
# - split long click handlers with scheduler.yield() / setTimeout(0)
# - defer third-party: &lt;script defer&gt; or type="module"
# - Partytown for analytics in a worker</div>
<h2>Spec</h2>
<p><a href="https://web.dev/articles/inp">web.dev — INP</a></p>
""",
            "faqs": [
                (
                    "Does SSR help INP?",
                    "It can reduce hydration cost if you send meaningful HTML, but heavy client hydration still hurts—profile the main thread.",
                ),
                (
                    "What INP should I target?",
                    "Aim for under 200 ms at the 75th percentile field measurement; SpeedFixer + PSI highlight blocking scripts.",
                ),
            ],
        },
        {
            "slug": "time-to-first-byte",
            "term_name": "Time to First Byte (TTFB)",
            "title": "What is TTFB? — WebFix Glossary",
            "description": "Server and network time before the first response byte—caps how fast LCP can be.",
            "h1": "Time to First Byte (TTFB)",
            "short": "How long it takes for the browser to receive the first byte from the server.",
            "tool_url": "/speedfixer/",
            "tool_cta": "Diagnose with SpeedFixer →",
            "content": """
<p class="lead">How long it takes for the browser to receive the first byte from the server.</p>
<p>TTFB covers DNS, TLS, connection setup, queueing at the CDN, and origin processing until the response head starts streaming. It is not a Core Web Vital by itself, but it sets the lower bound for document-linked metrics: you cannot hit a good LCP if HTML arrives a second late.</p>
<h2>Why developers care</h2>
<p>High TTFB usually means cold starts, missing edge cache on HTML, slow database queries on the critical path, or geographic distance from origin. Fixing it is “back end and edge,” not CSS tweaks. Rule of thumb: sustained document TTFB above ~600 ms on mobile deserves profiling—CDN caching, regional deploys, or DB indexing—not more client JS.</p>
<h2>Example</h2>
<div class="code-block"># Rough interpretation (lab or field, HTML document):
# TTFB &lt; 200 ms — strong
# TTFB 200–600 ms — common; look for cache misses / DB
# TTFB &gt; 600 ms — investigate origin + CDN before micro-optimizing images</div>
<h2>Spec</h2>
<p><a href="https://web.dev/articles/ttfb">web.dev — TTFB</a></p>
""",
            "faqs": [
                (
                    "Does gzip affect TTFB?",
                    "Compression can add a small CPU delay but usually wins overall; measure with and without on your stack.",
                ),
                (
                    "Is TTFB the same as server think time?",
                    "Think time is part of TTFB; network RTT and TLS also contribute headers-before-body timing.",
                ),
            ],
        },
        {
            "slug": "coop-coep",
            "term_name": "COOP and COEP",
            "title": "What are COOP and COEP? — WebFix Glossary",
            "description": "Cross-origin isolation headers gate powerful APIs and mitigate some side-channel risk.",
            "h1": "COOP and COEP (Cross-Origin Isolation)",
            "short": "Two headers that enable cross-origin isolation, required for SharedArrayBuffer and high-resolution timers.",
            "tool_url": "/headers/",
            "tool_cta": "Audit headers with HeadersFixer →",
            "content": """
<p class="lead">Two headers that enable cross-origin isolation, required for <code>SharedArrayBuffer</code> and high-resolution timers.</p>
<p><code>Cross-Origin-Opener-Policy</code> (COOP) defines whether your document shares a browsing context group with cross-origin windows—<code>same-origin</code> isolates you from foreign <code>window</code> references. <code>Cross-Origin-Embedder-Policy</code> (COEP) requires cross-origin resources to explicitly opt in (<code>Cross-Origin-Resource-Policy</code> or CORS) before they load in an isolated page. Together they put the page in a mode where the platform exposes sharper timing and shared memory—power users only.</p>
<h2>Why developers care</h2>
<p>Without isolation, <code>SharedArrayBuffer</code> stays disabled in many browsers, and WebAssembly pthreads or certain media pipelines stall. Isolation also moves the security posture closer to Spectre mitigations at the cost of breaking naïve third-party embeds that lack CORP headers. You enable these only when you need the APIs or explicit isolation guarantees.</p>
<h2>Example</h2>
<div class="code-block">Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp</div>
<h2>Spec</h2>
<p><a href="https://html.spec.whatwg.org/multipage/origin.html#cross-origin-opener-policy">HTML — COOP</a> · <a href="https://html.spec.whatwg.org/multipage/origin.html#coep">HTML — COEP</a></p>
""",
            "faqs": [
                (
                    "Will COEP break my analytics iframe?",
                    "Probably, unless the vendor sends CORP or you proxy assets same-origin. Audit every subresource.",
                ),
                (
                    "Credentialless alternative?",
                    "COEP: credentialless (where supported) relaxes some embed rules—check current browser tables before relying on it.",
                ),
            ],
        },
    ]

    for t in TERMS:
        paths.append(
            write_glossary_page(
                t["slug"],
                title=t["title"],
                description=t["description"],
                h1=t["h1"],
                content=t["content"].strip(),
                tool_url=t["tool_url"],
                tool_cta=t["tool_cta"],
                term_name=t["term_name"],
                term_desc_short=t["short"],
                faqs=t["faqs"],
                related=glossary_term_related(t["slug"]),
            )
        )

    # Index page with grid
    grid_items = []
    for t in TERMS:
        grid_items.append(
            f'<a href="/glossary/{t["slug"]}/"><div class="term-title">{t["term_name"]}</div>'
            f'<div class="term-d">{t["short"]}</div></a>'
        )
    grid_html = '<div class="glossary-grid">' + "".join(grid_items) + "</div>"
    index_content = (
        "<p>Plain-language definitions for the headers, browser policies, auth flows, cache directives, "
        "and performance metrics you touch in production—each with examples and a link to the WebFix tool that automates fixes.</p>"
        + grid_html
    )
    graph = [
        {
            "@type": "DefinedTermSet",
            "name": "WebFix Security Glossary",
            "description": "Developer-focused definitions for web security and performance terms.",
            "url": "https://webfix.dev/glossary/",
        },
        breadcrumb_ld([("WebFix", "/"), ("Glossary", "")]),
        faq_ld(
            [
                (
                    "What is the WebFix glossary?",
                    "A set of concise definitions for CSP, CORS, HSTS, OAuth, caching, and Core Web Vitals, each linked to interactive WebFix tools.",
                ),
                (
                    "How do I suggest a new term?",
                    "Open an issue on the WebFix GitHub repository with the term and primary sources (RFC, WHATWG, web.dev).",
                ),
            ]
        ),
    ]
    schema_str = ld_json({"@context": "https://schema.org", "@graph": graph})
    html = (
        TEMPLATE.replace("{schema}", "__SCHEMA__")
        .format(
            title="Glossary — WebFix",
            description="Security and performance glossary: CSP, CORS, HSTS, PKCE, Cache-Control, Core Web Vitals, and more.",
            canonical="/glossary/",
            nav_section="Glossary",
            breadcrumb=bc_html([("WebFix", "/"), ("Glossary", None)]),
            h1="WebFix glossary",
            content=index_content,
            tool_url="/headers/",
            tool_cta_text="Audit headers with HeadersFixer →",
            main_class="wide",
            related=related_block([("Fix guides", "/fix/"), ("Errors", "/error/")]),
        )
        .replace("__SCHEMA__", schema_str)
    )
    idx = ROOT / "glossary" / "index.html"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(html, encoding="utf-8")
    paths.append(idx)

    print(f"Generated {len(paths)} glossary pages")


if __name__ == "__main__":
    main()
