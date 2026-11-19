# Voz oficial del canal Modo Examen: Chatterbox multilingüe (MIT) con el timbre de referencia voz-ref.wav
import json,sys,numpy as np,soundfile as sf,torch
from pathlib import Path
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
d=sys.argv[1]; modelo=Path(sys.argv[2]); ref=sys.argv[3]
g=json.load(open(d+'/guion.json'))
m=ChatterboxMultilingualTTS.from_local(modelo,"cpu"); SR=m.sr
torch.manual_seed(1234)
pause=0.30; out=[np.zeros(int(0.35*SR))]; t=0.35; segs=[]
def silencio_max(a):
    fr=int(0.02*SR); e=np.array([np.sqrt(np.mean(a[k:k+fr]**2)) for k in range(0,max(1,len(a)-fr),fr)]); run=mx=0
    for x in e<0.03*e.max(): run=run+1 if x else 0; mx=max(mx,run)
    return mx*0.02
def recorta(a):
    th=0.02*np.max(np.abs(a)); nz=np.where(np.abs(a)>th)[0]; return a[max(0,nz[0]-int(0.01*SR)):nz[-1]+int(0.04*SR)]
for f in g['frases']:
    esperado=max(0.8,len(f['t'])/17); mejor=None
    for intento in range(4):
        torch.manual_seed(1234+intento*101)
        w=m.generate(f['t'],language_id="es",audio_prompt_path=ref,exaggeration=g.get('expresividad',0.45),cfg_weight=g.get('cfg',0.5))
        a=recorta(w.squeeze(0).numpy().astype(float)); dur=len(a)/SR; sm=silencio_max(a)
        pena=abs(np.log(dur/esperado))+max(0,sm-0.45)*3
        if mejor is None or pena<mejor[0]: mejor=(pena,a)
        if 0.65*esperado<=dur<=1.45*esperado and sm<=0.45: break
    a=mejor[1]; dur=len(a)/SR
    segs.append({'ini':round(t,3),'fin':round(t+dur,3),'texto':f.get('pantalla',f['t']),'esc':f['esc']})
    out.append(a); out.append(np.zeros(int(pause*SR))); t+=dur+pause
    print(f"{len(segs)}/{len(g['frases'])} {dur:.1f}s (esperado {esperado:.1f}s, intentos {intento+1})",flush=True)
v=np.concatenate(out); v=v/np.max(np.abs(v))*0.9
sf.write(d+'/voz.wav',v,SR); json.dump({'dur':round(len(v)/SR,3),'segs':segs},open(d+'/tiempos.json','w'),ensure_ascii=False,indent=1)
print('dur',len(v)/SR)
