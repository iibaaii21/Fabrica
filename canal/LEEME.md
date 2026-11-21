# Canal de YouTube "Modo Examen": producción

Canal educativo en español: explicaciones sencillas (ESO, Bachillerato, universidad), datos curiosos que ayudan a aprender y técnicas de estudio. Ganchos rápidos en el primer segundo ("¿No te acuerdas de lo que estudiaste hace una hora?"), voz calmada y clara, visuales 3D con movimiento fluido.

## Decisiones de Ibai (19/11, definitivas; no cambiar sin que él lo pida)
- **Idioma: español.** Canal **"Modo Examen"**.
- **Estilo: STICKMAN v2 colorido** (`herramientas/stick.html` + `stickframes.js`): fondos de color por sección, mucho movimiento, partículas, temblor, barridos, textos grandes con contorno y subtítulos palabra a palabra también en los vídeos largos. Formatos "Todas las X ordenadas / explicadas / qué pasaría si" (ver `ESTRATEGIA.md`). Más color, movimiento, dopamina y gancho que la competencia. El estilo neón 3D queda RETIRADO.
- **Voz: "voz B".** Chatterbox con el timbre de `herramientas/voz-ref-B.wav` (100 % sintético: Kokoro `bm_george`), `language_id` "es", **cfg 0.0** (quita el acento inglés), expresividad 0.45-0.5. En el guion: `"lang": "es", "cfg": 0.0`.
- **Ritmo:** 1 Short (vertical, `1080 1920 captions`) y 1 vídeo largo de más de 8 min (`1920 1080 captions`) al día.

## Pipeline (gratis, sin GPU)
1. **Guion**: `videos/<id>/guion.json`: `{titulo, frases: [{t (texto para la voz, números en letra), pantalla? (texto de subtítulos), esc (estación 3D A..E)}], fuentes: [...]}`. Cada dato, verificado con búsqueda web y con la fuente anotada; si un dato es dudoso, se quita.
2. **Voz**:
   - Instalación: `python3 -m venv cb-venv && cb-venv/bin/pip install chatterbox-tts "setuptools<81"`.
   - Modelo en `cb-model/`: descarga con curl de `https://huggingface.co/ResembleAI/chatterbox/resolve/main/<archivo>` los archivos `ve.pt`, `t3_mtl23ls_v2.safetensors`, `s3gen.pt`, `grapheme_mtl_merged_expanded_v1.json`, `conds.pt` y `Cangjie5_TC.json`. No uses la API de Hugging Face: limita por IP.
   - Uso: `cb-venv/bin/python tts_cb.py videos/<id> cb-model voz-ref.wav` → `voz.wav` + `tiempos.json`.
   - El script repite sola cada frase que sale demasiado larga, demasiado corta o con silencios raros.
   - Tarda unos 4 s de CPU por cada segundo de audio.
3. **Escenas (stickman v2)**: cada frase lleva `v: {chars:[{x,y?,pose,face,flip?}], props:[{k,x,y,s,d,anim?}], big, bigx, bigy, bigs, bigc, head, wipe, bg, board, boards, ground}`.
   - `head`: rótulo de sección (con `wipe`: barrido de 3 bandas de color al empezar).
   - `bg`: fondos dibujados `bedroom` (noche, estrellas), `classroom` (pizarra con `board`, tamaño `boards`), `lab` (estanterías con matraces) y `library`. Sin `bg`, paleta de color por sección.
   - Props nuevos: `moon`, `pillow`, `alarm` (tiembla con `anim`), `flask` (burbujas), `lamp` (cono de luz), `scale` (`anim` 'left'/'right').
   - 20/11 noche: fondo `stage` (teatro con telón, público y foco de luz en `v.spot`, 0-1), y props `shirt` (camiseta con cara; `anim:'cool'` = azul con estrella), `wheel` (ruleta; gira con `anim`), `ticket` (entrada de 100; `anim:'b'` = 50 azul) y `eye` (ojo que mira y parpadea). Comprobado que es-s02 renderiza idéntico píxel a píxel.
   - 21/11 mañana: fondo `hall` (sala de conciertos: pentagramas que ondulan, notas que cruzan y focos de colores) y props `note` (nota musical; bota con `anim`), `headphones` (ondas con `anim`), `cd` (gira con `anim`), `piano` (teclas que se iluminan con `anim`), `fish` (pez de colores; nada con `anim`), `candy` (caramelo) y `baby`. Comprobado que es-s03 renderiza idéntico píxel a píxel.
   - Para probar escenas antes de tener la voz: copia `guion.json` a una carpeta temporal con un `tiempos.json` provisional (unos 13 caracteres por segundo) y usa `stickbeats.js` sobre esa carpeta.
   - Con pizarra, el personaje fuera de ella (`x≈0.84, flip`) o la cabeza tapa el texto. Los props por encima de `y≈0.3` se cortan en 16:9.
4. **Render**: `node stickbeats.js ../videos/<id> 960 540 0,1,2,...` (los Shorts, SIEMPRE a 1080 1920: en vertical la escala es fija y a media resolución sale todo cortado) (fotograma de cada frase: haz una hoja de contacto, MÍRALA y corrige) → `node stickframes.js ../videos/<id> full 1920 1080 captions` (o `1080 1920` para Shorts) → `video-mudo.mp4`. Un Short de 54 s tarda ~1 min; un largo de 9 min, ~15 min.
   - Si la voz de un Short pasa de 55 s: `ffmpeg -i voz.wav -af atempo=1.12` y escala `tiempos.json` por el mismo factor (guarda los originales como `voz-orig.wav`/`tiempos-orig.json`).
   - Voz del largo (100 frases): ~1 h 30 de CPU. Lánzala en segundo plano y no compitas por CPU con otros renders.
5. **Audio**: `python3 sfx.py videos/<id> ../../productos/sfx-pack-vol1/wav` (`sfx.json`: `[{seg, off, s, g}]`; whoosh en cada `head`, golpe en cada `big`, confirm/error en check/cross) y luego `./mix.sh videos/<id> ../../productos/music-loops-vol1/ogg/<pista>.ogg` → `final.mp4` (voz + música propia con ducking, -14 LUFS). Renombra a `short.mp4` o `video.mp4`.
6. **Miniatura**: `node stickthumb.js spec.json videos/<id>/miniatura-1280x720.png` (`{t, title con <em>, tw, fs, pill, v}`: dibuja una escena stickman a 1280x720 con título).
7. **Ficha**: `videos/<id>/PUBLICAR.txt` (y `CAPITULOS.txt` en los largos, con los inicios de cada `head` sacados de `tiempos.json`) con título, descripción (con enlaces a OpoCalc o Cellmate cuando encaje), etiquetas, contenido alterado o sintético (No, salvo que se muestre algo realista inventado) y audiencia "no creado para niños".

## Ritmo y calidad
- 1 Short (35-55 s, vertical) y 1 vídeo largo (más de 8 min, 1920x1080, capítulos) al día, de temas distintos.
- YouTube desmonetiza el contenido repetitivo hecho en serie: cada vídeo con guion original, datos comprobados y escena propia.
- Publicación: en el Lote del domingo con `python3 herramientas/lote_youtube.py subir/lote-AAAA-MM-DD <lunes> <ids...>` (Shorts a las 14:00, largos a las 18:00, uno por día).
