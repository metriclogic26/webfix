#!/usr/bin/env python3
"""
HttpFixer — Blog Article Generator
Generates 61 blog articles across 10 batches.

Usage:
  cd ~/Projects/stackfix
  cp ~/Downloads/generate_blog_articles.py .
  python3 generate_blog_articles.py
  git add -A && git commit -m "feat: 61 blog articles — CORS, CSP, OAuth, Headers, Performance" && git push origin main && npx vercel --prod --force
"""

import os, json

BASE_URL = "https://httpfixer.dev"

# ─── HTML TEMPLATE ────────────────────────────────────────────────────────────

def template(title, description, canonical, schema, nav_label, breadcrumb, tag, tag_color, h1, content, cta_url, cta_text, related):
    schema_str = json.dumps(schema, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · HttpFixer</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="MetricLogic">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">{schema_str}</script>
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
    main{{max-width:760px;margin:0 auto;padding:2.5rem 1.5rem 4rem}}
    .breadcrumb{{font-size:12px;opacity:0.5;margin-bottom:1.5rem}}
    .breadcrumb a{{color:var(--purple);text-decoration:none}}
    .error-box{{background:#1a0a0a;border:1px solid var(--red);border-radius:6px;padding:1rem;margin:1.5rem 0;font-size:12px;color:#ff6b6b;font-family:"JetBrains Mono",monospace;line-height:1.6}}
    .error-label{{font-size:10px;text-transform:uppercase;opacity:0.6;margin-bottom:0.5rem;letter-spacing:0.05em}}
    .tag{{display:inline-block;padding:0.2rem 0.6rem;border-radius:4px;font-size:11px;font-weight:600;margin-bottom:1rem;background:{tag_color};}}
    h1{{font-size:1.6rem;font-weight:600;line-height:1.3;margin-bottom:1rem}}
    h2{{font-size:1.05rem;font-weight:600;margin:2rem 0 0.75rem}}
    h3{{font-size:0.95rem;font-weight:600;margin:1.5rem 0 0.5rem;opacity:0.85}}
    p{{margin-bottom:1rem;opacity:0.9;line-height:1.75}}
    .lead{{font-size:15px;opacity:0.95;margin-bottom:1.5rem;line-height:1.85}}
    pre{{background:#080a0f;border:1px solid var(--border);border-radius:6px;padding:1rem;font-size:12px;margin:1rem 0;overflow-x:auto;white-space:pre;line-height:1.6}}
    p code,li code{{background:rgba(108,99,255,0.15);color:var(--purple);padding:0.1rem 0.3rem;border-radius:3px;font-size:12px}}
    .tool-cta{{display:inline-block;margin:2rem 0 1rem;padding:0.75rem 1.5rem;background:var(--purple);color:white;text-decoration:none;border-radius:6px;font-weight:500;font-size:14px}}
    .tool-cta:hover{{filter:brightness(1.1)}}
    .related{{font-size:12px;opacity:0.6;margin:1.5rem 0;padding-top:1rem;border-top:1px solid var(--border)}}
    .related a{{color:var(--purple);text-decoration:none;margin-right:0.75rem}}
    table{{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:13px}}
    th,td{{padding:0.6rem 0.75rem;border:1px solid var(--border);text-align:left}}
    th{{background:var(--surface);color:var(--purple);font-weight:600}}
    tr:nth-child(even) td{{background:rgba(255,255,255,0.02)}}
    ul,ol{{margin:0.75rem 0 1rem 1.5rem;opacity:0.9}}
    li{{margin-bottom:0.4rem;line-height:1.7}}
    footer{{border-top:1px solid var(--border);padding:1.5rem 2rem;font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.5rem}}
    footer a{{color:var(--text);text-decoration:none;opacity:0.6}}
    .disclaimer{{width:100%;text-align:center;font-size:11px;opacity:0.4;margin-top:0.75rem;line-height:1.6}}
    @media(max-width:600px){{nav .right{{display:none}}footer{{flex-direction:column;text-align:center}}}}
  </style>
</head>
<body>
<nav>
  <a href="/" class="brand">HttpFixer <span>/</span> {nav_label}</a>
  <div class="right">
    <a href="/">Headers</a><a href="/cors/">CORS</a><a href="/oauth/">OAuth</a>
    <a href="/csp/">CSP</a><a href="/edge/">Edge</a><a href="/speedfixer/">Speed</a>
  </div>
</nav>
<main>
  <div class="breadcrumb">{breadcrumb}</div>
  <span class="tag">{tag}</span>
  <h1>{h1}</h1>
  {content}
  <a href="{cta_url}" class="tool-cta">{cta_text}</a>
  <div class="related">Related: {related}</div>
</main>
<footer>
  <span>HttpFixer by MetricLogic · <a href="https://configclarity.dev">configclarity.dev</a> · <a href="https://domainpreflight.dev">domainpreflight.dev</a> · <a href="https://packagefix.dev">packagefix.dev</a></span>
  <span><a href="https://github.com/metriclogic26/httpfixer">MIT · GitHub →</a> · <a href="https://github.com/metriclogic26/httpfixer/issues/new">Report issue →</a></span>
  <p class="disclaimer">Configurations are based on open standards (OWASP, RFC, MDN). Always test in a staging environment before deploying to production. HttpFixer provides these tools for informational purposes only and accepts no liability for misconfiguration, data loss, or security incidents. © 2026 MetricLogic.</p>
</footer>
</body>
</html>"""


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  ✓ {path}")


def make_schema(title, description, url, steps, faqs):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "headline": title,
                "description": description,
                "url": url,
                "datePublished": "2026-04-02",
                "author": {"@type": "Organization", "name": "MetricLogic"},
                "publisher": {"@type": "Organization", "name": "MetricLogic", "url": "https://metriclogic.dev"}
            },
            {
                "@type": "HowTo",
                "name": title,
                "step": [{"@type": "HowToStep", "position": i+1, "name": s[0], "text": s[1]} for i, s in enumerate(steps)]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "HttpFixer", "item": "https://httpfixer.dev"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://httpfixer.dev/blog/"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": url}
                ]
            }
        ]
    }


PURPLE_TAG = "rgba(108,99,255,0.2);color:var(--purple)"
GREEN_TAG = "rgba(34,197,94,0.2);color:var(--green)"
ORANGE_TAG = "rgba(249,115,22,0.2);color:var(--orange)"
RED_TAG = "rgba(239,68,68,0.2);color:var(--red)"

# ─── BATCH 1: CORS FIX GUIDES ─────────────────────────────────────────────────

def batch1_cors():
    print("\n📦 Batch 1 — CORS Fix Guides")

    # 1. Express
    write("blog/cors/fix-cors-express/index.html", template(
        title="Fix CORS Error in Express.js",
        description="Express returns 200 but the browser blocks it. Install the cors package and add one middleware call — here is the exact config.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-express/",
        schema=make_schema(
            "Fix CORS Error in Express.js",
            "Express CORS middleware setup for development and production.",
            f"{BASE_URL}/blog/cors/fix-cors-express/",
            [("Install cors package", "Run npm install cors in your project directory."),
             ("Apply middleware", "Call app.use(cors()) with your origin config before route definitions."),
             ("Handle preflight", "Add app.options('*', cors()) to respond to OPTIONS requests.")],
            [("Why does Express return 200 but the browser shows a CORS error?",
              "The server responded but did not include Access-Control-Allow-Origin. The browser blocks the response before JavaScript can read it. Install the cors npm package and call app.use(cors()) with your frontend origin before route definitions."),
             ("Can I use Access-Control-Allow-Origin * with cookies?",
              "No. Browsers reject wildcard origins when credentials are included. Set origin to your exact frontend domain and credentials to true."),
             ("Do I need to handle OPTIONS requests separately?",
              "Add app.options('*', cors()) before app.use(cors()) to handle preflight for all routes. Without it, POST and PUT with custom headers will fail.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Fix CORS in Express.js',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="Fix CORS Error in Express.js",
        content="""
<p class="lead">Your Express server is returning 200. The browser is blocking it anyway. That is CORS — the server responded but did not tell the browser the request was allowed. One middleware call fixes it.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to fetch at 'https://api.example.com/data' from origin 'https://app.example.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.</div>

<h2>Install and apply cors middleware</h2>
<pre>npm install cors</pre>

<pre>const express = require('express');
const cors = require('cors');
const app = express();

// Development — allows all origins (never use in production)
app.use(cors());

// Production — lock it to your frontend domain
app.use(cors({
  origin: 'https://app.example.com',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.get('/api/data', (req, res) => res.json({ ok: true }));
app.listen(3000);</pre>

<p>Put <code>app.use(cors())</code> before your route definitions. Middleware runs in declaration order — routes defined before the cors() call will not get CORS headers.</p>

<h2>If you are sending cookies or auth headers</h2>
<p>When your frontend sends <code>credentials: 'include'</code>, the wildcard origin stops working. The browser spec forbids <code>*</code> with credentials. You need an explicit origin.</p>

<pre>// Breaks when frontend uses credentials: 'include'
app.use(cors({ origin: '*', credentials: true })); // ❌

// Works
app.use(cors({
  origin: 'https://app.example.com',
  credentials: true
})); // ✅</pre>

<h2>If OPTIONS preflight is failing</h2>
<p>Browsers send an OPTIONS request before POST, PUT, or DELETE when custom headers are present. Add an explicit OPTIONS handler before the main cors() call.</p>

<pre>app.options('*', cors()); // Handle all preflight requests
app.use(cors({ origin: 'https://app.example.com' }));</pre>

<h2>Multiple allowed origins</h2>
<pre>const allowed = ['https://app.example.com', 'https://staging.example.com'];

app.use(cors({
  origin: function(origin, callback) {
    if (!origin || allowed.includes(origin)) {
      callback(null, origin);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));

// Add Vary: Origin so CDNs cache per-origin correctly
app.use((req, res, next) => { res.vary('Origin'); next(); });</pre>

<h2>Per-route CORS</h2>
<p>If you only need CORS on specific routes, pass the cors middleware directly to each route:</p>
<pre>const corsOpts = { origin: 'https://app.example.com' };

app.get('/api/public', cors(corsOpts), (req, res) => res.json({ data: 'ok' }));
app.post('/api/submit', cors(corsOpts), (req, res) => res.json({ status: 'received' }));</pre>

<p>Not sure if your CORS config is correct? CORSFixer sends a real OPTIONS preflight to your API and shows exactly what headers are missing or wrong.</p>
""",
        cta_url="/cors/",
        cta_text="Test your CORS config live → CORSFixer",
        related='<a href="/glossary/cors/">What is CORS?</a> <a href="/glossary/preflight-request/">Preflight requests</a> <a href="/fix/cors/express/">Express fix reference</a> <a href="/error/cors-blocked/">CORS blocked error</a>'
    ))

    # 2. FastAPI
    write("blog/cors/fix-cors-fastapi/index.html", template(
        title="Fix CORS Error in FastAPI",
        description="FastAPI blocks cross-origin requests by default. Add CORSMiddleware before your routes — works for React, Next.js, vLLM, and Ollama frontends.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-fastapi/",
        schema=make_schema(
            "Fix CORS Error in FastAPI",
            "FastAPI CORSMiddleware setup for browser frontends and LLM APIs.",
            f"{BASE_URL}/blog/cors/fix-cors-fastapi/",
            [("Add CORSMiddleware", "Import CORSMiddleware from fastapi.middleware.cors and call app.add_middleware()."),
             ("Set allowed origins", "Pass your frontend domain as a list. Never use ['*'] with credentials."),
             ("Test the connection", "Use CORSFixer to send a live preflight to your FastAPI endpoint.")],
            [("Why does FastAPI block requests from localhost:3000?",
              "Different ports count as different origins. localhost:8000 and localhost:3000 are cross-origin. Add CORSMiddleware with allow_origins=['http://localhost:3000']."),
             ("Does FastAPI handle OPTIONS preflight automatically?",
              "Yes — once CORSMiddleware is added, FastAPI responds to OPTIONS requests for all routes automatically."),
             ("Can I use allow_origins=['*'] with cookies?",
              "No. Wildcard origins are rejected when credentials are involved. List your origins explicitly.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Fix CORS in FastAPI',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="Fix CORS Error in FastAPI",
        content="""
<p class="lead">FastAPI does not add CORS headers by default. Your React app on port 3000 and FastAPI on port 8000 are different origins — the browser blocks the connection. Add CORSMiddleware before your routes and it works.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to fetch at 'http://localhost:8000/api' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.</div>

<h2>The fix</h2>
<pre>from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourapp.com"],  # your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
def get_data():
    return {"status": "ok"}</pre>

<p>Add the middleware before route definitions. FastAPI handles OPTIONS preflight automatically once CORSMiddleware is mounted — you do not need to write OPTIONS handlers manually.</p>

<h2>Development vs production</h2>
<pre>import os

dev_origins = ["http://localhost:3000", "http://localhost:5173"]
prod_origins = ["https://yourapp.com", "https://www.yourapp.com"]

origins = dev_origins if os.getenv("ENV") == "development" else prod_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)</pre>

<h2>Why allow_origins=["*"] breaks with credentials</h2>
<p>If your frontend sends cookies or an Authorization header, a wildcard origin will fail. The browser spec rejects this combination. Use an explicit origin list.</p>

<pre># Breaks when frontend uses credentials: 'include'
allow_origins=["*"], allow_credentials=True  # ❌

# Works
allow_origins=["https://yourapp.com"], allow_credentials=True  # ✅</pre>

<h2>vLLM and Ollama API backends</h2>
<p>Running a language model API that a browser-based chat UI calls? Configure allowed origins at startup:</p>
<pre># vLLM
vllm serve --host 0.0.0.0 --port 8000 \\
  --allowed-origins '["https://yourapp.com"]'

# Ollama
OLLAMA_ORIGINS=https://yourapp.com ollama serve</pre>

<h2>Starlette and raw ASGI apps</h2>
<pre>from starlette.middleware.cors import CORSMiddleware
from starlette.applications import Starlette

app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourapp.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)</pre>
""",
        cta_url="/cors/",
        cta_text="Test your FastAPI CORS config live →",
        related='<a href="/glossary/cors/">What is CORS?</a> <a href="/fix/cors/fastapi/">FastAPI fix reference</a> <a href="/glossary/preflight-request/">Preflight requests</a>'
    ))

    # 3. Nginx
    write("blog/cors/fix-cors-nginx/index.html", template(
        title="Fix CORS Error in Nginx",
        description="Nginx strips CORS headers from upstream responses and blocks preflight requests. Here is the exact server block config to fix both.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-nginx/",
        schema=make_schema(
            "Fix CORS Error in Nginx",
            "Nginx CORS configuration for reverse proxy and static servers.",
            f"{BASE_URL}/blog/cors/fix-cors-nginx/",
            [("Handle OPTIONS preflight", "Add an if block that returns 204 with CORS headers for OPTIONS requests."),
             ("Add CORS headers with always flag", "Use add_header with the always flag so headers appear on error responses too."),
             ("Reload Nginx", "Run nginx -t to test and nginx -s reload to apply changes.")],
            [("Why does Nginx strip CORS headers from my backend?",
              "Nginx does not automatically forward all headers from upstream services. You need to explicitly add CORS headers using add_header directives in your server block."),
             ("Why do I need to handle OPTIONS separately in Nginx?",
              "Nginx passes OPTIONS to the upstream by default. If your app does not handle OPTIONS, the preflight fails. Return 204 directly from Nginx for OPTIONS requests."),
             ("What does the always flag do in add_header?",
              "Without always, Nginx only adds the header on 2xx responses. always ensures CORS headers appear on error responses too, which is required when the browser checks preflight responses.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Fix CORS in Nginx',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="Fix CORS Error in Nginx — Reverse Proxy Configuration",
        content="""
<p class="lead">Nginx acts as a reverse proxy in front of your app. Unless you explicitly add CORS headers at the Nginx level, they may be stripped or never sent. This config handles both preflight and regular requests.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to XMLHttpRequest at 'https://api.example.com' from origin 'https://app.example.com' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present.</div>

<h2>Add to your server block</h2>
<pre>server {
    listen 443 ssl http2;
    server_name api.example.com;

    location / {
        # Handle OPTIONS preflight — return immediately without proxying
        if ($request_method = OPTIONS) {
            add_header Access-Control-Allow-Origin "https://app.example.com";
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Authorization, Content-Type";
            add_header Access-Control-Allow-Credentials "true";
            add_header Access-Control-Max-Age 86400;
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            return 204;
        }

        # Add CORS headers to all other responses
        add_header Access-Control-Allow-Origin "https://app.example.com" always;
        add_header Access-Control-Allow-Credentials "true" always;

        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}</pre>

<p>The <code>always</code> flag ensures headers appear on error responses too. Without it, a 401 or 500 response will not have CORS headers — the browser will show a CORS error instead of your actual error message, making debugging confusing.</p>

<h2>Multiple allowed origins</h2>
<pre>map $http_origin $cors_origin {
    default                      "";
    "https://app.example.com"    "https://app.example.com";
    "https://staging.example.com" "https://staging.example.com";
}

server {
    location / {
        if ($request_method = OPTIONS) {
            add_header Access-Control-Allow-Origin $cors_origin;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Authorization, Content-Type";
            add_header Content-Length 0;
            return 204;
        }

        add_header Access-Control-Allow-Origin $cors_origin always;
        add_header Vary Origin always;
        proxy_pass http://localhost:3000;
    }
}</pre>

<h2>Test and reload</h2>
<pre>nginx -t          # test configuration — fix errors before reloading
nginx -s reload   # apply changes without dropping connections</pre>

<p>After reloading, use CORSFixer to send a real preflight to your API and verify the response headers are correct.</p>
""",
        cta_url="/cors/",
        cta_text="Send a live preflight to your Nginx API →",
        related='<a href="/fix/cors/nginx/">Nginx CORS fix reference</a> <a href="/providers/nginx/">Nginx provider hub</a> <a href="/glossary/preflight-request/">What is a preflight?</a>'
    ))

    # 4. Next.js
    write("blog/cors/fix-cors-nextjs/index.html", template(
        title="Fix CORS Error in Next.js",
        description="Next.js API routes block cross-origin requests by default. Three ways to add CORS headers — next.config.js, middleware.ts, or per-route handlers.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-nextjs/",
        schema=make_schema(
            "Fix CORS Error in Next.js",
            "CORS configuration for Next.js API routes using next.config.js, middleware, or per-route handlers.",
            f"{BASE_URL}/blog/cors/fix-cors-nextjs/",
            [("Choose your approach", "Use next.config.js for all routes, middleware.ts for App Router with logic, or per-route for Pages Router."),
             ("Add CORS headers", "Set Access-Control-Allow-Origin, Allow-Methods, and Allow-Headers."),
             ("Handle OPTIONS preflight", "Return 204 with headers for OPTIONS requests in your handler or middleware.")],
            [("Which CORS method should I use in Next.js?",
              "Use next.config.js headers for simple global config. Use middleware.ts if you need conditional logic or dynamic origin matching. Use per-route headers for specific endpoints only."),
             ("Does Next.js handle OPTIONS preflight automatically?",
              "No. You need to explicitly return 204 for OPTIONS requests in your middleware or route handler."),
             ("Can I allow multiple origins in Next.js?",
              "Yes — in middleware.ts, read the request Origin header and conditionally set Access-Control-Allow-Origin to that value if it matches your allowlist.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Fix CORS in Next.js',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="Fix CORS Error in Next.js — API Routes and External APIs",
        content="""
<p class="lead">Next.js API routes block cross-origin requests by default. If another domain calls your API routes, you need CORS headers. There are three ways to add them depending on your setup.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to fetch at 'https://yourproject.vercel.app/api/data' from origin 'https://yourapp.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.</div>

<h2>Option 1 — next.config.js (cleanest for all routes)</h2>
<pre>// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: 'https://yourapp.com' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
        ],
      },
    ];
  },
};</pre>

<p>This applies to all API routes matching the pattern. It does not handle OPTIONS preflight automatically — you still need to return 204 for OPTIONS in your handler.</p>

<h2>Option 2 — middleware.ts (App Router, recommended)</h2>
<pre>// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Handle OPTIONS preflight
  if (request.method === 'OPTIONS') {
    return new NextResponse(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': 'https://yourapp.com',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400',
      },
    });
  }

  const response = NextResponse.next();
  response.headers.set('Access-Control-Allow-Origin', 'https://yourapp.com');
  response.headers.set('Access-Control-Allow-Credentials', 'true');
  return response;
}

export const config = { matcher: '/api/:path*' };</pre>

<h2>Option 3 — per route (Pages Router)</h2>
<pre>// pages/api/data.js
export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://yourapp.com');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  res.json({ data: 'ok' });
}</pre>

<h2>Dynamic origin for multiple allowed domains</h2>
<pre>// middleware.ts — allowlist approach
const ALLOWED = ['https://yourapp.com', 'https://staging.yourapp.com'];

export function middleware(request: NextRequest) {
  const origin = request.headers.get('origin') || '';
  const allowedOrigin = ALLOWED.includes(origin) ? origin : '';

  if (request.method === 'OPTIONS') {
    return new NextResponse(null, {
      status: 204,
      headers: { 'Access-Control-Allow-Origin': allowedOrigin, ... }
    });
  }
}</pre>
""",
        cta_url="/cors/",
        cta_text="Test your Next.js API CORS config →",
        related='<a href="/fix/cors/nextjs/">Next.js CORS fix reference</a> <a href="/providers/nextjs/">Next.js provider hub</a> <a href="/fix/cors/vercel/">Vercel CORS fix</a>'
    ))

    # 5. Preflight OPTIONS
    write("blog/cors/fix-cors-preflight-options/index.html", template(
        title="CORS Preflight Failing — OPTIONS Returns 404 or 403",
        description="Your POST works in Postman but fails in the browser. That is a missing preflight handler. Here is exactly what the browser sends and how to respond.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-preflight-options/",
        schema=make_schema(
            "CORS Preflight Failing — OPTIONS Returns 404 or 403",
            "Fix failing CORS preflight requests across Express, Nginx, FastAPI, and Django.",
            f"{BASE_URL}/blog/cors/fix-cors-preflight-options/",
            [("Understand the preflight", "The browser sends OPTIONS before POST, PUT, or DELETE with custom headers."),
             ("Return 204 with CORS headers", "Your server must respond to OPTIONS with a 200 or 204 and the correct CORS headers."),
             ("Cache the preflight result", "Set Access-Control-Max-Age to reduce repeated preflight requests.")],
            [("Why does my API work in Postman but fail in the browser?",
              "Postman is a developer tool that does not enforce CORS. The browser sends an OPTIONS preflight that your server is not handling. Add an OPTIONS route handler that returns 204 with CORS headers."),
             ("What status code should OPTIONS return?",
              "Return 204 (No Content) or 200 with the CORS headers and no body."),
             ("What is Access-Control-Max-Age?",
              "It tells the browser how long to cache the preflight result in seconds. Set it to 86400 (24 hours) to avoid a preflight on every request.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Preflight Failing',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="CORS Preflight Failing — OPTIONS Returns 404 or 403",
        content="""
<p class="lead">Postman works. curl works. The browser fails. That is almost always a missing preflight handler. Browsers send an OPTIONS request before POST, PUT, or DELETE — and your server is not responding to it correctly.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to fetch at 'https://api.example.com/submit' from origin 'https://app.example.com' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: It does not have HTTP ok status.</div>

<h2>What the browser actually sends first</h2>
<pre>OPTIONS /api/submit HTTP/1.1
Host: api.example.com
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization</pre>

<p>Your server must respond to this OPTIONS request with a 200 or 204 and the correct CORS headers. If it returns 404, the browser stops and shows a CORS error — even though your actual POST endpoint works fine.</p>

<h2>What triggers a preflight</h2>
<p>Not all requests get a preflight. Simple requests (GET, HEAD, POST with only simple headers like Content-Type: application/x-www-form-urlencoded) skip it. You get a preflight when you use:</p>
<ul>
  <li>Methods: PUT, DELETE, PATCH</li>
  <li>Headers: Authorization, Content-Type: application/json, or any custom header</li>
  <li>Credentials: any request with credentials: 'include'</li>
</ul>

<h2>Fix by framework</h2>

<h3>Express</h3>
<pre>app.options('*', cors()); // Handle all OPTIONS preflights
app.use(cors({ origin: 'https://app.example.com' }));</pre>

<h3>Nginx</h3>
<pre>if ($request_method = OPTIONS) {
    add_header Access-Control-Allow-Origin "https://app.example.com";
    add_header Access-Control-Allow-Methods "POST, GET, PUT, DELETE, OPTIONS";
    add_header Access-Control-Allow-Headers "Content-Type, Authorization";
    add_header Access-Control-Max-Age 86400;
    add_header Content-Length 0;
    return 204;
}</pre>

<h3>FastAPI</h3>
<pre># CORSMiddleware handles OPTIONS automatically — no extra config needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)</pre>

<h3>Django</h3>
<pre># Install django-cors-headers
pip install django-cors-headers

# settings.py
INSTALLED_APPS = [..., 'corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOWED_ORIGINS = ['https://app.example.com']
CORS_ALLOW_CREDENTIALS = True</pre>

<h2>Cache the preflight</h2>
<p><code>Access-Control-Max-Age: 86400</code> tells the browser to cache the preflight result for 24 hours. Without it, the browser sends OPTIONS before every single request — visible as extra network calls in DevTools.</p>
""",
        cta_url="/cors/",
        cta_text="Send a live OPTIONS preflight to your API →",
        related='<a href="/glossary/preflight-request/">What is a preflight?</a> <a href="/glossary/cors/">What is CORS?</a> <a href="/error/cors-blocked/">CORS blocked errors</a>'
    ))

    # 6. Credentials wildcard
    write("blog/cors/fix-cors-credentials/index.html", template(
        title="CORS Error With credentials: include — Why Wildcard Fails",
        description="Setting Access-Control-Allow-Origin to * breaks when you add credentials. The browser spec forbids this combination. Here is the exact fix.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-credentials/",
        schema=make_schema(
            "CORS Error With credentials: include — Why Wildcard Fails",
            "Fix the CORS wildcard + credentials error across Express, Nginx, FastAPI.",
            f"{BASE_URL}/blog/cors/fix-cors-credentials/",
            [("Replace wildcard with explicit origin", "Change allow_origins or origin from '*' to your exact frontend domain."),
             ("Set credentials flag", "Add credentials: true (Express) or allow_credentials=True (FastAPI)."),
             ("Add Vary: Origin header", "Tell CDNs to cache separate responses per origin.")],
            [("Why does Access-Control-Allow-Origin * work without credentials but fail with them?",
              "The browser spec forbids this combination as a security measure. A wildcard with credentials would let any website make authenticated requests on behalf of your users."),
             ("How do I allow multiple origins with credentials?",
              "Use a dynamic origin function that checks against an allowlist and returns the requesting origin if it matches. Never return * when credentials are involved."),
             ("Do I need Vary: Origin when using explicit origins?",
              "Yes — add Vary: Origin so CDNs cache separate responses per origin and do not serve one user's credentialed response to another.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Credentials Wildcard Error',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="CORS Error With credentials: include — Why * Stops Working",
        content="""
<p class="lead">You added <code>credentials: 'include'</code> to your fetch call and now CORS is broken even though it worked before. The browser spec explicitly forbids wildcard origins when credentials are sent. Switch to an explicit origin.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to fetch at 'https://api.example.com' from origin 'https://app.example.com' has been blocked by CORS policy: The value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*' when the request's credentials mode is 'include'.</div>

<h2>The combination that breaks</h2>
<pre>// Frontend — sends cookies or auth headers
fetch('https://api.example.com/data', {
  credentials: 'include' // sends session cookie
});

// Backend — this breaks
app.use(cors({ origin: '*', credentials: true })); // ❌</pre>

<h2>The fix — explicit origin on every stack</h2>

<h3>Express</h3>
<pre>app.use(cors({
  origin: 'https://app.example.com', // not '*'
  credentials: true
}));</pre>

<h3>Nginx</h3>
<pre>add_header Access-Control-Allow-Origin "https://app.example.com" always;
add_header Access-Control-Allow-Credentials "true" always;
add_header Vary Origin always;</pre>

<h3>FastAPI</h3>
<pre>app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],  # not ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)</pre>

<h2>Multiple origins with credentials</h2>
<pre>// Express — dynamic origin from allowlist
const allowedOrigins = ['https://app.example.com', 'https://staging.example.com'];

app.use(cors({
  origin: function(origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, origin); // return the actual origin, not '*'
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));

// Always add Vary: Origin so CDNs cache correctly
app.use((req, res, next) => { res.vary('Origin'); next(); });</pre>

<h2>Why Vary: Origin matters</h2>
<p>When your server returns a specific origin in Access-Control-Allow-Origin (instead of *), CDNs might cache that response and serve it to users from other origins. Adding <code>Vary: Origin</code> tells the CDN to store separate cached responses for each origin — preventing one user's cookies from leaking to another.</p>
""",
        cta_url="/cors/",
        cta_text="Test your CORS credentials config →",
        related='<a href="/glossary/cors/">What is CORS?</a> <a href="/glossary/vary-header/">The Vary header</a> <a href="/fix/cors/express/">Express CORS fix</a>'
    ))

    # 7. Vercel
    write("blog/cors/fix-cors-vercel/index.html", template(
        title="Fix CORS Error on Vercel Serverless Functions",
        description="Vercel functions do not add CORS headers automatically. Add them in vercel.json or directly in your function handler — here is both approaches.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-vercel/",
        schema=make_schema(
            "Fix CORS Error on Vercel Serverless Functions",
            "CORS configuration for Vercel serverless and edge functions.",
            f"{BASE_URL}/blog/cors/fix-cors-vercel/",
            [("Add headers in vercel.json", "Use the headers key to apply CORS headers to all API routes matching a pattern."),
             ("Handle OPTIONS in the function", "Return 204 with headers for OPTIONS requests to handle preflight."),
             ("Or use middleware.ts", "For App Router, middleware.ts handles CORS more cleanly with dynamic logic.")],
            [("Does vercel.json CORS config handle OPTIONS preflight?",
              "No — vercel.json adds headers to responses but does not intercept OPTIONS. Handle OPTIONS in your function handler or use Next.js middleware."),
             ("Should I use vercel.json or function-level headers?",
              "Use vercel.json for global config across all routes. Use function-level headers when you need different CORS config per route."),
             ("Does Vercel's free tier support custom headers?",
              "Yes — vercel.json headers work on all Vercel plans including the free hobby tier.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Fix CORS on Vercel',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="Fix CORS Error on Vercel Serverless Functions",
        content="""
<p class="lead">Vercel serverless functions do not add CORS headers automatically. When called from a different domain, the browser blocks the response. Add headers in vercel.json to fix all API routes at once.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to fetch at 'https://yourproject.vercel.app/api/data' from origin 'https://yourapp.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.</div>

<h2>Option 1 — vercel.json (applies to all API routes)</h2>
<pre>{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "https://yourapp.com" },
        { "key": "Access-Control-Allow-Methods", "value": "GET,POST,PUT,DELETE,OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type, Authorization" },
        { "key": "Access-Control-Allow-Credentials", "value": "true" }
      ]
    }
  ]
}</pre>

<p>This adds headers to all responses but does not handle OPTIONS preflight automatically. You still need to return 204 for OPTIONS in your function.</p>

<h2>Option 2 — inside the function handler</h2>
<pre>// api/data.js
export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://yourapp.com');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  return res.json({ data: 'ok' });
}</pre>

<h2>Option 3 — middleware.ts for App Router</h2>
<pre>// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request) {
  if (request.method === 'OPTIONS') {
    return new NextResponse(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': 'https://yourapp.com',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400',
      },
    });
  }
  const response = NextResponse.next();
  response.headers.set('Access-Control-Allow-Origin', 'https://yourapp.com');
  return response;
}

export const config = { matcher: '/api/:path*' };</pre>
""",
        cta_url="/cors/",
        cta_text="Test your Vercel CORS config live →",
        related='<a href="/fix/cors/nextjs/">Next.js CORS fix</a> <a href="/providers/vercel/">Vercel provider hub</a> <a href="/fix/headers/vercel/">Vercel security headers</a>'
    ))

    # 8. Spring Boot
    write("blog/cors/fix-cors-spring-boot/index.html", template(
        title="Fix CORS Error in Spring Boot",
        description="Spring Boot has built-in CORS support. Enable it globally with WebMvcConfigurer or per-controller with @CrossOrigin — and how to fix it when Spring Security overrides both.",
        canonical=f"{BASE_URL}/blog/cors/fix-cors-spring-boot/",
        schema=make_schema(
            "Fix CORS Error in Spring Boot",
            "Spring Boot CORS configuration via WebMvcConfigurer, @CrossOrigin, and Spring Security.",
            f"{BASE_URL}/blog/cors/fix-cors-spring-boot/",
            [("Choose global or per-controller", "WebMvcConfigurer applies to all endpoints. @CrossOrigin applies per controller or method."),
             ("Add CORS to Spring Security", "If Spring Security is enabled, add CORS to the SecurityFilterChain — it runs before MVC."),
             ("Test the preflight response", "Spring Boot handles OPTIONS automatically when CORS is configured correctly.")],
            [("Why does @CrossOrigin not work with Spring Security?",
              "Spring Security's filter chain runs before MVC, so it can block requests before @CrossOrigin is evaluated. Add CORS configuration to your SecurityFilterChain using http.cors()."),
             ("What is the difference between addCorsMappings and @CrossOrigin?",
              "addCorsMappings in WebMvcConfigurer is global — applies to all matching paths. @CrossOrigin is per controller or method and overrides global config for that endpoint."),
             ("Do I need to handle OPTIONS manually in Spring Boot?",
              "No — Spring Boot handles OPTIONS preflight automatically when CORS is configured via WebMvcConfigurer or @CrossOrigin. You do not need to write OPTIONS handlers.")]
        ),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/cors/">CORS</a> → Fix CORS in Spring Boot',
        tag="CORS", tag_color=PURPLE_TAG,
        h1="Fix CORS Error in Spring Boot — Java Backend",
        content="""
<p class="lead">Spring Boot blocks cross-origin requests by default. You have three options: global config via WebMvcConfigurer, per-controller via @CrossOrigin, or — the one most people miss — adding CORS to Spring Security's filter chain.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Access to XMLHttpRequest at 'http://localhost:8080/api/data' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.</div>

<h2>Option 1 — Global CORS config</h2>
<pre>@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("https://yourapp.com")
            .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(86400);
    }
}</pre>

<h2>Option 2 — Per controller with @CrossOrigin</h2>
<pre>@RestController
@CrossOrigin(origins = "https://yourapp.com", allowCredentials = "true")
public class DataController {

    @GetMapping("/api/data")
    public ResponseEntity&lt;?&gt; getData() {
        return ResponseEntity.ok(Map.of("status", "ok"));
    }
}</pre>

<h2>Option 3 — Spring Security (most common issue)</h2>
<p>If you have Spring Security, it processes requests before MVC — so WebMvcConfigurer CORS config never runs. Add CORS to your SecurityFilterChain directly:</p>
<pre>@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .csrf(csrf -> csrf.disable());
        return http.build();
    }

    @Bean
    CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("https://yourapp.com"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true);
        config.setMaxAge(86400L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}</pre>

<p>This is the fix 90% of Spring Boot + Spring Security CORS problems need. The other two options do nothing when Security is in the chain.</p>
""",
        cta_url="/cors/",
        cta_text="Test your Spring Boot CORS config →",
        related='<a href="/glossary/cors/">What is CORS?</a> <a href="/glossary/preflight-request/">Preflight requests</a> <a href="/fix/cors/nginx/">Nginx CORS fix</a>'
    ))


# ─── BATCH 2: CSP FIX GUIDES ──────────────────────────────────────────────────

def batch2_csp():
    print("\n📦 Batch 2 — CSP Fix Guides")

    articles = [
        {
            "slug": "fix-csp-nextjs",
            "dir": "blog/csp",
            "title": "Fix CSP Header in Next.js — Nonce-Based Approach",
            "description": "Next.js inline scripts break strict CSP. This guide shows nonce-based CSP that works with App Router without unsafe-inline.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "cta_url": "/csp/", "cta_text": "Scan your page CSP live → CSPFixer",
            "related": '<a href="/glossary/content-security-policy/">What is CSP?</a> <a href="/glossary/csp-nonce/">CSP nonces</a> <a href="/glossary/unsafe-inline/">Why unsafe-inline is dangerous</a>',
            "steps": [("Generate a nonce per request", "Create a random value in middleware.ts for each request."), ("Pass nonce to script tags", "Set the nonce attribute on all inline scripts."), ("Set CSP header with nonce", "Include the nonce in your script-src directive.")],
            "faqs": [("Why does Next.js break with a strict CSP?", "Next.js generates inline scripts for hydration. These inline scripts are blocked by a strict CSP unless you use nonces or unsafe-inline. Nonces are the secure approach."), ("What is unsafe-inline and why avoid it?", "unsafe-inline allows any inline script to run, which defeats XSS protection entirely. A nonce lets specific trusted scripts run while blocking injected scripts."), ("How do I generate a nonce in Next.js?", "Generate a random base64 string in middleware.ts, add it to the CSP header, and pass it to your layout via a response header that the layout reads.")],
            "content": """
<p class="lead">Next.js generates inline scripts for hydration that a strict CSP will block. Adding <code>unsafe-inline</code> fixes the error but defeats the purpose of CSP entirely. Nonces are the right solution — a random value per request that lets specific scripts run.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Refused to execute inline script because it violates the following Content Security Policy directive: "script-src 'self'". Either the 'unsafe-inline' keyword, a hash, or a nonce is required to enable inline execution.</div>

<h2>Step 1 — Generate nonce in middleware.ts</h2>
<pre>// middleware.ts
import { NextResponse } from 'next/server';
import crypto from 'crypto';

export function middleware(request) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');

  const csp = [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'`,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "frame-ancestors 'none'",
  ].join('; ');

  const response = NextResponse.next();
  response.headers.set('Content-Security-Policy', csp);
  response.headers.set('x-nonce', nonce); // pass to layout
  return response;
}

export const config = { matcher: '/((?!_next/static|_next/image|favicon.ico).*)' };</pre>

<h2>Step 2 — Read nonce in root layout</h2>
<pre>// app/layout.tsx
import { headers } from 'next/headers';

export default function RootLayout({ children }) {
  const nonce = headers().get('x-nonce') || '';

  return (
    &lt;html&gt;
      &lt;head&gt;
        &lt;script
          nonce={nonce}
          dangerouslySetInnerHTML={{
            __html: `window.__NONCE__ = "${nonce}";`
          }}
        /&gt;
      &lt;/head&gt;
      &lt;body&gt;{children}&lt;/body&gt;
    &lt;/html&gt;
  );
}</pre>

<h2>Step 3 — Pass nonce to Script components</h2>
<pre>// For next/script components
import Script from 'next/script';

&lt;Script
  nonce={nonce}
  src="https://example.com/script.js"
  strategy="afterInteractive"
/&gt;</pre>

<h2>Third-party scripts with nonces</h2>
<p>For Google Analytics, Hotjar, or any third-party script, pass the nonce and add their domains to script-src:</p>
<pre>const csp = [
  `script-src 'self' 'nonce-${nonce}' https://www.googletagmanager.com`,
  "connect-src 'self' https://www.google-analytics.com",
].join('; ');</pre>

<p>Not sure which resources your page is loading? CSPFixer scans your live URL and generates a CSP based on what it finds.</p>"""
        },
        {
            "slug": "csp-generator-vercel",
            "dir": "blog/csp",
            "title": "Content Security Policy for Vercel — Generate and Deploy",
            "description": "CSP on Vercel goes in vercel.json. Here is a working CSP config for common stacks deployed on Vercel, including Next.js and static sites.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "cta_url": "/csp/", "cta_text": "Generate your CSP from your live page →",
            "related": '<a href="/glossary/content-security-policy/">What is CSP?</a> <a href="/fix/csp/vercel/">Vercel CSP fix reference</a> <a href="/providers/vercel/">Vercel provider hub</a>',
            "steps": [("Scan your page", "Use CSPFixer to enumerate all external resources your page loads."), ("Build the CSP header", "Construct directives for each resource type: script-src, style-src, img-src, connect-src."), ("Add to vercel.json", "Put the CSP in vercel.json headers and deploy.")],
            "faqs": [("Where does CSP go in Vercel?", "In vercel.json under the headers key. Set the Content-Security-Policy header for the source pattern matching your pages."), ("Will CSP break my Vercel site?", "It can if external resources are not allowlisted. Use Content-Security-Policy-Report-Only first to collect violations without blocking anything."), ("Does Vercel add any security headers automatically?", "Vercel adds X-Content-Type-Options: nosniff and X-Frame-Options: SAMEORIGIN on some plans. Check with HeadersFixer — it shows you exactly what headers your site sends.")],
            "content": """
<p class="lead">Vercel does not add a Content Security Policy by default. You define it in vercel.json under the headers key. Start with report-only mode to collect violations before enforcing.</p>

<h2>Step 1 — Find what your page loads first</h2>
<p>Before writing a CSP, you need to know what external resources your page loads. Open DevTools → Network, reload the page, and note every external domain in the requests list. Or use CSPFixer — it scans your live URL automatically.</p>

<h2>Step 2 — Build your vercel.json config</h2>
<pre>{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com; frame-ancestors 'none'; object-src 'none';"
        }
      ]
    }
  ]
}</pre>

<h2>Step 3 — Start with report-only</h2>
<p>Use <code>Content-Security-Policy-Report-Only</code> first. It logs violations to the console without blocking anything, so you can see what needs to be added before enforcing:</p>
<pre>{
  "key": "Content-Security-Policy-Report-Only",
  "value": "default-src 'self'; script-src 'self'; report-uri https://your-reporting-endpoint.com/csp"
}</pre>

<h2>Common Vercel stack additions</h2>
<table>
  <thead><tr><th>Service</th><th>Directive to add</th></tr></thead>
  <tbody>
    <tr><td>Google Fonts</td><td>style-src + https://fonts.googleapis.com; font-src + https://fonts.gstatic.com</td></tr>
    <tr><td>Google Analytics</td><td>script-src + https://www.googletagmanager.com; connect-src + https://www.google-analytics.com</td></tr>
    <tr><td>Stripe.js</td><td>script-src + https://js.stripe.com; frame-src + https://js.stripe.com</td></tr>
    <tr><td>Intercom</td><td>script-src + https://widget.intercom.io; connect-src + https://api.intercom.io</td></tr>
    <tr><td>Hotjar</td><td>script-src + https://static.hotjar.com; connect-src + https://*.hotjar.com</td></tr>
  </tbody>
</table>

<h2>After deploying</h2>
<p>Open DevTools Console and look for CSP violation messages. Each one tells you exactly which domain needs to be added to which directive. Keep iterating until violations stop.</p>"""
        },
        {
            "slug": "fix-csp-refused-to-load",
            "dir": "blog/csp",
            "title": 'Fix "Refused to load script" CSP Error',
            "description": "The browser console shows exactly which resource was blocked and which CSP directive caused it. Here is how to read the error and add the right fix.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "cta_url": "/csp/", "cta_text": "Scan all blocked resources at once → CSPFixer",
            "related": '<a href="/glossary/content-security-policy/">What is CSP?</a> <a href="/blog/csp/csp-google-analytics-hotjar/">CSP for third-party scripts</a> <a href="/error/csp-refused-to-load/">CSP refused to load error</a>',
            "steps": [("Read the full error message", "The browser console tells you the blocked URL and which directive to update."), ("Add the domain to the right directive", "Match the resource type (script, style, image) to the correct CSP directive."), ("Redeploy and test", "Use CSPFixer to confirm no resources are still blocked.")],
            "faqs": [("How do I know which CSP directive to add a domain to?", "The browser console shows the exact directive that caused the block. Scripts go in script-src, stylesheets in style-src, images in img-src, API calls in connect-src, fonts in font-src."), ("Can I use a wildcard in CSP?", "Yes — https://api.example.com/* allows all paths under that domain. But wildcards for schemes or hostnames (https://*) are risky and should be avoided."), ("What is unsafe-inline and should I use it?", "unsafe-inline allows all inline scripts or styles. It works but defeats XSS protection. Use nonces or hashes instead for inline scripts.")],
            "content": """
<p class="lead">The browser console gives you everything you need to fix this. It shows the blocked URL, the directive that caused the block, and what your current policy says. Read the error, add the domain to the right directive, redeploy.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Refused to load the script 'https://cdn.example.com/widget.js' because it violates the following Content Security Policy directive: "script-src 'self' https://trusted.com". Note that 'script-src-elem' was not explicitly set, so 'script-src' is used as a fallback.</div>

<h2>Reading the error</h2>
<p>This error tells you three things:</p>
<ul>
  <li>What was blocked: <code>https://cdn.example.com/widget.js</code></li>
  <li>Which directive blocked it: <code>script-src</code></li>
  <li>What your current policy allows: <code>'self' https://trusted.com</code></li>
</ul>
<p>The fix is to add <code>https://cdn.example.com</code> to <code>script-src</code>.</p>

<h2>Resource type to directive mapping</h2>
<table>
  <thead><tr><th>Resource type</th><th>Directive</th><th>Example</th></tr></thead>
  <tbody>
    <tr><td>JavaScript files</td><td>script-src</td><td>script-src 'self' https://cdn.example.com</td></tr>
    <tr><td>CSS stylesheets</td><td>style-src</td><td>style-src 'self' https://fonts.googleapis.com</td></tr>
    <tr><td>Images</td><td>img-src</td><td>img-src 'self' data: https://images.example.com</td></tr>
    <tr><td>Fonts</td><td>font-src</td><td>font-src 'self' https://fonts.gstatic.com</td></tr>
    <tr><td>XHR / fetch / WebSocket</td><td>connect-src</td><td>connect-src 'self' https://api.example.com</td></tr>
    <tr><td>Iframes</td><td>frame-src</td><td>frame-src https://www.youtube.com</td></tr>
    <tr><td>Web Workers</td><td>worker-src</td><td>worker-src 'self' blob:</td></tr>
  </tbody>
</table>

<h2>Multiple violations at once</h2>
<p>When you add a CSP for the first time, you will likely see many violations. Instead of fixing them one by one, use CSPFixer — it scans your live page, finds all external resources, and generates the complete CSP in one shot.</p>

<h2>Inline script violations</h2>
<div class="error-box"><div class="error-label">Browser Console Error</div>Refused to execute inline script because it violates the following Content Security Policy directive: "script-src 'self'".</div>

<p>For inline scripts, you have three options:</p>
<pre>// Option 1 — nonce (secure, works per-request)
&lt;script nonce="random-base64-value"&gt;...&lt;/script&gt;
// CSP: script-src 'self' 'nonce-random-base64-value'

// Option 2 — hash (secure, works for static scripts)
// CSP: script-src 'self' 'sha256-hash-of-script-content'

// Option 3 — unsafe-inline (not recommended, defeats XSS protection)
// CSP: script-src 'self' 'unsafe-inline'</pre>"""
        },
        {
            "slug": "csp-google-analytics-hotjar",
            "dir": "blog/csp",
            "title": "CSP for Google Analytics, Hotjar and Third-Party Scripts",
            "description": "Marketing scripts are the hardest part of CSP. Here are the exact directives for GA4, Hotjar, Intercom, HubSpot, and Stripe — tested and working.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "cta_url": "/csp/", "cta_text": "Scan your page to find all third-party scripts →",
            "related": '<a href="/blog/csp/fix-csp-refused-to-load/">Fix refused to load errors</a> <a href="/glossary/content-security-policy/">What is CSP?</a> <a href="/blog/csp/csp-unsafe-inline-nonce-hash/">Nonce vs hash vs unsafe-inline</a>',
            "steps": [("Identify your third-party scripts", "Check the Network tab in DevTools for external script and connect requests."), ("Add required domains to CSP directives", "Each service needs specific domains added to script-src, connect-src, and sometimes img-src."), ("Test with CSPFixer", "Verify no violations remain after updating your CSP.")],
            "faqs": [("Why do third-party scripts break CSP?", "Third-party scripts often load from multiple subdomains, make XHR/fetch calls to their own APIs, and sometimes inject inline scripts. Each of these needs a separate allowlist entry."), ("Can I use wildcards for subdomains in CSP?", "Yes — https://*.hotjar.com covers all Hotjar subdomains. Be specific where possible; wildcards increase the attack surface slightly."), ("What is the safest way to add marketing scripts?", "Use Partytown to offload them to a Web Worker. This keeps them out of the main thread and reduces CSP complexity since Worker scripts have a separate policy.")],
            "content": """
<p class="lead">Marketing and analytics scripts are the hardest part of getting CSP right. They load from multiple subdomains, inject inline scripts, and make API calls — each requiring separate CSP entries. Here are the exact directives for the most common services.</p>

<h2>Google Analytics 4 (GA4)</h2>
<pre>script-src 'self' https://www.googletagmanager.com https://www.google-analytics.com;
connect-src 'self' https://www.google-analytics.com https://analytics.google.com https://region1.google-analytics.com;
img-src 'self' https://www.google-analytics.com https://www.googletagmanager.com;</pre>

<h2>Hotjar</h2>
<pre>script-src 'self' https://static.hotjar.com https://script.hotjar.com;
connect-src 'self' https://*.hotjar.com https://*.hotjar.io wss://*.hotjar.com;
img-src 'self' https://*.hotjar.com;
font-src 'self' https://static.hotjar.com;</pre>

<h2>Intercom</h2>
<pre>script-src 'self' https://widget.intercom.io https://js.intercomcdn.com;
connect-src 'self' https://api.intercom.io https://api-iam.intercom.io wss://nexus-websocket-a.intercom.io;
img-src 'self' https://static.intercomassets.com https://downloads.intercomcdn.com;
frame-src 'self' https://intercom-sheets.com;</pre>

<h2>Stripe.js</h2>
<pre>script-src 'self' https://js.stripe.com;
frame-src 'self' https://js.stripe.com https://hooks.stripe.com;
connect-src 'self' https://api.stripe.com;</pre>

<h2>HubSpot</h2>
<pre>script-src 'self' https://js.hs-scripts.com https://js.usemessages.com https://js.hscollectedforms.net;
connect-src 'self' https://api.hubspot.com https://forms.hubspot.com;
img-src 'self' https://track.hubspot.com;</pre>

<h2>reCAPTCHA v3</h2>
<pre>script-src 'self' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/;
frame-src 'self' https://www.google.com/recaptcha/;
connect-src 'self' https://www.google.com/recaptcha/;</pre>

<h2>Partytown — the better approach for analytics</h2>
<p>Instead of allowlisting all these domains, you can run third-party scripts in a Web Worker using Partytown. They execute off the main thread, improve performance, and simplify your CSP:</p>
<pre>&lt;!-- Replace your GA4 script type with text/partytown --&gt;
&lt;script type="text/partytown" src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"&gt;&lt;/script&gt;
&lt;script type="text/partytown"&gt;
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX');
&lt;/script&gt;

&lt;!-- Partytown loader --&gt;
&lt;script&gt;partytown = { forward: ['dataLayer.push'] };&lt;/script&gt;
&lt;script src="https://cdn.jsdelivr.net/npm/@builder.io/partytown/partytown.js"&gt;&lt;/script&gt;</pre>"""
        },
        {
            "slug": "csp-unsafe-inline-nonce-hash",
            "dir": "blog/csp",
            "title": "CSP unsafe-inline vs Nonce vs Hash — Which to Use",
            "description": "Three ways to allow inline scripts in CSP — and only two of them are actually safe. Here is when to use each and why unsafe-inline defeats the whole point.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "cta_url": "/csp/", "cta_text": "Generate a CSP for your page → CSPFixer",
            "related": '<a href="/glossary/csp-nonce/">What is a CSP nonce?</a> <a href="/glossary/unsafe-inline/">unsafe-inline explained</a> <a href="/blog/csp/fix-csp-nextjs/">CSP in Next.js with nonces</a>',
            "steps": [("Avoid unsafe-inline in production", "It allows any inline script to run and defeats XSS protection."), ("Use nonces for dynamic content", "Generate a random value per request and set it as the nonce attribute on your inline scripts."), ("Use hashes for static scripts", "Compute the SHA-256 hash of your inline script content and add it to script-src.")],
            "faqs": [("What is unsafe-inline?", "A CSP keyword that allows all inline scripts or styles to run. It works but defeats XSS protection — an attacker who can inject a script tag can execute arbitrary JavaScript."), ("When should I use a nonce?", "Use nonces when your inline scripts are generated server-side and change per request (like Next.js hydration scripts). Generate a cryptographically random value per request."), ("When should I use a hash?", "Use hashes when your inline script content is static and does not change between requests. Compute the SHA-256 hash of the exact script content and add it to script-src.")],
            "content": """
<p class="lead">You have a CSP that blocks inline scripts. You need inline scripts to run. You have three options — and only two of them actually keep you safe.</p>

<h2>Option 1 — unsafe-inline (avoid in production)</h2>
<pre>Content-Security-Policy: script-src 'self' 'unsafe-inline'</pre>

<p>This allows every inline script on your page to run — including any scripts an attacker manages to inject via XSS. It fixes the CSP error but defeats the entire purpose of having CSP. Use it in development only.</p>

<h2>Option 2 — Nonces (best for dynamic content)</h2>
<p>A nonce is a random base64 string generated per request. You set it on your inline scripts as an attribute, and include it in your CSP header. Only scripts with the matching nonce can run.</p>

<pre># Server generates nonce
nonce = base64.b64encode(os.urandom(16)).decode('utf-8')

# CSP header includes nonce
Content-Security-Policy: script-src 'self' 'nonce-{nonce}'

# HTML includes nonce attribute
&lt;script nonce="{nonce}"&gt;
  // This script is allowed
  console.log('hello');
&lt;/script&gt;</pre>

<p>An attacker who injects a script tag cannot know the nonce (it changes every request), so their injected script is blocked. Your legitimate scripts with the nonce attribute run.</p>

<h2>Option 3 — Hashes (best for static scripts)</h2>
<p>If your inline script content never changes, compute its SHA-256 hash and add it to the CSP. Only scripts with matching content can run.</p>

<pre># Compute hash (Python example)
import hashlib, base64
script = "console.log('hello');"
digest = hashlib.sha256(script.encode()).digest()
hash_b64 = base64.b64encode(digest).decode()
# hash_b64 = 'abc123...'

# CSP header
Content-Security-Policy: script-src 'self' 'sha256-abc123...'

# HTML — no attribute needed, the content must match exactly
&lt;script&gt;console.log('hello');&lt;/script&gt;</pre>

<p>If the script content changes even by one character, the hash no longer matches and the script is blocked. This makes hashes unsuitable for any dynamically generated content.</p>

<h2>Decision table</h2>
<table>
  <thead><tr><th>Approach</th><th>Safe?</th><th>Best for</th><th>Changes per request?</th></tr></thead>
  <tbody>
    <tr><td>unsafe-inline</td><td>❌ No</td><td>Development only</td><td>N/A</td></tr>
    <tr><td>Nonce</td><td>✅ Yes</td><td>Dynamic inline scripts</td><td>Yes — new nonce each request</td></tr>
    <tr><td>Hash</td><td>✅ Yes</td><td>Static inline scripts</td><td>No — content must stay identical</td></tr>
  </tbody>
</table>"""
        },
        {
            "slug": "csp-wordpress",
            "dir": "blog/csp",
            "title": "Content Security Policy for WordPress — Without Breaking Plugins",
            "description": "WordPress and plugins add inline scripts that break strict CSP. Here is a practical approach using report-only mode first, then gradual enforcement.",
            "tag": "CSP", "tag_color": GREEN_TAG,
            "cta_url": "/csp/", "cta_text": "Scan your WordPress site → CSPFixer",
            "related": '<a href="/glossary/content-security-policy/">What is CSP?</a> <a href="/blog/csp/csp-google-analytics-hotjar/">CSP for third-party scripts</a> <a href="/fix/csp/nginx/">Nginx CSP fix</a>',
            "steps": [("Start with report-only mode", "Deploy CSP-Report-Only to collect violations without breaking anything."), ("Identify what needs allowlisting", "Read the console violations and add each domain to the right directive."), ("Enforce gradually", "Switch to Content-Security-Policy once violations stop appearing.")],
            "faqs": [("Why is WordPress hard to secure with CSP?", "Plugins and themes add inline scripts without nonces, load from third-party CDNs, and generate dynamic script content. A strict CSP will break most WordPress sites out of the box."), ("How do I add CSP headers in WordPress?", "Use a plugin like WP Headers and Footers, add it to your Nginx/Apache config, or use functions.php with add_filter('wp_headers')."), ("Will CSP break my WordPress plugins?", "Many plugins will have CSP violations on first install. Use report-only mode for 1-2 weeks to collect violations and build your allowlist before enforcing.")],
            "content": """
<p class="lead">WordPress is one of the hardest platforms for CSP because plugins and themes add inline scripts that you do not control. The practical approach: start with report-only, collect violations for a week, then enforce.</p>

<h2>Step 1 — Start with report-only mode</h2>
<p>Never deploy an enforcing CSP on WordPress without testing first. Use report-only to collect violations without breaking anything:</p>
<pre># Nginx — add to your WordPress server block
add_header Content-Security-Policy-Report-Only "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; report-uri /csp-violations;" always;</pre>

<p>Open your browser console. Visit several pages of your site — home, shop, checkout, blog. Every CSP violation will appear in the console as an error message. Note down every blocked domain.</p>

<h2>Step 2 — Add CSP via WordPress hook</h2>
<pre>// functions.php
add_filter('wp_headers', function($headers) {
    $headers['Content-Security-Policy-Report-Only'] =
        "default-src 'self'; " .
        "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; " .
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " .
        "font-src 'self' https://fonts.gstatic.com; " .
        "img-src 'self' data: https:; " .
        "connect-src 'self' https://www.google-analytics.com;";
    return $headers;
});</pre>

<h2>Common WordPress plugin domains to allowlist</h2>
<table>
  <thead><tr><th>Plugin</th><th>Domains to add</th></tr></thead>
  <tbody>
    <tr><td>WooCommerce</td><td>script-src + 'unsafe-inline'; connect-src + your store domain</td></tr>
    <tr><td>Elementor</td><td>script-src + 'unsafe-inline'; style-src + 'unsafe-inline'</td></tr>
    <tr><td>Yoast SEO</td><td>script-src + 'unsafe-inline'</td></tr>
    <tr><td>Contact Form 7</td><td>script-src + 'unsafe-inline'</td></tr>
    <tr><td>Jetpack</td><td>script-src + https://stats.wp.com; connect-src + https://jetpack.wordpress.com</td></tr>
  </tbody>
</table>

<h2>Reality check on WordPress CSP</h2>
<p>Most WordPress sites end up needing <code>'unsafe-inline'</code> in script-src and style-src because plugins inject inline content without nonces. This is not ideal — but a CSP that allows only known external domains is still better than no CSP at all. It blocks external script injection even if it cannot block inline attacks.</p>

<p>If you need a strict CSP, consider a headless WordPress setup where the frontend is a separate Next.js or Nuxt app — you control all the inline scripts there.</p>"""
        },
    ]

    for art in articles:
        write(f"{art['dir']}/{art['slug']}/index.html", template(
            title=art["title"],
            description=art["description"],
            canonical=f"{BASE_URL}/{art['dir']}/{art['slug']}/",
            schema=make_schema(art["title"], art["description"], f"{BASE_URL}/{art['dir']}/{art['slug']}/", art["steps"], art["faqs"]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/csp/">CSP</a> → {art["title"]}',
            tag=art["tag"], tag_color=art["tag_color"],
            h1=art["title"],
            content=art["content"],
            cta_url=art["cta_url"], cta_text=art["cta_text"],
            related=art["related"]
        ))


# ─── BATCH 3: OAUTH FIX GUIDES ────────────────────────────────────────────────

def batch3_oauth():
    print("\n📦 Batch 3 — OAuth Fix Guides")

    articles = [
        {
            "slug": "fix-invalid-grant",
            "title": "Fix OAuth invalid_grant Error — Auth0, Okta, Google, Cognito",
            "description": "invalid_grant means the authorization code expired, was reused, has a PKCE mismatch, or the refresh token was revoked. Here is how to diagnose and fix each cause.",
            "content": """
<p class="lead">invalid_grant is the most common OAuth error and has four different causes. The error message rarely tells you which one. Here is how to diagnose and fix each.</p>

<div class="error-box"><div class="error-label">OAuth Error Response</div>{"error": "invalid_grant", "error_description": "Invalid authorization code"}</div>

<h2>Cause 1 — Authorization code expired</h2>
<p>Authorization codes expire fast — usually 10 minutes or less. If your exchange request arrives after expiry, you get invalid_grant.</p>
<p><strong>Fix:</strong> Ensure your code exchange happens immediately after the redirect. Do not store the code or delay the exchange. If your server is slow, check the time between the redirect and the POST to /token.</p>

<h2>Cause 2 — Authorization code reused</h2>
<p>Each authorization code can only be used once. If your code exchange runs twice (e.g., due to a React re-render, a duplicated API call, or a retry), the second call gets invalid_grant.</p>
<pre>// Prevent double exchange — check if already processing
if (sessionStorage.getItem('exchanging')) return;
sessionStorage.setItem('exchanging', 'true');

const tokens = await exchangeCode(code);
sessionStorage.removeItem('exchanging');</pre>

<h2>Cause 3 — PKCE verifier mismatch</h2>
<p>The code_verifier in your token request must match the code_challenge you sent in the authorization request. Any mismatch causes invalid_grant.</p>
<pre>// Generate and STORE the verifier before redirecting
const verifier = generateRandomString(64);
sessionStorage.setItem('pkce_verifier', verifier);

const challenge = await generateChallenge(verifier);
// redirect to auth with code_challenge=challenge

// On callback — retrieve the SAME verifier
const verifier = sessionStorage.getItem('pkce_verifier');
const tokens = await fetch('/token', {
  body: new URLSearchParams({
    code_verifier: verifier, // must match original
    code: authCode,
    ...
  })
});</pre>

<h2>Cause 4 — Refresh token revoked or rotated</h2>
<p>Refresh tokens can be revoked by the user, expired due to inactivity, or invalidated by token rotation (using a rotated refresh token triggers invalid_grant).</p>
<p><strong>Fix:</strong> Catch invalid_grant on refresh token calls and redirect to login:</p>
<pre>async function refreshTokens(refreshToken) {
  const response = await fetch('/token', {
    method: 'POST',
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
    })
  });

  if (!response.ok) {
    const error = await response.json();
    if (error.error === 'invalid_grant') {
      // Token revoked or expired — force re-login
      clearTokens();
      window.location.href = '/login';
      return;
    }
    throw new Error('Token refresh failed');
  }

  return response.json();
}</pre>

<h2>Clock skew (service accounts)</h2>
<p>For server-to-server OAuth (Google service accounts, JWT assertions), clock skew of more than 5 minutes between your server and the auth server causes invalid_grant. Sync your server time:</p>
<pre>sudo ntpdate -u pool.ntp.org
# or
sudo timedatectl set-ntp true</pre>""",
            "steps": [("Check if code expired", "Authorization codes expire in 10 minutes or less. Exchange immediately after redirect."), ("Check for double exchange", "Each code can only be used once. Prevent re-renders or retries from calling the exchange twice."), ("Verify PKCE verifier matches", "The code_verifier must match the code_challenge from the authorization request.")],
            "faqs": [("Why does invalid_grant happen on the first login attempt?", "Usually a PKCE mismatch, an expired code, or a clock skew issue. Check that your code_verifier is stored before the redirect and retrieved correctly on callback."), ("How do I handle invalid_grant on refresh token?", "Catch the error, clear stored tokens, and redirect the user to the login page. The refresh token is no longer valid — you need a fresh authorization code flow."), ("What causes clock skew in OAuth?", "Your server's system time differs from the auth server's time by more than the allowed window (usually 5 minutes). Sync your server time with an NTP server.")],
        },
        {
            "slug": "fix-redirect-uri-mismatch",
            "title": "Fix OAuth Redirect URI Mismatch Error",
            "description": "The redirect_uri in your request must exactly match the registered URI — including protocol, trailing slash, and every character. Here is how to find and fix mismatches.",
            "content": """
<p class="lead">The redirect_uri in your OAuth request must exactly match the URI registered in your provider dashboard — character for character, including protocol, port, and trailing slash. One difference causes the error.</p>

<div class="error-box"><div class="error-label">OAuth Error Response</div>{"error": "redirect_uri_mismatch", "error_description": "The redirect_uri does not match the registered redirect URIs"}</div>

<h2>Common mismatches</h2>
<table>
  <thead><tr><th>What you sent</th><th>What you registered</th><th>Problem</th></tr></thead>
  <tbody>
    <tr><td>http://localhost:3000</td><td>http://localhost:3000/</td><td>Trailing slash missing</td></tr>
    <tr><td>https://app.example.com</td><td>http://app.example.com</td><td>Protocol mismatch</td></tr>
    <tr><td>https://www.example.com/callback</td><td>https://example.com/callback</td><td>www prefix mismatch</td></tr>
    <tr><td>https://app.example.com/callback?session=1</td><td>https://app.example.com/callback</td><td>Query string not allowed</td></tr>
    <tr><td>https://app.example.com:3000/callback</td><td>https://app.example.com/callback</td><td>Port in URI not registered</td></tr>
  </tbody>
</table>

<h2>How to find your registered URIs per provider</h2>

<h3>Auth0</h3>
<p>Dashboard → Applications → Your App → Settings → Allowed Callback URLs</p>

<h3>Google</h3>
<p>Google Cloud Console → APIs & Services → Credentials → OAuth Client → Authorized redirect URIs</p>

<h3>Okta</h3>
<p>Okta Admin → Applications → Your App → General → Login redirect URIs</p>

<h3>AWS Cognito</h3>
<p>Cognito Console → User Pools → Your Pool → App clients → App client settings → Callback URL(s)</p>

<h2>Fix — match exactly, then add all environments</h2>
<pre>// In your code — log what you are actually sending
const redirectUri = 'https://app.example.com/callback';
console.log('redirect_uri:', redirectUri);

// Build auth URL
const params = new URLSearchParams({
  client_id: 'your-client-id',
  redirect_uri: redirectUri, // must match registered exactly
  response_type: 'code',
  scope: 'openid profile email',
});
window.location.href = `https://auth.example.com/oauth/authorize?${params}`;</pre>

<p>Register all environments you use — development, staging, and production — in the provider dashboard. There is no limit on the number of registered URIs for most providers.</p>""",
            "steps": [("Log the redirect_uri you are sending", "Print the exact value being sent in your authorization request."), ("Compare to registered URIs in provider dashboard", "Check for protocol, port, path, and trailing slash differences."), ("Register all environment URIs", "Add development, staging, and production URIs to your provider's allowed list.")],
            "faqs": [("Does the redirect_uri comparison allow partial matches?", "No. OAuth providers require an exact string match. Some providers like Google support wildcards for localhost in development only."), ("Can I use localhost redirect URIs in production apps?", "No. Localhost URIs are for development only. Register your production domain in the provider dashboard."), ("Can the redirect_uri contain query parameters?", "Most providers do not allow query parameters in registered redirect URIs. Pass state via the state parameter instead.")],
        },
        {
            "slug": "fix-refresh-token-expired",
            "title": "OAuth Refresh Token Expired — How to Handle It",
            "description": "Refresh tokens expire due to inactivity, rotation, or explicit revocation. Here is how to detect expiry and handle it without logging users out unnecessarily.",
            "content": """
<p class="lead">A refresh token expires silently — your app keeps working until the next API call fails with invalid_grant or token_expired. Handle it gracefully: catch the error, clear tokens, redirect to login.</p>

<h2>Why refresh tokens expire</h2>
<ul>
  <li><strong>Inactivity timeout</strong> — providers expire refresh tokens after a period of no use (Auth0 default: 30 days, Cognito: 30 days, Google: 6 months)</li>
  <li><strong>Token rotation</strong> — each refresh produces a new refresh token and invalidates the old one. Using an old token causes invalid_grant</li>
  <li><strong>User revoked access</strong> — the user disconnected your app via provider settings</li>
  <li><strong>Password changed</strong> — some providers revoke all tokens when a password changes</li>
</ul>

<h2>Catch expiry in your token refresh logic</h2>
<pre>async function getValidToken() {
  const stored = getStoredTokens();
  if (!stored) return promptLogin();

  // Check if access token is still valid
  if (Date.now() < stored.expires_at - 60000) {
    return stored.access_token;
  }

  // Try to refresh
  try {
    const fresh = await refreshAccessToken(stored.refresh_token);
    storeTokens(fresh);
    return fresh.access_token;
  } catch (err) {
    if (err.error === 'invalid_grant' || err.status === 401) {
      clearTokens();
      promptLogin(); // redirect to /login
      return null;
    }
    throw err; // re-throw other errors
  }
}</pre>

<h2>Token lifetimes by provider</h2>
<table>
  <thead><tr><th>Provider</th><th>Access token</th><th>Refresh token</th><th>Idle expiry</th></tr></thead>
  <tbody>
    <tr><td>Auth0</td><td>24h (configurable)</td><td>No expiry by default</td><td>30 days idle</td></tr>
    <tr><td>AWS Cognito</td><td>1h</td><td>30 days</td><td>30 days from issue</td></tr>
    <tr><td>Google</td><td>1h</td><td>No expiry</td><td>6 months unused</td></tr>
    <tr><td>Microsoft/Azure</td><td>1h</td><td>90 days</td><td>90 days idle</td></tr>
    <tr><td>Okta</td><td>1h</td><td>Configurable</td><td>Configurable</td></tr>
  </tbody>
</table>

<h2>Silent re-authentication for SPAs</h2>
<p>If you want to avoid visible login prompts, use silent auth — an invisible iframe that attempts to get a new token using a session cookie:</p>
<pre>// Auth0 example — checkSession
auth0.checkSession({}, function(err, result) {
  if (err) {
    // Session expired — full login required
    auth0.authorize();
  } else {
    // New tokens in result
    updateTokens(result);
  }
});</pre>""",
            "steps": [("Detect expiry in your refresh logic", "Catch invalid_grant errors on refresh calls and treat them as session expiry."), ("Clear tokens and redirect", "Remove stored tokens and send the user to the login page."), ("Optionally try silent re-auth", "Use an invisible iframe or prompt=none to attempt re-auth without a visible redirect.")],
            "faqs": [("How do I know when a refresh token will expire?", "Check the expires_in field in the token response and your provider's dashboard settings. Store the expiry time alongside the token."), ("Should I pre-emptively refresh before expiry?", "Yes — refresh the access token 60 seconds before it expires rather than waiting for an API call to fail."), ("What is token rotation?", "Each refresh operation issues a new refresh token and invalidates the old one. If you use a stale refresh token (e.g., from a cached response), you get invalid_grant.")],
        },
        {
            "slug": "fix-google-oauth-invalid-grant",
            "title": "Fix Google OAuth invalid_grant — Service Accounts and Clock Skew",
            "description": "Google rejects JWT assertions if your server clock is off by more than 5 minutes. Here is how to sync time and fix service account OAuth errors.",
            "content": """
<p class="lead">Google OAuth for service accounts uses JWTs with expiry timestamps. If your server clock is off by more than 5 minutes from Google's servers, every token request fails with invalid_grant. Fix your system time first.</p>

<div class="error-box"><div class="error-label">Google API Error Response</div>{"error": "invalid_grant", "error_description": "Invalid JWT: Token must be a short-lived token (60 minutes) and in a reasonable timeframe. Check your iat and exp values and use a clock with skew to account for differences in time."}</div>

<h2>Fix 1 — Sync your server time</h2>
<pre># Check current time offset
date
curl -s --head https://google.com | grep -i date

# Sync immediately (Ubuntu/Debian)
sudo ntpdate -u pool.ntp.org

# Enable automatic sync
sudo timedatectl set-ntp true
timedatectl status  # confirm NTPService: active</pre>

<h2>Fix 2 — Add clock skew tolerance in your JWT</h2>
<pre>import time
import jwt

now = int(time.time())
CLOCK_SKEW = 60  # 60 second buffer

payload = {
    'iss': service_account_email,
    'sub': service_account_email,
    'aud': 'https://oauth2.googleapis.com/token',
    'iat': now - CLOCK_SKEW,  # issued slightly in the past
    'exp': now + 3600 - CLOCK_SKEW,  # expire slightly earlier
    'scope': 'https://www.googleapis.com/auth/...'
}</pre>

<h2>Fix 3 — Rotate service account keys</h2>
<p>Old service account keys do not expire but can be revoked. If you are getting invalid_grant on a key that worked before, check if it was revoked:</p>
<pre># Check key status via gcloud
gcloud iam service-accounts keys list \\
  --iam-account=your-sa@your-project.iam.gserviceaccount.com

# Create a new key if needed
gcloud iam service-accounts keys create new-key.json \\
  --iam-account=your-sa@your-project.iam.gserviceaccount.com</pre>

<h2>Fix 4 — User consent required again</h2>
<p>For user-facing OAuth flows, invalid_grant can mean the user revoked access or Google invalidated the refresh token due to a security event (password change, suspicious activity). Handle it:</p>
<pre>def refresh_google_token(refresh_token):
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    if response.status_code == 400:
        error = response.json()
        if error.get('error') == 'invalid_grant':
            # Redirect user to re-authorize
            raise TokenExpiredError('Google token revoked — re-authorization required')

    return response.json()</pre>""",
            "steps": [("Check server time", "Compare your server time to Google's — more than 5 minutes off causes invalid_grant."), ("Sync NTP", "Run ntpdate or enable timedatectl set-ntp to keep time synchronized."), ("Rotate service account keys if needed", "Check if your key was revoked in the GCP console and create a new one.")],
            "faqs": [("How much clock skew does Google tolerate?", "Google allows up to 5 minutes (300 seconds) of clock skew. More than that and JWT assertions are rejected with invalid_grant."), ("How do I check if my service account key is still valid?", "Use gcloud iam service-accounts keys list to see key status. Keys marked as INVALID or not listed are revoked."), ("Can Google revoke OAuth tokens automatically?", "Yes — Google may revoke tokens when a user changes their password, revokes access, or when Google detects suspicious activity.")],
        },
        {
            "slug": "fix-pkce-errors",
            "title": "OAuth PKCE Flow Errors — Fix code_challenge and code_verifier",
            "description": "PKCE errors almost always mean a verifier mismatch. Here is how PKCE works and the three most common implementation bugs.",
            "content": """
<p class="lead">PKCE errors are almost always caused by a code_verifier that does not match the code_challenge you sent in the authorization request. Here is how the flow works and where it typically breaks.</p>

<div class="error-box"><div class="error-label">OAuth Error Response</div>{"error": "invalid_grant", "error_description": "PKCE verification failed"}</div>

<h2>How PKCE works</h2>
<pre>// Step 1 — Generate a random verifier (before redirect)
function generateVerifier() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64URLEncode(array);
}

// Step 2 — Generate challenge from verifier
async function generateChallenge(verifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return base64URLEncode(new Uint8Array(digest));
}

function base64URLEncode(array) {
  return btoa(String.fromCharCode(...array))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}</pre>

<h2>Step 3 — Authorization request with challenge</h2>
<pre>const verifier = generateVerifier();
sessionStorage.setItem('pkce_verifier', verifier); // STORE IT

const challenge = await generateChallenge(verifier);

const params = new URLSearchParams({
  client_id: CLIENT_ID,
  redirect_uri: REDIRECT_URI,
  response_type: 'code',
  scope: 'openid profile',
  code_challenge: challenge,
  code_challenge_method: 'S256',
  state: generateState(),
});

window.location.href = `${AUTH_URL}?${params}`;</pre>

<h2>Step 4 — Token exchange with verifier</h2>
<pre>// On callback page
const verifier = sessionStorage.getItem('pkce_verifier'); // RETRIEVE IT

const tokens = await fetch(TOKEN_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    code: authorizationCode,
    code_verifier: verifier, // must match original
  }),
}).then(r => r.json());</pre>

<h2>Common bugs</h2>
<table>
  <thead><tr><th>Bug</th><th>Symptom</th><th>Fix</th></tr></thead>
  <tbody>
    <tr><td>Verifier not stored before redirect</td><td>sessionStorage empty on callback</td><td>Store before window.location.href</td></tr>
    <tr><td>Wrong hash method</td><td>Challenge does not match</td><td>Always use SHA-256, not plain</td></tr>
    <tr><td>Wrong base64 encoding</td><td>Challenge character mismatch</td><td>Use base64url (- and _ not + and /), no padding</td></tr>
    <tr><td>Verifier regenerated on callback</td><td>New verifier does not match original challenge</td><td>Read from storage, do not regenerate</td></tr>
  </tbody>
</table>""",
            "steps": [("Generate verifier before redirect", "Create a random 32-byte string and store it in sessionStorage before redirecting to the auth server."), ("Compute SHA-256 challenge", "Hash the verifier using SHA-256 and base64url encode it (no padding, - and _ instead of + and /)."), ("Send verifier on token exchange", "Retrieve the stored verifier from sessionStorage and include it in the token request as code_verifier.")],
            "faqs": [("What is PKCE?", "Proof Key for Code Exchange — an OAuth extension that prevents authorization code interception. Required for public clients like SPAs and mobile apps."), ("What is the difference between code_challenge and code_verifier?", "The verifier is a random secret you generate. The challenge is a SHA-256 hash of the verifier. You send the challenge with the auth request and the verifier with the token exchange."), ("Why does my PKCE implementation fail only sometimes?", "Usually a race condition — the callback page loads before sessionStorage is populated. Or React re-renders the callback component, regenerating the verifier.")],
        },
    ]

    for art in articles:
        write(f"blog/oauth/{art['slug']}/index.html", template(
            title=art["title"],
            description=art["description"],
            canonical=f"{BASE_URL}/blog/oauth/{art['slug']}/",
            schema=make_schema(art["title"], art["description"], f"{BASE_URL}/blog/oauth/{art['slug']}/", art["steps"], art["faqs"]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/oauth/">OAuth</a> → {art["title"]}',
            tag="OAuth", tag_color=ORANGE_TAG,
            h1=art["title"],
            content=art["content"],
            cta_url="/oauth/", cta_text="Debug your OAuth error live → OAuthFixer",
            related='<a href="/glossary/pkce/">What is PKCE?</a> <a href="/glossary/oauth-grant-types/">OAuth grant types</a> <a href="/error/invalid-grant/">invalid_grant error</a>'
        ))


# ─── BATCH 4: HEADERS FIX GUIDES ─────────────────────────────────────────────

def batch4_headers():
    print("\n📦 Batch 4 — Headers Fix Guides")

    articles = [
        {
            "slug": "security-headers-checklist",
            "title": "HTTP Security Headers Checklist — What Every Site Needs",
            "description": "Nine security headers every production site should have, with the exact config for Nginx, Apache, Vercel, and Cloudflare.",
            "content": """
<p class="lead">Most web servers ship with no security headers by default. These nine headers take 30 minutes to add and protect against clickjacking, XSS, MIME sniffing, and forced downgrade attacks.</p>

<h2>1. Strict-Transport-Security (HSTS)</h2>
<p>Tells browsers to only connect via HTTPS for the specified duration. Prevents SSL stripping attacks.</p>
<pre>Strict-Transport-Security: max-age=31536000; includeSubDomains; preload</pre>
<p>Only add this if HTTPS is fully working. If you add HSTS and HTTPS breaks, users cannot access your site for the duration of max-age.</p>

<h2>2. Content-Security-Policy (CSP)</h2>
<p>Defines which resources are allowed to load. The most powerful XSS mitigation available.</p>
<pre>Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none'; object-src 'none';</pre>

<h2>3. X-Frame-Options</h2>
<p>Prevents your page from being embedded in iframes on other sites. Blocks clickjacking attacks.</p>
<pre>X-Frame-Options: SAMEORIGIN</pre>

<h2>4. X-Content-Type-Options</h2>
<p>Prevents browsers from guessing the content type of a response. One line, no configuration needed.</p>
<pre>X-Content-Type-Options: nosniff</pre>

<h2>5. Referrer-Policy</h2>
<p>Controls how much URL information is sent to third-party sites when users click links from your page.</p>
<pre>Referrer-Policy: strict-origin-when-cross-origin</pre>

<h2>6. Permissions-Policy</h2>
<p>Restricts which browser features your page (and embedded iframes) can use.</p>
<pre>Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()</pre>

<h2>7. Cross-Origin-Opener-Policy (COOP)</h2>
<p>Isolates your page from cross-origin popups. Required for SharedArrayBuffer and Spectre mitigations.</p>
<pre>Cross-Origin-Opener-Policy: same-origin</pre>

<h2>8. Cross-Origin-Embedder-Policy (COEP)</h2>
<p>Required alongside COOP for cross-origin isolation. Needed for SharedArrayBuffer and high-resolution timers.</p>
<pre>Cross-Origin-Embedder-Policy: require-corp</pre>

<h2>9. Remove Server header</h2>
<p>The Server header reveals your web server software and version. Remove it or set it to something generic.</p>
<pre># Nginx
server_tokens off;

# Apache
ServerTokens Prod
ServerSignature Off</pre>

<h2>Quick config for Nginx</h2>
<pre>add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
add_header Cross-Origin-Opener-Policy "same-origin" always;
server_tokens off;</pre>

<p>Use HeadersFixer to scan your live site and see which of these are missing or misconfigured — it generates the exact config for your specific stack.</p>""",
            "steps": [("Scan your current headers", "Use HeadersFixer to see which security headers are missing from your site."), ("Add missing headers to your server config", "Copy the generated config for your stack — Nginx, Apache, Vercel, or Cloudflare."), ("Re-scan to verify", "Confirm all headers are present after deploying.")],
            "faqs": [("Which security header is most important?", "Strict-Transport-Security if your site is HTTPS-only. Content-Security-Policy for XSS protection. X-Frame-Options for clickjacking. All three are essential for production sites."), ("Will adding security headers break my site?", "X-Content-Type-Options, Referrer-Policy, and Permissions-Policy are safe to add immediately. HSTS and CSP require testing — start with report-only mode for CSP."), ("Do I need COOP and COEP?", "Only if you use SharedArrayBuffer, high-resolution timers, or want Spectre mitigations. For most sites, HSTS, CSP, X-Frame-Options, and X-Content-Type-Options are the priority.")],
        },
        {
            "slug": "fix-x-frame-options",
            "title": "Fix Missing X-Frame-Options — Clickjacking Protection",
            "description": "X-Frame-Options prevents your page from being embedded in iframes on other sites. Missing it leaves you open to clickjacking attacks. Here is the fix for every stack.",
            "content": """
<p class="lead">Without X-Frame-Options, attackers can embed your page in an invisible iframe and trick users into clicking things they cannot see. One header line fixes it.</p>

<h2>What clickjacking looks like</h2>
<p>An attacker creates a page that embeds your site in a transparent iframe positioned exactly over a button on their page. The user thinks they are clicking the attacker's button but they are actually clicking on your site — transferring money, changing settings, or approving actions.</p>

<h2>The fix by stack</h2>

<h3>Nginx</h3>
<pre>add_header X-Frame-Options "SAMEORIGIN" always;</pre>

<h3>Apache</h3>
<pre>Header always set X-Frame-Options "SAMEORIGIN"</pre>

<h3>Express</h3>
<pre>const helmet = require('helmet');
app.use(helmet.frameguard({ action: 'sameorigin' }));</pre>

<h3>Vercel (vercel.json)</h3>
<pre>{
  "headers": [{ "source": "/(.*)", "headers": [
    { "key": "X-Frame-Options", "value": "SAMEORIGIN" }
  ]}]
}</pre>

<h3>Cloudflare Transform Rules</h3>
<p>Workers → Transform Rules → Response Headers → Add header: X-Frame-Options = SAMEORIGIN</p>

<h2>SAMEORIGIN vs DENY</h2>
<table>
  <thead><tr><th>Value</th><th>Allows</th><th>Use when</th></tr></thead>
  <tbody>
    <tr><td>SAMEORIGIN</td><td>Your own domain can embed the page</td><td>You have admin panels or embedded pages on the same domain</td></tr>
    <tr><td>DENY</td><td>No one can embed the page</td><td>Login pages, checkout, any page where embedding should never happen</td></tr>
  </tbody>
</table>

<h2>X-Frame-Options vs CSP frame-ancestors</h2>
<p>CSP <code>frame-ancestors</code> is the modern replacement for X-Frame-Options. It is more flexible (supports multiple origins) and takes precedence when both are set. Use both for maximum browser compatibility:</p>
<pre># Nginx — both for full coverage
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Content-Security-Policy "frame-ancestors 'self';" always;</pre>

<p>When both are present, browsers that support CSP use frame-ancestors and ignore X-Frame-Options. Older browsers fall back to X-Frame-Options.</p>""",
            "steps": [("Add X-Frame-Options header", "Set X-Frame-Options: SAMEORIGIN in your server config."), ("Also add CSP frame-ancestors", "Modern browsers use frame-ancestors from your Content-Security-Policy when both are present."), ("Verify with HeadersFixer", "Scan your live site to confirm the header is being sent correctly.")],
            "faqs": [("What is the difference between SAMEORIGIN and DENY?", "SAMEORIGIN allows your own domain to embed the page. DENY blocks embedding by anyone including your own domain. Use DENY for login pages and sensitive actions."), ("Is X-Frame-Options still needed if I have CSP?", "Yes — X-Frame-Options covers older browsers that do not support CSP frame-ancestors. Use both."), ("Can X-Frame-Options allow multiple origins?", "No — X-Frame-Options only supports SAMEORIGIN or DENY. For multiple allowed origins, use CSP frame-ancestors: frame-ancestors 'self' https://trusted-partner.com.")],
        },
        {
            "slug": "fix-hsts",
            "title": "HSTS Not Working — Fix HTTP Strict Transport Security",
            "description": "HSTS tells browsers to only connect via HTTPS. Common problems: wrong max-age, applied to HTTP response, or missing includeSubDomains. Here is how to debug and fix each.",
            "content": """
<p class="lead">HSTS only works when browsers receive it over HTTPS. If your site is sending it over HTTP, browsers ignore it. If max-age is 0 or very short, browsers discard it immediately.</p>

<h2>The correct HSTS header</h2>
<pre>Strict-Transport-Security: max-age=31536000; includeSubDomains; preload</pre>

<h2>Common mistakes</h2>

<h3>Mistake 1 — Applied to HTTP responses</h3>
<p>Browsers only process HSTS headers received over HTTPS. If your HTTP (port 80) virtual host also sets HSTS, browsers ignore it. The header must come from an HTTPS response.</p>
<pre># Nginx — correct: only set HSTS in SSL server block
server {
    listen 80;
    return 301 https://$host$request_uri; # no HSTS here
}

server {
    listen 443 ssl;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    # HSTS goes here, in the HTTPS block
}</pre>

<h3>Mistake 2 — max-age too short</h3>
<p>If max-age is 0, browsers delete the HSTS record immediately. Very short values (less than a week) provide minimal protection. The recommended value is 31536000 (1 year).</p>

<h3>Mistake 3 — Missing includeSubDomains</h3>
<p>Without <code>includeSubDomains</code>, attackers can intercept connections to subdomains (like staging.example.com) and use them to attack users. Add it if all your subdomains support HTTPS.</p>

<h3>Mistake 4 — Adding before HTTPS works fully</h3>
<p>If you add HSTS before your SSL certificate is fully configured, users who visit will be locked out until max-age expires. Test HTTPS thoroughly before adding the header.</p>

<h2>Config by stack</h2>

<h3>Nginx</h3>
<pre>server {
    listen 443 ssl http2;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
}</pre>

<h3>Apache</h3>
<pre>Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"</pre>

<h3>Express</h3>
<pre>const helmet = require('helmet');
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));</pre>

<h2>HSTS preload</h2>
<p>The preload flag signals that you want your domain added to browsers' built-in HSTS lists — meaning HTTPS is enforced even on the first visit before the browser has ever seen your header. Submit at <a href="https://hstspreload.org" style="color:var(--purple)">hstspreload.org</a> once HSTS is working correctly.</p>""",
            "steps": [("Verify HSTS is sent over HTTPS only", "Check that your HTTP server block redirects to HTTPS and does not set the HSTS header."), ("Set max-age to at least 1 year", "Use max-age=31536000 (1 year). Lower values provide minimal protection."), ("Add includeSubDomains if all subdomains support HTTPS", "Without it, attackers can intercept subdomain connections.")],
            "faqs": [("Why is HSTS not showing in my browser?", "Check that it is being sent over HTTPS (not HTTP) and that max-age is not 0. Use HeadersFixer to verify the header is present and correctly formatted."), ("Can I remove HSTS once I have added it?", "Set max-age=0 to signal to browsers that they should delete the HSTS record. But they need to receive this over HTTPS first — so you cannot remove it if HTTPS breaks."), ("What is the HSTS preload list?", "A list built into Chrome, Firefox, and Safari of domains that should always use HTTPS. Being on it means HTTPS is enforced even on the first ever visit. Submit at hstspreload.org.")],
        },
    ]

    for art in articles:
        write(f"blog/headers/{art['slug']}/index.html", template(
            title=art["title"],
            description=art["description"],
            canonical=f"{BASE_URL}/blog/headers/{art['slug']}/",
            schema=make_schema(art["title"], art["description"], f"{BASE_URL}/blog/headers/{art['slug']}/", art["steps"], art["faqs"]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/headers/">Headers</a> → {art["title"]}',
            tag="Headers", tag_color=RED_TAG,
            h1=art["title"],
            content=art["content"],
            cta_url="/", cta_text="Scan your security headers live → HeadersFixer",
            related='<a href="/glossary/hsts/">What is HSTS?</a> <a href="/glossary/content-security-policy/">What is CSP?</a> <a href="/fix/headers/nginx/">Nginx headers fix</a>'
        ))


# ─── BATCH 5: PERFORMANCE GUIDES ─────────────────────────────────────────────

def batch5_performance():
    print("\n📦 Batch 5 — Performance Guides")

    articles = [
        {
            "slug": "fix-ttfb-vercel",
            "title": "Fix Slow TTFB on Vercel — Edge Functions vs Serverless",
            "description": "TTFB over 600ms is a server problem. On Vercel, the main cause is cold starts on serverless functions. Here is how to move to Edge Runtime and cache aggressively.",
            "content": """
<p class="lead">TTFB over 600ms is almost always a server problem, not a frontend problem. On Vercel, the main cause is cold starts on serverless Node.js functions. Moving to Edge Runtime eliminates them.</p>

<h2>Diagnose first</h2>
<p>Open DevTools → Network → click your document request → Timing tab. If TTFB (Waiting for server response) is high, the problem is server-side. If TTFB is fine but the page is slow, the problem is rendering or resources.</p>

<h2>Cause 1 — Serverless cold starts</h2>
<p>Vercel serverless functions spin down after inactivity. The first request after a cold period takes 500-2000ms extra for the container to start.</p>
<pre>// Move to Edge Runtime — no cold starts, runs globally
// app/api/data/route.ts (App Router)
export const runtime = 'edge';

export async function GET(request: Request) {
  return Response.json({ data: 'fast' });
}</pre>

<p>Edge Runtime has limitations: no Node.js APIs, no filesystem access, smaller bundle size limit. If you need Node.js APIs, use edge middleware for the fast parts and defer heavy work to serverless.</p>

<h2>Cause 2 — No caching</h2>
<p>If your function fetches from a database or external API on every request, add caching at the function level:</p>
<pre>// App Router — cache at the fetch level
export async function GET() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 } // cache for 60 seconds
  });
  return Response.json(await data.json());
}

// Or use unstable_cache for fine-grained control
import { unstable_cache } from 'next/cache';

const getCachedData = unstable_cache(
  async () => fetchFromDB(),
  ['data-cache-key'],
  { revalidate: 3600 }
);</pre>

<h2>Cause 3 — Function not deployed at the right region</h2>
<p>Serverless functions deploy to a single region by default. If your users are in Europe and your function is in US East, add 100-200ms of latency.</p>
<pre>// vercel.json — set function region
{
  "functions": {
    "api/**/*.js": {
      "regions": ["fra1", "lhr1"]  // Frankfurt, London
    }
  }
}</pre>

<h2>Cache static pages at the CDN</h2>
<p>For pages that do not change per user, set Cache-Control to let Vercel's CDN serve them without hitting the function:</p>
<pre>// Next.js — set cache headers in route
export async function GET() {
  return new Response(JSON.stringify({ data: 'ok' }), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}</pre>""",
            "steps": [("Check TTFB in DevTools Network tab", "If TTFB is high, the problem is server-side — not frontend."), ("Move to Edge Runtime", "Add export const runtime = 'edge' to eliminate cold starts."), ("Add caching for database and API calls", "Use next: { revalidate } on fetch calls or unstable_cache for function-level caching.")],
            "faqs": [("What is a good TTFB?", "Under 200ms is good. Under 600ms is acceptable. Over 600ms needs investigation. Google PageSpeed flags TTFB over 600ms as a problem."), ("When should I use Edge Runtime vs Node.js?", "Edge Runtime for fast, stateless responses with no Node.js dependencies. Node.js for database connections, file system access, or npm packages that require Node.js APIs."), ("Does Vercel's free tier support Edge Runtime?", "Yes — Edge Runtime is available on all Vercel plans including free.")],
        },
        {
            "slug": "fix-cache-control-cdn",
            "title": "Fix Cache-Control Headers — Why Your CDN Isn't Caching",
            "description": "Missing Cache-Control means your CDN treats every response as uncacheable. Here is the right Cache-Control for static assets, API responses, and HTML pages.",
            "content": """
<p class="lead">If Cache-Control is missing, CDNs default to not caching — or make inconsistent decisions based on other headers. Explicit Cache-Control headers give you full control over what gets cached and for how long.</p>

<h2>Check your current headers first</h2>
<pre>curl -I https://yoursite.com/
curl -I https://yoursite.com/static/app.js
curl -I https://yoursite.com/api/data</pre>

<p>If you see no Cache-Control or <code>Cache-Control: no-cache</code> on static assets, your CDN is not caching them — every request goes to your origin server.</p>

<h2>Cache-Control by resource type</h2>

<h3>Versioned static assets (JS, CSS, fonts)</h3>
<p>These have content hashes in the filename (app.abc123.js). The content never changes, so cache them forever:</p>
<pre>Cache-Control: public, max-age=31536000, immutable</pre>
<p><code>immutable</code> tells browsers not to revalidate during max-age, even on back/forward navigation. Removes unnecessary conditional requests.</p>

<h3>Non-versioned static assets (images, logo.png)</h3>
<p>Cache for a week or month, but allow revalidation:</p>
<pre>Cache-Control: public, max-age=604800, stale-while-revalidate=86400</pre>

<h3>HTML pages</h3>
<p>Cache briefly or not at all — HTML references your versioned assets, so you need users to get fresh HTML when you deploy:</p>
<pre># Option 1 — no CDN cache (always fresh)
Cache-Control: public, max-age=0, must-revalidate

# Option 2 — CDN cache with instant invalidation
Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400</pre>

<h3>API responses (non-authenticated)</h3>
<pre># Cache for 60 seconds at CDN, serve stale for 24h while revalidating
Cache-Control: public, s-maxage=60, stale-while-revalidate=86400</pre>

<h3>API responses (authenticated)</h3>
<pre># Never cache at CDN — must use private
Cache-Control: private, no-store</pre>

<h2>Config by stack</h2>

<h3>Nginx</h3>
<pre>location ~* \.(js|css|woff2|png|jpg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, max-age=31536000, immutable" always;
}

location ~* \.html$ {
    add_header Cache-Control "public, max-age=0, must-revalidate" always;
}</pre>

<h3>Vercel (vercel.json)</h3>
<pre>{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    },
    {
      "source": "/(.*\\.html)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }]
    }
  ]
}</pre>

<h3>Cloudflare</h3>
<p>Cloudflare Dashboard → Caching → Cache Rules → Create rule → File extension matches js,css,png,jpg,woff2 → Edge Cache TTL: 1 year.</p>

<p>Use EdgeFix to audit your current caching headers and see exactly what the CDN is receiving for each resource type.</p>""",
            "steps": [("Audit current Cache-Control headers", "Use curl -I or EdgeFix to see what Cache-Control headers your server is sending."), ("Set long cache for versioned assets", "Use max-age=31536000 and immutable for JS and CSS files with content hashes."), ("Set short cache or no-store for API responses", "Never cache authenticated API responses at the CDN. Use private, no-store.")],
            "faqs": [("What is the difference between max-age and s-maxage?", "max-age applies to browser caching. s-maxage applies to CDN (shared) caching. Use s-maxage when you want different caching rules for the browser vs the CDN."), ("What does stale-while-revalidate do?", "Tells the CDN to serve a stale cached response immediately while fetching a fresh one in the background. Eliminates the user-visible wait during cache refresh."), ("What does immutable mean in Cache-Control?", "Tells browsers not to revalidate the resource during max-age, even during back/forward navigation. Only use it for truly immutable resources with content hashes.")],
        },
        {
            "slug": "fix-mixed-content",
            "title": "Fix Mixed Content Warnings — HTTP Resources on HTTPS Sites",
            "description": "Mixed content happens when an HTTPS page loads resources over HTTP. Active mixed content is blocked. Passive is warned. Here is how to find and fix all instances.",
            "content": """
<p class="lead">Your page loads over HTTPS but some resources — scripts, images, API calls — are requested over HTTP. Browsers block scripts and iframes (active mixed content) and warn about images and videos (passive mixed content). Here is how to find and fix all of them.</p>

<div class="error-box"><div class="error-label">Browser Console Error</div>Mixed Content: The page at 'https://example.com' was loaded over HTTPS, but requested an insecure resource 'http://cdn.example.com/script.js'. This request has been blocked; the content must be served over HTTPS.</div>

<h2>Find all mixed content</h2>
<p>Open DevTools → Console. Look for "Mixed Content" errors. Each one tells you the exact URL being loaded over HTTP. You can also use CSPFixer to scan your page and enumerate all resource URLs.</p>

<h2>Quick fix — upgrade-insecure-requests</h2>
<p>The fastest fix: tell the browser to upgrade all HTTP requests to HTTPS automatically:</p>
<pre>Content-Security-Policy: upgrade-insecure-requests;</pre>

<p>This only works if the resource actually exists over HTTPS. If http://cdn.example.com/file.js cannot be loaded as https://cdn.example.com/file.js (wrong certificate, does not exist), it will fail.</p>

<h2>Proper fix — update hardcoded URLs</h2>

<h3>In HTML</h3>
<pre>&lt;!-- Wrong --&gt;
&lt;script src="http://cdn.example.com/script.js"&gt;&lt;/script&gt;
&lt;img src="http://images.example.com/photo.jpg"&gt;

&lt;!-- Right --&gt;
&lt;script src="https://cdn.example.com/script.js"&gt;&lt;/script&gt;
&lt;img src="https://images.example.com/photo.jpg"&gt;

&lt;!-- Protocol-relative (works for both HTTP and HTTPS) --&gt;
&lt;script src="//cdn.example.com/script.js"&gt;&lt;/script&gt;</pre>

<h3>In CSS</h3>
<pre>/* Wrong */
background-image: url('http://images.example.com/bg.png');

/* Right */
background-image: url('https://images.example.com/bg.png');</pre>

<h3>In JavaScript fetch calls</h3>
<pre>// Wrong
fetch('http://api.example.com/data')

// Right
fetch('https://api.example.com/data')

// Or use a relative URL if same domain
fetch('/api/data')</pre>

<h2>In WordPress</h2>
<p>Mixed content in WordPress often comes from hardcoded HTTP URLs in the database (posts, options, theme settings). Use a plugin like Better Search Replace to update all URLs:</p>
<pre>-- Or with WP-CLI:
wp search-replace 'http://example.com' 'https://example.com' --all-tables</pre>

<h2>Verify all resources are now HTTPS</h2>
<p>After fixing, open DevTools Console and reload. All Mixed Content warnings should be gone. Use CSPFixer to do a full scan of your page resources to confirm no HTTP URLs remain.</p>""",
            "steps": [("Find mixed content in DevTools Console", "Look for Mixed Content errors that show the exact HTTP URLs being loaded."), ("Add upgrade-insecure-requests to CSP", "This upgrades HTTP to HTTPS automatically for resources that exist on both protocols."), ("Update hardcoded HTTP URLs", "Find and replace http:// with https:// in HTML, CSS, JavaScript, and database content.")],
            "faqs": [("What is the difference between active and passive mixed content?", "Active mixed content (scripts, iframes, stylesheets) is blocked by browsers — it can control your entire page. Passive mixed content (images, audio, video) shows warnings but is not blocked."), ("Does upgrade-insecure-requests fix all mixed content?", "It fixes resources that are available over HTTPS. If a resource only exists on HTTP, the request will fail. You still need to fix hardcoded HTTP URLs for resources that are HTTP-only."), ("How do I find mixed content in WordPress?", "Use Better Search Replace plugin or WP-CLI wp search-replace to find all http:// occurrences in the database. Also check theme files and plugins for hardcoded URLs.")],
        },
    ]

    for art in articles:
        write(f"blog/performance/{art['slug']}/index.html", template(
            title=art["title"],
            description=art["description"],
            canonical=f"{BASE_URL}/blog/performance/{art['slug']}/",
            schema=make_schema(art["title"], art["description"], f"{BASE_URL}/blog/performance/{art['slug']}/", art["steps"], art["faqs"]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/performance/">Performance</a> → {art["title"]}',
            tag="Performance", tag_color=ORANGE_TAG,
            h1=art["title"],
            content=art["content"],
            cta_url="/speedfixer/", cta_text="Run a live PageSpeed audit → SpeedFixer",
            related='<a href="/glossary/cache-control/">Cache-Control header</a> <a href="/glossary/core-web-vitals/">Core Web Vitals</a> <a href="/edge/">EdgeFix — cache auditor</a>'
        ))


# ─── BATCH 6: EXPLAINER PAGES ─────────────────────────────────────────────────

def batch6_explainers():
    print("\n📦 Batch 6 — Explainer Pages")

    articles = [
        ("what-is-cors", "What is CORS? A Plain English Explanation", "CORS", PURPLE_TAG,
         "CORS lets web pages make requests to different domains. Without it, your frontend and backend on different domains cannot talk. Here is how it actually works.",
         "/cors/", "Test your CORS config → CORSFixer",
         '<a href="/glossary/cors/">CORS glossary</a> <a href="/glossary/preflight-request/">Preflight requests</a> <a href="/blog/cors/fix-cors-express/">Fix CORS in Express</a>',
         """
<p class="lead">Browsers block requests from one domain to another by default. CORS is the mechanism that lets servers say "yes, requests from this other domain are allowed." Without it, your React frontend on app.example.com cannot call your API on api.example.com.</p>

<h2>The same-origin policy</h2>
<p>Browsers enforce the same-origin policy: JavaScript on page A can only make requests to the same origin as page A. Origin = protocol + hostname + port. https://app.example.com and https://api.example.com are different origins — even though they share the same domain.</p>

<h2>What CORS does</h2>
<p>CORS (Cross-Origin Resource Sharing) is a system where servers include response headers that tell the browser which cross-origin requests are allowed. The browser checks these headers and decides whether to let JavaScript read the response.</p>

<pre># Server response includes:
Access-Control-Allow-Origin: https://app.example.com

# Browser sees this and allows JavaScript to read the response
# Without it, the browser blocks the response even if the server returned 200</pre>

<h2>How a simple CORS request works</h2>
<ol>
  <li>JavaScript on app.example.com calls fetch('https://api.example.com/data')</li>
  <li>Browser adds Origin: https://app.example.com to the request</li>
  <li>Server processes the request normally and returns a response</li>
  <li>Browser checks the response for Access-Control-Allow-Origin</li>
  <li>If the origin matches, browser gives the response to JavaScript. If not, browser blocks it.</li>
</ol>

<h2>The preflight request</h2>
<p>For non-simple requests (POST with JSON, PUT, DELETE, or requests with custom headers like Authorization), the browser first sends an OPTIONS request to check permission. Only if the server responds correctly does the browser send the actual request.</p>

<pre>OPTIONS /api/data HTTP/1.1
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Authorization, Content-Type

# Server must respond:
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
# HTTP 204</pre>

<h2>Common misconceptions</h2>
<ul>
  <li><strong>CORS is not a security feature for your server</strong> — it is enforced by the browser. Server-side tools (curl, Postman, backend code) bypass it entirely.</li>
  <li><strong>CORS errors are not server errors</strong> — the server processes and responds to the request. The browser blocks the response from reaching JavaScript.</li>
  <li><strong>CORS does not protect your API</strong> — it protects users from malicious websites making requests in their browser. Use authentication to protect your API.</li>
</ul>"""),

        ("what-is-csp", "What is a Content Security Policy? CSP Explained", "CSP", GREEN_TAG,
         "CSP is a browser security mechanism that tells the browser which resources are allowed to load. Here is how it works and why unsafe-inline defeats it.",
         "/csp/", "Generate a CSP for your page → CSPFixer",
         '<a href="/glossary/content-security-policy/">CSP glossary</a> <a href="/glossary/unsafe-inline/">unsafe-inline</a> <a href="/blog/csp/fix-csp-nextjs/">CSP in Next.js</a>',
         """
<p class="lead">XSS attacks work by injecting scripts into your page. CSP is a browser-enforced allowlist that controls which scripts, styles, and resources are allowed to run — blocking injected scripts even if they get into your HTML.</p>

<h2>The problem CSP solves</h2>
<p>Without CSP, if an attacker finds a way to inject <code>&lt;script src="https://evil.com/steal.js"&gt;&lt;/script&gt;</code> into your page, the browser runs it. With CSP, the browser checks if evil.com is in your allowlist — it is not, so the script is blocked.</p>

<h2>How CSP works</h2>
<p>Your server sends a Content-Security-Policy header with directives that define what is allowed. The browser enforces them when loading the page.</p>

<pre>Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://trusted-cdn.com;
  style-src 'self' https://fonts.googleapis.com;
  img-src 'self' data: https:;
  frame-ancestors 'none';
  object-src 'none';</pre>

<h2>The main directives</h2>
<table>
  <thead><tr><th>Directive</th><th>Controls</th></tr></thead>
  <tbody>
    <tr><td>default-src</td><td>Fallback for all resource types not explicitly listed</td></tr>
    <tr><td>script-src</td><td>JavaScript files and inline scripts</td></tr>
    <tr><td>style-src</td><td>CSS files and inline styles</td></tr>
    <tr><td>img-src</td><td>Images</td></tr>
    <tr><td>connect-src</td><td>XHR, fetch, WebSocket connections</td></tr>
    <tr><td>font-src</td><td>Font files</td></tr>
    <tr><td>frame-src</td><td>Iframes your page loads</td></tr>
    <tr><td>frame-ancestors</td><td>Who can embed your page in an iframe</td></tr>
    <tr><td>object-src</td><td>Plugins (Flash etc) — set to none</td></tr>
  </tbody>
</table>

<h2>Why unsafe-inline defeats CSP</h2>
<p>Adding <code>'unsafe-inline'</code> to script-src allows any inline script to run — including injected ones. It fixes the "inline script blocked" error but removes all XSS protection. Use nonces instead.</p>

<h2>Start with report-only mode</h2>
<p>Use <code>Content-Security-Policy-Report-Only</code> to test your policy without blocking anything. Violations appear in the browser console, letting you build your allowlist before enforcing.</p>

<pre>Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self';</pre>"""),

        ("what-is-oauth", "What is OAuth 2.0? How It Actually Works", "OAuth", ORANGE_TAG,
         "OAuth 2.0 lets your app access a user's data on another service without their password. Here is how the authorization code flow works step by step.",
         "/oauth/", "Debug your OAuth errors → OAuthFixer",
         '<a href="/glossary/pkce/">PKCE explained</a> <a href="/glossary/oauth-grant-types/">Grant types</a> <a href="/blog/oauth/fix-invalid-grant/">Fix invalid_grant</a>',
         """
<p class="lead">OAuth lets your app access a user's data on another service without their password. Instead of entering credentials into your app, users log in at the service directly — and that service gives your app a limited-access token.</p>

<h2>The parking valet analogy</h2>
<p>Giving a parking valet your house key along with your car key would be stupid. Valet keys exist — they unlock the car but not the house, and some disable the trunk. OAuth is the valet key for APIs: limited access to specific resources, without exposing full credentials.</p>

<h2>The authorization code flow (most common)</h2>
<ol>
  <li><strong>Your app redirects the user to the auth server</strong> — with client_id, redirect_uri, scope, and a PKCE code challenge</li>
  <li><strong>User logs in at the auth server</strong> — your app never sees their password</li>
  <li><strong>Auth server redirects back to your app</strong> — with a short-lived authorization code in the URL</li>
  <li><strong>Your app exchanges the code for tokens</strong> — POST to /token with the code and PKCE verifier</li>
  <li><strong>Auth server returns access token and refresh token</strong></li>
  <li><strong>Your app uses the access token</strong> — in the Authorization header of API calls</li>
</ol>

<pre>// Step 1 — Redirect user
const authUrl = `https://auth.example.com/authorize?
  client_id=YOUR_CLIENT_ID&
  redirect_uri=https://yourapp.com/callback&
  response_type=code&
  scope=openid profile email&
  code_challenge=${challenge}&
  code_challenge_method=S256`;

window.location.href = authUrl;

// Step 4 — Exchange code for tokens (on callback)
const tokens = await fetch('https://auth.example.com/token', {
  method: 'POST',
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: 'https://yourapp.com/callback',
    client_id: 'YOUR_CLIENT_ID',
    code_verifier: storedVerifier,
  })
}).then(r => r.json());</pre>

<h2>OAuth vs OpenID Connect</h2>
<p>OAuth is authorization — "can this app access your data?" OpenID Connect (OIDC) adds authentication — "who are you?" — by adding an ID token to the OAuth flow. When you use "Sign in with Google," that is OIDC on top of OAuth.</p>

<h2>Why PKCE exists</h2>
<p>Authorization codes in the URL can be stolen by malicious browser extensions or apps. PKCE (Proof Key for Code Exchange) adds a verifier that proves the entity exchanging the code is the same one that started the flow. Required for SPAs and mobile apps.</p>"""),

        ("what-is-preflight", "What is a Preflight Request? Why Browsers Send OPTIONS First", "CORS", PURPLE_TAG,
         "A preflight is an OPTIONS request the browser sends before a cross-origin POST, PUT, or DELETE. Your server must handle it or the actual request never runs.",
         "/cors/", "Test your preflight response → CORSFixer",
         '<a href="/glossary/preflight-request/">Preflight glossary</a> <a href="/glossary/cors/">What is CORS?</a> <a href="/blog/cors/fix-cors-preflight-options/">Fix failing preflights</a>',
         """
<p class="lead">Before sending a cross-origin POST, PUT, DELETE, or any request with custom headers, the browser first asks for permission with an OPTIONS request. If your server does not respond correctly, the actual request never runs.</p>

<h2>Why preflights exist</h2>
<p>Simple GET requests (like loading an image from another domain) were already possible before CORS existed — via HTML img tags. For more complex requests that can have side effects (POST, PUT, DELETE), browsers add a safety check: ask the server first before sending data.</p>

<h2>What triggers a preflight</h2>
<p>You get a preflight when a cross-origin request uses:</p>
<ul>
  <li>Method: PUT, DELETE, PATCH (POST only triggers preflight if it has custom headers)</li>
  <li>Custom headers: Authorization, Content-Type: application/json, or any non-standard header</li>
  <li>Credentials: any request with credentials: 'include'</li>
</ul>

<h2>What the browser sends</h2>
<pre>OPTIONS /api/data HTTP/1.1
Host: api.example.com
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Authorization, Content-Type</pre>

<p>The browser is asking: "Is a POST from https://app.example.com with Authorization and Content-Type headers allowed?"</p>

<h2>What your server must respond</h2>
<pre>HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400</pre>

<p>The status must be 200 or 204. If your server returns 404 or 405 for OPTIONS, the browser blocks the actual request and shows a CORS error.</p>

<h2>Postman does not send preflights</h2>
<p>Postman is a developer tool — it does not enforce browser security policies. If your API works in Postman but fails in the browser, a missing preflight handler is almost always the reason. This is why "CORS errors only in browser" is such a common complaint.</p>

<h2>Caching preflights</h2>
<p><code>Access-Control-Max-Age: 86400</code> tells the browser to cache the preflight result for 24 hours. Without it, the browser sends OPTIONS before every single cross-origin request with custom headers.</p>"""),

        ("what-are-security-headers", "What Are HTTP Security Headers and Why Do They Matter?", "Headers", RED_TAG,
         "Security headers are HTTP response headers that tell browsers how to behave when handling your page. Most servers send none by default.",
         "/", "Scan your security headers → HeadersFixer",
         '<a href="/glossary/hsts/">HSTS</a> <a href="/glossary/content-security-policy/">CSP</a> <a href="/blog/headers/security-headers-checklist/">Full checklist</a>',
         """
<p class="lead">Security headers are instructions your server sends to browsers alongside every response. They tell the browser what to do — and what to refuse — when handling your page. Most web servers send none by default.</p>

<h2>The gap between HTTPS and secure</h2>
<p>Having an HTTPS certificate does not make a site secure. It only means the connection is encrypted in transit. Once the page loads, a browser with no security headers will:</p>
<ul>
  <li>Run any inline script (including injected ones)</li>
  <li>Load resources from any domain</li>
  <li>Allow your page to be embedded in iframes on other sites</li>
  <li>Send your URL as a referrer to every third-party resource</li>
  <li>Allow any website to use your users' camera and microphone if you do</li>
</ul>
<p>Security headers close these gaps.</p>

<h2>The headers that matter</h2>

<h3>Strict-Transport-Security</h3>
<p>Tells browsers to only connect to your site via HTTPS, even if the user types http://. Prevents SSL stripping attacks on subsequent visits.</p>

<h3>Content-Security-Policy</h3>
<p>Defines which resources are allowed to load. The main defense against XSS — blocks injected scripts even if they get into your HTML.</p>

<h3>X-Frame-Options</h3>
<p>Prevents your page from being embedded in iframes on other sites. Blocks clickjacking attacks.</p>

<h3>X-Content-Type-Options: nosniff</h3>
<p>Prevents browsers from guessing the content type of a response. Without it, browsers may execute a text file as JavaScript if it looks like code.</p>

<h3>Referrer-Policy</h3>
<p>Controls how much URL information is shared when users navigate away from your site. Without it, full URLs including query strings (which may contain session tokens) are sent to third parties.</p>

<h3>Permissions-Policy</h3>
<p>Controls which browser features (camera, microphone, geolocation) your page and embedded iframes can access. Third-party scripts in your page cannot access features you have not explicitly allowed.</p>

<h2>How to check yours</h2>
<p>Use HeadersFixer — it fetches your live URL, reads the response headers, and shows exactly which security headers are missing or misconfigured. It generates the exact config for your stack: Nginx, Apache, Vercel, Cloudflare, Express, Caddy, or Next.js.</p>"""),

        ("what-is-hsts", "What is HSTS? HTTP Strict Transport Security Explained", "Headers", RED_TAG,
         "HSTS tells browsers to always use HTTPS for your domain — even if the user types http://. Here is how it works and why max-age matters.",
         "/", "Check your HSTS config → HeadersFixer",
         '<a href="/glossary/hsts/">HSTS glossary</a> <a href="/blog/headers/fix-hsts/">Fix HSTS issues</a> <a href="/blog/headers/security-headers-checklist/">Security headers checklist</a>',
         """
<p class="lead">When a user types your domain without HTTPS, the browser first makes an HTTP request. HSTS solves this: once a browser has seen your HSTS header, it automatically upgrades future requests to HTTPS before sending them — no HTTP request ever leaves the browser.</p>

<h2>The first-visit problem</h2>
<p>HTTPS protects connections, but only after the browser knows to use HTTPS. On the very first visit to a domain, the browser may make an HTTP request — which can be intercepted by an attacker on the same network (coffee shop, hotel WiFi). That attacker can perform a downgrade attack, stripping HTTPS entirely.</p>

<h2>How HSTS solves it</h2>
<p>When your server sends <code>Strict-Transport-Security: max-age=31536000</code>, the browser records: "This domain requires HTTPS for the next 31536000 seconds (1 year)." On every subsequent visit, the browser upgrades the request to HTTPS internally — the HTTP request never leaves the device.</p>

<pre>Strict-Transport-Security: max-age=31536000; includeSubDomains; preload</pre>

<h2>The directives</h2>
<ul>
  <li><strong>max-age</strong> — how long (in seconds) to enforce HTTPS. Start with 86400 (1 day) for testing, then increase to 31536000 (1 year).</li>
  <li><strong>includeSubDomains</strong> — apply HSTS to all subdomains. Add this once all your subdomains support HTTPS.</li>
  <li><strong>preload</strong> — opt in to being included in browsers' built-in HSTS lists. See hstspreload.org.</li>
</ul>

<h2>What HSTS does not protect against</h2>
<ul>
  <li>The very first visit (before the browser has seen the header)</li>
  <li>Private browsing sessions on some browsers (HSTS is cleared)</li>
  <li>Servers that have invalid certificates (HSTS does not bypass certificate errors)</li>
</ul>

<h2>The preload list</h2>
<p>Chrome, Firefox, and Safari ship with built-in lists of HSTS-required domains. If your domain is on this list, HTTPS is enforced even on the first ever visit — before any HTTP request is made. Submit at hstspreload.org. Requirements: max-age of at least 1 year, includeSubDomains, and all subdomains must support HTTPS.</p>

<h2>Important: only add on working HTTPS</h2>
<p>If HTTPS breaks after adding HSTS, users cannot access your site until max-age expires — there is no way to send them a new header over HTTP. Test HTTPS thoroughly before adding HSTS, and start with a low max-age.</p>"""),

        ("what-is-clickjacking", "What is Clickjacking? How X-Frame-Options Stops It", "Headers", RED_TAG,
         "Clickjacking embeds your page in an invisible iframe and tricks users into clicking things they cannot see. One header prevents it.",
         "/", "Check for X-Frame-Options → HeadersFixer",
         '<a href="/glossary/x-frame-options/">X-Frame-Options glossary</a> <a href="/blog/headers/fix-x-frame-options/">Fix X-Frame-Options</a> <a href="/glossary/content-security-policy/">CSP frame-ancestors</a>',
         """
<p class="lead">Clickjacking embeds your site in a transparent iframe on an attacker's page. The user thinks they are clicking the attacker's button — but they are clicking on your page behind it. One header line prevents this.</p>

<h2>How a clickjacking attack works</h2>
<p>The attacker creates a page with an iframe containing your site, positioned with CSS opacity: 0 over a visible button on their page. Your bank transfer confirmation page sits invisible underneath "Click here to win a prize." The user clicks the prize button — they are actually confirming a transfer on your bank's site, logged in as themselves.</p>

<pre>&lt;!-- Attacker's page --&gt;
&lt;div style="position: relative;"&gt;
  &lt;iframe src="https://bank.example.com/transfer?amount=1000&to=attacker"
    style="opacity: 0; position: absolute; top: 0; left: 0; width: 100%; height: 100%;"&gt;
  &lt;/iframe&gt;
  &lt;button style="position: relative; z-index: -1;"&gt;Click here to win!&lt;/button&gt;
&lt;/div&gt;</pre>

<h2>The fix — X-Frame-Options</h2>
<p>Tell browsers not to allow your page to be embedded in iframes:</p>
<pre>X-Frame-Options: SAMEORIGIN</pre>

<p>With this header, browsers refuse to render your page inside an iframe on any other domain. The attack is impossible because the iframe will not load.</p>

<h2>SAMEORIGIN vs DENY</h2>
<ul>
  <li><strong>SAMEORIGIN</strong> — allows iframes on your own domain only. Use for admin panels or embedded tools on the same domain.</li>
  <li><strong>DENY</strong> — no iframes anywhere, including your own domain. Use for login pages, payment pages, and any sensitive action.</li>
</ul>

<h2>The modern approach — CSP frame-ancestors</h2>
<p>CSP <code>frame-ancestors</code> is more powerful: it supports multiple origins, regex patterns, and takes precedence over X-Frame-Options in modern browsers. Use both:</p>
<pre>X-Frame-Options: SAMEORIGIN
Content-Security-Policy: frame-ancestors 'self';</pre>

<p>Older browsers use X-Frame-Options. Browsers supporting CSP use frame-ancestors and ignore X-Frame-Options.</p>"""),

        ("what-is-https", "What is HTTPS and Why HTTP Isn't Enough", "Headers", RED_TAG,
         "HTTPS encrypts your connection to protect data in transit. Here is what it protects, what it does not, and why HTTP is not acceptable for any site handling user data.",
         "/", "Check your HTTPS headers → HeadersFixer",
         '<a href="/glossary/hsts/">HSTS</a> <a href="/blog/headers/fix-hsts/">Fix HSTS</a> <a href="/blog/performance/fix-mixed-content/">Fix mixed content</a>',
         """
<p class="lead">HTTP sends everything as plain text. On an open WiFi network, anyone between you and the server can read every request and response — login credentials, session cookies, personal data. HTTPS encrypts the connection. Here is what that means in practice.</p>

<h2>What HTTP looks like on the wire</h2>
<pre># HTTP request — visible to anyone on the network
GET /account?session=abc123 HTTP/1.1
Host: bank.example.com
Cookie: session=abc123; auth=user@email.com</pre>

<p>On a coffee shop WiFi network, every device on that network can see this. Including your session cookie — which an attacker can copy and use to access your account.</p>

<h2>What HTTPS does</h2>
<p>TLS (Transport Layer Security) encrypts the connection between the browser and server. The data above becomes unreadable to anyone on the network who is not the server. The server proves its identity with a certificate — preventing impersonation.</p>

<h2>What HTTPS does not protect against</h2>
<ul>
  <li><strong>Server-side attacks</strong> — if the server is compromised, encrypted data is decrypted there</li>
  <li><strong>Malicious JavaScript</strong> — XSS attacks run in the browser, after decryption</li>
  <li><strong>Downgrade attacks on first visit</strong> — if the user types http://, the first request is unencrypted (HSTS fixes this)</li>
  <li><strong>Certificate authority compromise</strong> — if a CA is compromised, fake certificates can be issued</li>
</ul>

<h2>HTTPS is not enough on its own</h2>
<p>A site can be HTTPS and still be completely insecure:</p>
<ul>
  <li>No security headers = XSS attacks can run injected scripts</li>
  <li>No CSP = any external resource can be loaded</li>
  <li>No HSTS = first visit can be downgraded to HTTP</li>
  <li>Mixed content = HTTP resources loaded on HTTPS pages</li>
</ul>

<h2>Getting HTTPS free</h2>
<p>Let's Encrypt provides free TLS certificates via Certbot. Most hosting providers (Vercel, Netlify, Cloudflare Pages) handle HTTPS automatically. There is no reason for any public website to be on HTTP in 2026.</p>

<pre># Certbot for Nginx
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com</pre>"""),
    ]

    for slug, title, tag, tag_color, desc, cta_url, cta_text, related, content in articles:
        write(f"blog/explainers/{slug}/index.html", template(
            title=title, description=desc,
            canonical=f"{BASE_URL}/blog/explainers/{slug}/",
            schema=make_schema(title, desc, f"{BASE_URL}/blog/explainers/{slug}/",
                [("Understand the concept", f"Learn what {tag} is and why it matters."),
                 ("See how it works", "Follow the step-by-step explanation with real examples."),
                 ("Apply the fix", "Use HttpFixer to verify your configuration.")],
                [("What is this?", f"A browser security mechanism related to {tag}. See the full explanation above."),
                 ("Why does it matter?", "Missing or misconfigured settings expose your users to attacks. See the details above.")]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/explainers/">Explainers</a> → {title}',
            tag=tag, tag_color=tag_color, h1=title, content=content,
            cta_url=cta_url, cta_text=cta_text, related=related
        ))


# ─── BATCH 7: COMPARISON PAGES ────────────────────────────────────────────────

def batch7_comparisons():
    print("\n📦 Batch 7 — Comparison Pages")

    comparisons = [
        ("cors-vs-csrf", "CORS vs CSRF — What is the Difference?", "CORS", PURPLE_TAG,
         "CORS and CSRF sound similar but protect against completely different attacks. Here is the clear distinction and why CORS does not prevent CSRF.",
         "/cors/", "Test your CORS config → CORSFixer",
         '<a href="/glossary/cors/">What is CORS?</a> <a href="/blog/explainers/what-is-cors/">CORS explained</a>',
         """
<p class="lead">CORS and CSRF both involve cross-origin requests but they are completely different mechanisms. CORS is a browser policy that controls which origins can read API responses. CSRF is an attack where a malicious site tricks your browser into making requests using your existing session.</p>

<h2>CORS — what it is</h2>
<p>CORS controls whether JavaScript on one origin can read a response from another origin. If api.example.com does not include Access-Control-Allow-Origin for app.example.com, the browser blocks JavaScript from reading the response.</p>
<p>CORS does not prevent requests from being made — it prevents the response from being read by JavaScript on unauthorized origins.</p>

<h2>CSRF — what it is</h2>
<p>CSRF (Cross-Site Request Forgery) tricks a logged-in user's browser into making a request to a site where they have an active session — without their knowledge. The request includes their session cookie automatically.</p>

<pre>&lt;!-- Attacker's page — user is logged into bank.example.com --&gt;
&lt;img src="https://bank.example.com/transfer?amount=1000&to=attacker"&gt;
&lt;!-- Browser makes the request and includes the user's session cookie --&gt;</pre>

<h2>Why CORS does not prevent CSRF</h2>
<p>A CSRF attack using a simple GET (like the img src above) does not go through CORS — simple requests are not preflighted. Even with strict CORS, the request is still made and the session cookie is still sent. CORS only controls whether the response can be read by JavaScript, not whether the request is made.</p>

<h2>What actually prevents CSRF</h2>
<ul>
  <li><strong>SameSite cookie attribute</strong> — <code>Set-Cookie: session=abc; SameSite=Lax</code> prevents cookies from being sent on cross-site requests</li>
  <li><strong>CSRF tokens</strong> — random tokens in forms that the server verifies</li>
  <li><strong>Custom request headers</strong> — AJAX requests with custom headers trigger a CORS preflight, which blocks the request if the origin is not allowed</li>
</ul>

<h2>Summary</h2>
<table>
  <thead><tr><th></th><th>CORS</th><th>CSRF</th></tr></thead>
  <tbody>
    <tr><td>What it is</td><td>Browser policy on cross-origin response access</td><td>Attack exploiting trusted session cookies</td></tr>
    <tr><td>Who enforces it</td><td>Browser</td><td>Nothing automatically — you must implement protection</td></tr>
    <tr><td>What it protects</td><td>Your API responses from unauthorized reads</td><td>Your server from unintended state changes</td></tr>
    <tr><td>Fix</td><td>Correct CORS headers on your API</td><td>SameSite cookies, CSRF tokens</td></tr>
  </tbody>
</table>"""),

        ("csp-nonce-vs-hash", "CSP Nonce vs Hash vs unsafe-inline — When to Use Each", "CSP", GREEN_TAG,
         "Three ways to allow inline scripts in CSP. Two are safe. One defeats the purpose. Here is when to use each.",
         "/csp/", "Generate your CSP → CSPFixer",
         '<a href="/glossary/csp-nonce/">CSP nonces</a> <a href="/glossary/unsafe-inline/">unsafe-inline</a> <a href="/blog/csp/csp-unsafe-inline-nonce-hash/">Full guide</a>',
         """
<p class="lead">Inline scripts are blocked by a strict CSP. You have three options to allow them — but only two actually keep you safe.</p>

<table>
  <thead><tr><th>Approach</th><th>Safe?</th><th>Best for</th><th>Works for dynamic content?</th></tr></thead>
  <tbody>
    <tr><td>unsafe-inline</td><td>❌ No</td><td>Development only</td><td>Yes — but allows all inline scripts</td></tr>
    <tr><td>Nonce</td><td>✅ Yes</td><td>Server-rendered pages</td><td>Yes — new nonce per request</td></tr>
    <tr><td>Hash</td><td>✅ Yes</td><td>Static inline scripts</td><td>No — content must match exactly</td></tr>
  </tbody>
</table>

<h2>unsafe-inline — why it defeats CSP</h2>
<pre>Content-Security-Policy: script-src 'self' 'unsafe-inline'</pre>
<p>This allows every inline script to run — including any scripts an attacker manages to inject via XSS. It eliminates the "inline script blocked" console error, but it also eliminates all XSS protection. Never use in production.</p>

<h2>Nonces — the right approach for dynamic pages</h2>
<pre># Server generates a random nonce each request
nonce = base64.b64encode(os.urandom(16)).decode()

# Header includes nonce
Content-Security-Policy: script-src 'self' 'nonce-{nonce}'

# HTML includes matching nonce attribute
&lt;script nonce="{nonce}"&gt;console.log('allowed');&lt;/script&gt;
&lt;script&gt;console.log('blocked — no nonce');&lt;/script&gt;</pre>

<p>An injected script cannot know the nonce (it is random per request), so it is blocked. Your trusted scripts with the attribute are allowed.</p>

<h2>Hashes — for static inline scripts</h2>
<pre># Compute SHA-256 hash of the exact script content
import hashlib, base64
content = "console.log('hello');"
hash_val = base64.b64encode(hashlib.sha256(content.encode()).digest()).decode()

# Header
Content-Security-Policy: script-src 'self' 'sha256-{hash_val}'

# HTML — no attribute needed, content must match exactly
&lt;script&gt;console.log('hello');&lt;/script&gt;</pre>

<p>Change one character in the script and the hash no longer matches. Only use for scripts that never change.</p>"""),

        ("oauth-vs-oidc", "OAuth 2.0 vs OpenID Connect — What is Actually Different?", "OAuth", ORANGE_TAG,
         "OAuth 2.0 handles authorization. OpenID Connect adds authentication on top. Here is exactly what each does and when you need OIDC vs plain OAuth.",
         "/oauth/", "Debug your OAuth errors → OAuthFixer",
         '<a href="/glossary/oauth-grant-types/">OAuth grant types</a> <a href="/blog/explainers/what-is-oauth/">OAuth explained</a>',
         """
<p class="lead">OAuth 2.0 answers "can this app access your data?" OpenID Connect answers "who are you?" OIDC is an identity layer built on top of OAuth — it adds a standard way to get user identity information alongside access tokens.</p>

<h2>OAuth 2.0 — authorization only</h2>
<p>OAuth gives your app an access token to call an API on the user's behalf. The token proves the user authorized your app to access specific resources (scopes). OAuth does not tell your app anything about who the user is — just that they granted permission.</p>

<pre># After OAuth, you have an access token
# You can call the API:
GET /api/data HTTP/1.1
Authorization: Bearer eyJhbGc...

# But you do not know WHO authorized this — OAuth does not define that</pre>

<h2>OpenID Connect — authentication on top</h2>
<p>OIDC adds an ID token (a JWT) to the OAuth response. This token contains standard claims about the user's identity — sub (user ID), name, email, picture. OIDC also defines a standard /userinfo endpoint to fetch additional claims.</p>

<pre># OIDC adds id_token to the token response
{
  "access_token": "eyJhbGc...",
  "id_token": "eyJhbGc...", // JWT with user identity claims
  "expires_in": 3600,
  "token_type": "Bearer"
}

# Decoded id_token contains:
{
  "sub": "user123",  // unique user ID
  "name": "Jane Smith",
  "email": "jane@example.com",
  "iss": "https://accounts.google.com",
  "aud": "your-client-id",
  "exp": 1234567890
}</pre>

<h2>When to use which</h2>
<table>
  <thead><tr><th>Scenario</th><th>Use</th></tr></thead>
  <tbody>
    <tr><td>Machine-to-machine API access</td><td>OAuth (client credentials flow)</td></tr>
    <tr><td>Let users log in to your app</td><td>OIDC (authorization code + PKCE)</td></tr>
    <tr><td>Access Google Drive on user's behalf</td><td>OAuth with Google's scopes</td></tr>
    <tr><td>Sign in with Google</td><td>OIDC — you get the user's identity</td></tr>
    <tr><td>Third-party API integration</td><td>OAuth — just need the access token</td></tr>
  </tbody>
</table>

<h2>The scope that signals OIDC</h2>
<p>Include <code>openid</code> in your scope to activate OIDC and receive an ID token. Without it, you get plain OAuth — access token only, no identity information.</p>

<pre>scope=openid profile email  // OIDC — returns id_token + access_token
scope=read:data             // plain OAuth — returns access_token only</pre>"""),

        ("authorization-code-vs-client-credentials", "Authorization Code vs Client Credentials — When to Use Each", "OAuth", ORANGE_TAG,
         "Authorization Code with PKCE is for users. Client Credentials is for servers. Here is how to pick the right OAuth flow for your use case.",
         "/oauth/", "Debug your OAuth errors → OAuthFixer",
         '<a href="/glossary/pkce/">What is PKCE?</a> <a href="/glossary/oauth-grant-types/">All grant types</a>',
         """
<p class="lead">The most common OAuth mistake is using the wrong grant type. Authorization Code + PKCE is for when a user is present and authorizing your app. Client Credentials is for server-to-server calls with no user involved.</p>

<h2>Authorization Code + PKCE — user present</h2>
<p>Use this when a human user needs to grant your app access to their account on another service.</p>
<ul>
  <li>User is redirected to the auth server to log in</li>
  <li>User sees a consent screen and approves access</li>
  <li>Auth server redirects back with an authorization code</li>
  <li>Your app exchanges the code for tokens</li>
</ul>

<pre>// Typical use cases:
// - "Sign in with Google"
// - "Connect your Slack workspace"
// - "Allow access to your GitHub repos"
// - Any flow where the user must approve access</pre>

<h2>Client Credentials — no user, machine-to-machine</h2>
<p>Use this for server-to-server API calls where there is no user involved. Your server authenticates directly with the auth server using its own credentials.</p>
<ul>
  <li>No redirect, no user interaction</li>
  <li>Your server sends client_id and client_secret directly</li>
  <li>Gets an access token for making API calls</li>
</ul>

<pre>// POST directly to the token endpoint
const response = await fetch('https://auth.example.com/token', {
  method: 'POST',
  body: new URLSearchParams({
    grant_type: 'client_credentials',
    client_id: 'YOUR_CLIENT_ID',
    client_secret: 'YOUR_CLIENT_SECRET',
    scope: 'read:data write:data',
  })
});

// Use the access token for API calls
const { access_token } = await response.json();</pre>

<h2>Other flows and when they apply</h2>
<table>
  <thead><tr><th>Flow</th><th>When to use</th></tr></thead>
  <tbody>
    <tr><td>Authorization Code + PKCE</td><td>SPAs, mobile apps, any user-facing flow</td></tr>
    <tr><td>Client Credentials</td><td>Server-to-server, background jobs, microservices</td></tr>
    <tr><td>Device Code</td><td>TVs, CLI tools, devices with no browser</td></tr>
    <tr><td>Refresh Token</td><td>Not a standalone flow — used with Authorization Code to get new access tokens</td></tr>
  </tbody>
</table>

<h2>Never use Implicit Flow</h2>
<p>Implicit Flow (response_type=token) was deprecated in OAuth 2.1. It returns tokens in the URL fragment — which gets logged in browser history, server logs, and can be stolen by referrer headers. Always use Authorization Code + PKCE for SPAs instead.</p>"""),

        ("x-frame-options-vs-csp-frame-ancestors", "X-Frame-Options vs CSP frame-ancestors — Which to Use in 2026", "Headers", RED_TAG,
         "X-Frame-Options is old. CSP frame-ancestors is modern and more powerful. Here is the difference and why you should use both.",
         "/", "Check your frame protection → HeadersFixer",
         '<a href="/glossary/x-frame-options/">X-Frame-Options</a> <a href="/blog/headers/fix-x-frame-options/">Fix clickjacking</a>',
         """
<p class="lead">X-Frame-Options and CSP frame-ancestors both control iframe embedding — but frame-ancestors is more powerful and takes precedence when both are set. Use both for maximum browser compatibility.</p>

<h2>X-Frame-Options — the old way</h2>
<pre>X-Frame-Options: SAMEORIGIN  # or DENY</pre>
<p>Introduced in 2008. Supported by all browsers. Simple but limited — only SAMEORIGIN or DENY, no support for multiple allowed origins.</p>

<h2>CSP frame-ancestors — the modern way</h2>
<pre>Content-Security-Policy: frame-ancestors 'none';
Content-Security-Policy: frame-ancestors 'self';
Content-Security-Policy: frame-ancestors 'self' https://trusted-partner.com https://embed.example.com;</pre>
<p>Part of CSP Level 2. Supports multiple origins, wildcards, and more granular control. Takes precedence over X-Frame-Options in browsers that support CSP (which is basically all modern browsers).</p>

<h2>Comparison</h2>
<table>
  <thead><tr><th></th><th>X-Frame-Options</th><th>CSP frame-ancestors</th></tr></thead>
  <tbody>
    <tr><td>Browser support</td><td>All browsers including IE</td><td>All modern browsers</td></tr>
    <tr><td>Multiple origins</td><td>❌ No</td><td>✅ Yes</td></tr>
    <tr><td>Wildcard support</td><td>❌ No</td><td>✅ Yes (https://*.example.com)</td></tr>
    <tr><td>Takes precedence</td><td>Ignored when CSP present</td><td>Wins over X-Frame-Options</td></tr>
    <tr><td>Works in meta tag</td><td>No</td><td>No (frame-ancestors cannot be in meta)</td></tr>
  </tbody>
</table>

<h2>Use both for full coverage</h2>
<pre># Nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Content-Security-Policy "frame-ancestors 'self';" always;</pre>

<p>Modern browsers use frame-ancestors and ignore X-Frame-Options. Older browsers without CSP support fall back to X-Frame-Options. Using both gives you clickjacking protection regardless of browser version.</p>

<h2>When to use DENY vs none</h2>
<ul>
  <li><code>frame-ancestors 'none'</code> / <code>X-Frame-Options: DENY</code> — no one can embed your page, including your own domain. Use for login pages, payment pages, sensitive actions.</li>
  <li><code>frame-ancestors 'self'</code> / <code>X-Frame-Options: SAMEORIGIN</code> — your own domain can embed the page. Use when you have legitimate iframe use cases on your own domain.</li>
</ul>"""),
    ]

    for slug, title, tag, tag_color, desc, cta_url, cta_text, related, content in comparisons:
        write(f"blog/compare/{slug}/index.html", template(
            title=title, description=desc,
            canonical=f"{BASE_URL}/blog/compare/{slug}/",
            schema=make_schema(title, desc, f"{BASE_URL}/blog/compare/{slug}/",
                [("Understand the difference", "Read the plain-English explanation of both concepts."),
                 ("See the comparison table", "Use the table to quickly identify which approach fits your use case."),
                 ("Apply the right fix", "Use HttpFixer to verify your configuration.")],
                [("Which is better?", "It depends on your use case. See the comparison table in the article for the full breakdown."),
                 ("Do I need both?", "In many cases yes — see the article for when to use both simultaneously.")]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/compare/">Compare</a> → {title}',
            tag=tag, tag_color=tag_color, h1=title, content=content,
            cta_url=cta_url, cta_text=cta_text, related=related
        ))


# ─── BATCH 8: REFERENCE PAGES ─────────────────────────────────────────────────

def batch8_reference():
    print("\n📦 Batch 8 — Reference Pages")

    write("blog/reference/http-security-headers-reference/index.html", template(
        title="Complete HTTP Security Headers Reference",
        description="Every HTTP security header explained — purpose, example value, common misconfiguration, and spec link. A practical reference for developers.",
        canonical=f"{BASE_URL}/blog/reference/http-security-headers-reference/",
        schema=make_schema("Complete HTTP Security Headers Reference", "HTTP security headers reference guide.", f"{BASE_URL}/blog/reference/http-security-headers-reference/",
            [("Review each header", "Read the purpose and example for each security header."), ("Identify missing headers", "Use HeadersFixer to check which headers your site sends."), ("Copy the config", "Generate stack-specific config for your server.")],
            [("How many security headers should my site have?", "At minimum: HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy. Ideally also CSP, Permissions-Policy, COOP, and COEP."), ("Which header is most important?", "Content-Security-Policy for XSS protection. Strict-Transport-Security for HTTPS enforcement. Both are essential for production sites.")]),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/reference/">Reference</a> → Security Headers',
        tag="Reference", tag_color=PURPLE_TAG,
        h1="Complete HTTP Security Headers Reference",
        content="""
<p class="lead">Every security header your server should be sending, with example values, what they protect against, and links to the relevant specs. Use this alongside HeadersFixer to verify your site sends all of them.</p>

<h2>Strict-Transport-Security (HSTS)</h2>
<pre>Strict-Transport-Security: max-age=31536000; includeSubDomains; preload</pre>
<p><strong>Protects against:</strong> SSL stripping, HTTP downgrade attacks. <strong>Common mistake:</strong> Adding before HTTPS works fully, or setting max-age too low. <strong>Spec:</strong> RFC 6797.</p>

<h2>Content-Security-Policy (CSP)</h2>
<pre>Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc123'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none'; object-src 'none';</pre>
<p><strong>Protects against:</strong> XSS, data injection, resource injection. <strong>Common mistake:</strong> Using unsafe-inline which defeats XSS protection. <strong>Spec:</strong> W3C CSP Level 3.</p>

<h2>X-Frame-Options</h2>
<pre>X-Frame-Options: SAMEORIGIN</pre>
<p><strong>Protects against:</strong> Clickjacking. <strong>Values:</strong> DENY (no iframes), SAMEORIGIN (same domain only). <strong>Note:</strong> Superseded by CSP frame-ancestors in modern browsers. Use both.</p>

<h2>X-Content-Type-Options</h2>
<pre>X-Content-Type-Options: nosniff</pre>
<p><strong>Protects against:</strong> MIME type confusion attacks. <strong>Common mistake:</strong> None — this one has no configuration options. Just add it. <strong>Spec:</strong> WHATWG Fetch Standard.</p>

<h2>Referrer-Policy</h2>
<pre>Referrer-Policy: strict-origin-when-cross-origin</pre>
<p><strong>Protects against:</strong> URL leakage to third parties via the Referer header. <strong>Values:</strong> no-referrer, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url. <strong>Default (no header):</strong> strict-origin-when-cross-origin in modern browsers — but set it explicitly anyway.</p>

<h2>Permissions-Policy</h2>
<pre>Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()</pre>
<p><strong>Protects against:</strong> Third-party scripts accessing browser features. <strong>Common mistake:</strong> Not setting it — third-party analytics scripts may have access to device APIs by default. <strong>Spec:</strong> W3C Permissions Policy.</p>

<h2>Cross-Origin-Opener-Policy (COOP)</h2>
<pre>Cross-Origin-Opener-Policy: same-origin</pre>
<p><strong>Protects against:</strong> Cross-origin window access, Spectre-style attacks. <strong>Required for:</strong> SharedArrayBuffer, high-resolution timers. <strong>Values:</strong> same-origin, same-origin-allow-popups, unsafe-none.</p>

<h2>Cross-Origin-Embedder-Policy (COEP)</h2>
<pre>Cross-Origin-Embedder-Policy: require-corp</pre>
<p><strong>Required alongside COOP for cross-origin isolation.</strong> <strong>Values:</strong> require-corp, credentialless, unsafe-none. <strong>Caution:</strong> Can break third-party resources that do not set CORP headers.</p>

<h2>Cross-Origin-Resource-Policy (CORP)</h2>
<pre>Cross-Origin-Resource-Policy: same-origin</pre>
<p><strong>Protects against:</strong> Cross-origin reads of your resources. <strong>Values:</strong> same-site, same-origin, cross-origin. <strong>Required when:</strong> Your resources are embedded in a COEP-enabled site.</p>

<h2>Server (remove or redact)</h2>
<pre>Server: Apache   # replace or remove entirely</pre>
<p><strong>Default behavior:</strong> Nginx sends "nginx/1.24.0", Apache sends "Apache/2.4.57". Revealing versions helps attackers target known vulnerabilities. Set to a generic value or remove.</p>""",
        cta_url="/", cta_text="Scan your security headers → HeadersFixer",
        related='<a href="/blog/headers/security-headers-checklist/">Checklist</a> <a href="/glossary/hsts/">HSTS</a> <a href="/glossary/content-security-policy/">CSP</a> <a href="/fix/headers/nginx/">Nginx config</a>'
    ))

    write("blog/reference/cors-headers-cheat-sheet/index.html", template(
        title="CORS Headers Cheat Sheet — Every Header Explained",
        description="Every CORS request and response header with direction, purpose, and example. A one-page reference for developers debugging cross-origin issues.",
        canonical=f"{BASE_URL}/blog/reference/cors-headers-cheat-sheet/",
        schema=make_schema("CORS Headers Cheat Sheet", "Complete CORS header reference.", f"{BASE_URL}/blog/reference/cors-headers-cheat-sheet/",
            [("Review request headers", "See what the browser sends in cross-origin requests."), ("Review response headers", "See what your server must respond with."), ("Test your headers", "Use CORSFixer to verify your CORS config is correct.")],
            [("What headers does the browser send?", "Origin (always), Access-Control-Request-Method and Access-Control-Request-Headers (on preflight OPTIONS requests)."), ("What headers must my server return?", "Access-Control-Allow-Origin (required), and Access-Control-Allow-Methods + Allow-Headers for preflight responses.")]),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/reference/">Reference</a> → CORS Cheat Sheet',
        tag="Reference", tag_color=PURPLE_TAG,
        h1="CORS Headers Cheat Sheet",
        content="""
<p class="lead">Quick reference for every CORS header — what the browser sends, what your server must return, and what each one does.</p>

<h2>Request headers (browser → server)</h2>
<table>
  <thead><tr><th>Header</th><th>When sent</th><th>Example</th></tr></thead>
  <tbody>
    <tr><td>Origin</td><td>Every cross-origin request</td><td>Origin: https://app.example.com</td></tr>
    <tr><td>Access-Control-Request-Method</td><td>Preflight OPTIONS only</td><td>Access-Control-Request-Method: POST</td></tr>
    <tr><td>Access-Control-Request-Headers</td><td>Preflight OPTIONS only</td><td>Access-Control-Request-Headers: Authorization, Content-Type</td></tr>
  </tbody>
</table>

<h2>Response headers (server → browser)</h2>
<table>
  <thead><tr><th>Header</th><th>Required?</th><th>Example</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Access-Control-Allow-Origin</td><td>Yes</td><td>https://app.example.com or *</td><td>Cannot use * with credentials</td></tr>
    <tr><td>Access-Control-Allow-Methods</td><td>On preflight</td><td>GET, POST, PUT, DELETE, OPTIONS</td><td>Must include the requested method</td></tr>
    <tr><td>Access-Control-Allow-Headers</td><td>On preflight</td><td>Authorization, Content-Type</td><td>Must include requested headers</td></tr>
    <tr><td>Access-Control-Allow-Credentials</td><td>With cookies/auth</td><td>true</td><td>Only valid with explicit origin, not *</td></tr>
    <tr><td>Access-Control-Max-Age</td><td>Optional</td><td>86400</td><td>Seconds to cache preflight. Default varies by browser.</td></tr>
    <tr><td>Access-Control-Expose-Headers</td><td>Optional</td><td>X-Request-ID, X-Rate-Limit</td><td>Headers JavaScript can read beyond the safe list</td></tr>
    <tr><td>Vary</td><td>With explicit origins</td><td>Origin</td><td>Prevents CDN from serving one origin's response to another</td></tr>
  </tbody>
</table>

<h2>The safe response headers (no Expose-Headers needed)</h2>
<p>By default, JavaScript can only read these response headers without Access-Control-Expose-Headers:</p>
<ul>
  <li>Cache-Control</li>
  <li>Content-Language</li>
  <li>Content-Length</li>
  <li>Content-Type</li>
  <li>Expires</li>
  <li>Last-Modified</li>
  <li>Pragma</li>
</ul>
<p>To expose other headers (like X-Rate-Limit, X-Request-ID), add them to Access-Control-Expose-Headers.</p>

<h2>Minimal working CORS for a public API</h2>
<pre>Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type</pre>

<h2>CORS for authenticated API with cookies</h2>
<pre>Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 86400
Vary: Origin</pre>""",
        cta_url="/cors/", cta_text="Test your CORS headers live → CORSFixer",
        related='<a href="/glossary/cors/">What is CORS?</a> <a href="/glossary/preflight-request/">Preflight requests</a> <a href="/blog/cors/fix-cors-express/">Express CORS fix</a>'
    ))

    write("blog/reference/oauth-error-codes-reference/index.html", template(
        title="OAuth 2.0 Error Codes Reference — Every Error and Fix",
        description="Every OAuth 2.0 error code, what it means, the most common cause, and how to fix it. A one-page reference for debugging OAuth issues.",
        canonical=f"{BASE_URL}/blog/reference/oauth-error-codes-reference/",
        schema=make_schema("OAuth 2.0 Error Codes Reference", "OAuth error codes reference and fixes.", f"{BASE_URL}/blog/reference/oauth-error-codes-reference/",
            [("Find your error code", "Look up the error code in the reference table."), ("Identify the cause", "Each error has the most common causes listed."), ("Apply the fix", "Use OAuthFixer for provider-specific debugging.")],
            [("What does invalid_grant mean?", "The authorization code expired, was reused, or the PKCE verifier does not match. Check your code exchange timing and PKCE implementation."), ("What does redirect_uri_mismatch mean?", "The redirect_uri in your request does not exactly match the registered URI in your provider dashboard.")]),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/reference/">Reference</a> → OAuth Errors',
        tag="Reference", tag_color=ORANGE_TAG,
        h1="OAuth 2.0 Error Codes Reference",
        content="""
<p class="lead">OAuth errors return a JSON body with an error field and usually an error_description. Here is every standard error code, what it means, and how to fix it.</p>

<table>
  <thead><tr><th>Error Code</th><th>Meaning</th><th>Common Cause</th><th>Fix</th></tr></thead>
  <tbody>
    <tr><td><strong>invalid_grant</strong></td><td>Authorization code or refresh token is invalid</td><td>Code expired, reused, PKCE mismatch, refresh token rotated</td><td>Exchange code immediately; check PKCE verifier; handle rotation</td></tr>
    <tr><td><strong>invalid_client</strong></td><td>Client authentication failed</td><td>Wrong client_id or client_secret; secret rotated</td><td>Check credentials in provider dashboard; update rotated secret</td></tr>
    <tr><td><strong>invalid_request</strong></td><td>Malformed request</td><td>Missing required parameter; wrong encoding</td><td>Check all required params; use URLSearchParams for encoding</td></tr>
    <tr><td><strong>unauthorized_client</strong></td><td>Client not authorized for this grant type</td><td>Grant type not enabled for your app</td><td>Enable the grant type in provider dashboard</td></tr>
    <tr><td><strong>access_denied</strong></td><td>User denied access</td><td>User clicked "Cancel" on consent screen</td><td>Handle gracefully — redirect to login or show explanation</td></tr>
    <tr><td><strong>unsupported_grant_type</strong></td><td>Server does not support this grant type</td><td>Using deprecated Implicit Flow or wrong grant type</td><td>Switch to Authorization Code + PKCE for user flows</td></tr>
    <tr><td><strong>invalid_scope</strong></td><td>Requested scope is invalid or not permitted</td><td>Typo in scope name; scope not configured for client</td><td>Check exact scope names in provider docs; enable in dashboard</td></tr>
    <tr><td><strong>redirect_uri_mismatch</strong></td><td>redirect_uri does not match registered URI</td><td>Trailing slash, protocol, or port difference</td><td>Exact string match required — check provider dashboard</td></tr>
    <tr><td><strong>server_error</strong></td><td>Auth server internal error</td><td>Provider-side issue</td><td>Retry with exponential backoff; check provider status page</td></tr>
    <tr><td><strong>temporarily_unavailable</strong></td><td>Auth server temporarily unavailable</td><td>Provider maintenance or outage</td><td>Retry after delay; check provider status page</td></tr>
  </tbody>
</table>

<h2>Error response format</h2>
<pre>{
  "error": "invalid_grant",
  "error_description": "The provided authorization grant is invalid, expired, or revoked.",
  "error_uri": "https://tools.ietf.org/html/rfc6749#section-5.2"
}</pre>

<h2>How to debug OAuth errors</h2>
<ol>
  <li>Log the full error response — including error_description, not just the status code</li>
  <li>Check the exact parameter values you are sending — log them before the request</li>
  <li>Use OAuthFixer to walk through the error by provider — Auth0, Okta, Cognito, Google, Microsoft each have specific causes and fixes</li>
</ol>""",
        cta_url="/oauth/", cta_text="Debug your OAuth error → OAuthFixer",
        related='<a href="/blog/oauth/fix-invalid-grant/">Fix invalid_grant</a> <a href="/blog/oauth/fix-redirect-uri-mismatch/">Fix redirect_uri_mismatch</a> <a href="/glossary/pkce/">What is PKCE?</a>'
    ))

    write("blog/reference/csp-third-party-services/index.html", template(
        title="CSP for Popular Third-Party Services — Google, Stripe, Intercom",
        description="Copy-paste CSP directives for the most common third-party services — GA4, Stripe, Intercom, HubSpot, Hotjar, reCAPTCHA, and more.",
        canonical=f"{BASE_URL}/blog/reference/csp-third-party-services/",
        schema=make_schema("CSP for Popular Third-Party Services", "CSP directives for GA4, Stripe, Intercom, HubSpot, and more.", f"{BASE_URL}/blog/reference/csp-third-party-services/",
            [("Find your service", "Locate the service in the reference below."), ("Copy the required directives", "Add each domain to the correct CSP directive."), ("Test with CSPFixer", "Verify no violations remain after updating your CSP.")],
            [("How do I add Google Analytics to my CSP?", "Add https://www.googletagmanager.com to script-src and https://www.google-analytics.com to both script-src and connect-src."), ("Why do third-party scripts break CSP?", "They load from multiple subdomains, make API calls, and sometimes inject inline scripts — each requiring separate allowlist entries.")]),
        nav_label="Blog",
        breadcrumb='<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/reference/">Reference</a> → CSP Third-Party',
        tag="Reference", tag_color=GREEN_TAG,
        h1="CSP Directives for Popular Third-Party Services",
        content="""
<p class="lead">Copy-paste CSP additions for the services your site most likely uses. Add these to your existing CSP directives — do not replace your full policy with them.</p>

<h2>Google Analytics 4 (GA4) via GTM</h2>
<pre>script-src https://www.googletagmanager.com https://www.google-analytics.com;
connect-src https://www.google-analytics.com https://analytics.google.com https://region1.google-analytics.com;
img-src https://www.google-analytics.com https://www.googletagmanager.com;</pre>

<h2>Google Fonts</h2>
<pre>style-src https://fonts.googleapis.com;
font-src https://fonts.gstatic.com;</pre>

<h2>Stripe.js</h2>
<pre>script-src https://js.stripe.com;
frame-src https://js.stripe.com https://hooks.stripe.com;
connect-src https://api.stripe.com;</pre>

<h2>Intercom</h2>
<pre>script-src https://widget.intercom.io https://js.intercomcdn.com;
connect-src https://api.intercom.io https://api-iam.intercom.io wss://nexus-websocket-a.intercom.io;
img-src https://static.intercomassets.com https://downloads.intercomcdn.com;
frame-src https://intercom-sheets.com;</pre>

<h2>HubSpot</h2>
<pre>script-src https://js.hs-scripts.com https://js.usemessages.com https://js.hscollectedforms.net https://js.hs-analytics.net;
connect-src https://api.hubspot.com https://forms.hubspot.com https://track.hubspot.com;
img-src https://track.hubspot.com;</pre>

<h2>Hotjar</h2>
<pre>script-src https://static.hotjar.com https://script.hotjar.com;
connect-src https://*.hotjar.com https://*.hotjar.io wss://*.hotjar.com;
img-src https://*.hotjar.com;
font-src https://static.hotjar.com;</pre>

<h2>reCAPTCHA v3</h2>
<pre>script-src https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/;
frame-src https://www.google.com/recaptcha/;
connect-src https://www.google.com/recaptcha/;</pre>

<h2>YouTube embeds</h2>
<pre>frame-src https://www.youtube.com https://www.youtube-nocookie.com;
img-src https://i.ytimg.com;
connect-src https://www.youtube.com;</pre>

<h2>Cloudflare Turnstile</h2>
<pre>script-src https://challenges.cloudflare.com;
frame-src https://challenges.cloudflare.com;
connect-src https://challenges.cloudflare.com;</pre>

<h2>Sentry (error monitoring)</h2>
<pre>script-src https://browser.sentry-cdn.com;
connect-src https://*.sentry.io;</pre>

<h2>Crisp chat</h2>
<pre>script-src https://client.crisp.chat;
connect-src https://client.relay.crisp.chat wss://client.relay.crisp.chat;
img-src https://image.crisp.chat https://storage.crisp.chat;
frame-src https://game.crisp.chat;</pre>

<p>Missing a service? Use CSPFixer — it scans your live page, finds every external resource your page loads, and generates a complete CSP automatically.</p>""",
        cta_url="/csp/", cta_text="Generate your full CSP → CSPFixer",
        related='<a href="/blog/csp/csp-google-analytics-hotjar/">Analytics scripts guide</a> <a href="/blog/csp/fix-csp-refused-to-load/">Fix refused to load</a> <a href="/glossary/content-security-policy/">CSP explained</a>'
    ))


# ─── BATCH 9: PLATFORM GUIDES ─────────────────────────────────────────────────

def batch9_platform():
    print("\n📦 Batch 9 — Platform Guides")

    platforms = [
        ("cors-aws-lambda", "CORS on AWS Lambda — API Gateway Configuration", "CORS", PURPLE_TAG,
         "AWS API Gateway handles CORS separately from Lambda. Both need to be configured. Here is exactly where each setting goes.",
         "/cors/", "Test your Lambda CORS config →",
         '<a href="/fix/cors/nginx/">Nginx CORS</a> <a href="/glossary/preflight-request/">Preflight requests</a>',
         """
<p class="lead">AWS API Gateway handles CORS at the gateway level — separate from your Lambda function. You need to configure both. Missing either one and the browser error is the same: no CORS headers.</p>

<h2>Step 1 — Enable CORS in API Gateway</h2>
<p>In the API Gateway console: select your resource → Actions → Enable CORS. This adds an OPTIONS method that returns CORS headers. Set the values to match your frontend domain.</p>

<pre># Using AWS SAM template
Resources:
  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Cors:
        AllowOrigin: "'https://yourapp.com'"
        AllowHeaders: "'Content-Type,Authorization'"
        AllowMethods: "'GET,POST,PUT,DELETE,OPTIONS'"
        AllowCredentials: "'true'"</pre>

<h2>Step 2 — Lambda must also return CORS headers</h2>
<p>API Gateway's CORS config handles the OPTIONS preflight. But your Lambda function response headers are what the browser sees on actual GET/POST calls. Your function must also include them:</p>

<pre>// Node.js Lambda handler
exports.handler = async (event) => {
  const origin = event.headers?.origin || event.headers?.Origin;

  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': 'https://yourapp.com',
      'Access-Control-Allow-Credentials': 'true',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ data: 'ok' }),
  };
};</pre>

<h2>Using AWS CDK</h2>
<pre>const api = new apigateway.RestApi(this, 'MyApi', {
  defaultCorsPreflightOptions: {
    allowOrigins: ['https://yourapp.com'],
    allowMethods: apigateway.Cors.ALL_METHODS,
    allowHeaders: ['Content-Type', 'Authorization'],
    allowCredentials: true,
  },
});</pre>

<h2>Common mistake</h2>
<p>Enabling CORS in API Gateway but not returning CORS headers from the Lambda function. The preflight passes (OPTIONS returns 204) but the actual request fails because the response from Lambda has no Access-Control-Allow-Origin header.</p>"""),

        ("cors-cloudflare-workers", "CORS on Cloudflare Workers — Headers Without a Backend", "CORS", PURPLE_TAG,
         "Cloudflare Workers run at the edge with no traditional server. Here is how to add CORS headers and handle preflight in a Worker.",
         "/cors/", "Test your Worker CORS config →",
         '<a href="/providers/cloudflare/">Cloudflare hub</a> <a href="/fix/cors/nginx/">Nginx CORS</a>',
         """
<p class="lead">Cloudflare Workers run JavaScript at the edge — no traditional server, no nginx.conf. Add CORS headers directly in your Worker's fetch handler.</p>

<h2>Basic CORS in a Worker</h2>
<pre>export default {
  async fetch(request) {
    // Handle OPTIONS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': 'https://yourapp.com',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    // Your actual response
    const data = { status: 'ok' };

    return new Response(JSON.stringify(data), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://yourapp.com',
        'Access-Control-Allow-Credentials': 'true',
      },
    });
  },
};</pre>

<h2>Dynamic origin allowlist</h2>
<pre>const ALLOWED_ORIGINS = ['https://yourapp.com', 'https://staging.yourapp.com'];

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : '';
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Credentials': 'true',
    'Vary': 'Origin',
  };
}

export default {
  async fetch(request) {
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    return new Response(JSON.stringify({ ok: true }), {
      headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
    });
  },
};</pre>

<h2>Using Hono framework</h2>
<pre>import { Hono } from 'hono';
import { cors } from 'hono/cors';

const app = new Hono();

app.use('/api/*', cors({
  origin: 'https://yourapp.com',
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
}));

app.get('/api/data', (c) => c.json({ data: 'ok' }));

export default app;</pre>"""),

        ("security-headers-netlify", "Security Headers for Netlify — Complete Configuration", "Headers", RED_TAG,
         "Netlify security headers go in a _headers file or netlify.toml. Here is the complete config for both, including HSTS, CSP, and all security headers.",
         "/", "Check your Netlify headers → HeadersFixer",
         '<a href="/providers/netlify/">Netlify provider hub</a> <a href="/fix/headers/netlify/">Netlify headers fix</a>',
         """
<p class="lead">Netlify lets you set security headers in a _headers file at your project root or in netlify.toml. The _headers file is simpler. Here is the complete config for both approaches.</p>

<h2>Using the _headers file</h2>
<p>Create a file called <code>_headers</code> in your project root (same level as index.html). Netlify processes it automatically on deploy.</p>
<pre>/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none'; object-src 'none';
  Cross-Origin-Opener-Policy: same-origin

/static/*
  Cache-Control: public, max-age=31536000, immutable

/api/*
  Cache-Control: no-store</pre>

<h2>Using netlify.toml</h2>
<pre>[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains"
    Content-Security-Policy = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none'; object-src 'none';"

[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"</pre>

<h2>What Netlify adds automatically</h2>
<p>Netlify automatically sets:</p>
<ul>
  <li>HTTPS redirect (all HTTP traffic → HTTPS)</li>
  <li>X-Content-Type-Options: nosniff (on some plans)</li>
</ul>
<p>Everything else — HSTS, CSP, X-Frame-Options — you must set explicitly. Use HeadersFixer to verify what is actually being sent after deploy.</p>

<h2>Testing before going live</h2>
<pre># Deploy to a preview URL first
netlify deploy

# Then verify headers on the preview URL
curl -I https://deploy-preview-123--yoursite.netlify.app/</pre>"""),

        ("csp-single-page-apps", "CSP for Single Page Apps — React, Vue, Angular", "CSP", GREEN_TAG,
         "SPAs are harder to secure with CSP because frameworks use eval and inline scripts. Here is how to build a working CSP for React, Vue, and Angular.",
         "/csp/", "Generate your SPA CSP → CSPFixer",
         '<a href="/blog/csp/fix-csp-nextjs/">Next.js CSP</a> <a href="/glossary/unsafe-inline/">unsafe-inline</a>',
         """
<p class="lead">Single-page apps make CSP harder because bundlers and frameworks sometimes use eval(), inject inline scripts, and load resources dynamically. Here is how to handle each framework.</p>

<h2>React (Create React App / Vite)</h2>
<p>CRA and Vite do not use eval() by default. A nonce-based CSP works if you are serving from a Node.js server. For static deployments (Netlify, Vercel, S3), use hashes for any inline scripts.</p>
<pre># Starting CSP for React on Vercel
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self' data:;
  connect-src 'self' https://api.yourbackend.com;
  frame-ancestors 'none';
  object-src 'none';</pre>

<p>The <code>style-src 'unsafe-inline'</code> is usually required for CSS-in-JS (styled-components, emotion). Use nonces or the strictDynamic approach to avoid it.</p>

<h2>Next.js (App Router)</h2>
<pre># Next.js with nonces — see our dedicated guide
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{nonce}' 'strict-dynamic'; style-src 'self' 'unsafe-inline';</pre>

<h2>Vue.js</h2>
<p>Vue's template compiler does not use eval(). The runtime-only build is CSP-compatible. If you use the full build (including compiler), set script-src to allow eval:</p>
<pre># Vue runtime-only (recommended for production)
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';

# Vue full build (includes template compiler) — less secure
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-eval';</pre>

<h2>Angular</h2>
<p>Angular supports Trusted Types — the strictest CSP mode available:</p>
<pre># Angular with Trusted Types
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  require-trusted-types-for 'script';
  trusted-types angular angular#unsafe-bypass;</pre>

<h2>Dynamic imports and code splitting</h2>
<p>Webpack and Vite code splitting loads chunks dynamically. Add your CDN domain or use <code>'strict-dynamic'</code> to allow script tags created by your trusted inline scripts:</p>
<pre>script-src 'self' 'nonce-{nonce}' 'strict-dynamic';
# strict-dynamic propagates trust from your nonce to any script those scripts load</pre>"""),

        ("cors-docker", "CORS in Docker — Why localhost Works but Container Does Not", "CORS", PURPLE_TAG,
         "Docker containers have their own network namespace. localhost inside a container is not the same as localhost on your host machine. Here is how to fix CORS in Docker.",
         "/cors/", "Test your Docker CORS config →",
         '<a href="/fix/cors/nginx/">Nginx CORS</a> <a href="/fix/cors/express/">Express CORS</a>',
         """
<p class="lead">When you run your frontend and backend in separate Docker containers, they cannot reach each other via localhost. Container networking has its own namespace — localhost inside a container refers to the container itself, not your host machine.</p>

<h2>The Docker networking problem</h2>
<pre># This works locally (no Docker):
fetch('http://localhost:8000/api')  # frontend on :3000 → backend on :8000

# This breaks in Docker:
# frontend container: localhost = the frontend container
# backend container: localhost = the backend container
# They are different machines</pre>

<h2>Fix 1 — Use service names in docker-compose</h2>
<p>Docker Compose creates a network where containers can reach each other by their service name. Use the service name instead of localhost:</p>
<pre># docker-compose.yml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8000  # use service name

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - CORS_ORIGIN=http://localhost:3000  # browser still uses localhost</pre>

<p>The browser calls the backend using <code>http://localhost:8000</code> (the host port mapping). The backend must allow the origin <code>http://localhost:3000</code> for CORS.</p>

<h2>Fix 2 — For host machine access, use host.docker.internal</h2>
<pre># From inside a container, reach the host machine:
fetch('http://host.docker.internal:8000/api')

# Or in docker-compose:
extra_hosts:
  - "host.docker.internal:host-gateway"</pre>

<h2>Fix 3 — Nginx reverse proxy for both services</h2>
<p>The cleanest setup: Nginx in front of both. Same origin = no CORS needed:</p>
<pre># nginx.conf inside the Nginx container
server {
    listen 80;

    location / {
        proxy_pass http://frontend:3000;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        # No CORS needed — same origin from browser's perspective
    }
}</pre>

<h2>CORS config for Docker environment</h2>
<pre>// Express backend — allow the host port the browser uses
app.use(cors({
  origin: [
    'http://localhost:3000',     // browser access via host port mapping
    'http://frontend:3000',      // container-to-container (if needed)
  ],
  credentials: true,
}));</pre>"""),
    ]

    for slug, title, tag, tag_color, desc, cta_url, cta_text, related, content in platforms:
        write(f"blog/platform/{slug}/index.html", template(
            title=title, description=desc,
            canonical=f"{BASE_URL}/blog/platform/{slug}/",
            schema=make_schema(title, desc, f"{BASE_URL}/blog/platform/{slug}/",
                [("Understand the platform specifics", f"See how {tag} configuration works on this platform."),
                 ("Apply the fix", "Copy the configuration appropriate for your setup."),
                 ("Verify with HttpFixer", "Test the live result to confirm headers are correct.")],
                [("Is this platform-specific fix different from the general approach?", f"Yes — each platform has its own way to configure {tag}. The general principles are the same but the config syntax differs."),
                 ("Does this work on the free tier?", "Check the article — free tier limitations are noted where relevant.")]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/platform/">Platform Guides</a> → {title}',
            tag=tag, tag_color=tag_color, h1=title, content=content,
            cta_url=cta_url, cta_text=cta_text, related=related
        ))


# ─── BATCH 10: ERROR MESSAGE LANDING PAGES ────────────────────────────────────

def batch10_errors():
    print("\n📦 Batch 10 — Error Message Landing Pages")

    errors = [
        ("no-access-control-allow-origin",
         "No 'Access-Control-Allow-Origin' header is present",
         "No Access-Control-Allow-Origin Header — Fix",
         "Your API response is missing the Access-Control-Allow-Origin header. The browser blocked it before JavaScript could read it. Here is the fix for your stack.",
         "/cors/", "Find the exact fix for your stack → CORSFixer",
         '<a href="/blog/cors/fix-cors-express/">Express fix</a> <a href="/blog/cors/fix-cors-nginx/">Nginx fix</a> <a href="/blog/cors/fix-cors-fastapi/">FastAPI fix</a>',
         """
<div class="error-box"><div class="error-label">Exact Browser Console Error</div>Access to fetch at 'https://api.example.com/data' from origin 'https://app.example.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.</div>

<p class="lead">Your server processed the request and returned a response — but the response is missing <code>Access-Control-Allow-Origin</code>. The browser blocked it before JavaScript could read it.</p>

<h2>The fix — add the header to your server response</h2>

<h3>Express (Node.js)</h3>
<pre>const cors = require('cors');
app.use(cors({ origin: 'https://app.example.com' }));</pre>

<h3>Nginx</h3>
<pre>add_header Access-Control-Allow-Origin "https://app.example.com" always;</pre>

<h3>FastAPI (Python)</h3>
<pre>from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"])</pre>

<h3>Django</h3>
<pre>pip install django-cors-headers
# settings.py: CORS_ALLOWED_ORIGINS = ['https://app.example.com']</pre>

<h3>Next.js (vercel.json)</h3>
<pre>{ "headers": [{ "source": "/api/(.*)", "headers": [
  { "key": "Access-Control-Allow-Origin", "value": "https://app.example.com" }
]}]}</pre>

<p>Not sure which fix applies to your stack? CORSFixer sends a real OPTIONS preflight to your API and shows exactly what is missing.</p>"""),

        ("request-header-not-allowed",
         "Request header field not allowed by Access-Control-Allow-Headers",
         "CORS Header Not Allowed — Fix",
         "Your request includes a header (like Authorization or Content-Type: application/json) that the server's CORS policy does not allow. Here is the exact fix.",
         "/cors/", "Find the preflight fix for your stack → CORSFixer",
         '<a href="/glossary/preflight-request/">Preflight requests</a> <a href="/blog/cors/fix-cors-preflight-options/">Fix OPTIONS preflight</a>',
         """
<div class="error-box"><div class="error-label">Exact Browser Console Error</div>Access to fetch at 'https://api.example.com' from origin 'https://app.example.com' has been blocked by CORS policy: Request header field authorization is not allowed by Access-Control-Allow-Headers in preflight response.</div>

<p class="lead">Your request includes a custom header (Authorization, Content-Type: application/json, or similar) that your server's OPTIONS preflight response does not allow. Add it to Access-Control-Allow-Headers.</p>

<h2>The fix — allow the header in your preflight response</h2>

<h3>Express</h3>
<pre>app.use(cors({
  origin: 'https://app.example.com',
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Custom-Header'],
}));</pre>

<h3>Nginx</h3>
<pre>if ($request_method = OPTIONS) {
    add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-Custom-Header";
    return 204;
}</pre>

<h3>FastAPI</h3>
<pre>app.add_middleware(CORSMiddleware,
  allow_origins=["https://app.example.com"],
  allow_headers=["Authorization", "Content-Type"]
)</pre>

<h2>Allow all headers (development only)</h2>
<pre># Not for production — allows any header
add_header Access-Control-Allow-Headers "*";</pre>

<p>Use CORSFixer to send a real preflight to your API — it shows the exact headers the browser is requesting and what your server is allowing.</p>"""),

        ("refused-to-load-script-csp",
         "Refused to load the script because it violates the following Content Security Policy directive",
         "CSP: Refused to Load Script — Fix",
         "Your Content Security Policy is blocking a script. The browser console shows exactly which URL was blocked and which directive caused it.",
         "/csp/", "Scan all blocked resources → CSPFixer",
         '<a href="/blog/csp/fix-csp-refused-to-load/">Full guide</a> <a href="/glossary/content-security-policy/">What is CSP?</a>',
         """
<div class="error-box"><div class="error-label">Exact Browser Console Error</div>Refused to load the script 'https://cdn.example.com/widget.js' because it violates the following Content Security Policy directive: "script-src 'self'". Note that 'script-src-elem' was not explicitly set, so 'script-src' is used as a fallback.</div>

<p class="lead">Your CSP is blocking a script. The error tells you exactly what was blocked and which directive caused it. Add the domain to <code>script-src</code>.</p>

<h2>Read the error — it tells you exactly what to add</h2>
<p>From the error above: <code>https://cdn.example.com/widget.js</code> is blocked. The directive is <code>script-src</code>. The fix is adding <code>https://cdn.example.com</code> to script-src.</p>

<h2>Add the domain to script-src</h2>
<pre># Nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.example.com;" always;

# Vercel (vercel.json)
{ "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' https://cdn.example.com;" }

# Express
res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self' https://cdn.example.com;");</pre>

<h2>Resource type to directive</h2>
<pre>Script blocked      → add to script-src
Stylesheet blocked  → add to style-src
Image blocked       → add to img-src
API call blocked    → add to connect-src
Font blocked        → add to font-src
Iframe blocked      → add to frame-src</pre>

<p>Have multiple violations? CSPFixer scans your live page and generates a complete CSP that allows all your legitimate resources.</p>"""),

        ("preflight-failed",
         "Response to preflight request doesn't pass access control check",
         "CORS Preflight Failed — Fix",
         "The OPTIONS preflight request your browser sent was rejected. Your server must return 204 with CORS headers for OPTIONS requests.",
         "/cors/", "Send a live preflight → CORSFixer",
         '<a href="/blog/cors/fix-cors-preflight-options/">Preflight guide</a> <a href="/glossary/preflight-request/">What is a preflight?</a>',
         """
<div class="error-box"><div class="error-label">Exact Browser Console Error</div>Access to fetch at 'https://api.example.com/data' from origin 'https://app.example.com' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.</div>

<p class="lead">Before your POST/PUT/DELETE request runs, the browser sent an OPTIONS request. Your server returned an error (404, 405, or 200 without CORS headers). Add an OPTIONS handler that returns 204 with CORS headers.</p>

<h2>The fix by framework</h2>

<h3>Express</h3>
<pre>app.options('*', cors());  // Handle preflight for all routes
app.use(cors({ origin: 'https://app.example.com' }));</pre>

<h3>Nginx</h3>
<pre>if ($request_method = OPTIONS) {
    add_header Access-Control-Allow-Origin "https://app.example.com";
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
    add_header Access-Control-Allow-Headers "Authorization, Content-Type";
    add_header Content-Length 0;
    return 204;
}</pre>

<h3>FastAPI</h3>
<pre># CORSMiddleware handles OPTIONS automatically
app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"], allow_methods=["*"])</pre>

<h3>Django</h3>
<pre># django-cors-headers handles OPTIONS automatically after install
CORS_ALLOWED_ORIGINS = ['https://app.example.com']</pre>

<p>CORSFixer sends a real OPTIONS preflight to your endpoint and shows exactly what your server returns — so you can see what is missing.</p>"""),

        ("pkce-required",
         "PKCE verification failed / PKCE required",
         "OAuth PKCE Error — Fix",
         "Your OAuth token exchange failed because of a PKCE mismatch. The code_verifier must match the code_challenge sent in the authorization request.",
         "/oauth/", "Debug your OAuth PKCE error → OAuthFixer",
         '<a href="/glossary/pkce/">What is PKCE?</a> <a href="/blog/oauth/fix-pkce-errors/">PKCE errors guide</a>',
         """
<div class="error-box"><div class="error-label">OAuth Error Response</div>{"error": "invalid_grant", "error_description": "PKCE verification failed: code_verifier does not match code_challenge"}</div>

<p class="lead">The code_verifier you sent in the token exchange does not match the code_challenge you sent in the authorization request. They must be cryptographically linked — the challenge is the SHA-256 hash of the verifier.</p>

<h2>Common causes</h2>
<ul>
  <li>Verifier not stored before the redirect — regenerated on the callback page</li>
  <li>Wrong base64 encoding — must be base64url (no padding, - and _ instead of + and /)</li>
  <li>Wrong hash method — must be SHA-256 (S256), not plain</li>
  <li>Verifier stored in localStorage but cleared (private browsing, storage policies)</li>
</ul>

<h2>Correct PKCE implementation</h2>
<pre>// Generate verifier and store BEFORE redirecting
const verifier = generateVerifier();
sessionStorage.setItem('pkce_verifier', verifier); // store here

const challenge = await sha256Base64url(verifier);
// redirect to auth with code_challenge=challenge

// On callback — retrieve the STORED verifier
const verifier = sessionStorage.getItem('pkce_verifier'); // NOT regenerated
await exchangeCode(code, verifier);</pre>

<pre>function generateVerifier() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return btoa(String.fromCharCode(...array))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

async function sha256Base64url(str) {
  const data = new TextEncoder().encode(str);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}</pre>"""),

        ("invalid-grant-error",
         "invalid_grant OAuth error",
         "OAuth invalid_grant — Fix",
         "invalid_grant is the most common OAuth error. It has four causes. Here is how to diagnose which one you are hitting and fix it.",
         "/oauth/", "Debug your invalid_grant error → OAuthFixer",
         '<a href="/blog/oauth/fix-invalid-grant/">Full invalid_grant guide</a> <a href="/error/redirect-uri-mismatch/">redirect_uri_mismatch</a>',
         """
<div class="error-box"><div class="error-label">OAuth Error Response</div>{"error": "invalid_grant", "error_description": "Invalid authorization code"}</div>

<p class="lead">invalid_grant has four causes. Each one feels the same from the outside. Here is how to tell them apart and fix each one.</p>

<h2>Cause 1 — Authorization code expired (most common)</h2>
<p>Authorization codes expire in 10 minutes or less. Exchange the code immediately after the redirect — do not wait.</p>

<h2>Cause 2 — Code reused</h2>
<p>Each code can only be used once. React re-renders, duplicate API calls, or retries can call the exchange endpoint twice. The second call gets invalid_grant.</p>
<pre>// Prevent double exchange
const exchanging = sessionStorage.getItem('exchanging');
if (exchanging) return;
sessionStorage.setItem('exchanging', 'true');
await exchangeCode(code);
sessionStorage.removeItem('exchanging');</pre>

<h2>Cause 3 — PKCE verifier mismatch</h2>
<p>The code_verifier must match the code_challenge sent in the authorization request. If you regenerate it on the callback page, it will not match. Store it before redirecting, retrieve on callback.</p>

<h2>Cause 4 — Refresh token revoked or rotated</h2>
<p>If you are getting invalid_grant on a refresh call, the refresh token was revoked (user revoked access, password changed) or you used a stale token after rotation. Clear tokens and re-authenticate.</p>
<pre>try {
  const tokens = await refreshToken(storedRefreshToken);
} catch (err) {
  if (err.error === 'invalid_grant') {
    clearStoredTokens();
    redirectToLogin();
  }
}</pre>"""),
    ]

    for slug, error_str, title, desc, cta_url, cta_text, related, content in errors:
        write(f"blog/errors/{slug}/index.html", template(
            title=title, description=desc,
            canonical=f"{BASE_URL}/blog/errors/{slug}/",
            schema=make_schema(title, desc, f"{BASE_URL}/blog/errors/{slug}/",
                [("Find your exact error", "Match your console error to the one shown at the top of this page."),
                 ("Apply the fix", "Copy the fix for your framework."),
                 ("Verify with HttpFixer", "Use the live tool to confirm the fix worked.")],
                [("What causes this error?", f"See the explanation and causes in the article above."),
                 ("How do I fix it quickly?", "Use HttpFixer — it sends a real request to your API and shows exactly what is missing.")]),
            nav_label="Blog",
            breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → <a href="/blog/errors/">Error Pages</a> → {title}',
            tag="Error", tag_color=RED_TAG,
            h1=title,
            content=content,
            cta_url=cta_url, cta_text=cta_text, related=related
        ))


# ─── BLOG INDEX PAGES ─────────────────────────────────────────────────────────

def generate_indexes():
    print("\n📦 Generating blog index pages")

    categories = [
        ("cors", "CORS Fix Guides", "Fix CORS errors in Express, FastAPI, Nginx, Next.js, and more."),
        ("csp", "CSP Fix Guides", "Fix Content Security Policy errors and generate working CSP headers."),
        ("oauth", "OAuth Fix Guides", "Debug OAuth errors — invalid_grant, redirect_uri_mismatch, PKCE failures."),
        ("headers", "Security Headers Guides", "Add and fix HTTP security headers — HSTS, X-Frame-Options, CSP, and more."),
        ("performance", "Performance Guides", "Fix TTFB, cache headers, mixed content, and PageSpeed issues."),
        ("explainers", "Explainers", "Plain-English explanations of CORS, CSP, OAuth, HSTS, and more."),
        ("compare", "Comparisons", "Side-by-side comparisons of common web security concepts."),
        ("reference", "Reference Pages", "Quick reference for security headers, CORS headers, OAuth errors, and CSP directives."),
        ("platform", "Platform Guides", "Stack-specific guides for AWS Lambda, Cloudflare Workers, Netlify, Docker, and more."),
        ("errors", "Error Pages", "Short pages targeting exact browser console error strings."),
    ]

    for slug, name, desc in categories:
        os.makedirs(f"blog/{slug}", exist_ok=True)
        with open(f"blog/{slug}/index.html", "w") as f:
            f.write(template(
                title=f"{name} — HttpFixer Blog",
                description=desc,
                canonical=f"{BASE_URL}/blog/{slug}/",
                schema={"@context": "https://schema.org", "@type": "CollectionPage", "name": name, "url": f"{BASE_URL}/blog/{slug}/"},
                nav_label="Blog",
                breadcrumb=f'<a href="/">HttpFixer</a> → <a href="/blog/">Blog</a> → {name}',
                tag="Blog", tag_color=PURPLE_TAG,
                h1=name,
                content=f"<p class='lead'>{desc}</p><p>Browse the articles below — each one targets a specific error message or problem and gives you the exact fix for your stack.</p>",
                cta_url="/", cta_text="Scan your site → HttpFixer",
                related='<a href="/blog/">All articles</a> <a href="/glossary/">Glossary</a> <a href="/fix/">Fix guides</a>'
            ))
        print(f"  ✓ blog/{slug}/index.html")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🚀 HttpFixer Blog Generator")
    print("=" * 50)

    batch1_cors()
    batch2_csp()
    batch3_oauth()
    batch4_headers()
    batch5_performance()
    batch6_explainers()
    batch7_comparisons()
    batch8_reference()
    batch9_platform()
    batch10_errors()
    generate_indexes()

    # Count pages
    count = 0
    for root, dirs, files in os.walk("blog"):
        count += len([f for f in files if f.endswith(".html")])

    print(f"\n✅ Done — {count} blog pages generated")
    print("\nNext steps:")
    print("  git add -A")
    print('  git commit -m "feat: 61 blog articles — CORS, CSP, OAuth, Headers, Performance"')
    print("  git push origin main")
    print("  npx vercel --prod --force")
