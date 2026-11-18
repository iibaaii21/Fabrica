// Imágenes de venta 1200x1200 de Control de alquileres. Uso: node imagenes.js
const {chromium}=require('playwright');const path=require('path');
const OUT=path.join(__dirname,'imagenes');
const css=`*{box-sizing:border-box;margin:0}body{width:1200px;height:1200px;background:#f1f4f8;font-family:Inter,sans-serif;color:#1f3a5f;padding:90px 70px;display:flex;flex-direction:column;justify-content:center}
.ey{font:800 22px Inter;letter-spacing:.18em;color:#c2603d;text-transform:uppercase}h1{font:900 104px/0.95 'Inter Tight',Inter;letter-spacing:-.05em;margin:22px 0 22px}
.sub{font-size:29px;color:#5d6577;margin-bottom:46px}.win{background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 30px 60px rgba(31,58,95,.16)}
.bar{background:#1f3a5f;height:40px;display:flex;gap:9px;align-items:center;padding:0 20px}.bar i{width:12px;height:12px;border-radius:50%;background:#7d8fa8}
.tabs{display:flex;background:#e3e9f1;padding:0 20px}.tabs span{font:600 18px Inter;color:#5d6577;padding:12px 20px}.tabs span.on{background:#fff;color:#1f3a5f;border-radius:10px 10px 0 0}
table{width:100%;border-collapse:collapse;font-size:22px}th{background:#1f3a5f;color:#fff;font:700 19px Inter;padding:14px 12px;text-align:right}th:first-child,td:first-child{text-align:left}
td{padding:14px 12px;border-bottom:1px solid #e9edf2;text-align:right;font-variant-numeric:tabular-nums}tr.t td{font-weight:800}
.p{background:#f8cbad}.a{background:#ffe699}.ok{color:#2e7d4f;font-weight:700}.pills{display:flex;gap:12px;margin-top:40px}.pills span{background:#1f3a5f;color:#fff;font:700 24px Inter;padding:13px 24px;border-radius:999px}`;
const fonts='<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Inter+Tight:wght@800;900&display=swap" rel="stylesheet">';
const win=(tab,t)=>`<div class="win"><div class="bar"><i></i><i></i><i></i></div><div class="tabs">${['Instrucciones','Resumen','Mes a mes','Inmuebles','Cobros','Gastos'].map(x=>`<span class="${x===tab?'on':''}">${x}</span>`).join('')}</div>${t}</div>`;
const pages={
portada:`<div class="ey">Excel · Google Sheets · LibreOffice</div><h1>Control de<br>alquileres</h1><div class="sub">Cobros, morosos, gastos y rentabilidad real de tus pisos.</div>`+
win('Resumen',`<table><tr><th>Inmueble</th><th>Cobrado</th><th>Pendiente</th><th>Gastos</th><th>Beneficio</th><th>Rent. neta</th></tr>
<tr><td>Piso Centro</td><td>2.250 €</td><td class="p">750 €</td><td>600 €</td><td>1.650 €</td><td>1,10 %</td></tr>
<tr><td>Estudio Playa</td><td>1.300 €</td><td class="p">260 €</td><td>256 €</td><td>1.045 €</td><td>1,07 %</td></tr>
<tr class="t"><td>Total</td><td>3.550 €</td><td>1.010 €</td><td>856 €</td><td>2.695 €</td><td>1,09 %</td></tr></table>`)+`<div class="pills"><span>Hasta 10 inmuebles</span><span>Sin macros</span><span>Pago único</span></div>`,
cobros:`<div class="ey">Quién te debe, de un vistazo</div><h1 style="font-size:84px;line-height:1.04">Cada recibo,<br>con su estado.</h1><div class="sub">Apunta lo que tocaba cobrar y lo cobrado: los impagos se marcan solos.</div>`+
win('Cobros',`<table><tr><th>Inmueble</th><th>Mes</th><th>Tocaba</th><th>Cobrado</th><th>Pendiente</th><th>Estado</th></tr>
<tr><td>Piso Centro</td><td>3</td><td>750 €</td><td>750 €</td><td>0 €</td><td class="ok">Cobrado</td></tr>
<tr class="a"><td>Estudio Playa</td><td>3</td><td>520 €</td><td>260 €</td><td>260 €</td><td>Parcial</td></tr>
<tr class="p"><td>Piso Centro</td><td>4</td><td>750 €</td><td></td><td>750 €</td><td>Pendiente</td></tr>
<tr><td>Estudio Playa</td><td>4</td><td>520 €</td><td>520 €</td><td>0 €</td><td class="ok">Cobrado</td></tr></table>`)+`<div class="pills"><span>Aviso de fin de contrato</span><span>Gasto por categoría</span></div>`,
};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1200}});
for(const [n,h] of Object.entries(pages)){await p.setContent(`<!doctype html><html><head>${fonts}<style>${css}</style></head><body>${h}</body></html>`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);await p.screenshot({path:path.join(OUT,n+'.png')});}
await b.close();console.log('ok')})();
