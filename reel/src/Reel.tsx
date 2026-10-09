import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  Sequence,
  continueRender,
  delayRender,
  interpolate,
  staticFile,
  useCurrentFrame,
} from 'remotion';

/* ------------------------------------------------------------------
   XR Universe Studio — "Beyond the Ordinary" hybrid reel
   24 s · 1080×1920 · 30 fps. Every move is a pure function of frame.
   Coordinates are measured on the 1080×1920 Phase 01 masters.
------------------------------------------------------------------- */

export const FPS = 30;
export const W = 1080;
export const H = 1920;
export const DURATION = 720;

const C = {
  midnight: '#080C12',
  graphite: '#17212D',
  cyan: '#54D8F2',
  ice: '#E9F1F6',
};

const A = (f: string) => staticFile(`assets/${f}.png`);

/* scene boundaries (frames) */
const S = {
  s01: [0, 90],
  s02: [90, 240],
  s03: [240, 300],
  s04: [300, 450],
  s05: [450, 600],
  s06: [600, 720],
} as const;

/* measured anchors */
const S01_SCREEN = {x: 535, y: 990};
const S02_EDIT = {l: 316, t: 689, r: 783, b: 1315}; // product patch (MASTER vs CLEAN differ only here)
const S02_PRODUCT = {x: 557, y: 950}; // product centre
const S02_FLOOR = {x: 557, y: 1236}; // product contact point inside the screen
const S03_SPEAKER = {l: 227, t: 480, r: 713, b: 1365, dx: 162, dy: -18};
const S03_DISPLAY = {l: 302, t: 238, r: 821, b: 1490, dx: 54, dy: -20};
const S03_SPEAKER_C = {x: 551, y: 922};
const S04_MIRROR = {l: 572, t: 302, r: 961, b: 1587};
const S04_DOT = {x: 611, y: 594}; // selectable element (BEFORE vs AFTER differ only here)
const S05_PATCH = {l: 175, t: 195, r: 564, b: 1225};

const ease = Easing.bezier(0.45, 0, 0.2, 1);
const out = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = (f: number, a: number, b: number, from = 0, to = 1, e = ease) =>
  interpolate(f, [a, b], [from, to], {...clamp, easing: e});
const lerp = (a: number, b: number, k: number) => a + (b - a) * k;

/* ------------------------------ fonts ------------------------------ */
const useFonts = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const faces = [
      new FontFace('Sora', `url(${staticFile('fonts/Sora-Regular.ttf')})`, {weight: '400'}),
      new FontFace('Sora', `url(${staticFile('fonts/Sora-SemiBold.ttf')})`, {weight: '600'}),
    ];
    Promise.all(faces.map((f) => f.load()))
      .then((loaded) => {
        loaded.forEach((f) => document.fonts.add(f));
        continueRender(handle);
      })
      .catch(() => continueRender(handle));
  }, [handle]);
};

/* --------------------------- primitives ---------------------------- */
const Plate: React.FC<{src: string; style?: React.CSSProperties}> = ({src, style}) => (
  <Img src={src} style={{position: 'absolute', left: 0, top: 0, width: W, height: H, ...style}} />
);

/* camera move expressed as scale about a pivot plus a pivot shift */
const cam = (scale: number, px: number, py: number, tx = px, ty = py): React.CSSProperties => ({
  position: 'absolute',
  inset: 0,
  transformOrigin: '0 0',
  transform: `translate(${tx}px, ${ty}px) scale(${scale}) translate(${-px}px, ${-py}px)`,
});

const Vignette: React.FC<{strength?: number}> = ({strength = 0.55}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse 75% 60% at 50% 50%, rgba(8,12,18,0) 55%, rgba(8,12,18,${strength}) 100%)`,
    }}
  />
);

/* headline: words rise in sequence, then fade together */
const Headline: React.FC<{
  text: string;
  start: number;
  end: number;
  y?: number;
  size?: number;
  scrim?: boolean;
}> = ({text, start, end, y = 236, size = 58, scrim}) => {
  const f = useCurrentFrame();
  const words = text.split(' ');
  const exit = io(f, end - 10, end, 1, 0);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {scrim ? (
        <AbsoluteFill
          style={{
            opacity: io(f, start - 6, start + 6) * exit,
            background: 'linear-gradient(180deg, rgba(8,12,18,.78) 0%, rgba(8,12,18,.42) 26%, rgba(8,12,18,0) 42%)',
          }}
        />
      ) : null}
      <div
        style={{
          position: 'absolute',
          top: y,
          left: 110,
          right: 110,
          textAlign: 'center',
          fontFamily: 'Sora, sans-serif',
          fontWeight: 600,
          fontSize: size,
          lineHeight: 1.16,
          letterSpacing: -0.6,
          color: C.ice,
          opacity: exit,
          textShadow: '0 2px 24px rgba(8,12,18,.55)',
        }}
      >
        {words.map((w, i) => {
          const k = io(f, start + i * 3, start + i * 3 + 14, 0, 1, out);
          return (
            <span
              key={i}
              style={{
                display: 'inline-block',
                opacity: k,
                transform: `translateY(${(1 - k) * 26}px)`,
                marginRight: i < words.length - 1 ? '0.26em' : 0,
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
      <div
        style={{
          position: 'absolute',
          top: y - 34,
          left: W / 2 - 36,
          width: 72,
          height: 3,
          background: C.cyan,
          opacity: exit,
          transform: `scaleX(${io(f, start, start + 16, 0, 1, out)})`,
        }}
      />
    </AbsoluteFill>
  );
};

/* ------------------------------ S01 ------------------------------- */
const S01: React.FC<{f: number}> = ({f}) => {
  // slow 4% push-in toward the phone, then light gathers in the screen
  const s = lerp(1.0, 1.04, io(f, 0, 90, 0, 1, Easing.linear));
  const glow = io(f, 66, 90);
  return (
    <AbsoluteFill>
      <div style={cam(s, S01_SCREEN.x, S01_SCREEN.y)}>
        <Plate src={A('S01_MASTER')} />
      </div>
      <AbsoluteFill
        style={{
          opacity: glow,
          background: `radial-gradient(circle at ${S01_SCREEN.x}px ${S01_SCREEN.y}px, rgba(233,241,246,.95) 0px, rgba(84,216,242,.55) ${lerp(40, 520, glow)}px, rgba(8,12,18,0) ${lerp(200, 1100, glow)}px)`,
          mixBlendMode: 'screen',
        }}
      />
    </AbsoluteFill>
  );
};

/* ------------------------------ S02 ------------------------------- */
const S02: React.FC<{f: number}> = ({f}) => {
  const u = f - S.s02[0];
  // light settles back into the screen
  const flash = io(u, 0, 14, 1, 0);
  // gentle push toward the phone, then the match-cut move onto the product
  const push = lerp(1.02, 1.06, io(u, 0, 130));
  const k = io(u, 128, 150, 0, 1, Easing.bezier(0.6, 0, 0.9, 0.4));
  const scale = lerp(1, 2.15 / push, k);
  const tx = lerp(S02_PRODUCT.x, S03_SPEAKER_C.x, k);
  const ty = lerp(S02_PRODUCT.y, S03_SPEAKER_C.y, k);
  // placement reticle, then a top-to-bottom reveal of the product patch
  const ret = io(u, 12, 24) * io(u, 44, 52, 1, 0);
  const reveal = io(u, 34, 56);
  const scanY = lerp(S02_EDIT.t, S02_EDIT.b, reveal);
  return (
    <AbsoluteFill>
      <div style={cam(scale, S02_PRODUCT.x, S02_PRODUCT.y, tx, ty)}>
      <div style={cam(push, S02_PRODUCT.x, 0)}>
        <Plate src={A('S02_CLEAN_PHONE')} />
        <Plate
          src={A('S02_MASTER')}
          style={{
            clipPath: `polygon(${S02_EDIT.l}px ${S02_EDIT.t}px, ${S02_EDIT.r}px ${S02_EDIT.t}px, ${S02_EDIT.r}px ${scanY}px, ${S02_EDIT.l}px ${scanY}px)`,
          }}
        />
        {reveal > 0 && reveal < 1 ? (
          <div
            style={{
              position: 'absolute',
              left: S02_EDIT.l + 20,
              width: S02_EDIT.r - S02_EDIT.l - 40,
              top: scanY - 1,
              height: 2,
              background: C.cyan,
              boxShadow: `0 0 18px 4px ${C.cyan}`,
              opacity: 0.9,
            }}
          />
        ) : null}
        <svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity: ret}}>
          <ellipse
            cx={S02_FLOOR.x}
            cy={S02_FLOOR.y}
            rx={lerp(150, 120, io(u, 12, 30))}
            ry={lerp(30, 24, io(u, 12, 30))}
            fill="none"
            stroke={C.cyan}
            strokeWidth={3}
          />
          <ellipse cx={S02_FLOOR.x} cy={S02_FLOOR.y} rx={10} ry={3} fill={C.cyan} />
        </svg>
      </div>
      </div>
      <AbsoluteFill style={{background: 'rgba(233,241,246,1)', opacity: flash * 0.6, mixBlendMode: 'screen'}} />
    </AbsoluteFill>
  );
};

/* ------------------------------ S03 ------------------------------- */
type Box = {l: number; t: number; r: number; b: number; dx: number; dy: number};
const mixBox = (a: Box, b: Box, k: number): Box => ({
  l: lerp(a.l, b.l, k),
  t: lerp(a.t, b.t, k),
  r: lerp(a.r, b.r, k),
  b: lerp(a.b, b.b, k),
  dx: lerp(a.dx, b.dx, k),
  dy: lerp(a.dy, b.dy, k),
});

const WireBox: React.FC<{box: Box; opacity: number; rows?: number; cols?: number}> = ({box, opacity, rows = 6, cols = 4}) => {
  const {l, t, r, b, dx, dy} = box;
  const lines: React.ReactNode[] = [];
  for (let i = 1; i < cols; i++) {
    const x = lerp(l, r, i / cols);
    lines.push(<line key={`c${i}`} x1={x} y1={t} x2={x} y2={b} />);
  }
  for (let i = 1; i < rows; i++) {
    const y = lerp(t, b, i / rows);
    lines.push(<line key={`r${i}`} x1={l} y1={y} x2={r} y2={y} />);
    lines.push(<line key={`s${i}`} x1={r} y1={y} x2={r + dx} y2={y + dy} />);
  }
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity}}>
      <g stroke={C.cyan} fill="none" strokeLinecap="round" style={{filter: `drop-shadow(0 0 6px ${C.cyan})`}}>
        <g strokeWidth={1.2} opacity={0.45}>{lines}</g>
        <g strokeWidth={3}>
          <rect x={l} y={t} width={r - l} height={b - t} rx={18} />
          <polyline points={`${l},${t} ${l + dx},${t + dy} ${r + dx},${t + dy} ${r + dx},${b + dy} ${r},${b}`} />
          <line x1={r} y1={t} x2={r + dx} y2={t + dy} />
        </g>
      </g>
    </svg>
  );
};

const S03: React.FC<{f: number}> = ({f}) => {
  const u = f - S.s03[0];
  const startOp = io(u, 6, 18, 1, 0.12);
  const endOp = io(u, 38, 56);
  const k = io(u, 8, 46);
  const wireOp = io(u, 0, 8) * io(u, 50, 58, 1, 0);
  const drift = lerp(1.0, 1.03, io(u, 0, 60, 0, 1, Easing.linear));
  return (
    <AbsoluteFill style={{background: C.midnight}}>
      <div style={cam(drift, W / 2, H / 2)}>
        <Plate src={A('S03_WIREFRAME_START')} style={{opacity: startOp * (1 - endOp)}} />
        <Plate src={A('S03_WIREFRAME_END')} style={{opacity: endOp}} />
        <WireBox box={mixBox(S03_SPEAKER, S03_DISPLAY, k)} opacity={wireOp} rows={Math.round(lerp(6, 9, k))} cols={Math.round(lerp(4, 3, k))} />
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------ S04 ------------------------------- */
const S04: React.FC<{f: number}> = ({f}) => {
  const u = f - S.s04[0];
  // land: the display outline from S03 resolves into the mirror, camera pulls back to the full scene
  const land = io(u, 0, 40);
  const mirC = {x: (S04_MIRROR.l + S04_MIRROR.r) / 2, y: (S04_MIRROR.t + S04_MIRROR.b) / 2};
  let scale = lerp(1.32, 1.0, land);
  // start nearer the S03 display position; values keep every frame edge covered at 1.32x
  let tx = lerp(680, mirC.x, land);
  let ty = lerp(860, mirC.y, land);
  scale *= lerp(1.0, 1.035, io(u, 40, 130, 0, 1, Easing.linear));
  // exit: the selected element grows to fill the frame
  const exit = io(u, 128, 150, 0, 1, Easing.bezier(0.7, 0, 0.95, 0.5));
  const px = lerp(mirC.x, S04_DOT.x, exit);
  const py = lerp(mirC.y, S04_DOT.y, exit);
  scale *= lerp(1, 9, exit);
  tx = lerp(tx, W / 2, exit);
  ty = lerp(ty, H / 2, exit);

  const SEL = 78; // selection frame (12.6 s)
  const selected = u >= SEL;
  const pre = io(u, SEL - 14, SEL, 0, 1) * (selected ? 0 : 1);
  const ripple = io(u, SEL, SEL + 22, 0, 1, out);
  const outline = io(u, 0, 10) * io(u, 28, 44, 1, 0);
  const fill = io(u, 136, 150);
  return (
    <AbsoluteFill style={{background: C.midnight}}>
      <div style={cam(scale, exit > 0 ? px : mirC.x, exit > 0 ? py : mirC.y, tx, ty)}>
        <Plate src={A('S04_BEFORE_INTERACTION')} />
        <Plate src={A('S04_AFTER_INTERACTION')} style={{opacity: selected ? 1 : 0}} />
        <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
          {pre > 0 ? (
            <circle cx={S04_DOT.x} cy={S04_DOT.y} r={lerp(34, 24, pre)} fill="none" stroke={C.cyan} strokeWidth={2.5} opacity={pre} />
          ) : null}
          {selected && ripple < 1 ? (
            <>
              <circle cx={S04_DOT.x} cy={S04_DOT.y} r={lerp(26, 90, ripple)} fill="none" stroke={C.cyan} strokeWidth={3} opacity={1 - ripple} />
              <circle cx={S04_DOT.x} cy={S04_DOT.y} r={lerp(20, 30, ripple)} fill={C.cyan} opacity={(1 - ripple) * 0.45} />
            </>
          ) : null}
          {outline > 0 ? (
            <rect
              x={S04_MIRROR.l}
              y={S04_MIRROR.t}
              width={S04_MIRROR.r - S04_MIRROR.l}
              height={S04_MIRROR.b - S04_MIRROR.t}
              rx={10}
              fill="none"
              stroke={C.cyan}
              strokeWidth={3 / scale}
              opacity={outline}
              style={{filter: `drop-shadow(0 0 6px ${C.cyan})`}}
            />
          ) : null}
        </svg>
      </div>
      <AbsoluteFill style={{background: C.cyan, opacity: fill * 0.9}} />
      <AbsoluteFill style={{background: C.ice, opacity: io(u, 144, 150) * 0.6}} />
    </AbsoluteFill>
  );
};

/* ------------------------------ S05 ------------------------------- */
const S05: React.FC<{f: number}> = ({f}) => {
  const u = f - S.s05[0];
  const fromLight = io(u, 0, 16, 1, 0);
  const push = lerp(1.0, 1.05, io(u, 0, 150, 0, 1, Easing.linear));
  // reconstruction rises from the column bases to the entablature
  const rev = io(u, 34, 84);
  const scanY = lerp(S05_PATCH.b, S05_PATCH.t, rev);
  const settle = io(u, 84, 100, 1, 0.92);
  const toBrand = io(u, 132, 166, 0, 0.55);
  return (
    <AbsoluteFill style={{background: C.midnight}}>
      <div style={cam(push, 370, 900)}>
        <Plate src={A('S05_REAL_WORLD')} />
        <Plate
          src={A('S05_OVERLAY_ISOLATED_RGBA')}
          style={{
            clipPath: `polygon(0px ${scanY}px, ${W}px ${scanY}px, ${W}px ${H}px, 0px ${H}px)`,
            opacity: settle * (1 - toBrand * 0.6),
            filter: `drop-shadow(0 0 4px rgba(84,216,242,.95)) drop-shadow(0 0 14px rgba(84,216,242,.6))`,
          }}
        />
        {rev > 0 && rev < 1 ? (
          <div
            style={{
              position: 'absolute',
              left: S05_PATCH.l - 20,
              width: S05_PATCH.r - S05_PATCH.l + 40,
              top: scanY - 1,
              height: 2,
              background: C.cyan,
              boxShadow: `0 0 16px 3px ${C.cyan}`,
            }}
          />
        ) : null}
      </div>
      <AbsoluteFill style={{background: C.ice, opacity: fromLight * 0.7}} />
      <AbsoluteFill style={{background: C.midnight, opacity: toBrand}} />
    </AbsoluteFill>
  );
};

/* ------------------------------ S06 ------------------------------- */
const LogoSlot: React.FC<{f: number; logo?: string}> = ({f, logo}) => {
  const k = io(f, 630, 654, 0, 1, out);
  const box = {w: 520, h: 260, y: 760};
  if (logo) {
    return (
      <Img
        src={logo}
        style={{position: 'absolute', left: W / 2 - box.w / 2, top: box.y, width: box.w, height: box.h, objectFit: 'contain', opacity: k, transform: `scale(${lerp(0.94, 1, k)})`}}
      />
    );
  }
  // review cut: replaceable slot, deliberately not a brand mark
  return (
    <div
      style={{
        position: 'absolute',
        left: W / 2 - box.w / 2,
        top: box.y,
        width: box.w,
        height: box.h,
        border: `2px dashed rgba(233,241,246,.45)`,
        borderRadius: 18,
        opacity: k,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'Sora, sans-serif',
        fontSize: 22,
        letterSpacing: 4,
        color: 'rgba(233,241,246,.55)',
      }}
    >
      OFFICIAL LOGO
    </div>
  );
};

const S06: React.FC<{f: number; logo?: string}> = ({f, logo}) => {
  const u = f - S.s06[0];
  const inK = io(u, 0, 16);
  const breathe = 0.5 + 0.5 * Math.sin((u / FPS) * Math.PI * 0.9);
  const conv = io(u, 6, 34, 0, 1, out);
  const lineOp = io(u, 6, 14) * io(u, 40, 56, 1, 0.25);
  const cx = W / 2;
  const cy = 890;
  return (
    <AbsoluteFill style={{opacity: inK}}>
      <Plate src={A('S06_BACKGROUND')} />
      <AbsoluteFill
        style={{
          opacity: inK * (0.25 + 0.2 * breathe),
          background: `radial-gradient(ellipse 50% 22% at 50% 46%, rgba(84,216,242,.22), rgba(84,216,242,0) 70%)`,
        }}
      />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity: lineOp}}>
        <g stroke={C.cyan} strokeWidth={2} style={{filter: `drop-shadow(0 0 6px ${C.cyan})`}}>
          <line x1={lerp(0, cx - 300, conv)} y1={lerp(1500, cy, conv)} x2={lerp(120, cx - 280, conv)} y2={lerp(1700, cy + 24, conv)} />
          <line x1={lerp(W, cx + 300, conv)} y1={lerp(1500, cy, conv)} x2={lerp(W - 120, cx + 280, conv)} y2={lerp(1700, cy + 24, conv)} />
          <line x1={lerp(cx, cx - 260, conv)} y1={lerp(1880, cy + 160, conv)} x2={lerp(cx, cx + 260, conv)} y2={lerp(1880, cy + 160, conv)} />
        </g>
      </svg>
      <LogoSlot f={f} logo={logo} />
    </AbsoluteFill>
  );
};

/* ------------------------------ reel ------------------------------ */
export type ReelProps = {showText: boolean; withAudio: boolean; logo?: string};

export const Reel: React.FC<ReelProps> = ({showText, withAudio, logo}) => {
  useFonts();
  const f = useCurrentFrame();
  const scene = f < S.s02[0] ? 1 : f < S.s03[0] ? 2 : f < S.s04[0] ? 3 : f < S.s05[0] ? 4 : f < S.s06[0] ? 5 : 6;
  return (
    <AbsoluteFill style={{background: C.midnight}}>
      {scene === 1 && <S01 f={f} />}
      {scene === 2 && <S02 f={f} />}
      {scene === 3 && <S03 f={f} />}
      {scene === 4 && <S04 f={f} />}
      {scene === 5 && <S05 f={f} />}
      {scene === 6 && f < S.s06[0] + 16 && <S05 f={f} />}
      {scene === 6 && <S06 f={f} logo={logo} />}
      <Vignette strength={scene === 5 ? 0.35 : 0.55} />
      {showText ? (
        <>
          <Headline text="What if reality could do more?" start={8} end={80} />
          <Headline text="Products you can explore." start={118} end={226} />
          <Headline text="Experiences you can control." start={330} end={430} />
          <Headline text="Stories you can experience." start={476} end={588} scrim />
          <Headline text="We create interactive realities." start={650} end={730} y={1110} size={58} />
        </>
      ) : null}
      {withAudio ? (
        <Sequence from={0}>
          <Audio src={staticFile('audio/reel_audio.wav')} />
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
