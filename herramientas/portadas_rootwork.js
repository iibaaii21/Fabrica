// Portada 630x500, portadas CrazyGames y 3 capturas de Rootwork. Uso: node herramientas/portadas_rootwork.js
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const D = path.join(__dirname, '..', 'juegos', 'rootwork'), GAME = 'file://' + D + '/index.html', IMG = D + '/imagenes';
(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async (w, h) => { const p = await b.newPage({ viewport: { width: w, height: h } }); p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); return p; };
  const play = async (p, lv, f) => { await p.goto(GAME); await p.evaluate(() => { try { localStorage.setItem('rootwork.unlocked', '300'); localStorage.setItem('rootwork.sound', 'false'); } catch (e) {} }); await p.reload();
    await p.evaluate(n => __root.go(n), lv); await p.waitForTimeout(100); await p.evaluate(f => __root.peek(f), f); await p.waitForTimeout(700); };
  // board-only shot for covers
  { const p = await page(1000, 1000); await play(p, 47, 0.78); await p.addStyleTag({ content: '#hud,#help{display:none!important}' }); await p.evaluate(() => dispatchEvent(new Event('resize'))); await p.waitForTimeout(500);
    await p.screenshot({ path: IMG + '/_board.png' }); await p.close(); }
  // screenshots 1280x720
  { const p = await page(1280, 720); await play(p, 23, 0.88); await p.screenshot({ path: IMG + '/captura-1.png' });
    await play(p, 64, 0); await p.evaluate(() => __root.solve()); await p.waitForTimeout(1300); await p.screenshot({ path: IMG + '/captura-2.png' });
    await p.click('#hMenu'); await p.evaluate(() => { try { localStorage.setItem('rootwork.stars', JSON.stringify(Object.fromEntries(Array.from({length: 17}, (_, i) => [i + 1, [3,3,2,3,3,1,3,2,3,3,3,2,3,3,2,3,1][i]])))); localStorage.setItem('rootwork.unlocked', '18'); } catch (e) {} });
    await p.reload(); await p.click('#bLevels'); await p.waitForTimeout(400); await p.screenshot({ path: IMG + '/captura-3.png' }); await p.close(); }
  // covers from an HTML composition
  const cover = (w, h) => `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&family=Inter+Tight:wght@800;900&display=swap" rel="stylesheet">
<style>*{margin:0;box-sizing:border-box}body{width:${w}px;height:${h}px;overflow:hidden;background:radial-gradient(120% 100% at 30% 20%,#2a6b45,#0b1f16 70%);font-family:Inter,sans-serif;color:#fff;position:relative}
.board{position:absolute;background:url(_board.png) center/cover;border-radius:${Math.round(Math.min(w,h)*0.04)}px;box-shadow:0 30px 80px #000a;transform:rotate(-6deg)}
.t{position:absolute;font-family:'Inter Tight',Inter,sans-serif;font-weight:900;letter-spacing:-.04em;line-height:.9;text-shadow:0 6px 0 #0a1c13,0 14px 40px #000a}.t b{color:#ffd166}
.s{position:absolute;font-weight:700;color:#d9ecd6;text-shadow:0 2px 10px #000c}</style></head><body>
${w > h * 1.1 ? `<div class="board" style="width:${h*0.98}px;height:${h*0.98}px;right:${-h*0.08}px;top:${h*0.04}px"></div>
<div class="t" style="left:${w*0.06}px;top:${h*0.30}px;font-size:${h*0.2}px">Root<b>work</b></div><div class="s" style="left:${w*0.065}px;top:${h*0.56}px;font-size:${h*0.055}px;max-width:${w*0.45}px">Turn the roots.<br>Water every flower.</div>`
: `<div class="board" style="width:${w*0.9}px;height:${w*0.9}px;left:${w*0.05}px;top:${h - w*0.95}px"></div>
<div class="t" style="left:0;right:0;text-align:center;top:${h*0.07}px;font-size:${w*0.2}px">Root<b>work</b></div><div class="s" style="left:0;right:0;text-align:center;top:${h*0.07 + w*0.22}px;font-size:${w*0.055}px">Turn the roots. Water every flower.</div>`}</body></html>`;
  for (const [file, w, h] of [['cover.png', 630, 500], ['crazygames-1920x1080.png', 1920, 1080], ['crazygames-800x1200.png', 800, 1200], ['crazygames-800x800.png', 800, 800]]) {
    fs.writeFileSync(IMG + '/_c.html', cover(w, h)); const p = await page(w, h); await p.goto('file://' + IMG + '/_c.html'); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(IMG, file) }); await p.close(); }
  fs.unlinkSync(IMG + '/_c.html'); fs.unlinkSync(IMG + '/_board.png');
  console.log('errores:', errs); await b.close();
})();
