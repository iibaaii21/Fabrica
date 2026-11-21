#!/usr/bin/env python3
"""Genera GUION-PARA-GRABAR.txt (para que Ibai lea el guion en voz alta) a partir de guion.json.
Uso: python3 herramientas/guion_grabar.py canal/videos/<id>
- Una frase corta por línea; línea en blanco entre bloques (cada bloque = una escena del guion).
- Indicaciones de tono entre corchetes (campo "tono" de cada frase) y rótulos de sección.
- Duración estimada a 2,5 palabras por segundo. Saltos de línea de Windows.
"""
import json, os, re, sys

WPS = 2.5

def frases(texto):
    partes = re.split(r'(?<=[.!?…])\s+(?=[¿¡«A-ZÁÉÍÓÚÑ0-9])', texto.strip())
    out = []
    for p in partes:
        # frases muy largas: partir por dos puntos o punto y coma
        if len(p.split()) > 22:
            out += [q.strip() for q in re.split(r'(?<=[:;])\s+', p) if q.strip()]
        else:
            out.append(p)
    return out

def main():
    d = sys.argv[1]
    g = json.load(open(os.path.join(d, 'guion.json'), encoding='utf-8'))
    pal = sum(len(f['t'].split()) for f in g['frases'])
    seg = pal / WPS
    L = [f'GUION PARA GRABAR · {g["titulo"]}',
         f'Duración estimada: {int(seg // 60)} min {int(seg % 60):02d} s ({pal} palabras, a ritmo tranquilo)',
         '',
         'CÓMO GRABARLO',
         '- Sitio silencioso (mejor una habitación con cortinas o ropa), móvil a un palmo de la boca, en modo avión.',
         '- Lee con calma y con naturalidad, como si se lo contaras a un amigo. No hace falta ir rápido.',
         '- Cada bloque es una escena: deja 1 segundo de silencio entre bloques.',
         '- Si te equivocas, haz una pausa y repite la frase entera desde el principio. Me quedo con la última toma.',
         '- Lo que va entre [corchetes] son indicaciones: no se leen.',
         '- Cuando acabes, sube la grabación en la app, en «Tu voz», indicando este vídeo.',
         '', '=' * 60, '']
    for f in g['frases']:
        h = f.get('v', {}).get('head')
        if h:
            L += ['', f'[— {h} —]']
        if f.get('tono'):
            L.append(f'[{f["tono"]}]')
        L += frases(f['t'])
        L.append('')
    L += ['=' * 60, 'FIN. ¡Gracias!']
    out = os.path.join(d, 'GUION-PARA-GRABAR.txt')
    open(out, 'w', encoding='utf-8', newline='').write('\r\n'.join(L) + '\r\n')
    print(out, f'{pal} palabras ≈ {seg / 60:.1f} min')

if __name__ == '__main__':
    main()
