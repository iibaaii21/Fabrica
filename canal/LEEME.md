# Canal de YouTube "Modo Examen": producción

Canal en español para AYUDAR A ESTUDIANTES a estudiar mejor, aprobar y aprovechar las clases y las horas de estudio: métodos paso a paso, organización, concentración, memoria, exámenes y herramientas reales (Anki, Quizlet, Notion, Google Calendar, Forest, Pomodoro…) descritas con honestidad. Ver `ESTRATEGIA.md`.

## Decisiones de Ibai (21/11, definitivas; no cambiar sin que él lo pida)
- **Idioma: español.** Canal **"Modo Examen"**.
- **Enfoque: práctico y accionable** (ver `ESTRATEGIA.md`). Las curiosidades, solo como gancho al servicio del consejo. Sin enlaces de afiliado ocultos: si algún día los hay, se declaran.
- **Estilo: STICKMAN v2 colorido** (`herramientas/stick.html` + `stickframes.js`): fondos de color por sección, mucho movimiento, textos grandes con contorno y subtítulos palabra a palabra. El estilo neón 3D queda RETIRADO.
- **Voz: la de Ibai, grabada por él.** Las voces sintéticas (Chatterbox «voz B» y Kokoro) quedan RETIRADAS. **Mientras no haya grabación, no se publica nada en YouTube** (ni tarea de YouTube en el lote). Los vídeos es-s02…s04 y es-l02…l04 se quedan solo como referencia visual.
- **Su voz es un dato personal**: nunca al repositorio (es público) ni a otro sitio. Solo en la sesión, fuera del repo (p. ej. `~/privado/`). En `.gitignore` de cada vídeo: `voz*.wav`, `grabacion*`.
- **Ritmo:** guiones listos para grabar (1 largo y 2 Shorts por tanda); la producción va al ritmo de las grabaciones de Ibai.

## Guion para grabar (cada vídeo nuevo)
- `videos/<id>/guion.json` con las escenas, como siempre, y además `videos/<id>/GUION-PARA-GRABAR.txt`, generado con `python3 herramientas/guion_grabar.py videos/<id>`:
  - texto limpio, una frase corta por línea, números escritos como se leen;
  - una línea en blanco entre frases del guion (cada bloque es una escena);
  - indicaciones de tono entre corchetes (campo `tono` de la frase) y la duración estimada (unas 2,5 palabras por segundo).
- Instrucciones para Ibai (van al principio del archivo):
  - grabar en un sitio silencioso, con el móvil a un palmo;
  - si se equivoca, hacer una pausa y repetir la frase entera (se queda la última toma);
  - dejar 1 s de silencio entre bloques.

## Pipeline con la voz de Ibai
1. Ibai sube la grabación de cada vídeo en la sección «Tu voz» de la app (`config/voz` o documentos en `voces/` con `assetId` y el id del vídeo).
2. Descárgala con la herramienta Artifact (`action: "read"`, url del panel, `path` = assetId) **a una carpeta fuera del repo**.
3. **Limpieza**: `ffmpeg -af "highpass=f=80,agate=threshold=0.02:ratio=2:attack=5:release=200,acompressor=threshold=-20dB:ratio=3:attack=5:release=100,loudnorm=I=-16:TP=-1.5"`, mono 48 kHz. La mezcla final queda a -14 LUFS.
4. **Fallos y repeticiones**: transcribe con faster-whisper (modelo small o medium, CPU, `word_timestamps=True`; huggingface está permitido). Cuando una frase aparece repetida tras una pausa, se queda la ÚLTIMA toma. Se recortan las muletillas largas y los silencios de más de 0,6 s.
5. **Alineado**: frase a frase del guion contra las palabras de whisper (comparación difusa del texto), lo que da `ini`/`fin` de cada frase. Con eso se escribe `tiempos.json` (`{dur, segs:[{ini, fin, texto, esc}]}`) y `voz.wav` limpia.
6. Después, render, efectos y mezcla como siempre (pasos 4-5). `PUBLICAR.txt` dice «Contenido alterado o sintético: No» (voz real de Ibai y animación).

## Pipeline (gratis, sin GPU)
1. **Guion**: `videos/<id>/guion.json`: `{titulo, frases: [{t (texto para la voz, números en letra), pantalla? (texto de subtítulos), esc (estación 3D A..E)}], fuentes: [...]}`. Cada dato, verificado con búsqueda web y con la fuente anotada; si un dato es dudoso, se quita.
2. **Voz**: la grabación de Ibai, limpia y alineada (ver «Pipeline con la voz de Ibai») → `voz.wav` + `tiempos.json`.
   - (Retirado: `tts_cb.py` con Chatterbox y `tts.py` con Kokoro. Se conservan solo para pruebas de escenas, nunca para publicar.)
   - Para probar escenas antes de tener la grabación: `tiempos.json` provisional a 2,5 palabras por segundo en una carpeta temporal.
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
- Short: 35-55 s, vertical. Largo: más de 8 min, 1920x1080, con capítulos. Temas distintos y prácticos.
- YouTube desmonetiza el contenido repetitivo hecho en serie: cada vídeo con guion original, datos comprobados y escena propia.
- Publicación (cuando haya voz de Ibai): en el Lote del domingo con `python3 herramientas/lote_youtube.py subir/lote-AAAA-MM-DD <lunes> <ids...>` (Shorts a las 14:00, largos a las 18:00, uno por día).
