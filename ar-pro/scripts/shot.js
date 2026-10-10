const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path'), http = require('http');
const D = path.resolve(__dirname, '..'), page = process.argv[2], out = process.argv[3];
const types = { '.html': 'text/html', '.js': 'text/javascript' };
const srv = http.createServer((q, r) => { const f = path.join(D, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, b) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(b); }); }).listen(8501);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1500, height: 1000 } });
  p.on('pageerror', e => console.log('ERR', e.message)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log(m.type(), m.text().slice(0, 200)); });
  await p.goto('http://localhost:8501/' + page); await p.waitForFunction(() => window.READY, null, { timeout: 300000 });
  console.log(JSON.stringify(await p.evaluate(() => window.INFO), null, 0));
  await (await p.$('canvas')).screenshot({ path: out }); await b.close(); srv.close();
})();
