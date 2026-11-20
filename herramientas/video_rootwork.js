// Vídeos de gameplay de Rootwork para CrazyGames (1920x1080 y 1080x1620, ~20 s), jugando con clics reales.
// Uso: node herramientas/video_rootwork.js   (necesita playwright y ffmpeg)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const D = path.join(__dirname, '..', 'juegos', 'rootwork'), GAME = 'file://' + D + '/index.html', OUT = D + '/videos', TMP = path.join(OUT, '_tmp');
const ALL = { seen: { w0: 1, w1: 1, w2: 1, w3: 1, w4: 1, w5: 1 }, sound: false, music: false, stars: Object.fromEntries(Array.from({ length: 140 }, (_, i) => [i + 1, [3,3,2,3,3,1,3,2,3,3][i % 10]])) };
async function solveByClicks(p, gap) {
  for (let k = 0; k < 200; k++) {
    const xy = await p.evaluate(() => { const st = __root.state(), L = st.L; if (st.won) return null;
      const rot = (m, k) => { for (let j = 0; j < k; j++) m = ((m << 1) | (m >> 3)) & 15; return m; };
      const bad = L.live.filter(i => rot(L.start[i], st.turns[i]) !== L.sol[i]); if (!bad.length) return null;
      bad.sort((a, b) => (st.wet[b] ? 1 : 0) - (st.wet[a] ? 1 : 0)); const i = bad[0];
      const W = innerWidth, H = innerHeight, top = 72, bot = 64, av = Math.min(W - 28, H - top - bot), ts = Math.floor(av / L.sz), bx = Math.round((W - ts * L.sz) / 2), by = Math.round(top + (H - top - bot - ts * L.sz) / 2);
      return [bx + (i % L.sz) * ts + ts / 2, by + Math.floor(i / L.sz) * ts + ts / 2]; });
    if (!xy) break; await p.mouse.move(xy[0], xy[1], { steps: 4 }); await p.mouse.down(); await p.mouse.up(); await p.waitForTimeout(gap);
  }
}
async function rec(w, h, name, lvA, lvB) {
  fs.mkdirSync(TMP, { recursive: true });
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: w, height: h }, recordVideo: { dir: TMP, size: { width: w, height: h } } });
  const p = await ctx.newPage(); const t0 = Date.now();
  await p.goto(GAME); await p.waitForTimeout(400); await p.evaluate(a => __root.setProgress(a), ALL); const tStart = (Date.now() - t0) / 1000;
  await p.waitForTimeout(1600);
  await p.evaluate(n => __root.go(n), lvA); await p.evaluate(() => __root.peek(0.55)); await p.waitForTimeout(700);
  await solveByClicks(p, 230); await p.waitForTimeout(3000);
  await p.evaluate(n => __root.go(n), lvB); await p.evaluate(() => __root.peek(0.6)); await p.waitForTimeout(600);
  await solveByClicks(p, 200); await p.waitForTimeout(2600);
  await p.click('#wLevels'); await p.waitForTimeout(250); await p.click('#lBack'); await p.waitForTimeout(1800);
  const total = (Date.now() - t0) / 1000; await ctx.close(); await b.close();
  const webm = fs.readdirSync(TMP).filter(f => f.endsWith('.webm')).map(f => path.join(TMP, f))[0];
  const ss = Math.max(0, tStart + 0.2), dur = Math.min(30, total - ss - 0.3);
  execSync(`ffmpeg -v error -y -ss ${ss} -i "${webm}" -t ${dur} -vf "fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 20 -an -movflags +faststart "${path.join(OUT, name)}"`);
  fs.rmSync(TMP, { recursive: true, force: true }); console.log(name, dur.toFixed(1) + ' s');
}
(async () => { await rec(1920, 1080, 'landscape-1920x1080.mp4', 79, 112); await rec(1080, 1620, 'portrait-1080x1620.mp4', 54, 129); })();
