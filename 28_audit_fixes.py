#!/usr/bin/env python3
"""
HttpFixer — Audit Fixes
Fixes all 10 items from the live site audit:

🔴 Critical:
  1. Homepage <title> → "HttpFixer — Fix CORS, CSP, OAuth & HTTP Header Errors"
  2. Homepage H1 → site-level headline + tool grid
  3. (GSC check — manual, not scriptable)
  4. (GitHub repo rename — manual, not scriptable)

🟡 Important:
  5. Add Blog link to nav on ALL pages
  6. Fix footer — remove external network links, replace with internal links
  7. Footer blog section → single "Visit the Blog →" link

🔵 Nice to have:
  8. Verify/add meta descriptions (already on all pages — skip)
  9. Add Open Graph tags to all pages
  10. Create custom 404.html

Usage:
  cd ~/Projects/stackfix
  cp ~/Downloads/28_audit_fixes.py .
  python3 28_audit_fixes.py
  git add -A && git commit -m "fix: audit fixes — title, H1, nav blog link, footer, OG tags, 404" && git push origin main && npx vercel --prod --force

Manual tasks (not scriptable):
  - Rename GitHub repo: github.com/metriclogic26/webfix → httpfixer
    Settings → Repository name → rename
  - GSC: check Coverage for crawl errors / noindex
"""

import os, re

BASE_URL = "https://httpfixer.dev"
SKIP_DIRS = {".git", "node_modules", ".vercel", ".next", "__pycache__"}

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def all_html_files():
    """Walk project and return all .html file paths."""
    files = []
    for root, dirs, fnames in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fnames:
            if f.endswith(".html"):
                files.append(os.path.join(root, f))
    return files


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def patch(path, old, new, label=""):
    content = read(path)
    if old not in content:
        return False
    write(path, content.replace(old, new, 1))
    return True


# ─── FIX 1 — HOMEPAGE TITLE ───────────────────────────────────────────────────

def fix_homepage_title():
    print("\n🔴 Fix 1 — Homepage title")
    path = "index.html"
    if not os.path.exists(path):
        print("  ⚠️  index.html not found")
        return

    content = read(path)

    # Fix <title>
    old_title_patterns = [
        "<title>HeadersFixer · HttpFixer</title>",
        "<title>HeadersFixer — HttpFixer</title>",
        "<title>HeadersFixer | HttpFixer</title>",
    ]
    new_title = "<title>HttpFixer — Fix CORS, CSP, OAuth &amp; HTTP Header Errors</title>"

    fixed = False
    for old in old_title_patterns:
        if old in content:
            content = content.replace(old, new_title, 1)
            fixed = True
            break

    # Fallback: find any <title>...</title> and replace
    if not fixed:
        content = re.sub(r'<title>[^<]*</title>', new_title, content, count=1)
        fixed = True

    # Fix og:title to match
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        '<meta property="og:title" content="HttpFixer — Fix CORS, CSP, OAuth &amp; HTTP Header Errors">',
        content
    )

    # Fix meta description on homepage
    homepage_desc = "Fix CORS errors, CSP violations, OAuth failures, and HTTP security header misconfigurations instantly. Free browser-based developer tools — no signup, no backend."
    content = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        f'\\g<1>{homepage_desc}\\g<2>',
        content,
        count=1
    )

    write(path, content)
    print("  ✓ index.html — title, og:title, meta description updated")


# ─── FIX 2 — HOMEPAGE H1 ──────────────────────────────────────────────────────

def fix_homepage_h1():
    print("\n🔴 Fix 2 — Homepage H1 + hero section")
    path = "index.html"
    if not os.path.exists(path):
        print("  ⚠️  index.html not found")
        return

    content = read(path)

    # We'll inject a new hero section right before the first <h1> or near the top of <main>
    # Strategy: find the tool-specific H1 and replace with site-level one

    old_h1_patterns = [
        "Security scanners give you a D. HeadersFixer gives you the exact config to paste.",
        "HeadersFixer gives you the exact config to paste.",
        "Fixers, not checkers.",
    ]

    new_hero = """<div class="site-hero">
  <h1>Fix CORS, CSP, OAuth and HTTP header errors — instantly.</h1>
  <p class="site-lead">Paste your URL or config. Get the exact copy-paste fix for your stack — Nginx, Vercel, Express, FastAPI, Cloudflare, and more. No signup. No backend. Nothing leaves your browser.</p>
  <div class="tool-pills">
    <a href="/" class="pill pill-red">🔒 HeadersFixer</a>
    <a href="/cors/" class="pill pill-purple">⚡ CORSFixer</a>
    <a href="/oauth/" class="pill pill-orange">🔑 OAuthFixer</a>
    <a href="/csp/" class="pill pill-green">🛡 CSPFixer</a>
    <a href="/edge/" class="pill pill-orange">📦 EdgeFix</a>
    <a href="/speedfixer/" class="pill pill-purple">🚀 SpeedFixer</a>
  </div>
</div>
<style>
  .site-hero{padding:2rem 0 1.5rem;border-bottom:1px solid var(--border);margin-bottom:1.5rem}
  .site-hero h1{font-size:1.7rem;font-weight:600;line-height:1.25;margin-bottom:0.75rem;color:var(--text)}
  .site-lead{font-size:14px;opacity:0.7;max-width:580px;line-height:1.8;margin-bottom:1.25rem}
  .tool-pills{display:flex;flex-wrap:wrap;gap:0.5rem}
  .pill{display:inline-block;padding:0.3rem 0.75rem;border-radius:4px;font-size:12px;font-weight:500;text-decoration:none;border:1px solid var(--border);color:var(--text);transition:all 0.15s}
  .pill:hover{border-color:currentColor;opacity:1}
  .pill-purple:hover{color:var(--purple);border-color:var(--purple)}
  .pill-green:hover{color:var(--green);border-color:var(--green)}
  .pill-orange:hover{color:var(--orange);border-color:var(--orange)}
  .pill-red:hover{color:var(--red);border-color:var(--red)}
  @media(max-width:600px){.site-hero h1{font-size:1.3rem}}
</style>"""

    # Try to find and replace the old H1 section
    h1_pattern = re.search(r'<h1[^>]*>.*?</h1>', content, re.DOTALL)
    if h1_pattern:
        old_h1_block = h1_pattern.group(0)
        # Only replace the very first H1 on the page
        if any(phrase in old_h1_block for phrase in ["HeadersFixer", "Fixers, not checkers", "Security scanner"]):
            content = content.replace(old_h1_block, new_hero, 1)
            write(path, content)
            print("  ✓ index.html — H1 replaced with site-level hero")
            return

    # Fallback: inject after <main> opening tag
    if "<main" in content:
        content = re.sub(r'(<main[^>]*>)', r'\1\n' + new_hero, content, count=1)
        write(path, content)
        print("  ✓ index.html — hero injected after <main>")
    else:
        print("  ⚠️  Could not find injection point for H1 — check index.html manually")


# ─── FIX 5 — ADD BLOG TO NAV ──────────────────────────────────────────────────

def add_blog_to_nav():
    print("\n🟡 Fix 5 — Add Blog link to nav on all pages")

    files = all_html_files()
    patched = 0
    skipped = 0

    # Patterns for the end of the nav right section — add Blog after Speed
    old_patterns = [
        '<a href="/speedfixer/">Speed</a>\n  </div>',
        '<a href="/speedfixer/">Speed</a></div>',
        '<a href="/speedfixer/">Speed</a>\n    </div>',
    ]
    new_suffix_map = {
        '<a href="/speedfixer/">Speed</a>\n  </div>': '<a href="/speedfixer/">Speed</a><a href="/blog/">Blog</a>\n  </div>',
        '<a href="/speedfixer/">Speed</a></div>': '<a href="/speedfixer/">Speed</a><a href="/blog/">Blog</a></div>',
        '<a href="/speedfixer/">Speed</a>\n    </div>': '<a href="/speedfixer/">Speed</a><a href="/blog/">Blog</a>\n    </div>',
    }

    for fpath in files:
        content = read(fpath)

        if '<a href="/blog/">Blog</a>' in content:
            skipped += 1
            continue

        fixed = False
        for old, new in new_suffix_map.items():
            if old in content:
                write(fpath, content.replace(old, new, 1))
                fixed = True
                patched += 1
                break

        # Fallback: regex replace
        if not fixed and '/speedfixer/' in content and 'Speed</a>' in content:
            new_content = re.sub(
                r'(<a href="/speedfixer/">Speed</a>)(.*?</div>)',
                r'\1<a href="/blog/">Blog</a>\2',
                content,
                count=1,
                flags=re.DOTALL
            )
            if new_content != content:
                write(fpath, new_content)
                patched += 1

    print(f"  ✓ Blog link added to {patched} pages ({skipped} already had it)")


# ─── FIX 6 — FIX FOOTER LINKS ─────────────────────────────────────────────────

def fix_footer_links():
    print("\n🟡 Fix 6 — Fix footer links (remove external network links)")

    files = all_html_files()
    patched = 0

    # Old footer span with external sites
    old_footers = [
        'HttpFixer by MetricLogic · <a href="https://configclarity.dev">configclarity.dev</a> · <a href="https://domainpreflight.dev">domainpreflight.dev</a> · <a href="https://packagefix.dev">packagefix.dev</a>',
        'HttpFixer by MetricLogic · <a href="https://configclarity.dev">configclarity.dev</a> · <a href="https://domainpreflight.dev">domainpreflight.dev</a> · <a href="https://packagefix.dev">packagefix.dev</a>',
    ]

    new_footer_left = 'HttpFixer by <a href="https://metriclogic.dev">MetricLogic</a> · <a href="/blog/">Blog</a> · <a href="/generators/">Generators</a> · <a href="/changelog/">Changelog</a>'

    for fpath in files:
        content = read(fpath)
        fixed = False

        for old in old_footers:
            if old in content:
                content = content.replace(old, new_footer_left, 1)
                fixed = True
                break

        # Broader regex fallback
        if not fixed and 'configclarity.dev' in content:
            new_content = re.sub(
                r'HttpFixer by MetricLogic[^<]*(<a[^>]*>[^<]*</a>[^<]*)*',
                new_footer_left,
                content,
                count=1
            )
            if new_content != content:
                content = new_content
                fixed = True

        if fixed:
            write(fpath, content)
            patched += 1

    print(f"  ✓ Footer updated on {patched} pages")


# ─── FIX 7 — FOOTER BLOG SECTION ──────────────────────────────────────────────

def fix_footer_blog_section():
    print("\n🟡 Fix 7 — Update footer blog section to single link")

    files = all_html_files()
    patched = 0

    # The auto-injected related articles block — replace with simpler link
    old_section_marker = 'id="related-articles"'

    simple_blog_bar = """
<!-- Blog bar — streamlined -->
<div style="border-top:1px solid #252836;padding:1rem 1.5rem;background:#0B0D14;font-family:'JetBrains Mono',monospace;text-align:center">
  <a href="/blog/" style="color:#6C63FF;text-decoration:none;font-size:13px;opacity:0.8">
    📖 HttpFixer Blog — 61 fix guides, explainers, and references →
  </a>
</div>"""

    for fpath in files:
        content = read(fpath)

        if old_section_marker not in content:
            continue

        # Replace the entire related-articles section with simple bar
        # Find from <!-- Related Articles to the closing </style> after it
        new_content = re.sub(
            r'<!-- Related Articles.*?</style>',
            simple_blog_bar,
            content,
            count=1,
            flags=re.DOTALL
        )

        if new_content != content:
            write(fpath, new_content)
            patched += 1

    print(f"  ✓ Blog section simplified on {patched} tool pages")


# ─── FIX 9 — OPEN GRAPH TAGS ──────────────────────────────────────────────────

def add_og_tags():
    print("\n🔵 Fix 9 — Add Open Graph tags to all pages")

    files = all_html_files()
    patched = 0
    skipped = 0

    # OG image — a simple branded URL (we'll use a text-based fallback)
    OG_IMAGE = f"{BASE_URL}/og-image.png"

    for fpath in files:
        content = read(fpath)

        # Skip if OG tags already comprehensive
        if 'og:image' in content:
            skipped += 1
            continue

        # Extract title and description from the page
        title_match = re.search(r'<title>([^<]+)</title>', content)
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
        canon_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)

        title = title_match.group(1) if title_match else "HttpFixer"
        desc = desc_match.group(1) if desc_match else "Free browser-based developer tools to fix HTTP errors."
        url = canon_match.group(1) if canon_match else BASE_URL

        # Build OG block
        og_block = f"""  <meta property="og:type" content="website">
  <meta property="og:site_name" content="HttpFixer">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@metriclogic">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc[:200]}">
  <meta name="twitter:image" content="{OG_IMAGE}">"""

        # Check if og:title and og:description already exist — add only og:image etc
        if 'og:title' in content and 'og:description' in content:
            # Just add og:image, og:type, twitter tags
            og_block = f"""  <meta property="og:type" content="website">
  <meta property="og:site_name" content="HttpFixer">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@metriclogic">
  <meta name="twitter:image" content="{OG_IMAGE}">"""

        # Inject before </head>
        new_content = content.replace('</head>', og_block + '\n</head>', 1)
        if new_content != content:
            write(fpath, new_content)
            patched += 1

    print(f"  ✓ OG tags added to {patched} pages ({skipped} already complete)")


# ─── FIX 10 — CUSTOM 404 PAGE ─────────────────────────────────────────────────

def create_404():
    print("\n🔵 Fix 10 — Create custom 404.html")

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 — Page Not Found · HttpFixer</title>
  <meta name="robots" content="noindex">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root{--bg:#0B0D14;--surface:#12151F;--border:#252836;--purple:#6C63FF;--green:#22C55E;--orange:#F97316;--red:#EF4444;--text:#E2E4F0;}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:var(--bg);color:var(--text);font-family:"JetBrains Mono",monospace;font-size:14px;min-height:100vh;display:flex;flex-direction:column}
    nav{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;border-bottom:1px solid var(--border);background:var(--surface)}
    nav .brand{font-weight:600;color:var(--text);text-decoration:none}
    nav .brand span{color:var(--purple)}
    nav .right{display:flex;gap:1rem}
    nav a{color:var(--text);text-decoration:none;opacity:0.6;font-size:13px}
    nav a:hover{color:var(--purple);opacity:1}
    main{flex:1;display:flex;align-items:center;justify-content:center;padding:2rem}
    .box{max-width:500px;text-align:center}
    .code{font-size:5rem;font-weight:600;color:var(--purple);opacity:0.3;line-height:1;margin-bottom:1rem}
    h1{font-size:1.2rem;font-weight:600;margin-bottom:0.75rem}
    p{opacity:0.6;font-size:13px;line-height:1.7;margin-bottom:2rem}
    .tools{display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;margin-bottom:2rem}
    .tool-link{display:block;padding:0.75rem;background:var(--surface);border:1px solid var(--border);border-radius:6px;text-decoration:none;color:var(--text);font-size:12px;transition:border-color 0.2s}
    .tool-link:hover{border-color:var(--purple);color:var(--purple)}
    .tool-link .icon{display:block;font-size:1.2rem;margin-bottom:0.3rem}
    .home-link{display:inline-block;padding:0.6rem 1.25rem;background:var(--purple);color:white;text-decoration:none;border-radius:4px;font-size:13px}
    footer{padding:1rem 2rem;border-top:1px solid var(--border);font-size:12px;text-align:center;opacity:0.4}
    @media(max-width:500px){.tools{grid-template-columns:repeat(2,1fr)}.code{font-size:3rem}}
  </style>
</head>
<body>
<nav>
  <a href="/" class="brand">HttpFixer <span>/</span> 404</a>
  <div class="right">
    <a href="/">Headers</a>
    <a href="/cors/">CORS</a>
    <a href="/oauth/">OAuth</a>
    <a href="/csp/">CSP</a>
    <a href="/blog/">Blog</a>
  </div>
</nav>
<main>
  <div class="box">
    <div class="code">404</div>
    <h1>Page not found</h1>
    <p>The URL you requested does not exist. Try one of the tools below — or head back to the homepage.</p>
    <div class="tools">
      <a href="/" class="tool-link"><span class="icon">🔒</span>HeadersFixer</a>
      <a href="/cors/" class="tool-link"><span class="icon">⚡</span>CORSFixer</a>
      <a href="/oauth/" class="tool-link"><span class="icon">🔑</span>OAuthFixer</a>
      <a href="/csp/" class="tool-link"><span class="icon">🛡</span>CSPFixer</a>
      <a href="/edge/" class="tool-link"><span class="icon">📦</span>EdgeFix</a>
      <a href="/speedfixer/" class="tool-link"><span class="icon">🚀</span>SpeedFixer</a>
    </div>
    <a href="/" class="home-link">← Back to HttpFixer</a>
  </div>
</main>
<footer>HttpFixer by MetricLogic · MIT Licensed · <a href="https://github.com/metriclogic26/httpfixer" style="color:inherit">GitHub</a></footer>
</body>
</html>"""

    with open("404.html", "w") as f:
        f.write(html)
    print("  ✓ 404.html created")

    # Also create a vercel.json entry if not already there
    vercel_path = "vercel.json"
    if os.path.exists(vercel_path):
        content = read(vercel_path)
        if '"404"' not in content and 'cleanUrls' not in content:
            # Inject cleanUrls and 404 into vercel.json
            try:
                import json
                config = json.loads(content)
                config["cleanUrls"] = True
                # Vercel uses 404.html automatically — no extra config needed
                write(vercel_path, json.dumps(config, indent=2))
                print("  ✓ vercel.json — cleanUrls enabled")
            except Exception as e:
                print(f"  ⚠️  vercel.json update skipped: {e}")
    else:
        # Create minimal vercel.json
        vercel_config = {
            "cleanUrls": True
        }
        with open(vercel_path, "w") as f:
            import json
            json.dump(vercel_config, f, indent=2)
        print("  ✓ vercel.json created with cleanUrls")


# ─── BONUS — OG IMAGE PLACEHOLDER ────────────────────────────────────────────

def create_og_image_svg():
    """Create a simple SVG-based OG image placeholder."""
    print("\n🔵 Bonus — Create og-image.svg (1200x630)")

    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#0B0D14"/>
  <rect x="0" y="0" width="8" height="630" fill="#6C63FF"/>
  <text x="80" y="220" font-family="monospace" font-size="72" font-weight="bold" fill="#E2E4F0">HttpFixer</text>
  <text x="80" y="300" font-family="monospace" font-size="28" fill="#6C63FF">Fix CORS · CSP · OAuth · Security Headers</text>
  <text x="80" y="370" font-family="monospace" font-size="20" fill="#E2E4F0" opacity="0.5">Free browser-based developer tools. No signup. No backend.</text>
  <rect x="80" y="440" width="180" height="52" rx="6" fill="#6C63FF" opacity="0.15" stroke="#6C63FF" stroke-width="1"/>
  <text x="170" y="472" font-family="monospace" font-size="14" fill="#6C63FF" text-anchor="middle">HeadersFixer</text>
  <rect x="280" y="440" width="180" height="52" rx="6" fill="#6C63FF" opacity="0.15" stroke="#6C63FF" stroke-width="1"/>
  <text x="370" y="472" font-family="monospace" font-size="14" fill="#6C63FF" text-anchor="middle">CORSFixer</text>
  <rect x="480" y="440" width="180" height="52" rx="6" fill="#6C63FF" opacity="0.15" stroke="#6C63FF" stroke-width="1"/>
  <text x="570" y="472" font-family="monospace" font-size="14" fill="#6C63FF" text-anchor="middle">OAuthFixer</text>
  <rect x="680" y="440" width="180" height="52" rx="6" fill="#6C63FF" opacity="0.15" stroke="#6C63FF" stroke-width="1"/>
  <text x="770" y="472" font-family="monospace" font-size="14" fill="#6C63FF" text-anchor="middle">CSPFixer</text>
  <text x="1120" y="590" font-family="monospace" font-size="14" fill="#E2E4F0" opacity="0.3" text-anchor="end">httpfixer.dev</text>
</svg>"""

    with open("og-image.svg", "w") as f:
        f.write(svg)
    print("  ✓ og-image.svg created (use as OG image or convert to PNG)")
    print("  ℹ️  For a proper PNG: open in browser, screenshot, or use imagemagick:")
    print("     convert og-image.svg og-image.png")


# ─── PRINT MANUAL TASKS ───────────────────────────────────────────────────────

def print_manual_tasks():
    print("""
📋 Manual tasks (not scriptable):

  🔴 Fix 3 — Check GSC for crawl errors:
     search.google.com/search-console → Coverage → Errors tab
     Look for: noindex tags, crawl anomalies, redirect errors

  🔴 Fix 4 — Rename GitHub repo:
     github.com/metriclogic26/webfix → Settings → Repository name → "httpfixer"
     After renaming, update footer GitHub link from:
       github.com/metriclogic26/webfix
     to:
       github.com/metriclogic26/httpfixer
     (run 28b_fix_github_link.py after repo rename, or update manually)

  🔵 OG Image — convert SVG to PNG if needed:
     brew install imagemagick
     convert og-image.svg og-image.png
     (or just upload og-image.svg — most platforms accept SVG for OG)
""")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🚀 HttpFixer — Audit Fixes")
    print("=" * 50)

    fix_homepage_title()       # Fix 1
    fix_homepage_h1()          # Fix 2
    add_blog_to_nav()          # Fix 5
    fix_footer_links()         # Fix 6
    fix_footer_blog_section()  # Fix 7
    add_og_tags()              # Fix 9
    create_404()               # Fix 10
    create_og_image_svg()      # Bonus

    print_manual_tasks()

    print("""
✅ Script complete. Run:

  git add -A
  git commit -m "fix: audit fixes — title, H1, nav blog link, footer, OG tags, 404"
  git push origin main
  npx vercel --prod --force

After deploy, verify:
  curl -s https://httpfixer.dev/ | grep "<title>"
  curl -s https://httpfixer.dev/ | grep "og:image"
  curl -I https://httpfixer.dev/nonexistent-page  (should return 404 with custom page)
""")
