// node beats.js <carpeta> w h i1,i2,...  -> b-XX.jpg  (prueba rápida de escenas concretas)
const { chromium } = require('playwright');const fs=require('fs'),path=require('path');
const [,,dir,w,h,list]=process.argv;
(async()=>{const g=JSON.parse(fs.readFileSync(path.join(dir,'guion.json')));const T=JSON.parse(fs.readFileSync(path.join(dir,'tiempos.json')));
const beats=T.segs.map((s,i)=>({ini:s.ini,fin:s.fin,texto:s.texto,v:g.frases[i].v||{}}));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.goto('file://'+__dirname+'/stick.html');await p.waitForFunction(()=>window.ready===true);await p.evaluate(c=>window.setup(c),{w:+w,h:+h,dur:T.dur,beats,captions:true});
for(const i of list.split(',').map(Number)){await p.evaluate(t=>window.renderAt(t),(beats[i].ini+beats[i].fin)/2);const u=await p.evaluate(()=>document.getElementById('c').toDataURL('image/jpeg',0.8));fs.writeFileSync(path.join(dir,`b-${String(i).padStart(2,'0')}.jpg`),Buffer.from(u.split(',')[1],'base64'));}
await b.close();})();
