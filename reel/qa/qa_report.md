# QA report — review cut

Checked with ffprobe/ffmpeg and by viewing frames (contact sheet every second, plus every frame around each scene boundary).

| Check | Result |
|---|---|
| Resolution / fps / frames | 1080×1920, 30 fps, 720 frames, 24.000 s (all three files) |
| Codecs | H.264 yuv420p; AAC 48 kHz stereo 192 kb/s (main file) |
| Black / blank frames | none (blackdetect d≥0.03 s, pix_th 0.06) |
| Loudness | about −18 LUFS integrated, peak −0.9 dBFS |
| Stretching | none — plates are drawn 1:1 at 1080×1920 and only scaled uniformly |
| Frame edges | no exposed edges; every camera move has scale ≥ 1 about a point inside the frame |
| Text | Sora SemiBold 58 px, top band y≈236 (clear of the Reels header and caption area), one line per headline; S03 deliberately text-free |
| Sync | SFX at 2.45 s (light), 3.4 s (reticle), 4.15 s (product), 7.55 s / 9.75 s (match cuts), 12.6 s (selection, frame 378), 16.1 s (reconstruction), 21.0 s (end card) |

## Known limitations
- The product does not rotate: the brief asks for a slight rotation, but the speaker exists only as a flat patch. A real turn needs a 3D model of the product or image-to-video on S02_MASTER.
- The visitor's hand does not move; selection is shown on the screen only, to avoid deforming the hand or face.
- All imagery is AI concept visualization, not footage of a working AR app. The Palmyra overlay is not a verified archaeological reconstruction.
- No official logo: the end card has a labelled placeholder, so this is a **review cut**.
