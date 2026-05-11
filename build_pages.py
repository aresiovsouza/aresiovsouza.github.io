import re

# ── Shared nav HTML ──────────────────────────────────────────────────────────
NAV_HTML = '''<nav class="site-nav" id="site-nav">
  <div class="nav-inner">
    <a class="nav-logo" href="about.html">Aresio Souza</a>
    <div class="nav-links" id="nav-links">
      <a href="about.html" class="nav-item">About</a>
      <a href="blog.html" class="nav-item">Blog</a>
      <div class="dropdown">
        <button class="dropdown-toggle" aria-haspopup="true">Lists <span class="caret">&#9662;</span></button>
        <div class="dropdown-menu">
          <a href="bookmarks.html">Bookmarks</a>
          <a href="books.html">Books</a>
          <a href="tools.html">Tools</a>
        </div>
      </div>
      <a href="principles.html" class="nav-item">Principles</a>
      <a href="tinkering.html" class="nav-item">Tinkering</a>
    </div>
    <button class="nav-toggle" id="nav-toggle" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>'''

# ── Shared CSS ───────────────────────────────────────────────────────────────
NAV_CSS = '''
    /* ─── Site Navigation ───────────────────────────────────────────── */
    .site-nav {
      position: sticky;
      top: 0;
      z-index: 200;
      background: rgba(10,10,10,.96);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border-bottom: 1px solid rgba(201,168,76,.12);
    }
    .nav-inner {
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 clamp(1.25rem, 5vw, 2.5rem);
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 56px;
    }
    .nav-logo {
      font-family: var(--serif);
      font-size: 1rem;
      font-weight: 600;
      color: #fff;
      letter-spacing: .02em;
      text-decoration: none;
      flex-shrink: 0;
    }
    .nav-logo:hover { color: var(--gold); text-decoration: none; }
    .nav-links {
      display: flex;
      align-items: center;
      gap: clamp(1.25rem, 3vw, 2rem);
    }
    .nav-item {
      font-size: .73rem;
      font-weight: 500;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--muted);
      text-decoration: none;
      transition: color .2s;
    }
    .nav-item:hover, .nav-item.active { color: var(--gold); text-decoration: none; }

    /* Dropdown */
    .dropdown { position: relative; }
    .dropdown-toggle {
      font-family: var(--sans);
      font-size: .73rem;
      font-weight: 500;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--muted);
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
      display: flex;
      align-items: center;
      gap: .3rem;
      transition: color .2s;
    }
    .dropdown-toggle:hover { color: var(--gold); }
    .caret { font-size: .6rem; }
    .dropdown-menu {
      position: absolute;
      top: calc(100% + 1rem);
      left: 50%;
      transform: translateX(-50%) translateY(-6px);
      background: #181818;
      border: 1px solid rgba(201,168,76,.2);
      border-radius: 4px;
      padding: .4rem 0;
      min-width: 130px;
      opacity: 0;
      pointer-events: none;
      transition: opacity .18s, transform .18s;
    }
    .dropdown:hover .dropdown-menu,
    .dropdown:focus-within .dropdown-menu {
      opacity: 1;
      pointer-events: auto;
      transform: translateX(-50%) translateY(0);
    }
    .dropdown-menu a {
      display: block;
      padding: .55rem 1.25rem;
      font-size: .72rem;
      letter-spacing: .1em;
      text-transform: uppercase;
      color: var(--muted);
      text-decoration: none;
      transition: color .15s, background .15s;
    }
    .dropdown-menu a:hover {
      color: var(--gold);
      background: rgba(201,168,76,.05);
      text-decoration: none;
    }

    /* Hamburger */
    .nav-toggle {
      display: none;
      flex-direction: column;
      gap: 5px;
      background: none;
      border: none;
      cursor: pointer;
      padding: 4px;
    }
    .nav-toggle span {
      display: block;
      width: 22px;
      height: 2px;
      background: var(--muted);
      border-radius: 2px;
      transition: background .2s;
    }
    .nav-toggle:hover span { background: var(--gold); }

    @media (max-width: 640px) {
      .nav-toggle { display: flex; }
      .nav-links {
        display: none;
        position: absolute;
        top: 56px;
        left: 0; right: 0;
        background: rgba(12,12,12,.98);
        flex-direction: column;
        align-items: flex-start;
        gap: 0;
        border-bottom: 1px solid rgba(201,168,76,.12);
        padding: .5rem 0 1rem;
      }
      .nav-links.open { display: flex; }
      .nav-item, .dropdown-toggle {
        padding: .75rem clamp(1.25rem, 5vw, 2rem);
        width: 100%;
      }
      .dropdown-menu {
        position: static;
        transform: none !important;
        opacity: 1;
        pointer-events: auto;
        background: rgba(201,168,76,.04);
        border: none;
        border-left: 2px solid rgba(201,168,76,.15);
        border-radius: 0;
        margin-left: clamp(2rem, 7vw, 3rem);
        display: none;
        padding: .25rem 0;
      }
      .dropdown.open .dropdown-menu { display: block; }
      .dropdown-menu a { padding: .5rem 1rem; }
    }'''

# ── Shared JS ────────────────────────────────────────────────────────────────
NAV_JS = '''
  <script>
    // Mobile nav
    const toggle = document.getElementById('nav-toggle');
    const links  = document.getElementById('nav-links');
    toggle?.addEventListener('click', () => links.classList.toggle('open'));

    // Mobile dropdown
    document.querySelectorAll('.dropdown-toggle').forEach(btn => {
      btn.addEventListener('click', e => {
        if (window.innerWidth <= 640) {
          e.stopPropagation();
          btn.closest('.dropdown').classList.toggle('open');
        }
      });
    });

    // Mark active page
    const path = location.pathname.split('/').pop() || 'about.html';
    document.querySelectorAll('.nav-item').forEach(a => {
      if (a.getAttribute('href') === path) a.classList.add('active');
    });
  </script>'''

# ── Base template ────────────────────────────────────────────────────────────
def make_page(title, page_id, hero_bg, hero_label, hero_title, hero_sub,
              body_html, extra_css=''):
    hero_bg_css = (
        f"background-image: url('{hero_bg}'); background-size: cover; background-position: center center;"
        if hero_bg else
        "background: linear-gradient(160deg, #1c1408 0%, #0a0a0a 100%);"
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} – Aresio Souza</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --gold:       #c9a84c;
      --gold-light: #e2c97e;
      --dark:       #0f0f0f;
      --dark-2:     #1a1a1a;
      --dark-3:     #242424;
      --text:       #e8e4dc;
      --muted:      #9a9490;
      --serif:      'Playfair Display', Georgia, serif;
      --sans:       'Inter', system-ui, sans-serif;
      --max-w:      780px;
      --section-gap: clamp(3rem, 8vw, 5rem);
    }}
    html {{ scroll-behavior: smooth; }}
    body {{
      background: var(--dark);
      color: var(--text);
      font-family: var(--sans);
      font-size: clamp(15px, 1.6vw, 17px);
      line-height: 1.75;
      -webkit-font-smoothing: antialiased;
    }}
    h1, h2, h3 {{ font-family: var(--serif); line-height: 1.2; }}
    p {{ margin-bottom: 1.1em; }}
    p:last-child {{ margin-bottom: 0; }}
    a {{ color: var(--gold); text-decoration: none; transition: color .2s; }}
    a:hover {{ color: var(--gold-light); text-decoration: underline; }}
{NAV_CSS}
    /* ─── Hero ──────────────────────────────────────────────────── */
    .hero {{
      position: relative;
      width: 100%;
      min-height: clamp(320px, 45vw, 500px);
      display: flex;
      align-items: flex-end;
      justify-content: center;
      padding: clamp(2rem, 6vw, 4rem) 1.5rem clamp(2.5rem, 6vw, 4rem);
      {hero_bg_css}
      background-color: #0a0a0a;
      overflow: hidden;
      text-align: center;
    }}
    .hero::after {{
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, rgba(8,8,8,.92) 0%, rgba(8,8,8,.45) 45%, rgba(8,8,8,.15) 100%);
    }}
    .hero-content {{ position: relative; z-index: 1; }}
    .hero-eyebrow {{
      font-size: .75rem; font-weight: 500; letter-spacing: .2em;
      text-transform: uppercase; color: var(--gold); margin-bottom: .75rem;
    }}
    .hero h1 {{
      font-size: clamp(2.4rem, 7vw, 4rem); font-weight: 700;
      color: #fff; margin-bottom: .6rem;
    }}
    .hero-rule {{ width: 3rem; height: 2px; background: var(--gold); margin: 0 auto .9rem; }}
    .hero-sub {{
      font-size: clamp(.8rem, 1.4vw, .95rem); font-weight: 300;
      letter-spacing: .12em; text-transform: uppercase; color: var(--muted);
    }}
    /* ─── Page layout ───────────────────────────────────────────── */
    .page-wrap {{
      max-width: var(--max-w);
      margin: 0 auto;
      padding: 0 clamp(1.25rem, 5vw, 2.5rem);
    }}
    /* ─── Placeholder section ───────────────────────────────────── */
    .placeholder {{
      padding: var(--section-gap) 0;
      text-align: center;
    }}
    .placeholder-icon {{
      font-size: 2.5rem;
      margin-bottom: 1.25rem;
      opacity: .4;
    }}
    .placeholder h2 {{
      font-family: var(--serif);
      font-size: clamp(1.4rem, 3.5vw, 1.9rem);
      color: #fff;
      margin-bottom: .75rem;
    }}
    .placeholder p {{
      color: var(--muted);
      font-weight: 300;
      max-width: 460px;
      margin: 0 auto;
    }}
    .placeholder-rule {{
      width: 3rem; height: 1px;
      background: rgba(201,168,76,.3);
      margin: 1.75rem auto;
    }}
    /* ─── Footer ────────────────────────────────────────────────── */
    .footer-strip {{
      background: var(--dark-2);
      border-top: 1px solid rgba(201,168,76,.1);
      text-align: center;
      padding: 1.5rem;
      font-size: .75rem;
      color: var(--muted);
      letter-spacing: .06em;
    }}
{extra_css}
  </style>
</head>
<body>

{NAV_HTML}

<section class="hero">
  <div class="hero-content">
    <p class="hero-eyebrow">{hero_label}</p>
    <h1>{hero_title}</h1>
    <div class="hero-rule"></div>
    <p class="hero-sub">{hero_sub}</p>
  </div>
</section>

<div class="page-wrap">
{body_html}
</div>

<div class="footer-strip">
  &copy; 2026 Aresio Souza &nbsp;&middot;&nbsp; Rio de Janeiro &rarr; New York &rarr; New Jersey &rarr; California
</div>

{NAV_JS}
</body>
</html>'''

# ── Placeholder body ─────────────────────────────────────────────────────────
def placeholder_body(icon, heading, note):
    return f'''  <div class="placeholder">
    <div class="placeholder-icon">{icon}</div>
    <h2>{heading}</h2>
    <div class="placeholder-rule"></div>
    <p>{note}</p>
  </div>'''

# ── Build pages ───────────────────────────────────────────────────────────────
pages = [
    ('blog', make_page(
        'Blog', 'blog', None,
        'Blog', 'Writing', 'Thoughts &nbsp;·&nbsp; Ideas &nbsp;·&nbsp; Observations',
        placeholder_body('✍️', 'Posts Coming Soon',
            'Essays, reflections, and ideas on ergonomics, health, technology, sport, and life between two cultures.')
    )),
    ('bookmarks', make_page(
        'Bookmarks', 'bookmarks', None,
        'Lists', 'Bookmarks', 'Links Worth Keeping',
        placeholder_body('🔖', 'Curated Links Coming Soon',
            'Articles, papers, tools, and rabbit holes worth saving — organized so they\'re actually findable.')
    )),
    ('books', make_page(
        'Books', 'books', None,
        'Lists', 'Books', 'Reading List',
        placeholder_body('📚', 'Reading List Coming Soon',
            'Books that shaped how I think — across medicine, philosophy, sport, and everything in between.')
    )),
    ('tools', make_page(
        'Tools', 'tools', None,
        'Lists', 'Tools', 'What I Use',
        placeholder_body('🛠️', 'Tools List Coming Soon',
            'Software, hardware, and systems that make work and life run a little more smoothly.')
    )),
    ('principles', make_page(
        'Principles', 'principles',
        'principles-hero.jpg',   # ← save the Japanese illustration as this filename
        'Principles', 'Principles', 'The beliefs that guide how I live and work',
        placeholder_body('⛩️', 'Principles Coming Soon',
            'A working set of beliefs about health, discipline, learning, and what it means to show up consistently over a long life.')
    )),
    ('tinkering', make_page(
        'Tinkering', 'tinkering', None,
        'Tinkering', 'Tinkering', 'Experiments &nbsp;·&nbsp; Projects &nbsp;·&nbsp; Curiosities',
        placeholder_body('⚙️', 'Projects Coming Soon',
            'Side projects, experiments, and things built out of curiosity — where professional knowledge meets the joy of making.')
    )),
]

out = '/sessions/jolly-charming-hawking/mnt/outputs/'
for name, html in pages:
    with open(f'{out}{name}.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Created {name}.html')

print('All done.')
