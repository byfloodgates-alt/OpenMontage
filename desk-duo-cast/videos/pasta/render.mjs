// node render.mjs still <t1,t2,...>   -> stills/t_<t>.png  (quick checks)
// node render.mjs video               -> frames/ then out/video.mp4 (1080x1920, 30 fps)
// needs a static server on :8766 rooted at /home/user
import { createRequire } from 'module';
import { mkdirSync, writeFileSync, rmSync } from 'fs';
const { chromium } = createRequire(import.meta.url)(process.env.NODE_PATH + '/playwright');
const [mode = 'still', arg = '1'] = process.argv.slice(2);
const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: 720, height: 1280 }, deviceScaleFactor: 1.5 });
p.on('pageerror', (e) => console.error('page error:', e.message));
p.on('console', (m) => m.type() === 'error' && console.error('page:', m.text()));
await p.goto('http://localhost:8766/pasta/index.html');
await p.waitForFunction(() => window.__done, null, { timeout: 60000 });
if (mode === 'still') {
  mkdirSync('stills', { recursive: true });
  for (const t of arg.split(',').map(Number)) {
    await p.evaluate((i) => window.frame(i), Math.round(t * 30));
    await p.screenshot({ path: `stills/t_${t}.png` });
  }
} else {
  rmSync('frames', { recursive: true, force: true }); mkdirSync('frames', { recursive: true });
  const n = await p.evaluate(() => window.frameCount);
  for (let i = 0; i < n; i++) {
    await p.evaluate((i) => window.frame(i), i);
    writeFileSync(`frames/${String(i).padStart(5, '0')}.jpg`, await p.screenshot({ type: 'jpeg', quality: 93 }));
    if (i % 90 === 0) console.log(`frame ${i}/${n}`);
  }
}
await b.close();
