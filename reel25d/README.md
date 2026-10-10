# XR Universe Studio — 2.5D Reel (review cut)

24 s · 1080×1920 · 30 fps · H.264/AAC. The Phase 01 photoreal plates are given a real camera:
each plate has a depth map (OpenCV GrabCut segmentation + ground-plane gradient, `scripts/make_depth.py`),
and a WebGL shader moves the camera through it (zoom, dolly, parallax), with motion blur, radial zoom blur
and chromatic aberration on the cuts. A 2D layer adds kinetic type, tracking brackets, measurements,
skeleton tracking, scan lines and the brand frame. Every value is a function of time.

## Edit (cuts land on the 120 BPM grid)
| Time | Shots | Graphics |
|---|---|---|
| 0–3 s | S01 ALT_A → MASTER → ALT_B, a cut each second, screen light blooms | WHAT IF / REALITY / COULD DO more? |
| 3–8 s | Clean phone → product scanned in (registered patch) → ALT_A 360° → product hero | surface scan + floor lattice, lock-on brackets, 34 cm × 52 cm, PRODUCTS |
| 8–10 s | Wireframe speaker → display | procedural box morph, PRODUCT → EXPERIENCE |
| 10–15 s | Wide mirror → visitor (selection at 12.6 s) → push into the mirror | body tracking, hover/selected ring, EXPERIENCES |
| 15–20 s | Palmyra wide with ground scan, reconstruction rises bottom-up, close on the arch | 34.55°N 38.27°E, CONCEPT RECONSTRUCTION, STORIES |
| 20–24 s | Brand background | frame converges, logo slot, WE CREATE / INTERACTIVE / REALITIES. |

## Render
```bash
python3 -I scripts/make_depth.py plates depth          # depth maps (needs opencv-python-headless, numpy)
python3 scripts/make_music.py audio/reel_music.wav     # original soundtrack
node render.js stills 4.1 12.8 17.2                    # spot-check
PORT=8411 node render.js video 0 240 & PORT=8412 node render.js video 240 480 & PORT=8413 node render.js video 480 720 & wait
./finish.sh                                            # join + audio → out/
LOGO=brand/logo.png node render.js …                   # with the official logo (file next to index.html)
```
About 1.5 s per frame on CPU (SwiftShader); the full reel takes ~6 minutes in three processes.

Fonts: Sora, JetBrains Mono (SIL OFL 1.1, licences in `fonts/`). Imagery is AI concept visualization;
the Palmyra overlay is labelled as a concept reconstruction.
