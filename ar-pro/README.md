# XR Universe Studio — أنواع الواقع المعزز (3D Pro)

36 s · 30 fps · two masters from one scene file:
- `out/XR_Universe_AR_Types_Reel_1080x1920.mp4` — Instagram Reel (9:16)
- `out/XR_Universe_AR_Types_1920x1080.mp4` — horizontal (16:9)

Real-time 3D (Three.js r160): glTF PBR models, soft shadows, studio environment reflections, bloom,
Arabic type (Cairo). Brand palette taken from the XR Universe Studio logo. Every motion is a function of time.

| Time | Scene | 3D content |
|---|---|---|
| 0–4 s | Intro | XR mark rises from a mirror floor, brand rings |
| 4–8.5 s | 1 · القائم على العلامات | Chronograph watch rises over a printed marker (with the XR mark); phone shows its rear-camera feed |
| 8.5–13 s | 2 · بدون علامات | Room scan → velvet sofa placed at true size (219 × 79 cm), armchair, iridescent lamp |
| 13–17.5 s | 3 · القائم على الموقع | Dusk city with lit windows, river, pins, route, landmark card |
| 17.5–22 s | 4 · القائم على الإسقاط | Projector turns the table into a touch interface |
| 22–26.5 s | 5 · القائم على التراكب | Scan ring reveals the helmet's inner structure (holographic shell + components) |
| 26.5–31 s | 6 · القائم على التحديد | Night road: lanes, concept car and pedestrian outlined |
| 31–36 s | Outro | Logo, «المستقبل… مُعزَّز», call to action |

## Swapping in your own models
Drop `.glb` files into `models/` and change the file name in `index.html` (`MODELS.<name>` in the scene's
`build`). `prep(gltf, { width | height | depth })` scales any model to real metres and stands it on the floor.

## Render
```bash
npm install
FMT=h node render.js stills 6.6 25        # horizontal spot-check → stills/
FMT=v node render.js stills 6.6 25        # vertical
./run_all.sh                              # both formats, 3 processes each, + soundtrack → out/
```
CPU (SwiftShader) ≈ 4–10 s per frame per process.

## Credits
3D models: Khronos glTF Sample Assets — all licensed for commercial use:
ChronographWatch (CC-BY 4.0, graphiccompressor), GlamVelvetSofa (CC-BY 4.0, Wayfair LLC), IridescenceLamp (CC-BY 4.0, Wayfair LLC),
SheenChair (CC0), SciFiHelmet (CC0), CarConcept (CC0). Source: KhronosGroup/glTF-Sample-Assets. Fonts: Cairo, JetBrains Mono (SIL OFL 1.1).
Music: original synthesis (`scripts/music_v1.py`).
