#!/usr/bin/env python3
"""
HttpFixer — Generators, Case Studies, Changelogs, Tool Schema
Handles four pending tasks:
  1. Schema injection (FAQPage + WebApplication + BreadcrumbList) on 6 tool pages
  2. Type 5 — 5 Generator pages (CSP, CORS, Security Headers, Permissions-Policy, robots.txt)
  3. Type 6 — 3 Case study pages (SharePoint, CloudFront, Azure)
  4. Type 7 — 3 Changelog pages (CSP browser compat, Headers 2026, OAuth 2.1)

Usage:
  cd ~/Projects/stackfix
  cp ~/Downloads/27_generators_casestudies_schema.py .
  python3 27_generators_casestudies_schema.py
  git add -A && git commit -m "feat: generator pages, case studies, changelogs, tool schema" && git push origin main && npx vercel --prod --force
"""

import os, json, re
from datetime import date

BASE_URL = "https://httpfixer.dev"
TODAY = date.today().isoformat()

# ─── SHARED HELPERS ───────────────────────────────────────────────────────────

def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  ✓ {path}")


PURPLE_TAG = "rgba(108,99,255,0.2);color:var(--purple)"
GREEN_TAG  = "rgba(34,197,94,0.2);color:var(--green)"
ORANGE_TAG = "rgba(249,115,22,0.2);color:var(--orange)"
RED_TAG    = "rgba(239,68,68,0.2);color:var(--red)"

SHARED_CSS = """
    :root{--bg:#0B0D14;--surface:#12151F;--border:#252836;--purple:#6C63FF;--green:#22C55E;--orange:#F97316;--red:#EF4444;--text:#E2E4F0;}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:var(--bg);color:var(--text);font-family:"JetBrains Mono",monospace;font-size:14px;line-height:1.7;min-height:100vh}
    nav{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;border-bottom:1px solid var(--border);background:var(--surface)}
    nav .brand{font-weight:600;color:var(--text);text-decoration:none}
    nav .brand span{color:var(--purple)}
    nav .right{display:flex;gap:1rem;align-items:center}
    nav a{color:var(--text);text-decoration:none;opacity:0.6;font-size:13px}
    nav a:hover{color:var(--purple);opacity:1}
    main{max-width:800px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
    .breadcrumb{font-size:12px;opacity:0.5;margin-bottom:1.5rem}
    .breadcrumb a{color:var(--purple);text-decoration:none}
    .tag{display:inline-block;padding:0.2rem 0.6rem;border-radius:4px;font-size:11px;font-weight:600;margin-bottom:1rem}
    h1{font-size:1.6rem;font-weight:600;line-height:1.3;margin-bottom:1rem}
    h2{font-size:1.05rem;font-weight:600;margin:2rem 0 0.75rem}
    h3{font-size:0.95rem;font-weight:600;margin:1.5rem 0 0.5rem;opacity:0.85}
    p{margin-bottom:1rem;opacity:0.9;line-height:1.75}
    .lead{font-size:15px;opacity:0.95;margin-bottom:1.5rem;line-height:1.85}
    pre{background:#080a0f;border:1px solid var(--border);border-radius:6px;padding:1rem;font-size:12px;margin:1rem 0;overflow-x:auto;white-space:pre;line-height:1.6}
    p code,li code{background:rgba(108,99,255,0.15);color:var(--purple);padding:0.1rem 0.3rem;border-radius:3px;font-size:12px}
    .tool-cta{display:inline-block;margin:2rem 0 1rem;padding:0.75rem 1.5rem;background:var(--purple);color:white;text-decoration:none;border-radius:6px;font-weight:500;font-size:14px}
    .tool-cta:hover{filter:brightness(1.1)}
    .related{font-size:12px;opacity:0.6;margin:1.5rem 0;padding-top:1rem;border-top:1px solid var(--border)}
    .related a{color:var(--purple);text-decoration:none;margin-right:0.75rem}
    table{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:13px}
    th,td{padding:0.6rem 0.75rem;border:1px solid var(--border);text-align:left}
    th{background:var(--surface);color:var(--purple);font-weight:600}
    tr:nth-child(even) td{background:rgba(255,255,255,0.02)}
    ul,ol{margin:0.75rem 0 1rem 1.5rem;opacity:0.9}
    li{margin-bottom:0.4rem;line-height:1.7}
    .note-box{background:#0d1117;border:1px solid var(--border);border-left:3px solid var(--purple);border-radius:6px;padding:1rem;margin:1.5rem 0;font-size:13px;opacity:0.85}
    .warn-box{background:#1a0f00;border:1px solid var(--orange);border-radius:6px;padding:1rem;margin:1.5rem 0;font-size:12px;color:#fba44a;line-height:1.6}
    .warn-label{font-size:10px;text-transform:uppercase;opacity:0.6;margin-bottom:0.5rem;letter-spacing:0.05em}
    footer{border-top:1px solid var(--border);padding:1.5rem 2rem;font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem}
    footer a{color:var(--text);text-decoration:none;opacity:0.6}
    .disclaimer{width:100%;text-align:center;font-size:11px;opacity:0.4;margin-top:0.75rem;line-height:1.6}
    @media(max-width:600px){nav .right{display:none}footer{flex-direction:column;text-align:center}}
"""

SHARED_NAV = """<nav>
  <a href="/" class="brand">HttpFixer <span>/</span> {label}</a>
  <div class="right">
    <a href="/">Headers</a><a href="/cors/">CORS</a><a href="/oauth/">OAuth</a>
    <a href="/csp/">CSP</a><a href="/edge/">Edge</a><a href="/speedfixer/">Speed</a>
  </div>
</nav>"""

SHARED_FOOTER = """<footer>
  <span>HttpFixer by MetricLogic · <a href="https://configclarity.dev">configclarity.dev</a> · <a href="https://domainpreflight.dev">domainpreflight.dev</a> · <a href="https://packagefix.dev">packagefix.dev</a></span>
  <span><a href="https://github.com/metriclogic26/httpfixer">MIT · GitHub →</a> · <a href="https://github.com/metriclogic26/httpfixer/issues/new">Report issue →</a></span>
  <p class="disclaimer">Configurations are based on open standards (OWASP, RFC, MDN). Always test in a staging environment before deploying to production. HttpFixer provides these tools for informational purposes only. © 2026 MetricLogic.</p>
</footer>"""


def page(title, desc, canonical, schema, label, breadcrumb, tag, tag_color, h1, content, cta_url, cta_text, related):
    schema_str = json.dumps(schema, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · HttpFixer</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="MetricLogic">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">{schema_str}</script>
  <style>{SHARED_CSS}
    .gen-box{{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.5rem;margin:1.5rem 0}}
    .gen-box label{{display:block;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;opacity:0.5;margin-bottom:0.5rem}}
    .gen-box select,.gen-box input[type=text]{{width:100%;background:#080a0f;border:1px solid var(--border);border-radius:4px;padding:0.5rem 0.75rem;color:var(--text);font-family:"JetBrains Mono",monospace;font-size:13px;margin-bottom:0.75rem}}
    .gen-box select:focus,.gen-box input[type=text]:focus{{outline:none;border-color:var(--purple)}}
    .gen-output{{background:#080a0f;border:1px solid var(--border);border-radius:6px;padding:1rem;font-size:12px;margin-top:1rem;min-height:80px;white-space:pre-wrap;word-break:break-all;line-height:1.6;color:#a8b4c8}}
    .gen-btn{{padding:0.5rem 1rem;background:var(--purple);color:white;border:none;border-radius:4px;font-family:"JetBrains Mono",monospace;font-size:13px;cursor:pointer;margin-right:0.5rem}}
    .gen-btn:hover{{filter:brightness(1.1)}}
    .copy-btn{{padding:0.5rem 1rem;background:transparent;color:var(--purple);border:1px solid var(--purple);border-radius:4px;font-family:"JetBrains Mono",monospace;font-size:13px;cursor:pointer}}
    .copy-btn:hover{{background:rgba(108,99,255,0.1)}}
    .checkbox-group{{display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.75rem}}
    .checkbox-group label{{display:flex;align-items:center;gap:0.4rem;font-size:12px;cursor:pointer;opacity:0.8;background:#0d1117;padding:0.3rem 0.6rem;border-radius:4px;border:1px solid var(--border)}}
    .checkbox-group input{{width:auto;margin:0}}
  </style>
</head>
<body>
{SHARED_NAV.format(label=label)}
<main>
  <div class="breadcrumb">{breadcrumb}</div>
  <span class="tag" style="background:{tag_color}">{tag}</span>
  <h1>{h1}</h1>
  {content}
  <a href="{cta_url}" class="tool-cta">{cta_text}</a>
  <div class="related">Related: {related}</div>
</main>
{SHARED_FOOTER}
</body>
</html>"""


def make_schema(title, desc, url, app_name=None, faqs=None, steps=None):
    graph = [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "HttpFixer", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": title, "item": url}
        ]},
        {"@type": "TechArticle", "headline": title, "description": desc, "url": url,
         "datePublished": TODAY, "dateModified": TODAY,
         "author": {"@type": "Organization", "name": "MetricLogic"},
         "publisher": {"@type": "Organization", "name": "MetricLogic", "url": "https://metriclogic.dev"}}
    ]
    if app_name:
        graph.append({
            "@type": "WebApplication",
            "name": app_name,
            "url": url,
            "description": desc,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Any",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
        })
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
        })
    if steps:
        graph.append({
            "@type": "HowTo",
            "name": title,
            "step": [{"@type": "HowToStep", "position": i+1, "name": s[0], "text": s[1]}
                     for i, s in enumerate(steps)]
        })
    return {"@context": "https://schema.org", "@graph": graph}


# ─── TASK 1 — SCHEMA ON 6 TOOL PAGES ─────────────────────────────────────────

def inject_tool_schema():
    print("\n📍 Task 1 — Injecting schema into 6 tool pages")

    tools = {
        "index.html": {
            "name": "HeadersFixer",
            "url": BASE_URL + "/",
            "desc": "Scan any URL and get the exact Nginx, Apache, Vercel, or Cloudflare config to fix missing security headers.",
            "faqs": [
                ("What does HeadersFixer check?",
                 "HeadersFixer checks for 9 HTTP security headers: Strict-Transport-Security (HSTS), Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, Cross-Origin-Opener-Policy, Cross-Origin-Embedder-Policy, and Server header exposure."),
                ("Is HeadersFixer free?",
                 "Yes. HeadersFixer is completely free with no signup, no account, and no tracking. It runs entirely in your browser."),
                ("What is a security header?",
                 "Security headers are HTTP response headers that tell browsers how to behave when handling your page — blocking clickjacking, XSS, MIME sniffing, and forced downgrade attacks."),
                ("Which security header is most important?",
                 "Strict-Transport-Security (HSTS) if your site is HTTPS-only. Content-Security-Policy for XSS protection. Both are essential for any production site."),
                ("How do I add security headers in Nginx?",
                 "Use add_header directives in your server block. For example: add_header X-Frame-Options 'SAMEORIGIN' always; — HeadersFixer generates the exact config for your specific missing headers.")
            ]
        },
        "cors/index.html": {
            "name": "CORSFixer",
            "url": BASE_URL + "/cors/",
            "desc": "Send a real OPTIONS preflight to any API endpoint and get the exact CORS configuration to fix it — for Express, Nginx, FastAPI, Next.js, and more.",
            "faqs": [
                ("What causes a CORS error?",
                 "CORS errors occur when a browser blocks a cross-origin request because the server's response is missing the Access-Control-Allow-Origin header, or the preflight OPTIONS request fails."),
                ("Why does my API work in Postman but fail in the browser?",
                 "Postman does not enforce CORS — it is a developer tool. The browser sends an OPTIONS preflight before POST, PUT, or DELETE requests with custom headers. If your server doesn't handle OPTIONS, the browser blocks the request."),
                ("What is Access-Control-Allow-Origin: *?",
                 "A wildcard that allows any origin to read your API responses. It breaks when credentials (cookies or Authorization headers) are involved — you must use an explicit origin instead."),
                ("How do I fix CORS in Express.js?",
                 "Install the cors npm package: npm install cors. Then add app.use(cors({ origin: 'https://yourdomain.com' })) before your route definitions."),
                ("What is a CORS preflight request?",
                 "An OPTIONS request the browser sends before cross-origin POST, PUT, DELETE, or requests with custom headers. The server must respond with 204 and CORS headers or the actual request never runs.")
            ]
        },
        "oauth/index.html": {
            "name": "OAuthFixer",
            "url": BASE_URL + "/oauth/",
            "desc": "Diagnose OAuth 2.0 errors instantly — invalid_grant, redirect_uri_mismatch, PKCE failures, and more. Provider-specific fixes for Auth0, Okta, Cognito, Google, and Microsoft.",
            "faqs": [
                ("What does invalid_grant mean in OAuth?",
                 "The authorization code expired (codes typically last under 10 minutes), was reused, has a PKCE verifier mismatch, or the refresh token was revoked. Each cause has a different fix."),
                ("Why do I get redirect_uri_mismatch?",
                 "The redirect_uri in your request must exactly match the registered URI in your provider dashboard — including protocol, port, trailing slash, and every character."),
                ("What is PKCE in OAuth?",
                 "Proof Key for Code Exchange — an OAuth extension that prevents authorization code interception. Required for SPAs and mobile apps. You generate a random verifier, hash it to create a challenge, and send both through the flow."),
                ("How do I fix invalid_grant on a refresh token?",
                 "Catch the error, clear stored tokens, and redirect the user to the login page. The refresh token is no longer valid — a fresh authorization code flow is required."),
                ("What is the difference between OAuth 2.0 and OpenID Connect?",
                 "OAuth 2.0 handles authorization — giving your app access to a user's data. OpenID Connect adds authentication — proving who the user is — by adding a standardised ID token to the OAuth flow.")
            ]
        },
        "csp/index.html": {
            "name": "CSPFixer",
            "url": BASE_URL + "/csp/",
            "desc": "Scan your live page, find all blocked resources, and generate a working Content Security Policy — no unsafe-inline required.",
            "faqs": [
                ("What is a Content Security Policy?",
                 "A browser-enforced allowlist that controls which scripts, styles, images, and other resources are allowed to load on your page. The main defence against XSS — it blocks injected scripts even if they get into your HTML."),
                ("Why does unsafe-inline defeat CSP?",
                 "Adding unsafe-inline to script-src allows any inline script to run — including scripts an attacker injects via XSS. It fixes the console error but removes all XSS protection. Use nonces instead."),
                ("What is a CSP nonce?",
                 "A random base64 value generated per request. You add it to the nonce attribute of trusted inline scripts and include it in your CSP header. Injected scripts cannot know the nonce, so they are blocked."),
                ("How do I fix a CSP violation?",
                 "The browser console shows the exact URL that was blocked and which directive caused it. Add the domain to the correct directive — script-src for scripts, style-src for styles, connect-src for API calls."),
                ("How do I add CSP for Google Analytics?",
                 "Add https://www.googletagmanager.com to script-src, https://www.google-analytics.com to both script-src and connect-src, and https://www.googletagmanager.com to img-src.")
            ]
        },
        "edge/index.html": {
            "name": "EdgeFix",
            "url": BASE_URL + "/edge/",
            "desc": "Audit Cache-Control, Vary, Age, X-Cache, ETag, and Stale-While-Revalidate headers. Find why your CDN isn't caching and generate the fix for your stack.",
            "faqs": [
                ("Why is my CDN not caching responses?",
                 "Missing or incorrect Cache-Control headers. CDNs default to not caching when Cache-Control is absent. Use Cache-Control: public, s-maxage=3600 for CDN caching. Never cache authenticated responses — use private, no-store."),
                ("What is Cache-Control: immutable?",
                 "Tells browsers not to revalidate the resource during max-age, even on back/forward navigation. Only use for truly immutable resources — files with content hashes in the filename."),
                ("What is stale-while-revalidate?",
                 "A Cache-Control extension that tells the CDN to serve a stale cached response immediately while fetching a fresh one in the background. Eliminates the user-visible wait during cache refresh."),
                ("What is the Vary header?",
                 "Tells CDNs which request headers affect the response. Vary: Origin means the CDN stores separate cached responses per origin — required when using explicit CORS origins to prevent cross-user response leakage."),
                ("Should I cache API responses?",
                 "Only unauthenticated, public responses. Use public, s-maxage=60, stale-while-revalidate=86400 for public data. Use private, no-store for any response tied to a user session or auth token.")
            ]
        },
        "speedfixer/index.html": {
            "name": "SpeedFixer",
            "url": BASE_URL + "/speedfixer/",
            "desc": "Fetch your live PageSpeed Insights score and generate the exact Nginx, Cloudflare, Vercel, or Apache config to fix each failing audit.",
            "faqs": [
                ("What is SpeedFixer?",
                 "SpeedFixer calls the Google PageSpeed Insights API on your URL, reads the failing audits, detects your server stack from response headers, and generates the exact copy-paste config to fix each issue."),
                ("What stacks does SpeedFixer support?",
                 "Nginx, Apache, Cloudflare (Cache Rules / Transform Rules), Vercel (vercel.json), Netlify (_headers file), and WordPress (WP Rocket / LiteSpeed Cache plugin paths)."),
                ("What is the difference between Category A and Category B fixes?",
                 "Category A fixes are server config — copy-paste ready blocks for your stack. Category B fixes require code changes (unused CSS removal, image format conversion, JavaScript bundle splitting) — SpeedFixer labels these clearly so you know what still needs developer work."),
                ("Why does SpeedFixer beat ChatGPT for this task?",
                 "SpeedFixer calls the live PageSpeed Insights API on your URL and reads your actual server headers. ChatGPT cannot make real HTTP requests — it can only give generic advice, not fixes specific to your failing audits."),
                ("What is TTFB and how do I fix it?",
                 "Time To First Byte — how long the browser waits before receiving the first byte of your response. Fix it by moving to edge/CDN delivery, adding server-side caching, or switching from serverless cold-start functions to edge runtime.")
            ]
        }
    }

    patched = 0
    for filepath, config in tools.items():
        if not os.path.exists(filepath):
            print(f"  ⚠️  {filepath} — not found, skipping")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if '"FAQPage"' in content or '"WebApplication"' in content:
            print(f"  ⏭  {filepath} — schema already present")
            continue

        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebApplication",
                    "name": config["name"],
                    "url": config["url"],
                    "description": config["desc"],
                    "applicationCategory": "DeveloperApplication",
                    "operatingSystem": "Any",
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}
                        }
                        for q, a in config["faqs"]
                    ]
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "HttpFixer", "item": BASE_URL},
                        {"@type": "ListItem", "position": 2, "name": config["name"], "item": config["url"]}
                    ]
                }
            ]
        }

        schema_tag = f'\n<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'

        # Inject after the last existing ld+json block, or before </head>
        if 'application/ld+json' in content:
            # Find the end of the last ld+json script tag
            last_pos = content.rfind('</script>')
            # Find the next </head> or just append before </head>
            insert_pos = content.find('</head>', last_pos)
            if insert_pos != -1:
                content = content[:insert_pos] + schema_tag + "\n" + content[insert_pos:]
        else:
            content = content.replace('</head>', schema_tag + '\n</head>', 1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  ✓ {filepath} — WebApplication + FAQPage + BreadcrumbList injected")
        patched += 1

    print(f"  → {patched} tool pages patched")


# ─── TASK 2 — GENERATOR PAGES ─────────────────────────────────────────────────

def generate_generator_pages():
    print("\n📍 Task 2 — Generator Pages")

    # 1. CSP Generator
    write("generators/csp/index.html", page(
        title="CSP Header Generator — Build a Content Security Policy",
        desc="Generate a Content Security Policy header from scratch. Select your sources, copy the header value, and deploy to Nginx, Apache, Vercel, or Cloudflare.",
        canonical=f"{BASE_URL}/generators/csp/",
        schema=make_schema(
            "CSP Header Generator",
            "Free browser-based Content Security Policy generator. Select sources and get the exact header for your stack.",
            f"{BASE_URL}/generators/csp/",
            app_name="CSP Generator",
            faqs=[
                ("How do I generate a Content Security Policy?", "Select which external domains your site loads scripts, styles, images, and fonts from. The generator builds the directives automatically. Start with default-src 'self' and add sources as needed."),
                ("What is the safest CSP I can add?", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; — this blocks all external resources and inline scripts. Add sources incrementally as you identify what your page needs."),
                ("Should I use report-only mode first?", "Yes. Use Content-Security-Policy-Report-Only with your new policy first. Violations appear in the browser console without blocking anything. Enforce once violations stop.")
            ]
        ),
        label="Generators",
        breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/generators/">Generators</a> → CSP Generator',
        tag="Generator", tag_color=GREEN_TAG,
        h1="CSP Header Generator",
        content="""
<p class="lead">Build a Content Security Policy header by selecting your sources. The generator outputs a header value ready to paste into Nginx, Apache, Vercel, or Cloudflare — and includes the config block for your stack.</p>

<div class="gen-box">
  <label>Script sources (script-src)</label>
  <div class="checkbox-group" id="script-sources">
    <label><input type="checkbox" value="'self'" checked> self</label>
    <label><input type="checkbox" value="'nonce-REPLACE'"> nonce</label>
    <label><input type="checkbox" value="'strict-dynamic'"> strict-dynamic</label>
    <label><input type="checkbox" value="https://www.googletagmanager.com"> Google Tag Manager</label>
    <label><input type="checkbox" value="https://www.google-analytics.com"> Google Analytics</label>
    <label><input type="checkbox" value="https://js.stripe.com"> Stripe.js</label>
    <label><input type="checkbox" value="https://js.intercomcdn.com"> Intercom</label>
    <label><input type="checkbox" value="https://static.hotjar.com"> Hotjar</label>
    <label><input type="checkbox" value="https://challenges.cloudflare.com"> CF Turnstile</label>
    <label><input type="checkbox" value="'unsafe-inline'"> unsafe-inline ⚠</label>
    <label><input type="checkbox" value="'unsafe-eval'"> unsafe-eval ⚠</label>
  </div>

  <label>Style sources (style-src)</label>
  <div class="checkbox-group" id="style-sources">
    <label><input type="checkbox" value="'self'" checked> self</label>
    <label><input type="checkbox" value="'unsafe-inline'" checked> unsafe-inline</label>
    <label><input type="checkbox" value="https://fonts.googleapis.com"> Google Fonts</label>
  </div>

  <label>Image sources (img-src)</label>
  <div class="checkbox-group" id="img-sources">
    <label><input type="checkbox" value="'self'" checked> self</label>
    <label><input type="checkbox" value="data:" checked> data:</label>
    <label><input type="checkbox" value="https:"> https: (all)</label>
    <label><input type="checkbox" value="https://www.google-analytics.com"> GA images</label>
  </div>

  <label>Connect sources (connect-src — fetch, XHR, WebSocket)</label>
  <div class="checkbox-group" id="connect-sources">
    <label><input type="checkbox" value="'self'" checked> self</label>
    <label><input type="checkbox" value="https://www.google-analytics.com"> Google Analytics</label>
    <label><input type="checkbox" value="https://api.stripe.com"> Stripe API</label>
    <label><input type="checkbox" value="https://*.hotjar.com"> Hotjar</label>
    <label><input type="checkbox" value="https://api.intercom.io"> Intercom</label>
  </div>

  <label>Font sources (font-src)</label>
  <div class="checkbox-group" id="font-sources">
    <label><input type="checkbox" value="'self'" checked> self</label>
    <label><input type="checkbox" value="https://fonts.gstatic.com"> Google Fonts</label>
    <label><input type="checkbox" value="data:"> data:</label>
  </div>

  <label>Frame ancestors (who can embed your page)</label>
  <div class="checkbox-group" id="frame-ancestors">
    <label><input type="checkbox" value="'none'" checked> none (no iframes allowed)</label>
    <label><input type="checkbox" value="'self'"> self only</label>
  </div>

  <label>Additional options</label>
  <div class="checkbox-group" id="extras">
    <label><input type="checkbox" value="object-src-none" checked> object-src 'none' (block Flash/plugins)</label>
    <label><input type="checkbox" value="base-uri-self" checked> base-uri 'self'</label>
    <label><input type="checkbox" value="upgrade"> upgrade-insecure-requests</label>
    <label><input type="checkbox" value="report-only"> Start in report-only mode</label>
  </div>

  <label>Custom additional domain (optional)</label>
  <input type="text" id="custom-domain" placeholder="https://api.yourdomain.com">

  <button class="gen-btn" onclick="buildCSP()">Generate CSP</button>
  <button class="copy-btn" onclick="copyOutput('csp-output')">Copy</button>

  <label style="margin-top:1rem">Generated Header Value</label>
  <div class="gen-output" id="csp-output">Click "Generate CSP" to build your policy.</div>

  <label style="margin-top:1rem">Nginx Config</label>
  <div class="gen-output" id="nginx-output"></div>

  <label style="margin-top:1rem">Vercel (vercel.json)</label>
  <div class="gen-output" id="vercel-output"></div>
</div>

<h2>What each directive controls</h2>
<table>
  <thead><tr><th>Directive</th><th>Controls</th><th>Tip</th></tr></thead>
  <tbody>
    <tr><td>default-src</td><td>Fallback for all types not listed</td><td>Start with 'self'</td></tr>
    <tr><td>script-src</td><td>JavaScript files and inline scripts</td><td>Avoid unsafe-inline — use nonces</td></tr>
    <tr><td>style-src</td><td>CSS files and inline styles</td><td>unsafe-inline usually required for CSS-in-JS</td></tr>
    <tr><td>img-src</td><td>Images</td><td>Add data: for base64 images</td></tr>
    <tr><td>connect-src</td><td>fetch, XHR, WebSocket, EventSource</td><td>Required for any API calls</td></tr>
    <tr><td>font-src</td><td>Font files</td><td>Google Fonts needs fonts.gstatic.com</td></tr>
    <tr><td>frame-ancestors</td><td>Who can embed your page in an iframe</td><td>'none' blocks clickjacking</td></tr>
    <tr><td>object-src</td><td>Plugins (Flash, Java)</td><td>Always set to 'none'</td></tr>
  </tbody>
</table>

<h2>Deploy in report-only mode first</h2>
<p>Use <code>Content-Security-Policy-Report-Only</code> instead of <code>Content-Security-Policy</code> when first deploying. Violations appear in the browser console without blocking anything — letting you catch missing sources before enforcing.</p>

<p>If you have a live page and want to generate a CSP from what it actually loads, use CSPFixer instead — it scans your URL and builds the policy automatically.</p>

<script>
function getChecked(groupId) {
  return [...document.querySelectorAll('#' + groupId + ' input:checked')].map(i => i.value);
}

function buildCSP() {
  const scripts = getChecked('script-sources');
  const styles = getChecked('style-sources');
  const imgs = getChecked('img-sources');
  const connects = getChecked('connect-sources');
  const fonts = getChecked('font-sources');
  const frameAnc = getChecked('frame-ancestors');
  const extras = getChecked('extras');
  const custom = document.getElementById('custom-domain').value.trim();

  const reportOnly = extras.includes('report-only');
  const headerName = reportOnly ? 'Content-Security-Policy-Report-Only' : 'Content-Security-Policy';

  let parts = ["default-src 'self'"];
  if (scripts.length) parts.push("script-src " + scripts.join(' '));
  if (styles.length) parts.push("style-src " + styles.join(' '));
  if (imgs.length) parts.push("img-src " + imgs.join(' '));
  if (connects.length) parts.push("connect-src " + connects.join(' '));
  if (fonts.length) parts.push("font-src " + fonts.join(' '));
  if (frameAnc.length) parts.push("frame-ancestors " + frameAnc.join(' '));
  if (extras.includes('object-src-none')) parts.push("object-src 'none'");
  if (extras.includes('base-uri-self')) parts.push("base-uri 'self'");
  if (extras.includes('upgrade')) parts.push("upgrade-insecure-requests");
  if (custom) parts.push("connect-src 'self' " + custom);

  const policy = parts.join('; ') + ';';
  const headerVal = headerName + ': ' + policy;

  document.getElementById('csp-output').textContent = headerVal;
  document.getElementById('nginx-output').textContent = 'add_header ' + headerName + ' "' + policy + '" always;';
  document.getElementById('vercel-output').textContent = JSON.stringify({
    headers: [{ source: "/(.*)", headers: [{ key: headerName, value: policy }] }]
  }, null, 2);
}

function copyOutput(id) {
  const text = document.getElementById(id).textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
  });
}
</script>
""",
        cta_url="/csp/",
        cta_text="Scan a live URL and auto-generate CSP → CSPFixer",
        related='<a href="/blog/csp/fix-csp-refused-to-load/">Fix refused to load</a> <a href="/blog/csp/csp-unsafe-inline-nonce-hash/">Nonce vs hash vs unsafe-inline</a> <a href="/blog/reference/csp-third-party-services/">Third-party CSP reference</a>'
    ))

    # 2. CORS Header Generator
    write("generators/cors/index.html", page(
        title="CORS Header Generator — Generate Access-Control Headers",
        desc="Build the exact CORS response headers for your API. Select your origin, methods, and headers — get copy-paste config for Nginx, Express, FastAPI, or Vercel.",
        canonical=f"{BASE_URL}/generators/cors/",
        schema=make_schema(
            "CORS Header Generator",
            "Free browser-based CORS header generator for Nginx, Express, FastAPI, and Vercel.",
            f"{BASE_URL}/generators/cors/",
            app_name="CORS Header Generator",
            faqs=[
                ("What CORS headers does my API need?", "At minimum: Access-Control-Allow-Origin. For authenticated requests: also Access-Control-Allow-Credentials: true with an explicit origin (not *). For non-simple requests: also Access-Control-Allow-Methods and Access-Control-Allow-Headers in the OPTIONS preflight response."),
                ("Can I use * for Access-Control-Allow-Origin?", "Only for fully public APIs with no authentication. If your API uses cookies, Authorization headers, or any credentials, you must specify an explicit origin."),
                ("Do I need to handle OPTIONS separately?", "Yes for POST, PUT, DELETE, and requests with custom headers. The browser sends OPTIONS first. Your server must return 204 with CORS headers for the actual request to run.")
            ]
        ),
        label="Generators",
        breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/generators/">Generators</a> → CORS Generator',
        tag="Generator", tag_color=PURPLE_TAG,
        h1="CORS Header Generator",
        content="""
<p class="lead">Select your configuration and get the exact CORS headers for your API — with copy-paste config for every major stack.</p>

<div class="gen-box">
  <label>Allowed Origin</label>
  <input type="text" id="cors-origin" placeholder="https://app.example.com  (or * for public API)">

  <label>Allowed Methods</label>
  <div class="checkbox-group" id="cors-methods">
    <label><input type="checkbox" value="GET" checked> GET</label>
    <label><input type="checkbox" value="POST" checked> POST</label>
    <label><input type="checkbox" value="PUT"> PUT</label>
    <label><input type="checkbox" value="DELETE"> DELETE</label>
    <label><input type="checkbox" value="PATCH"> PATCH</label>
    <label><input type="checkbox" value="OPTIONS" checked> OPTIONS</label>
  </div>

  <label>Allowed Headers</label>
  <div class="checkbox-group" id="cors-headers">
    <label><input type="checkbox" value="Content-Type" checked> Content-Type</label>
    <label><input type="checkbox" value="Authorization" checked> Authorization</label>
    <label><input type="checkbox" value="X-Requested-With"> X-Requested-With</label>
    <label><input type="checkbox" value="X-API-Key"> X-API-Key</label>
    <label><input type="checkbox" value="Accept"> Accept</label>
  </div>

  <label>Options</label>
  <div class="checkbox-group" id="cors-options">
    <label><input type="checkbox" value="credentials"> Allow credentials (cookies / auth)</label>
    <label><input type="checkbox" value="vary"> Add Vary: Origin header</label>
    <label><input type="checkbox" value="maxage"> Cache preflight (86400s)</label>
  </div>

  <button class="gen-btn" onclick="buildCORS()">Generate Headers</button>
  <button class="copy-btn" onclick="copyOutput('cors-nginx')">Copy Nginx</button>

  <label style="margin-top:1rem">Nginx Config</label>
  <div class="gen-output" id="cors-nginx">Click "Generate Headers" to build your config.</div>

  <label style="margin-top:1rem">Express (Node.js)</label>
  <div class="gen-output" id="cors-express"></div>

  <label style="margin-top:1rem">FastAPI (Python)</label>
  <div class="gen-output" id="cors-fastapi"></div>
</div>

<script>
function buildCORS() {
  const origin = document.getElementById('cors-origin').value.trim() || 'https://app.example.com';
  const methods = getChecked('cors-methods').join(', ');
  const headers = getChecked('cors-headers').join(', ');
  const opts = getChecked('cors-options');
  const creds = opts.includes('credentials');
  const vary = opts.includes('vary');
  const maxAge = opts.includes('maxage');

  const nginx = [
    'if ($request_method = OPTIONS) {',
    '    add_header Access-Control-Allow-Origin "' + origin + '";',
    '    add_header Access-Control-Allow-Methods "' + methods + '";',
    '    add_header Access-Control-Allow-Headers "' + headers + '";',
    creds ? '    add_header Access-Control-Allow-Credentials "true";' : '',
    maxAge ? '    add_header Access-Control-Max-Age 86400;' : '',
    '    add_header Content-Length 0;',
    '    return 204;',
    '}',
    '',
    'add_header Access-Control-Allow-Origin "' + origin + '" always;',
    creds ? 'add_header Access-Control-Allow-Credentials "true" always;' : '',
    vary ? 'add_header Vary Origin always;' : '',
  ].filter(Boolean).join('\\n');

  const express = [
    "app.use(cors({",
    "  origin: '" + origin + "',",
    "  methods: ['" + methods.split(', ').join("', '") + "'],",
    "  allowedHeaders: ['" + headers.split(', ').join("', '") + "'],",
    creds ? "  credentials: true," : "",
    maxAge ? "  maxAge: 86400," : "",
    "}));",
    "",
    "app.options('*', cors()); // Handle preflight",
  ].filter(Boolean).join('\\n');

  const fastapi = [
    "app.add_middleware(",
    "    CORSMiddleware,",
    "    allow_origins=['" + origin + "'],",
    "    allow_methods=['" + methods.split(', ').join("', '") + "'],",
    "    allow_headers=['" + headers.split(', ').join("', '") + "'],",
    creds ? "    allow_credentials=True," : "",
    ")",
  ].filter(Boolean).join('\\n');

  document.getElementById('cors-nginx').textContent = nginx;
  document.getElementById('cors-express').textContent = express;
  document.getElementById('cors-fastapi').textContent = fastapi;
}

function getChecked(groupId) {
  return [...document.querySelectorAll('#' + groupId + ' input:checked')].map(i => i.value);
}

function copyOutput(id) {
  const text = document.getElementById(id).textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
  });
}
</script>
""",
        cta_url="/cors/",
        cta_text="Test your CORS config with a live preflight → CORSFixer",
        related='<a href="/blog/cors/fix-cors-express/">Express CORS fix</a> <a href="/blog/cors/fix-cors-nginx/">Nginx CORS fix</a> <a href="/blog/reference/cors-headers-cheat-sheet/">CORS headers cheat sheet</a>'
    ))

    # 3. Security Headers Generator
    write("generators/security-headers/index.html", page(
        title="Security Headers Generator — All 9 Headers in One Click",
        desc="Generate the complete set of HTTP security headers for your site. Select your options and get copy-paste config for Nginx, Apache, Vercel, Cloudflare, or Express.",
        canonical=f"{BASE_URL}/generators/security-headers/",
        schema=make_schema(
            "Security Headers Generator",
            "Generate all 9 HTTP security headers for Nginx, Apache, Vercel, or Cloudflare.",
            f"{BASE_URL}/generators/security-headers/",
            app_name="Security Headers Generator",
            faqs=[
                ("Which security headers should every site have?", "At minimum: Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, Referrer-Policy. Add Content-Security-Policy for XSS protection and Permissions-Policy for feature control."),
                ("Is it safe to add all security headers at once?", "X-Content-Type-Options, Referrer-Policy, and Permissions-Policy are safe to add immediately. HSTS requires HTTPS to be fully working. CSP requires testing — use report-only mode first."),
                ("What is Permissions-Policy?", "Controls which browser features (camera, microphone, geolocation) your page and embedded iframes can access. Setting them all to () disables them entirely.")
            ]
        ),
        label="Generators",
        breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/generators/">Generators</a> → Security Headers Generator',
        tag="Generator", tag_color=RED_TAG,
        h1="Security Headers Generator",
        content="""
<p class="lead">Configure your security headers and get copy-paste config for your stack. Safe defaults are pre-selected — adjust for your specific setup.</p>

<div class="gen-box">
  <label>HSTS (Strict-Transport-Security)</label>
  <div class="checkbox-group" id="hsts-opts">
    <label><input type="checkbox" value="hsts" checked> Enable HSTS</label>
    <label><input type="checkbox" value="subdomains" checked> includeSubDomains</label>
    <label><input type="checkbox" value="preload"> preload (submit to hstspreload.org first)</label>
  </div>

  <label>X-Frame-Options</label>
  <div class="checkbox-group" id="xfo-opts">
    <label><input type="checkbox" value="SAMEORIGIN" checked> SAMEORIGIN (allow same-domain iframes)</label>
    <label><input type="checkbox" value="DENY"> DENY (no iframes anywhere)</label>
  </div>

  <label>Referrer-Policy</label>
  <div class="checkbox-group" id="ref-opts">
    <label><input type="checkbox" value="strict-origin-when-cross-origin" checked> strict-origin-when-cross-origin (recommended)</label>
    <label><input type="checkbox" value="no-referrer"> no-referrer (maximum privacy)</label>
    <label><input type="checkbox" value="same-origin"> same-origin only</label>
  </div>

  <label>Permissions-Policy (disable unused features)</label>
  <div class="checkbox-group" id="perm-opts">
    <label><input type="checkbox" value="camera" checked> camera=()</label>
    <label><input type="checkbox" value="microphone" checked> microphone=()</label>
    <label><input type="checkbox" value="geolocation" checked> geolocation=()</label>
    <label><input type="checkbox" value="interest-cohort" checked> interest-cohort=()</label>
    <label><input type="checkbox" value="payment"> payment=()</label>
    <label><input type="checkbox" value="usb"> usb=()</label>
  </div>

  <label>Additional Headers</label>
  <div class="checkbox-group" id="extra-headers">
    <label><input type="checkbox" value="xcto" checked> X-Content-Type-Options: nosniff</label>
    <label><input type="checkbox" value="coop" checked> Cross-Origin-Opener-Policy: same-origin</label>
    <label><input type="checkbox" value="server"> Remove Server header (Nginx only)</label>
  </div>

  <button class="gen-btn" onclick="buildSecHeaders()">Generate Headers</button>
  <button class="copy-btn" onclick="copyOutput('sec-nginx')">Copy Nginx</button>

  <label style="margin-top:1rem">Nginx Config</label>
  <div class="gen-output" id="sec-nginx">Click "Generate Headers" to build your config.</div>

  <label style="margin-top:1rem">Vercel (vercel.json)</label>
  <div class="gen-output" id="sec-vercel"></div>
</div>

<script>
function buildSecHeaders() {
  const hsts = getChecked('hsts-opts');
  const xfo = getChecked('xfo-opts');
  const ref = getChecked('ref-opts');
  const perms = getChecked('perm-opts');
  const extras = getChecked('extra-headers');

  const headers = [];
  const vercelHeaders = [];

  if (hsts.includes('hsts')) {
    let hval = 'max-age=31536000';
    if (hsts.includes('subdomains')) hval += '; includeSubDomains';
    if (hsts.includes('preload')) hval += '; preload';
    headers.push('add_header Strict-Transport-Security "' + hval + '" always;');
    vercelHeaders.push({ key: 'Strict-Transport-Security', value: hval });
  }

  const xfoVal = xfo.includes('DENY') ? 'DENY' : xfo.includes('SAMEORIGIN') ? 'SAMEORIGIN' : null;
  if (xfoVal) {
    headers.push('add_header X-Frame-Options "' + xfoVal + '" always;');
    vercelHeaders.push({ key: 'X-Frame-Options', value: xfoVal });
  }

  if (extras.includes('xcto')) {
    headers.push("add_header X-Content-Type-Options \"nosniff\" always;");
    vercelHeaders.push({ key: 'X-Content-Type-Options', value: 'nosniff' });
  }

  const refVal = ref[0] || 'strict-origin-when-cross-origin';
  headers.push('add_header Referrer-Policy "' + refVal + '" always;');
  vercelHeaders.push({ key: 'Referrer-Policy', value: refVal });

  if (perms.length) {
    const permVal = perms.map(p => p + '=()').join(', ');
    headers.push('add_header Permissions-Policy "' + permVal + '" always;');
    vercelHeaders.push({ key: 'Permissions-Policy', value: permVal });
  }

  if (extras.includes('coop')) {
    headers.push('add_header Cross-Origin-Opener-Policy "same-origin" always;');
    vercelHeaders.push({ key: 'Cross-Origin-Opener-Policy', value: 'same-origin' });
  }

  if (extras.includes('server')) {
    headers.push('server_tokens off;');
  }

  document.getElementById('sec-nginx').textContent = headers.join('\\n');
  document.getElementById('sec-vercel').textContent = JSON.stringify({
    headers: [{ source: "/(.*)", headers: vercelHeaders }]
  }, null, 2);
}

function getChecked(groupId) {
  return [...document.querySelectorAll('#' + groupId + ' input:checked')].map(i => i.value);
}

function copyOutput(id) {
  const text = document.getElementById(id).textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
  });
}
</script>
""",
        cta_url="/",
        cta_text="Scan your live site → HeadersFixer",
        related='<a href="/blog/headers/security-headers-checklist/">Security headers checklist</a> <a href="/blog/reference/http-security-headers-reference/">Headers reference</a> <a href="/blog/headers/fix-hsts/">Fix HSTS</a>'
    ))

    # 4. Permissions-Policy Generator
    write("generators/permissions-policy/index.html", page(
        title="Permissions-Policy Header Generator",
        desc="Generate a Permissions-Policy header to control camera, microphone, geolocation, and other browser features. Copy-paste config for Nginx, Apache, Vercel.",
        canonical=f"{BASE_URL}/generators/permissions-policy/",
        schema=make_schema(
            "Permissions-Policy Header Generator",
            "Generate the Permissions-Policy header to control browser feature access.",
            f"{BASE_URL}/generators/permissions-policy/",
            app_name="Permissions-Policy Generator",
            faqs=[
                ("What is Permissions-Policy?", "An HTTP header that controls which browser features your page and embedded iframes can access — camera, microphone, geolocation, payment, USB, and more. Restricting unused features reduces your attack surface."),
                ("What is the difference between Permissions-Policy and Feature-Policy?", "Feature-Policy was the old name, deprecated in 2020. Permissions-Policy is the current standard with a different syntax. Most modern browsers support Permissions-Policy."),
                ("Should I disable all features by default?", "Disable features your site does not use. If you never use the camera or geolocation, set them to (). This prevents third-party scripts on your page from accessing these features without your knowledge.")
            ]
        ),
        label="Generators",
        breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/generators/">Generators</a> → Permissions-Policy Generator',
        tag="Generator", tag_color=RED_TAG,
        h1="Permissions-Policy Header Generator",
        content="""
<p class="lead">Control which browser APIs your page can access. Restricting unused features prevents third-party scripts from silently accessing your users' camera, microphone, or location.</p>

<div class="gen-box">
  <p style="font-size:12px;opacity:0.6;margin-bottom:1rem">For each feature: <strong>() = blocked for all</strong> · <strong>self = your origin only</strong> · <strong>* = allow all</strong></p>

  <label>Sensor / Device Features</label>
  <table style="margin:0 0 1rem;font-size:12px">
    <thead><tr><th>Feature</th><th>() Block</th><th>self only</th><th>* Allow all</th></tr></thead>
    <tbody id="perm-table">
      <tr><td>camera</td><td><input type="radio" name="camera" value="()" checked></td><td><input type="radio" name="camera" value="self"></td><td><input type="radio" name="camera" value="*"></td></tr>
      <tr><td>microphone</td><td><input type="radio" name="microphone" value="()" checked></td><td><input type="radio" name="microphone" value="self"></td><td><input type="radio" name="microphone" value="*"></td></tr>
      <tr><td>geolocation</td><td><input type="radio" name="geolocation" value="()" checked></td><td><input type="radio" name="geolocation" value="self"></td><td><input type="radio" name="geolocation" value="*"></td></tr>
      <tr><td>accelerometer</td><td><input type="radio" name="accelerometer" value="()" checked></td><td><input type="radio" name="accelerometer" value="self"></td><td><input type="radio" name="accelerometer" value="*"></td></tr>
      <tr><td>gyroscope</td><td><input type="radio" name="gyroscope" value="()" checked></td><td><input type="radio" name="gyroscope" value="self"></td><td><input type="radio" name="gyroscope" value="*"></td></tr>
    </tbody>
  </table>

  <label>Payment / Commerce</label>
  <table style="margin:0 0 1rem;font-size:12px">
    <thead><tr><th>Feature</th><th>() Block</th><th>self only</th><th>* Allow all</th></tr></thead>
    <tbody>
      <tr><td>payment</td><td><input type="radio" name="payment" value="()"></td><td><input type="radio" name="payment" value="self" checked></td><td><input type="radio" name="payment" value="*"></td></tr>
      <tr><td>usb</td><td><input type="radio" name="usb" value="()" checked></td><td><input type="radio" name="usb" value="self"></td><td><input type="radio" name="usb" value="*"></td></tr>
    </tbody>
  </table>

  <label>Privacy</label>
  <table style="margin:0 0 1rem;font-size:12px">
    <thead><tr><th>Feature</th><th>() Block</th><th>self only</th><th>* Allow all</th></tr></thead>
    <tbody>
      <tr><td>interest-cohort</td><td><input type="radio" name="interest-cohort" value="()" checked></td><td><input type="radio" name="interest-cohort" value="self"></td><td><input type="radio" name="interest-cohort" value="*"></td></tr>
      <tr><td>fullscreen</td><td><input type="radio" name="fullscreen" value="()"></td><td><input type="radio" name="fullscreen" value="self" checked></td><td><input type="radio" name="fullscreen" value="*"></td></tr>
    </tbody>
  </table>

  <button class="gen-btn" onclick="buildPermsPolicy()">Generate Header</button>
  <button class="copy-btn" onclick="copyOutput('perms-output')">Copy</button>

  <label style="margin-top:1rem">Generated Header</label>
  <div class="gen-output" id="perms-output">Click "Generate Header" to build your policy.</div>

  <label style="margin-top:1rem">Nginx</label>
  <div class="gen-output" id="perms-nginx"></div>
</div>

<script>
const FEATURES = ['camera','microphone','geolocation','accelerometer','gyroscope','payment','usb','interest-cohort','fullscreen'];

function buildPermsPolicy() {
  const parts = FEATURES.map(f => {
    const el = document.querySelector('input[name="' + f + '"]:checked');
    return f + '=' + (el ? el.value : '()');
  });
  const val = parts.join(', ');
  document.getElementById('perms-output').textContent = 'Permissions-Policy: ' + val;
  document.getElementById('perms-nginx').textContent = 'add_header Permissions-Policy "' + val + '" always;';
}

function copyOutput(id) {
  const text = document.getElementById(id).textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
  });
}
</script>
""",
        cta_url="/",
        cta_text="Scan all your security headers → HeadersFixer",
        related='<a href="/blog/headers/security-headers-checklist/">Security headers checklist</a> <a href="/generators/security-headers/">Security headers generator</a>'
    ))

    # 5. Generators index
    write("generators/index.html", page(
        title="HttpFixer Generators — Build Security Headers Without Guessing",
        desc="Free browser-based generators for CSP, CORS, security headers, and Permissions-Policy. Select options, copy config, deploy.",
        canonical=f"{BASE_URL}/generators/",
        schema={"@context": "https://schema.org", "@type": "CollectionPage",
                "name": "HttpFixer Generators", "url": f"{BASE_URL}/generators/"},
        label="Generators",
        breadcrumb=f'<a href="/">HttpFixer</a> → Generators',
        tag="Generators", tag_color=PURPLE_TAG,
        h1="Generators",
        content="""
<p class="lead">Building a new site or adding a header for the first time? Generators build the config from scratch. If you have a live site to scan, use the fixer tools instead.</p>

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1rem;margin:1.5rem 0">
  <a href="/generators/csp/" style="text-decoration:none;display:block;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.25rem;transition:border-color 0.2s" onmouseover="this.style.borderColor='var(--green)'" onmouseout="this.style.borderColor='var(--border)'">
    <div style="color:var(--green);font-size:1.2rem;margin-bottom:0.5rem">🛡</div>
    <strong style="display:block;margin-bottom:0.4rem">CSP Generator</strong>
    <span style="font-size:12px;opacity:0.6">Build a Content Security Policy by selecting your sources. Outputs header value + Nginx/Vercel config.</span>
  </a>
  <a href="/generators/cors/" style="text-decoration:none;display:block;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.25rem;transition:border-color 0.2s" onmouseover="this.style.borderColor='var(--purple)'" onmouseout="this.style.borderColor='var(--border)'">
    <div style="color:var(--purple);font-size:1.2rem;margin-bottom:0.5rem">⚡</div>
    <strong style="display:block;margin-bottom:0.4rem">CORS Header Generator</strong>
    <span style="font-size:12px;opacity:0.6">Select origin, methods, and headers. Get Nginx, Express, and FastAPI config in one click.</span>
  </a>
  <a href="/generators/security-headers/" style="text-decoration:none;display:block;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.25rem;transition:border-color 0.2s" onmouseover="this.style.borderColor='var(--red)'" onmouseout="this.style.borderColor='var(--border)'">
    <div style="color:var(--red);font-size:1.2rem;margin-bottom:0.5rem">🔒</div>
    <strong style="display:block;margin-bottom:0.4rem">Security Headers Generator</strong>
    <span style="font-size:12px;opacity:0.6">Configure all 9 security headers at once. HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy, and more.</span>
  </a>
  <a href="/generators/permissions-policy/" style="text-decoration:none;display:block;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.25rem;transition:border-color 0.2s" onmouseover="this.style.borderColor='var(--red)'" onmouseout="this.style.borderColor='var(--border)'">
    <div style="color:var(--red);font-size:1.2rem;margin-bottom:0.5rem">🎛</div>
    <strong style="display:block;margin-bottom:0.4rem">Permissions-Policy Generator</strong>
    <span style="font-size:12px;opacity:0.6">Control camera, microphone, geolocation, payment, and more. Block features you do not use.</span>
  </a>
</div>

<h2>Generators vs Fixers — which to use</h2>
<table>
  <thead><tr><th>Situation</th><th>Use</th></tr></thead>
  <tbody>
    <tr><td>I have a live site and want to see what's missing</td><td><a href="/" style="color:var(--purple)">HeadersFixer</a> — scans your URL</td></tr>
    <tr><td>I'm building from scratch and need a starting config</td><td>Generators — this page</td></tr>
    <tr><td>I have a CORS error in the browser console</td><td><a href="/cors/" style="color:var(--purple)">CORSFixer</a> — live preflight test</td></tr>
    <tr><td>I need a CSP for a page I haven't deployed yet</td><td><a href="/generators/csp/" style="color:var(--green)">CSP Generator</a></td></tr>
    <tr><td>My CSP is blocking something on a live page</td><td><a href="/csp/" style="color:var(--green)">CSPFixer</a> — scans your URL</td></tr>
  </tbody>
</table>
""",
        cta_url="/",
        cta_text="Scan your live site instead → HeadersFixer",
        related='<a href="/">HeadersFixer</a> <a href="/cors/">CORSFixer</a> <a href="/csp/">CSPFixer</a>'
    ))


# ─── TASK 3 — CASE STUDY PAGES ────────────────────────────────────────────────

def generate_case_studies():
    print("\n📍 Task 3 — Case Study Pages")

    cases = [
        {
            "slug": "sharepoint-csp-blocked",
            "title": "How SharePoint Online Enforces CSP — And How to Work Around It",
            "desc": "Microsoft enforced CSP on SharePoint Online in March 2026. Here is why your scripts are blocked, what the policy actually allows, and how to update your SPFx components.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "cta_url": "/csp/", "cta_text": "Scan your SharePoint page CSP → CSPFixer",
            "related": '<a href="/blog/csp/fix-csp-refused-to-load/">Fix refused to load</a> <a href="/blog/csp/csp-unsafe-inline-nonce-hash/">Nonce vs unsafe-inline</a>',
            "content": """
<p class="lead">On March 1, 2026, Microsoft began enforcing Content Security Policy on SharePoint Online pages. Scripts that worked for years now produce "Refused to load" console errors. Here is exactly what changed and how to fix your SPFx components.</p>

<div class="warn-box"><div class="warn-label">Affected Since</div>March 1, 2026 (enforcement). Optional delay to June 1, 2026 available via tenant settings. After June 1, no override is possible.</div>

<h2>What Microsoft's SharePoint CSP actually blocks</h2>
<p>SharePoint Online's enforced CSP blocks the following by default:</p>
<ul>
  <li><strong>External script sources</strong> not on Microsoft's allowlist — including most CDN-loaded libraries</li>
  <li><strong>Inline scripts</strong> — <code>&lt;script&gt;...&lt;/script&gt;</code> blocks injected into page markup</li>
  <li><strong>eval() and Function() constructors</strong> — dynamic code execution</li>
  <li><strong>Custom JavaScript files</strong> loaded from non-SharePoint domains</li>
</ul>

<h2>What is still allowed</h2>
<ul>
  <li>Scripts from <code>*.sharepoint.com</code> and <code>*.microsoft.com</code></li>
  <li>Scripts uploaded to SharePoint document libraries (loaded from the same origin)</li>
  <li>SPFx components deployed through the App Catalog</li>
  <li>Scripts explicitly whitelisted via the tenant CSP settings</li>
</ul>

<h2>How to check what is blocked on your tenant</h2>
<pre># Check tenant CSP setting
Get-SPOTenant | Select-Object DisableCustomAppAuthentication

# View current CSP headers on your SharePoint site
curl -I https://yourtenant.sharepoint.com/sites/yoursite | grep -i content-security</pre>

<h2>Fix 1 — Move scripts to SharePoint CDN or App Catalog</h2>
<p>The safest fix: upload your JavaScript files to a SharePoint document library or deploy through the App Catalog. Both are on the allowed origin.</p>
<pre>// SPFx webpart — reference local files instead of CDN
// Instead of:
// &lt;script src="https://cdn.example.com/library.js"&gt;&lt;/script&gt;

// Deploy library.js to:
// https://yourtenant.sharepoint.com/sites/yoursite/SiteAssets/library.js

// Or use SPFx externals in config/config.json to bundle it:
{
  "externals": {
    "your-library": {
      "path": "https://yourtenant.sharepoint.com/sites/yoursite/SiteAssets/library.js",
      "globalName": "YourLibrary"
    }
  }
}</pre>

<h2>Fix 2 — Add your domain to the tenant CSP allowlist (admin)</h2>
<pre># PowerShell — add external script source to tenant CSP
Connect-SPOService -Url https://yourtenant-admin.sharepoint.com

Add-SPOTenantCdnOrigin -CdnType Public -OriginUrl */SiteAssets
Set-SPOTenant -ContentSecurityPolicyConfiguration @{
  DefaultSrc = @("'self'", "*.microsoft.com", "*.sharepoint.com", "https://cdn.yourdomain.com")
  ScriptSrc = @("'self'", "*.microsoft.com", "*.sharepoint.com", "https://cdn.yourdomain.com")
}</pre>

<h2>Fix 3 — Rewrite inline scripts as external files</h2>
<p>If you have inline <code>&lt;script&gt;</code> blocks in Script Editor webparts or page content, move them to <code>.js</code> files in a document library:</p>
<pre>// Before — inline script (blocked)
// &lt;script&gt;
//   var x = document.getElementById('myEl');
//   x.style.color = 'red';
// &lt;/script&gt;

// After — external file in SiteAssets (allowed)
// &lt;script src="/sites/yoursite/SiteAssets/myScript.js"&gt;&lt;/script&gt;</pre>

<h2>How to delay enforcement to June 1, 2026</h2>
<pre># Tenant admin — delay enforcement
Set-SPOTenant -ContentSecurityPolicyEnforcementDelay $true
# Note: This option expires June 1, 2026. Plan your migration now.</pre>

<p>Use CSPFixer to scan your SharePoint page and see exactly which resources are being blocked. It outputs the corrected header values and fix instructions.</p>"""
        },
        {
            "slug": "cloudfront-strips-security-headers",
            "title": "Why AWS CloudFront Strips Security Headers — And How to Add Them Back",
            "desc": "CloudFront does not forward all headers from your origin by default. Security headers set on your EC2 or ECS backend may be stripped before reaching the browser. Here is the fix.",
            "tag": "Headers", "tag_color": RED_TAG,
            "cta_url": "/", "cta_text": "Verify your CloudFront headers → HeadersFixer",
            "related": '<a href="/blog/headers/security-headers-checklist/">Security headers checklist</a> <a href="/blog/performance/fix-cache-control-cdn/">Cache-Control on CDN</a>',
            "content": """
<p class="lead">CloudFront caches responses from your origin and may not forward all response headers to the browser. Security headers you set in Nginx or Express on your EC2 instance often never reach the user. There are two ways to fix this.</p>

<h2>Why CloudFront strips headers</h2>
<p>By default, CloudFront only forwards a subset of response headers from your origin. Headers it does not recognise or whitelist in the cache policy are dropped before the response reaches the browser.</p>

<div class="warn-box"><div class="warn-label">Common symptom</div>Headers appear in curl requests directly to your EC2 IP but are missing when you curl through the CloudFront distribution URL. The headers exist on your origin — CloudFront is dropping them.</div>

<h2>Fix 1 — Response Headers Policy (recommended)</h2>
<p>CloudFront has a built-in Response Headers Policy feature. Create a managed or custom policy and attach it to your distribution behaviours:</p>
<pre># Using AWS CLI
aws cloudfront create-response-headers-policy --response-headers-policy-config '{
  "Name": "SecurityHeadersPolicy",
  "SecurityHeadersConfig": {
    "StrictTransportSecurity": {
      "Override": true,
      "IncludeSubdomains": true,
      "Preload": true,
      "AccessControlMaxAgeSec": 31536000
    },
    "ContentTypeOptions": { "Override": true },
    "FrameOptions": { "FrameOption": "SAMEORIGIN", "Override": true },
    "XSSProtection": { "Protection": false, "Override": true },
    "ReferrerPolicy": { "ReferrerPolicy": "strict-origin-when-cross-origin", "Override": true }
  },
  "CustomHeadersConfig": {
    "Quantity": 1,
    "Items": [{
      "Header": "Permissions-Policy",
      "Value": "camera=(), microphone=(), geolocation=()",
      "Override": true
    }]
  }
}'

# Then attach to your distribution behaviour
aws cloudfront update-distribution --id YOURDISTRIID ...</pre>

<p>In the AWS Console: CloudFront → Your Distribution → Behaviours → Edit → Response headers policy → Create policy or select "SecurityHeadersPolicy" (AWS managed).</p>

<h2>Fix 2 — CloudFront Function</h2>
<p>Add headers on the viewer response using a CloudFront Function (cheaper than Lambda@Edge for simple header manipulation):</p>
<pre>// CloudFront Function — viewer-response event
function handler(event) {
  var response = event.response;
  var headers = response.headers;

  headers['strict-transport-security'] = { value: 'max-age=31536000; includeSubDomains; preload' };
  headers['x-frame-options'] = { value: 'SAMEORIGIN' };
  headers['x-content-type-options'] = { value: 'nosniff' };
  headers['referrer-policy'] = { value: 'strict-origin-when-cross-origin' };
  headers['permissions-policy'] = { value: 'camera=(), microphone=(), geolocation=()' };

  return response;
}
</pre>

<p>Deploy: CloudFront → Functions → Create function → paste code → Publish → attach to distribution behaviour on Viewer Response event.</p>

<h2>Verify headers reach the browser</h2>
<pre># Check headers through CloudFront (not your origin directly)
curl -I https://d1234abcd.cloudfront.net/
# or
curl -I https://yoursite.com/

# Confirm headers like X-Frame-Options appear in the response</pre>

<p>Use HeadersFixer — it fetches your live CloudFront URL and shows exactly which security headers are missing or misconfigured after CDN processing.</p>"""
        },
        {
            "slug": "azure-api-management-cors",
            "title": "CORS on Azure API Management — Complete Configuration",
            "desc": "Azure APIM handles CORS at the gateway level using policies. Your backend CORS config is irrelevant — here is exactly where to add it and what the policy XML looks like.",
            "tag": "CORS", "tag_color": PURPLE_TAG,
            "cta_url": "/cors/", "cta_text": "Test your APIM CORS config → CORSFixer",
            "related": '<a href="/blog/cors/fix-cors-nginx/">Nginx CORS</a> <a href="/blog/platform/cors-aws-lambda/">AWS Lambda CORS</a>',
            "content": """
<p class="lead">Azure API Management sits in front of your backend — and handles CORS before requests reach it. Your backend's CORS configuration is completely bypassed. You configure CORS in APIM using inbound policy XML.</p>

<h2>Where CORS goes in APIM</h2>
<p>APIM uses XML policy documents at four scopes (global, product, API, operation). Add CORS at the API scope to apply it to all operations in your API, or at the operation scope for per-endpoint control.</p>

<h2>The CORS policy XML</h2>
<pre>&lt;!-- Azure Portal → API Management → Your API → Inbound processing → Add policy --&gt;
&lt;cors allow-credentials="true"&gt;
  &lt;allowed-origins&gt;
    &lt;origin&gt;https://app.example.com&lt;/origin&gt;
    &lt;origin&gt;https://staging.example.com&lt;/origin&gt;
  &lt;/allowed-origins&gt;
  &lt;allowed-methods preflight-result-max-age="300"&gt;
    &lt;method&gt;GET&lt;/method&gt;
    &lt;method&gt;POST&lt;/method&gt;
    &lt;method&gt;PUT&lt;/method&gt;
    &lt;method&gt;DELETE&lt;/method&gt;
    &lt;method&gt;OPTIONS&lt;/method&gt;
  &lt;/allowed-methods&gt;
  &lt;allowed-headers&gt;
    &lt;header&gt;Authorization&lt;/header&gt;
    &lt;header&gt;Content-Type&lt;/header&gt;
    &lt;header&gt;Ocp-Apim-Subscription-Key&lt;/header&gt;
  &lt;/allowed-headers&gt;
  &lt;expose-headers&gt;
    &lt;header&gt;X-Request-ID&lt;/header&gt;
  &lt;/expose-headers&gt;
&lt;/cors&gt;</pre>

<h2>Apply in Azure Portal</h2>
<ol>
  <li>Azure Portal → API Management → Your service → APIs → Your API</li>
  <li>Select "All operations" for API-level, or a specific operation</li>
  <li>Inbound processing → click the policy icon → add the cors element inside &lt;inbound&gt;&lt;base /&gt;</li>
  <li>Save and test</li>
</ol>

<h2>Wildcard origin in APIM</h2>
<pre>&lt;!-- Public API — no credentials --&gt;
&lt;cors allow-credentials="false"&gt;
  &lt;allowed-origins&gt;
    &lt;origin&gt;*&lt;/origin&gt;
  &lt;/allowed-origins&gt;
  &lt;allowed-methods&gt;
    &lt;method&gt;GET&lt;/method&gt;
    &lt;method&gt;OPTIONS&lt;/method&gt;
  &lt;/allowed-methods&gt;
  &lt;allowed-headers&gt;
    &lt;header&gt;*&lt;/header&gt;
  &lt;/allowed-headers&gt;
&lt;/cors&gt;</pre>

<h2>Bicep / ARM deployment</h2>
<pre>resource apiPolicy 'Microsoft.ApiManagement/service/apis/policies@2022-08-01' = {
  name: 'policy'
  parent: myApi
  properties: {
    format: 'rawxml'
    value: '''
      &lt;policies&gt;
        &lt;inbound&gt;
          &lt;base /&gt;
          &lt;cors allow-credentials="true"&gt;
            &lt;allowed-origins&gt;
              &lt;origin&gt;https://app.example.com&lt;/origin&gt;
            &lt;/allowed-origins&gt;
            &lt;allowed-methods&gt;&lt;method&gt;GET&lt;/method&gt;&lt;method&gt;POST&lt;/method&gt;&lt;/allowed-methods&gt;
            &lt;allowed-headers&gt;&lt;header&gt;Authorization&lt;/header&gt;&lt;header&gt;Content-Type&lt;/header&gt;&lt;/allowed-headers&gt;
          &lt;/cors&gt;
        &lt;/inbound&gt;
        &lt;backend&gt;&lt;base /&gt;&lt;/backend&gt;
        &lt;outbound&gt;&lt;base /&gt;&lt;/outbound&gt;
      &lt;/policies&gt;
    '''
  }
}</pre>

<p>After applying the policy, use CORSFixer to send a real OPTIONS preflight to your APIM endpoint and confirm the response headers are correct.</p>"""
        }
    ]

    for case in cases:
        write(f"case-studies/{case['slug']}/index.html", page(
            title=case["title"], desc=case["desc"],
            canonical=f"{BASE_URL}/case-studies/{case['slug']}/",
            schema=make_schema(case["title"], case["desc"], f"{BASE_URL}/case-studies/{case['slug']}/",
                faqs=[(f"What is the main fix for this issue?", "See the step-by-step fix in the article above."),
                      ("Does this affect all users?", "See the affected platforms and versions described in the article.")]),
            label="Case Studies",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/case-studies/">Case Studies</a> → {case["title"]}',
            tag=case["tag"], tag_color=case["tag_color"],
            h1=case["title"], content=case["content"],
            cta_url=case["cta_url"], cta_text=case["cta_text"],
            related=case["related"]
        ))

    # Case studies index
    write("case-studies/index.html", page(
        title="Case Studies — Real-World HTTP Security Fixes",
        desc="Real-world case studies: SharePoint CSP enforcement, AWS CloudFront header stripping, Azure APIM CORS configuration.",
        canonical=f"{BASE_URL}/case-studies/",
        schema={"@context": "https://schema.org", "@type": "CollectionPage",
                "name": "HttpFixer Case Studies", "url": f"{BASE_URL}/case-studies/"},
        label="Case Studies",
        breadcrumb=f'<a href="/">HttpFixer</a> → Case Studies',
        tag="Case Studies", tag_color=ORANGE_TAG,
        h1="Case Studies",
        content="""
<p class="lead">Platform-specific investigations showing why security headers and CORS configurations fail on specific infrastructure — and exactly how to fix them.</p>
<ul style="list-style:none;padding:0;margin:1.5rem 0">
  <li style="margin-bottom:1rem;padding:1rem;background:var(--surface);border:1px solid var(--border);border-radius:6px">
    <a href="/case-studies/sharepoint-csp-blocked/" style="color:var(--text);text-decoration:none;font-weight:600">How SharePoint Online Enforces CSP — And How to Work Around It</a>
    <p style="font-size:12px;opacity:0.6;margin:0.3rem 0 0">Microsoft enforced CSP on SharePoint Online in March 2026. Why your SPFx components are blocked and how to fix them.</p>
  </li>
  <li style="margin-bottom:1rem;padding:1rem;background:var(--surface);border:1px solid var(--border);border-radius:6px">
    <a href="/case-studies/cloudfront-strips-security-headers/" style="color:var(--text);text-decoration:none;font-weight:600">Why AWS CloudFront Strips Security Headers — And How to Add Them Back</a>
    <p style="font-size:12px;opacity:0.6;margin:0.3rem 0 0">Security headers on your EC2/ECS backend are dropped before reaching the browser. Response Headers Policy and CloudFront Functions are the fix.</p>
  </li>
  <li style="padding:1rem;background:var(--surface);border:1px solid var(--border);border-radius:6px">
    <a href="/case-studies/azure-api-management-cors/" style="color:var(--text);text-decoration:none;font-weight:600">CORS on Azure API Management — Complete Configuration</a>
    <p style="font-size:12px;opacity:0.6;margin:0.3rem 0 0">APIM handles CORS via XML policy documents — your backend config is bypassed entirely. Here is the exact policy XML.</p>
  </li>
</ul>""",
        cta_url="/", cta_text="Scan your live site → HeadersFixer",
        related='<a href="/blog/">Blog</a> <a href="/generators/">Generators</a>'
    ))


# ─── TASK 4 — CHANGELOG PAGES ─────────────────────────────────────────────────

def generate_changelogs():
    print("\n📍 Task 4 — Changelog Pages")

    changelogs = [
        {
            "slug": "csp-browser-support-2026",
            "title": "CSP Browser Support 2026 — Directive Compatibility Table",
            "desc": "Which CSP directives are supported in Chrome, Firefox, Safari, and Edge in 2026. Includes Trusted Types, require-trusted-types-for, and newer directives.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "updated": TODAY,
            "content": """
<p class="lead">CSP Level 3 is now well-supported across all major browsers. A handful of newer directives — Trusted Types, script-src-attr, navigate-to — have partial support. Here is the full compatibility picture as of early 2026.</p>

<div class="note-box">Last updated: {today}. Browser versions: Chrome 131+, Firefox 133+, Safari 18+, Edge 131+.</div>

<h2>Core directives — full support everywhere</h2>
<table>
  <thead><tr><th>Directive</th><th>Chrome</th><th>Firefox</th><th>Safari</th><th>Edge</th></tr></thead>
  <tbody>
    <tr><td>default-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>script-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>style-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>img-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>connect-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>font-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>frame-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>frame-ancestors</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>object-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>base-uri</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>form-action</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>worker-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>manifest-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>media-src</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>upgrade-insecure-requests</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>block-all-mixed-content</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
  </tbody>
</table>

<h2>Nonces, hashes, strict-dynamic</h2>
<table>
  <thead><tr><th>Feature</th><th>Chrome</th><th>Firefox</th><th>Safari</th><th>Edge</th></tr></thead>
  <tbody>
    <tr><td>'nonce-value'</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>'sha256-hash'</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td>'strict-dynamic'</td><td>✅</td><td>✅</td><td>✅ 15.4+</td><td>✅</td></tr>
    <tr><td>'unsafe-hashes'</td><td>✅</td><td>✅</td><td>✅ 15.4+</td><td>✅</td></tr>
    <tr><td>'wasm-unsafe-eval'</td><td>✅</td><td>✅</td><td>✅ 16+</td><td>✅</td></tr>
  </tbody>
</table>

<h2>Newer / partial support directives</h2>
<table>
  <thead><tr><th>Directive</th><th>Chrome</th><th>Firefox</th><th>Safari</th><th>Edge</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>script-src-elem</td><td>✅ 90+</td><td>✅ 105+</td><td>✅ 16+</td><td>✅ 90+</td><td>Granular control over script elements vs inline handlers</td></tr>
    <tr><td>script-src-attr</td><td>✅ 90+</td><td>✅ 105+</td><td>✅ 16+</td><td>✅ 90+</td><td>Controls inline event handlers separately from scripts</td></tr>
    <tr><td>style-src-elem</td><td>✅ 90+</td><td>✅ 105+</td><td>✅ 16+</td><td>✅ 90+</td><td></td></tr>
    <tr><td>require-trusted-types-for 'script'</td><td>✅ 83+</td><td>⚠️ Partial</td><td>❌</td><td>✅ 83+</td><td>Trusted Types — Safari no support</td></tr>
    <tr><td>trusted-types</td><td>✅ 83+</td><td>⚠️ Partial</td><td>❌</td><td>✅ 83+</td><td>Define Trusted Type policies</td></tr>
    <tr><td>navigate-to</td><td>❌</td><td>❌</td><td>❌</td><td>❌</td><td>Spec'd but no browser has shipped it</td></tr>
    <tr><td>report-to</td><td>✅ 70+</td><td>⚠️ Partial</td><td>⚠️ Partial</td><td>✅ 70+</td><td>Use report-uri as fallback</td></tr>
  </tbody>
</table>

<h2>What changed in 2025–2026</h2>
<ul>
  <li><strong>Safari 18</strong> — Added full support for strict-dynamic and unsafe-hashes, closing the main Safari CSP gap</li>
  <li><strong>Firefox 105+</strong> — script-src-elem and script-src-attr now fully supported</li>
  <li><strong>Chrome 131+</strong> — Improved Trusted Types enforcement, better DevTools violation reporting</li>
  <li><strong>SharePoint Online</strong> — Began enforcing CSP for all tenant pages March 2026</li>
  <li><strong>navigate-to</strong> — Still unshipped in all browsers despite being in the spec since CSP3</li>
</ul>

<h2>Practical recommendation</h2>
<p>For maximum browser compatibility in 2026, a nonce-based policy with strict-dynamic works across all major browsers including Safari 15.4+. Trusted Types remains Chrome/Edge only — use it for those environments only and do not rely on it for Safari users.</p>
""".format(today=TODAY)
        },
        {
            "slug": "http-security-headers-2026",
            "title": "HTTP Security Headers 2026 — What Changed, What's New",
            "desc": "Browser changes to HSTS preloading, CSP enforcement, COEP, Permissions-Policy, and the headers that were deprecated in 2025–2026.",
            "tag": "Headers", "tag_color": RED_TAG,
            "updated": TODAY,
            "content": f"""
<p class="lead">Security header support and browser enforcement changes every year. Here is what changed in 2025–2026 — what tightened, what was deprecated, and what newly matters.</p>

<div class="note-box">Last updated: {TODAY}. Covers Chrome 120–131, Firefox 120–133, Safari 17–18, Edge 120–131.</div>

<h2>What changed in 2025–2026</h2>

<h3>Permissions-Policy — interest-cohort removed</h3>
<p>The <code>interest-cohort</code> feature (Google's FLoC) was deprecated. Chrome 115+ ignores it. You can keep <code>interest-cohort=()</code> in your header — it does no harm — but it no longer controls anything. The relevant current features are <code>browsing-topics</code> and <code>attribution-reporting</code>.</p>

<h3>X-XSS-Protection deprecated</h3>
<p>Chrome 78+ removed the XSS Auditor. Firefox never implemented it. The <code>X-XSS-Protection</code> header is now deprecated and ignored by all major browsers. Remove it from your config — it provides no protection and in some edge cases could create vulnerabilities on older browsers. Replace it with a strict CSP.</p>

<h3>COEP credentialless — broader support</h3>
<p><code>Cross-Origin-Embedder-Policy: credentialless</code> is now supported in Chrome 96+, Edge 96+, and Firefox 119+. This is easier to deploy than <code>require-corp</code> because it does not require third-party resources to set CORP headers — they are loaded without credentials instead.</p>

<h3>CSP frame-ancestors — now preferred over X-Frame-Options</h3>
<p>All major browsers now support CSP frame-ancestors and use it when both headers are present, ignoring X-Frame-Options. Keep both for IE and legacy browser coverage, but CSP frame-ancestors is the canonical solution.</p>

<h3>HSTS preload list — stricter minimum max-age</h3>
<p>The HSTS preload list now requires a minimum max-age of 1 year (31536000 seconds). Sites submitted with lower values are rejected. Sites already on the list with lower values are being contacted to update.</p>

<h3>Permissions-Policy — new features added</h3>
<p>Several new features were added to the Permissions-Policy spec in 2025:</p>
<ul>
  <li><code>speaker-selection</code> — controls access to audio output device enumeration</li>
  <li><code>window-management</code> — controls multi-screen window placement API</li>
  <li><code>local-fonts</code> — controls access to locally installed fonts</li>
  <li><code>idle-detection</code> — controls the Idle Detection API</li>
</ul>

<h2>Current recommended headers (2026)</h2>
<pre>Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{{nonce}}'; ...
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: credentialless

# Remove these — deprecated:
# X-XSS-Protection: 1; mode=block  ← remove</pre>

<h2>What to watch in 2026</h2>
<ul>
  <li><strong>Fetch Metadata headers</strong> (<code>Sec-Fetch-*</code>) — browsers send these automatically, servers can use them for CSRF protection</li>
  <li><strong>Origin-Agent-Cluster</strong> — keyed origin isolation, improving on the COOP/COEP model</li>
  <li><strong>CSP Trusted Types</strong> — Firefox implementation progressing but still incomplete</li>
  <li><strong>Private Network Access</strong> — Chrome enforcing stricter controls on requests to private network addresses from public pages</li>
</ul>"""
        },
        {
            "slug": "oauth-21-changes",
            "title": "OAuth 2.1 Changes — What Developers Need to Update",
            "desc": "OAuth 2.1 consolidates OAuth 2.0 best practices into a single spec. Implicit Flow and Resource Owner Password Credentials are removed. PKCE is required for all clients.",
            "tag": "OAuth", "tag_color": ORANGE_TAG,
            "updated": TODAY,
            "content": f"""
<p class="lead">OAuth 2.1 is the consolidation of the original OAuth 2.0 spec with the security updates from six years of BCP (Best Current Practice) documents. It does not introduce new features — it formalises what was already best practice and removes what is no longer safe.</p>

<div class="note-box">Last updated: {TODAY}. OAuth 2.1 (draft-ietf-oauth-v2-1) is in IETF draft status as of 2026. Major providers (Auth0, Okta, Cognito, Google) already implement the security requirements.</div>

<h2>What is removed in OAuth 2.1</h2>

<h3>1. Implicit Flow (response_type=token) — REMOVED</h3>
<p>The Implicit Flow returns tokens directly in the URL fragment. This means access tokens appear in browser history, server logs, and can be leaked via the Referer header. All OAuth 2.1 clients must use Authorization Code + PKCE instead.</p>
<pre># OAuth 2.0 — Implicit Flow (do not use)
GET /authorize?response_type=token&client_id=...
# Returns: https://app.com/callback#access_token=eyJ...  ❌ token in URL

# OAuth 2.1 — Authorization Code + PKCE (correct)
GET /authorize?response_type=code&code_challenge=...&code_challenge_method=S256
# Returns: https://app.com/callback?code=abc123  ✅ code, not token</pre>

<h3>2. Resource Owner Password Credentials (ROPC) — REMOVED</h3>
<p>The password grant requires the client to collect and transmit the user's username and password — defeating the security purpose of OAuth. Remove any <code>grant_type=password</code> flows in your applications.</p>
<pre># Do not use
POST /token
grant_type=password&username=user@example.com&password=secret  ❌

# Use authorization code flow instead — user logs in at the auth server</pre>

<h2>What is now required in OAuth 2.1</h2>

<h3>PKCE required for all clients</h3>
<p>PKCE (Proof Key for Code Exchange) was previously only required for public clients (SPAs, mobile apps). OAuth 2.1 requires PKCE for all authorization code flows — including confidential clients (server-side apps with a client secret).</p>
<pre>// All OAuth 2.1 authorization requests must include:
const params = new URLSearchParams({{
  response_type: 'code',
  client_id: CLIENT_ID,
  redirect_uri: REDIRECT_URI,
  code_challenge: challenge,          // required
  code_challenge_method: 'S256',      // required — plain is not allowed
  scope: 'openid profile',
}});</pre>

<h3>Redirect URI exact matching</h3>
<p>OAuth 2.1 mandates exact string matching for redirect URIs. Partial path matching and wildcard patterns are prohibited. All environments (dev, staging, production) must be registered as separate URIs.</p>

<h3>Bearer token transmission</h3>
<p>Access tokens must only be sent in the Authorization header. Sending tokens in URL query parameters (<code>?access_token=...</code>) is prohibited in OAuth 2.1.</p>
<pre># Correct — Authorization header
GET /api/resource HTTP/1.1
Authorization: Bearer eyJhbGc...  ✅

# Prohibited — URL parameter
GET /api/resource?access_token=eyJhbGc...  ❌</pre>

<h2>What OAuth 2.1 does not change</h2>
<ul>
  <li>Client Credentials flow — unchanged, no PKCE required for machine-to-machine</li>
  <li>Refresh Token flow — unchanged</li>
  <li>Device Authorization flow — unchanged</li>
  <li>Token formats — no requirement for JWT, opaque tokens still valid</li>
  <li>Scope semantics — no changes</li>
</ul>

<h2>Provider support status</h2>
<table>
  <thead><tr><th>Provider</th><th>PKCE required</th><th>Implicit blocked</th><th>ROPC blocked</th></tr></thead>
  <tbody>
    <tr><td>Auth0</td><td>✅ Yes (configurable)</td><td>✅ Deprecated</td><td>✅ Available but deprecated</td></tr>
    <tr><td>Okta</td><td>✅ Yes (configurable)</td><td>✅ Removed for new apps</td><td>⚠️ Available</td></tr>
    <tr><td>AWS Cognito</td><td>✅ Yes for SPAs</td><td>⚠️ Still available</td><td>⚠️ Available</td></tr>
    <tr><td>Google</td><td>✅ Enforced</td><td>✅ Removed</td><td>N/A</td></tr>
    <tr><td>Microsoft/Azure</td><td>✅ Yes</td><td>⚠️ Still available</td><td>⚠️ Available</td></tr>
  </tbody>
</table>

<h2>Migration checklist</h2>
<ul>
  <li>Find all <code>response_type=token</code> flows and replace with Authorization Code + PKCE</li>
  <li>Find all <code>grant_type=password</code> flows and replace with a redirect-based flow</li>
  <li>Add PKCE to server-side apps that use Authorization Code without it</li>
  <li>Ensure all redirect URIs are registered as exact strings in provider dashboards</li>
  <li>Audit any code that appends tokens to URLs</li>
</ul>"""
        }
    ]

    for log in changelogs:
        write(f"changelog/{log['slug']}/index.html", page(
            title=log["title"], desc=log["desc"],
            canonical=f"{BASE_URL}/changelog/{log['slug']}/",
            schema=make_schema(log["title"], log["desc"], f"{BASE_URL}/changelog/{log['slug']}/",
                faqs=[("When was this last updated?", f"This page was last updated {log['updated']}."),
                      ("What changed?", "See the full changelog in the article above.")]),
            label="Changelog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/changelog/">Changelog</a> → {log["title"]}',
            tag=log["tag"], tag_color=log["tag_color"],
            h1=log["title"], content=log["content"],
            cta_url="/", cta_text="Verify your config → HttpFixer Tools",
            related='<a href="/blog/">Blog</a> <a href="/glossary/">Glossary</a>'
        ))

    # Changelog index
    write("changelog/index.html", page(
        title="HttpFixer Changelog — Browser & Spec Changes That Affect Your Config",
        desc="Updated reference pages tracking browser support changes, spec updates, and deprecated headers. Last updated 2026.",
        canonical=f"{BASE_URL}/changelog/",
        schema={"@context": "https://schema.org", "@type": "CollectionPage",
                "name": "HttpFixer Changelog", "url": f"{BASE_URL}/changelog/"},
        label="Changelog",
        breadcrumb=f'<a href="/">HttpFixer</a> → Changelog',
        tag="Changelog", tag_color=PURPLE_TAG,
        h1="Changelog",
        content=f"""
<p class="lead">Browser support and spec changes that affect security headers, CSP, and OAuth. Updated when something material changes.</p>
<div class="note-box">Pages in this section are living documents — updated when browsers ship new support or specs change. Last updated: {TODAY}</div>
<ul style="list-style:none;padding:0;margin:1.5rem 0">
  <li style="margin-bottom:1rem;padding:1rem;background:var(--surface);border:1px solid var(--border);border-radius:6px">
    <a href="/changelog/csp-browser-support-2026/" style="color:var(--text);text-decoration:none;font-weight:600">CSP Browser Support 2026 — Directive Compatibility Table</a>
    <p style="font-size:12px;opacity:0.6;margin:0.3rem 0 0">Which CSP directives work in Chrome, Firefox, Safari, Edge — including Trusted Types and newer directives.</p>
  </li>
  <li style="margin-bottom:1rem;padding:1rem;background:var(--surface);border:1px solid var(--border);border-radius:6px">
    <a href="/changelog/http-security-headers-2026/" style="color:var(--text);text-decoration:none;font-weight:600">HTTP Security Headers 2026 — What Changed, What's New</a>
    <p style="font-size:12px;opacity:0.6;margin:0.3rem 0 0">X-XSS-Protection deprecated, COEP credentialless support, HSTS preload stricter minimum — all 2025–2026 changes.</p>
  </li>
  <li style="padding:1rem;background:var(--surface);border:1px solid var(--border);border-radius:6px">
    <a href="/changelog/oauth-21-changes/" style="color:var(--text);text-decoration:none;font-weight:600">OAuth 2.1 Changes — What Developers Need to Update</a>
    <p style="font-size:12px;opacity:0.6;margin:0.3rem 0 0">Implicit Flow removed, ROPC removed, PKCE required for all clients. Migration checklist included.</p>
  </li>
</ul>""",
        cta_url="/", cta_text="Scan your live site → HttpFixer Tools",
        related='<a href="/blog/">Blog</a> <a href="/generators/">Generators</a>'
    ))


# ─── TASK 5 — UPDATE SITEMAP ──────────────────────────────────────────────────

def update_sitemap():
    print("\n📍 Updating sitemap.xml with new pages")

    skip_dirs = {".git", "node_modules", ".vercel", ".next", "__pycache__"}
    urls = []

    def priority(path):
        if path == "/": return "1.0", "daily"
        if path in ("/cors/", "/oauth/", "/csp/", "/edge/", "/speedfixer/"): return "0.9", "weekly"
        if path.startswith("/generators/"): return "0.8", "weekly"
        if path.startswith("/blog/cors/") and path.count("/") == 3: return "0.8", "monthly"
        if path.startswith("/blog/") and path.count("/") == 3: return "0.7", "monthly"
        if path.startswith("/blog/"): return "0.6", "monthly"
        if path.startswith("/case-studies/"): return "0.7", "monthly"
        if path.startswith("/changelog/"): return "0.6", "monthly"
        if path.startswith("/fix/"): return "0.6", "monthly"
        if path.startswith("/error/"): return "0.6", "monthly"
        if path.startswith("/providers/"): return "0.5", "monthly"
        if path.startswith("/glossary/"): return "0.5", "monthly"
        if path.startswith("/learn/"): return "0.5", "monthly"
        if path.startswith("/vs/"): return "0.5", "monthly"
        return "0.4", "monthly"

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
        for f in files:
            if f != "index.html":
                continue
            rel = root[2:] if root.startswith("./") else root
            if rel == ".":
                rel = ""
            url_path = ("/" + rel + "/").replace("//", "/")
            if url_path == "//":
                url_path = "/"
            prio, freq = priority(url_path)
            urls.append((url_path, prio, freq))

    urls.sort(key=lambda x: (0 if x[0] == "/" else 1, -float(x[1]), x[0]))
    seen = set()
    unique = []
    for u in urls:
        if u[0] not in seen:
            seen.add(u[0])
            unique.append(u)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio, freq in unique:
        lines.append(f"""  <url>
    <loc>{BASE_URL}{path}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>""")
    lines.append("</urlset>")

    with open("sitemap.xml", "w") as f:
        f.write("\n".join(lines))

    print(f"  ✓ sitemap.xml — {len(unique)} URLs")
    return len(unique)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🚀 HttpFixer — Generators, Case Studies, Changelogs, Schema")
    print("=" * 60)

    inject_tool_schema()
    generate_generator_pages()
    generate_case_studies()
    generate_changelogs()
    url_count = update_sitemap()

    print(f"""
✅ Done.

  Schema patched   → 6 tool pages (WebApplication + FAQPage + BreadcrumbList)
  Generators       → 5 pages (CSP, CORS, Security Headers, Permissions-Policy, index)
  Case Studies     → 4 pages (SharePoint, CloudFront, Azure APIM, index)
  Changelogs       → 4 pages (CSP browser compat, Headers 2026, OAuth 2.1, index)
  Sitemap          → {url_count} URLs

Run:
  git add -A
  git commit -m "feat: generator pages, case studies, changelogs, tool schema"
  git push origin main
  npx vercel --prod --force

Then in GSC — manually request indexing on:
  /generators/
  /generators/csp/
  /generators/cors/
  /generators/security-headers/
  /case-studies/sharepoint-csp-blocked/
  /changelog/oauth-21-changes/
""")
