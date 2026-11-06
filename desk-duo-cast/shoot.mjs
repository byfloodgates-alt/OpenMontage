// node shoot.mjs <mode> <out.png> [w] [h]  — renders sheet.html?mode=... to a PNG (needs `python3 -m http.server 8765` in this folder)
import { createRequire } from 'module'; const { chromium } = createRequire(import.meta.url)(process.env.NODE_PATH + '/playwright');
const [mode = 'turnaround', out = `${mode}.png`, w = 1920, h = 1080] = process.argv.slice(2);
const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: +w, height: +h } });
p.on('console', (m) => m.type() === 'error' && console.error('page:', m.text()));
p.on('pageerror', (e) => console.error('page error:', e.message));
await p.goto(`http://localhost:8765/sheet.html?mode=${mode}&w=${w}&h=${h}`);
await p.waitForFunction(() => window.__done, null, { timeout: 60000 });
await p.locator('canvas').screenshot({ path: out });
await b.close();
console.log('wrote', out);
