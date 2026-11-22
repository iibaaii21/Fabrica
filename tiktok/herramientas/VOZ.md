# Voz de los TikTok originales (decidido 22/11)
Kokoro em_alex (lang es), velocidad 1.18 (sube hasta 1.5 solo si la frase no cabe en su escena), cada frase colocada al inicio de su escena.
Cadena de procesado (ffmpeg, a 48 kHz):
asetrate=48000*0.965,aresample=48000,atempo=1/0.965,highpass=f=75,equalizer=f=140:t=q:w=1:g=3.5,equalizer=f=380:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1:g=3,equalizer=f=7200:t=q:w=1.5:g=-3,acompressor=threshold=-20dB:ratio=4:attack=3:release=60:makeup=4,alimiter=limit=0.9
Mezcla: voz ×1.6, música ×0.22 con sidechain (ducking) bajo la voz, efectos ×0.55, loudnorm I=-14 TP=-1.5.
El texto hablado lleva los números en letra y cuenta la cifra grande de la escena («Número cinco: tres coma tres millones…»).
