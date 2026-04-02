#!/usr/bin/env python3
"""Generate SEO content pages for webfix.dev. Run from repo root: python3 generate_seo_pages.py"""

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
    .breadcrumb {{ font-size: 12px; color: var(--text); opacity: 0.5; margin-bottom: 1.5rem; }}
    .breadcrumb a {{ color: var(--purple); text-decoration: none; }}
    h1 {{ font-size: 1.75rem; font-weight: 600; line-height: 1.3; margin-bottom: 1rem; }}
    h2 {{ font-size: 1.1rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--text); }}
    p {{ margin-bottom: 1rem; opacity: 0.9; line-height: 1.7; }}
    .tool-cta {{ display: inline-block; margin: 1.5rem 0; padding: 0.75rem 1.25rem; background: var(--purple); color: white; text-decoration: none; border-radius: 6px; font-weight: 500; font-size: 14px; }}
    .tool-cta:hover {{ filter: brightness(1.1); }}
    .code-block {{ background: #080a0f; border: 1px solid var(--border); border-radius: 6px; padding: 1rem; font-size: 12px; margin: 1rem 0; overflow-x: auto; white-space: pre; }}
    .tag {{ display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 11px; font-weight: 600; margin-right: 0.5rem; }}
    .tag-fix {{ background: rgba(34,197,94,0.15); color: var(--green); }}
    .tag-error {{ background: rgba(239,68,68,0.15); color: var(--red); }}
    .tag-provider {{ background: rgba(108,99,255,0.15); color: var(--purple); }}
    .index-list {{ list-style: none; margin: 1rem 0; }}
    .index-list li {{ margin-bottom: 0.65rem; }}
    .index-list a {{ color: var(--purple); text-decoration: none; }}
    .index-list a:hover {{ text-decoration: underline; }}
    .related-links {{ font-size: 12px; opacity: 0.7; margin: 1.5rem 0; }}
    .related-links a {{ color: var(--purple); text-decoration: none; }}
    footer {{ border-top: 1px solid var(--border); padding: 2rem 1.5rem; font-size: 12px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; opacity: 0.6; }}
    footer a {{ color: var(--text); text-decoration: none; }}
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
  <main>
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


def related_block(links: list[tuple[str, str]], *, include_vs: bool = True) -> str:
    """Build Related links row; (label, href). Optionally append WebFix vs securityheaders.com."""
    pairs = list(links)
    if include_vs:
        pairs.append(("WebFix vs securityheaders.com", "/vs/webfix-vs-securityheaders/"))
    parts = [f'<a href="{h}">{t}</a>' for t, h in pairs]
    inner = " · ".join(parts)
    return f'<div class="related-links"><span>Related:</span> {inner}</div>'


def write_page(
    rel_dir: str,
    slug: str,
    *,
    title: str,
    description: str,
    canonical: str,
    nav_section: str,
    breadcrumb: str,
    h1: str,
    content: str,
    tool_url: str,
    tool_cta_text: str,
    schema_graph: list,
    flat: bool = False,
    related: str = "",
) -> Path:
    if flat:
        out_dir = ROOT / rel_dir
    else:
        out_dir = ROOT / rel_dir / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    schema_str = ld_json({"@context": "https://schema.org", "@graph": schema_graph})
    html = (
        TEMPLATE.replace("{schema}", "__SCHEMA__")
        .format(
            title=title,
            description=description,
            canonical=canonical,
            nav_section=nav_section,
            breadcrumb=breadcrumb,
            h1=h1,
            content=content,
            tool_url=tool_url,
            tool_cta_text=tool_cta_text,
            related=related,
        )
        .replace("__SCHEMA__", schema_str)
    )
    path = out_dir / "index.html"
    path.write_text(html, encoding="utf-8")
    return path


def breadcrumb_items_to_graph(items: list[tuple[str, str]]) -> list:
    """items: (name, url) last may be ('Current', '') for no link."""
    elements = []
    pos = 1
    for name, url in items:
        if url:
            elements.append(
                {
                    "@type": "ListItem",
                    "position": pos,
                    "name": normalize_bc(name),
                    "item": f"https://webfix.dev{url}",
                }
            )
        else:
            elements.append({"@type": "ListItem", "position": pos, "name": normalize_bc(name)})
        pos += 1
    return [{"@type": "BreadcrumbList", "itemListElement": elements}]


def normalize_bc(s: str) -> str:
    return s.replace("&rarr;", "→").strip()


def bc_html(items: list[tuple[str, str | None]]) -> str:
    parts = []
    for name, href in items:
        if href:
            parts.append(f'<a href="{href}">{name}</a>')
        else:
            parts.append(name)
    return " → ".join(parts)


def seo_related_fix(cat: str, _slug: str) -> str:
    if cat == "headers":
        return related_block(
            [
                ("HSTS (glossary)", "/glossary/hsts/"),
                ("CSP (glossary)", "/glossary/content-security-policy/"),
            ]
        )
    if cat == "cors":
        return related_block(
            [
                ("CORS (glossary)", "/glossary/cors/"),
                ("Preflight (glossary)", "/glossary/preflight-request/"),
            ]
        )
    if cat == "csp":
        return related_block(
            [
                ("CSP (glossary)", "/glossary/content-security-policy/"),
                ("unsafe-inline", "/glossary/unsafe-inline/"),
                ("CSP nonce", "/glossary/csp-nonce/"),
            ]
        )
    if cat == "oauth":
        return related_block(
            [
                ("PKCE (glossary)", "/glossary/pkce/"),
                ("OAuth grants", "/glossary/oauth-grant-types/"),
            ]
        )
    if cat == "cache":
        return related_block(
            [
                ("Cache-Control", "/glossary/cache-control/"),
                ("Vary", "/glossary/vary-header/"),
                ("ETag", "/glossary/etag/"),
            ]
        )
    if cat == "pagespeed":
        return related_block(
            [
                ("Core Web Vitals", "/glossary/core-web-vitals/"),
                ("LCP", "/glossary/largest-contentful-paint/"),
            ]
        )
    return related_block([("Fix guides", "/fix/")])


def seo_related_error(slug: str) -> str:
    if slug == "cors-blocked":
        return related_block(
            [
                ("Fix CORS (Nginx)", "/fix/cors/nginx/"),
                ("Fix CORS (Express)", "/fix/cors/express/"),
            ]
        )
    if slug == "csp-refused-to-load":
        return related_block(
            [
                ("Fix CSP (Nginx)", "/fix/csp/nginx/"),
                ("Fix CSP (Cloudflare)", "/fix/csp/cloudflare/"),
                ("Fix CSP (SharePoint)", "/fix/csp/sharepoint/"),
            ]
        )
    if slug == "invalid-grant":
        return related_block(
            [
                ("Fix OAuth (Auth0)", "/fix/oauth/auth0/"),
                ("Fix OAuth (Cognito)", "/fix/oauth/cognito/"),
            ]
        )
    if slug == "redirect-uri-mismatch":
        return related_block(
            [
                ("Fix OAuth (Auth0)", "/fix/oauth/auth0/"),
                ("Fix OAuth (Okta)", "/fix/oauth/okta/"),
            ]
        )
    if slug == "pkce-required":
        return related_block(
            [
                ("PKCE (glossary)", "/glossary/pkce/"),
                ("Fix OAuth (Auth0)", "/fix/oauth/auth0/"),
            ]
        )
    if slug.startswith("pagespeed-"):
        return related_block(
            [
                ("Fix PageSpeed (Nginx)", "/fix/pagespeed/nginx/"),
                ("Fix PageSpeed (Cloudflare)", "/fix/pagespeed/cloudflare/"),
            ]
        )
    if slug == "hsts-missing":
        return related_block(
            [
                ("HSTS (glossary)", "/glossary/hsts/"),
                ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ]
        )
    if slug == "mixed-content":
        return related_block(
            [
                ("CSP (glossary)", "/glossary/content-security-policy/"),
                ("Fix CSP (Nginx)", "/fix/csp/nginx/"),
            ]
        )
    if slug == "cache-authenticated-response":
        return related_block(
            [
                ("Cache-Control", "/glossary/cache-control/"),
                ("Fix cache (Nginx)", "/fix/cache/nginx/"),
            ]
        )
    if slug == "x-frame-options-missing":
        return related_block(
            [
                ("X-Frame-Options", "/glossary/x-frame-options/"),
                ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ]
        )
    return related_block([("Error guides", "/error/")])


ITEMLIST_FIX_INDEX = {
    "@type": "ItemList",
    "name": "WebFix — Security & Performance Fix Guides",
    "description": "Copy-paste config fixes for security headers, CORS, CSP, OAuth, cache headers, and PageSpeed — for Nginx, Cloudflare, Vercel, Apache, and more.",
    "numberOfItems": 27,
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Fix Missing Security Headers on Nginx",
            "url": "https://webfix.dev/fix/headers/nginx/",
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Fix Missing Security Headers on Cloudflare",
            "url": "https://webfix.dev/fix/headers/cloudflare/",
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Fix SharePoint CSP Refused to Load",
            "url": "https://webfix.dev/fix/headers/sharepoint/",
        },
        {
            "@type": "ListItem",
            "position": 4,
            "name": "Fix CORS Errors on Express",
            "url": "https://webfix.dev/fix/cors/express/",
        },
        {
            "@type": "ListItem",
            "position": 5,
            "name": "Fix CORS Errors on FastAPI",
            "url": "https://webfix.dev/fix/cors/fastapi/",
        },
        {
            "@type": "ListItem",
            "position": 6,
            "name": "Fix CORS Errors on Nginx",
            "url": "https://webfix.dev/fix/cors/nginx/",
        },
        {
            "@type": "ListItem",
            "position": 7,
            "name": "Fix OAuth invalid_grant on Auth0",
            "url": "https://webfix.dev/fix/oauth/auth0/",
        },
        {
            "@type": "ListItem",
            "position": 8,
            "name": "Fix OAuth Errors on Cognito",
            "url": "https://webfix.dev/fix/oauth/cognito/",
        },
        {
            "@type": "ListItem",
            "position": 9,
            "name": "Fix PageSpeed Score on Nginx",
            "url": "https://webfix.dev/fix/pagespeed/nginx/",
        },
        {
            "@type": "ListItem",
            "position": 10,
            "name": "Fix PageSpeed Score on Cloudflare",
            "url": "https://webfix.dev/fix/pagespeed/cloudflare/",
        },
    ],
}

ITEMLIST_GLOSSARY_INDEX = {
    "@type": "ItemList",
    "name": "WebFix Security Glossary",
    "description": "Plain-English definitions of web security and performance terms — CSP, HSTS, CORS, PKCE, Cache-Control, Core Web Vitals, and more.",
    "numberOfItems": 20,
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Content Security Policy (CSP)",
            "url": "https://webfix.dev/glossary/content-security-policy/",
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "HTTP Strict Transport Security (HSTS)",
            "url": "https://webfix.dev/glossary/hsts/",
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Cross-Origin Resource Sharing (CORS)",
            "url": "https://webfix.dev/glossary/cors/",
        },
        {
            "@type": "ListItem",
            "position": 4,
            "name": "CORS Preflight Request",
            "url": "https://webfix.dev/glossary/preflight-request/",
        },
        {
            "@type": "ListItem",
            "position": 5,
            "name": "CSP Nonce",
            "url": "https://webfix.dev/glossary/csp-nonce/",
        },
        {
            "@type": "ListItem",
            "position": 6,
            "name": "unsafe-inline CSP directive",
            "url": "https://webfix.dev/glossary/unsafe-inline/",
        },
        {
            "@type": "ListItem",
            "position": 7,
            "name": "PKCE — Proof Key for Code Exchange",
            "url": "https://webfix.dev/glossary/pkce/",
        },
        {
            "@type": "ListItem",
            "position": 8,
            "name": "Cache-Control",
            "url": "https://webfix.dev/glossary/cache-control/",
        },
        {
            "@type": "ListItem",
            "position": 9,
            "name": "Core Web Vitals",
            "url": "https://webfix.dev/glossary/core-web-vitals/",
        },
        {
            "@type": "ListItem",
            "position": 10,
            "name": "Largest Contentful Paint (LCP)",
            "url": "https://webfix.dev/glossary/largest-contentful-paint/",
        },
    ],
}

ITEMLIST_PROVIDERS_INDEX = {
    "@type": "ItemList",
    "name": "WebFix — Fix Guides by Stack",
    "description": "Security and performance fix guides for Nginx, Cloudflare, Vercel, Apache, Express, Next.js, FastAPI, WordPress, and more.",
    "numberOfItems": 14,
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Nginx Security & Performance Fixes",
            "url": "https://webfix.dev/providers/nginx/",
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Cloudflare Security & Performance Fixes",
            "url": "https://webfix.dev/providers/cloudflare/",
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Vercel Security & Performance Fixes",
            "url": "https://webfix.dev/providers/vercel/",
        },
        {
            "@type": "ListItem",
            "position": 4,
            "name": "Express Security Fixes",
            "url": "https://webfix.dev/providers/express/",
        },
        {
            "@type": "ListItem",
            "position": 5,
            "name": "FastAPI CORS & Security Fixes",
            "url": "https://webfix.dev/providers/fastapi/",
        },
        {
            "@type": "ListItem",
            "position": 6,
            "name": "WordPress Performance Fixes",
            "url": "https://webfix.dev/providers/wordpress/",
        },
    ],
}

ITEMLIST_ERROR_INDEX = {
    "@type": "ItemList",
    "name": "WebFix — Web Error Fix Guides",
    "description": "Fix guides for CORS blocked errors, CSP refused to load, OAuth invalid_grant, redirect_uri mismatch, PageSpeed failures, and more.",
    "numberOfItems": 12,
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "CORS Error: Access Blocked",
            "url": "https://webfix.dev/error/cors-blocked/",
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "CSP: Refused to Load Script",
            "url": "https://webfix.dev/error/csp-refused-to-load/",
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "OAuth Error: invalid_grant",
            "url": "https://webfix.dev/error/invalid-grant/",
        },
        {
            "@type": "ListItem",
            "position": 4,
            "name": "OAuth Error: redirect_uri_mismatch",
            "url": "https://webfix.dev/error/redirect-uri-mismatch/",
        },
        {
            "@type": "ListItem",
            "position": 5,
            "name": "PageSpeed: Render-Blocking Resources",
            "url": "https://webfix.dev/error/pagespeed-render-blocking/",
        },
        {
            "@type": "ListItem",
            "position": 6,
            "name": "Security: Authenticated Response Cached",
            "url": "https://webfix.dev/error/cache-authenticated-response/",
        },
    ],
}


def seo_related_provider(slug: str) -> str:
    hub: dict[str, list[tuple[str, str]]] = {
        "nginx": [
            ("Fix headers (Nginx)", "/fix/headers/nginx/"),
            ("Fix CORS (Nginx)", "/fix/cors/nginx/"),
            ("Fix CSP (Nginx)", "/fix/csp/nginx/"),
        ],
        "apache": [("Fix headers (Apache)", "/fix/headers/apache/")],
        "cloudflare": [
            ("Fix headers (Cloudflare)", "/fix/headers/cloudflare/"),
            ("Fix CSP (Cloudflare)", "/fix/csp/cloudflare/"),
            ("Fix cache (Cloudflare)", "/fix/cache/cloudflare/"),
        ],
        "vercel": [
            ("Fix headers (Vercel)", "/fix/headers/vercel/"),
            ("Fix CSP (Vercel)", "/fix/csp/vercel/"),
            ("Fix PageSpeed (Vercel)", "/fix/pagespeed/vercel/"),
        ],
        "netlify": [("Fix headers (Netlify)", "/fix/headers/netlify/")],
        "express": [
            ("Fix headers (Express)", "/fix/headers/express/"),
            ("Fix CORS (Express)", "/fix/cors/express/"),
        ],
        "nextjs": [
            ("Fix CORS (Next.js)", "/fix/cors/nextjs/"),
            ("Fix headers (Vercel)", "/fix/headers/vercel/"),
        ],
        "django": [("Fix CORS (Django)", "/fix/cors/django/")],
        "fastapi": [("Fix CORS (FastAPI)", "/fix/cors/fastapi/")],
        "flask": [("Fix CORS (Flask)", "/fix/cors/flask/")],
        "wordpress": [("Fix PageSpeed (WordPress)", "/fix/pagespeed/wordpress/")],
        "auth0": [
            ("Fix OAuth (Auth0)", "/fix/oauth/auth0/"),
            ("invalid_grant error", "/error/invalid-grant/"),
        ],
        "okta": [
            ("Fix OAuth (Okta)", "/fix/oauth/okta/"),
            ("redirect_uri mismatch", "/error/redirect-uri-mismatch/"),
        ],
        "cognito": [("Fix OAuth (Cognito)", "/fix/oauth/cognito/")],
    }
    return related_block(hub.get(slug, [("Provider hubs", "/providers/")]))


def main() -> None:
    created: list[Path] = []
    dirs_set: set[str] = set()

    def tech_article(
        headline: str,
        url_path: str,
        description: str,
        date_published: str = "2026-03-31",
    ) -> dict:
        return {
            "@type": "TechArticle",
            "headline": headline,
            "description": description,
            "url": f"https://webfix.dev{url_path}",
            "datePublished": date_published,
            "author": {"@type": "Organization", "name": "MetricLogic"},
            "publisher": {"@type": "Organization", "name": "MetricLogic", "url": "https://metriclogic.dev"},
        }

    def article_ld(headline: str, url_path: str, description: str) -> dict:
        return {
            "@type": "Article",
            "headline": headline,
            "description": description,
            "url": f"https://webfix.dev{url_path}",
            "author": {"@type": "Organization", "name": "MetricLogic"},
            "publisher": {"@type": "Organization", "name": "MetricLogic", "url": "https://metriclogic.dev"},
        }

    def collection_ld(name: str, url_path: str, description: str) -> dict:
        return {
            "@type": "CollectionPage",
            "name": name,
            "description": description,
            "url": f"https://webfix.dev{url_path}",
        }

    # ——— GROUP 1: FIX PAGES ———
    FIX = [
        (
            "headers",
            "nginx",
            "Fix Missing Security Headers on Nginx — WebFix",
            "Add HSTS, CSP, X-Frame-Options, and related headers in nginx.conf server blocks with add_header directives.",
            '<p>Nginx does not ship secure defaults for <code>HSTS</code>, <code>Content-Security-Policy</code>, or <code>X-Frame-Options</code>. Most breaches start with a missing or weak header set, so production <code>server { }</code> blocks should declare explicit policies instead of relying on application code.</p><p>Use <code>add_header</code> (and <code>always</code> where you need headers on error responses) for strict transport, framing, referrer, and permissions. Place policies once per server name, then reload with <code>nginx -t</code> before <code>systemctl reload nginx</code>.</p><p><a href="/fix/headers/apache/">Apache</a> and <a href="/fix/headers/cloudflare/">Cloudflare</a> guides cover the same controls on other stacks. HeadersFixer scans your live URL and outputs copy-paste snippets matched to what your site actually needs.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/fix/headers/nginx/",
        ),
        (
            "headers",
            "apache",
            "Fix Missing Security Headers on Apache — WebFix",
            "Set HSTS, CSP, and X-Frame-Options using mod_headers in .htaccess or VirtualHost configuration.",
            '<p>Apache can emit security headers with <code>mod_headers</code> via <code>Header set</code> or <code>Header always set</code> in <code>.htaccess</code> or a <code>&lt;VirtualHost&gt;</code>. Without them, browsers fall back to permissive defaults and your site may fail an audit or corporate policy scan.</p><p>Order matters: enable the module, then add one block per directive family (HSTS with a sane max-age, a concrete CSP instead of wildcards, <code>X-Frame-Options</code> or frame ancestors in CSP). Test on staging because a typo can take down CSS or scripts.</p><p>Compare <a href="/fix/headers/nginx/">Nginx</a> and <a href="/fix/headers/vercel/">Vercel</a>. HeadersFixer reads your deployment and suggests the exact Apache lines.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/fix/headers/apache/",
        ),
        (
            "headers",
            "cloudflare",
            "Fix Missing Security Headers on Cloudflare — WebFix",
            "Use Transform Rules or managed snippets to inject HSTS, CSP, and X-Frame-Options at the edge.",
            '<p>Cloudflare terminates TLS for many sites, so it is the right place to enforce <code>Strict-Transport-Security</code> and a baseline <code>Content-Security-Policy</code> before traffic hits your origin. Transform Rules can set static response headers per hostname or path without origin changes.</p><p>Edge headers apply globally and propagate quickly, which also means mistakes affect every user—roll out in report-only CSP mode first when migrating policies. Pair with Page Rules or Cache Rules only where they do not strip security headers.</p><p>See also <a href="/providers/cloudflare/">Cloudflare provider hub</a>. HeadersFixer detects your current header gaps from a live fetch.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/fix/headers/cloudflare/",
        ),
        (
            "headers",
            "vercel",
            "Fix Missing Security Headers on Vercel — WebFix",
            "Define a vercel.json headers array to attach HSTS, CSP, X-Frame-Options, and Permissions-Policy to routes.",
            '<p>Vercel projects declare headers in <code>vercel.json</code> using a <code>headers</code> array with <code>source</code> glob patterns. This keeps policy in Git and redeploys with every merge, which is ideal for teams that want reviewable security changes.</p><p>Match the strictness of your CSP to frameworks you use: Next.js may need hashes or nonces for inline scripts if you move away from <code>unsafe-inline</code>. Start from HeadersFixer output and narrow <code>script-src</code> over time.</p><p>Related: <a href="/fix/cors/nextjs/">CORS on Next.js</a>, <a href="/fix/headers/netlify/">Netlify headers</a>.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/fix/headers/vercel/",
        ),
        (
            "headers",
            "netlify",
            "Fix Missing Security Headers on Netlify — WebFix",
            "Use a root _headers file or netlify.toml to attach HSTS, XContent-Type-Options, and CSP.",
            '<p>Netlify serves static headers from a top-level <code>_headers</code> file or from TOML configuration. Paths are prefix-based; put global rules first, then route-specific overrides for admin or preview deploys.</p><p>Because Netlify sits in front of your build output, headers are consistent across CDN PoPs—similar to Cloudflare but tied to deploy artifacts. Validate with curl against your production URL after each deploy.</p><p>HeadersFixer maps missing directives to Netlify syntax so you do not memorize path glob rules.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/fix/headers/netlify/",
        ),
        (
            "headers",
            "express",
            "Fix Missing Security Headers on Express — WebFix",
            "Use helmet middleware to set HSTS, CSP, X-Frame-Options, and related headers with sensible defaults.",
            '<p>Express serves API and SSR apps without security headers until you add them. The <code>helmet</code> package centralizes modern defaults and lets you override each middleware for CSP, HSTS length, and cross-origin policies.</p><p>Mount <code>helmet()</code> early in the chain so every route inherits the baseline; tighten <code>contentSecurityPolicy</code> directives when you drop inline scripts. For APIs, disable framing and lock down <code>crossOriginEmbedderPolicy</code> only if your clients require it.</p><p>For CORS plus headers, see <a href="/fix/cors/express/">CORS on Express</a>.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/fix/headers/express/",
        ),
        (
            "headers",
            "sharepoint",
            "Fix SharePoint CSP 'Refused to Load' — 2026 Enforcement — WebFix",
            "<span class='tag tag-error'>Urgent</span> SharePoint Online CSP allowlist steps for March–June 2026 enforcement.",
            '<p><span class="tag tag-error">Time-sensitive</span> Microsoft tightened Content Security Policy enforcement for SharePoint Online in 2026. Custom scripts, SPFx bundles, and third-party widgets that load from CDNs outside the tenant allowlist now show <strong>Refused to load the script</strong> or stylesheet errors in the browser console.</p><p>Open <strong>SharePoint Admin Center → Policies → Other features → Content Security Policy</strong>. Add each legitimate <code>script-src</code> and <code>style-src</code> origin your solutions require, save, and allow up to ~15 minutes for propagation. This is the durable fix—not a browser workaround.</p><p>Deep dive: <a href="/blog/sharepoint-csp-fix-2026/">SharePoint CSP blog</a> and <a href="/fix/csp/sharepoint/">CSP allowlist guide</a>. Use CSPFixer on a public mirror page if you need to enumerate blocked hosts.</p>',
            "/csp/",
            "Open CSPFixer →",
            "/fix/headers/sharepoint/",
        ),
        (
            "cors",
            "nginx",
            "Fix CORS Errors on Nginx — WebFix",
            "Add Access-Control-Allow-Origin and preflight handling with add_header in Nginx for APIs behind your server.",
            '<p>Browsers block cross-origin calls when your API omits <code>Access-Control-Allow-Origin</code> or mishandles <code>OPTIONS</code>. Nginx can terminate CORS at the edge with <code>add_header</code> and a dedicated <code>location</code> for <code>OPTIONS</code> returning 204.</p><p>Avoid echoing arbitrary <code>Origin</code> in production unless you validate against an allowlist; misconfigured reflection becomes an open proxy pattern. Pair with correct <code>Vary: Origin</code> when responses differ by caller.</p><p>CORSFixer sends a live preflight to your URL and labels the failure mode. See <a href="/error/cors-blocked/">CORS blocked</a>.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/fix/cors/nginx/",
        ),
        (
            "cors",
            "express",
            "Fix CORS Errors on Express — WebFix",
            "Use the cors middleware with explicit origin callbacks and credentials options for Express APIs.",
            '<p>The <code>cors</code> package wraps preflight and response headers for Express. Pass an <code>origin</code> function that whitelists dev and prod frontends instead of <code>*</code> when cookies or Authorization headers are involved.</p><p>Order middleware so <code>cors</code> runs before routes; log rejected origins during integration tests. Combine with <a href="/fix/headers/express/">Helmet</a> for a full browser-facing hardening stack.</p><p>Instrument with CORSFixer to confirm <code>OPTIONS</code> returns the status and headers your SPA expects.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/fix/cors/express/",
        ),
        (
            "cors",
            "fastapi",
            "Fix CORS Errors on FastAPI — WebFix",
            "Enable Starlette CORSMiddleware with allow_origins and expose_headers; note for vLLM and OpenAI-compatible proxies.",
            '<p>FastAPI applications add <code>CORSMiddleware</code> with explicit <code>allow_origins</code>—wildcards and credentials do not mix per the Fetch spec. Mount the middleware first so every route, including OpenAPI and health checks, gets consistent headers.</p><p>AI gateways such as vLLM or Ollama HTTP frontends often omit CORS; put Nginx or FastAPI in front to add preflight support for browser-based chat UIs. Lock origins to your admin UI hostname.</p><p><a href="/providers/fastapi/">FastAPI provider hub</a> lists related fixes.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/fix/cors/fastapi/",
        ),
        (
            "cors",
            "django",
            "Fix CORS Errors on Django — WebFix",
            "Install django-cors-headers, add to INSTALLED_APPS and MIDDLEWARE, set CORS_ALLOWED_ORIGINS.",
            '<p><code>django-cors-headers</code> injects CORS response headers and answers <code>OPTIONS</code> for Django REST Framework and vanilla views. Set <code>CORS_ALLOWED_ORIGINS</code> explicitly in settings instead of turning on <code>CORS_ALLOW_ALL_ORIGINS</code> in production.</p><p>Place the middleware high enough that authentication middleware can still run on API routes without breaking preflight. Use environment variables per stage so staging and production origins stay separate.</p><p>Cross-check with CORSFixer after deploy.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/fix/cors/django/",
        ),
        (
            "cors",
            "nextjs",
            "Fix CORS Errors on Next.js — WebFix",
            "Use next.config.js headers async redirects for API routes or edge middleware for selective Access-Control headers.",
            '<p>Next.js API routes and Route Handlers need explicit CORS when a SPA on another origin calls them. Use <code>headers()</code> in <code>next.config.js</code> or return CORS headers inside handlers for dynamic <code>Origin</code> checks.</p><p>App Router edge functions can short-circuit <code>OPTIONS</code> with 204. Keep credentials flows strict: reflected origins must be validated.</p><p>Headers for static assets live in the same config—see <a href="/fix/headers/vercel/">Vercel headers</a>.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/fix/cors/nextjs/",
        ),
        (
            "cors",
            "flask",
            "Fix CORS Errors on Flask — WebFix",
            "Use flask-cors with resources dict and supports_credentials for session cookies.",
            '<p><code>Flask-Cors</code> decorates apps or blueprints with per-resource rules. Prefer <code>resources={r\"/api/*\": {\"origins\": [...]}}</code> over blanket open CORS so admin namespaces stay locked down.</p><p>When <code>supports_credentials</code> is true, never use <code>*</code> for <code>origins</code>. Flask sessions and JWT in cookies require exact origin reflection you control.</p><p>CORSFixer validates preflight against your live endpoint.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/fix/cors/flask/",
        ),
        (
            "csp",
            "nginx",
            "Fix Content Security Policy on Nginx — WebFix",
            "Serve Content-Security-Policy via add_header in Nginx; align script-src and style-src with your real assets.",
            '<p>CSP belongs in HTTP headers, typically via <code>add_header Content-Security-Policy &quot;...&quot; always;</code> in Nginx. Start from report-only mode if you inherit a large legacy app, then tighten <code>script-src</code> once violations stop.</p><p>Inline bootstrap snippets need nonces or hashes—generate them in your template layer, not by permanently allowing <code>unsafe-inline</code>. Frame your API subdomains separately if they ship different asset tiers.</p><p>CSPFixer fetches HTML, lists origins, and proposes a policy that covers them.</p>',
            "/csp/",
            "Open CSPFixer →",
            "/fix/csp/nginx/",
        ),
        (
            "csp",
            "cloudflare",
            "Fix Content Security Policy on Cloudflare — WebFix",
            "Use Transform Rules or Workers to attach CSP and Reporting-Endpoints at the edge.",
            '<p>Cloudflare can inject or mutate <code>Content-Security-Policy</code> for all origins behind the zone. That centralizes policy when multiple microservices sit upstream and avoids configuring each Kubernetes ingress separately.</p><p>Reporting endpoints for <code>report-to</code> or legacy <code>report-uri</code> should hit infrastructure you operate; Cloudflare Logs can complement violation streams. Watch header size limits on very long allowlists.</p><p>Pair with <a href="/fix/cache/cloudflare/">cache tuning</a> so CSP headers are not stripped at the CDN.</p>',
            "/csp/",
            "Open CSPFixer →",
            "/fix/csp/cloudflare/",
        ),
        (
            "csp",
            "vercel",
            "Fix Content Security Policy on Vercel — WebFix",
            "Attach CSP through vercel.json headers; use nonces with Next.js when eliminating unsafe-inline.",
            '<p>Vercel deployments benefit from versioned CSP in <code>vercel.json</code>, often scoped with <code>source</code> globs. Frameworks like Next.js 13+ support nonced scripts—wire nonce generation through middleware and match <code>script-src &#39;nonce-...&#39;</code>.</p><p>Preview deployments may need relaxed <code>frame-ancestors</code> for design tools; isolate them on unique hostnames. CSPFixer still works against preview URLs if they are publicly reachable.</p>',
            "/csp/",
            "Open CSPFixer →",
            "/fix/csp/vercel/",
        ),
        (
            "csp",
            "sharepoint",
            "Fix SharePoint Content Security Policy — 2026 — WebFix",
            "<span class='tag tag-error'>URGENT</span> Tenant CSP allowlist for SharePoint Online script-src and style-src.",
            '<p><span class="tag tag-error">URGENT</span> SharePoint enforces CSP against third-party CDNs and inline dependencies that are not tenant-approved. Add each required host under Admin Center CSP settings; SPFx packages that pull widgets remotely must either bundle locally or update manifest permissions.</p><p>Failure looks like console violations naming <code>script-src</code> or <code>style-src</code>. Document every external dependency during PR review so the allowlist stays intentional.</p><p>Read <a href="/fix/headers/sharepoint/">headers overview</a>, <a href="/error/csp-refused-to-load/">refused to load</a>, and <a href="/blog/sharepoint-csp-fix-2026/">blog</a>.</p>',
            "/csp/",
            "Open CSPFixer →",
            "/fix/csp/sharepoint/",
        ),
        (
            "oauth",
            "auth0",
            "Fix OAuth Errors on Auth0 — PKCE, redirect_uri, invalid_grant — WebFix",
            "Resolve Auth0 invalid_grant, redirect mismatches, and PKCE code verifier issues with dashboard checks.",
            '<p>Auth0 tenants reject tokens when <code>redirect_uri</code> does not exactly match an Allowed Callback URL—including trailing slashes and custom schemes. PKCE public clients must send <code>code_verifier</code> that matches the original challenge; rotation errors surface as <code>invalid_grant</code>.</p><p>Use Auth0’s debugger and OAuthFixer’s provider hints to compare authorization requests with Application settings. Enable refresh token rotation only when your server stores refresh tokens securely.</p><p>Also see <a href="/error/invalid-grant/">invalid_grant</a> and <a href="/error/pkce-required/">PKCE required</a>.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/fix/oauth/auth0/",
        ),
        (
            "oauth",
            "okta",
            "Fix OAuth Errors on Okta — WebFix",
            "Align Okta app sign-on policies, redirect URIs, and PKCE settings with your SPA or native client.",
            '<p>Okta authorization servers scope claims and audiences separately from Auth Server defaults. Mismatched <code>aud</code> or <code>issuer</code> URLs cause obscure failures after the code exchange. Ensure the app integration lists every environment-specific redirect URI.</p><p>Org policies may require MFA or device trust before tokens issue—surface those errors distinctly from pure OAuth misconfig. OAuthFixer walks through common Okta error strings.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/fix/oauth/okta/",
        ),
        (
            "oauth",
            "cognito",
            "Fix OAuth Errors on AWS Cognito — WebFix",
            "Fix Cognito hosted UI and app client callback URLs, PKCE, and token scope mismatches.",
            '<p>Cognito app clients differ for public SPAs vs confidential backends. Public clients must use PKCE; confidential clients need a secret that never ships to browsers. Hosted UI return URLs must match the domain allowlist character-for-character.</p><p>Custom domains add another TLS and redirect layer—verify both the user pool domain and the custom domain settings. OAuthFixer helps decode <code>invalid_grant</code> coming from Cognito’s token endpoint.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/fix/oauth/cognito/",
        ),
        (
            "oauth",
            "google",
            "Fix OAuth Errors on Google — WebFix",
            "Configure Google Cloud OAuth consent screen, authorized redirect URIs, and PKCE for mobile or SPA clients.",
            '<p>Google Cloud marks clients as Web, iOS, or Android; each type restricts which redirect patterns are legal. Publishing status affects which Google accounts may sign in during testing.</p><p>Dynamic redirect ports on localhost must be pre-registered or use a loopback-friendly flow. OAuthFixer relates error payloads to the Console fields you need to edit.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/fix/oauth/google/",
        ),
        (
            "cache",
            "nginx",
            "Fix Cache-Control Headers on Nginx — WebFix",
            "Use expires, add_header Cache-Control, and proxy_cache_bypass rules so HTML stays fresh while static assets cache long.",
            '<p>Nginx often ships static files with short or missing <code>Cache-Control</code>, causing repeat downloads or the opposite problem—immutable JS cached forever without hashed filenames. Set long TTLs only for fingerprinted assets; keep HTML at <code>no-cache</code> or short revalidate where auth might vary.</p><p>Reverse proxies must forward or strip <code>Set-Cookie</code> carefully: caching private responses is a security issue EdgeFix flags. Align <code>Vary</code> with compression and content negotiation.</p>',
            "/edge/",
            "Open EdgeFix →",
            "/fix/cache/nginx/",
        ),
        (
            "cache",
            "cloudflare",
            "Fix Cache-Control Headers on Cloudflare — WebFix",
            "Tune Cache Rules, edge TTL, and origin cache-control respect for HTML vs assets.",
            '<p>Cloudflare can override origin directives or honor them depending on Cache Rules and Business logic features. Misaligned TTL on authenticated pages leaks cached HTML containing PII—tighten <code>Cache-Control: private</code> upstream and bypass cache on cookie presence.</p><p>Use tiered rules: aggressive cache for <code>/static/*</code>, bypass for <code>/api/*</code>. EdgeFix reads response headers your users actually see.</p>',
            "/edge/",
            "Open EdgeFix →",
            "/fix/cache/cloudflare/",
        ),
        (
            "cache",
            "vercel",
            "Fix Cache-Control Headers on Vercel — WebFix",
            "Use vercel.json and framework headers to mark ISR, static immutable assets, and dynamic API routes.",
            '<p>Vercel’s CDN respects framework signals: Next.js route segment config and <code>fetch</code> cache options influence <code>s-maxage</code>. APIs default to dynamic—opt into edge caching only when responses are anonymous.</p><p>Set <code>stale-while-revalidate</code> thoughtfully for marketing pages; never for per-user JSON. Pair with <a href="/fix/pagespeed/vercel/">PageSpeed on Vercel</a>.</p>',
            "/edge/",
            "Open EdgeFix →",
            "/fix/cache/vercel/",
        ),
        (
            "pagespeed",
            "nginx",
            "Fix PageSpeed Score on Nginx — WebFix",
            "Enable gzip/brotli, HTTP/2, long-cache static assets, and tuned buffer settings for Core Web Vitals.",
            '<p>PageSpeed penalizes large uncompressed text, short cache lifetimes on static files, and slow server response. Nginx can enable <code>gzip</code> or a brotli module, HTTP/2, and sendfile tuning without changing application code.</p><p>Preconnect and preload hints sometimes belong in upstream HTML, but Nginx can inject <code>Link</code> headers for critical LCP resources. Measure after each change—some optimizations trade CPU for bytes.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/fix/pagespeed/nginx/",
        ),
        (
            "pagespeed",
            "cloudflare",
            "Fix PageSpeed Score on Cloudflare — WebFix",
            "Use Polish, Mirage, HTTP/3, and cache rules to improve LCP and TBT without origin refactors.",
            '<p>Cloudflare’s image optimization and minification features reduce transfer sizes when your origin cannot. Rocket Loader and Auto Minify help legacy JS but test for breakage; prefer build-time bundling when possible.</p><p>Argo, Tiered Cache, and early hints improve perceived performance on high-latency routes. SpeedFixer pulls PSI audits tied to your stack for targeted fixes.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/fix/pagespeed/cloudflare/",
        ),
        (
            "pagespeed",
            "vercel",
            "Fix PageSpeed Score on Vercel — WebFix",
            "Leverage next/image, edge functions, and Vercel Analytics to address CLS, LCP, and bundle size.",
            '<p>Vercel optimizes images and splits deployments geographically by default, but client-side JavaScript bloat still hurts TBT. Adopt dynamic imports, review third-party tags, and ensure fonts use <code>display=swap</code> or self-host.</p><p>Compare field vs lab data: SpeedFixer surfaces PageSpeed’s view of your canonical URL after CDN behavior.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/fix/pagespeed/vercel/",
        ),
        (
            "pagespeed",
            "wordpress",
            "Fix PageSpeed Score on WordPress — WebFix",
            "Combine caching plugins, theme audits, and image lazy-loading to clear PSI opportunities on shared hosting.",
            '<p>WordPress stacks often accumulate render-blocking plugins and oversized hero images. Use a reputable performance plugin to minify and defer CSS/JS, convert images to WebP/AVIF, and page-cache HTML at the edge or reverse proxy.</p><p>Choose themes that avoid massive builder bundles on above-the-fold content. SpeedFixer maps failing audits to Nginx, Cloudflare, or WP-specific remediations.</p><p><a href="/providers/wordpress/">WordPress provider hub</a>.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/fix/pagespeed/wordpress/",
        ),
    ]

    for cat, slug, title, description, content, tool_url, cta, canonical in FIX:
        dirs_set.add(f"fix/{cat}")
        headline = title.replace(" — WebFix", "")
        graph = [
            tech_article(headline, canonical, description),
        ]
        graph.extend(
            breadcrumb_items_to_graph(
                [
                    ("WebFix", "/"),
                    ("Fix guides", "/fix/"),
                    (cat.capitalize(), f"/fix/{cat}/"),
                    (slug.replace("-", " ").title(), ""),
                ]
            )
        )
        p = write_page(
            "fix/" + cat,
            slug,
            title=title,
            description=description.replace("<span class='tag tag-error'>Urgent</span> ", "")
            .replace("<span class='tag tag-error'>URGENT</span> ", "")
            .strip(),
            canonical=canonical.rstrip("/") + "/",
            nav_section="Fix",
            breadcrumb=bc_html(
                [
                    ("WebFix", "/"),
                    ("Fix", "/fix/"),
                    (cat.capitalize(), f"/fix/{cat}/"),
                    (headline, None),
                ]
            ),
            h1=headline,
            content=content,
            tool_url=tool_url,
            tool_cta_text=cta,
            schema_graph=graph,
            related=seo_related_fix(cat, slug),
        )
        created.append(p)

    # fix category index pages (headers, cors, csp, oauth, cache, pagespeed)
    for cat in ["headers", "cors", "csp", "oauth", "cache", "pagespeed"]:
        sub = [canonical for _, s, _, _, _, _, _, canonical in FIX if _ == cat]
        links_html = "<ul class='index-list'>"
        for _, s, title, *_ in [f for f in FIX if f[0] == cat]:
            href = f"/fix/{cat}/{s}/"
            links_html += f"<li><a href='{href}'>{title.replace(' — WebFix', '')}</a></li>"
        links_html += "</ul>"
        canonical = f"/fix/{cat}/"
        dirs_set.add(f"fix/{cat}")
        name = f"{cat.capitalize()} fixes"
        graph = [
            collection_ld(name + " — WebFix", canonical + "/", f"Index of WebFix {cat} configuration guides."),
            *breadcrumb_items_to_graph([("WebFix", "/"), ("Fix", "/fix/"), (name, "")]),
        ]
        p = write_page(
            "fix",
            cat,
            title=f"{name} — WebFix",
            description=f"All WebFix guides for fixing {cat} issues across stacks.",
            canonical=canonical + "/",
            nav_section="Fix",
            breadcrumb=bc_html([("WebFix", "/"), ("Fix", "/fix/"), (name, None)]),
            h1=name,
            content=f"<p>Step-by-step fixes for {cat} on the stacks below. Each page links to the matching WebFix tool for live diagnostics.</p>{links_html}",
            tool_url={"headers": "/headers/", "cors": "/cors/", "csp": "/csp/", "oauth": "/oauth/", "cache": "/edge/", "pagespeed": "/speedfixer/"}[
                cat
            ],
            tool_cta_text={"headers": "Open HeadersFixer →", "cors": "Open CORSFixer →", "csp": "Open CSPFixer →", "oauth": "Open OAuthFixer →", "cache": "Open EdgeFix →", "pagespeed": "Open SpeedFixer →"}[
                cat
            ],
            schema_graph=graph,
            related=seo_related_fix(cat, "_"),
        )
        created.append(p)

    # ——— GROUP 2: ERROR PAGES ———
    ERR = [
        (
            "cors-blocked",
            "CORS Error: Access Blocked — WebFix",
            "Why browsers block cross-origin requests without proper Access-Control headers and how to fix them.",
            '<p>When a web page on <code>https://app.example</code> calls <code>https://api.example</code>, the browser enforces CORS. If the API omits <code>Access-Control-Allow-Origin</code> or blocks the preflight <code>OPTIONS</code> request, DevTools shows a network error that sounds like a failure to fetch even though the server returned 200.</p><p>Fixes belong on the API: return explicit allowed origins, forward methods and headers your client sends, and use <code>Vary: Origin</code> when appropriate. The SPA cannot "disable CORS"—only the server or a deliberate proxy can.</p><p>Read <a href="/fix/cors/nginx/">Nginx CORS</a> or <a href="/fix/cors/express/">Express CORS</a> after CORSFixer identifies your failure mode.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/error/cors-blocked/",
        ),
        (
            "csp-refused-to-load",
            "CSP: Refused to Load Script — WebFix",
            "Content Security Policy blocked a script or stylesheet; urgent SharePoint 2026 enforcement context.",
            '<p>The console error <em>Refused to load the script</em> means the response’s <code>Content-Security-Policy</code> (or meta tag) does not include the script’s origin in <code>script-src</code> (or a fallback). Styles hit the same check under <code>style-src</code>.</p><p><span class="tag tag-error">SharePoint</span> tenants may see a surge of these errors after Microsoft CSP enforcement in 2026—use the admin allowlist rather than weakening global browser policy. For static sites, tighten incrementally using CSPFixer-generated policies.</p><p>Guides: <a href="/fix/csp/sharepoint/">SharePoint CSP fix</a>, <a href="/blog/sharepoint-csp-fix-2026/">blog</a>.</p>',
            "/csp/",
            "Open CSPFixer →",
            "/error/csp-refused-to-load/",
        ),
        (
            "hsts-missing",
            "HSTS Header Missing — WebFix",
            "Why Strict-Transport-Security matters and how to add it without breaking local development.",
            '<p>HSTS tells browsers to use HTTPS-only for your host and optionally include subdomains. Without it, users can be downgraded to HTTP on first visit or evil twin networks. Security scanners flag missing HSTS as high severity.</p><p>Start with a modest <code>max-age</code>, preload only when every subdomain serves TLS correctly, and use a staging hostname to test before prod. HeadersFixer shows whether your live site already emits HSTS and the exact snippet for your stack.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/error/hsts-missing/",
        ),
        (
            "mixed-content",
            "Mixed Content Error — WebFix",
            "HTTPS pages loading HTTP subresources are blocked; fix by upgrading URLs and redirects.",
            '<p>Mixed content errors occur when an HTML page loads over HTTPS but pulls scripts, iframes, or images over plaintext HTTP. Modern browsers block active mixed content and may warn on passive assets.</p><p>Remediation: use relative URLs, scheme-relative upgrades to <code>https://</code>, or Content Security Policy <code>upgrade-insecure-requests</code> after verifying every dependency supports TLS. HeadersFixer pairs with CSPFixer to validate production HTML.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/error/mixed-content/",
        ),
        (
            "invalid-grant",
            "OAuth Error: invalid_grant — WebFix",
            "Token endpoint rejected the authorization code or refresh token—common causes and fixes.",
            '<p><code>invalid_grant</code> usually means the authorization code expired, was reused, lacks the matching PKCE verifier, or the refresh token was revoked or rotated. Clock skew between servers can also invalidate <code>exp</code> assertions.</p><p>Trace the full authorization code flow in network tabs: confirm one code exchange, matching redirect URI, and client authentication method expected by the provider. OAuthFixer summarizes provider-specific checklists.</p><p><a href="/fix/oauth/auth0/">Auth0</a>, <a href="/fix/oauth/cognito/">Cognito</a>.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/error/invalid-grant/",
        ),
        (
            "redirect-uri-mismatch",
            "OAuth Error: redirect_uri_mismatch — WebFix",
            "The authorization server rejected redirect_uri because it is not registered for this client.",
            '<p>OAuth clients must register every redirect URI exactly—including scheme, host, port, path, and trailing slash. SPA libraries that default to <code>http://localhost:3000/</code> will fail if the console only lists <code>http://localhost:3000/callback</code>.</p><p>Update the provider dashboard, redeploy, and clear stale state parameters. Mobile custom URL schemes need their own registered entries. OAuthFixer maps errors to the fields you must edit.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/error/redirect-uri-mismatch/",
        ),
        (
            "pkce-required",
            "OAuth Error: PKCE Required — WebFix",
            "Public clients must send code_challenge and code_verifier; failures surface as invalid_grant or policy errors.",
            '<p>Proof Key for Code Exchange prevents authorization code interception on mobile and SPA clients. If your library omits <code>code_challenge_method=S256</code> or drops the verifier on token exchange, the provider rejects the flow.</p><p>Ensure your OAuth library stores verifier in session storage or secure memory until the callback completes. Confidential server apps may opt out depending on provider policy—never ship client secrets to browsers.</p><p><a href="/fix/oauth/okta/">Okta PKCE</a>.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/error/pkce-required/",
        ),
        (
            "cache-authenticated-response",
            "Security: Authenticated Response Cached — WebFix",
            "CDN or browser cached HTML or JSON that varies by cookie or Authorization—fix with private Cache-Control.",
            '<p>When <code>Cache-Control</code> allows shared caching of responses that include user-specific data, another visitor might receive someone else’s payload from an edge POP. This is both a privacy incident and a compliance failure.</p><p>Mark dynamic responses <code>private, no-store</code> or bypass cache when <code>Authorization</code> or session cookies appear. Validate with EdgeFix on logged-in and logged-out sessions.</p><p><a href="/fix/cache/cloudflare/">Cloudflare cache</a>, <a href="/fix/cache/nginx/">Nginx cache</a>.</p>',
            "/edge/",
            "Open EdgeFix →",
            "/error/cache-authenticated-response/",
        ),
        (
            "x-frame-options-missing",
            "X-Frame-Options Missing — WebFix",
            "Clickjacking risk when your site can be embedded in arbitrary iframes; use X-Frame-Options or CSP frame-ancestors.",
            "<p>Without <code>X-Frame-Options: DENY</code> (or <code>SAMEORIGIN</code>) or a restrictive <code>frame-ancestors</code> directive, attackers can load your site in transparent iframes and trick users into clicking sensitive actions.</p><p>Modern apps prefer CSP <code>frame-ancestors 'none'</code> for finer control and consistency with other directives. HeadersFixer will show if neither header is present on your canonical URL.</p>",
            "/headers/",
            "Open HeadersFixer →",
            "/error/x-frame-options-missing/",
        ),
        (
            "pagespeed-render-blocking",
            "PageSpeed: Render-Blocking Resources — WebFix",
            "CSS and synchronous JS delay first paint; defer, inline critical CSS, or split bundles.",
            '<p>Lighthouse flags scripts and stylesheets in the critical path that must download and execute before pixels hit the screen. Moving non-critical JavaScript to <code>defer</code> or module graphs, and trimming unused CSS, improves LCP and FCP.</p><p>Server-side, enable compression and HTTP/2 multiplexing so blocking resources at least transfer quickly. SpeedFixer ties each failing audit to stack snippets.</p><p><a href="/fix/pagespeed/nginx/">Nginx PageSpeed</a>.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/error/pagespeed-render-blocking/",
        ),
        (
            "pagespeed-cache-policy",
            "PageSpeed: Inefficient Cache Policy — WebFix",
            "Short TTLs on static assets waste bandwidth; align cache lifetimes with content hashing.",
            '<p>PSI deducts score when fonts, scripts, or images ship with <code>max-age</code> under recommended thresholds. Immutable build artifacts should carry long TTLs and <code>immutable</code> while HTML stays short-lived.</p><p>CDNs must not strip upstream directives unintentionally. EdgeFix plus SpeedFixer confirm real headers in production.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/error/pagespeed-cache-policy/",
        ),
        (
            "pagespeed-no-compression",
            "PageSpeed: Enable Text Compression — WebFix",
            "gzip or Brotli reduces text payload size; enable on origin or CDN.",
            '<p>Uncompressed HTML, CSS, and JS inflate transfer times especially on mobile networks. Nginx, Cloudflare, Vercel, and most PaaS layers can negotiate <code>gzip</code> or <code>br</code> based on <code>Accept-Encoding</code>.</p><p>Verify responses with <code>curl -H &quot;Accept-Encoding: gzip&quot; -I</code>. SpeedFixer surfaces this audit when PSI detects waste.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/error/pagespeed-no-compression/",
        ),
    ]

    for slug, title, description, content, tool_url, cta, canonical in ERR:
        dirs_set.add("error")
        headline = title.replace(" — WebFix", "")
        graph = [tech_article(headline, canonical, description)]
        graph.extend(
            breadcrumb_items_to_graph(
                [("WebFix", "/"), ("Errors", "/error/"), (headline, "")]
            )
        )
        p = write_page(
            "error",
            slug,
            title=title,
            description=description,
            canonical=canonical.rstrip("/") + "/",
            nav_section="Errors",
            breadcrumb=bc_html([("WebFix", "/"), ("Errors", "/error/"), (headline, None)]),
            h1=headline,
            content=content,
            tool_url=tool_url,
            tool_cta_text=cta,
            schema_graph=graph,
            related=seo_related_error(slug),
        )
        created.append(p)

    # ——— GROUP 3: PROVIDERS ———
    PROV = [
        (
            "nginx",
            "Nginx Security & Performance Fixes — WebFix",
            "Headers, CORS, CSP, caching, and PageSpeed-related configuration for Nginx.",
            '<p>Nginx fronts a huge share of APIs and static sites. WebFix targets Nginx for <strong>security headers</strong> (<a href="/fix/headers/nginx/">guide</a>), <strong>CORS</strong> (<a href="/fix/cors/nginx/">guide</a>), <strong>CSP</strong> (<a href="/fix/csp/nginx/">guide</a>), <strong>cache headers</strong> (<a href="/fix/cache/nginx/">guide</a>), and <strong>PageSpeed-oriented tuning</strong> (<a href="/fix/pagespeed/nginx/">guide</a>).</p><p>Use HeadersFixer and CORSFixer against public URLs to capture real header and preflight behavior before editing <code>nginx.conf</code>. EdgeFix validates <code>Cache-Control</code> after changes; SpeedFixer maps Core Web Vitals gaps to concrete directives.</p><p>Related errors: <a href="/error/cors-blocked/">CORS blocked</a>, <a href="/error/cache-authenticated-response/">cached auth responses</a>.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/providers/nginx/",
        ),
        (
            "apache",
            "Apache Security & Performance Fixes — WebFix",
            "httpd modules for headers, compression, and CSP on Apache.",
            '<p>Apache deployments rely on <code>mod_headers</code>, <code>mod_rewrite</code>, and sometimes <code>mod_security</code>. WebFix documents <a href="/fix/headers/apache/">security headers</a> and connects to CORS patterns when you proxy to a backend.</p><p>Because .htaccess and VirtualHost differ per host, live scans prevent guessing which directives apply. SpeedFixer still helps when Apache serves static build output behind TLS termination.</p><p>Compare <a href="/providers/nginx/">Nginx hub</a> for the same categories.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/providers/apache/",
        ),
        (
            "cloudflare",
            "Cloudflare Security & Performance Fixes — WebFix",
            "Edge headers, caching, image polish, CSP, and CORS at Cloudflare.",
            '<p>Cloudflare users should configure <a href="/fix/headers/cloudflare/">security headers</a>, <a href="/fix/csp/cloudflare/">CSP injection</a>, <a href="/fix/cache/cloudflare/">cache rules</a>, and <a href="/fix/pagespeed/cloudflare/">PageSpeed features</a> in the dashboard or Wrangler-managed rules.</p><p>CORS may be handled via Workers if your origin cannot change. EdgeFix ensures authenticated HTML is not cached at the edge; CSPFixer enumerates origins your Workers must permit.</p>',
            "/csp/",
            "Open CSPFixer →",
            "/providers/cloudflare/",
        ),
        (
            "vercel",
            "Vercel Security & Performance Fixes — WebFix",
            "vercel.json headers, Next.js CORS, CSP, and caching conventions.",
            '<p>Vercel’s platform pairs with <a href="/fix/headers/vercel/">headers in vercel.json</a>, <a href="/fix/cors/nextjs/">Next.js CORS</a>, <a href="/fix/csp/vercel/">CSP</a>, <a href="/fix/cache/vercel/">cache headers</a>, and <a href="/fix/pagespeed/vercel/">PageSpeed</a> optimizations.</p><p>Each guide links to the tool that validates your production deployment. OAuth SPAs on Vercel should double-check <a href="/error/redirect-uri-mismatch/">redirect URI</a> settings with providers.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/providers/vercel/",
        ),
        (
            "netlify",
            "Netlify Security & Performance Fixes — WebFix",
            "_headers, build plugins, and CDN behavior for Netlify sites.",
            '<p>Netlify excels at atomic deploys; configure <a href="/fix/headers/netlify/">security headers via _headers</a> and align <a href="/error/pagespeed-cache-policy/">cache policy</a> with long-lived asset folders.</p><p>CORS for serverless functions may require <code>netlify.toml</code> headers blocks per path. CSPFixer still applies when your HTML is statically generated.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/providers/netlify/",
        ),
        (
            "express",
            "Express.js Security Fixes — WebFix",
            "Helmet, CORS middleware, and session-safe defaults for Node Express.",
            '<p>Express apps combine <a href="/fix/headers/express/">Helmet headers</a> and <a href="/fix/cors/express/">cors()</a> middleware. OAuth backends built on Express should validate <a href="/error/invalid-grant/">invalid_grant</a> scenarios with structured logging.</p><p>When Express sits behind Nginx, configure headers at one layer to avoid duplicates—HeadersFixer shows effective client-visible values.</p>',
            "/headers/",
            "Open HeadersFixer →",
            "/providers/express/",
        ),
        (
            "nextjs",
            "Next.js Security Fixes — WebFix",
            "CORS on Route Handlers, CSP nonces, Vercel deployment headers.",
            '<p>Next.js projects cross-cut <a href="/fix/cors/nextjs/">CORS</a>, <a href="/fix/headers/vercel/">Vercel headers</a>, and framework-specific CSP with nonces. Speed and security both benefit from disciplined third-party script loading.</p><p>Use SpeedFixer on your production URL after enabling image optimization.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/providers/nextjs/",
        ),
        (
            "django",
            "Django Security Fixes — WebFix",
            "django-cors-headers, security middleware, and reverse-proxy headers.",
            '<p>Django stacks commonly need <a href="/fix/cors/django/">django-cors-headers</a> for SPAs and hardened <code>SECURE_*</code> settings behind TLS proxies. HeadersFixer helps verify what users see after <code>X-Forwarded-Proto</code> rewriting.</p><p>Review <a href="/error/cors-blocked/">CORS errors</a> when CSRF and CORS interact on cookie sessions.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/providers/django/",
        ),
        (
            "fastapi",
            "FastAPI Security Fixes — WebFix",
            "CORSMiddleware, dependency injection for auth, and proxy headers.",
            '<p>FastAPI’s async stack uses <a href="/fix/cors/fastapi/">CORSMiddleware</a> for browser clients; LLM gateways often need the same for admin UIs calling vLLM. Headers may be terminated at Nginx—see <a href="/providers/nginx/">Nginx hub</a>.</p><p>OAuth resource servers should validate issuer and audience aggressively.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/providers/fastapi/",
        ),
        (
            "flask",
            "Flask Security Fixes — WebFix",
            "flask-cors, secure cookies, and reverse proxy setup.",
            '<p>Flask APIs use <a href="/fix/cors/flask/">Flask-Cors</a> with blueprint-scoped rules. Combine with TLS and HSTS at the proxy—HeadersFixer audits the public URL.</p>',
            "/cors/",
            "Open CORSFixer →",
            "/providers/flask/",
        ),
        (
            "wordpress",
            "WordPress Security & Performance Fixes — WebFix",
            "Plugins for headers, caching, WebP, and PageSpeed on WordPress.",
            '<p>WordPress benefits from <a href="/fix/pagespeed/wordpress/">PageSpeed-oriented plugins</a>, server-level headers where you control Apache or Nginx, and CSP allowlists when using inline content builders.</p><p>SharePoint-style CSP enforcement is less common but enterprise WP networks still need strict <a href="/csp/">CSP tooling</a> for multisite.</p>',
            "/speedfixer/",
            "Open SpeedFixer →",
            "/providers/wordpress/",
        ),
        (
            "auth0",
            "Auth0 OAuth Fixes — WebFix",
            "redirect URI, PKCE, refresh rotation, and application type settings for Auth0.",
            '<p>Auth0-specific guidance lives in <a href="/fix/oauth/auth0/">Auth0 fix</a> plus generic <a href="/error/invalid-grant/">invalid_grant</a>, <a href="/error/redirect-uri-mismatch/">redirect_uri_mismatch</a>, and <a href="/error/pkce-required/">PKCE</a> pages. OAuthFixer encodes the checks teams repeat during incidents.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/providers/auth0/",
        ),
        (
            "okta",
            "Okta OAuth Fixes — WebFix",
            "Authorization servers, app integrations, and PKCE for Okta.",
            '<p>See <a href="/fix/oauth/okta/">Okta fix</a> and cross-reference OAuth error manifests when upgrading Okta Identity Engine policies.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/providers/okta/",
        ),
        (
            "cognito",
            "AWS Cognito OAuth Fixes — WebFix",
            "Hosted UI, app clients, and token endpoint quirks for Cognito.",
            '<p>Use <a href="/fix/oauth/cognito/">Cognito fix</a> alongside OAuthFixer when debugging mobile or SPA flows against user pools.</p>',
            "/oauth/",
            "Open OAuthFixer →",
            "/providers/cognito/",
        ),
    ]

    dirs_set.add("providers")
    for slug, title, description, content, tool_url, cta, canonical in PROV:
        headline = title.replace(" — WebFix", "")
        graph = [tech_article(headline, canonical, description)]
        graph.extend(
            breadcrumb_items_to_graph(
                [("WebFix", "/"), ("Providers", "/providers/"), (headline, "")]
            )
        )
        p = write_page(
            "providers",
            slug,
            title=title,
            description=description,
            canonical=canonical.rstrip("/") + "/",
            nav_section="Providers",
            breadcrumb=bc_html([("WebFix", "/"), ("Providers", "/providers/"), (headline, None)]),
            h1=headline,
            content=content,
            tool_url=tool_url,
            tool_cta_text=cta,
            schema_graph=graph,
            related=seo_related_provider(slug),
        )
        created.append(p)

    # ——— GROUP 4 & 5: INDEX + VS ———# fix master index
    fix_links = "".join(
        f"<li><a href='/fix/{cat}/'>{cat.capitalize()} fixes</a></li>" for cat in ["headers", "cors", "csp", "oauth", "cache", "pagespeed"]
    )
    graph = [
        collection_ld("WebFix fix guides", "/fix/", "All stack-specific fix guides for headers, CORS, CSP, OAuth, cache, and PageSpeed."),
        *breadcrumb_items_to_graph([("WebFix", "/"), ("Fix guides", "")]),
        ITEMLIST_FIX_INDEX,
    ]
    p = write_page(
        "fix",
        "index",
        title="Fix Guides — WebFix",
        description="Stack-specific fixes for security headers, CORS, CSP, OAuth, caching, and PageSpeed.",
        canonical="/fix/",
        nav_section="Fix",
        breadcrumb=bc_html([("WebFix", "/"), ("Fix guides", None)]),
        h1="Fix guides",
        content=f"<p>Browse fixes by category, then open the matching WebFix tool to validate your live deployment.</p><ul class='index-list'>{fix_links}</ul><p>Errors: <a href='/error/'>error hub</a>. Providers: <a href='/providers/'>provider hub</a>.</p>",
        tool_url="/headers/",
        tool_cta_text="Open HeadersFixer →",
        schema_graph=graph,
        flat=True,
        related=related_block([("Glossary", "/glossary/"), ("Errors", "/error/")]),
    )
    created.append(p)
    dirs_set.add("fix")

    err_links = "".join(
        f"<li><a href='{canonical}'>{title.replace(' — WebFix', '')}</a></li>" for _, title, _, _, _, _, canonical in ERR
    )
    graph = [
        collection_ld("WebFix error guides", "/error/", "Explain browser and OAuth errors with remediation paths."),
        *breadcrumb_items_to_graph([("WebFix", "/"), ("Errors", "")]),
        ITEMLIST_ERROR_INDEX,
    ]
    p = write_page(
        "error",
        "index",
        title="Error Guides — WebFix",
        description="CORS, CSP, OAuth, cache, and PageSpeed errors explained with fixes.",
        canonical="/error/",
        nav_section="Errors",
        breadcrumb=bc_html([("WebFix", "/"), ("Errors", None)]),
        h1="Error guides",
        content=f"<p>Each page describes the symptom, why it happens, and links to the WebFix tool that diagnoses it.</p><ul class='index-list'>{err_links}</ul>",
        tool_url="/cors/",
        tool_cta_text="Open CORSFixer →",
        schema_graph=graph,
        flat=True,
        related=related_block(
            [
                ("Fix CORS (Nginx)", "/fix/cors/nginx/"),
                ("CSP refused", "/error/csp-refused-to-load/"),
            ]
        ),
    )
    created.append(p)
    dirs_set.add("error")

    prov_links = "".join(
        f"<li><a href='{canonical}'>{title.replace(' — WebFix', '')}</a></li>" for _, title, _, _, _, _, canonical in PROV
    )
    graph = [
        collection_ld("WebFix provider hubs", "/providers/", "All tools mapped to hosting and framework stacks."),
        *breadcrumb_items_to_graph([("WebFix", "/"), ("Providers", "")]),
        ITEMLIST_PROVIDERS_INDEX,
    ]
    p = write_page(
        "providers",
        "index",
        title="Provider & Stack Hubs — WebFix",
        description="Nginx, Cloudflare, Vercel, frameworks, and identity providers on WebFix.",
        canonical="/providers/",
        nav_section="Providers",
        breadcrumb=bc_html([("WebFix", "/"), ("Providers", None)]),
        h1="Provider & stack hubs",
        content=f"<p>Jump to the stack you operate; each hub links the relevant fix articles and tools.</p><ul class='index-list'>{prov_links}</ul>",
        tool_url="/headers/",
        tool_cta_text="Open HeadersFixer →",
        schema_graph=graph,
        flat=True,
        related=related_block([("Nginx hub", "/providers/nginx/"), ("All fixes", "/fix/")]),
    )
    created.append(p)
    dirs_set.add("providers")

    graph = [
        collection_ld("WebFix glossary", "/glossary/", "Glossary entries coming soon."),
        *breadcrumb_items_to_graph([("WebFix", "/"), ("Glossary", "")]),
        ITEMLIST_GLOSSARY_INDEX,
    ]
    p = write_page(
        "glossary",
        "index",
        title="Glossary — WebFix",
        description="Security and performance glossary — entries coming soon.",
        canonical="/glossary/",
        nav_section="Glossary",
        breadcrumb=bc_html([("WebFix", "/"), ("Glossary", None)]),
        h1="Glossary",
        content="<p>Definitions for CSP, CORS, HSTS, PKCE, and related terms will appear here. For now, see <a href='/fix/'>fix guides</a> and <a href='/error/'>error guides</a>.</p>",
        tool_url="/csp/",
        tool_cta_text="Open CSPFixer →",
        schema_graph=graph,
        flat=True,
        related=related_block([("Full glossary", "/glossary/"), ("Fix guides", "/fix/")]),
    )
    created.append(p)
    dirs_set.add("glossary")

    graph = [
        collection_ld("WebFix comparisons", "/vs/", "Tool comparisons — more articles coming soon."),
        *breadcrumb_items_to_graph([("WebFix", "/"), ("Comparisons", "")]),
    ]
    p = write_page(
        "vs",
        "index",
        title="Comparisons — WebFix",
        description="WebFix vs other tools — articles coming soon.",
        canonical="/vs/",
        nav_section="Vs",
        breadcrumb=bc_html([("WebFix", "/"), ("Comparisons", None)]),
        h1="Comparisons",
        content="<p>WebFix vs other scanners and checkers. Read <a href='/vs/webfix-vs-securityheaders/'>WebFix vs securityheaders.com</a>. More matchups coming.</p>",
        tool_url="/headers/",
        tool_cta_text="Open HeadersFixer →",
        schema_graph=graph,
        flat=True,
        related=related_block(
            [
                ("VS article", "/vs/webfix-vs-securityheaders/"),
                ("Headers tool", "/headers/"),
            ]
        ),
    )
    created.append(p)
    dirs_set.add("vs")

    blog_posts = [
        ("SharePoint CSP \"Refused to Load\" Fix (2026)", "/blog/sharepoint-csp-fix-2026/"),
    ]
    blog_list = "".join(f"<li><a href='{u}'>{t}</a></li>" for t, u in blog_posts)
    graph = [
        collection_ld("WebFix blog", "/blog/", "Articles on CSP enforcement, headers, and performance."),
        *breadcrumb_items_to_graph([("WebFix", "/"), ("Blog", "")]),
    ]
    p = write_page(
        "blog",
        "index",
        title="Blog — WebFix",
        description="WebFix articles on SharePoint CSP, security headers, and web performance.",
        canonical="/blog/",
        nav_section="Blog",
        breadcrumb=bc_html([("WebFix", "/"), ("Blog", None)]),
        h1="Blog",
        content=f"<p>Long-form posts from MetricLogic. Fix guides live under <a href='/fix/'>/fix/</a>.</p><ul class='index-list'>{blog_list}</ul>",
        tool_url="/csp/",
        tool_cta_text="Open CSPFixer →",
        schema_graph=graph,
        flat=True,
        related=related_block(
            [
                ("SharePoint CSP post", "/blog/sharepoint-csp-fix-2026/"),
                ("Fix guides", "/fix/"),
            ]
        ),
    )
    created.append(p)
    dirs_set.add("blog")

    # VS page — Article schema
    vs_canonical = "/vs/webfix-vs-securityheaders/"
    vs_title = "WebFix vs securityheaders.com — Why Fixers Beat Checkers — WebFix"
    vs_desc = "securityheaders.com gives letter grades; WebFix generates copy-paste fixes for Nginx, Cloudflare, Vercel, and more."
    vs_content = (
        "<p>Security header scanners such as securityheaders.com attract massive traffic—on the order of <strong>251K monthly visits</strong>—because teams want a quick grade. The scan is valuable, but the output stops at diagnosis: you still translate red rows into nginx.conf, Cloudflare Transform Rules, or vercel.json on your own.</p>"
        "<h2>Comparison</h2>"
        "<div class='code-block'>"
        "| | securityheaders.com | WebFix |\n"
        "| --- | --- | --- |\n"
        "| Output | Letter grade + header checklist | Same audits + stack-specific snippets |\n"
        "| Config | None (manual research) | Copy-paste for Nginx, Apache, CF, Vercel, Express… |\n"
        "| Scope | Headers snapshot | Headers, CORS preflight, CSP resource graph, OAuth errors, cache audits, PSI |\n"
        "| Price | Free | Free (MIT) |\n"
        "</div>"
        "<p>WebFix fills the gap between <em>knowing</em> you are missing HSTS and <em>shipping</em> the exact directive. Run HeadersFixer on your canonical URL, then deploy the recommended block and re-scan.</p>"
        "<p>Related: <a href='/fix/headers/nginx/'>Fix headers on Nginx</a>, <a href='/providers/cloudflare/'>Cloudflare hub</a>, <a href='/headers/'>HeadersFixer tool</a>.</p>"
    )
    graph = [
        article_ld(
            "WebFix vs securityheaders.com — Why Fixers Beat Checkers",
            vs_canonical,
            vs_desc,
        ),
        *breadcrumb_items_to_graph(
            [("WebFix", "/"), ("Comparisons", "/vs/"), ("vs securityheaders.com", "")]
        ),
    ]
    p = write_page(
        "vs",
        "webfix-vs-securityheaders",
        title=vs_title,
        description=vs_desc,
        canonical=vs_canonical.rstrip("/") + "/",
        nav_section="Vs",
        breadcrumb=bc_html(
            [
                ("WebFix", "/"),
                ("Comparisons", "/vs/"),
                ("WebFix vs securityheaders.com", None),
            ]
        ),
        h1="WebFix vs securityheaders.com — Why Fixers Beat Checkers",
        content=vs_content,
        tool_url="/headers/",
        tool_cta_text="Try HeadersFixer →",
        schema_graph=graph,
        related=related_block(
            [
                ("Fix headers (Nginx)", "/fix/headers/nginx/"),
                ("Glossary", "/glossary/"),
                ("Comparisons hub", "/vs/"),
            ],
            include_vs=False,
        ),
    )
    created.append(p)
    dirs_set.add("vs")

    n = len(created)
    y = len(dirs_set)
    print(f"Generated {n} pages across {y} directories")
    for path in sorted(created):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
