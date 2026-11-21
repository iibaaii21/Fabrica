#!/usr/bin/env python3
"""Genera Soft UI Sounds Vol. 2 (sonidos de interfaz suaves, sintetizados desde cero).
Uso: python3 herramientas/sfx_ui.py  -> productos/ui-sounds-vol2/wav/*.wav (44,1 kHz, 16 bits, mono)"""
import numpy as np, os, wave
from scipy.signal import butter, sosfilt
SR = 44100
OUT = os.path.join(os.path.dirname(__file__), '..', 'productos', 'ui-sounds-vol2', 'wav')
rng = np.random.default_rng(2026)

def t_(d): return np.arange(int(SR * d)) / SR
def env(n, a=0.002, d=0.08, curve=6.0):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-curve * np.maximum(0, t - a) / max(d, 1e-4))
    return e
def tone(f, d, kind='sine', a=0.002, dec=0.1, curve=6.0, glide=None, fm=0.0, fmr=2.0):
    t = t_(d); fr = np.full(len(t), float(f)) if glide is None else np.linspace(f, glide, len(t))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    if fm: ph = ph + fm * np.sin(ph * fmr)
    if kind == 'sine': w = np.sin(ph)
    elif kind == 'tri': w = 2 / np.pi * np.arcsin(np.sin(ph))
    elif kind == 'square': w = np.tanh(4 * np.sin(ph)) * 0.6
    return w * env(len(t), a, dec, curve)
def noise(d, lp=4000, hp=200, a=0.001, dec=0.02, curve=6.0):
    n = rng.standard_normal(int(SR * d)); X = np.fft.rfft(n); f = np.fft.rfftfreq(len(n), 1 / SR)
    X[(f > lp) | (f < hp)] = 0; n = np.fft.irfft(X, len(n)); n /= np.max(np.abs(n)) + 1e-9
    return n * env(len(n), a, dec, curve)
def sweep_noise(d, f0, f1, a=0.01):
    n = rng.standard_normal(int(SR * d)); out = np.zeros_like(n); y = 0.0
    fc = np.linspace(f0, f1, len(n)); al = 1 - np.exp(-2 * np.pi * fc / SR)
    for i in range(len(n)): y += al[i] * (n[i] - y); out[i] = y
    out /= np.max(np.abs(out)) + 1e-9; e = np.sin(np.linspace(0, np.pi, len(n))) ** 1.5
    return out * e
def mix(*parts):
    L = max(len(p[1]) + int(p[0] * SR) for p in parts); o = np.zeros(L)
    for off, s, g in parts: i = int(off * SR); o[i:i + len(s)] += s * g
    return o
def seq(notes, kind='sine', gap=0.07, dec=0.12, g=1.0, **kw):
    return mix(*[(i * gap, tone(f, dec * 3, kind, dec=dec, **kw), g) for i, f in enumerate(notes)])
def reverb(s, wet=0.18):
    o = np.copy(s)
    for dly, gn in ((0.031, 0.5), (0.047, 0.4), (0.071, 0.3), (0.113, 0.2), (0.163, 0.12)):
        k = int(dly * SR); o = np.concatenate([o, np.zeros(k)]); o[k:k + len(s)] += s * gn * wet / 0.5
    return o
def save(name, s, peak=0.89):
    s = sosfilt(butter(2, 40, 'highpass', fs=SR, output='sos'), s); s = s / (np.max(np.abs(s)) + 1e-9) * peak
    nz = np.where(np.abs(s) > 0.001)[0]; s = s[: nz[-1] + 1] if len(nz) else s
    f = int(0.004 * SR); s[-f:] *= np.linspace(1, 0, f)
    with wave.open(os.path.join(OUT, name + '.wav'), 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((s * 32767).astype('<i2').tobytes())
C = {n: 440 * 2 ** ((i - 9) / 12) for i, n in enumerate('C Db D Eb E F Gb G Ab A Bb B'.split())}
def N(n, o): return C[n] * 2 ** (o - 4)

def main():
    os.makedirs(OUT, exist_ok=True)
    S = {}
    # clicks
    S['click_soft_01'] = mix((0, noise(0.05, 6000, 800, dec=0.012), 0.5), (0, tone(1800, 0.06, dec=0.022), 0.6))
    S['click_soft_02'] = mix((0, noise(0.05, 3500, 300, dec=0.014), 0.6), (0, tone(1100, 0.07, dec=0.025), 0.5))
    S['click_pop_01'] = tone(700, 0.06, glide=1300, dec=0.018)
    S['click_pop_02'] = tone(500, 0.07, glide=900, dec=0.022, kind='tri')
    S['click_wood_01'] = mix((0, tone(1250, 0.08, dec=0.025, fm=1.2, fmr=2.76), 1), (0, noise(0.02, 5000, 1500, dec=0.004), 0.3))
    S['click_glass_01'] = reverb(mix((0, tone(2637, 0.15, dec=0.04), 0.6), (0, tone(3951, 0.12, dec=0.025), 0.3)), 0.2)
    # hover
    S['hover_01'] = tone(1500, 0.07, dec=0.025) * 0.6
    S['hover_02'] = tone(900, 0.06, glide=1100, dec=0.02, kind='tri') * 0.6
    S['hover_03'] = noise(0.06, 9000, 3000, a=0.004, dec=0.02) * 0.5
    # toggles
    S['toggle_on_01'] = seq([N('E', 5), N('B', 5)], gap=0.05, dec=0.04)
    S['toggle_off_01'] = seq([N('B', 5), N('E', 5)], gap=0.05, dec=0.04)
    S['toggle_on_02'] = mix((0, noise(0.02, 4000, 500, dec=0.004), 0.5), (0.01, tone(880, 0.08, glide=1320, dec=0.03), 0.8))
    S['toggle_off_02'] = mix((0, noise(0.02, 4000, 500, dec=0.004), 0.5), (0.01, tone(1320, 0.08, glide=880, dec=0.03), 0.8))
    # confirm
    S['confirm_01'] = reverb(seq([N('C', 5), N('G', 5)], gap=0.07, dec=0.08))
    S['confirm_02'] = reverb(seq([N('E', 5), N('G', 5), N('C', 6)], gap=0.06, dec=0.07, kind='tri'))
    S['confirm_03'] = reverb(mix((0, tone(N('A', 5), 0.4, dec=0.12, fm=0.8, fmr=3.5), 1), (0.05, tone(N('E', 6), 0.4, dec=0.12, fm=0.8, fmr=3.5), 0.7)))
    S['confirm_04'] = reverb(seq([N('G', 4), N('D', 5)], gap=0.09, dec=0.1, kind='sine', fm=0.5, fmr=2))
    # cancel / back
    S['cancel_01'] = reverb(seq([N('G', 5), N('C', 5)], gap=0.07, dec=0.08))
    S['cancel_02'] = seq([N('E', 5), N('C', 5)], gap=0.06, dec=0.06, kind='tri')
    S['back_01'] = mix((0, sweep_noise(0.12, 3000, 600), 0.4), (0, tone(1000, 0.1, glide=600, dec=0.04), 0.6))
    # errors
    S['error_01'] = mix((0, tone(220, 0.12, dec=0.06, kind='square'), 0.6), (0.13, tone(196, 0.16, dec=0.08, kind='square'), 0.6))
    S['error_02'] = seq([N('Eb', 4), N('Eb', 4)], gap=0.11, dec=0.05, kind='tri')
    S['error_03'] = mix((0, tone(160, 0.25, dec=0.12, fm=3, fmr=1.41), 1), (0, noise(0.05, 1500, 100, dec=0.02), 0.3))
    # notifications
    S['notify_01'] = reverb(seq([N('C', 6), N('E', 6), N('G', 6)], gap=0.09, dec=0.15, fm=0.6, fmr=3.5), 0.3)
    S['notify_02'] = reverb(seq([N('G', 5), N('C', 6)], gap=0.12, dec=0.2, fm=0.9, fmr=2.0), 0.3)
    S['notify_03'] = reverb(mix((0, tone(N('E', 6), 0.8, dec=0.3, fm=1.4, fmr=3.5), 1)), 0.3)
    S['notify_04'] = reverb(seq([N('A', 5), N('E', 6), N('A', 6)], gap=0.07, dec=0.1, kind='tri'), 0.25)
    S['message_01'] = reverb(mix((0, tone(N('D', 6), 0.3, glide=N('A', 6), dec=0.08), 0.8), (0.08, tone(N('A', 6), 0.3, dec=0.1), 0.6)), 0.25)
    # open / close
    S['open_01'] = mix((0, sweep_noise(0.18, 400, 4000), 0.5), (0.05, tone(700, 0.12, glide=1100, dec=0.05), 0.5))
    S['close_01'] = mix((0, sweep_noise(0.18, 4000, 400), 0.5), (0.05, tone(1100, 0.12, glide=700, dec=0.05), 0.5))
    S['open_02'] = reverb(seq([N('C', 5), N('E', 5), N('G', 5), N('C', 6)], gap=0.035, dec=0.05, kind='tri'))
    S['close_02'] = reverb(seq([N('C', 6), N('G', 5), N('E', 5), N('C', 5)], gap=0.035, dec=0.05, kind='tri'))
    # typing
    for k in range(4):
        f = [1700, 2100, 1500, 2400][k]
        S[f'type_{k + 1:02d}'] = mix((0, noise(0.05, 7000, 1200, dec=0.012), 0.7), (0, tone(f, 0.05, dec=0.015), 0.35))
    # slider
    S['slider_tick_01'] = tone(2400, 0.05, dec=0.012) * 0.7
    S['slider_tick_02'] = mix((0, noise(0.04, 9000, 4000, dec=0.01), 0.6), (0, tone(3000, 0.05, dec=0.012), 0.4))
    # rewards
    S['reward_coin_01'] = seq([N('B', 5), N('E', 6)], gap=0.06, dec=0.12, kind='square')
    S['reward_star_01'] = reverb(seq([N('C', 6), N('G', 6), N('C', 7), N('E', 7)], gap=0.05, dec=0.1, fm=0.4, fmr=4), 0.3)
    S['reward_xp_01'] = mix((0, tone(500, 0.35, glide=1600, dec=0.2, kind='tri'), 0.6), (0.3, tone(N('C', 6), 0.4, dec=0.15), 0.6))
    S['purchase_01'] = reverb(mix((0, noise(0.04, 6000, 2000, dec=0.01), 0.4), (0.02, seq([N('E', 6), N('A', 6)], gap=0.08, dec=0.15, fm=1.0, fmr=3.5), 1)), 0.25)
    S['unlock_01'] = reverb(mix((0, tone(300, 0.08, dec=0.02, kind='square'), 0.4), (0.06, noise(0.03, 3000, 400, dec=0.008), 0.5), (0.1, seq([N('G', 5), N('D', 6), N('G', 6)], gap=0.06, dec=0.1), 0.8)), 0.25)
    S['complete_01'] = reverb(mix((0, seq([N('C', 5), N('E', 5), N('G', 5)], gap=0.08, dec=0.1), 0.8), (0.26, mix((0, tone(N('C', 6), 0.9, dec=0.35, fm=0.5, fmr=2), 1), (0, tone(N('E', 6), 0.9, dec=0.35), 0.6), (0, tone(N('G', 6), 0.9, dec=0.35), 0.5)), 0.8)), 0.3)
    S['delete_01'] = mix((0, sweep_noise(0.2, 2500, 200), 0.6), (0, tone(600, 0.18, glide=150, dec=0.08, kind='tri'), 0.5))
    S['copy_01'] = seq([N('A', 5), N('A', 5)], gap=0.06, dec=0.03)
    for k, s in S.items(): save(k, s)
    print(len(S), 'sonidos en', os.path.abspath(OUT))

if __name__ == '__main__':
    main()

# ---------- página de escucha (itch.io, HTML) ----------
CATS = [("CLICKS & HOVER", ("click_", "hover_", "slider_")), ("TOGGLES", ("toggle_",)), ("CONFIRM & CANCEL", ("confirm_", "cancel_", "back_", "error_")),
        ("NOTIFICATIONS", ("notify_", "message_")), ("PANELS", ("open_", "close_")), ("TYPING & EDIT", ("type_", "copy_", "delete_")),
        ("REWARDS", ("reward_", "purchase_", "unlock_", "complete_"))]
def peaks(path, n=40):
    w = wave.open(path); a = np.abs(np.frombuffer(w.readframes(w.getnframes()), '<i2') / 32768)
    ch = np.array_split(a, n); p = np.array([c.max() if len(c) else 0 for c in ch]); return [round(float(v), 3) for v in p / (p.max() + 1e-9)]
def preview(store, cta='Get the full pack on itch.io →', cta2=None, top=''):
    import json
    names = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith('.wav'))
    P = {n: peaks(os.path.join(OUT, n + '.wav')) for n in names}
    cats = [[t, list(p)] for t, p in CATS]
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Soft UI Sounds Vol. 2 — Listen to every sound</title>
<meta name="description" content="Preview all {len(names)} soft interface sounds: clicks, toggles, notifications, rewards. Royalty-free WAV files for games and apps.">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f2ff;color:#1d1836;font:15px/1.5 Inter,-apple-system,"Segoe UI",sans-serif}}
.wrap{{max-width:1000px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-size:clamp(30px,6vw,52px);line-height:1;margin:0 0 8px;letter-spacing:-.03em}}
.g{{background:linear-gradient(90deg,#7c5cff,#ff6fb1 60%,#ffb35c);-webkit-background-clip:text;background-clip:text;color:transparent}}
.sub{{color:#5e5679;margin:0 0 22px}}
.cat{{font:600 12px "JetBrains Mono",monospace;letter-spacing:.2em;color:#7c5cff;margin:26px 0 10px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}}
button{{all:unset;cursor:pointer;display:grid;gap:6px;padding:12px 14px;border-radius:14px;background:#fff;border:1px solid #e3dcff;box-shadow:0 2px 6px rgba(60,40,140,.06);transition:.15s}}
button:hover,button:focus-visible{{border-color:#7c5cff;transform:translateY(-1px)}}
button.on{{border-color:#ff6fb1;background:#fff5fa}}
button span{{font:13px "JetBrains Mono",monospace}}
canvas{{width:100%;height:28px}}
.cta{{display:inline-block;margin-top:6px;padding:12px 20px;border-radius:999px;background:linear-gradient(90deg,#7c5cff,#ff6fb1);color:#fff;font-weight:800;text-decoration:none}}
footer{{margin-top:40px;color:#8a83a3;font-size:13px}}
</style>{top}</head><body><div class="wrap">
<h1>Soft UI Sounds <span class="g">Vol. 2</span></h1>
<p class="sub">Tap any sound to hear it. {len(names)} original, gentle interface sounds for menus, apps and cozy games · 44.1 kHz WAV · royalty-free, no attribution required.</p>
<a class="cta" href="{store}">{cta}</a>
<div id="list"></div>
<p style="margin-top:30px"><a class="cta" href="{store}">{cta2 or f"Download all {len(names)} sounds →"}</a></p>
<footer>All sounds synthesized from scratch with code.</footer></div>
<script>
const N={json.dumps(names)},P={json.dumps(P)};
const C={json.dumps(cats)};
const L=document.getElementById('list');let cur=null;
C.forEach(([t,ps])=>{{const h=document.createElement('div');h.className='cat';h.textContent=t;L.appendChild(h);const g=document.createElement('div');g.className='grid';L.appendChild(g);
N.filter(n=>ps.some(p=>n.startsWith(p))).forEach(n=>{{const b=document.createElement('button');b.innerHTML='<span>'+n+'.wav</span><canvas width="400" height="56"></canvas>';g.appendChild(b);
const c=b.querySelector('canvas'),x=c.getContext('2d'),gr=x.createLinearGradient(0,0,400,0);gr.addColorStop(0,'#7c5cff');gr.addColorStop(1,'#ff6fb1');x.fillStyle=gr;const pk=P[n],bw=400/pk.length;pk.forEach((v,i)=>{{const bh=Math.max(3,v*52);x.beginPath();x.roundRect(i*bw+1.5,(56-bh)/2,bw-3,bh,3);x.fill()}});
const a=new Audio('wav/'+n+'.wav');a.preload='none';
b.onclick=()=>{{if(cur&&cur!==a){{cur.pause();cur.currentTime=0}}document.querySelectorAll('button.on').forEach(e=>e.classList.remove('on'));b.classList.add('on');a.currentTime=0;a.play();cur=a;a.onended=()=>b.classList.remove('on')}}}})}});
</script></body></html>'''
