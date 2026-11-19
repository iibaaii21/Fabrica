// Genera canal/marca/avatar-800x800.png y banner-2560x1440.png. Uso: node canal/herramientas/marca.js
const {chromium}=require('playwright');const path=require('path');
const OUT=path.join(__dirname,'..','marca');
const F='<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;800&family=Inter+Tight:wght@900&display=swap" rel="stylesheet">';
const BG='radial-gradient(circle at 20% 15%,#5b3fd1 0%,transparent 45%),radial-gradient(circle at 85% 90%,#0f7bb8 0%,transparent 50%),linear-gradient(150deg,#1a1240,#22195a 55%,#0d3a66)';
const sphere=(x,y,r,a,b)=>`<div style="position:absolute;left:${x}px;top:${y}px;width:${r*2}px;height:${r*2}px;border-radius:50%;background:radial-gradient(circle at 32% 28%,${a},${b} 70%);box-shadow:0 ${r/3}px ${r}px #0007"></div>`;
const torus=(x,y,r,c,rot)=>`<div style="position:absolute;left:${x}px;top:${y}px;width:${r*2}px;height:${r*2}px;border-radius:50%;border:${r*0.42}px solid ${c};transform:rotate(${rot}deg) scaleY(.55);box-shadow:0 ${r/3}px ${r}px #0006, inset 0 ${r/6}px ${r/4}px #ffffff55"></div>`;
const avatar=`${F}<body style="margin:0;width:800px;height:800px;overflow:hidden;background:${BG};position:relative;font-family:Inter">
${sphere(560,90,70,'#ffe08a','#e0a21c')}${torus(70,560,80,'#ff6b8b',-20)}${sphere(600,600,40,'#7ee0ff','#2f7fd6')}
<div style="position:absolute;inset:0;display:grid;place-items:center">
<div style="text-align:center;transform:translateY(-10px)"><div style="font:900 330px/0.85 'Inter Tight';letter-spacing:-.06em;color:#fff;text-shadow:0 20px 60px #0008">M<span style="color:#ffc93d">E</span></div>
<div style="font:800 46px Inter;letter-spacing:.32em;color:#e6e0ff;margin-top:26px;padding-left:.32em">EXAMEN</div></div></div></body>`;
// banner: 2560x1440; zona segura centrada 1546x423 (x 507..2053, y 508..931)
const banner=`${F}<body style="margin:0;width:2560px;height:1440px;overflow:hidden;background:${BG};position:relative;font-family:Inter">
${sphere(260,380,150,'#ffe08a','#e0a21c')}${torus(2150,330,170,'#ff6b8b',25)}${sphere(2220,880,90,'#7ee0ff','#2f7fd6')}${torus(330,860,110,'#8ff0a8',-30)}${sphere(1900,1080,60,'#c79bff','#6a3fc4')}${sphere(560,1050,46,'#ff9fb5','#d24c78')}
<div style="position:absolute;left:507px;top:508px;width:1546px;height:423px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">
<div style="font:900 170px/0.95 'Inter Tight';letter-spacing:-.045em;color:#fff;text-shadow:0 20px 60px #0008">MODO <span style="color:#ffc93d">EXAMEN</span></div>
<div style="font:600 50px Inter;color:#e6e0ff;margin-top:22px">Entiéndelo fácil. Recuérdalo siempre.</div>
<div style="display:flex;gap:18px;margin-top:30px">${['ESO','Bachillerato','Universidad','Técnicas de estudio'].map(t=>`<span style="font:800 32px Inter;color:#fff;background:#ffffff22;border:2px solid #ffffff40;padding:10px 26px;border-radius:999px">${t}</span>`).join('')}</div>
</div></body>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:800,height:800}});
await p.setContent(avatar,{waitUntil:'networkidle'});await p.screenshot({path:path.join(OUT,'avatar-800x800.png')});
await p.setViewportSize({width:2560,height:1440});await p.setContent(banner,{waitUntil:'networkidle'});await p.screenshot({path:path.join(OUT,'banner-2560x1440.png')});
// comprobación de zona segura: recorte 1546x423 centrado
await p.screenshot({path:path.join(OUT,'..','herramientas','.check-zona-segura.png'),clip:{x:507,y:508,width:1546,height:423}});
await b.close();console.log('ok')})();
