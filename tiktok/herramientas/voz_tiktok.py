#!/usr/bin/env python3
"""Voz y mezcla de los TikTok originales (receta de VOZ.md).
Uso:  ../../canal/herramientas/kk-venv/bin/python voz_tiktok.py <carpeta> voz      -> voz.wav (procesada) + tiempos.json (escenas según la voz)
      python3 voz_tiktok.py <carpeta> mezcla <musica.ogg>                          -> <id>.mp4 (video-mudo.mp4 + voz + música con ducking + sfx.wav)
Cada frase de guion.json: "t" (texto en pantalla) y "voz" (texto hablado, números en letra; si falta, se usa "t"). "min": duración mínima de la escena (2,0 s por defecto)."""
import json, os, subprocess, sys
D, MODO = sys.argv[1], sys.argv[2]
SR = 24000; CHAIN = ("asetrate=48000*0.965,aresample=48000,atempo=1/0.965,highpass=f=75,equalizer=f=140:t=q:w=1:g=3.5,"
                     "equalizer=f=380:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1:g=3,equalizer=f=7200:t=q:w=1.5:g=-3,"
                     "acompressor=threshold=-20dB:ratio=4:attack=3:release=60:makeup=4,alimiter=limit=0.9")
if MODO == 'voz':
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    H = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'canal', 'herramientas', 'kokoro')
    k = Kokoro(H + '/kokoro-v1.0.onnx', H + '/voices-v1.0.bin')
    g = json.load(open(os.path.join(D, 'guion.json')))
    out, segs, t = [], [], 0.0
    for f in g['frases']:
        a, _ = k.create(f.get('voz', f['t']), voice='em_alex', speed=1.18, lang='es')
        a = np.asarray(a, float); th = 0.01 * np.max(np.abs(a)); nz = np.where(np.abs(a) > th)[0]; a = a[max(0, nz[0] - 120):nz[-1] + 360]
        mx = f.get('max')
        if mx and len(a) / SR > mx - 0.2:   # la frase no cabe: acelerar hasta 1,5
            sp = min(1.5, 1.18 * (len(a) / SR) / (mx - 0.2)); a, _ = k.create(f.get('voz', f['t']), voice='em_alex', speed=sp, lang='es')
            a = np.asarray(a, float); nz = np.where(np.abs(a) > 0.01 * np.max(np.abs(a)))[0]; a = a[max(0, nz[0] - 120):nz[-1] + 360]
        dv = len(a) / SR; dur = max(f.get('min', 2.0), dv + 0.3)
        seg = np.zeros(int(dur * SR)); seg[int(0.08 * SR):int(0.08 * SR) + len(a)] = a[:len(seg) - int(0.08 * SR)]
        out.append(seg); segs.append({'ini': round(t, 3), 'fin': round(t + dur - 0.05, 3), 'texto': f.get('pantalla', f['t']), 'esc': 'A'}); t += dur
    v = np.concatenate(out); v = v / np.max(np.abs(v)) * 0.9
    sf.write(os.path.join(D, 'voz-raw.wav'), v, SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(D, 'voz-raw.wav'), '-af', 'aresample=48000,' + CHAIN, '-ar', '48000', os.path.join(D, 'voz.wav')], check=True)
    os.remove(os.path.join(D, 'voz-raw.wav'))
    json.dump({'dur': round(t, 3), 'segs': segs}, open(os.path.join(D, 'tiempos.json'), 'w'), ensure_ascii=False)
    print('dur', round(t, 2), 'escenas', len(segs))
else:
    mus = sys.argv[3]; ident = os.path.basename(os.path.abspath(D)); dur = json.load(open(os.path.join(D, 'tiempos.json')))['dur'] + 0.4
    sfx = os.path.join(D, 'sfx.wav'); fxin = ['-i', sfx] if os.path.exists(sfx) else ['-f', 'lavfi', '-t', '1', '-i', 'anullsrc=r=48000:cl=mono']
    fc = (f"[1:a]aresample=48000,volume=1.6,asplit[v1][v2];[2:a]aresample=48000,volume=0.22,afade=t=in:d=0.5,afade=t=out:st={dur - 1.0}:d=1.0[mu];"
          f"[3:a]aresample=48000,volume=0.55,apad[fx];[mu][v1]sidechaincompress=threshold=0.04:ratio=8:attack=15:release=250[duck];"
          f"[duck][fx][v2]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(D, 'video-mudo.mp4'), '-i', os.path.join(D, 'voz.wav'), '-stream_loop', '-1', '-i', mus] + fxin +
                   ['-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(dur), '-movflags', '+faststart', os.path.join(D, ident + '.mp4')], check=True)
    print('ok', ident + '.mp4')
