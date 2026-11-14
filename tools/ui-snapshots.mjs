#!/usr/bin/env node
/* Capture AURA's main screens in every style, light and dark, at phone, tablet and desktop widths.
   Uses an installed Chrome or Edge through the DevTools protocol, so it needs no packages.

   node tools/ui-snapshots.mjs --url http://127.0.0.1:8765/ --business towson-dental --out <folder>
     [--styles modern,classic] [--themes light,dark] [--widths 1440,820,390] [--pages home,files]

   Writes JPEGs plus index.html, a gallery grouped by screen. It only looks: it never sends a message
   or saves a preference (the look is applied in the page for the shot, not stored). */
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, existsSync, mkdtempSync, rmSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const arg = (name, fallback) => { const i = process.argv.indexOf('--' + name); return i > 0 ? process.argv[i + 1] : fallback; };
const list = (name, fallback) => arg(name, fallback).split(',').map(s => s.trim()).filter(Boolean);
const base = arg('url', 'http://127.0.0.1:8765/');
const business = arg('business', '');
const out = resolve(arg('out', 'ui-snapshots'));
const STYLES = { modern: 'forest', classic: 'cm-ink', desktop90: 'd90-navy', console90: 'c90-grey', desktop00: 'd00-blue', console00: 'c00-blue' };
const styles = list('styles', Object.keys(STYLES).join(','));
const themes = list('themes', 'light,dark');
const widths = list('widths', '1440,820,390').map(Number);

/* Each screen: the address to open, then optional steps run in the page before the shot. */
const SCREENS = {
  home: { title: 'Home', view: '' },
  'home-lower': { title: 'Home, scrolled', view: '', run: `const m=document.querySelector('#main');if(m)m.scrollTop=m.scrollHeight;window.scrollTo(0,document.body.scrollHeight);` },
  chat: { title: 'New chat', query: 'new=1' },
  business: { title: 'Knowledge', view: 'business' },
  files: { title: 'Files', view: 'files' },
  collection: { title: 'Collection in the side panel', view: 'files', run: `document.querySelector('.file-card')?.click();`, wait: 1800 },
  library: { title: 'Library', view: 'work' },
  schedules: { title: 'Scheduled tasks', view: 'tools' },
  settings: { title: 'Settings', view: '', run: `document.dispatchEvent(new KeyboardEvent('keydown',{key:',',ctrlKey:true,bubbles:true}));` },
  activity: { title: 'Activity', view: '', run: `document.querySelector('#notification-bell')?.click();` },
  sidebar: { title: 'Sidebar open (phone)', view: '', phoneOnly: true, run: `document.querySelector('#sidebar-open')?.click();` },
};
const pages = list('pages', Object.keys(SCREENS).join(','));

function findBrowser() {
  const candidates = process.platform === 'win32'
    ? ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'C:/Program Files/Microsoft/Edge/Application/msedge.exe']
    : process.platform === 'darwin'
      ? ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']
      : ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge'];
  const found = arg('browser', '') || candidates.find(existsSync);
  if (!found) throw new Error('Chrome or Edge was not found. Pass --browser <path>.');
  return found;
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function main() {
  mkdirSync(out, { recursive: true });
  const profile = mkdtempSync(join(tmpdir(), 'aura-snap-'));
  const port = 9300 + Math.floor(Math.random() * 500);
  const browser = spawn(findBrowser(), ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--no-first-run', '--hide-scrollbars', '--force-color-profile=srgb', 'about:blank'], { stdio: 'ignore' });
  let ws;
  try {
    let version;
    for (let i = 0; i < 50 && !version; i++) { try { version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); } catch { await sleep(200); } }
    if (!version) throw new Error('The browser did not start.');
    ws = new WebSocket(version.webSocketDebuggerUrl);
    await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
    let id = 0; const pending = new Map(); const waiters = [];
    ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.fail(new Error(m.error.message)) : p.ok(m.result); } else if (m.method) waiters.splice(0).forEach(w => w(m)); };
    const send = (method, params = {}, sessionId) => new Promise((ok, fail) => { const n = ++id; pending.set(n, { ok, fail }); ws.send(JSON.stringify({ id: n, method, params, sessionId })); });
    const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
    const page = (method, params) => send(method, params, sessionId);
    await page('Page.enable');
    const evaluate = async expression => (await page('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true })).result?.value;
    const shots = [];
    for (const width of widths) {
      const phone = width < 600, height = phone ? 844 : width < 1000 ? 1100 : 960;
      await page('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: phone });
      await page('Emulation.setTouchEmulationEnabled', { enabled: phone, maxTouchPoints: 5 });
      for (const style of styles) for (const theme of themes) {
        await page('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: theme }] });
        for (const key of pages) {
          const screen = SCREENS[key]; if (!screen || (screen.phoneOnly && !phone)) continue;
          const query = [business && `business=${encodeURIComponent(business)}`, screen.view && `view=${screen.view}`, screen.query].filter(Boolean).join('&');
          await page('Page.navigate', { url: base + (query ? '?' + query : '') });
          await sleep(1600);
          /* Hold the look for this shot only: wrap the app's own appearance functions so background refreshes keep it. */
          await evaluate(`(()=>{const look={style:${JSON.stringify(style)},accent:${JSON.stringify(STYLES[style] || '')},theme:${JSON.stringify(theme)}};
            if(typeof applyProfile==='function'&&!window.__snapProfile){const orig=applyProfile;window.__snapProfile=1;window.applyProfile=p=>orig({...p,style:look.style,accent:look.accent});}
            if(typeof applyAppearance==='function'&&!window.__snapTheme){const orig=applyAppearance;window.__snapTheme=1;window.applyAppearance=()=>orig(look.theme);}
            const r=document.documentElement;r.dataset.style=look.style;r.dataset.accent=look.accent;r.dataset.theme=look.theme;
            document.querySelectorAll('dialog[open]').forEach(d=>{if(d.matches(':modal'))d.close();});})()`);
          if (screen.run) { await evaluate(screen.run); await sleep(screen.wait || 900); } else await sleep(400);
          const { data } = await page('Page.captureScreenshot', { format: 'jpeg', quality: 80 });
          const file = `${key}--${style}-${theme}--${width}.jpg`;
          writeFileSync(join(out, file), Buffer.from(data, 'base64'));
          shots.push({ key, style, theme, width, file });
          process.stdout.write('.');
        }
      }
    }
    writeFileSync(join(out, 'index.html'), gallery(shots));
    console.log(`\n${shots.length} screenshots in ${out}`);
  } finally {
    try { ws?.close(); } catch {}
    browser.kill();
    await sleep(500);
    try { rmSync(profile, { recursive: true, force: true }); } catch {}
  }
}

function gallery(shots) {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const groups = Object.keys(SCREENS).filter(k => shots.some(s => s.key === k));
  const options = (name, values) => `<label>${name} <select data-filter="${name.toLowerCase()}"><option value="">All</option>${values.map(v => `<option>${esc(v)}</option>`).join('')}</select></label>`;
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AURA screens</title>
<style>:root{color-scheme:light dark;--bg:#f6f6f4;--ink:#1d1d1b;--muted:#6b6b66;--card:#fff}@media(prefers-color-scheme:dark){:root{--bg:#161615;--ink:#ecece8;--muted:#9a9a94;--card:#222220}}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}header{position:sticky;top:0;background:var(--bg);padding:16px 24px;border-bottom:1px solid #8883;display:flex;gap:16px;flex-wrap:wrap;align-items:center;z-index:1}
h1{font-size:20px;margin:0 16px 0 0}h2{font-size:17px;margin:32px 24px 12px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;padding:0 24px}
figure{margin:0;background:var(--card);border-radius:10px;overflow:hidden}figure img{width:100%;display:block}figcaption{padding:8px 12px;color:var(--muted);font-size:13px}a{color:inherit}</style></head><body>
<header><h1>AURA screens</h1>${options('Style', [...new Set(shots.map(s => s.style))])}${options('Theme', [...new Set(shots.map(s => s.theme))])}${options('Width', [...new Set(shots.map(s => s.width))])}<span style="color:var(--muted)">Captured ${new Date().toISOString().slice(0, 10)}</span></header>
${groups.map(k => `<section><h2>${esc(SCREENS[k].title)}</h2><div class="grid">${shots.filter(s => s.key === k).map(s => `<figure data-style="${s.style}" data-theme="${s.theme}" data-width="${s.width}"><a href="${esc(s.file)}"><img loading="lazy" src="${esc(s.file)}" alt="${esc(SCREENS[k].title)}, ${s.style} ${s.theme}, ${s.width}px"></a><figcaption>${s.style} · ${s.theme} · ${s.width}px</figcaption></figure>`).join('')}</div></section>`).join('')}
<script>document.querySelectorAll('[data-filter]').forEach(sel=>sel.onchange=()=>{const f={};document.querySelectorAll('[data-filter]').forEach(s=>f[s.dataset.filter]=s.value);document.querySelectorAll('figure').forEach(fig=>{fig.hidden=Object.entries(f).some(([k,v])=>v&&fig.dataset[k]!==v)});document.querySelectorAll('section').forEach(s=>s.hidden=![...s.querySelectorAll('figure')].some(f=>!f.hidden))});</script></body></html>`;
}

main().catch(error => { console.error(error.message || error); process.exit(1); });
