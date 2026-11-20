#!/usr/bin/env python3
"""Regenera la tarea de YouTube del lote semanal (tabla de programación + carpetas de vídeo + zips de vídeo).

Uso: python3 herramientas/lote_youtube.py subir/lote-2026-11-22 2026-11-23 es-s02-noche-en-vela es-l02-tipos-de-memoria ...
  - 1.er argumento: carpeta del lote.
  - 2.º: lunes de la semana en que se publican (AAAA-MM-DD).
  - resto: ids de canal/videos/<id> en orden. Los Shorts (short.mp4) van a las 14:00 y los largos (video.mp4) a las 18:00,
    uno por día de lunes a domingo, en el orden dado.
Reescribe en LEEME.txt la sección que empieza por "=== 11-YouTube" hasta "ÚLTIMO PASO", mete los vídeos en zips
"<Lote>-parte-N.zip" a partir de la parte 3 (máx. 90 MB cada uno) y actualiza el LEEME dentro de todas las partes.
"""
import datetime as dt, os, re, sys, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MAXB = 90 * 1024 * 1024
TASK = '11-YouTube-programar-videos-de-la-semana'

def titulo(pub):
    t = open(pub, encoding='utf-8').read().replace('\r', '')
    m = re.search(r'TÍTULO:\s*\n(.+)', t)
    return m.group(1).strip() if m else '?'

def main():
    lote, lunes, ids = sys.argv[1], dt.date.fromisoformat(sys.argv[2]), sys.argv[3:]
    lote = os.path.join(ROOT, lote) if not os.path.isabs(lote) else lote
    nombre = 'Lote-' + os.path.basename(lote).split('lote-')[1]
    vids, ns, nl = [], 0, 0
    for i in ids:
        d = os.path.join(ROOT, 'canal', 'videos', i)
        short = os.path.exists(os.path.join(d, 'short.mp4'))
        mp4 = os.path.join(d, 'short.mp4' if short else 'video.mp4')
        assert os.path.exists(mp4), mp4
        k = ns if short else nl
        if short: ns += 1
        else: nl += 1
        assert k < 7, 'más de 7 vídeos del mismo tipo en la semana'
        fecha = lunes + dt.timedelta(days=k)
        extra = [f for f in ('CAPITULOS.txt',) if os.path.exists(os.path.join(d, f))]
        vids.append(dict(id=i, mp4=mp4, d=d, short=short, fecha=fecha, hora='14:00' if short else '18:00',
                         titulo=titulo(os.path.join(d, 'PUBLICAR.txt')), extra=extra))
    vids.sort(key=lambda v: (v['fecha'], v['hora']))
    # --- partes de zip con los vídeos (a partir de la parte 3)
    partes, cur, tam = [], [], 0
    for v in vids:
        s = os.path.getsize(v['mp4']) + 2_000_000
        if cur and tam + s > MAXB: partes.append(cur); cur, tam = [], 0
        cur.append(v); tam += s
    if cur: partes.append(cur)
    for v in vids:
        v['parte'] = next(3 + j for j, p in enumerate(partes) if v in p)
    # --- texto de la tarea
    W = max(len(v['id']) for v in vids) + 2
    ps = [str(3 + j) for j in range(len(partes))]
    donde = 'la PARTE ' + ps[0] if len(ps) == 1 else 'las PARTES ' + ', '.join(ps[:-1]) + ' y ' + ps[-1]
    L = [f'=== {TASK}  (~{6 + 2 * len(vids)} min, está en {donde}) ===',
         'Sube todos los vídeos de golpe y programa cada uno en su día y hora:',
         f'   {"VÍDEO".ljust(W)}| {"FECHA Y HORA (Madrid)".ljust(31)}| TÍTULO']
    for v in vids:
        f = v['fecha']
        L.append(f'   {v["id"].ljust(W)}| {(DIAS[f.weekday()] + f" {f:%d/%m/%Y} a las " + v["hora"]).ljust(31)}| {v["titulo"]}')
    L += ['1. En YouTube Studio (en el canal Modo Examen): Crear > Subir vídeos > arrastra a la vez el short.mp4 o video.mp4 de cada carpeta.',
          '2. Para cada vídeo, copia título, descripción y etiquetas de su PUBLICAR.txt' + (' (en los largos, los capítulos ya van dentro de la descripción: no los borres).' if any(v['extra'] for v in vids) else '.'),
          '3. Audiencia: «No, no es contenido creado para niños». Contenido alterado o sintético: lo que dice su PUBLICAR.txt.',
          '4. Miniatura: sube su miniatura-1280x720.png (en los Shorts a veces solo se elige un fotograma desde la app; si no aparece la opción, sáltalo).',
          '5. Visibilidad: Programar > la fecha y hora de la tabla > Programar.',
          '(Los Shorts antiguos de estilo neón, s01 y s02, ya no se suben: el canal es ahora de dibujos stickman.)', '']
    bloque = '\r\n'.join(L)
    lp = os.path.join(lote, 'LEEME.txt')
    t = open(lp, encoding='utf-8').read().replace('\r\n', '\n')
    a = t.index('=== 11-YouTube'); b = t.index('ÚLTIMO PASO')
    t = t[:a] + bloque.replace('\r\n', '\n') + '\n' + t[b:]
    # cabecera: número de zips
    nz = 2 + len(partes)
    pal = {3: 'TRES', 4: 'CUATRO', 5: 'CINCO'}[nz]
    t = re.sub(r'- El lote va en \w+ zips \([^)]*\)', f'- El lote va en {pal} zips ({", ".join(f"parte-{k}" for k in range(1, nz))} y parte-{nz})', t)
    tot = sum(int(x) for x in re.findall(r'^=== .*?\(~(\d+) min', t, re.M))
    t = re.sub(r'(LOTE DEL DOMINGO [^:]*: \d+ tareas, unos )\d+( minutos)', lambda m: m.group(1) + str(tot) + m.group(2), t)
    open(lp, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
    # --- zips
    for f in os.listdir(lote):
        m = re.match(re.escape(nombre) + r'-parte-(\d+)\.zip$', f)
        if m and int(m.group(1)) >= 3: os.remove(os.path.join(lote, f))
    for j, p in enumerate(partes):
        zp = os.path.join(lote, f'{nombre}-parte-{3 + j}.zip')
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_STORED) as z:
            z.write(lp, 'LEEME.txt')
            for v in p:
                base = f'{TASK}/{v["id"]}/'
                z.write(v['mp4'], base + os.path.basename(v['mp4']))
                for f in ['miniatura-1280x720.png'] + v['extra']:
                    z.write(os.path.join(v['d'], f), base + f)
                pub = open(os.path.join(v['d'], 'PUBLICAR.txt'), encoding='utf-8').read().replace('\r\n', '\n').replace('\n', '\r\n')
                z.writestr(base + 'PUBLICAR.txt', pub.encode('utf-8'))
        print(zp, round(os.path.getsize(zp) / 1e6, 1), 'MB')
    # LEEME dentro de las partes 1 y 2
    for k in (1, 2):
        zp = os.path.join(lote, f'{nombre}-parte-{k}.zip')
        if not os.path.exists(zp): continue
        tmp = zp + '.tmp'
        with zipfile.ZipFile(zp) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
            for it in zi.infolist():
                data = open(lp, 'rb').read() if it.filename == 'LEEME.txt' else zi.read(it.filename)
                zo.writestr(it, data)
        os.replace(tmp, zp)
    print('partes de vídeo:', len(partes), '· vídeos:', len(vids))

if __name__ == '__main__':
    main()
