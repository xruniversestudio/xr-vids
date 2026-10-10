"""Original 24 s soundtrack, 120 BPM, synthesized from scratch (no samples, no licensing).
Structure follows the edit: intro hits on the shot cuts (0/1/2 s), drop at 3 s, breakdown
for the wireframe (8–10 s), second drop at 10 s, final impact at 20 s, logo hit at 21 s."""
import sys, wave
import numpy as np

SR = 48000; DUR = 24.0; N = int(SR * DUR); BEAT = 0.5
t = np.arange(N) / SR
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)

def put(sig, at, g=1.0, pan=0.0):
    i = int(round(at * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += sig[:n] * g * min(1, 1 - pan); R[i:i + n] += sig[:n] * g * min(1, 1 + pan)

def onepole(x, k):
    """low-pass; k may be a scalar or a per-sample array in (0,1]"""
    y = np.empty_like(x); a = 0.0
    kk = np.broadcast_to(np.asarray(k, dtype=np.float64), x.shape)
    for i in range(len(x)): a += kk[i] * (x[i] - a); y[i] = a
    return y

def env(n, a, d):  # attack / exponential decay, seconds
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

groove(3.0, 7.5, fill_at=7.5)
groove(10.0, 19.5, fill_at=19.5)
groove(20.0, 23.0)
for bt in np.arange(1.0, 3.0, BEAT / 2): put(HC, bt, .1, .2)

# ---------- harmony: Am – F – C – G, one bar (2 s) each ----------
ROOTS = [110.0, 87.31, 130.81, 98.0]
TRIADS = [[0, 3, 7], [0, 4, 7], [0, 4, 7], [0, 4, 7]]
def chord_at(tt): i = int(tt // 2) % 4; return ROOTS[i], TRIADS[i]

# sidechain envelope from the kicks
side = np.ones(N)
for a, b in ((3.0, 7.5), (10.0, 19.5), (20.0, 23.0)):
    for bt in np.arange(a, b, BEAT):
        i = int(bt * SR); n = min(int(.45 * SR), N - i); x = np.arange(n) / SR
        side[i:i + n] = np.minimum(side[i:i + n], 1 - .7 * np.exp(-x * 9))

# pad (detuned saws, filtered) throughout
pad = np.zeros(N)
for bar in range(12):
    a = bar * 2.0; i0 = int(a * SR); i1 = min(N, int((a + 2.15) * SR)); x = t[i0:i1] - a
    root, tri = chord_at(a); e = np.minimum(x / .3, 1) * np.minimum(np.maximum(2.15 - x, 0) / .25, 1)
    for st in tri:
        for det in (-.006, 0, .006):
            f = root * 4 * 2 ** (st / 12) * (1 + det)
            pad[i0:i1] += e * (2 * ((f * x) % 1) - 1) * .022
pad = onepole(pad, .06)

# bass: 8th-note saw, filter opens per note, only in the drops
bass = np.zeros(N)
for a, b in ((3.0, 8.0), (10.0, 20.0), (20.0, 23.0)):
    for nt in np.arange(a, b, BEAT / 2):
        root, _ = chord_at(nt); n = int(.24 * SR); x = np.arange(n) / SR
        s = (2 * ((root * x) % 1) - 1) + .5 * (2 * ((root * 2.003 * x) % 1) - 1)
        i = int(nt * SR); m = min(n, N - i); bass[i:i + m] += (s * env(n, .004, .12))[:m] * .32
bass = onepole(bass, .09)

# arpeggio pluck (16ths) in the breakdown and second half
arp = np.zeros(N)
for a, b, g in ((8.0, 10.0, .9), (12.0, 20.0, .55)):
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

put(riser(2.9), .1, .5)                         # build through the intro
for a in (0.0, 1.0, 2.0): put(impact(1.0, 50), a, .55); put(glitch(), a, .4)
put(impact(2.2), 3.0, .9)                       # drop
put(chime(1318.5, 1.2), 3.9, .35, .2); put(impact(1.2, 60), 4.0, .55)  # product materialises
put(whoosh(.45), 5.95, .4, -.3); put(whoosh(.45), 6.95, .4, .3)        # quick cuts
put(riser(1.9), 8.05, .45)                      # wireframe build
put(impact(2.2), 10.0, .85)                     # second drop
put(chime(880, 1.3), 12.6, .55, .25); put(glitch(.12), 12.6, .35)       # selection
put(whoosh(.5), 14.5, .55)
put(impact(1.6, 48), 15.0, .7)                  # Palmyra
put(riser(1.9), 16.5, .3)                       # reconstruction scan
put(chime(659.25, 1.6), 18.4, .4, -.2)
put(riser(.5), 19.5, .4)
put(impact(3.0, 38), 20.0, 1.0)                 # final impact
put(chime(523.25, 2.6), 21.0, .5); put(impact(1.5, 70), 21.0, .4)       # logo

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
fade = np.ones(N); fi = int(23.0 * SR); fade[fi:] = np.linspace(1, 0, N - fi) ** 1.5
mix *= fade[:, None]
mix = np.tanh(mix / np.max(np.abs(mix)) * 1.6) / np.tanh(1.6) * .78   # gentle glue/limit
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[1])
