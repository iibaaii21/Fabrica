"""Genera el pack 'Synth Music Loops Vol. 1': bucles musicales originales sintetizados desde cero.
Uso: python3 herramientas/musica_loops.py  -> productos/music-loops-vol1/{wav,ogg}/ + preview.mp3
Todo es determinista (semillas fijas). Los bucles empalman sin corte: la cola de reverb/eco
se suma al principio, así el final enlaza exactamente con el inicio."""
import numpy as np, wave, os, subprocess, shutil
SR = 44100
OUT = os.path.join(os.path.dirname(__file__), '..', 'productos', 'music-loops-vol1')

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
NOTE = {'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}
def chord(name, octave=4):
    root = name.rstrip('m7aj9sus24').rstrip('m') if False else None
    q = name; r = q[:2] if len(q) > 1 and q[1] in '#b' else q[:1]; rest = q[len(r):]
    base = 12 * (octave + 1) + NOTE[r]
    iv = {'':[0,4,7],'m':[0,3,7],'7':[0,4,7,10],'m7':[0,3,7,10],'maj7':[0,4,7,11],'sus2':[0,2,7],'sus4':[0,5,7],'add9':[0,4,7,14],'m9':[0,3,7,10,14]}[rest]
    return [base + i for i in iv]

def env(n, a, d, s, r, sustain_len=None):
    """Envolvente ADSR de longitud exacta n."""
    a, d, r = int(a*SR), int(d*SR), int(r*SR)
    hold = max(0, n - r) if sustain_len is None else min(n, int(sustain_len*SR))
    e = np.zeros(n)
    seg = np.full(hold, float(s))
    if a: k = min(a, hold); seg[:k] = np.linspace(0, 1, a)[:k]
    if d and a < hold: k = min(d, hold - a); seg[a:a+k] = np.linspace(1, s, d)[:k]
    e[:hold] = seg
    last = seg[-1] if hold else s
    k = min(r, n - hold)
    if k > 0: e[hold:hold+k] = np.linspace(last, 0, r)[:k]
    return e

def osc(kind, f, n, phase=0.0, detune=0.0, pw=0.5):
    t = np.arange(n) / SR
    out = np.zeros(n)
    voices = [0.0] if not detune else [-detune, 0.0, detune]
    for dv in voices:
        ff = f * 2 ** (dv / 1200); ph = (t * ff + phase) % 1.0
        if kind == 'sine': w = np.sin(2*np.pi*ph)
        elif kind == 'tri': w = 4*np.abs(ph-0.5)-1
        elif kind == 'saw': w = 2*ph-1
        elif kind == 'square': w = np.where(ph < pw, 1.0, -1.0)
        out += w
    return out / len(voices)

from scipy.signal import lfilter
def lp_fast(x, cutoff):
    """Filtro paso bajo de un polo."""
    a = 1 - np.exp(-2*np.pi*cutoff/SR)
    return lfilter([a], [1, -(1-a)], x)

class Track:
    def __init__(self, bpm, bars, beats=4, tail=4.0):
        self.bpm, self.spb = bpm, 60.0/bpm
        self.n = int(round(bars*beats*self.spb*SR))
        self.buf = np.zeros((self.n + int(tail*SR), 2))
    def beat(self, b): return int(round(b*self.spb*SR))
    def add(self, sig, at_beat, pan=0.0, gain=1.0):
        s = self.beat(at_beat); e = min(len(self.buf), s+len(sig))
        L, R = np.cos((pan+1)*np.pi/4), np.sin((pan+1)*np.pi/4)
        self.buf[s:e, 0] += sig[:e-s]*gain*L*1.4142
        self.buf[s:e, 1] += sig[:e-s]*gain*R*1.4142
    def echo(self, time_beats, fb=0.35, mix=0.25):
        d = self.beat(time_beats); wet = np.zeros_like(self.buf); src = self.buf.copy()
        g = mix
        for k in range(1, 7):
            sh = d*k
            if sh >= len(src): break
            wet[sh:, 0 if k % 2 else 1] += src[:-sh, 0 if k % 2 else 1]*g
            wet[sh:, 1 if k % 2 else 0] += src[:-sh, 1 if k % 2 else 0]*g*0.5
            g *= fb
        self.buf += wet
    def reverb(self, mix=0.2, size=1.0, seed=7):
        rng = np.random.default_rng(seed); ln = int(2.2*size*SR)
        ir = rng.standard_normal((ln, 2)) * np.exp(-np.linspace(0, 6, ln))[:, None]
        ir[:int(0.01*SR)] = 0
        for c in range(2):
            ir[:, c] = lp_fast(ir[:, c], 5000)
            wet = np.fft.irfft(np.fft.rfft(self.buf[:, c], 2**int(np.ceil(np.log2(len(self.buf)+ln))))*np.fft.rfft(ir[:, c], 2**int(np.ceil(np.log2(len(self.buf)+ln)))))[:len(self.buf)]
            self.buf[:, c] += wet/np.max(np.abs(ir[:, c]))/ln**0.5*mix*8
    def finish(self, loop=True, peak=0.89):
        x = self.buf.copy()
        if loop:
            body = x[:self.n].copy(); tail = x[self.n:]
            k = 0
            while k < len(tail):
                m = min(self.n, len(tail)-k); body[:m] += tail[k:k+m]; k += m
            x = body
        else:
            nz = np.where(np.abs(x).max(axis=1) > 1e-4)[0]; x = x[:nz[-1]+1] if len(nz) else x
            f = int(0.05*SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
        # volumen homogéneo entre pistas (RMS objetivo) con limitador suave
        x = x/np.sqrt((x**2).mean())*0.2
        lim = np.abs(x) > 0.8
        x = np.where(lim, np.sign(x)*(0.8 + 0.15*np.tanh((np.abs(x)-0.8)/0.15)), x)
        return x

# ---------- instrumentos ----------
def pad(m, dur, bright=1800):
    n = int(dur*SR); s = sum(osc('saw', hz(k), n, detune=9) for k in m)/len(m)
    return lp_fast(s, bright)*env(n, 0.6, 0.3, 0.8, 0.8, sustain_len=dur-0.6)[:n+int(0.8*SR)][:n] * 0.5
def pad_full(m, dur, bright=1800, rel=0.8):
    n = int((dur+rel)*SR); s = sum(osc('saw', hz(k), n, detune=9) for k in m)/len(m)
    return lp_fast(s, bright)*env(n, 0.5, 0.3, 0.8, rel, sustain_len=dur)[:n]*0.45
def pluck(m, dur=0.5, kind='tri', bright=3500):
    n = int((dur+0.2)*SR); s = osc(kind, hz(m), n)
    return lp_fast(s, bright)*env(n, 0.003, dur, 0.0, 0.2, sustain_len=dur)[:n]
def bell(m, dur=1.5):
    n = int(dur*SR); t = np.arange(n)/SR
    s = np.sin(2*np.pi*hz(m)*t + 1.8*np.exp(-t*3)*np.sin(2*np.pi*hz(m)*3.5*t))
    return s*np.exp(-t*3/dur)*np.minimum(1, t/0.004)
def bass(m, dur, kind='saw', bright=600):
    n = int((dur+0.05)*SR); s = osc(kind, hz(m), n) + 0.5*osc('sine', hz(m-12), n)
    return lp_fast(s, bright)*env(n, 0.005, 0.1, 0.7, 0.05, sustain_len=dur)[:n]*0.6
def lead(m, dur, kind='square', pw=0.5, vib=True):
    n = int((dur+0.08)*SR); t = np.arange(n)/SR
    f = hz(m)*(1 + (0.004*np.sin(2*np.pi*5.5*t)*np.clip((t-0.15)/0.2, 0, 1) if vib else 0))
    ph = np.cumsum(f)/SR
    w = np.where(ph % 1 < pw, 1.0, -1.0) if kind == 'square' else 2*(ph % 1)-1
    return lp_fast(w, 4500)*env(n, 0.006, 0.08, 0.75, 0.08, sustain_len=dur)[:n]*0.35
def kick(gain=1.0):
    n = int(0.35*SR); t = np.arange(n)/SR
    f = 45 + 110*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*gain
def snare(seed=1, gain=1.0):
    n = int(0.22*SR); t = np.arange(n)/SR; r = np.random.default_rng(seed)
    nz = r.standard_normal(n); nz = nz - lp_fast(nz, 1200)
    return (nz*0.7*np.exp(-t*18) + 0.4*np.sin(2*np.pi*190*t)*np.exp(-t*25))*gain
def hat(seed=2, open_=False, gain=1.0):
    n = int((0.25 if open_ else 0.05)*SR); t = np.arange(n)/SR; r = np.random.default_rng(seed)
    nz = r.standard_normal(n); nz = nz - lp_fast(nz, 7000)
    return nz*np.exp(-t*(10 if open_ else 70))*0.35*gain
def chip_noise(seed=3, dur=0.08):
    n = int(dur*SR); r = np.random.default_rng(seed); step = 8
    nz = np.repeat(r.choice([-1.0, 1.0], n//step+1), step)[:n]
    return nz*np.exp(-np.arange(n)/SR*40)*0.4

def melody(chords_seq, scale, rng, beats_per_chord, pattern, octave=5):
    """Melodía original: motivo con notas del acorde + notas de paso de la escala, repetido con variación."""
    notes = []
    motif = None
    for ci, ch in enumerate(chords_seq):
        tones = sorted({(t % 12) for t in chord(ch)})
        if motif is None or ci % 2 == 0:
            motif = [rng.integers(0, len(tones)) for _ in pattern]
        b = ci*beats_per_chord
        for k, (off, du) in enumerate(pattern):
            pc = tones[(motif[k] + (ci // 2)) % len(tones)]
            if rng.random() < 0.25 and k > 0:  # nota de paso
                pc = scale[(scale.index(min(scale, key=lambda s: abs(s-pc))) + 1) % len(scale)]
            notes.append((b+off, du, 12*(octave+1)+pc))
    return notes

def save(name, x, outdir):
    os.makedirs(os.path.join(outdir, 'wav'), exist_ok=True); os.makedirs(os.path.join(outdir, 'ogg'), exist_ok=True)
    p = os.path.join(outdir, 'wav', name+'.wav')
    with wave.open(p, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-c:a', 'libvorbis', '-q:a', '6', os.path.join(outdir, 'ogg', name+'.ogg')], check=True)
    return p

# ---------- piezas ----------
def calm_menu():
    t = Track(78, 16, tail=5); prog = ['Am7', 'Fmaj7', 'Cmaj7', 'G']*2 + ['Dm7', 'Fmaj7', 'Am7', 'Esus4']*2
    for i, c in enumerate(prog):
        t.add(pad_full(chord(c, 3), 4*t.spb, 1400, rel=1.2), i*4, gain=0.55)
        t.add(bass(chord(c, 2)[0], 3.5*t.spb, 'sine', 300), i*4, gain=0.7)
        arp = chord(c, 4) + [chord(c, 5)[0]]
        for k in range(8):
            t.add(pluck(arp[[0, 1, 2, 3, 2, 1, 3, 4][k] % len(arp)], 0.35, 'tri', 2600), i*4+k*0.5, pan=0.4*np.sin(k), gain=0.32)
    t.echo(0.75, 0.4, 0.22); t.reverb(0.35, 1.3); return t.finish()

def action_chip():
    t = Track(150, 16, tail=1.5); prog = ['Em', 'C', 'D', 'Bm']*2 + ['Am', 'C', 'D', 'B7']*2
    rng = np.random.default_rng(11); scale = [4, 6, 7, 9, 11, 0, 2]
    for i, c in enumerate(prog):
        r = chord(c, 2)[0]
        for k in range(8):
            t.add(bass(r + (12 if k % 2 else 0), 0.45*t.spb*1, 'square', 1800), i*4+k*0.5, gain=0.45)
        for k in range(4):
            t.add(kick(0.8) if k % 2 == 0 else chip_noise(k, 0.12)*1.6, i*4+k)
            t.add(chip_noise(30+k, 0.03), i*4+k+0.5, gain=0.6)
    pat = [(0, 0.75), (0.75, 0.75), (1.5, 0.5), (2, 1), (3, 0.5), (3.5, 0.5)]
    for b, d, m in melody(prog, scale, rng, 4, pat, 5):
        t.add(lead(m, d*t.spb*0.9, 'square', 0.25), b, pan=-0.15, gain=0.9)
    t.echo(0.75, 0.3, 0.15); return t.finish()

def puzzle_think():
    t = Track(96, 16, tail=4); prog = ['Dmaj7', 'Gmaj7', 'Em7', 'A7']*2 + ['Bm7', 'Gmaj7', 'Em7', 'Asus4']*2
    rng = np.random.default_rng(5); scale = [2, 4, 6, 7, 9, 11, 1]
    for i, c in enumerate(prog):
        ch = chord(c, 4)
        for k, off in enumerate([0, 1.5, 2.5]):
            for m in ch[:3]: t.add(pluck(m, 0.25, 'sine', 4000), i*4+off, gain=0.18)
        t.add(bass(chord(c, 2)[0], 1.4*t.spb, 'tri', 500), i*4, gain=0.8)
        t.add(bass(chord(c, 2)[2], 0.9*t.spb, 'tri', 500), i*4+2.5, gain=0.6)
        t.add(kick(0.5), i*4); t.add(kick(0.35), i*4+2.5)
        for k in range(8): t.add(hat(k, gain=0.5 if k % 2 else 0.8), i*4+k*0.5, pan=0.3)
        t.add(snare(i, 0.35), i*4+1); t.add(snare(i+50, 0.35), i*4+3)
    pat = [(0, 0.5), (0.5, 0.5), (1, 1), (2.5, 0.5), (3, 1)]
    for b, d, m in melody(prog, scale, rng, 4, pat, 5):
        t.add(bell(m, 1.0), b, pan=-0.3, gain=0.22)
    t.echo(0.5, 0.35, 0.18); t.reverb(0.25, 1.0); return t.finish()

def dark_dungeon():
    t = Track(68, 8, tail=6); prog = ['Dm', 'Bb', 'Gm', 'A']*2
    rng = np.random.default_rng(23); scale = [2, 4, 5, 7, 9, 10, 1]
    drone = np.zeros(t.n); n = t.n; tt = np.arange(n)/SR
    q = lambda f: round(f*n/SR)/(n/SR)  # ciclos enteros en el bucle: empalme sin clic
    drone = (osc('saw', q(hz(38)), n) + osc('saw', q(hz(38)*1.004), n) + 0.6*osc('saw', q(hz(45)), n) + 0.6*osc('saw', q(hz(45)*0.996), n))/2
    drone = lp_fast(np.concatenate([drone, drone]), 220)[n:]*(0.8 + 0.2*np.sin(2*np.pi*tt/(n/SR)))*0.5  # filtrado circular: sin salto al empalmar
    t.add(drone, 0, gain=0.6)
    for i, c in enumerate(prog):
        t.add(pad_full(chord(c, 3), 4*t.spb, 900, rel=2.0), i*4, gain=0.45)
        t.add(kick(0.7), i*4); t.add(kick(0.4), i*4+2.75)
    pat = [(0, 1.5), (2, 1), (3, 1)]
    for b, d, m in melody(prog, scale, rng, 4, pat, 5):
        t.add(bell(m, 2.2), b, pan=0.25, gain=0.2)
    t.reverb(0.6, 1.8); return t.finish()

def retro_racer():
    t = Track(124, 16, tail=2); prog = ['Am', 'F', 'C', 'G']*2 + ['Dm', 'F', 'G', 'Esus4']*2
    rng = np.random.default_rng(42); scale = [9, 11, 0, 2, 4, 5, 7]
    duck = np.ones(t.n + int(2*SR))
    for b in range(64):
        s = t.beat(b); k = int(0.25*SR); duck[s:s+k] = np.minimum(duck[s:s+k], np.linspace(0.35, 1, k))
    for i, c in enumerate(prog):
        r = chord(c, 1)[0]
        for k in range(16): t.add(bass(r + (12 if k % 4 == 2 else 0), 0.22*t.spb, 'saw', 900), i*4+k*0.25, gain=0.42)
        t.add(pad_full(chord(c, 4), 4*t.spb, 2200, rel=0.4), i*4, gain=0.35)
        for k in range(4):
            t.add(kick(1.0), i*4+k)
            if k % 2: t.add(snare(i*4+k, 0.9), i*4+k)
            t.add(hat(k+i, open_=True, gain=0.5), i*4+k+0.5, pan=0.35)
    t.buf[:len(duck)] *= duck[:len(t.buf), None]
    pat = [(0, 1), (1, 0.5), (1.5, 1.5), (3, 1)]
    for b, d, m in melody(prog, scale, rng, 4, pat, 5):
        t.add(lead(m, d*t.spb*0.95, 'saw'), b, pan=0.1, gain=0.6)
    t.echo(0.75, 0.35, 0.2); t.reverb(0.2, 1.0); return t.finish()

def cozy_town():
    t = Track(104, 16, tail=3); prog = ['C', 'Am', 'F', 'G']*2 + ['F', 'G', 'Em', 'Am']*2
    rng = np.random.default_rng(8); scale = [0, 2, 4, 5, 7, 9, 11]
    for i, c in enumerate(prog):
        ch = chord(c, 4)
        t.add(bass(chord(c, 2)[0], 0.9*t.spb, 'tri', 450), i*4, gain=0.8)
        t.add(bass(chord(c, 2)[2]-12, 0.9*t.spb, 'tri', 450), i*4+2, gain=0.6)
        for off in [1, 3]:
            for m in ch: t.add(pluck(m, 0.18, 'square', 1800), i*4+off, gain=0.07)
        t.add(hat(i, gain=0.4), i*4+1); t.add(hat(i+9, gain=0.4), i*4+3)
    pat = [(0, 0.5), (0.5, 0.5), (1, 0.5), (1.5, 1), (3, 0.5), (3.5, 0.5)]
    for b, d, m in melody(prog, scale, rng, 4, pat, 5):
        t.add(pluck(m, d*t.spb*0.8, 'tri', 3000), b, pan=-0.2, gain=0.45)
    t.echo(0.5, 0.25, 0.12); t.reverb(0.2, 0.8); return t.finish()

def stinger_win():
    t = Track(132, 4, tail=3)
    for b, m in [(0, 72), (0.25, 76), (0.5, 79), (0.75, 84)]: t.add(lead(m, 0.2, 'square', 0.25), b, gain=0.9)
    for m in chord('C', 4) + [84]: t.add(pad_full([m], 1.6*t.spb*1, 3000, 1.2), 1, gain=0.35)
    t.add(lead(88, 1.2, 'square', 0.25), 1, gain=0.7); t.add(bell(96, 2.0), 1, gain=0.2)
    t.reverb(0.3, 1.0); return t.finish(loop=False)

def stinger_lose():
    t = Track(90, 4, tail=3)
    for b, m in [(0, 67), (0.5, 66), (1, 65)]: t.add(lead(m, 0.3, 'square', 0.5), b, gain=0.8)
    n = int(1.4*SR); tt = np.arange(n)/SR; f = hz(64)*2**(-tt*0.35)
    w = np.where((np.cumsum(f)/SR) % 1 < 0.5, 1.0, -1.0)
    t.add(lp_fast(w, 2500)*np.exp(-tt*1.8)*0.35, 1.5, gain=0.8)
    t.add(bass(40, 1.2, 'tri', 300), 1.5, gain=0.7)
    t.reverb(0.3, 1.0); return t.finish(loop=False)

PIECES = [
    ('01_calm_menu_78bpm_loop', calm_menu), ('02_action_chiptune_150bpm_loop', action_chip),
    ('03_puzzle_thinking_96bpm_loop', puzzle_think), ('04_dark_dungeon_68bpm_loop', dark_dungeon),
    ('05_retro_racer_124bpm_loop', retro_racer), ('06_cozy_town_104bpm_loop', cozy_town),
    ('07_stinger_victory', stinger_win), ('08_stinger_game_over', stinger_lose),
]

if __name__ == '__main__':
    out = os.path.abspath(OUT); os.makedirs(out, exist_ok=True)
    for name, fn in PIECES:
        x = fn(); save(name, x, out)
        jump = np.abs(x[0]-x[-1]).max() if 'loop' in name else 0
        print(f'{name}: {len(x)/SR:.2f}s peak={np.abs(x).max():.2f} salto_bucle={jump:.4f}')
