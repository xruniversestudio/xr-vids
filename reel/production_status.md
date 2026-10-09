# Production status — XR Universe Studio Hybrid Reel

| Phase | State | Notes |
|---|---|---|
| Phase 01 — keyframes | qa_passed (inherited) | 24 assets + 2 RGBA line layers from the supplied ZIP; SHA-256 verified 61/61. S04_ALT_B needs_revision (unused). |
| Phase 02 — motion | generated · qa_passed | Deterministic compositing in Remotion (no AI video). See method per scene below. |
| Phase 03 — edit, audio, export | generated · qa_passed | Review cut exported. Official logo missing → **blocked for final branding**. |

## Method per scene

| Scene | Frames | Sources | Motion |
|---|---|---|---|
| S01 | 0–89 | S01_MASTER | 4% push-in toward the screen; light gathers in the screen (frames 66–90). |
| S02 | 90–239 | S02_CLEAN_PHONE + S02_MASTER patch [316,689,783,1315] | Placement reticle inside the screen, top-to-bottom scan reveals the product (only the registered patch changes), push-in, then a 2.15× move onto the product that lines up with the S03 speaker. |
| S03 | 240–299 | S03_WIREFRAME_START / END | Procedural SVG box (front face, depth edges, grid) interpolates from the speaker bounds to the display bounds while the references cross-fade. Text-free. |
| S04 | 300–449 | S04_BEFORE / AFTER (differ only at [584,565,639,624]) | Cyan outline resolves onto the mirror while the camera pulls back from 1.32×; hover ring, selection at frame 378 (12.6 s) with ripple; selected element grows to fill the frame. The visitor is not animated (no hand warping). |
| S05 | 450–599 | S05_REAL_WORLD + S05_OVERLAY_ISOLATED_RGBA | 5% push; reconstruction revealed bottom-to-top with a scan line; overlay stays aligned because both layers share one transform. |
| S06 | 600–719 | S06_BACKGROUND | Cross-fade from S05, three cyan edges converge, logo slot, closing line; holds clean to the end. |

## Missing inputs
- Official XR Universe Studio logo (and any handle/contact line to show on the end card).
- Client sign-off on the English copy.
