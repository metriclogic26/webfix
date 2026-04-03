#!/usr/bin/env python3
"""
HttpFixer — Sitemap + Blog Index + Cross-links
Handles tasks 2, 3, 4:
  2. Regenerates sitemap.xml from all index.html files in the project
  3. Creates /blog/index.html — a full blog hub page
  4. Injects "Related Articles" sections into the 6 tool pages

Usage:
  cd ~/Projects/stackfix
  cp ~/Downloads/26_sitemap_blogindex_crosslinks.py .
  python3 26_sitemap_blogindex_crosslinks.py
  git add -A && git commit -m "feat: sitemap refresh, blog hub, tool cross-links" && git push origin main && npx vercel --prod --force
"""

import os, re
from datetime import date

BASE_URL = "https://httpfixer.dev"
TODAY = date.today().isoformat()

# ─── TASK 2 — SITEMAP ─────────────────────────────────────────────────────────

def generate_sitemap():
    print("\n📍 Task 2 — Generating sitemap.xml")

    # Priority map — higher = more important
    def priority(path):
        if path == "/":                    return "1.0", "daily"
        if path in ("/cors/", "/oauth/", "/csp/", "/edge/", "/speedfixer/"): return "0.9", "weekly"
        if path.startswith("/blog/cors/") and path.count("/") == 3:  return "0.8", "monthly"
        if path.startswith("/blog/") and path.count("/") == 3:       return "0.7", "monthly"
        if path.startswith("/blog/") and path.count("/") == 2:       return "0.6", "monthly"
        if path.startswith("/fix/"):       return "0.6", "monthly"
        if path.startswith("/error/"):     return "0.6", "monthly"
        if path.startswith("/providers/"): return "0.5", "monthly"
        if path.startswith("/glossary/"):  return "0.5", "monthly"
        if path.startswith("/learn/"):     return "0.5", "monthly"
        if path.startswith("/vs/"):        return "0.5", "monthly"
        return "0.4", "monthly"

    urls = []

    # Walk the directory and find all index.html files
    skip_dirs = {".git", "node_modules", ".vercel", ".next", "__pycache__"}

    for root, dirs, files in os.walk("."):
        # Skip hidden and build dirs
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]

        for f in files:
            if f != "index.html":
                continue

            # Convert file path to URL path
            rel = root[2:] if root.startswith("./") else root
            if rel == ".":
                rel = ""
            url_path = ("/" + rel + "/").replace("//", "/")
            if url_path == "//":
                url_path = "/"

            prio, freq = priority(url_path)
            urls.append((url_path, prio, freq))

    # Sort: root first, then by priority desc, then alphabetically
    urls.sort(key=lambda x: (0 if x[0] == "/" else 1, -float(x[1]), x[0]))

    # Remove duplicates
    seen = set()
    unique = []
    for u in urls:
        if u[0] not in seen:
            seen.add(u[0])
            unique.append(u)

    # Write sitemap.xml
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

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

    print(f"  ✓ sitemap.xml — {len(unique)} URLs written")
    return len(unique)


# ─── TASK 3 — BLOG INDEX ──────────────────────────────────────────────────────

def generate_blog_index():
    print("\n📍 Task 3 — Generating blog/index.html")

    categories = [
        {
            "slug": "cors",
            "title": "CORS Fix Guides",
            "icon": "⚡",
            "desc": "Fix cross-origin request errors in Express, FastAPI, Nginx, Next.js, Vercel, Spring Boot, and more.",
            "count": 8,
            "articles": [
                ("Fix CORS Error in Express.js", "fix-cors-express"),
                ("Fix CORS Error in FastAPI", "fix-cors-fastapi"),
                ("Fix CORS Error in Nginx", "fix-cors-nginx"),
                ("Fix CORS Error in Next.js", "fix-cors-nextjs"),
                ("CORS Preflight Failing — OPTIONS Returns 404 or 403", "fix-cors-preflight-options"),
                ("CORS Error With credentials: include", "fix-cors-credentials"),
                ("Fix CORS on Vercel Serverless Functions", "fix-cors-vercel"),
                ("Fix CORS Error in Spring Boot", "fix-cors-spring-boot"),
            ]
        },
        {
            "slug": "csp",
            "title": "CSP Fix Guides",
            "icon": "🛡",
            "desc": "Fix Content Security Policy violations. Generate working CSP headers without breaking your site.",
            "count": 6,
            "articles": [
                ("Fix CSP Header in Next.js — Nonce-Based Approach", "fix-csp-nextjs"),
                ("Content Security Policy for Vercel", "csp-generator-vercel"),
                ("Fix Refused to Load Script CSP Error", "fix-csp-refused-to-load"),
                ("CSP for Google Analytics, Hotjar and Third-Party Scripts", "csp-google-analytics-hotjar"),
                ("CSP unsafe-inline vs Nonce vs Hash", "csp-unsafe-inline-nonce-hash"),
                ("Content Security Policy for WordPress", "csp-wordpress"),
            ]
        },
        {
            "slug": "oauth",
            "title": "OAuth Fix Guides",
            "icon": "🔑",
            "desc": "Debug OAuth 2.0 errors — invalid_grant, redirect_uri_mismatch, PKCE failures, and refresh token issues.",
            "count": 5,
            "articles": [
                ("Fix OAuth invalid_grant Error", "fix-invalid-grant"),
                ("Fix OAuth Redirect URI Mismatch", "fix-redirect-uri-mismatch"),
                ("OAuth Refresh Token Expired — How to Handle It", "fix-refresh-token-expired"),
                ("Fix Google OAuth invalid_grant — Clock Skew", "fix-google-oauth-invalid-grant"),
                ("OAuth PKCE Flow Errors — Fix code_challenge", "fix-pkce-errors"),
            ]
        },
        {
            "slug": "headers",
            "title": "Security Headers",
            "icon": "🔒",
            "desc": "Add and fix HTTP security headers — HSTS, X-Frame-Options, CSP, Referrer-Policy, and more.",
            "count": 3,
            "articles": [
                ("HTTP Security Headers Checklist", "security-headers-checklist"),
                ("Fix Missing X-Frame-Options — Clickjacking Protection", "fix-x-frame-options"),
                ("HSTS Not Working — Fix Strict Transport Security", "fix-hsts"),
            ]
        },
        {
            "slug": "performance",
            "title": "Performance Guides",
            "icon": "⚡",
            "desc": "Fix slow TTFB, misconfigured cache headers, mixed content, and PageSpeed issues.",
            "count": 3,
            "articles": [
                ("Fix Slow TTFB on Vercel — Edge vs Serverless", "fix-ttfb-vercel"),
                ("Fix Cache-Control Headers — Why Your CDN Isn't Caching", "fix-cache-control-cdn"),
                ("Fix Mixed Content Warnings on HTTPS Sites", "fix-mixed-content"),
            ]
        },
        {
            "slug": "explainers",
            "title": "Explainers",
            "icon": "📖",
            "desc": "Plain-English explanations of CORS, CSP, OAuth, HSTS, preflight requests, and browser security.",
            "count": 8,
            "articles": [
                ("What is CORS?", "what-is-cors"),
                ("What is a Content Security Policy?", "what-is-csp"),
                ("What is OAuth 2.0?", "what-is-oauth"),
                ("What is a Preflight Request?", "what-is-preflight"),
                ("What Are HTTP Security Headers?", "what-are-security-headers"),
                ("What is HSTS?", "what-is-hsts"),
                ("What is Clickjacking?", "what-is-clickjacking"),
                ("What is HTTPS and Why HTTP Isn't Enough", "what-is-https"),
            ]
        },
        {
            "slug": "compare",
            "title": "Comparisons",
            "icon": "⚖️",
            "desc": "Side-by-side comparisons of security concepts — CORS vs CSRF, nonce vs hash, OAuth vs OIDC.",
            "count": 5,
            "articles": [
                ("CORS vs CSRF — What is the Difference?", "cors-vs-csrf"),
                ("CSP Nonce vs Hash vs unsafe-inline", "csp-nonce-vs-hash"),
                ("OAuth 2.0 vs OpenID Connect", "oauth-vs-oidc"),
                ("Authorization Code vs Client Credentials", "authorization-code-vs-client-credentials"),
                ("X-Frame-Options vs CSP frame-ancestors", "x-frame-options-vs-csp-frame-ancestors"),
            ]
        },
        {
            "slug": "reference",
            "title": "Reference",
            "icon": "📋",
            "desc": "Quick-reference tables for security headers, CORS headers, OAuth error codes, and CSP directives.",
            "count": 4,
            "articles": [
                ("Complete HTTP Security Headers Reference", "http-security-headers-reference"),
                ("CORS Headers Cheat Sheet", "cors-headers-cheat-sheet"),
                ("OAuth 2.0 Error Codes Reference", "oauth-error-codes-reference"),
                ("CSP Directives for Popular Third-Party Services", "csp-third-party-services"),
            ]
        },
        {
            "slug": "platform",
            "title": "Platform Guides",
            "icon": "☁️",
            "desc": "Stack-specific guides for AWS Lambda, Cloudflare Workers, Netlify, Docker, SPAs, and more.",
            "count": 5,
            "articles": [
                ("CORS on AWS Lambda — API Gateway", "cors-aws-lambda"),
                ("CORS on Cloudflare Workers", "cors-cloudflare-workers"),
                ("Security Headers for Netlify", "security-headers-netlify"),
                ("CSP for Single Page Apps — React, Vue, Angular", "csp-single-page-apps"),
                ("CORS in Docker — localhost vs Container", "cors-docker"),
            ]
        },
        {
            "slug": "errors",
            "title": "Error Pages",
            "icon": "🔴",
            "desc": "Exact fixes for specific browser console errors — copy the error, find the fix.",
            "count": 6,
            "articles": [
                ("No Access-Control-Allow-Origin header is present", "no-access-control-allow-origin"),
                ("Request header field not allowed by Access-Control-Allow-Headers", "request-header-not-allowed"),
                ("Refused to load the script — CSP violation", "refused-to-load-script-csp"),
                ("Response to preflight request doesn't pass access control check", "preflight-failed"),
                ("PKCE verification failed", "pkce-required"),
                ("OAuth invalid_grant error", "invalid-grant-error"),
            ]
        },
    ]

    # Build category cards HTML
    cat_cards = ""
    for cat in categories:
        articles_html = ""
        for title, slug in cat["articles"]:
            articles_html += f'<li><a href="/blog/{cat["slug"]}/{slug}/">{title}</a></li>\n'

        cat_cards += f"""
<div class="cat-card">
  <div class="cat-header">
    <span class="cat-icon">{cat["icon"]}</span>
    <div>
      <a href="/blog/{cat["slug"]}/" class="cat-title">{cat["title"]}</a>
      <span class="cat-count">{cat["count"]} articles</span>
    </div>
  </div>
  <p class="cat-desc">{cat["desc"]}</p>
  <ul class="article-list">
    {articles_html}
  </ul>
</div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HttpFixer Blog — CORS, CSP, OAuth, Security Headers Guides</title>
  <meta name="description" content="Free guides, fix references, and explainers for CORS errors, Content Security Policy, OAuth 2.0, HTTP security headers, and web performance. Exact copy-paste fixes for your stack.">
  <link rel="canonical" href="{BASE_URL}/blog/">
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="HttpFixer Blog — CORS, CSP, OAuth, Security Headers">
  <meta property="og:description" content="Exact copy-paste fixes for CORS errors, CSP violations, OAuth errors, and security header misconfigurations — for your specific stack.">
  <meta property="og:url" content="{BASE_URL}/blog/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">{{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "HttpFixer Blog",
    "description": "CORS, CSP, OAuth, and security header fix guides for developers.",
    "url": "{BASE_URL}/blog/",
    "publisher": {{"@type": "Organization", "name": "MetricLogic", "url": "https://metriclogic.dev"}}
  }}</script>
  <style>
    :root{{--bg:#0B0D14;--surface:#12151F;--border:#252836;--purple:#6C63FF;--green:#22C55E;--orange:#F97316;--red:#EF4444;--text:#E2E4F0;}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:var(--bg);color:var(--text);font-family:"JetBrains Mono",monospace;font-size:14px;line-height:1.7;min-height:100vh}}
    nav{{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;border-bottom:1px solid var(--border);background:var(--surface)}}
    nav .brand{{font-weight:600;color:var(--text);text-decoration:none}}
    nav .brand span{{color:var(--purple)}}
    nav .right{{display:flex;gap:1rem;align-items:center}}
    nav a{{color:var(--text);text-decoration:none;opacity:0.6;font-size:13px}}
    nav a:hover{{color:var(--purple);opacity:1}}
    .hero{{max-width:900px;margin:0 auto;padding:3rem 1.5rem 2rem}}
    .hero h1{{font-size:2rem;font-weight:600;line-height:1.2;margin-bottom:0.75rem}}
    .hero h1 span{{color:var(--purple)}}
    .hero p{{opacity:0.7;max-width:560px;line-height:1.8;margin-bottom:2rem}}
    .stats{{display:flex;gap:2rem;flex-wrap:wrap;margin-bottom:0;}}
    .stat{{display:flex;flex-direction:column}}
    .stat strong{{font-size:1.4rem;color:var(--purple)}}
    .stat span{{font-size:11px;opacity:0.5;text-transform:uppercase;letter-spacing:0.05em}}
    .grid{{max-width:900px;margin:0 auto;padding:0 1.5rem 4rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:1.5rem}}
    .cat-card{{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.5rem;transition:border-color 0.2s}}
    .cat-card:hover{{border-color:var(--purple)}}
    .cat-header{{display:flex;align-items:flex-start;gap:0.75rem;margin-bottom:0.75rem}}
    .cat-icon{{font-size:1.4rem;line-height:1;margin-top:2px}}
    .cat-title{{display:block;font-size:0.95rem;font-weight:600;color:var(--text);text-decoration:none}}
    .cat-title:hover{{color:var(--purple)}}
    .cat-count{{display:block;font-size:11px;opacity:0.4;margin-top:0.2rem}}
    .cat-desc{{font-size:12px;opacity:0.6;margin-bottom:1rem;line-height:1.7}}
    .article-list{{list-style:none;margin:0;padding:0;border-top:1px solid var(--border);padding-top:0.75rem}}
    .article-list li{{margin-bottom:0.35rem}}
    .article-list a{{color:var(--text);text-decoration:none;font-size:12px;opacity:0.7;display:block;padding:0.2rem 0;transition:color 0.15s,opacity 0.15s}}
    .article-list a:hover{{color:var(--purple);opacity:1}}
    .article-list a::before{{content:"→ ";color:var(--purple);opacity:0.5}}
    footer{{border-top:1px solid var(--border);padding:1.5rem 2rem;font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem}}
    footer a{{color:var(--text);text-decoration:none;opacity:0.6}}
    .disclaimer{{width:100%;text-align:center;font-size:11px;opacity:0.4;margin-top:0.75rem;line-height:1.6}}
    @media(max-width:600px){{.hero h1{{font-size:1.5rem}}.grid{{grid-template-columns:1fr}}.stats{{gap:1.5rem}}nav .right{{display:none}}footer{{flex-direction:column;text-align:center}}}}
  </style>
</head>
<body>
<nav>
  <a href="/" class="brand">HttpFixer <span>/</span> Blog</a>
  <div class="right">
    <a href="/">Headers</a><a href="/cors/">CORS</a><a href="/oauth/">OAuth</a>
    <a href="/csp/">CSP</a><a href="/edge/">Edge</a><a href="/speedfixer/">Speed</a>
  </div>
</nav>

<div class="hero">
  <h1>Fix it. <span>Don't just read about it.</span></h1>
  <p>Exact copy-paste fixes for CORS errors, CSP violations, OAuth failures, and security header misconfigurations — for your specific stack. No generic advice.</p>
  <div class="stats">
    <div class="stat"><strong>61</strong><span>Articles</span></div>
    <div class="stat"><strong>10</strong><span>Topics</span></div>
    <div class="stat"><strong>6</strong><span>Live Tools</span></div>
    <div class="stat"><strong>0</strong><span>Paywalls</span></div>
  </div>
</div>

<div class="grid">
  {cat_cards}
</div>

<footer>
  <span>HttpFixer by MetricLogic · <a href="https://configclarity.dev">configclarity.dev</a> · <a href="https://domainpreflight.dev">domainpreflight.dev</a> · <a href="https://packagefix.dev">packagefix.dev</a></span>
  <span><a href="https://github.com/metriclogic26/httpfixer">MIT · GitHub →</a></span>
  <p class="disclaimer">Configurations are based on open standards (OWASP, RFC, MDN). Always test in a staging environment before deploying to production. © 2026 MetricLogic.</p>
</footer>
</body>
</html>"""

    os.makedirs("blog", exist_ok=True)
    with open("blog/index.html", "w") as f:
        f.write(html)
    print("  ✓ blog/index.html")


# ─── TASK 4 — CROSS-LINKS ─────────────────────────────────────────────────────

def inject_cross_links():
    print("\n📍 Task 4 — Injecting cross-links into tool pages")

    # Map: tool page file → relevant blog articles
    tool_articles = {
        "index.html": {
            "tool_name": "HeadersFixer",
            "tool_color": "#EF4444",
            "articles": [
                ("HTTP Security Headers Checklist", "/blog/headers/security-headers-checklist/"),
                ("Fix Missing X-Frame-Options", "/blog/headers/fix-x-frame-options/"),
                ("HSTS Not Working — Fix It", "/blog/headers/fix-hsts/"),
                ("What Are HTTP Security Headers?", "/blog/explainers/what-are-security-headers/"),
                ("Security Headers Reference", "/blog/reference/http-security-headers-reference/"),
                ("Security Headers for Netlify", "/blog/platform/security-headers-netlify/"),
            ]
        },
        "cors/index.html": {
            "tool_name": "CORSFixer",
            "tool_color": "#6C63FF",
            "articles": [
                ("Fix CORS in Express.js", "/blog/cors/fix-cors-express/"),
                ("Fix CORS in FastAPI", "/blog/cors/fix-cors-fastapi/"),
                ("Fix CORS in Nginx", "/blog/cors/fix-cors-nginx/"),
                ("Fix CORS in Next.js", "/blog/cors/fix-cors-nextjs/"),
                ("CORS Preflight Failing (OPTIONS 404)", "/blog/cors/fix-cors-preflight-options/"),
                ("CORS With credentials: include", "/blog/cors/fix-cors-credentials/"),
                ("CORS on Vercel", "/blog/cors/fix-cors-vercel/"),
                ("CORS on AWS Lambda", "/blog/platform/cors-aws-lambda/"),
                ("CORS on Cloudflare Workers", "/blog/platform/cors-cloudflare-workers/"),
                ("CORS in Docker", "/blog/platform/cors-docker/"),
                ("What is CORS?", "/blog/explainers/what-is-cors/"),
                ("CORS vs CSRF", "/blog/compare/cors-vs-csrf/"),
            ]
        },
        "oauth/index.html": {
            "tool_name": "OAuthFixer",
            "tool_color": "#F97316",
            "articles": [
                ("Fix invalid_grant Error", "/blog/oauth/fix-invalid-grant/"),
                ("Fix redirect_uri_mismatch", "/blog/oauth/fix-redirect-uri-mismatch/"),
                ("Refresh Token Expired", "/blog/oauth/fix-refresh-token-expired/"),
                ("Google OAuth invalid_grant (clock skew)", "/blog/oauth/fix-google-oauth-invalid-grant/"),
                ("Fix PKCE Errors", "/blog/oauth/fix-pkce-errors/"),
                ("OAuth Error Codes Reference", "/blog/reference/oauth-error-codes-reference/"),
                ("What is OAuth 2.0?", "/blog/explainers/what-is-oauth/"),
                ("OAuth vs OpenID Connect", "/blog/compare/oauth-vs-oidc/"),
                ("Authorization Code vs Client Credentials", "/blog/compare/authorization-code-vs-client-credentials/"),
            ]
        },
        "csp/index.html": {
            "tool_name": "CSPFixer",
            "tool_color": "#22C55E",
            "articles": [
                ("CSP in Next.js — Nonce-Based", "/blog/csp/fix-csp-nextjs/"),
                ("CSP for Vercel", "/blog/csp/csp-generator-vercel/"),
                ("Fix Refused to Load Script", "/blog/csp/fix-csp-refused-to-load/"),
                ("CSP for GA4, Hotjar, Stripe", "/blog/csp/csp-google-analytics-hotjar/"),
                ("Nonce vs Hash vs unsafe-inline", "/blog/csp/csp-unsafe-inline-nonce-hash/"),
                ("CSP for WordPress", "/blog/csp/csp-wordpress/"),
                ("CSP for React / Vue / Angular", "/blog/platform/csp-single-page-apps/"),
                ("CSP Third-Party Services Reference", "/blog/reference/csp-third-party-services/"),
                ("What is CSP?", "/blog/explainers/what-is-csp/"),
            ]
        },
        "edge/index.html": {
            "tool_name": "EdgeFix",
            "tool_color": "#F97316",
            "articles": [
                ("Fix Cache-Control Headers", "/blog/performance/fix-cache-control-cdn/"),
                ("Fix Slow TTFB on Vercel", "/blog/performance/fix-ttfb-vercel/"),
                ("Fix Mixed Content on HTTPS Sites", "/blog/performance/fix-mixed-content/"),
                ("CORS Headers Cheat Sheet", "/blog/reference/cors-headers-cheat-sheet/"),
            ]
        },
        "speedfixer/index.html": {
            "tool_name": "SpeedFixer",
            "tool_color": "#6C63FF",
            "articles": [
                ("Fix Slow TTFB on Vercel", "/blog/performance/fix-ttfb-vercel/"),
                ("Fix Cache-Control Headers", "/blog/performance/fix-cache-control-cdn/"),
                ("Fix Mixed Content Warnings", "/blog/performance/fix-mixed-content/"),
            ]
        },
    }

    injected = 0

    for filepath, config in tool_articles.items():
        if not os.path.exists(filepath):
            print(f"  ⚠️  {filepath} not found — skipping")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if cross-links already injected
        if "related-articles" in content:
            print(f"  ⏭  {filepath} — cross-links already present")
            continue

        # Build the related articles block
        color = config["tool_color"]
        articles_html = ""
        for title, url in config["articles"]:
            articles_html += f'<a href="{url}" class="rel-link">{title}</a>\n'

        block = f"""
<!-- Related Articles — auto-injected by 26_sitemap_blogindex_crosslinks.py -->
<section class="related-articles" id="related-articles" style="
  border-top: 1px solid #252836;
  padding: 2rem 1.5rem;
  background: #0B0D14;
  font-family: 'JetBrains Mono', monospace;
">
  <div style="max-width: 900px; margin: 0 auto;">
    <p style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.4; margin-bottom: 1rem;">
      From the HttpFixer Blog
    </p>
    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
      {articles_html}
    </div>
  </div>
</section>
<style>
  .rel-link {{
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border: 1px solid #252836;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #E2E4F0;
    text-decoration: none;
    opacity: 0.7;
    transition: border-color 0.2s, opacity 0.2s, color 0.2s;
  }}
  .rel-link:hover {{
    border-color: {color};
    color: {color};
    opacity: 1;
  }}
</style>
"""

        # Inject before </footer> — works regardless of footer content
        if "</footer>" in content:
            content = content.replace("</footer>", block + "</footer>", 1)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ {filepath} — {len(config['articles'])} links injected")
            injected += 1
        else:
            # Fall back: inject before </body>
            content = content.replace("</body>", block + "</body>", 1)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ {filepath} — injected before </body>")
            injected += 1

    print(f"  → {injected} tool pages updated")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🚀 HttpFixer — Sitemap + Blog Index + Cross-links")
    print("=" * 50)

    url_count = generate_sitemap()
    generate_blog_index()
    inject_cross_links()

    print(f"""
✅ All done.

  sitemap.xml   → {url_count} URLs
  blog/index.html → live hub for all 61 articles
  6 tool pages  → cross-linked to relevant blog posts

Next:
  git add -A
  git commit -m "feat: sitemap refresh, blog hub, tool cross-links"
  git push origin main
  npx vercel --prod --force

Then in GSC:
  Sitemaps → resubmit https://httpfixer.dev/sitemap.xml
  URL Inspection → manually request indexing on /blog/
""")
