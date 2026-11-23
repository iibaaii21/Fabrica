"""Genera las tres webs independientes en sites/ a partir de herramientas/catalogo.json.

  sites/cellmate/      tienda de plantillas (marca Cellmate)
  sites/oposiciones/   calculadoras gratis para opositores (OpoCalc)
  sites/estudio/       estudio de juegos y recursos (Nimbloom)

Uso: python3 herramientas/sites.py   (después: node herramientas/sites_og.js para las imágenes OG)
Si un nombre de Cloudflare Pages está cogido, cambia solo BASE y vuelve a ejecutar.
"""
import json, os, re, shutil, html
from PIL import Image

BASE = {
    'cellmate': 'https://cellmate-plantillas.pages.dev',
    'oposiciones': 'https://calculadora-oposiciones.pages.dev',
    'estudio': 'https://nimbloom.pages.dev',
}
ITCH = 'https://iibaaii21.itch.io'
PAYHIP = 'https://payhip.com/Cellmate'
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(R, 'sites')
P = {p['id']: p for p in json.load(open(os.path.join(R, 'herramientas/catalogo.json')))}
e = html.escape
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Inter+Tight:wght@700;800;900&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">'


def w(site, path, text):
    p = os.path.join(S, site, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)


def img(site, src, name, size=1200):
    out = os.path.join(S, site, 'img', name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = Image.open(os.path.join(R, src)).convert('RGB')
    im.thumbnail((size, size))
    im.save(out, quality=84, optimize=True, progressive=True)
    return im.size


def head(site, title, desc, path, css, extra=''):
    url = BASE[site] + path
    brand = {'cellmate': 'Cellmate', 'oposiciones': 'OpoCalc', 'estudio': 'Nimbloom'}[site]
    return f'''<!doctype html>
<html lang="{'en' if site == 'estudio' else 'es'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="{brand}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE[site]}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{ {'cellmate': '#1f2a44', 'oposiciones': '#1d4ed8', 'estudio': '#140d24'}[site] }">
{FONTS}
<style>{css}</style>{extra}
</head>
<body>'''


def seo_files(site, paths):
    w(site, 'robots.txt', f'User-agent: *\nAllow: /\nSitemap: {BASE[site]}/sitemap.xml\n')
    urls = ''.join(f'  <url><loc>{BASE[site]}{p}</loc></url>\n' for p in paths)
    w(site, 'sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


# ------------------------------------------------------------------ CELLMATE
CM_CSS = '''
:root{--bg:#f6f3ec;--card:#fff;--ink:#1f2a44;--muted:#5d6577;--line:#e4ded2;--gold:#b0893f;--soft:#ece6d9}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}
a{color:inherit}
.w{max-width:1120px;margin:0 auto;padding:0 20px}
header.top{position:sticky;top:0;z-index:5;background:rgba(246,243,236,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header.top .w{display:flex;align-items:center;justify-content:space-between;height:64px;gap:16px}
.logo{display:flex;align-items:center;gap:10px;font:800 21px 'Inter Tight',Inter,sans-serif;text-decoration:none;letter-spacing:-.02em}
.logo i{width:28px;height:28px;border-radius:8px;background:var(--ink);display:grid;place-items:center;color:#f6f3ec;font:800 13px 'Inter Tight';font-style:normal}
nav.m{display:flex;gap:22px;font-weight:600;font-size:15px}nav.m a{text-decoration:none;color:var(--muted)}nav.m a:hover{color:var(--ink)}
.hero{padding:72px 0 40px}
.eyebrow{font:700 13px Inter;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
h1{font:900 clamp(38px,6.4vw,72px)/1 'Inter Tight',Inter,sans-serif;letter-spacing:-.035em;margin:14px 0 18px;text-wrap:balance}
.lead{font-size:clamp(17px,2.2vw,20px);color:var(--muted);max-width:620px;margin:0}
.badges{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}.badges span{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:22px;padding:24px 0 70px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-3px);box-shadow:0 16px 40px rgba(31,42,68,.1)}
.card img{width:100%;height:auto;display:block;aspect-ratio:1;object-fit:cover;background:var(--soft)}
.card .b{padding:18px 20px 22px;display:grid;gap:8px}
.card h3{margin:0;font:800 19px/1.25 'Inter Tight',Inter;letter-spacing:-.01em}
.card p{margin:0;color:var(--muted);font-size:15px}
.price{font-weight:800;color:var(--gold)}
.tag{display:inline-block;font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;background:var(--soft);color:var(--muted)}
h2{font:800 30px/1.15 'Inter Tight',Inter;letter-spacing:-.02em;margin:0}
.why{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;padding:10px 0 80px}
.why div{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px}
.why b{display:block;font-size:17px;margin-bottom:6px}.why p{margin:0;color:var(--muted);font-size:15px}
.prod{display:grid;grid-template-columns:1.1fr 1fr;gap:44px;padding:44px 0 70px;align-items:start}
.gal{display:grid;gap:14px}.gal img{width:100%;height:auto;border-radius:16px;border:1px solid var(--line);display:block}
.prod h1{font-size:clamp(32px,4.6vw,50px)}
.buy{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin:24px 0}
.btn{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:700;padding:14px 26px;border-radius:999px;font-size:16px}
.btn:hover{background:#2c3a5c}.btn.alt{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.soon{display:inline-block;background:var(--soft);color:var(--muted);font-weight:700;padding:13px 22px;border-radius:999px}
.big{font:900 34px 'Inter Tight';color:var(--ink)}
ul.pts{list-style:none;padding:0;margin:20px 0;display:grid;gap:10px}ul.pts li{padding-left:30px;position:relative}
ul.pts li:before{content:"";position:absolute;left:0;top:4px;width:18px;height:18px;border-radius:50%;background:var(--ink) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath d='M5 10.5l3 3 7-7' stroke='white' stroke-width='2.4' fill='none' stroke-linecap='round'/%3E%3C/svg%3E") center/14px no-repeat}
.note{font-size:14px;color:var(--muted)}
.legal{max-width:760px;padding-top:50px;padding-bottom:80px}.legal h1{font-size:40px}.legal h2{font-size:22px;margin-top:28px}
footer.f{border-top:1px solid var(--line);padding:30px 0 40px;font-size:14px;color:var(--muted)}
footer.f .w{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}footer.f a{color:var(--muted)}
img.mfirst{display:none}
@media(max-width:820px){.prod{grid-template-columns:1fr;gap:26px}.prod .gal{order:2}.prod .gal img:first-child{display:none}img.mfirst{display:block;width:100%;height:auto;border-radius:16px;border:1px solid var(--line);margin-bottom:18px}nav.m{gap:14px;font-size:14px}.hero{padding:44px 0 24px}}
@media(max-width:420px){nav.m a.hide{display:none}}
'''


def cm_top():
    return f'''<header class="top"><div class="w"><a class="logo" href="/"><i>C</i>Cellmate</a>
<nav class="m"><a href="/#plantillas">Plantillas</a><a href="/calculadora-autonomos/">IVA e IRPF</a><a class="hide" href="{BASE['oposiciones']}/">Opositores</a><a href="/legal/">Legal</a></nav></div></header>'''


def cm_foot():
    return f'''<footer class="f"><div class="w"><span>© 2026 Cellmate · Plantillas de Excel y Google Sheets en español</span>
<span><a href="/legal/">Aviso legal</a> · <a href="/privacidad/">Privacidad</a> · <a href="{BASE['oposiciones']}/">Calculadoras gratis para opositores</a></span></div></footer>
</body></html>'''


def build_cellmate():
    site = 'cellmate'
    ids = [k for k, p in P.items() if p.get('marca') == 'cellmate']
    cards = ''
    for k in ids:
        p = P[k]
        img(site, p['img'], f'{k}.jpg', 800)
        cards += f'''<a class="card" href="/plantillas/{k}/"><img src="/img/{k}.jpg" width="800" height="800" alt="{e(p['nombre'])}" loading="lazy">
<div class="b"><span class="tag">{'Gratis' if p['precio'] == 'Gratis' else 'Excel · Google Sheets'}</span><h3>{e(p['nombre'])}</h3><p>{e(p.get('lema', p['desc']))}</p><span class="price">{e(p['precio'])}</span></div></a>'''
    w(site, 'index.html', head(site, 'Cellmate · Plantillas de Excel y Google Sheets en español', 'Plantillas de Excel y Google Sheets listas para usar: planificador de oposiciones, organizador de boda, libro de autónomos y control de alquileres. Pago único, sin suscripciones.', '/', CM_CSS) + cm_top() + f'''
<main><section class="hero"><div class="w"><div class="eyebrow">Excel · Google Sheets · LibreOffice</div>
<h1>Plantillas que hacen las cuentas por ti.</h1>
<p class="lead">Organiza tu oposición, tu boda, tus cuentas de autónomo o tus pisos de alquiler en un solo archivo. Sin apps, sin suscripciones y sin macros: lo abres y funciona.</p>
<div class="badges"><span>Pago único</span><span>Descarga inmediata</span><span>Fórmulas verificadas</span><span>En español</span></div></div></section>
<section class="w" id="plantillas"><h2>Plantillas</h2><div class="grid">{cards}</div></section>
<section class="w" style="padding-bottom:40px"><div class="cta" style="background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px;display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap"><div><span class="tag">Gratis</span><h2 style="margin:8px 0 4px;font-size:24px">Calculadora trimestral de IVA e IRPF para autónomos</h2><p style="margin:0;color:var(--muted)">Modelo 303 y modelo 130 en un minuto, sin registrarte.</p></div><a class="btn" href="/calculadora-autonomos/">Calcular ahora</a></div></section>
<section class="w"><h2 style="margin-bottom:18px">Por qué Cellmate</h2><div class="why">
<div><b>Funciona en todas partes</b><p>Excel, Google Sheets (Archivo &gt; Importar) y LibreOffice. También en el móvil.</p></div>
<div><b>Sin macros ni trucos</b><p>Solo fórmulas. Nada se ejecuta a escondidas y tus datos no salen de tu ordenador.</p></div>
<div><b>Verificadas a mano</b><p>Cada fórmula se comprueba con datos de prueba antes de publicar la plantilla.</p></div>
<div><b>Instrucciones dentro</b><p>Cada archivo explica en su primera hoja qué rellenar y qué se calcula solo.</p></div></div></section></main>''' + cm_foot())
    paths = ['/', '/calculadora-autonomos/', '/legal/', '/privacidad/']
    w(site, 'calculadora-autonomos/index.html', head(site, 'Calculadora de IVA e IRPF trimestral para autónomos (modelos 303 y 130) · Cellmate', 'Calcula gratis cuánto pagas cada trimestre como autónomo: IVA del modelo 303 y pago fraccionado del IRPF del modelo 130, con gastos de difícil justificación y retenciones.', '/calculadora-autonomos/', CM_CSS) + cm_top() + open(os.path.join(R, 'herramientas/calc_autonomos.html')).read() + cm_foot())
    for k in ids:
        p = P[k]
        gal = ''
        for i, src in enumerate(p.get('imgs', [p['img']])):
            wd, ht = img(site, src, f'{k}-{i}.jpg', 1200)
            gal += f'<img src="/img/{k}-{i}.jpg" width="{wd}" height="{ht}" alt="{e(p["nombre"])}: imagen {i + 1}"{" loading=lazy" if i else ""}>'
        if p.get('comprar'):
            buy = f'<a class="btn" href="{e(p["comprar"])}" rel="noopener">Comprar · {e(p["precio"])}</a>'
        else:
            buy = '<span class="soon">Disponible muy pronto</span>'
        extra = ''
        if k in ('planificador', 'planificador-lite'):
            extra = f'<p class="note">¿Quieres calcular una nota ahora mismo? Usa las <a href="{BASE["oposiciones"]}/">calculadoras gratuitas para opositores</a>.</p>'
        if k == 'autonomos':
            extra = '<p class="note">Herramienta de control y estimación: no sustituye al asesoramiento fiscal ni a los programas de la Agencia Tributaria.</p><p class="note">¿Solo quieres saber cuánto pagas este trimestre? Prueba la <a href="/calculadora-autonomos/">calculadora gratuita de IVA e IRPF para autónomos</a>.</p>'
        if k == 'alquileres':
            extra = '<p class="note">Herramienta de organización: no calcula impuestos ni sustituye al asesoramiento fiscal.</p>'
        pts = ''.join(f'<li>{e(x)}</li>' for x in p.get('puntos', []))
        w(site, f'plantillas/{k}/index.html', head(site, f'{p["nombre"]} · Cellmate', p.get('lema', p['desc']), f'/plantillas/{k}/', CM_CSS) + cm_top() + f'''
<main class="w"><section class="prod"><div class="gal">{gal}</div>
<div><img class="mfirst" src="/img/{k}-0.jpg" alt="{e(p['nombre'])}"><div class="eyebrow">Plantilla · Excel y Google Sheets</div><h1>{e(p['nombre'])}</h1><p class="lead">{e(p.get('lema', p['desc']))}</p>
<div class="buy"><span class="big">{e(p['precio'])}</span>{buy}</div>
<ul class="pts">{pts}</ul><p class="note">Archivo .xlsx sin macros · Instrucciones dentro · Descarga inmediata tras el pago, gestionado por Payhip.</p>{extra}
<p style="margin-top:26px"><a href="/#plantillas">← Ver todas las plantillas</a></p></div></section></main>''' + cm_foot())
        paths.append(f'/plantillas/{k}/')
    w(site, 'legal/index.html', head(site, 'Aviso legal · Cellmate', 'Aviso legal y condiciones de venta de Cellmate.', '/legal/', CM_CSS) + cm_top() + f'''
<main class="w legal"><h1>Aviso legal y condiciones</h1>
<h2>Titular</h2><p>Este sitio pertenece a Cellmate, marca de plantillas digitales. Los datos identificativos del titular se facilitan a petición a través del formulario de contacto de la <a href="{PAYHIP}">tienda en Payhip</a>.</p>
<h2>Compras</h2><p>Las ventas se realizan a través de Payhip, que procesa el pago y entrega el archivo de forma inmediata. El precio mostrado es el precio final; los impuestos aplicables se calculan en el pago.</p>
<h2>Productos digitales y desistimiento</h2><p>Al tratarse de contenido digital que se descarga de inmediato, al completar la compra aceptas el inicio de la descarga y, con ello, la pérdida del derecho de desistimiento (art. 103.m del Real Decreto Legislativo 1/2007). Si el archivo no funciona como se describe, escríbenos y lo solucionaremos o te devolveremos el importe.</p>
<h2>Uso de las plantillas</h2><p>Puedes usar las plantillas para ti o para tu negocio. No está permitido revenderlas ni redistribuirlas. Las plantillas son herramientas de organización y estimación y no sustituyen al asesoramiento profesional.</p>
<h2>Inteligencia artificial</h2><p>Las plantillas se diseñan con ayuda de herramientas de IA y se revisan y prueban a mano antes de publicarse.</p></main>''' + cm_foot())
    w(site, 'privacidad/index.html', head(site, 'Privacidad · Cellmate', 'Política de privacidad de Cellmate.', '/privacidad/', CM_CSS) + cm_top() + f'''
<main class="w legal"><h1>Privacidad</h1>
<p>Esta web no usa cookies propias ni formularios, y no recoge datos personales.</p>
<h2>Estadísticas</h2><p>Para contar visitas usamos Cloudflare Web Analytics, que no usa cookies ni identifica a los visitantes.</p>
<h2>Compras</h2><p>Cuando compras, tus datos (email y pago) los trata Payhip según su propia política de privacidad. Solo recibimos lo necesario para entregarte el producto y atender tus consultas.</p>
<h2>Tus derechos</h2><p>Puedes pedir el acceso, la rectificación o la supresión de tus datos escribiéndonos desde la <a href="{PAYHIP}">tienda</a>. También puedes reclamar ante la Agencia Española de Protección de Datos.</p></main>''' + cm_foot())
    w(site, '404.html', head(site, 'Página no encontrada · Cellmate', 'Esta página no existe.', '/404', CM_CSS) + cm_top() + '<main class="w legal"><h1>Esta página no existe</h1><p><a class="btn" href="/">Ir a las plantillas</a></p></main>' + cm_foot())
    w(site, 'favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#1f2a44"/><text x="16" y="22.5" font-family="Arial Black,Arial,sans-serif" font-size="17" font-weight="900" fill="#f6f3ec" text-anchor="middle">C</text></svg>')
    seo_files(site, paths)


# ------------------------------------------------------------------ OPOSICIONES
OP_BAR = '''<style>.opbar{background:#1f2a44;color:#fff}.opbar .in{max-width:760px;margin:0 auto;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.opbar a{color:#fff;text-decoration:none}.opbar .lg{font:800 19px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;display:flex;align-items:center;gap:8px}
.opbar .lg i{font-style:normal;background:#f3c969;color:#1f2a44;border-radius:7px;padding:1px 7px;font-size:15px}.opbar .r{font-size:14px;opacity:.85}
body{font-family:Inter,-apple-system,"Segoe UI",Roboto,system-ui,sans-serif}nav[aria-label="Herramientas"] a{margin-right:4px}
.opfoot{max-width:760px;margin:0 auto;padding:0 16px 40px;font-size:13px;color:#5a6275;text-align:center}.opfoot a{color:#5a6275}</style>'''


def build_oposiciones():
    site = 'oposiciones'
    C = BASE['cellmate']
    pages = [('index.html', '/', 'herramientas/fuentes/opocalc/index.html'), ('arriesgar/index.html', '/arriesgar/', 'herramientas/fuentes/opocalc/arriesgar/index.html'), ('baremo/index.html', '/baremo/', 'herramientas/fuentes/opocalc/baremo/index.html'), ('ritmo/index.html', '/ritmo/', 'herramientas/fuentes/opocalc/ritmo/index.html')]
    for out, path, src in pages:
        s = open(os.path.join(R, src)).read()
        s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{BASE[site]}{path}">', s)
        title = re.search(r'<title>(.*?)</title>', s).group(1)
        desc = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
        og = (f'<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="OpoCalc">'
              f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{BASE[site]}{path}">'
              f'<meta property="og:image" content="{BASE[site]}/og.png"><meta name="twitter:card" content="summary_large_image">{FONTS}{OP_BAR}')
        s = s.replace('</head>', og + '\n</head>', 1)
        s = s.replace('<body>', f'<body>\n<div class="opbar"><div class="in"><a class="lg" href="/"><i>%</i>OpoCalc</a><span class="r">Calculadoras gratis para opositores · <a href="{C}/">Plantillas Cellmate</a></span></div></div>', 1)
        # catálogo y enlaces a la tienda -> fichas de Cellmate
        s = re.sub(r'<a href="(\.\./)?catalogo/"[^>]*>Catálogo</a>', f'<a href="{C}/" style="color:var(--muted)">Plantillas</a>', s)
        s = s.replace('href="https://payhip.com/Cellmate"', f'href="{C}/plantillas/planificador/"')
        s = s.replace('</main>', f'</main>\n<div class="opfoot">OpoCalc es gratuito y no guarda ningún dato: todo se calcula en tu navegador. Las cifras son orientativas; revisa siempre las bases de tu convocatoria. · <a href="{C}/privacidad/">Privacidad</a></div>', 1)
        assert 'Fabrica' not in s and 'github' not in s.lower(), src
        w(site, out, s)
    w(site, 'favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#1f2a44"/><text x="16" y="22" font-family="Arial Black,Arial,sans-serif" font-size="16" font-weight="900" fill="#f3c969" text-anchor="middle">%</text></svg>')
    w(site, '404.html', '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada · OpoCalc</title><link rel="icon" href="/favicon.svg"></head><body style="font-family:system-ui,sans-serif;background:#f7f5f0;color:#1f2a44;display:grid;place-items:center;min-height:100vh;margin:0;padding:16px;text-align:center"><div><h1>Esta página no existe</h1><p><a href="/" style="color:#1f2a44">Ir a la calculadora de nota</a></p></div></body></html>')
    seo_files(site, [p for _, p, _ in pages])


# ------------------------------------------------------------------ NIMBLOOM
NB_CSS = '''
:root{--bg:#120c20;--bg2:#1b1430;--card:#21193a;--ink:#f4f0ff;--muted:#b7aed6;--line:#33295a;--lime:#b6f36a;--pink:#ff7ab6}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}
a{color:inherit}.w{max-width:1140px;margin:0 auto;padding:0 20px}
header.top{position:sticky;top:0;z-index:5;background:rgba(18,12,32,.88);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header.top .w{display:flex;align-items:center;justify-content:space-between;height:64px;gap:14px}
.logo{display:flex;align-items:center;gap:10px;font:900 22px 'Inter Tight',Inter;letter-spacing:-.03em;text-decoration:none}
.logo svg{width:30px;height:30px}
nav.m{display:flex;gap:22px;font-weight:600;font-size:15px}nav.m a{text-decoration:none;color:var(--muted)}nav.m a:hover{color:var(--ink)}
.hero{padding:80px 0 50px;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;inset:-40% -10% auto auto;width:620px;height:620px;background:radial-gradient(circle,rgba(182,243,106,.18),transparent 60%);pointer-events:none}
.eyebrow{font:500 13px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--lime)}
h1{font:900 clamp(40px,7vw,80px)/.98 'Inter Tight',Inter;letter-spacing:-.04em;margin:16px 0 18px;text-wrap:balance}
h1 em{font-style:normal;color:var(--lime)}
.lead{font-size:clamp(17px,2.2vw,20px);color:var(--muted);max-width:640px;margin:0}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.btn{display:inline-block;background:var(--lime);color:#14200a;text-decoration:none;font-weight:800;padding:13px 24px;border-radius:12px}
.btn.alt{background:transparent;color:var(--ink);border:1.5px solid var(--line)}.btn:hover{filter:brightness(1.07)}
h2{font:800 32px/1.1 'Inter Tight',Inter;letter-spacing:-.02em;margin:0 0 6px}
.sub{color:var(--muted);margin:0 0 22px}
section.s{padding:30px 0 50px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:#4a3d80}
.card img{width:100%;height:auto;display:block;aspect-ratio:1260/1000;object-fit:cover}
.card .b{padding:18px 20px 22px;display:grid;gap:8px}.card h3{margin:0;font:800 21px 'Inter Tight'}.card p{margin:0;color:var(--muted);font-size:15px}
.chips{display:flex;gap:6px;flex-wrap:wrap}.chips span{font:500 12px 'JetBrains Mono';color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:2px 8px}
.game{display:grid;gap:26px;padding-top:40px;padding-bottom:70px}
.frame{position:relative;width:100%;aspect-ratio:16/9;border-radius:18px;overflow:hidden;border:1px solid var(--line);background:#000}
.frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.shots img{width:100%;height:auto;border-radius:12px;border:1px solid var(--line)}
.two{display:grid;grid-template-columns:1.3fr 1fr;gap:30px}
audio{width:100%;margin-top:6px}
.legal{max-width:760px;padding-top:50px;padding-bottom:80px}
footer.f{border-top:1px solid var(--line);padding:30px 0 40px;font-size:14px;color:var(--muted)}
footer.f .w{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}footer.f a{color:var(--muted)}
@media(max-width:820px){.two{grid-template-columns:1fr}.hero{padding:50px 0 30px}nav.m{gap:14px;font-size:14px}.frame{aspect-ratio:3/4}}
'''
NB_LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="15" fill="#21193a" stroke="#33295a"/><path d="M16 25c0-6 0-9-5-12 4 0 5 2 5 4 0-5 2-8 7-9-3 3-5 7-5 17z" fill="#b6f36a"/><circle cx="11" cy="12" r="2.6" fill="#ff7ab6"/></svg>'
GAMES = [('lumen', 'Lumen Drift', ['arcade', 'one button', 'endless']), ('loomlines', 'Loomlines', ['puzzle', 'logic', '200 levels']), ('rootwork', 'Rootwork', ['puzzle', '6 worlds', 'daily garden']), ('lunavault', 'Lunavault', ['one tap', 'space', 'endless'])]
EN = {
    'lumen': 'Hold to rise, release to fall. Guide a spark of light through an endless neon cave that keeps getting faster.',
    'loomlines': 'Connect every pair of spools without crossing threads and fill the whole board. Calm, colourful logic.',
    'rootwork': 'Turn the root tiles so water reaches every flower. 150 gardens in 6 worlds, stones, pools, twin springs and a new garden every day.',
    'lunavault': 'Tap to leap from moon to moon. Fly through the centre for perfect combos and see how high you can climb.',
    'sfx': '42 original retro sound effects for your game: UI, pickups, movement, combat and states. WAV, royalty-free.',
    'music': '6 seamless game music loops and 2 stingers, WAV + OGG. Menu, action, puzzle, dungeon, racer and town themes.',
    'ui-sounds': '46 soft, modern interface sounds for menus, apps and cozy games: clicks, toggles, notifications and rewards. WAV, royalty-free.',
    'pixel-icons': '73 original 16×16 pixel-art icons: weapons, potions, gems, food, tools and UI buttons. PNG 16/32/64 px + spritesheet with JSON atlas.',
}


def nb_top():
    return f'<header class="top"><div class="w"><a class="logo" href="/">{NB_LOGO}Nimbloom</a><nav class="m"><a href="/#games">Games</a><a href="/#assets">Assets</a><a href="{ITCH}" rel="noopener">itch.io</a></nav></div></header>'


def nb_foot():
    return f'<footer class="f"><div class="w"><span>© 2026 Nimbloom · Small games and game-ready assets</span><span><a href="/legal/">Legal &amp; privacy</a> · <a href="{ITCH}" rel="noopener">itch.io</a></span></div></footer></body></html>'


def build_estudio():
    site = 'estudio'
    cards = ''
    paths = ['/', '/legal/', '/sounds/', '/music/', '/icons/', '/ui-sounds/']
    for g, name, chips in GAMES:
        img(site, P[g]['img'], f'{g}.jpg', 900)
        cards += f'<a class="card" href="/games/{g}/"><img src="/img/{g}.jpg" width="900" height="714" alt="{name}" loading="lazy"><div class="b"><div class="chips">{"".join(f"<span>{c}</span>" for c in chips)}</div><h3>{name}</h3><p>{EN[g]}</p></div></a>'
        dst = os.path.join(S, site, 'play', g)
        os.makedirs(dst, exist_ok=True)
        shutil.copy(os.path.join(R, 'juegos', g, 'index.html'), os.path.join(dst, 'index.html'))
        shots = ''
        for i, src in enumerate(P[g]['imgs']):
            wd, ht = img(site, src, f'{g}-{i}.jpg', 900)
            shots += f'<img src="/img/{g}-{i}.jpg" width="{wd}" height="{ht}" alt="{name} screenshot {i + 1}" loading="lazy">'
        w(site, f'games/{g}/index.html', head(site, f'{name} · Play free in your browser · Nimbloom', EN[g], f'/games/{g}/', NB_CSS) + nb_top() + f'''
<main class="w game"><div><div class="eyebrow">Free browser game</div><h1 style="font-size:clamp(36px,6vw,64px)">{name}</h1><p class="lead">{EN[g]}</p></div>
<div class="frame"><iframe src="/play/{g}/" title="{name}" allow="fullscreen; autoplay" loading="lazy"></iframe></div>
<div class="cta" style="margin-top:0"><a class="btn" href="/play/{g}/">Play full screen</a><a class="btn alt" href="/#games">More games</a></div>
<div class="shots">{shots}</div></main>''' + nb_foot())
        paths += [f'/games/{g}/', f'/play/{g}/']
    acards = ''
    for k, href, label in [('sfx', '/sounds/', 'Listen to all 42'), ('ui-sounds', '/ui-sounds/', 'Listen to all 46'), ('music', '/music/', 'Listen to the preview'), ('pixel-icons', '/icons/', 'See all 73 + free sample')]:
        img(site, P[k]['img'], f'{k}.jpg', 900)
        acards += f'<a class="card" href="{href}"><img src="/img/{k}.jpg" width="900" height="714" alt="{e(P[k]["nombre"])}" loading="lazy"><div class="b"><div class="chips"><span>{e(P[k]["precio"])}</span><span>royalty-free</span></div><h3>{e(P[k]["nombre"])}</h3><p>{EN[k]}</p><p style="color:var(--lime);font-weight:700">{label} →</p></div></a>'
    w(site, 'index.html', head(site, 'Nimbloom · Small games and game-ready audio', 'Nimbloom makes small, polished browser games you can play for free, plus original sound effects, music loops and pixel-art icons for game developers.', '/', NB_CSS) + nb_top() + f'''
<main><section class="hero"><div class="w"><div class="eyebrow">Indie studio · games &amp; audio</div>
<h1>Small games.<br><em>Big</em> “one more go”.</h1>
<p class="lead">We make polished little games you can play right now in your browser, plus original sound effects, music and pixel art that other developers use in theirs.</p>
<div class="cta"><a class="btn" href="#games">Play our games</a><a class="btn alt" href="#assets">Assets for developers</a></div></div></section>
<section class="s w" id="games"><h2>Games</h2><p class="sub">Free to play on desktop and mobile. No downloads, no sign-up.</p><div class="grid">{cards}</div></section>
<section class="s w" id="assets"><h2>Assets for developers</h2><p class="sub">Original, made from scratch, royalty-free for commercial games.</p><div class="grid">{acards}</div></section></main>''' + nb_foot())
    # sonidos: demo existente reubicada
    src = os.path.join(R, 'herramientas/fuentes/sfx-demo')
    dst = os.path.join(S, site, 'sounds')
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    s = open(os.path.join(dst, 'index.html')).read()
    s = s.replace('</head>', f'<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="canonical" href="{BASE[site]}/sounds/"><meta property="og:image" content="{BASE[site]}/og.png">\n</head>', 1)
    s = s.replace('<body>', '<body><p style="margin:14px 16px 0;font:600 14px Inter,system-ui,sans-serif"><a href="/" style="color:inherit">← Nimbloom</a></p>', 1) if '<body>' in s else s
    open(os.path.join(dst, 'index.html'), 'w').write(s)
    # Soft UI Sounds Vol. 2: página de escucha generada con sfx_ui.py
    import sfx_ui
    uk = P['ui-sounds']; dst = os.path.join(S, site, 'ui-sounds')
    shutil.rmtree(dst, ignore_errors=True); shutil.copytree(os.path.join(R, 'productos/ui-sounds-vol2/wav'), os.path.join(dst, 'wav'))
    top = f'<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="canonical" href="{BASE[site]}/ui-sounds/"><meta property="og:image" content="{BASE[site]}/og.png">'
    if uk.get('comprar'): html = sfx_ui.preview(uk['comprar'], top=top)
    else: html = sfx_ui.preview('/#assets', 'Coming soon to itch.io · see our other packs →', 'More assets from Nimbloom →', top=top)
    html = html.replace('<body>', '<body><p style="margin:14px 16px 0;font:600 14px Inter,system-ui,sans-serif"><a href="/" style="color:inherit">← Nimbloom</a></p>', 1)
    open(os.path.join(dst, 'index.html'), 'w').write(html)
    os.makedirs(os.path.join(S, site, 'media'), exist_ok=True)
    shutil.copy(os.path.join(R, 'productos/music-loops-vol1/preview.mp3'), os.path.join(S, site, 'media/music-loops-preview.mp3'))
    shots = ''
    for i, srcp in enumerate(P['music']['imgs']):
        wd, ht = img(site, srcp, f'music-{i}.jpg', 1000)
        shots += f'<img src="/img/music-{i}.jpg" width="{wd}" height="{ht}" alt="Synth Music Loops Vol. 1 image {i + 1}" loading="lazy">'
    buy = f'<a class="btn" href="{e(P["music"]["comprar"])}" rel="noopener">Buy on itch.io · {e(P["music"]["precio"])}</a>' if P['music'].get('comprar') else '<span class="btn alt">Coming soon to itch.io</span>'
    w(site, 'music/index.html', head(site, 'Synth Music Loops Vol. 1 · Nimbloom', EN['music'], '/music/', NB_CSS) + nb_top() + f'''
<main class="w game"><div class="two"><div><div class="eyebrow">Game music · WAV + OGG</div><h1 style="font-size:clamp(34px,5.4vw,58px)">Synth Music Loops Vol.&nbsp;1</h1><p class="lead">{EN['music']}</p>
<p style="margin-top:20px"><b>Preview</b> (10 seconds of each track):</p><audio controls preload="none" src="/media/music-loops-preview.mp3"></audio>
<div class="cta">{buy}<a class="btn alt" href="/sounds/">Sound effects pack</a></div>
<p class="sub" style="margin-top:18px">Seamless loops (no click at the loop point) · consistent loudness · works in Godot, Unity, GameMaker and HTML5 · royalty-free, no attribution required.</p></div>
<div class="shots" style="grid-template-columns:1fr">{shots}</div></div></main>''' + nb_foot())
    # iconos pixel art: página con todos los iconos y muestra gratis descargable
    pk = P['pixel-icons']
    shutil.copy(os.path.join(R, 'productos/pixel-icons-vol1/Pixel-Icons-Vol1-Free-Sample.zip'), os.path.join(S, site, 'media/Pixel-Icons-Vol1-Free-Sample.zip'))
    shots = ''
    for i, srcp in enumerate(pk['imgs'][1:]):
        wd, ht = img(site, srcp, f'icons-{i}.jpg', 1280)
        shots += f'<img src="/img/icons-{i}.jpg" width="{wd}" height="{ht}" alt="Pixel Icons Vol. 1 image {i + 1}" loading="lazy">'
    buy = f'<a class="btn" href="{e(pk["comprar"])}" rel="noopener">Buy on itch.io · {e(pk["precio"])}</a>' if pk.get('comprar') else '<span class="btn alt">Full pack coming soon to itch.io</span>'
    w(site, 'icons/index.html', head(site, 'Pixel Icons Vol. 1 · 73 RPG & UI icons 16×16 · Nimbloom', EN['pixel-icons'], '/icons/', NB_CSS) + nb_top() + f'''
<main class="w game"><div><div class="eyebrow">Pixel art · 16×16 · PNG + spritesheet</div><h1 style="font-size:clamp(34px,5.4vw,58px)">Pixel Icons Vol.&nbsp;1</h1><p class="lead">{EN['pixel-icons']}</p>
<div class="cta"><a class="btn" href="/media/Pixel-Icons-Vol1-Free-Sample.zip" download>Download 12 icons free</a>{buy}</div>
<p class="sub" style="margin-top:18px">One consistent palette and a 1 px outline, so every icon reads on light or dark backgrounds · pre-scaled to 32 and 64 px with no blur · import notes for Godot, Unity, GameMaker and HTML5 · royalty-free, no attribution required. The free sample uses the same licence.</p></div>
<div class="shots" style="grid-template-columns:1fr">{shots}</div>
<div class="cta" style="margin-top:0"><a class="btn alt" href="/sounds/">Sound effects pack</a><a class="btn alt" href="/music/">Music loops</a></div></main>''' + nb_foot())
    w(site, 'legal/index.html', head(site, 'Legal & privacy · Nimbloom', 'Legal notice and privacy policy for Nimbloom.', '/legal/', NB_CSS) + nb_top() + f'''
<main class="w legal"><h1 style="font-size:40px">Legal &amp; privacy</h1>
<p>Nimbloom is an independent game and audio label. Games on this site are free to play. Paid assets are sold and delivered through <a href="{ITCH}">itch.io</a>, which processes payments and taxes.</p>
<h2>Privacy</h2><p>This site has no accounts, forms or advertising cookies. Games store your progress and best scores only in your own browser (local storage). Visits are counted with Cloudflare Web Analytics, which does not use cookies or identify visitors.</p>
<h2>Assets licence</h2><p>Sound effects, music and pixel art are licensed for use in your own commercial and non-commercial projects without attribution. Reselling or redistributing the files as they are is not allowed. The full licence is included in each download.</p>
<h2>AI</h2><p>Our games, audio and graphics are made with the help of AI tools, then designed, tested and polished by hand.</p></main>''' + nb_foot())
    w(site, '404.html', head(site, 'Not found · Nimbloom', 'This page does not exist.', '/404', NB_CSS) + nb_top() + '<main class="w legal"><h1 style="font-size:40px">Nothing grows here</h1><p><a class="btn" href="/">Back to Nimbloom</a></p></main>' + nb_foot())
    w(site, 'favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" ' + NB_LOGO[5:])
    seo_files(site, paths)


if __name__ == '__main__':
    for d in ('cellmate', 'oposiciones', 'estudio'):
        shutil.rmtree(os.path.join(S, d), ignore_errors=True)
    build_cellmate(); build_oposiciones(); build_estudio()
    for root, _, files in os.walk(S):
        for f in files:
            if f.endswith(('.html', '.xml', '.txt', '.svg')):
                t = open(os.path.join(root, f)).read()
                assert not re.search(r'fabrica|github|claude', t, re.I), os.path.join(root, f)
    print('webs generadas en sites/')
