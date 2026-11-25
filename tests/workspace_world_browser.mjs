/* The aura in a real browser: what only layout and the camera can show. Run by workspace_world_browser.py.
   node tests/workspace_world_browser.mjs <browser> <url>
   Checks: the expanded Connections diagram is visible with a long list beside it; following a link to something the
   world does not draw keeps the camera where it was; a still frame costs less than a drawn one; no page errors. */
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const [browserPath, url] = process.argv.slice(2);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const profile = mkdtempSync(join(tmpdir(), 'aura-world-browser-'));
const browser = spawn(browserPath, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--window-size=1400,900', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
let launchError, stderr = '';
browser.on('error', error => { launchError = error; });
browser.stderr.setEncoding('utf8').on('data', chunk => { stderr = (stderr + chunk).slice(-1500); });
let ws, failed = null;
try {
  let version;
  for (let i = 0; i < 125 && !version; i++) {
    if (launchError || browser.exitCode !== null) break;
    try {
      const [port] = readFileSync(join(profile, 'DevToolsActivePort'), 'utf8').trim().split(/\r?\n/);
      if (!/^\d+$/.test(port)) throw new Error('Waiting for the browser debug port.');
      const response = await fetch(`http://127.0.0.1:${port}/json/version`, {signal: AbortSignal.timeout(1000)});
      const info = await response.json();
      if (info.webSocketDebuggerUrl) version = info;
    } catch {}
    if (!version) await sleep(200);
  }
  if (!version) throw new Error('The browser did not start. ' + (launchError?.message || stderr.trim() || 'No debug port was reported.'));
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
  await page('Page.bringToFront');
  await page('Page.navigate', { url });
  const evaluate = async expression => { const r = await page('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result?.value; };
  const until = async (expression, what, tries = 150) => { for (let i = 0; i < tries; i++) { if (await evaluate(expression).catch(() => false)) return; await sleep(200); } throw new Error('Timed out waiting for ' + what); };
  const check = (ok, message) => { if (!ok) throw new Error(message); };

  await until(`!!document.querySelector('#world-side [data-world-go^="land:"]') && !!window.auraLinks`, 'the aura to open');
  await until(`!!window.auraWorld && (!window.auraWorld.available || !!window.auraWorld.model())`, 'the world renderer to load');
  const has3d = await evaluate(`!!window.auraWorld?.available && !!window.auraWorld.model()`);
  // Select a collection from the list, then open Connections: the diagram takes the stage and the world goes small.
  await evaluate(`document.querySelector('#world-side [data-world-go^="land:col_"]').click()`);
  await evaluate(`document.querySelector('[data-world-tab="map"]').click()`);
  await until(`!!document.querySelector('#world-map .ln')`, 'Connections to draw its lines');
  const map = await evaluate(`(()=>{const m=document.querySelector('#world-lens #world-map'),side=document.querySelector('#world-side'),stage=document.querySelector('#world-stage').getBoundingClientRect();return m?{height:m.getBoundingClientRect().height,lines:m.querySelectorAll('.ln').length,nodes:m.querySelectorAll('.wm-node').length,side:!!side.querySelector('h2'),mini:stage.width<260}:null;})()`);
  check(map && map.nodes > 1, 'the diagram on the stage has its nodes: ' + JSON.stringify(map));
  check(map.height > 40 && map.side, 'the diagram is visible with its list beside it: ' + JSON.stringify(map));
  check(map.lines > 0, 'the diagram draws its lines: ' + JSON.stringify(map));
  check(map.mini, 'the world keeps going small in the corner: ' + JSON.stringify(map));
  // Pointing at a box traces its chain in the diagram, as the prototype's Map did.
  const traced = await evaluate(`(()=>{const n=document.querySelector('#world-map .wm-node[data-world-go^="task:"]')||document.querySelector('#world-map .wm-node[data-world-go^="app:"]');n.dispatchEvent(new PointerEvent('pointerover',{bubbles:true}));const d=document.querySelectorAll('#world-map .world-dim').length;n.dispatchEvent(new PointerEvent('pointerout',{bubbles:true,relatedTarget:document.body}));return {dimmed:d,after:document.querySelectorAll('#world-map .world-dim').length};})()`);
  check(traced.dimmed > 0 && traced.after === 0, 'pointing at a box traces its chain and lets go after: ' + JSON.stringify(traced));
  // Time and AI effort take the stage too.
  await evaluate(`document.querySelector('[data-world-tab="timeline"]').click()`);
  await until(`!!document.querySelector('#world-lens .tl-today') && document.querySelectorAll('#world-lens .tl-lane').length>0`, 'Time to draw its rows with today on the stage');
  await evaluate(`document.querySelector('[data-world-tab="effort"]').click()`);
  await until(`!document.querySelector('#world-lens').hidden && !!document.querySelector('#world-lens .we-stage, #world-lens .tl-empty')`, 'AI effort to take the stage');
  // The side panel can be made wider from its edge, with the keyboard as well as by dragging.
  const widths = await evaluate(`(()=>{const g=document.querySelector('#world-grip'),side=document.querySelector('#world-side'),a=side.getBoundingClientRect().width;g.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));const b=side.getBoundingClientRect().width;localStorage.removeItem('aura-world-side-width');return [a,b];})()`);
  check(widths[1] > widths[0], 'the side panel widens from its edge: ' + JSON.stringify(widths));
  if (has3d) {
    // An AI app in the sky beside the world opens its connections when clicked.
    await evaluate(`document.querySelector('[data-world-tab="world"]').click()`); await sleep(300);
    // Satellites orbit above the places their work reached, so turn the world to face the app first.
    await evaluate(`(()=>{const w=window.auraWorld,a=w.model().actors.find(x=>x.kind==='app');const d=a.dir;w.restoreCamera({lon:Math.atan2(d.x,d.z),lat:Math.asin(d.y),alt:5.2});w.settle();w.idle(2);return true;})()`); await sleep(300);
    const spot = await evaluate(`(()=>{const r=document.querySelector('#world-stage canvas.world-ui').getBoundingClientRect(),d=window.auraWorld.state().dock[0];return d&&{x:r.left+d.x,y:r.top+d.y};})()`);
    check(spot, 'the sky shows the AI app');
    for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) await page('Input.dispatchMouseEvent', { type, x: spot.x, y: spot.y, button: 'left', clickCount: 1 });
    await sleep(500);
    const opened = await evaluate(`document.querySelector('#world-side .kind')?.textContent+' · '+document.querySelector('#world-side h2')?.textContent`);
    check(/AI app · Sample app/.test(opened), 'an AI app in the sky opens its connections: ' + opened);
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
