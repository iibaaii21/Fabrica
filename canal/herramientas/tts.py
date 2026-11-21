import json,sys,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
d=sys.argv[1]; g=json.load(open(d+'/guion.json'))
import os; H=os.path.dirname(os.path.abspath(__file__)); k=Kokoro(H+'/kokoro/kokoro-v1.0.onnx',H+'/kokoro/voices-v1.0.bin')
SR=24000; pause=0.32; out=[]; t=0.35; segs=[]
out.append(np.zeros(int(0.35*SR)))
for f in g['frases']:
    a,sr=k.create(f['t'],voice=g.get('voz','em_alex'),speed=g.get('velocidad',1.1),lang='es')
    a=np.asarray(a,float); th=0.01*np.max(np.abs(a)); nz=np.where(np.abs(a)>th)[0]
    a=a[max(0,nz[0]-240):nz[-1]+480]
    dur=len(a)/SR; segs.append({'ini':round(t,3),'fin':round(t+dur,3),'texto':f.get('pantalla',f['t']),'esc':f['esc']})
    out.append(a); out.append(np.zeros(int(pause*SR))); t+=dur+pause
v=np.concatenate(out); v=v/np.max(np.abs(v))*0.9
sf.write(d+'/voz.wav',v,SR); json.dump({'dur':round(len(v)/SR,3),'segs':segs},open(d+'/tiempos.json','w'),ensure_ascii=False,indent=1)
print('dur',len(v)/SR)
