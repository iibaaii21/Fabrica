// Miniatura 1280x720 con el stickman v2: node stickthumb.js <spec.json> <salida.png>
// spec: {"v": {...visual de una frase...}, "t": 1.2, "title": "TEXTO <em>COLOR</em>", "pill": "texto opcional", "bg": ["#ffe9b3","#ffc979"]}
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const [, , specF, out] = process.argv; const sp = JSON.parse(fs.readFileSync(specF));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file://' + __dirname + '/stick.html'); await p.waitForFunction(() => window.ready === true);
  await p.evaluate(c => window.setup(c), { w: 1280, h: 720, dur: 1e9, beats: [{ ini: 0, fin: 10, texto: '', v: sp.v }], captions: false });
  await p.evaluate(t => window.renderAt(t), sp.t || 1.5);
  const img = await p.evaluate(() => document.getElementById('c').toDataURL('image/png'));
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0;padding:0;box-sizing:border-box}
  body{width:1280px;height:720px;overflow:hidden;position:relative;font-family:"Inter Display",Inter,sans-serif}
  .s{position:absolute;inset:0;background:url(${img}) center/cover}
  .fade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.0) 0%,rgba(0,0,0,0) 100%)}
  .t{position:absolute;left:44px;top:34px;width:${sp.tw || 820}px;color:#151515;font-weight:900;font-size:${sp.fs || 100}px;line-height:.98;letter-spacing:-.035em;
     paint-order:stroke fill;-webkit-text-stroke:14px #fff;text-shadow:0 8px 0 rgba(0,0,0,.18)}
  .t em{font-style:normal;color:#e8483f}
  .pill{position:absolute;left:44px;bottom:44px;background:#e8483f;color:#fff;font-weight:900;font-size:52px;padding:12px 30px;border-radius:16px;transform:rotate(-2.5deg);border:6px solid #151515;box-shadow:8px 8px 0 #151515}
  </style></head><body><div class="s"></div><div class="t">${sp.title}</div>${sp.pill ? `<div class="pill">${sp.pill}</div>` : ''}</body></html>`;
  await p.setContent(html); await p.waitForTimeout(300); await p.screenshot({ path: out }); await b.close();
})();
