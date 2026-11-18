// Genera sites/<web>/og.png (1200x630). Uso: node herramientas/sites_og.js
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.resolve(__dirname,'..');const b64=f=>'data:image/jpeg;base64,'+fs.readFileSync(path.join(R,f)).toString('base64');
const F='<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&family=Inter+Tight:wght@900&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">';
const pages={
cellmate:`${F}<body style="margin:0;width:1200px;height:630px;background:#f6f3ec;font-family:Inter;color:#1f2a44;display:flex;overflow:hidden">
<div style="padding:70px 0 0 70px;width:640px"><div style="display:flex;align-items:center;gap:14px;font:900 34px 'Inter Tight'"><span style="width:48px;height:48px;border-radius:12px;background:#1f2a44;color:#f6f3ec;display:grid;place-items:center;font-size:24px">C</span>Cellmate</div>
<div style="font:900 74px/1 'Inter Tight';letter-spacing:-.035em;margin:56px 0 22px">Plantillas que hacen las cuentas por ti.</div>
<div style="font-size:26px;color:#5d6577">Excel y Google Sheets · Pago único</div></div>
<div style="flex:1;position:relative"><img src="${b64('sites/cellmate/img/boda.jpg')}" style="position:absolute;width:360px;top:60px;left:90px;border-radius:18px;box-shadow:0 20px 50px #0003;transform:rotate(5deg)"><img src="${b64('sites/cellmate/img/planificador.jpg')}" style="position:absolute;width:360px;top:150px;left:0;border-radius:18px;box-shadow:0 20px 50px #0003;transform:rotate(-4deg)"></div></body>`,
oposiciones:`${F}<body style="margin:0;width:1200px;height:630px;background:#1f2a44;font-family:Inter;color:#fff;padding:70px;box-sizing:border-box">
<div style="display:flex;align-items:center;gap:14px;font:900 34px 'Inter Tight'"><span style="background:#f3c969;color:#1f2a44;border-radius:12px;padding:2px 14px">%</span>OpoCalc</div>
<div style="font:900 80px/1 'Inter Tight';letter-spacing:-.035em;margin:60px 0 26px;max-width:960px">Calcula tu nota real con penalización.</div>
<div style="font-size:28px;color:#c9d2e6">Nota de un test · ¿arriesgar o dejar en blanco? · concurso-oposición — gratis</div></body>`,
estudio:`${F}<body style="margin:0;width:1200px;height:630px;background:radial-gradient(circle at 80% 10%,#2b5a1e55,transparent 50%),#120c20;font-family:Inter;color:#f4f0ff;display:flex;overflow:hidden">
<div style="padding:70px 0 0 70px;width:620px"><div style="display:flex;align-items:center;gap:14px;font:900 36px 'Inter Tight'">${fs.readFileSync(path.join(R,'sites/estudio/favicon.svg'),'utf8').replace('<svg','<svg width="52" height="52"')}Nimbloom</div>
<div style="font:500 18px 'JetBrains Mono';letter-spacing:.14em;color:#b6f36a;margin-top:60px">INDIE STUDIO · GAMES &amp; AUDIO</div>
<div style="font:900 78px/1 'Inter Tight';letter-spacing:-.04em;margin:18px 0">Small games.<br><span style="color:#b6f36a">Big</span> “one more go”.</div></div>
<div style="flex:1;position:relative"><img src="${b64('sites/estudio/img/rootwork.jpg')}" style="position:absolute;width:420px;top:40px;left:60px;border-radius:18px;transform:rotate(4deg)"><img src="${b64('sites/estudio/img/lumen.jpg')}" style="position:absolute;width:420px;top:270px;left:-10px;border-radius:18px;transform:rotate(-3deg)"></div></body>`};
(async()=>{const b=await chromium.launch();for(const [k,h] of Object.entries(pages)){const p=await b.newPage({viewport:{width:1200,height:630}});await p.setContent(h,{waitUntil:'networkidle'});await p.screenshot({path:path.join(R,'sites',k,'og.png')});await p.close();}await b.close();console.log('og ok')})();
