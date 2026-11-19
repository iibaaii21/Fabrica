import base64,sys,subprocess
frame,title_html,pill,out=sys.argv[1:5]
img='data:image/jpeg;base64,'+base64.b64encode(open(frame,'rb').read()).decode()
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1280px;height:720px;overflow:hidden;background:#140d3a;font-family:"Inter Display",Inter,sans-serif;position:relative}}
.bg{{position:absolute;inset:0;background:radial-gradient(70% 90% at 80% 40%,#5b2bbf 0%,transparent 60%),radial-gradient(60% 80% at 0% 100%,#0e6b8c 0%,transparent 60%),#140d3a}}
.shot{{position:absolute;right:-30px;top:-10px;width:620px;height:740px;background:url({img}) center 0/620px auto;transform:rotate(5deg);border-radius:40px;box-shadow:0 30px 80px rgba(0,0,0,.6);border:8px solid #fff}}
.t{{position:absolute;left:56px;top:70px;width:690px;color:#fff;font-weight:900;font-size:118px;line-height:.95;letter-spacing:-.03em;text-shadow:0 10px 30px rgba(0,0,0,.5)}}
.t em{{font-style:normal;color:#ffc145}}
.pill{{position:absolute;left:56px;bottom:70px;background:#ff5d73;color:#fff;font-weight:900;font-size:46px;padding:14px 30px;border-radius:18px;transform:rotate(-2deg)}}
</style></head><body><div class="bg"></div><div class="shot"></div><div class="t">{title_html}</div><div class="pill">{pill}</div></body></html>'''
open('thumb.html','w').write(html)
subprocess.run(['node','-e',"const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});await p.goto('file://'+process.cwd()+'/thumb.html');await p.waitForTimeout(300);await p.screenshot({path:'"+out+"'});await b.close()})()"],check=True)
