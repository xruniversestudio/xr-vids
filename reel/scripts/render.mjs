// Bundle once, then render stills or the full reel.
// usage: node scripts/render.mjs stills <outDir> <frame...>
//        node scripts/render.mjs video <compositionId> <out.mp4> [--muted]
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

const [mode, a, b, ...rest] = process.argv.slice(2);
const browserExecutable = process.env.REMOTION_BROWSER || null;
const chromiumOptions = {gl: 'swiftshader'};
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});

if (mode === 'stills') {
  fs.mkdirSync(a, {recursive: true});
  const composition = await selectComposition({serveUrl, id: 'Reel', browserExecutable, chromiumOptions});
  for (const fr of [b, ...rest].map(Number)) {
    await renderStill({composition, serveUrl, output: path.join(a, `f${String(fr).padStart(3, '0')}.jpg`), frame: fr, imageFormat: 'jpeg', jpegQuality: 92, browserExecutable, chromiumOptions});
  }
} else {
  const composition = await selectComposition({serveUrl, id: a, browserExecutable, chromiumOptions});
  await renderMedia({
    composition, serveUrl, codec: 'h264', outputLocation: b, browserExecutable, chromiumOptions,
    imageFormat: 'jpeg', jpegQuality: 95, crf: 16, pixelFormat: 'yuv420p', audioCodec: 'aac', audioBitrate: '192k',
    muted: rest.includes('--muted'), concurrency: 3,
    onProgress: ({progress}) => { const p = Math.round(progress * 100); if (p % 10 === 0) process.stdout.write(`\r${p}%  `); },
  });
  console.log('\nwrote', b);
}
