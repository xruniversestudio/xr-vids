"""Original 37.4 s soundtrack for the XR Universe Studio services film, synthesized from
scratch (no samples, no licensing). 100 BPM, bars of 2.4 s on a grid starting at 1.5 s, so
every scene cut (6.3, 11.1, 15.9, 23.1, 27.9, 32.7) lands on a downbeat. Intro builds over the
ribbons/globe, drops at the first service, whooshes carry each wipe, outro resolves on the mark."""
import sys, wave
import numpy as np

SR = 48000; DUR = 37.4; N = int(SR * DUR); BEAT = 0.6; G0 = 1.5
CUTS = [6.3, 11.1, 15.9, 23.1, 27.9, 32.7]
t = np.arange(N) / SR
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def put(sig, at, g=1.0, pan=0.0):
    i = int(round(at * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += sig[:n] * g * min(1, 1 - pan); R[i:i + n] += sig[:n] * g * min(1, 1 + pan)

def onepole(x, k):
    y = np.empty_like(x); a = 0.0
    kk = np.broadcast_to(np.asarray(k, dtype=np.float64), x.shape)
    for i in range(len(x)): a += kk[i] * (x[i] - a); y[i] = a
    return y

def env(n, a, d):
    x = np.arange(n) / SR
    return np.minimum(x / max(a, 1e-4), 1) * np.exp(-np.maximum(x - a, 0) / d)

# ---------- drums ----------
def kick():
    n = int(.42 * SR); x = np.arange(n) / SR
    f = 46 + 110 * np.exp(-x * 28)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 7.5)
    click = rng.standard_normal(n) * np.exp(-x * 400) * .25
    return np.tanh((body + click) * 1.6)
def clap():
    n = int(.35 * SR); x = np.arange(n) / SR; nz = rng.standard_normal(n)
    e = sum(np.exp(-np.maximum(x - d, 0) * 60) * (x >= d) for d in (0, .011, .022)) + .6 * np.exp(-x * 14)
    return np.diff(np.concatenate([[0], onepole(nz, .5)])) * e * 1.8
def hat(open_=False):
    n = int((.18 if open_ else .05) * SR); x = np.arange(n) / SR
    nz = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
    return nz * np.exp(-x * (22 if open_ else 90)) * .5
K, CL, HC, HO = kick(), clap(), hat(), hat(True)

def groove(a, b, fill_at=None):
    bt = a
    while bt < b - 1e-6:
        i = int(round((bt - a) / BEAT))
        put(K, bt, .95)
        if i % 2 == 1: put(CL, bt, .45, .1)
        for s in range(4):
            tt = bt + s * BEAT / 4
            put(HO if s == 2 else HC, tt, .22 if s == 2 else .12, -.25 if s % 2 else .25)
        bt += BEAT
    if fill_at is not None:  # 16th snare roll rising into the next section
        for s in range(8): put(CL, fill_at + s * BEAT / 4, .15 + .05 * s, .0)

groove(6.3, 15.9 - 4 * BEAT / 4 * 0, fill_at=15.9 - 2 * BEAT)
groove(15.9, 32.7 - 2 * BEAT, fill_at=32.7 - 2 * BEAT)
for bt in np.arange(3.9, 6.3, BEAT / 2): put(HC, bt, .1, .2)

# ---------- harmony: Am – F – C – G, one bar (2 s) each ----------
ROOTS = [110.0, 87.31, 130.81, 98.0]   # Am F C G
TRIADS = [[0, 3, 7], [0, 4, 7], [0, 4, 7], [0, 4, 7]]
def chord_at(tt): i = int(max(0, tt - G0) // 2.4) % 4; return ROOTS[i], TRIADS[i]

# sidechain envelope from the kicks
side = np.ones(N)
for a, b in ((6.3, 32.7 - 2 * BEAT),):
    for bt in np.arange(a, b, BEAT):
        i = int(bt * SR); n = min(int(.45 * SR), N - i); x = np.arange(n) / SR
        side[i:i + n] = np.minimum(side[i:i + n], 1 - .7 * np.exp(-x * 9))

# pad (detuned saws, filtered) throughout
pad = np.zeros(N)
for bar in range(-1, 14):
    a = max(0.0, G0 + bar * 2.4); i0 = int(a * SR); i1 = min(N, int((G0 + bar * 2.4 + 2.55) * SR)); x = t[i0:i1] - a
    if i1 <= i0: continue
    root, tri = chord_at(a + .01); ln = (i1 - i0) / SR; e = np.minimum(x / .3, 1) * np.minimum(np.maximum(ln - x, 0) / .25, 1)
    for st in tri:
        for det in (-.006, 0, .006):
            f = root * 4 * 2 ** (st / 12) * (1 + det)
            pad[i0:i1] += e * (2 * ((f * x) % 1) - 1) * .022
pad = onepole(pad, .06)

# bass: 8th-note saw, filter opens per note, only in the drops
bass = np.zeros(N)
for a, b in ((6.3, 32.7 - 2 * BEAT),):
    for nt in np.arange(a, b, BEAT / 2):
        root, _ = chord_at(nt); n = int(.24 * SR); x = np.arange(n) / SR
        s = (2 * ((root * x) % 1) - 1) + .5 * (2 * ((root * 2.003 * x) % 1) - 1)
        i = int(nt * SR); m = min(n, N - i); bass[i:i + m] += (s * env(n, .004, .12))[:m] * .32
bass = onepole(bass, .09)

# arpeggio pluck (16ths) in the breakdown and second half
arp = np.zeros(N)
for a, b, g in ((3.9, 6.3, .7), (8.7, 32.7, .5), (32.7, 36.3, .8)):
    for k, nt in enumerate(np.arange(a, b, BEAT / 4)):
        root, tri = chord_at(nt); st = tri[k % 3] + (12 if (k // 3) % 2 else 0)
        f = root * 4 * 2 ** (st / 12); n = int(.18 * SR); x = np.arange(n) / SR
        s = np.sign(np.sin(2 * np.pi * f * x)) * .5 + np.sin(2 * np.pi * f * x)
        i = int(nt * SR); m = min(n, N - i); arp[i:i + m] += (s * env(n, .002, .07))[:m] * .09 * g
arp = onepole(arp, .25)

mus = (pad + bass) * side + arp
L += mus; R += mus
# arp ping-pong width
R[int(.125 * SR):] += arp[:-int(.125 * SR)] * .5

# ---------- sound design ----------
def riser(dur):
    n = int(dur * SR); x = np.arange(n) / SR
    nz = rng.standard_normal(n); k = np.linspace(.01, .6, n) ** 2
    s = onepole(nz, k) * (x / dur) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(200 + 1400 * (x / dur) ** 2) / SR) * (x / dur) ** 3 * .25
    return s * 1.6 + tone
def impact(dur=1.8, f=42):
    n = int(dur * SR); x = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(f + 60 * np.exp(-x * 15)) / SR) * np.exp(-x * 2.6)
    crack = onepole(rng.standard_normal(n), .35) * np.exp(-x * 9) * 1.2
    return np.tanh((sub + crack) * 1.4)
def whoosh(dur=.5):
    n = int(dur * SR); x = np.arange(n) / SR
    return onepole(rng.standard_normal(n), np.linspace(.02, .45, n)) * np.sin(np.pi * x / dur) ** 2 * 2.4
def chime(f0, dur=1.4):
    n = int(dur * SR); x = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f0 * m * x) * np.exp(-x * (3 + m * 2.5)) / m for m in (1, 2, 3, 4.2)) * .45
def glitch(dur=.18):
    n = int(dur * SR); x = np.arange(n) / SR
    return np.sign(np.sin(2 * np.pi * 900 * x * (1 + 3 * x))) * (np.floor(x * 60) % 2) * np.exp(-x * 12) * .35

put(riser(1.6), .0, .35)                                   # ribbons fly in
put(impact(1.2, 55), 1.5, .45); put(whoosh(.6), 1.2, .5, -.2)
put(riser(1.8), 1.5, .4)                                    # ribbons wind into orbits
put(chime(659.25, 1.4), 3.3, .35, .2)                        # globe grid
put(impact(1.6, 50), 3.9, .6); put(chime(1046.5, 1.6), 3.9, .4)   # mark resolves
put(glitch(.14), 4.3, .4); put(chime(1318.5, .9), 4.4, .3, -.2)    # AR lock
put(riser(1.4), 4.9, .45)
for k, c in enumerate(CUTS):
    put(whoosh(.6), c - .5, .65, -.35 if k % 2 else .35)    # ribbon wipe
    put(impact(2.0 if k in (0, 5) else 1.3, 42 if k in (0, 5) else 52), c, .95 if k in (0, 5) else .6)
    if k < 5:
        put(chime([880, 987.77, 1046.5, 783.99, 1174.66][k], 1.2), c + 1.1, .35, .25)  # AR scan reveal
        put(glitch(.1), c + 2.4, .25)                                                       # HUD lock
put(chime(523.25, 3.0), 33.3, 1.1); put(chime(783.99, 2.6), 33.4, .7, .3); put(chime(1046.5, 2.4), 33.5, .45, -.3)  # outro: the mark
M = 15.9
put(chime(1318.5, .9), M + 1.0, .3, .2)                                   # body tracking
for sw in (2.5, 4.1): put(glitch(.08), M + sw - .35, .3); put(whoosh(.4), M + sw, .35); put(chime(1567.98, 1.0), M + sw + .5, .3, -.2)  # outfit swaps
put(whoosh(.5), M + 4.6, .45, .3); put(chime(1174.66, 1.2), M + 5.4, .3)     # phone try-on
# outro swell: a held A-minor-add9 pad under the mark
xo = np.arange(int(4.6 * SR)) / SR; sw = np.zeros_like(xo)
for f in (220.0, 261.63, 329.63, 493.88):
    for det in (-.004, 0, .004): sw += (2 * ((f * (1 + det) * xo) % 1) - 1)
sw = onepole(sw * np.minimum(xo / .6, 1) * np.exp(-xo / 4.5) * .11, .05); put(sw, 32.7, 1.0)
# ---------- room reverb (FFT convolution with a decaying-noise IR) ----------
ir_n = int(1.3 * SR); xi = np.arange(ir_n) / SR
irL = rng.standard_normal(ir_n) * np.exp(-xi * 4.2); irR = rng.standard_normal(ir_n) * np.exp(-xi * 4.2)
irL[:200] = 0; irR[:200] = 0
def conv(a, ir):
    m = len(a) + len(ir); nf = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(a, nf) * np.fft.rfft(ir, nf), nf)[:len(a)]
wetL, wetR = conv(L, irL), conv(R, irR)
L = L + wetL * .012; R = R + wetR * .012

mix = np.stack([L, R], 1)
fade = np.ones(N); fi = int(36.0 * SR); fade[fi:] = np.linspace(1, 0, N - fi) ** 1.5
mix *= fade[:, None]
mix = np.tanh(mix / np.max(np.abs(mix)) * 1.6) / np.tanh(1.6) * .78   # gentle glue/limit
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[1])
