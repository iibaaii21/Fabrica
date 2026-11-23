#!/usr/bin/env python3
"""Genera las 3 versiones de Rootwork a partir de juegos/rootwork/index.html (fuente única):
  - Rootwork-crazygames.zip : con el script del SDK v3 de CrazyGames (el juego funciona igual si no carga).
  - Rootwork-web.zip        : sin recursos externos (GameDistribution, itch.io, otros portales).
  - itch/index.html + Rootwork-itch.zip : versión web con enlace discreto «More games».
(docs/ redirige a las webs nuevas desde el 23/11: Nimbloom sirve el juego desde juegos/rootwork/index.html.)"""
import os, zipfile, shutil
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')); D = os.path.join(R, 'juegos', 'rootwork')
src = open(os.path.join(D, 'index.html'), encoding='utf-8').read()
assert '<!--PORTAL-SDK-->' in src
web = src.replace('<!--PORTAL-SDK-->\n', '')
cg = src.replace('<!--PORTAL-SDK-->', '<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>')
itch = web.replace('<p class="sub" data-t="tagline"></p>', '<p class="sub" data-t="tagline"></p>', 1).replace(
    '<button class="ghost ib" id="bSettings" aria-label="Settings">&#9881;</button></div>',
    '<button class="ghost ib" id="bSettings" aria-label="Settings">&#9881;</button></div>\n    <a href="https://iibaaii21.itch.io" target="_blank" rel="noopener" style="color:inherit;opacity:.6;font-size:14px;text-decoration:none">More games ↗</a>', 1)
assert itch != web
os.makedirs(os.path.join(D, 'itch'), exist_ok=True)
open(os.path.join(D, 'itch', 'index.html'), 'w', encoding='utf-8').write(itch)
def z(name, html):
    p = os.path.join(D, name)
    with zipfile.ZipFile(p, 'w', zipfile.ZIP_DEFLATED) as f: f.writestr('index.html', html.encode('utf-8'))
    print(name, os.path.getsize(p), 'bytes')
z('Rootwork-crazygames.zip', cg); z('Rootwork-web.zip', web); z('Rootwork-itch.zip', itch)

