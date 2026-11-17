/* The aura in a real browser: what only layout and the camera can show. Run by workspace_world_browser.py.
   node tests/workspace_world_browser.mjs <browser> <url>
   Checks: the expanded Connections diagram is visible with a long list beside it; following a link to something the
   world does not draw keeps the camera where it was; a still frame costs less than a drawn one; no page errors. */
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const [browserPath, url] = process.argv.slice(2);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const profile = mkdtempSync(join(tmpdir(), 'aura-world-browser-'));
const port = 9300 + Math.floor(Math.random() * 500);
const browser = spawn(browserPath, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--no-first-run', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--window-size=1400,900', 'about:blank'], { stdio: 'ignore' });
let ws, failed = null;
try {
  let version;
  for (let i = 0; i < 75 && !version; i++) { try { version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); } catch { await sleep(200); } }
  if (!version) throw new Error('The browser did not start.');
  ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
  let id = 0; const pending = new Map(), errors = [];
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.fail(new Error(m.error.message)) : p.ok(m.result); } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails?.exception?.description || m.params.exceptionDetails?.text); };
  const send = (method, params = {}, sessionId) => new Promise((ok, fail) => { const n = ++id; pending.set(n, { ok, fail }); ws.send(JSON.stringify({ id: n, method, params, sessionId })); });
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const page = (method, params) => send(method, params, sessionId);
  await page('Runtime.enable'); await page('Page.enable');
  await page('Emulation.setDeviceMetricsOverride', { width: 1400, height: 900, deviceScaleFactor: 1, mobile: false });
  await page('Page.navigate', { url });
  const evaluate = async expression => { const r = await page('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result?.value; };
  const until = async (expression, what, tries = 150) => { for (let i = 0; i < tries; i++) { if (await evaluate(expression).catch(() => false)) return; await sleep(200); } throw new Error('Timed out waiting for ' + what); };
  const check = (ok, message) => { if (!ok) throw new Error(message); };

  await until(`!!document.querySelector('#world-side [data-world-go^="land:"]') && !!window.auraLinks`, 'the aura to open');
  await until(`!!window.auraWorld && (!window.auraWorld.available || !!window.auraWorld.model())`, 'the world renderer to load');
  const has3d = await evaluate(`!!window.auraWorld?.available && !!window.auraWorld.model()`);
  // Select a collection from the list, then open Connections and give the diagram the whole screen.
  await evaluate(`document.querySelector('#world-side [data-world-go^="land:col_"]').click()`);
  await sleep(400);
  await evaluate(`document.querySelector('[data-world-tab="map"]').click()`);
  await evaluate(`document.querySelector('[data-world-expand]').click()`);
  await sleep(600);
  const map = await evaluate(`(()=>{const m=document.querySelector('#world-map'),side=document.querySelector('#world-side');return m?{height:m.getBoundingClientRect().height,lines:m.querySelectorAll('path').length,nodes:m.querySelectorAll('.wm-node').length,overflows:side.scrollHeight>side.clientHeight}:null;})()`);
  check(map && map.nodes > 1, 'the expanded diagram has its nodes: ' + JSON.stringify(map));
  check(map.height > 40, 'the expanded diagram is visible even when the list beside it is long: ' + JSON.stringify(map));
  check(map.lines > 0, 'the expanded diagram draws its lines: ' + JSON.stringify(map));
  await evaluate(`document.querySelector('[data-world-expand]').click()`);
  if (has3d) {
    // Zoom into the collection, then follow a link to a conversation, which the world does not draw.
    await evaluate(`document.querySelector('[data-world-tab="world"]').click()`);
    await evaluate(`window.auraWorld.settle()`);
    const before = await evaluate(`window.auraWorld.cameraState()`);
    await evaluate(`document.querySelector('[data-world-tab="map"]').click()`);
    const chat = await evaluate(`(()=>{const b=document.querySelector('#world-side [data-world-go^="chat:"]');if(b)b.click();return !!b;})()`);
    check(chat, 'the collection lists the conversation that worked on it');
    await sleep(300); await evaluate(`window.auraWorld.settle()`);
    const after = await evaluate(`window.auraWorld.cameraState()`);
    check(Math.abs(after.alt - before.alt) < 1, `following a link keeps the camera close to where it was (altitude ${before.alt.toFixed(2)} → ${after.alt.toFixed(2)})`);
    // With nothing moving, frames are not redrawn (the work saved is on the GPU, so it is counted, not timed).
    await evaluate(`(window.auraWorld.settle(),window.auraWorld.idle(2))`);
    const idle = await evaluate(`(()=>{const w=window.auraWorld,n=w.state().draws;w.idle(10);return w.state().draws-n;})()`);
    check(idle === 0, `a still world is not redrawn (${idle} of 10 still frames were drawn)`);
    const moving = await evaluate(`(()=>{const w=window.auraWorld,n=w.state().draws;w.bench(3);return w.state().draws-n;})()`);
    check(moving === 3, 'a frame that must be drawn is drawn');
  }
  check(!errors.length, 'no page errors: ' + errors.join(' | '));
  console.log('world browser: ok' + (has3d ? '' : ' (3D unavailable here; layout checked)'));
} catch (error) { failed = error; }
finally { try { ws?.close(); } catch {} browser.kill(); await sleep(300); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
if (failed) { console.error('world browser: ' + failed.message); process.exit(1); }
