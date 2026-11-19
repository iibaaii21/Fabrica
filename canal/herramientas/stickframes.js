// uso: node stickframes.js <carpeta> <test|full> <w> <h> [captions]
const { chromium } = require('playwright');const fs=require('fs'),path=require('path');const {spawn}=require('child_process');
const [,,dir,mode,w,h,caps]=process.argv;
(async()=>{const g=JSON.parse(fs.readFileSync(path.join(dir,'guion.json')));const T=JSON.parse(fs.readFileSync(path.join(dir,'tiempos.json')));
const beats=T.segs.map((s,i)=>({ini:s.ini,fin:s.fin,texto:s.texto,v:g.frases[i].v||{}}));
const cfg={w:+w,h:+h,dur:T.dur,beats,captions:caps==='captions'};
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+__dirname+'/stick.html');await p.waitForFunction(()=>window.ready===true);await p.evaluate(c=>window.setup(c),cfg);
const shot=async()=>{const u=await p.evaluate(()=>document.getElementById('c').toDataURL('image/jpeg',0.9));return Buffer.from(u.split(',')[1],'base64')};
if(mode==='test'){const n=Math.min(beats.length,12);for(let i=0;i<n;i++){const t=(beats[i].ini+beats[i].fin)/2;await p.evaluate(t=>window.renderAt(t),t);fs.writeFileSync(path.join(dir,`test-${String(i).padStart(2,'0')}.jpg`),await shot());}console.log('errors',errs);await b.close();return;}
const fps=30,N=Math.ceil(T.dur*fps);const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','21','-maxrate','8M','-bufsize','16M','-pix_fmt','yuv420p',path.join(dir,'video-mudo.mp4')]);
const t0=Date.now();for(let i=0;i<N;i++){await p.evaluate(t=>window.renderAt(t),i/fps);const buf=await shot();if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%900===0)console.log(i,'/',N,((Date.now()-t0)/1000|0)+'s');}
ff.stdin.end();await new Promise(r=>ff.on('close',r));console.log('errors',errs,'total',(Date.now()-t0)/1000);await b.close();})();
