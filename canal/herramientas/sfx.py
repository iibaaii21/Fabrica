# Pista de efectos de sonido sincronizada (sonidos propios del pack SFX). uso: sfx.py <carpeta> <carpeta_wav>
import json,sys,wave,numpy as np
d,lib=sys.argv[1],sys.argv[2]; T=json.load(open(d+'/tiempos.json')); SR=44100
def load(n):
    w=wave.open(f'{lib}/{n}.wav'); a=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768; return a
segs=T['segs']; first=lambda L: next(s['ini'] for s in segs if s['esc']==L)
cues=[(0.0,'move_whoosh_01',0.5)]
for L in ['B','C','D','E']:
    try: st=first(L)-0.9
    except StopIteration: continue
    cues+= [(st,'move_whoosh_01',0.55),(st+0.95,'combat_hit_02',0.25)]
try:
    cues+= [(first('B'),'misc_pop_01',0.35)]
    s4=segs[4]; cues+=[(s4['ini']+0.2,'misc_bounce_01',0.25),(s4['ini']+(s4['fin']-s4['ini'])*0.45,'combat_hit_01',0.35)]
    s6=segs[6]; cues+=[(s6['ini']+0.6,'move_dash_01',0.4)]
    s7=segs[7]; cues+=[(s7['ini'],'pickup_powerup_01',0.18)]
    s8,s10=segs[8],segs[10]; span=s10['fin']-s8['ini']-0.3
    for r in [0,0.22,0.47,0.73]: cues.append((s8['ini']+0.3+r*span,'ui_click_01',0.5))
    cues.append((first('E')-0.2,'state_levelup_01',0.3))
except Exception as e: print('aviso',e)
out=np.zeros(int((T['dur']+1)*SR))
for t,n,g in cues:
    a=load(n)*g; i=int(max(0,t)*SR); j=min(len(out),i+len(a)); out[i:j]+=a[:j-i]
w=wave.open(d+'/sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes()); w.close()
print(len(cues),'efectos')
