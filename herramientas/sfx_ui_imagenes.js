// Imágenes de Soft UI Sounds Vol. 2: node herramientas/sfx_ui_imagenes.js <picos.json> productos/ui-sounds-vol2/imagenes
const {chromium}=require('playwright');const fs=require('fs');
const P=JSON.parse(fs.readFileSync(process.argv[2]));const OUT=process.argv[3];
const tiles=['confirm_02','notify_01','toggle_on_01','click_pop_01','reward_star_01','error_01','open_02','type_01','unlock_01'];
const css=`*{box-sizing:border-box;margin:0}body{font-family:Inter,sans-serif;background:radial-gradient(circle at 20% 10%,#ffe3f1,transparent 50%),radial-gradient(circle at 90% 90%,#e2dbff,transparent 55%),#f5f2ff;color:#1d1836;width:100vw;height:100vh;overflow:hidden;display:flex;flex-direction:column;justify-content:center;padding:6%}
h1{font-weight:900;letter-spacing:-.04em;line-height:.95}.g{white-space:nowrap;background:linear-gradient(90deg,#7c5cff,#ff6fb1 60%,#ffb35c);-webkit-background-clip:text;color:transparent}
.k{font:700 13px "JetBrains Mono",monospace;letter-spacing:.2em;color:#7c5cff}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:6%}.t{background:#fff;border:1px solid #e3dcff;border-radius:14px;padding:10px 12px;box-shadow:0 3px 10px rgba(60,40,140,.08)}
.t span{font:12px "JetBrains Mono",monospace;color:#5e5679}canvas{width:100%;height:30px;display:block;margin-top:4px}
.pill{display:inline-block;align-self:flex-start;margin-top:4%;padding:8px 16px;border-radius:999px;background:linear-gradient(90deg,#7c5cff,#ff6fb1);color:#fff;font-weight:800}`;
const page=(w,h,big,showGrid)=>`<html><head><style>${css}</style></head><body><div class="k">ROYALTY-FREE · WAV · GAMES & APPS</div><h1 style="font-size:${big}px;margin-top:2%">Soft UI Sounds <span class="g">Vol. 2</span></h1>
<div class="pill">46 gentle interface sounds</div>${showGrid?`<div class="grid">${tiles.map(n=>`<div class="t"><span>${n}.wav</span><canvas data-n="${n}" width="300" height="60"></canvas></div>`).join('')}</div>`:''}
<script>const P=${JSON.stringify(P)};document.querySelectorAll('canvas').forEach(c=>{const x=c.getContext('2d'),g=x.createLinearGradient(0,0,300,0);g.addColorStop(0,'#7c5cff');g.addColorStop(1,'#ff6fb1');x.fillStyle=g;const pk=P[c.dataset.n],bw=300/pk.length;pk.forEach((v,i)=>{const bh=Math.max(3,v*56);x.beginPath();x.roundRect(i*bw+1.5,(60-bh)/2,bw-3,bh,3);x.fill()})})</script></body></html>`;
(async()=>{const b=await chromium.launch();
for(const [w,h,big,grid,f,dsf] of [[630,500,54,true,'cover.png'],[960,300,64,false,'banner.png'],[600,600,50,true,'cuadrada.png',2]]){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:dsf||1});await p.setContent(page(w,h,big,grid));await p.waitForTimeout(300);await p.screenshot({path:OUT+'/'+f});}
await b.close();})();
