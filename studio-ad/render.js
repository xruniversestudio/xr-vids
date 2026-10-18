// Headless render of $PAGE (default index.html; TAG prefixes output names) → JPEG frames piped to ffmpeg.
// node render.js stills <t...>            → stills/s_<t>.png
// node render.js video <from> <to>       → parts/part_<from>.mp4 (frame range, 30 fps)
// Playwright: local install first (npm install), then the global one this cloud setup uses
let chromium; try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
// ffmpeg: FFMPEG env, else the bundled ffmpeg-static binary (npm install), else ffmpeg on PATH
let FFMPEG = process.env.FFMPEG; if (!FFMPEG) { try { FFMPEG = require('ffmpeg-static'); } catch (e) { FFMPEG = 'ffmpeg'; } }
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path'), http = require('http');
const D = __dirname, mode = process.argv[2], PORT = +(process.env.PORT || 8801), FMT = process.env.FMT || 'h', VW = FMT === 'v' ? 1080 : 1920, VH = FMT === 'v' ? 1920 : 1080;
const PAGE = process.env.PAGE || 'index.html', TAG = process.env.TAG || '';
const html = '<!doctype html><html lang="ar"><head><meta charset="utf-8"></head><body>' + fs.readFileSync(path.join(D, PAGE), 'utf8').replaceAll('THREE_BASE', '/node_modules/three') + '</body></html>';
fs.writeFileSync(path.join(D, `_wrap_${TAG}${FMT}_${PORT}.html`), html);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.png': 'image/png', '.svg': 'image/svg+xml', '.glb': 'model/gltf-binary', '.json': 'application/json', '.jpg': 'image/jpeg' };
const srv = http.createServer((q, r) => { const f = path.join(D, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, b) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(b); }); }).listen(PORT);
(async () => {
    // GPU by default (fast on a laptop); SWIFTSHADER=1 forces the software renderer (servers without a GPU)
  const args = process.env.SWIFTSHADER === '1' ? ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] : ['--ignore-gpu-blocklist', '--enable-gpu', '--enable-webgl'];
  const b = await chromium.launch({ args });
  const p = await b.newPage({ viewport: { width: VW, height: VH } });
  p.on('pageerror', e => console.log('ERR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  const logo = process.env.LOGO ? '&logo=' + encodeURIComponent(process.env.LOGO) : '';
  await p.goto(`http://localhost:${PORT}/_wrap_${TAG}${FMT}_${PORT}.html?fmt=${FMT}${logo}`);
  await p.waitForFunction(() => window.READY === true, null, { timeout: 120000 });
  const cvs = await p.$('canvas'), t0 = Date.now();
  if (mode === 'stills') {
    fs.mkdirSync(path.join(D, 'stills'), { recursive: true });
    const ts = process.argv.slice(3).map(Number);
    for (const t of ts) { await p.evaluate(t => renderAt(t), t); await cvs.screenshot({ path: path.join(D, 'stills', `${TAG}${FMT}_${t}.png`) }); }
    console.log('ms/frame', Math.round((Date.now() - t0) / ts.length));
  } else {
    fs.mkdirSync(path.join(D, 'parts'), { recursive: true });
    const a = +process.argv[3], z = +process.argv[4];
    const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'medium', path.join(D, 'parts', `${TAG}${FMT}_${String(a).padStart(4, '0')}.mp4`)], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = a; i < z; i++) {
      await p.evaluate(t => renderAt(t), i / 30);
      const buf = await cvs.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if ((i - a) % 30 === 0) console.log('frame', i, Math.round((Date.now() - t0) / (i - a + 1)), 'ms/f');
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log('done', a, z);
  }
  await b.close(); srv.close();
})();
