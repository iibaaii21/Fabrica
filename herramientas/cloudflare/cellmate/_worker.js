const ORIGIN = 'https://raw.githubusercontent.com/iibaaii21/Fabrica/claude/fabrica-ingresos-legales-9iymbg/sites/cellmate';
const TYPES = { html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', js: 'text/javascript; charset=utf-8', json: 'application/json', svg: 'image/svg+xml', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', webp: 'image/webp', ico: 'image/x-icon', mp3: 'audio/mpeg', wav: 'audio/wav', ogg: 'audio/ogg', mp4: 'video/mp4', txt: 'text/plain; charset=utf-8', xml: 'application/xml', woff2: 'font/woff2', zip: 'application/zip' };
export default {
  async fetch(request) {
    const url = new URL(request.url);
    let path = decodeURIComponent(url.pathname);
    if (path.includes('..')) return new Response('Bad request', { status: 400 });
    if (path.endsWith('/')) path += 'index.html';
    let ext = (path.split('/').pop().split('.')[1] || '').toLowerCase();
    if (!ext) { path += '/index.html'; ext = 'html'; }
    let res = await fetch(ORIGIN + path, { cf: { cacheTtl: 300, cacheEverything: true } });
    if (res.status === 404) { const nf = await fetch(ORIGIN + '/404.html', { cf: { cacheTtl: 300, cacheEverything: true } }); return new Response(nf.ok ? nf.body : 'Not found', { status: 404, headers: { 'content-type': TYPES.html } }); }
    if (!res.ok) return new Response('Error', { status: 502 });
    const h = new Headers({ 'content-type': TYPES[ext] || 'application/octet-stream', 'cache-control': ext === 'html' ? 'public, max-age=300' : 'public, max-age=86400', 'x-content-type-options': 'nosniff' });
    return new Response(res.body, { status: 200, headers: h });
  }
};
