"""Hand-guided depth maps for 2.5D parallax.
Ground plane = vertical gradient below the horizon; the subject is segmented with
OpenCV GrabCut from a measured rectangle and lifted to the depth of its contact line.
Depth is 0 (far) .. 1 (near), stored as 8-bit greyscale PNG at 540x960."""
import sys, os, json
import numpy as np, cv2

SRC = sys.argv[1]; OUT = sys.argv[2]
# name: (horizon_y, [subject rects x0,y0,x1,y1 with contact_y]) in 1080x1920 pixels
SPEC = {
  # phones lying flat sit on the table plane: ground only
  'S01_ALT_A':  (600,  []),
  'S01_MASTER': (600,  []),
  'S01_ALT_B':  (640,  []),
  'S02_CLEAN_PHONE': (1030, [(250, 330, 830, 1480, 1480)]),
  'S02_MASTER': (1030, [(250, 330, 830, 1480, 1480)]),
  'S02_ALT_A':  (1035, [(294, 405, 828, 1500, 1500)]),
  'S02_ALT_B':  (1020, [(234, 345, 846, 1506, 1506)]),
  'S02_PRODUCT_REFERENCE': (1030, [(249, 585, 855, 1374, 1374)]),
  'S04_BEFORE_INTERACTION': (1000, [(140, 432, 500, 1560, 1560), (572, 302, 961, 1600, 1600)]),
  'S04_AFTER_INTERACTION':  (1000, [(140, 432, 500, 1560, 1560), (572, 302, 961, 1600, 1600)]),
  'S04_ALT_A':  (930,  [(180, 570, 456, 1350, 1350), (560, 459, 910, 1240, 1240)]),
}

def ground(h_y, H=1920, W=1080):
    y = np.arange(H, dtype=np.float32)[:, None].repeat(W, 1)
    g = np.where(y < h_y, 0.08 + 0.10 * (y / h_y), 0.18 + 0.82 * ((y - h_y) / (H - h_y)) ** 1.15)
    return g.astype(np.float32)

def segment(img, rect):
    x0, y0, x1, y1 = rect
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, (x0, y0, x1 - x0, y1 - y0), bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype(np.uint8)
    # screens and mirrors are flat displays: fill every hole inside the outer silhouette
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = np.zeros_like(m)
    cv2.drawContours(out, [c for c in cs if cv2.contourArea(c) > 3000], -1, 1, thickness=cv2.FILLED)
    return out

def palmyra(img):
    # sky (blue, bright) far; stone/ground by vertical position; the monument patch nearer
    H, W = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    sky = ((hsv[..., 0] > 90) & (hsv[..., 0] < 130) & (hsv[..., 1] > 30)) | ((hsv[..., 1] < 40) & (hsv[..., 2] > 200))
    sky[1000:] = False
    sky = cv2.morphologyEx(sky.astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(sky)
    sky = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 4000])
    d = ground(980)
    mono = np.zeros((H, W), np.float32); mono[195:1300, 160:600] = 1
    mono = cv2.GaussianBlur(mono, (0, 0), 25)
    d = np.maximum(d, 0.55 * mono + d * (1 - mono))
    d[sky.astype(bool)] = 0.02
    return d

def build(name):
    img = cv2.imread(os.path.join(SRC, name + '.png'))
    if name == 'S05_REAL_WORLD':
        d = palmyra(img)
    else:
        h_y, rects = SPEC[name]
        d = ground(h_y)
        for (x0, y0, x1, y1, cy) in rects:
            m = segment(img, (x0, y0, x1, y1)).astype(np.float32)
            m = cv2.dilate(m, np.ones((15, 15), np.uint8))  # grow so edges move with the subject
            m = cv2.GaussianBlur(m, (0, 0), 4)
            lift = float(ground(h_y)[min(cy, 1919), 540]) + 0.08
            d = np.maximum(d, m * lift)
    d = cv2.GaussianBlur(d, (0, 0), 6)
    d = cv2.resize(d, (540, 960), interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(OUT, name + '.png'), np.clip(d * 255, 0, 255).astype(np.uint8))
    return name

for n in list(SPEC) + ['S05_REAL_WORLD']:
    print('depth', build(n))
