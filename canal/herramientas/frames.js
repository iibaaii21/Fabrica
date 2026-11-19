const { chromium } = require('playwright');const http=require('http'),fs=require('fs'),path=require('path');const {spawn}=require('child_process');
const [,,dir,mode]=process.argv; // mode: test | full
const root=__dirname;const srv=http.createServer((q,r)=>{let f=path.join(root,decodeURIComponent(q.url.split('?')[0]));if(!fs.existsSync(f)||fs.statSync(f).isDirectory()){r.statusCode=404;return r.end()}r.setHeader('content-type',{'.html':'text/html','.js':'text/javascript','.json':'application/json'}[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}).listen(8931);
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
await p.goto('http://localhost:8931/render.html');await p.waitForFunction(()=>window.ready===true,null,{timeout:30000});
const T=JSON.parse(fs.readFileSync(path.join(dir,'tiempos.json')));await p.evaluate(t=>window.setup(t),T);
if(mode==='test'){for(const t of [1.5,4.5,6.5,10,16,19,22.5,25.5,29,33,37.2]){await p.evaluate(t=>window.renderAt(t),t);await p.screenshot({path:path.join(dir,`test-${String(t).replace('.','_')}.jpg`),type:'jpeg',quality:80});}console.log('errors',errs);await b.close();srv.close();return;}
const fps=30,N=Math.ceil(T.dur*fps);const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p',path.join(dir,'video-mudo.mp4')]);
const t0=Date.now();for(let i=0;i<N;i++){await p.evaluate(t=>window.renderAt(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%150===0)console.log(i,'/',N,((Date.now()-t0)/1000|0)+'s');}
ff.stdin.end();await new Promise(r=>ff.on('close',r));console.log('errors',errs,'total',(Date.now()-t0)/1000);await b.close();srv.close();})();
