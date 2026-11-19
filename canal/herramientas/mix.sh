#!/bin/bash
# uso: mix.sh <carpeta> <musica.ogg>
d=$1; m=$2
dur=$(python3 -c "import json;print(json.load(open('$d/tiempos.json'))['dur']+0.6)")
ffmpeg -v error -y -i "$d/video-mudo.mp4" -i "$d/voz.wav" -stream_loop -1 -i "$m" -filter_complex \
"[1:a]aresample=48000,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,volume=1.6,asplit[v1][v2];\
[2:a]aresample=48000,volume=0.11,afade=t=in:d=1,afade=t=out:st=$(python3 -c "print($dur-1.2)"):d=1.2[mu];\
[mu][v1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t $dur -movflags +faststart "$d/final.mp4"
