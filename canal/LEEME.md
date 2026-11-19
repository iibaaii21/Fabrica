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
3. **Escena 3D**: copia `render.html` a `videos/<id>/escena.html` y adapta las estaciones al tema del vídeo (objetos y animaciones propios de cada tema; nada de la misma plantilla con otro texto). Requiere `npm install three@0.160.0` en `herramientas/`. En three 0.160, el grosor de TextGeometry es `height` (no `depth`).
4. **Render**: `node frames.js videos/<id> test` (fotogramas de prueba: MÍRALOS y corrige) → `node frames.js videos/<id> full` → `video-mudo.mp4` (1080x1920 a 30 fps; unos 6 min por Short de 40 s).
5. **Audio**: `python3 sfx.py videos/<id> ../../productos/sfx-pack-vol1/wav` (pista de efectos sincronizada; adapta las marcas a cada escena) y luego `./mix.sh videos/<id> ../../productos/music-loops-vol1/ogg/03_puzzle_thinking_96bpm_loop.ogg` → `final.mp4` (voz + música propia con ducking, -14 LUFS).
6. **Miniatura**: `python3 thumb.py <fotograma.jpg> 'TEXTO <em>GANCHO</em>' 'PASTILLA' videos/<id>/miniatura-1280x720.png`.
7. **Ficha**: `videos/<id>/PUBLICAR.txt` con título, descripción (con enlaces a OpoCalc o Cellmate cuando encaje), etiquetas, contenido alterado o sintético (No, salvo que se muestre algo realista inventado) y audiencia "no creado para niños".

## Ritmo y calidad
- 2 Shorts por semana (30-55 s, vertical) y 1 vídeo largo cada 2 semanas (6-10 min, 1920x1080, capítulos).
- YouTube desmonetiza el contenido repetitivo hecho en serie: cada vídeo con guion original, datos comprobados y escena propia.
- Publicación: en el Lote del domingo, programando cada vídeo en días distintos.
