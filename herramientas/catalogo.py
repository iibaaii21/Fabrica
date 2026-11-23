"""Antes generaba docs/catalogo/. Desde el 23/11 docs/ redirige a las webs nuevas (el catálogo está en Cellmate y Nimbloom, generado por sites.py), así que no hace nada."""
import sys
print("catalogo.py: docs/ ya redirige a las webs nuevas; no hay nada que generar"); sys.exit(0)
"""Genera docs/catalogo/ desde herramientas/catalogo.json. Uso: python3 herramientas/catalogo.py"""
import json, os, html
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(R, 'herramientas/catalogo.json')))
OUT = os.path.join(R, 'docs/catalogo'); os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
e = html.escape
cards = {}
for p in P:
    im = Image.open(os.path.join(R, p['img'])).convert('RGB'); im.thumbnail((720, 720))
    im.save(os.path.join(OUT, 'img', p['id'] + '.jpg'), quality=82, optimize=True)
    w, h = im.size
    btns = []
    if p.get('jugar'): btns.append(f'<a class="btn" href="{e(p["jugar"])}">Jugar gratis</a>')
    if p.get('comprar'): btns.append(f'<a class="btn" href="{e(p["comprar"])}" rel="noopener">{e(p.get("boton", "Comprar"))}</a>')
    for t, u in p.get('extra', []): btns.append(f'<a class="btn ghost" href="{e(u)}">{e(t)}</a>')
    if not p.get('comprar') and not p.get('jugar') and p['precio'] != 'Gratis': btns.append('<span class="soon">Muy pronto a la venta</span>')
    elif not p.get('comprar') and not p.get('jugar'): btns.append('<span class="soon">Muy pronto</span>')
    audio = f'<audio controls preload="none" src="{e(p["audio"])}"></audio>' if p.get('audio') else ''
    cards.setdefault(p['cat'], []).append(f'''<article class="item" id="{e(p['id'])}">
  <img src="img/{e(p['id'])}.jpg" width="{w}" height="{h}" alt="{e(p['nombre'])}" loading="lazy">
  <div class="body"><div class="top"><h3>{e(p['nombre'])}</h3><span class="price">{e(p['precio'])}</span></div>
  <p>{e(p['desc'])}</p>{audio}<div class="btns">{''.join(btns)}</div></div>
</article>''')
secs = ''.join(f'<section><h2>{e(c)}</h2><div class="cards">{"".join(v)}</div></section>' for c, v in cards.items())
page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Catálogo: plantillas, juegos y sonidos</title>
<meta name="description" content="Plantillas de Excel y Google Sheets en español (oposiciones, boda, autónomos), juegos gratis para el navegador y packs de sonido y música para desarrolladores.">
<link rel="canonical" href="https://iibaaii21.github.io/Fabrica/catalogo/">
<style>
:root{{--bg:#f7f5f0;--card:#fff;--ink:#1f2a44;--muted:#5a6275;--line:#e2ddd1;--gold:#b08d4c}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI",Roboto,system-ui,sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:28px 16px 60px;display:grid;gap:30px}}
nav{{font-size:14px;display:flex;gap:14px;flex-wrap:wrap}} nav a{{color:var(--muted)}}
h1{{font-size:clamp(28px,5vw,42px);line-height:1.1;margin:0;text-wrap:balance}}
.lead{{color:var(--muted);margin:6px 0 0;max-width:640px}}
h2{{font-size:22px;margin:0 0 14px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}}
.item{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.item img{{width:100%;height:auto;aspect-ratio:auto;display:block;background:#eee}}
.body{{padding:16px 18px 18px;display:grid;gap:10px;flex:1;align-content:start}}
.top{{display:flex;justify-content:space-between;gap:10px;align-items:baseline}}
h3{{margin:0;font-size:18px;line-height:1.25}}
.price{{font-weight:800;white-space:nowrap;color:var(--gold)}}
p{{margin:0;color:var(--muted);font-size:15px}}
audio{{width:100%;height:36px}}
.btns{{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}}
.btn{{background:var(--ink);color:#fff;text-decoration:none;font-weight:700;font-size:14px;padding:9px 16px;border-radius:999px}}
.btn.ghost{{background:transparent;color:var(--ink);border:1px solid var(--line)}}
.btn:hover{{opacity:.9}}
.soon{{font-size:13px;font-weight:700;color:var(--muted);background:#efe9dc;padding:8px 14px;border-radius:999px}}
footer{{font-size:13px;color:var(--muted);text-align:center}}
</style>
</head>
<body>
<main class="wrap">
  <nav aria-label="Secciones"><a href="../">Calculadora de nota y días</a><a href="../arriesgar/">¿Arriesgar o dejar en blanco?</a><a href="../baremo/">Concurso-oposición</a><a href="./" aria-current="page">Catálogo</a></nav>
  <header><h1>Plantillas, juegos y sonidos</h1><p class="lead">Herramientas en español para organizarte sin suscripciones, juegos gratis para jugar en el navegador y recursos originales para quien hace videojuegos.</p></header>
  {secs}
  <footer>Productos originales creados con ayuda de IA y revisados a mano. Pagos seguros a través de Payhip e itch.io.</footer>
</main>
</body>
</html>
'''
open(os.path.join(OUT, 'index.html'), 'w').write(page)
print('catalogo ok:', len(P), 'productos')
