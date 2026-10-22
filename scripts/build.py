"""Génère le site statique dans public/ à partir de apps.json.

Usage : python scripts/build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE_URL = "https://apps.maythayus1.store"
STORE = "https://maythayus1.store/"
GITHUB = "https://github.com/maythayus"
SOCIAL = [
    ("Boutique", STORE),
    ("YouTube", "https://www.youtube.com/@maythayus1?sub_confirmation=1"),
    ("SoundCloud", "https://soundcloud.com/user-807863479-448305626"),
    ("GitHub", GITHUB),
    ("XDA", "https://xdaforums.com/m/maythayus.7719338/"),
]

e = html.escape


def page(title, description, body, depth, path):
    up = "../" * depth
    footer_links = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIAL)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE_URL}/{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE_URL}/assets/logo.jpg">
<meta name="theme-color" content="#141618">
<link rel="icon" href="{up}assets/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}styles.css">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up or './'}"><img src="{up}assets/logo.jpg" alt="">MAYTHAYUS APPS</a>
<nav><a href="{up}#apps">Apps</a><a href="{STORE}">Boutique</a><a href="{GITHUB}">GitHub</a></nav>
</div></header>
{body}
<footer><div class="wrap">
<span>&copy; Maythayus &middot; C'est Marseille bébé</span>
<span>{footer_links}</span>
</div></footer>
</body>
</html>
"""


def card(app):
    platform = app.get("platform", "Android")
    return f"""<a class="card" href="{app['slug']}/">
<span class="tag">{e(app['category'])} &middot; {e(platform)}</span>
<h3>{e(app['name'])}</h3>
<p>{e(app['tagline'])}</p>
<p>{e(app['summary'])}</p>
<span class="more">Découvrir &rarr;</span>
</a>"""


def app_page(app):
    repo = f"{GITHUB}/{app['repo']}"
    buttons = []
    if app.get("download"):
        buttons.append(f'<a class="btn primary" href="{app["download"]}">{e(app["downloadLabel"])}</a>')
    buttons.append(f'<a class="btn {"ghost" if buttons else "primary"}" href="{repo}/releases/latest">Dernière version</a>')
    buttons.append(f'<a class="btn ghost" href="{repo}">Code source</a>')
    for link in app.get("links", []):
        buttons.append(f'<a class="btn orange" href="{link["url"]}">{e(link["label"])}</a>')
    features = "".join(f"<li>{e(f)}</li>" for f in app["features"])
    note = f'<p class="note">{e(app["note"])}</p>' if app.get("note") else ""
    img = f'<img class="shot" src="../{app["image"]}" alt="Capture de {e(app["name"])}" loading="lazy">' if app.get("image") else ""
    platform = app.get("platform", "Android")
    body = f"""<main class="wrap">
<section class="app-hero">
<a class="back" href="../">&larr; Toutes les apps</a>
<p><span class="tag">{e(app['category'])} &middot; {e(platform)}</span></p>
<h1>{e(app['name'])}</h1>
<p class="lead">{e(app['tagline'])} {e(app['summary'])}</p>
<div class="actions left">{''.join(buttons)}</div>
</section>
<section class="app-body{' has-img' if img else ''}">
<div><h2>Fonctionnalités</h2><ul>{features}</ul>{note}</div>
{img}
</section>
</main>"""
    return page(f"{app['name']} - {app['tagline']} | Maythayus Apps", app["summary"], body, 1, f"{app['slug']}/")


def main():
    apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
    cards = "\n".join(card(a) for a in apps)
    body = f"""<section class="hero"><div class="wrap">
<h1>Les apps <span>Maythayus</span></h1>
<p>Applications Android open source pour le terrain, l'urgence, la sécurité et l'audio. Codées à Marseille, téléchargeables gratuitement.</p>
<div class="actions"><a class="btn primary" href="#apps">Voir les apps</a><a class="btn orange" href="{STORE}">La boutique</a></div>
</div></section>
<main class="wrap" id="apps">
<h2 class="section">Toutes les apps</h2>
<div class="grid">
{cards}
</div>
</main>"""
    description = "Applications Android open source de Maythayus : SatTemps, SuperSOS, Intercom2SOS, GeoFlash, TrustLink et plus."
    (PUBLIC / "index.html").write_text(page("Maythayus Apps - Applications Android open source", description, body, 0, ""), encoding="utf-8")
    not_found = """<main class="wrap"><section class="app-hero"><h1>Page introuvable</h1>
<p class="lead">Cette page n'existe pas (ou plus).</p>
<div class="actions left"><a class="btn primary" href="/">Retour aux apps</a></div></section></main>"""
    (PUBLIC / "404.html").write_text(page("Page introuvable | Maythayus Apps", description, not_found, 0, "404"), encoding="utf-8")
    for app in apps:
        out = PUBLIC / app["slug"]
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(app_page(app), encoding="utf-8")
    urls = [""] + [f"{a['slug']}/" for a in apps]
    sitemap = "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>" for u in urls)
    (PUBLIC / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>\n',
        encoding="utf-8",
    )
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(apps)} apps -> {PUBLIC}")


if __name__ == "__main__":
    main()
