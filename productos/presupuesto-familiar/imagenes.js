// Imágenes de venta 1200x1200 de Presupuesto familiar. Uso: node imagenes.js
const {chromium}=require('playwright');const path=require('path');
const OUT=path.join(__dirname,'imagenes');
const css=`*{box-sizing:border-box;margin:0}body{width:1200px;height:1200px;background:#eef4f1;font-family:Inter,sans-serif;color:#2e5e4e;padding:90px 70px;display:flex;flex-direction:column;justify-content:center}
.ey{font:800 22px Inter;letter-spacing:.18em;color:#c2603d;text-transform:uppercase}h1{font:900 100px/0.95 'Inter Tight',Inter;letter-spacing:-.05em;margin:22px 0 22px}
.sub{font-size:29px;color:#5d6b66;margin-bottom:44px}.win{background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 30px 60px rgba(46,94,78,.16)}
.bar{background:#2e5e4e;height:40px;display:flex;gap:9px;align-items:center;padding:0 20px}.bar i{width:12px;height:12px;border-radius:50%;background:#8fb1a4}
.tabs{display:flex;background:#dfe9e4;padding:0 20px}.tabs span{font:600 18px Inter;color:#5d6b66;padding:12px 16px}.tabs span.on{background:#fff;color:#2e5e4e;border-radius:10px 10px 0 0}
table{width:100%;border-collapse:collapse;font-size:22px}th{background:#2e5e4e;color:#fff;font:700 19px Inter;padding:14px 12px;text-align:right}th:first-child,td:first-child{text-align:left}
td{padding:13px 12px;border-bottom:1px solid #e6eeea;text-align:right;font-variant-numeric:tabular-nums}tr.t td{font-weight:800}
.p{background:#f8cbad}.ok{color:#2e7d4f;font-weight:700}.pills{display:flex;gap:12px;margin-top:40px;flex-wrap:wrap}.pills span{background:#2e5e4e;color:#fff;font:700 24px Inter;padding:13px 24px;border-radius:999px}
.bars{display:grid;gap:18px;padding:28px 30px}.row{display:grid;grid-template-columns:210px 1fr 120px;gap:16px;align-items:center;font-size:23px}.trk{height:30px;background:#e6eeea;border-radius:8px;position:relative;overflow:hidden}.fil{position:absolute;inset:0 auto 0 0;border-radius:8px}.g{position:absolute;top:-6px;bottom:-6px;width:4px;background:#1d2b26}`;
const fonts='<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Inter+Tight:wght@800;900&display=swap" rel="stylesheet">';
const win=(tab,t)=>`<div class="win"><div class="bar"><i></i><i></i><i></i></div><div class="tabs">${['Instrucciones','Resumen','Ajustes','Movimientos','Presupuesto','Mes a mes','Metas'].map(x=>`<span class="${x===tab?'on':''}">${x}</span>`).join('')}</div>${t}</div>`;
const bar=(l,v,g,c)=>`<div class="row"><b>${l}</b><div class="trk"><div class="fil" style="width:${v*100}%;background:${c}"></div><div class="g" style="left:${g*100}%"></div></div><span>${Math.round(v*100)} %</span></div>`;
const pages={
portada:`<div class="ey">Excel · Google Sheets · LibreOffice</div><h1>Presupuesto<br>familiar</h1><div class="sub">Sabe cada mes cuánto entra, en qué se va y cuánto ahorras.</div>`+
win('Presupuesto',`<table><tr><th>Categoría</th><th>Presupuesto</th><th>Real</th><th>Diferencia</th></tr>
<tr><td>Vivienda</td><td>650 €</td><td>650 €</td><td>0 €</td></tr>
<tr><td>Supermercado</td><td>280 €</td><td>310 €</td><td class="p">−30 €</td></tr>
<tr><td>Ocio y salidas</td><td>60 €</td><td>95 €</td><td class="p">−35 €</td></tr>
<tr><td>Transporte</td><td>60 €</td><td>20 €</td><td class="ok">40 €</td></tr>
<tr class="t"><td>Te queda este mes</td><td></td><td>585 €</td><td></td></tr></table>`)+`<div class="pills"><span>Sin macros</span><span>Metas de ahorro</span><span>Pago único</span></div>`,
reparto:`<div class="ey">¿Vas bien?</div><h1 style="font-size:84px;line-height:1.04">Necesidades, deseos<br>y ahorro, claros.</h1><div class="sub">Tu reparto real frente a la regla 50/30/20, y tu tasa de ahorro.</div>`+
win('Resumen',`<div class="bars">${bar('Necesidades',.50,.5,'#5b9b7e')}${bar('Deseos',.05,.3,'#e2a54b')}${bar('Ahorro',.45,.2,'#2e5e4e')}
<div class="row" style="font-size:20px;color:#5d6b66"><span></span><span>La raya negra marca la guía 50/30/20</span><span></span></div></div>
<table><tr><th>Mes</th><th>Ingresos</th><th>Gastos</th><th>Tasa de ahorro</th></tr><tr><td>Enero</td><td>1.800 €</td><td>879,80 €</td><td class="ok">51,1 %</td></tr><tr><td>Febrero</td><td>1.800 €</td><td>1.115 €</td><td class="ok">38,1 %</td></tr></table>`)+`<div class="pills"><span>Gráfico mes a mes</span><span>Top 5 de gastos</span></div>`,
};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1200}});
for(const [n,h] of Object.entries(pages)){await p.setContent(`<!doctype html><html><head>${fonts}<style>${css}</style></head><body>${h}</body></html>`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);await p.screenshot({path:path.join(OUT,n+'.png')});}
await b.close();console.log('ok')})();
