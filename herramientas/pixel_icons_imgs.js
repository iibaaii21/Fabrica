// Imágenes de venta de Pixel Icons Vol. 1. Uso: node herramientas/pixel_icons_imgs.js <png-64px> <salida>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [src, out] = process.argv.slice(2);
const files = fs.readdirSync(src).filter(f => f.endsWith('.png')).sort();
const order = JSON.parse(fs.readFileSync(path.join(src, '..', 'spritesheet-16px.json'))).frames;
const names = Object.keys(order);
const uri = n => 'data:image/png;base64,' + fs.readFileSync(path.join(src, n + '.png')).toString('base64');
const I = (n, s) => `<img src="${uri(n)}" style="width:${s}px;height:${s}px;image-rendering:pixelated;display:block">`;
const BG = '#1b1830', CARD = '#262244', INK = '#f4efe6', MUT = '#a59fc7', ACC = '#fcc934';
const base = (w, h, body) => `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0}body{width:${w}px;height:${h}px;overflow:hidden;background:${BG};color:${INK};font-family:Inter}
.d{font-family:'Inter Display';font-weight:800;letter-spacing:-.02em}.m{font-family:'JetBrains Mono'}
.bgdots{position:absolute;inset:0;background-image:radial-gradient(#ffffff10 1px,transparent 1px);background-size:16px 16px}
</style></head><body><div class="bgdots"></div><div style="position:relative;width:100%;height:100%">${body}</div></body></html>`;

const pages = {};
// Portada 630x500
const coverIcons = ['sword', 'shield', 'potion_red', 'gem_blue', 'heart', 'coin', 'key', 'chest', 'crown', 'potion_green', 'bomb', 'star', 'skull', 'orb_purple', 'fire', 'mushroom', 'axe', 'trophy', 'map', 'gem_gold', 'apple'];
pages.cover = [630, 500, base(630, 500, `
<div style="padding:34px 38px 0">
 <div class="m" style="color:${ACC};font-size:15px;letter-spacing:.12em">16×16 PIXEL ART · RPG + UI</div>
 <div class="d" style="font-size:62px;line-height:1;margin-top:10px">Pixel Icons<span style="color:${ACC}"> Vol.1</span></div>
 <div style="font-size:19px;color:${MUT};margin-top:10px">73 original icons · PNG 16/32/64 px · spritesheet + JSON</div>
</div>
<div style="position:absolute;left:38px;right:38px;bottom:34px;display:grid;grid-template-columns:repeat(7,1fr);gap:10px">
${coverIcons.map(n => `<div style="background:${CARD};border-radius:12px;height:72px;display:grid;place-items:center;box-shadow:inset 0 -3px 0 #00000040">${I(n, 48)}</div>`).join('')}
</div>`)];

// Captura 1: todos los iconos
pages['captura-1'] = [1280, 650, base(1280, 650, `
<div style="padding:30px 40px 0;display:flex;justify-content:space-between;align-items:baseline">
 <div class="d" style="font-size:34px">All 73 icons</div><div class="m" style="color:${MUT};font-size:15px">shown at 3× · 61 designs + 12 color variants</div></div>
<div style="padding:18px 40px;display:grid;grid-template-columns:repeat(13,1fr);gap:10px">
${names.map(n => `<div style="background:${CARD};border-radius:10px;padding:8px 0 6px;display:flex;flex-direction:column;align-items:center;gap:4px">${I(n, 48)}<div class="m" style="font-size:9.5px;color:${MUT};white-space:nowrap;overflow:hidden;max-width:84px;text-overflow:ellipsis">${n}</div></div>`).join('')}
</div>`)];

// Captura 2: maqueta de uso en un juego
const inv = ['sword', 'axe', 'bow', 'arrow', 'staff', 'dagger', 'potion_red', 'potion_blue', 'potion_green', 'apple', 'meat', 'bread', 'key', 'map', 'scroll', 'bomb', 'gem_purple', 'ring', null, null, null, null, null, null];
pages['captura-2'] = [1280, 800, base(1280, 800, `
<div style="position:absolute;inset:0;background:linear-gradient(180deg,#2b4a3a 0%,#1f3a2f 60%,#18291f 100%)"></div>
<div style="position:absolute;inset:0;background-image:radial-gradient(#ffffff0c 2px,transparent 2px);background-size:32px 32px"></div>
<div style="position:absolute;left:28px;top:24px;display:flex;gap:4px">${['heart', 'heart', 'heart', 'heart_half', 'heart_empty'].map(n => I(n, 48)).join('')}</div>
<div style="position:absolute;left:30px;top:84px;display:flex;align-items:center;gap:10px">${I('coin', 40)}<span class="m" style="font-size:28px;font-weight:700;text-shadow:0 3px 0 #0006">1,250</span>
 <span style="width:20px"></span>${I('gem_blue', 40)}<span class="m" style="font-size:28px;font-weight:700;text-shadow:0 3px 0 #0006">36</span></div>
<div style="position:absolute;right:28px;top:24px;display:flex;gap:10px">${['sound_on', 'gear', 'pause'].map(n => `<div style="background:#00000055;border-radius:12px;padding:8px">${I(n, 40)}</div>`).join('')}</div>
<div style="position:absolute;left:50%;top:150px;transform:translateX(-50%);width:640px;background:#1b1830ee;border:4px solid #0d0a12;border-radius:18px;padding:22px 26px;box-shadow:0 12px 0 #0005">
 <div style="display:flex;justify-content:space-between;align-items:center"><div class="d" style="font-size:30px">Inventory</div><div style="display:flex;gap:8px;align-items:center">${I('bag', 32)}<span class="m" style="color:${MUT}">18 / 24</span></div></div>
 <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-top:16px">
 ${inv.map((n, i) => `<div style="aspect-ratio:1;background:${i === 6 ? '#3a335f' : CARD};border-radius:10px;display:grid;place-items:center;outline:${i === 6 ? '3px solid ' + ACC : 'none'};box-shadow:inset 0 -4px 0 #00000045">${n ? I(n, 64) : ''}</div>`).join('')}
 </div>
 <div style="display:flex;gap:14px;align-items:center;margin-top:18px;background:${CARD};border-radius:12px;padding:12px 14px">${I('potion_red', 48)}<div><div style="font-weight:700;font-size:18px">Health Potion</div><div style="color:${MUT};font-size:14px">Restores 2 hearts</div></div>
 <div style="margin-left:auto;display:flex;gap:8px">${['check', 'cross'].map(n => `<div style="background:#00000040;border-radius:10px;padding:6px">${I(n, 32)}</div>`).join('')}</div></div>
</div>
<div style="position:absolute;left:0;right:0;bottom:22px;text-align:center" class="m"><span style="background:#0008;padding:6px 14px;border-radius:8px;color:${INK};font-size:14px">Mock-up made only with icons from the pack</span></div>`)];

// Captura 3: tamaños y formatos
pages['captura-3'] = [1280, 680, base(1280, 680, `
<div style="padding:44px 56px">
 <div class="d" style="font-size:40px">Crisp at every size</div>
 <div style="color:${MUT};font-size:19px;margin-top:8px">Pre-scaled PNGs with nearest-neighbor — no blurry edges.</div>
 <div style="display:flex;gap:28px;align-items:flex-end;margin-top:36px">
 ${[16, 32, 64, 128, 256].map(s => `<div style="display:flex;flex-direction:column;align-items:center;gap:12px">${I('chest', s)}<div class="m" style="color:${ACC};font-size:15px">${s}px</div></div>`).join('')}
 </div>
 <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:44px">
 ${[['png-16px · png-32px · png-64px', '73 individual PNGs in each size, transparent background'],
    ['spritesheet + JSON atlas', 'One sheet (16 per row) at 16 px and 64 px with x / y / w / h per icon'],
    ['Engine-ready', 'Notes for Godot, Unity, GameMaker and HTML5 canvas in README.txt']].map(([a, b]) =>
    `<div style="background:${CARD};border-radius:14px;padding:18px 20px"><div class="m" style="color:${ACC};font-size:15px">${a}</div><div style="font-size:16px;margin-top:8px;color:${INK}">${b}</div></div>`).join('')}
 </div>
</div>`)];

(async () => {
  const b = await chromium.launch();
  fs.mkdirSync(out, { recursive: true });
  for (const [n, [w, h, html]] of Object.entries(pages)) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.setContent(html); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(out, n + '.png') }); await p.close();
  }
  await b.close();
})();
