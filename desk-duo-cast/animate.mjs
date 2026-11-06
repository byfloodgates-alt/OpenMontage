// node animate.mjs <voice_out_dir> <out.mp4> [w h]  — renders the lip-synced scene and muxes dialogue.wav
// (needs `python3 -m http.server 8765` running in this folder)
import { createRequire } from 'module';
import { mkdirSync, writeFileSync, rmSync } from 'fs';
import { execFileSync } from 'child_process';
const { chromium } = createRequire(import.meta.url)(process.env.NODE_PATH + '/playwright');
const [dir = 'voice/preview', out = 'preview.mp4', w = 720, h = 1280] = process.argv.slice(2);
const frames = `${dir}/frames`; rmSync(frames, { recursive: true, force: true }); mkdirSync(frames, { recursive: true });
const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: +w, height: +h } });
p.on('pageerror', (e) => console.error('page error:', e.message));
await p.goto(`http://localhost:8765/sheet.html?mode=anim&w=${w}&h=${h}&tl=${dir}/timeline.json`);
await p.waitForFunction(() => window.__done && window.frame, null, { timeout: 60000 });
const n = await p.evaluate(() => window.frameCount);
for (let i = 0; i < n; i++) {
  const data = await p.evaluate((i) => { window.frame(i); return document.querySelector('canvas').toDataURL('image/jpeg', 0.92); }, i);
  writeFileSync(`${frames}/${String(i).padStart(5, '0')}.jpg`, Buffer.from(data.split(',')[1], 'base64'));
  if (i % 60 === 0) console.log(`frame ${i}/${n}`);
}
await b.close();
execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '30', '-i', `${frames}/%05d.jpg`, '-i', `${dir}/dialogue.wav`,
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-shortest', out]);
rmSync(frames, { recursive: true, force: true });
console.log('wrote', out);
