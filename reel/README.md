# XR Universe Studio — "Beyond the Ordinary" Reel (review cut)

24 s · 1080×1920 · 30 fps · H.264/AAC. Built in Remotion from the Phase 01 keyframes.

## Render

```bash
cd reel
npm install
# In this cloud container the preinstalled Playwright headless shell is used:
export REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell   # omit on a normal machine
node scripts/render.mjs video Reel      out/XR_Universe_Studio_Hybrid_Reel_1080x1920_REVIEW.mp4
node scripts/render.mjs video Reel      out/XR_Universe_Studio_Hybrid_Reel_1080x1920_REVIEW_silent.mp4 --muted
node scripts/render.mjs video ReelClean out/XR_Universe_Studio_Hybrid_Reel_1080x1920_CLEAN_notext.mp4 --muted
node scripts/render.mjs stills qa/stills 45 140 272 380 540 700   # spot-check frames
npx remotion studio src/index.ts                                   # interactive editing
```

Regenerate the soundtrack: `python3 scripts/make_audio.py public/audio/reel_audio.wav` (numpy).

## Adding the official logo

Put the file at `public/brand/logo.png` (transparent PNG or SVG) and pass it as a prop, e.g. in `src/Root.tsx`:
`defaultProps={{showText: true, withAudio: true, logo: staticFile('brand/logo.png')}}`.
Until then the end card shows a dashed "OFFICIAL LOGO" slot — this is a review cut, not the branded final.

## Structure

- `src/Reel.tsx` — all six scenes, headline component, timeline. Every movement is a pure function of the frame number; anchor coordinates are measured on the 1080×1920 masters and listed at the top of the file.
- `public/assets/` — the Phase 01 images used by the edit.
- `public/audio/reel_audio.wav` — original synthesized soundtrack (`scripts/make_audio.py`).
- `public/fonts/` — Sora (SIL OFL 1.1, licence included).
- `out/` — rendered deliverables. `qa/` — contact sheets and the QA report.
