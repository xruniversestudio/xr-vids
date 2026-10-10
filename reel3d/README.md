# XR Universe Studio — 3D Reel (review cut)

24 s · 1080×1920 · 30 fps. Real-time 3D (Three.js r160) with studio lighting, soft shadows and bloom,
rendered frame by frame. Every movement is a pure function of time; nothing is random.

| Scene | Time | What happens |
|---|---|---|
| S01 | 0–3 s | Phone lying on a graphite table; camera push-in, the screen wakes up. |
| S02 | 3–8 s | Phone on a stand. Its screen shows a **live render from the phone's own rear camera** looking at the table behind it. The speaker exists only in that camera's layer, so it appears inside the screen and never in the room. Reticle → placement ring → product → slow turn → push into the screen. |
| S03 | 8–10 s | Wireframe of the same speaker (driver rings, grid) morphs into the portrait display. No text. |
| S04 | 10–15 s | Exhibition hall. The AR mirror shows a **live, mirrored camera feed of the visitor in the scene**; the visitor raises an arm and selects "STYLE" at 12.6 s; the camera pushes into the selection. |
| S05 | 15–20 s | Palmyra-inspired colonnade at low sun. A cyan concept reconstruction (missing shaft, entablature, cornice) rises on a scan plane, labelled **CONCEPT RECONSTRUCTION**. |
| S06 | 20–24 s | Cyan frame converges around the logo slot; closing line. |

## Render

```bash
npm install
node render.js stills 4 12.8 18.5          # spot-check → stills/
# full reel in three parallel chunks, then join + audio
PORT=8311 node render.js video 0 240 & PORT=8312 node render.js video 240 480 & PORT=8313 node render.js video 480 720 & wait
./finish.sh
```
`render.js` uses the preinstalled Playwright Chromium with SwiftShader (≈2.5–4 s per frame on CPU).
With the official logo: `LOGO=brand/logo.png node render.js …` (PNG/SVG next to `index.html`).

Audio: `audio/reel_audio.wav`, original synthesis from `make_audio.py`; cues land on 2.45 s, 4.15 s, 7.55 s, 9.75 s, 12.6 s, 16.1 s, 21.0 s.
