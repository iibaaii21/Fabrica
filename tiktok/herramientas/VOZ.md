# Voz de los TikTok originales (decidido 22/11)
Kokoro em_alex (lang es), velocidad 1.18 (sube hasta 1.5 solo si la frase no cabe en su escena), cada frase colocada al inicio de su escena.
Cadena de procesado (ffmpeg, a 48 kHz):
asetrate=48000*0.965,aresample=48000,atempo=1/0.965,highpass=f=75,equalizer=f=140:t=q:w=1:g=3.5,equalizer=f=380:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1:g=3,equalizer=f=7200:t=q:w=1.5:g=-3,acompressor=threshold=-20dB:ratio=4:attack=3:release=60:makeup=4,alimiter=limit=0.9
Mezcla: voz ×1.6, música ×0.22 con sidechain (ducking) bajo la voz, efectos ×0.55, loudnorm I=-14 TP=-1.5.
El texto hablado lleva los números en letra y cuenta la cifra grande de la escena («Número cinco: tres coma tres millones…»).

## Herramienta (22/11)
- `tiktok/herramientas/voz_tiktok.py <carpeta> voz` (con `canal/herramientas/kk-venv/bin/python`): genera la voz de cada frase (campo `voz`; números en letra), aplica la cadena y escribe `voz.wav` y `tiempos.json`. Cada escena dura lo que su frase + 0,3 s, con un mínimo de 2 s o `min`.
- `python3 tiktok/herramientas/voz_tiktok.py <carpeta> mezcla <música.ogg>`: une `video-mudo.mp4`, la voz, la música con ducking y `sfx.wav`, y escribe `<id>.mp4` a -14 LUFS.
- Motor (`stick.html`), todo opcional:
  - `v.count {to, dec, pre, suf, dur}`: el número grande cuenta hacia arriba.
  - `v.punch`: golpe de zoom al empezar la escena (0,08-0,14).
  - `v.flash`: destello de color de transición.
- Ritmo: escenas cortas (una idea cada 2-3 s), con escenas «#N» de 1,6 s entre cifras.
- Etiqueta de IA: la voz es sintética, así que al subir se activa «Contenido generado por IA».
