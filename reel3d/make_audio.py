"""Original soundtrack for the reel: 24 s, 120 BPM pulse (0.5 s beats) aligned to the scene cuts.
Everything is synthesized here, so there is no third-party music to license."""
import wave, sys
import numpy as np

SR = 48000; DUR = 24.0; N = int(SR * DUR)
t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def put(sig, at, g=1.0, pan=0.0):
    i = int(at * SR); n = min(len(sig), N - i)
    if n <= 0: return
    L[i:i+n] += sig[:n] * g * (1 - max(pan, 0)); R[i:i+n] += sig[:n] * g * (1 + min(pan, 0))

def lp(x, k):  # one-pole low-pass, k in (0,1]
    y = np.empty_like(x); a = 0.0
    for i, v in enumerate(x): a += k * (v - a); y[i] = a
    return y

# --- pad: Dm9 -> Bbmaj7 -> Fmaj7 -> C6, 6 s each, slow attack ---
chords = [[146.83, 220.0, 261.63, 329.63], [116.54, 174.61, 220.0, 293.66],
          [174.61, 220.0, 261.63, 329.63], [130.81, 196.0, 261.63, 329.63]]
pad = np.zeros(N)
for ci, ch in enumerate(chords):
    s0 = ci * 6.0; i0 = int(s0 * SR); i1 = min(N, int((s0 + 6.4) * SR)); tt = t[i0:i1] - s0
    env = np.minimum(tt / 1.2, 1) * np.minimum(np.maximum(6.4 - tt, 0) / 1.0, 1)
    for f in ch:
        for d in (-0.003, 0.003):
            pad[i0:i1] += env * np.sin(2 * np.pi * f * (1 + d) * tt + d * 900) * 0.035
pad = lp(pad, 0.12)
L += pad; R += pad

# --- soft pulse: sub kick on every beat from 3.0 s, muted in S03 and the final hold ---
kl = int(0.35 * SR); kt = np.arange(kl) / SR
kick = np.sin(2 * np.pi * (48 * kt + 70 / 20 * (1 - np.exp(-kt * 20)))) * np.exp(-kt * 9)
hl = int(0.05 * SR); hat = np.diff(np.concatenate([[0], rng.standard_normal(hl)])) * np.exp(-np.arange(hl) / SR * 90)
b = 3.0
while b < 21.0:
    if not (8.0 <= b < 10.0):
        put(kick, b, 0.55)
        put(hat, b + 0.25, 0.10, 0.25)
    b += 0.5

# --- sound design ---
def whoosh(dur=0.6, rise=True):
    n = int(dur * SR); x = np.arange(n) / SR; nz = rng.standard_normal(n)
    k = np.linspace(0.02, 0.35, n) if rise else np.linspace(0.35, 0.02, n)
    y = np.empty(n); a = 0.0
    for i in range(n): a += k[i] * (nz[i] - a); y[i] = a
    return y * np.sin(np.pi * x / dur) ** 2 * 2.2

def chime(f0, dur=1.6):
    n = int(dur * SR); x = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f0 * m * x) * np.exp(-x * (3 + m * 2)) / m for m in (1, 2, 3)) * 0.5

def tick():
    n = int(0.05 * SR); x = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * x) * np.exp(-x * 120)

def shimmer(dur=1.7):
    n = int(dur * SR); x = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * (1 + 0.6 * x / dur) * x) for f in (880, 1320, 1760)) / 3
    return y * np.sin(np.pi * x / dur) * 0.35

def hit(dur=2.4):
    n = int(dur * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * 55 * x) + 0.5 * np.sin(2 * np.pi * 110 * x)) * np.exp(-x * 2.2) * 0.8

put(whoosh(0.7), 2.45, 0.5)                     # light gathers into the screen (S01 -> S02)
put(tick(), 3.40, 0.35); put(tick(), 3.55, 0.3)  # placement reticle
put(chime(659.25), 4.15, 0.55, -0.2)            # product appears in the phone
put(whoosh(0.5), 7.55, 0.55)                    # match cut onto the product
put(shimmer(1.6), 8.2, 0.5)                     # wireframe morph
put(whoosh(0.6, False), 9.75, 0.45)             # outline lands on the mirror
put(tick(), 12.40, 0.4)                         # hover
put(chime(880.0, 1.2), 12.60, 0.6, 0.2)         # selection confirmed
put(whoosh(0.6), 14.35, 0.55)                   # element fills the frame
put(shimmer(1.8), 16.10, 0.55)                  # reconstruction rises
put(whoosh(0.7, False), 19.5, 0.4)              # geometry dissolves toward brand
put(hit(), 21.0, 0.7)                           # logo lands
put(chime(523.25, 2.4), 21.0, 0.35)

mix = np.stack([L, R], 1)
fade = np.ones(N); fi = int(22.6 * SR); fade[fi:] = np.linspace(1, 0, N - fi); fade[:int(0.2 * SR)] = np.linspace(0, 1, int(0.2 * SR))
mix *= fade[:, None]
mix /= np.max(np.abs(mix)) / 0.89  # peak about -1 dBFS
out = sys.argv[1]
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', out)
