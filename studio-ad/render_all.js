// One command for the whole services film: renders 9:16 and 16:9 in parallel chunks,
// joins the chunks and adds the soundtrack.  Output: out/XR_Universe_Services_*.mp4
//   node render_all.js                 both formats
//   node render_all.js --only v        vertical (Reel) only;  --only h  horizontal only
//   node render_all.js --workers 2     parallel browsers per format (default: half the CPU cores, max 4)
//   node render_all.js --frames 60     quick test with the first 60 frames
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
let FFMPEG = process.env.FFMPEG; if (!FFMPEG) { try { FFMPEG = require('ffmpeg-static'); } catch (e) { FFMPEG = 'ffmpeg'; } }

const D = __dirname, argv = process.argv.slice(2), opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : null; };
const FPS = 30, DUR = 37.4, TOTAL = +(opt('frames') || Math.round(DUR * FPS));
const FMTS = opt('only') ? [opt('only')] : ['v', 'h'];
const WORKERS = Math.max(1, +(opt('workers') || Math.min(4, Math.floor(os.cpus().length / 2))));
const NAMES = { h: 'XR_Universe_Services_1920x1080', v: 'XR_Universe_Services_1080x1920' };

function run(cmd, args, env, tag) {
  return new Promise((ok, fail) => {
    const p = spawn(cmd, args, { cwd: D, env, stdio: ['ignore', 'pipe', 'pipe'] });
    const out = d => String(d).split(/\r?\n/).filter(Boolean).forEach(l => console.log(tag ? `[${tag}] ${l}` : l));
    p.stdout.on('data', out); p.stderr.on('data', out);
    p.on('close', c => c === 0 ? ok() : fail(new Error(`${tag || cmd} exited with ${c}`)));
  });
}

(async () => {
  fs.mkdirSync(path.join(D, 'parts'), { recursive: true }); fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const t0 = Date.now();
  for (const f of FMTS) {
    const step = Math.ceil(TOTAL / WORKERS), chunks = [];
    for (let a = 0; a < TOTAL; a += step) chunks.push([a, Math.min(TOTAL, a + step)]);
    console.log(`\n== ${NAMES[f]}: ${TOTAL} frames, ${chunks.length} workers ==`);
    await Promise.all(chunks.map(([a, b], i) => run(process.execPath, ['render.js', 'video', String(a), String(b)],
      { ...process.env, PAGE: 'ad.html', TAG: 'loc', FMT: f, PORT: String(9100 + (f === 'h' ? 50 : 0) + i) }, `${f}${i + 1}`)));
    const list = path.join(D, 'parts', `loc_list_${f}.txt`);
    fs.writeFileSync(list, chunks.map(([a]) => `file 'loc${f}_${String(a).padStart(4, '0')}.mp4'`).join('\n') + '\n');
    const dst = path.join(D, 'out', `${NAMES[f]}${opt('frames') ? '_test' : ''}.mp4`);
    await run(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-i', path.join(D, 'audio', 'music_ad.wav'),
      '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', dst], process.env, 'ffmpeg');
    console.log(`✓ ${path.relative(D, dst)}`);
  }
  console.log(`\nDone in ${((Date.now() - t0) / 60000).toFixed(1)} min — files are in the out folder.`);
})().catch(e => { console.error('\n✗', e.message); process.exit(1); });
