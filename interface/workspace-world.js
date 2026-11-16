/* Your world: the organization drawn as a planet lit by what it knows. It draws only what /api/world returns
   (saved records), and writes nothing.
     continent = a collection, or an area of findings kept outside one; always in the same place, growing as it fills
     light     = a current result in that collection; brighter the more recently it was checked, bigger the more is recorded about it
     small light = a finding (hollow = not yet verified); faint light = a change a check noticed
     ring      = a goal with a number, filled to its latest measurement
     clock     = a collection a scheduled task keeps current; amber = it has gone quiet, or something needs review
   Nothing moves unless the person moves it or replays time. */
import * as THREE from '/vendor/three.module.min.js';
const MAXL = 24, NA = MAXL, TAU = Math.PI * 2, FOV = 35, TANH = Math.tan(FOV * Math.PI / 360), ALT_MIN = .16, ALT_MAX = 6.4, HOME_ALT = 5.2;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), sstep = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const hash1 = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const hashS = s => { let h = 2166136261; for (const c of String(s)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
const el = (tag, cls, html = '') => { const e = document.createElement(tag); e.className = cls; e.innerHTML = html; return e; };
const safe = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const glc = el('canvas', 'world-gl'), ui = el('canvas', 'world-ui'), g = ui.getContext('2d');
let renderer = null; try { renderer = new THREE.WebGLRenderer({ canvas: glc, antialias: true, alpha: false }); } catch { renderer = null; }
const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(FOV, 1, .05, 300), globe = new THREE.Group(); scene.add(globe);
let W = 1, H = 1, HOME = 0, TOP = 10;
const CENTERS = Array.from({ length: MAXL }, () => new THREE.Vector3(0, 1, 0));
const U = { uC: { value: CENTERS }, uR: { value: new Array(MAXL).fill(0) }, uCol: { value: CENTERS.map(() => new THREE.Color()) }, uDim: { value: new Array(MAXL).fill(1) }, uPulse: { value: new Array(MAXL).fill(0) },
  uW: { value: new Array(MAXL).fill(0) }, uKit: { value: 0 }, uTime: { value: 0 }, uZoom: { value: 1 }, uSeed: { value: new THREE.Vector3() }, uPaper: { value: new THREE.Color('#ebe7de') } };
const basis = c => { const up = Math.abs(c.y) > .97 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0), e = new THREE.Vector3().crossVectors(up, c).normalize(), n = new THREE.Vector3().crossVectors(c, e); return [e, n]; };
const offset = (c, r, th) => { const [e, n] = basis(c); return c.clone().multiplyScalar(Math.cos(r)).addScaledVector(e, Math.sin(r) * Math.cos(th)).addScaledVector(n, Math.sin(r) * Math.sin(th)).normalize(); };
const lonlat = v => [Math.atan2(v.x, v.z), Math.asin(clamp(v.y, -1, 1))];
const NOISE = `
float hash(vec3 p){p=fract(p*.3183099+.1);p*=17.;return fract(p.x*p.y*p.z*(p.x+p.y+p.z));}
float vnoise(vec3 x){vec3 i=floor(x),f=fract(x);f=f*f*(3.-2.*f);
  return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fbm(vec3 p){float a=.5,s=0.;for(int i=0;i<5;i++){s+=a*vnoise(p);p*=2.03;a*=.5;}return s;}`;
const globeMat = new THREE.ShaderMaterial({ uniforms: U, vertexShader: `varying vec3 vP;varying vec3 vNv;void main(){vP=position;vNv=normalize(normalMatrix*normal);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `precision highp float;varying vec3 vP;varying vec3 vNv;
uniform vec3 uC[${NA}];uniform float uR[${NA}];uniform vec3 uCol[${NA}];uniform float uDim[${NA}];uniform float uPulse[${NA}];uniform float uW[${NA}];uniform int uKit;uniform float uTime,uZoom;uniform vec3 uPaper,uSeed;
${NOISE}
float grid(float x){float f=abs(fract(x-.5)-.5)/max(fwidth(x),1e-5);return 1.-min(f,1.);}
void main(){vec3 p=normalize(vP);float n=fbm(p*5.+3.7+uSeed),n2=fbm(p*15.+9.1+uSeed);
  float best=-9.;vec3 col=vec3(0.);float dim=1.,pulse=0.;vec3 aura=vec3(0.);float aw=0.;
  for(int i=0;i<${NA};i++){float d=acos(clamp(dot(p,uC[i]),-1.,1.));float m=uR[i]-d+(n-.5)*.11*min(1.,uR[i]*4.)+(n2-.5)*.018;
    if(uR[i]>.001&&m>best){best=m;col=uCol[i];dim=uDim[i];pulse=uPulse[i];}
    float w=uW[i]*uDim[i]*pow(max(dot(p,uC[i]),0.),4.);aura+=uCol[i]*w;aw+=w;}
  float land=smoothstep(0.,.005,best),coast=exp(-abs(best)*(50.+110./uZoom)),inner=smoothstep(0.,.22,best);
  float ndv=clamp(vNv.z,0.,1.),rim=pow(1.-ndv,3.);
  float lat=asin(clamp(p.y,-1.,1.)),lon=atan(p.x,p.z);float gr=max(grid(lat*3.8197),grid(lon*3.8197)*step(abs(lat),1.4));
  float live=1.+pulse*(.6+.6*sin(uTime*5.));
  vec3 outc;
  if(uKit==0){
    vec3 ocean=vec3(.014,.028,.055)*(.5+.75*ndv)+vec3(.25,.45,.7)*gr*.07;
    vec3 terrain=mix(vec3(.045,.055,.08),col*.3,.32+.5*inner)*(.55+.95*n2);
    terrain+=col*.1*smoothstep(.5,.78,n2)+col*.06*inner*inner;
    float topo=grid(n*16.+n2*2.5);terrain+=col*topo*.085*(.4+.6*inner);terrain*=(.9+.2*fbm(p*70.)*max(0.,1.5-uZoom))*mix(.45,1.,smoothstep(.3,3.,uZoom));
    vec3 landc=mix(terrain*.3,terrain,dim);
    outc=mix(ocean,landc,land)+col*(coast*.95+exp(-abs(best)*30.)*.16*min(1.,uZoom))*dim*live+(aw>.0001?aura/aw:vec3(0.))*rim*.5*min(1.,aw*3.)+vec3(.3,.45,.7)*rim*.1;
  }else if(uKit==1){
    vec3 paper=uPaper;vec3 ocean=paper*(.955+.045*ndv)-vec3(.5,.45,.35)*gr*.07;
    float hatch=smoothstep(.55,.95,sin((p.x*1.3+p.y*.9+p.z*.4)*240.));
    vec3 landc=mix(paper*1.03,col,.07+.1*inner);landc=mix(landc,col*.75,hatch*.16*(1.-inner*.4));
    landc=mix(paper,landc,mix(.35,1.,dim));
    outc=mix(ocean,landc,land);outc=mix(outc,col*.6,smoothstep(.007*min(1.,uZoom),.0,abs(best))*.9*mix(.3,1.,dim)*live*.9);
    outc=mix(outc,paper*.82,rim*.5);
  }else{
    vec2 q=floor(gl_FragCoord.xy);float ch=mod(q.x+q.y,2.);
    vec3 ocean=vec3(0.)+vec3(.11,.17,.33)*step(.5,gr)*ch;
    vec3 landc=col*(.3+.25*ch*step(.5,n2))*mix(.35,1.,dim);
    outc=mix(ocean,landc,step(0.,best));outc=mix(outc,col*mix(.4,1.,dim)*live,step(abs(best),.007)*step(0.,best));
  }
  gl_FragColor=vec4(outc,1.);}` });
globe.add(new THREE.Mesh(new THREE.SphereGeometry(1, 160, 112), globeMat));
const atmo = (scale, pow, gain) => { const k = Math.sqrt(1 - 1 / (scale * scale)); const m = new THREE.ShaderMaterial({ uniforms: { ...U, uK: { value: k }, uPow: { value: pow }, uGain: { value: gain } }, side: THREE.BackSide, transparent: true, depthWrite: false,
  vertexShader: `varying vec3 vP;varying vec3 vNv;void main(){vP=position;vNv=normalize(normalMatrix*normal);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
  fragmentShader: `precision highp float;varying vec3 vP;varying vec3 vNv;uniform vec3 uC[${NA}];uniform vec3 uCol[${NA}];uniform float uW[${NA}];uniform float uDim[${NA}];uniform int uKit;uniform float uK,uPow,uGain;
void main(){vec3 p=normalize(vP);float f=pow(clamp(-vNv.z/uK,0.,1.),uPow);vec3 a=vec3(0.);float aw=0.;
  for(int i=0;i<${NA};i++){float w=uW[i]*uDim[i]*pow(max(dot(p,uC[i])*.5+.5,0.),5.);a+=uCol[i]*w;aw+=w;}
  vec3 c=aw>.0001?a/aw:vec3(.5,.6,.8);float s=.18+.82*min(1.,aw*2.2);
  if(uKit==0)gl_FragColor=vec4(mix(vec3(.45,.6,.9),c,.85)*f*s*uGain,1.);
  else gl_FragColor=vec4(c,f*s*uGain*.55);}` }); const mesh = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), m); mesh.scale.setScalar(scale); globe.add(mesh); return mesh; };
const atmoIn = atmo(1.2, 2.6, 1.15), atmoOut = atmo(1.75, 5.5, .5);
const LU = { uDay: { value: 730 }, uScale: { value: 600 }, uAlt: { value: HOME_ALT }, uKit: { value: 0 } };
const lightMat = new THREE.ShaderMaterial({ uniforms: LU, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  vertexShader: `attribute vec3 aColor;attribute float aSize,aBorn,aDie,aAlpha,aKind,aState;uniform float uDay,uScale,uAlt;uniform int uKit;varying vec3 vCol;varying float vA,vS,vFlash;
void main(){vec4 mv=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mv;float age=uDay-aBorn;
  float on=smoothstep(0.,5.,age)*(1.-smoothstep(0.,5.,uDay-aDie));vFlash=exp(-max(age,0.)/9.)*step(0.,age);
  float lod=aKind<.5?1.:aKind<1.5?(.45+.55*smoothstep(4.,1.4,uAlt)):aKind<2.5?smoothstep(1.,.38,uAlt):1.;
  vA=on*aAlpha*lod;vCol=aColor;vS=aState;
  float px=aSize*uScale/pow(-mv.z,.55)*(1.+vFlash*.9);if(uKit==2)px=max(2.,floor(px*.34));gl_PointSize=clamp(px,1.,260.);}`,
  fragmentShader: `precision highp float;uniform int uKit;varying vec3 vCol;varying float vA,vS,vFlash;
void main(){vec2 q=gl_PointCoord-.5;float d=length(q)*2.;if(vA<.004)discard;
  if(uKit==0){if(d>1.)discard;float core=exp(-d*d*48.),halo=exp(-d*d*6.)*.55*(1.-d);
    if(vS>.5&&vS<1.5){core=exp(-pow((d-.2)/.055,2.))*.8;}
    vec3 c=vCol*(halo+core*.9)+vec3(1.)*core*(.9+vFlash)+vCol*vFlash*halo*2.;gl_FragColor=vec4(c,vA);}
  else if(uKit==1){if(d>1.)discard;float disc=smoothstep(.34,.28,d),ring=smoothstep(.07,.03,abs(d-.3));float a=vS>.5&&vS<1.5?ring:disc;
    a=max(a,(1.-d)*.13);gl_FragColor=vec4(vCol*(vS>.5&&vS<1.5?.8:.85),a*vA);}
  else{float m=max(abs(q.x),abs(q.y))*2.;if(m>.9)discard;float hollow=vS>.5&&vS<1.5&&m<.45?0.:1.;gl_FragColor=vec4(vCol,step(.35,vA)*hollow);}}` });
const lights = new THREE.Points(new THREE.BufferGeometry(), lightMat); lights.frustumCulled = false; globe.add(lights);
const starGeo = new THREE.BufferGeometry(), sp = new Float32Array(1400 * 3);
for (let i = 0; i < 1400; i++) { const y = hash1(i) * 2 - 1, r = Math.sqrt(1 - y * y), ph = hash1(i + 9000) * TAU; sp[i * 3] = Math.cos(ph) * r * 90; sp[i * 3 + 1] = y * 90; sp[i * 3 + 2] = Math.sin(ph) * r * 90; }
starGeo.setAttribute('position', new THREE.BufferAttribute(sp, 3));
const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xaebbd6, size: 1.5, sizeAttenuation: false, transparent: true, opacity: .55, depthWrite: false })); globe.add(stars);
function ringBuild(R, done) { if (Math.abs(done - R.built) < .003) return; R.built = done; const a = Math.max(.02, done) * TAU; R.arc.geometry.dispose(); R.glow.geometry.dispose();
  R.arc.geometry = new THREE.TorusGeometry(R.r, done >= 1 ? .009 : .0065, 8, 260, a); R.glow.geometry = new THREE.TorusGeometry(R.r, done >= 1 ? .034 : .02, 8, 260, a);
  R.end.set(Math.cos(a) * R.r, Math.sin(a) * R.r, 0).applyMatrix4(R.holder.matrix); }
const cam = { lon: 0, lat: .28, alt: HOME_ALT, to: { lon: 0, lat: .28, alt: HOME_ALT }, v: [0, 0] };
const wrap = a => { a = (a + Math.PI) % TAU; if (a < 0) a += TAU; return a - Math.PI; };
function flyTo(v, alt) { const [lo, la] = lonlat(v); cam.to.lon = cam.lon + wrap(lo - cam.lon); cam.to.lat = clamp(la, -1.35, 1.35); if (alt != null) cam.to.alt = alt; cam.v = [0, 0]; }
function home() { cam.to.lon = cam.lon + wrap(HOME - cam.lon); cam.to.lat = .28; cam.to.alt = HOME_ALT; cam.v = [0, 0]; }
function applyCam(c = cam) { globe.rotation.set(c.lat, -c.lon, 0, 'XYZ'); camera.position.set(0, 0, 1 + c.alt); camera.near = Math.max(.02, c.alt * .2); camera.far = 300; camera.updateProjectionMatrix(); globe.updateMatrixWorld(true); camera.updateMatrixWorld(true); }
const V = new THREE.Vector3();
/* Project a point given in the world's own frame to the screen, and say whether the planet hides it. */
function proj(p, radius = 1, surface = true) { V.copy(p).multiplyScalar(radius).applyMatrix4(globe.matrixWorld); const z = V.z, dist = 1 + cam.alt; let vis, fade;
  if (surface) { const lim = 1 / dist; vis = z > lim + .015; fade = sstep(lim, lim + .14, z); }
  else { const dx = V.x, dy = V.y, dz = V.z - dist, L = Math.hypot(dx, dy, dz), tt = -(dz * dist) / (L * L), cx = dx * tt, cy = dy * tt, cz = dist + dz * tt, dmin = Math.hypot(cx, cy, cz); vis = z > 0 || tt >= 1 || tt <= 0 || dmin > 1.01; fade = vis ? 1 : 0; }
  V.project(camera); return { x: (V.x * .5 + .5) * W, y: (-V.y * .5 + .5) * H, vis, fade }; }
const ray = new THREE.Raycaster(), unit = new THREE.Sphere(new THREE.Vector3(), 1), hitV = new THREE.Vector3(), inv = new THREE.Matrix4();
function pick(clientX, clientY) { const r = ui.getBoundingClientRect(); ray.setFromCamera(new THREE.Vector2((clientX - r.left) / r.width * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1), camera);
  if (!ray.ray.intersectSphere(unit, hitV)) return null; return hitV.clone().applyMatrix4(inv.copy(globe.matrixWorld).invert()).normalize(); }

/* ------------------------------ The stage and its controls ------------------------------ */
const headEl = el('div', 'world-head'), capEl = el('div', 'world-cap'), tipEl = el('div', 'world-tip'), shareEl = el('div', 'world-share'); shareEl.hidden = true;
const barEl = el('div', 'world-bar', `<button type="button" class="primary compact" data-w="play">▶ Watch it light up</button><input type="range" min="0" max="1000" value="1000" aria-label="Move through time"><span class="world-when"></span><span class="world-gap"></span><button type="button" class="secondary compact" data-w="changed">What changed</button><button type="button" class="secondary compact" data-w="flat" aria-pressed="false">Flat map</button><button type="button" class="secondary compact" data-w="tour">Tour</button><button type="button" class="secondary compact" data-w="home">Whole world</button><button type="button" class="secondary compact" data-w="share">Share</button>`);
const range = barEl.querySelector('input'), whenEl = barEl.querySelector('.world-when'), playEl = barEl.querySelector('[data-w=play]');
let M = null, S = { day: 0, q: '' }, dday = 0, ramp = null, show = null, sel = null, hov = null, cb = {}, kit = 0, C = {}, rings = [], hits = [], placed = [], pd = null, moved = false, pointer = null, rec = null, raf = 0, last = 0, touched = false, stage = null, capT = 0, capOpen = null, dirty = true, themeKey = '';

/* ------------------------------ The model, from the feed ------------------------------ */
const landColor = (l, out = new THREE.Color()) => out.setHSL(l.hue / 360, kit ? .72 : .78, kit ? .4 : .62);
const cssHue = (h, l = 68, a = 1) => `hsla(${h},${kit ? 70 : 78}%,${kit ? Math.min(l, 36) : l}%,${a})`;
const gval = (G, d) => { let v = null; for (const p of G.points) if (p.day <= d + .01) v = p.value; return v; };
const gdone = (G, d) => { const v = gval(G, d); if (v == null) return 0; return G.direction === 'lower_better' ? clamp(G.target / Math.max(v, 1e-9), 0, 1) : clamp(v / (G.target || 1), 0, 1); };
const amount = (v, unit) => unit === 'USD' ? '$' + Number(v).toLocaleString(undefined, { maximumFractionDigits: v < 10 ? 2 : 0 }) : Number(v).toLocaleString(undefined, { maximumFractionDigits: 2 }) + (unit && !['count', 'rank', 'USD'].includes(unit) ? ' ' + unit : '');
const goalText = G => { const v = gval(G, S.day); return G.reached && S.day >= M.T - .01 ? 'reached' : v == null ? 'no number yet' : G.direction === 'lower_better' ? `${amount(v, G.unit === 'USD' ? 'USD' : '')} · target ${amount(G.target, G.unit)} or lower` : `${amount(v, G.unit === 'USD' ? 'USD' : '')} of ${amount(G.target, G.unit)}`; };
const dateOf = d => M.date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
function load(feed) { const t = d => d ? Date.parse(d) : NaN, all = [t(feed.business.since)];
  feed.lands.forEach(l => l.items.forEach(i => all.push(t(i.first_seen)))); feed.findings.forEach(f => all.push(t(f.at))); feed.changes.forEach(c => all.push(t(c.at))); feed.goals.forEach(x => (x.points || []).forEach(p => all.push(t(p.at))));
  const now = t(feed.as_of) || Date.now(), t0 = Math.min(now, ...all.filter(Number.isFinite)), day = d => { const v = t(d); return Number.isFinite(v) ? (v - t0) / 864e5 : 0; }, T = Math.max(.01, (now - t0) / 864e5);
  const lands = [...feed.lands.map(l => ({ ...l, unch: false })), ...(feed.uncharted || []).map(a => ({ id: 'new:' + a.id, name: a.name, kind: 'uncharted', items: [], unch: true, area: a.id, slot: a.slot }))].slice(0, MAXL);
  const li = Object.fromEntries(lands.map((l, i) => [l.id, i])), things = [], finds = [], sparks = [], seed = hashS(feed.business.id), n = Math.max(1, lands.length), ph0 = hash1(seed % 9973) * TAU;
  lands.forEach((l, i) => { l.i = i; l.kindOf = 'land'; l.slot = l.slot ?? i; l.hue = (seed % 360 + l.slot * 137.5) % 360; l.things = []; l.finds = [];
    (l.items || []).forEach(it => { const x = { kind: 'item', id: l.id + '|' + it.id, raw: it, land: l, name: it.title, from: day(it.first_seen), seen: day(it.last_seen || it.updated_at), need: !!it.needs_review, changes: 0 }; things.push(x); l.things.push(x); }); });
  feed.findings.forEach(f => { const l = lands[li[f.land]]; if (!l || f.label === 'replaced') return; const x = { kind: 'finding', id: f.id, raw: f, land: l, name: f.statement, label: f.label, from: day(f.at), need: ['challenged', 'needs_review', 'out_of_date'].includes(f.label) }; finds.push(x); l.finds.push(x); });
  const byItem = Object.fromEntries(things.map(x => [x.id, x]));
  finds.forEach(x => { x.tied = (x.raw.items || []).map(id => byItem[x.land.id + '|' + id]).filter(Boolean); });
  feed.changes.forEach((c, k) => { const l = lands[li[c.land]]; if (!l) return; const th = byItem[c.land + '|' + c.item_id]; if (th) th.changes++; sparks.push({ day: day(c.at), land: l, th, raw: c, k }); });
  lands.forEach((l, i) => { const u = (.5 + l.slot * .7548776662) % 1, v = (.5 + l.slot * .569840291 + ph0 / TAU) % 1, y = .8 * (1 - 2 * u), r = Math.sqrt(1 - y * y), ph = v * TAU; CENTERS[i].set(Math.cos(ph) * r, y, Math.sin(ph) * r); l.c = CENTERS[i];
    const order = [...l.things, ...l.finds]; l.rmax = l.unch ? .2 : l.kind === 'group' ? Math.min(.42, .2 + .02 * Math.sqrt(l.more || 1)) : Math.min(n > 10 ? .34 : .5, .2 + .05 * Math.sqrt(order.length));
    order.forEach((x, k) => { x.p = offset(l.c, l.rmax * .74 * Math.sqrt((k + .5) / order.length), k * 2.39996 + i); }); });
  /* A finding sits beside the result it rests on, when the same saved source stands behind both. */
  { const per = {}; finds.forEach(x => { const th = x.tied[0]; if (!th) return; const j = per[th.id] = (per[th.id] || 0) + 1; x.p = offset(th.p, .024 + .007 * ((j - 1) % 3), j * 2.39996 + hash1(j + th.from)); }); }
  sparks.forEach(s => { s.p = offset(s.th ? s.th.p : s.land.c, s.th ? .014 + .06 * Math.sqrt(hash1(s.k + 3)) : s.land.rmax * .6 * Math.sqrt(hash1(s.k + 3)), hash1(s.k + 11) * TAU); });
  const goals = feed.goals.filter(x => typeof x.target === 'number').slice(0, 4).map(x => ({ kind: 'goal', id: x.id, raw: x, name: x.name, unit: x.unit, target: x.target, direction: x.direction, reached: !!x.reached, lands: x.lands || [], points: (x.points || []).map(p => ({ day: day(p.at), value: p.value })) }));
  const real = lands.filter(l => !l.unch && l.kind !== 'group'), fById = Object.fromEntries(finds.map(x => [x.id, x])), decisions = real.length ? feed.decisions.map((d, k) => { const basis = (d.basis || []).map(id => fById[id]).filter(Boolean), l = basis[0]?.land || lands[li['area:' + d.area]] || real[k % real.length]; return { kind: 'decision', lesson: d.kind === 'lesson', id: d.id, raw: d, name: d.title, day: day(d.at), land: l, basis, p: basis[0] ? offset(basis[0].p, .035, 1 + k * 2.1) : offset(l.c, l.rmax * .5, 1 + k * 2.1) }; }) : [];
  const seenTasks = {}, tasks = (feed.tasks || []).filter(k => lands[li[k.land]]).map(k => { const l = lands[li[k.land]], n = seenTasks[l.id] = (seenTasks[l.id] || 0) + 1, foot = offset(l.c, l.rmax * .55, 2.2 + l.i + n * 1.7); return { kind: 'task', id: k.id, raw: k, name: k.name || 'Scheduled task', land: l, foot, p: foot.clone().multiplyScalar(1.2) }; });
  M = { feed, lands, things, finds, sparks, goals, decisions, tasks, T, date: d => new Date(t0 + d * 864e5), name: feed.business.name, days: T };
  for (let i = lands.length; i < MAXL; i++) { U.uR.value[i] = 0; U.uW.value[i] = 0; }
  const r = k => hash1(seed % 9973 + k * 31.7); U.uSeed.value.set(r(1) * 40, r(2) * 40, r(3) * 40);
  /* Lights. */
  const N = things.length + finds.length + sparks.length, A = { position: new Float32Array(N * 3), aColor: new Float32Array(N * 3), aSize: new Float32Array(N), aBorn: new Float32Array(N), aDie: new Float32Array(N).fill(1e9), aAlpha: new Float32Array(N), aKind: new Float32Array(N), aState: new Float32Array(N) };
  [...things, ...finds, ...sparks].forEach((x, i) => { A.position.set([x.p.x * 1.004, x.p.y * 1.004, x.p.z * 1.004], i * 3); A.aBorn[i] = x.kind ? x.from : x.day; A.aKind[i] = x.kind === 'item' ? 0 : x.kind === 'finding' ? 1 : 3; });
  const geo = new THREE.BufferGeometry(); for (const k in A) geo.setAttribute(k, new THREE.BufferAttribute(A[k], k === 'position' || k === 'aColor' ? 3 : 1)); lights.geometry.dispose(); lights.geometry = geo;
  /* Goal rings: concentric, tilted by an amount that belongs to this organization. */
  rings.forEach(R => { globe.remove(R.holder); for (const o of [R.track, R.arc, R.glow]) { o.geometry.dispose(); o.material.dispose(); } });
  rings = goals.map((G, i) => { const rr = 1.5 + i * .12, holder = new THREE.Group(); holder.rotation.set(Math.PI / 2 + (r(4) - .5) * .5, (r(5) - .5) * .5, .9 + i * 2.2 + r(6) * 6); holder.updateMatrix(); globe.add(holder);
    const pts = Array.from({ length: 241 }, (_, k) => new THREE.Vector3(Math.cos(k / 240 * TAU) * rr, Math.sin(k / 240 * TAU) * rr, 0));
    const track = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ transparent: true, opacity: .22, depthWrite: false })), arc = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false })), glow = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ transparent: true, opacity: .16, depthWrite: false }));
    holder.add(track); holder.add(arc); holder.add(glow); return { G, r: rr, holder, track, arc, glow, built: -1, shown: 0, end: new THREE.Vector3(), around: pts.filter((_, k) => k % 4 === 0 && k < 240).map(v => v.clone().applyMatrix4(holder.matrix)) }; });
  /* Home faces the side where most is known. */
  let bs = -1; for (let k = 0; k < 90; k++) { const lon = k / 90 * TAU, f = new THREE.Vector3(Math.cos(.28) * Math.sin(lon), Math.sin(.28), Math.cos(.28) * Math.cos(lon)); let sc = 0; lands.forEach(l => sc += (l.things.length + l.finds.length + .5) * Math.pow(Math.max(0, l.c.dot(f)), 1.5)); if (sc > bs) { bs = sc; HOME = lon; } }
  cam.lon = cam.to.lon = HOME; cam.lat = cam.to.lat = .28; cam.alt = cam.to.alt = HOME_ALT; cam.v = [0, 0];
  S.day = T; S.q = ''; dday = T; sel = null; hov = null; show = null; ramp = null; themeKey = ''; dirty = true; range.value = 1000; barEl.classList.toggle('young', T < 2); }

let px = false;
function theme() { const cs = getComputedStyle(stage), style = document.documentElement.dataset.style || '', key = cs.backgroundColor + cs.color + cs.fontFamily + style; if (key === themeKey) return; themeKey = key; px = style === 'console90' || style === 'desktop90'; pxRatio = style === 'desktop90' ? 1 / 2 : 1 / 3;
  const rgb = (cs.backgroundColor.match(/[\d.]+/g) || [10, 12, 16]).map(Number), lum = (.299 * rgb[0] + .587 * rgb[1] + .114 * rgb[2]) / 255, v = n => cs.getPropertyValue(n).trim();
  kit = lum > .55 ? 1 : 0; C = { stage: `rgb(${rgb[0]},${rgb[1]},${rgb[2]})`, ink: cs.color, muted: v('--muted') || (kit ? '#5d5a52' : '#8d98ab'), accent: v('--accent') || (kit ? '#1d7552' : '#7cf0bd'), warn: kit ? '#a35f0a' : '#f2b45a', font: cs.fontFamily, amber: new THREE.Color(kit ? '#a35f0a' : '#f2b45a') };
  renderer.setClearColor(new THREE.Color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255), 1); U.uKit.value = px ? 2 : kit; LU.uKit.value = px ? 2 : kit; glc.style.imageRendering = px ? 'pixelated' : ''; atmoIn.material.uniforms.uGain.value = style === 'desktop00' ? 1.7 : 1.15; fit(); U.uPaper.value.setRGB(rgb[0] / 255 * .97, rgb[1] / 255 * .96, rgb[2] / 255 * .94);
  const add = kit ? THREE.NormalBlending : THREE.AdditiveBlending; lightMat.blending = add; lightMat.needsUpdate = true; for (const m of [atmoIn, atmoOut]) { m.material.blending = add; m.material.needsUpdate = true; m.visible = !px; } atmoOut.visible = !px && style !== 'classic'; stars.visible = !kit && style !== 'classic';
  rings.forEach(R => { const c = new THREE.Color().setHSL((hashS(R.G.id) % 360) / 360, kit ? .72 : .78, kit ? .4 : .66); R.hue = hashS(R.G.id) % 360; for (const o of [R.track, R.arc, R.glow]) { o.material.color.copy(c); o.material.blending = add; o.material.needsUpdate = true; } R.glow.visible = !kit; }); dirty = true; }
function fit() { if (!stage) return; const r = stage.getBoundingClientRect(); W = Math.max(1, r.width); H = Math.max(1, r.height); const dpr = Math.min(2, devicePixelRatio || 1); renderer.setPixelRatio(px ? pxRatio : dpr); renderer.setSize(W, H, false); camera.aspect = W / H; camera.updateProjectionMatrix(); ui.width = W * dpr; ui.height = H * dpr; g.setTransform(dpr, 0, 0, dpr, 0, 0); TOP = headEl.offsetHeight ? 10 : 10; }
let F = { lands: null, needs: false }, running = [], flat = false, sinceT = 0, pxRatio = 1 / 3;
const dimOf = l => F.lands && !F.lands.includes(l.id) ? .15 : sel && sel.kindOf === 'land' && !sel.unch ? (l === sel ? 1 : .2) : sel && sel.kind === 'goal' && sel.lands.length ? (sel.lands.includes(l.id) ? 1 : .2) : 1;
function sync() { dirty = false; const geo = lights.geometry, A = n => geo.attributes[n].array, col = A('aColor'), size = A('aSize'), al = A('aAlpha'), st = A('aState'), tmp = new THREE.Color(), q = S.q; let i = 0, wmax = 1;
  M.lands.forEach(l => { const nt = l.things.filter(x => x.from <= S.day).length + l.finds.filter(x => x.from <= S.day).length, tot = l.things.length + l.finds.length; l.rto = l.kind === 'group' ? l.rmax : l.unch || !nt ? 0 : l.rmax * Math.sqrt((nt + 1) / (tot + 1)); l.w = l.kind === 'group' ? 1 : nt; wmax = Math.max(wmax, nt); l.dim = dimOf(l); landColor(l, U.uCol.value[l.i]); });
  M.lands.forEach(l => { U.uW.value[l.i] = l.w / wmax; });
  const put = c => { col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b; }, match = x => (!q || x.name.toLowerCase().includes(q)) && (!F.needs || x.need);
  for (const x of M.things) { const fresh = clamp(1 - (M.T - x.seen) / 120, 0, 1); put(x.need ? C.amber : landColor(x.land, tmp)); size[i] = .078 + .02 * Math.log2(1 + (x.raw.sources || 0) + x.changes); al[i] = (.5 + .5 * fresh) * x.land.dim * (match(x) ? 1 : .14); st[i] = x.need ? 2 : 0; i++; }
  for (const x of M.finds) { put(x.need ? C.amber : kit ? landColor(x.land, tmp) : landColor(x.land, tmp).lerp(new THREE.Color('#ffffff'), .25)); size[i] = .04 + .012 * Math.log2(1 + (x.raw.given || 0)); al[i] = (x.label === 'unverified' ? .75 : .9) * x.land.dim * (match(x) ? 1 : .14); st[i] = x.need ? 2 : x.label === 'unverified' ? 1 : 0; i++; }
  for (const s of M.sparks) { put(landColor(s.land, tmp)); const h = hash1(s.k + 5); size[i] = .017 + .008 * h; al[i] = (.35 + .4 * h) * s.land.dim * (q || F.needs ? .25 : 1); i++; }
  for (const k of ['aColor', 'aSize', 'aAlpha', 'aState']) geo.attributes[k].needsUpdate = true;
  whenEl.textContent = `${dateOf(S.day)} · ${M.things.filter(x => x.from <= S.day).length} tracked · ${M.finds.filter(x => x.from <= S.day).length} findings`; headline(); }

/* ------------------------------ Words on the picture ------------------------------ */
function txt(s, x, y, { size = 12, weight = 600, color = C.ink, align = 'left', alpha = 1, track = 0 } = {}) { if (alpha <= .01) return; g.save(); g.font = `${weight} ${size}px ${C.font}`; g.letterSpacing = track + 'px'; g.textAlign = align; g.textBaseline = 'middle'; g.lineJoin = 'round'; g.lineWidth = 3.5; g.strokeStyle = C.stage; g.globalAlpha = alpha * (kit ? .9 : .8); g.strokeText(s, x, y); g.globalAlpha = alpha; g.fillStyle = color; g.fillText(s, x, y); g.restore(); }
const wOf = (s, size, weight = 600, track = 0) => { g.save(); g.font = `${weight} ${size}px ${C.font}`; g.letterSpacing = track + 'px'; const w = g.measureText(s).width; g.restore(); return w; };
function wrapText(s, size, max) { const lines = ['']; for (const w of String(s).split(' ')) { const t = lines.at(-1) ? lines.at(-1) + ' ' + w : w; if (wOf(t, size, 500) > max && lines.at(-1)) lines.push(w); else lines[lines.length - 1] = t; } if (lines.length > 3) { lines.length = 3; lines[2] += '…'; } return lines; }
const free = (x, y, w, h) => { if (y < TOP + 48 || y + h > H - 56 || x < 4 || x + w > W - 4) return false; for (const b of placed) if (x < b[0] + b[2] && x + w > b[0] && y < b[1] + b[3] && y + h > b[1]) return false; return true; };
const take = (x, y, w, h) => placed.push([x - 3, y - 2, w + 6, h + 4]);
const hit = (x, y, w, h, s, tip) => hits.push({ x, y, w, h, s, tip });
const alertDot = (x, y) => { g.save(); g.fillStyle = C.warn; g.beginPath(); g.arc(x, y, 7, 0, TAU); g.fill(); g.fillStyle = kit ? '#fff' : '#111'; g.font = `800 10px ${C.font}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('!', x, y + .5); g.restore(); };
const fieldLine = x => { const e = Object.entries(x.raw.fields || {})[0]; return e ? `${e[0]}: ${e[1]}` : ''; };
function overlay(t, dd) { placed = []; hits = []; const alt = cam.alt, playing = show?.type === 'play', focus = hov && hov.p ? hov : sel && sel.p ? sel : null; g.clearRect(0, 0, W, H);
  /* Rings: the goal's name and number where its ring comes nearest. */
  rings.forEach((R, ri) => { const far = sstep(1.2, 2.2, alt); if (far < .02) return; const c = cssHue(R.hue, 72), pv = proj(R.end, 1, false);
    if (pv.vis && R.shown < .995) { g.save(); g.globalAlpha = far; g.fillStyle = c; g.beginPath(); g.arc(pv.x, pv.y, 4.5, 0, TAU); g.fill(); g.fillStyle = C.stage; g.beginPath(); g.arc(pv.x, pv.y, 2, 0, TAU); g.fill(); g.restore(); }
    let bi = 0, bz = -9; R.around.forEach((v, k) => { V.copy(v).applyMatrix4(globe.matrixWorld); const sc = V.z + V.x * .55; if (sc > bz) { bz = sc; bi = k; } }); const an = proj(R.around[(bi + (ri - 1) * 4 + 60) % 60], 1, false), lbl = `${R.G.name} · ${goalText(R.G)}`, w = wOf(lbl, 12), lx = Math.min(an.x + 12, W - w - 10); let ly = an.y; for (const dy of [0, 19, -19, 38, -38, 57, -57]) { if (free(lx, an.y + dy - 9, w + 4, 18)) { ly = an.y + dy; break; } }
    g.save(); g.globalAlpha = far; g.fillStyle = c; g.beginPath(); g.arc(an.x, an.y, 3, 0, TAU); g.fill(); g.restore();
    const words = !playing && W >= 560; if (words) { txt(lbl, lx, ly, { size: 12, color: sel === R.G ? C.accent : c, alpha: far }); take(lx, ly - 9, w, 18); } hit(an.x - 10, ly - 11, words ? w + 26 : 20, 22, R.G, [R.G.name, 'Goal · ' + goalText(R.G) + ' · click to open']); });
  /* Continents, and places still to chart. */
  for (const l of M.lands) { const c = proj(l.c, 1.004); if (!c.vis) continue;
    if (U.uR.value[l.i] < .02) { if (!l.unch) continue; const al = c.fade * sstep(.6, 1.4, alt) * (playing ? .5 : 1); if (al < .03) continue; g.save(); g.strokeStyle = cssHue(l.hue, 66); g.globalAlpha = al * .6; g.setLineDash([3, 5]); g.beginPath(); let pen = false;
        for (let k = 0; k <= 48; k++) { const s = proj(offset(l.c, l.rmax * (1 + .13 * Math.sin(k * .8 + l.i * 2)), k / 48 * TAU), 1.004); if (!s.vis) { pen = false; continue; } pen ? g.lineTo(s.x, s.y) : g.moveTo(s.x, s.y); pen = true; } g.stroke(); g.restore(); if (playing) continue;
        const w = Math.max(74, wOf(l.name, 12)); txt('UNCHARTED', c.x, c.y - 8, { size: 9.5, weight: 700, color: C.muted, align: 'center', alpha: al, track: 2 }); txt(l.name, c.x, c.y + 7, { size: 12, color: cssHue(l.hue, 74), align: 'center', alpha: al }); take(c.x - w / 2, c.y - 16, w, 32); hit(c.x - w / 2 - 6, c.y - 18, w + 12, 36, l, [l.name + ' · uncharted', 'Nothing is saved here yet. Click to start charting it.']); continue; }
    const top = proj(offset(l.c, U.uR.value[l.i] * .92, Math.PI / 2), 1.004), al = c.fade * sstep(.28, .6, alt) * (l.dim > .5 ? 1 : .35), size = clamp(10.5 + (2.2 - alt) * 2.2, 10.5, 15), name = l.name.toUpperCase(), w = wOf(name, size, 700, 2), x = top.x, y = Math.max(TOP + 58, Math.min(top.y, c.y - 14)); if (al < .03) continue;
    txt(name, x, y, { size, weight: 700, color: cssHue(l.hue, 74), align: 'center', alpha: al, track: 2 }); take(x - w / 2, y - size * .7, w, size * 1.4);
    if (alt < 3.6 && alt > .5 && !playing) { const nt = l.things.length + (l.more || 0), sub = [nt ? `${nt} tracked` : '', l.finds.length ? `${l.finds.length} finding${l.finds.length === 1 ? '' : 's'}` : ''].filter(Boolean).join(' · '); txt(sub, x, y + size + 3, { size: 10.5, weight: 500, color: C.muted, align: 'center', alpha: al * .9 }); take(x - 60, y + size - 5, 120, 15); }
    if (l.quiet) alertDot(x + w / 2 + 12, y);
    hit(x - w / 2 - 6, y - 10, w + 12, 22, l, [l.name, 'Click to fly there']); }
  if (alt < 1.25) { const ta = sstep(1.25, .8, alt); g.save(); g.lineWidth = 1; for (const f of M.finds) { if (!f.tied.length || f.from > dd || f.land.dim < .5) continue; const a = proj(f.p, 1.004); if (!a.vis || a.x < -50 || a.x > W + 50 || a.y < -50 || a.y > H + 50) continue;
      for (const th of f.tied) { const b = proj(th.p, 1.004); if (!b.vis) continue; g.strokeStyle = cssHue(f.land.hue, 70); g.globalAlpha = ta * (f === focus || th === focus ? .9 : .3); g.beginPath(); g.moveTo(a.x, a.y); g.lineTo(b.x, b.y); g.stroke(); } } g.restore(); }
  if (alt > .7) for (const k of M.tasks) { const l = k.land; if (U.uR.value[l.i] < .02) continue; const a = proj(k.p, 1, false), b = proj(k.foot, 1.004); if (!a.vis) continue; const far = sstep(.7, 1.3, alt) * (l.dim > .5 ? 1 : .3), bad = ['failed', 'missing', 'paused'].includes(k.raw.health), col = bad ? C.warn : C.muted, on = sel === k || hov === k; if (far < .02) continue;
    g.save(); g.globalAlpha = far * .6; g.strokeStyle = col; g.lineWidth = 1; g.setLineDash([2, 3]); if (b.vis) { g.beginPath(); g.moveTo(a.x, a.y); g.lineTo(b.x, b.y); g.stroke(); } g.setLineDash([]);
    g.globalAlpha = far; g.fillStyle = C.stage; g.beginPath(); g.arc(a.x, a.y, 8, 0, TAU); g.fill(); g.strokeStyle = on ? C.accent : col; g.lineWidth = 1.5; g.beginPath(); g.arc(a.x, a.y, 6, 0, TAU); g.moveTo(a.x, a.y - 3.5); g.lineTo(a.x, a.y); g.lineTo(a.x + 2.6, a.y + 1.6); g.stroke(); g.restore();
    if (bad) alertDot(a.x + 8, a.y - 8); if (on) txt(k.name, a.x + 14, a.y, { size: 11.5, color: C.accent, alpha: far });
    hit(a.x - 11, a.y - 11, 22, 22, k, [k.name, (k.raw.schedule ? k.raw.schedule + ' · ' : '') + (k.raw.status || '')]); }
  running.forEach((r, i) => { const y0 = TOP + 62 + i * 22, l = M.lands.find(z => z.id === r.land); txt(r.label, 28, y0, { size: 11.5, color: C.accent }); g.save(); g.fillStyle = C.accent; g.beginPath(); g.arc(15, y0, 3 + Math.sin(t / 220), 0, TAU); g.fill();
    if (l) { const c = proj(l.c, 1.004); if (c.vis) { g.strokeStyle = C.accent; g.globalAlpha = .4; g.setLineDash([2, 5]); g.lineDashOffset = -t / 40; g.beginPath(); g.moveTo(34 + wOf(r.label, 11.5), y0); g.lineTo(c.x, c.y); g.stroke(); } } g.restore(); });
  /* Up close, findings as sentences and lights by name. */
  const shown = [];
  if (alt < 2.6) for (const f of M.finds) { if (f.from > dd || f.land.dim < .5 || (S.q && !f.name.toLowerCase().includes(S.q))) continue; const s = proj(f.p, 1.004); if (!s.vis || s.x < 0 || s.x > W || s.y < TOP || s.y > H) continue; const r = clamp(5 + (1.2 - alt) * 5, 5, 10); hit(s.x - r, s.y - r, r * 2, r * 2, f, [f.name, FLABEL[f.label] + ' · click to open']); shown.push({ f, s }); }
  const tl = [];
  for (const x of M.things) { if (x.from > dd) continue; const s = proj(x.p, 1.004); if (!s.vis || s.x < -40 || s.x > W + 40 || s.y < 0 || s.y > H + 40) continue; const dim = x.land.dim < .5 || (S.q && !x.name.toLowerCase().includes(S.q)), r = clamp(8 + (1.4 - alt) * 5, 7, 15);
    if (!dim) hit(s.x - r, s.y - r, r * 2, r * 2, x, [x.name, [x.land.name, fieldLine(x), 'click to open'].filter(Boolean).join(' · ')]); tl.push({ x, s, dim, pri: (x === focus ? 1e6 : 0) + (x.need ? 5e4 : 0) + (S.q && !dim ? 1e4 : 0) + x.changes * 10 + (x.raw.sources || 0) + clamp(1 - (M.T - x.seen) / 120, 0, 1) * 5 + hash1(x.from) }); }
  tl.sort((a, b) => b.pri - a.pri); const cap = playing ? 0 : alt > 3.6 ? 9 : alt > 2.2 ? 18 : alt > 1.2 ? 36 : 999; let n = 0;
  const mark = (o, c, r0) => { const s = proj(o.p, 1.004); if (!s.vis) return; g.save(); g.strokeStyle = c; g.lineWidth = 1.4; const r1 = r0 + (o.kind === 'item' ? 6 : 0); g.beginPath(); g.arc(s.x, s.y, r1, 0, TAU); g.stroke(); for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2; g.beginPath(); g.moveTo(s.x + Math.cos(a) * (r1 + 3), s.y + Math.sin(a) * (r1 + 3)); g.lineTo(s.x + Math.cos(a) * (r1 + 8), s.y + Math.sin(a) * (r1 + 8)); g.stroke(); } g.restore(); };
  if (sel && sel.p) mark(sel, C.accent, 9); if (hov && hov.p && hov !== sel) mark(hov, C.ink, 8);
  for (const { x, s, dim, pri } of tl) { if (dim && pri < 1e4) continue; if (n >= cap && pri < 1e4) break; const size = clamp(11 + (1.4 - alt) * 2.2, 11, 14.5), w = wOf(x.name, size), extra = alt < .62 ? Object.entries(x.raw.fields || {}).slice(0, alt < .4 ? 3 : 1).map(([k, v]) => `${k}: ${v}`) : [], line2 = extra.length, bw = Math.max(w, ...extra.map(e => wOf(e, 11, 500))), bh = size + 5 + extra.length * 14, r = clamp(9 + (1.4 - alt) * 5, 8, 18), al = s.fade;
    let px = s.x + r, py = s.y - bh / 2, ok = free(px, py, bw, bh); if (!ok) { px = s.x - r - bw; ok = free(px, py, bw, bh); } if (!ok) { px = s.x - bw / 2; py = s.y + r; ok = free(px, py, bw, bh); } if (!ok && pri < 1e5) continue;
    txt(x.name, px, py + size * .6, { size, color: x.need ? C.warn : x === focus ? C.accent : C.ink, alpha: al }); extra.forEach((e, i) => txt(e, px, py + size + 9 + i * 14, { size: 11, weight: 500, color: C.muted, alpha: al })); take(px, py, bw, bh); n++; if (x.need) alertDot(s.x - r, s.y - r); }
  if (alt < .95 && !playing) { shown.sort((a, b) => (b.f === focus) - (a.f === focus) || b.f.from - a.f.from); const a0 = sstep(.95, .7, alt);
    for (const { f, s } of shown) { const lines = wrapText(f.name, 11.5, 210), bw = Math.max(...lines.map(l => wOf(l, 11.5, 500))), bh = lines.length * 15 + 2; let px = s.x + 9, py = s.y - bh / 2, ok = free(px, py, bw, bh); if (!ok) { px = s.x - 9 - bw; ok = free(px, py, bw, bh); } if (!ok) { px = s.x - bw / 2; py = s.y + 9; ok = free(px, py, bw, bh); } if (!ok && f !== focus) continue;
      lines.forEach((l, i) => txt(l, px, py + 8 + i * 15, { size: 11.5, weight: 500, color: f.need ? C.warn : f === focus ? C.accent : f.label === 'unverified' ? C.muted : cssHue(f.land.hue, kit ? 30 : 84), alpha: a0 * s.fade })); take(px, py, bw, bh); hit(px, py, bw, bh, f, [f.name, FLABEL[f.label] + ' · click to open']); if (f.need) alertDot(s.x - 9, s.y - 9); } }
  /* Landmarks: decisions stay on the map, in the person's own words. */
  if (alt < 3.8 && !playing) for (const d of M.decisions) { if (d.day > dd || d.land.dim < .5) continue; const s = proj(d.p, 1.004); if (!s.vis || s.x < 0 || s.x > W || s.y < TOP || s.y > H - 56) continue; const r = clamp(4 + (1.6 - alt) * 2, 4, 7), on = sel === d, c = on ? C.accent : C.ink, a0 = sstep(3.8, 2.6, alt) * s.fade;
    g.save(); g.globalAlpha = a0; g.fillStyle = C.stage; g.strokeStyle = c; g.lineWidth = 1.5; g.beginPath(); g.moveTo(s.x, s.y - r); g.lineTo(s.x + r, s.y); g.lineTo(s.x, s.y + r); g.lineTo(s.x - r, s.y); g.closePath(); g.fill(); g.stroke(); g.restore(); hit(s.x - r - 3, s.y - r - 3, r * 2 + 6, r * 2 + 6, d, [d.name, (d.lesson ? 'Lesson · ' : 'Decision · ') + dateOf(d.day) + ' · click to open']); if (on || hov === d) for (const b of d.basis) { const e = proj(b.p, 1.004); if (e.vis) { g.save(); g.strokeStyle = C.accent; g.globalAlpha = .7; g.lineWidth = 1.2; g.beginPath(); g.moveTo(s.x, s.y); g.lineTo(e.x, e.y); g.stroke(); g.restore(); } }
    if (alt < 1.7 || on) { const lines = wrapText(d.name, 11.5, 190), bw = Math.max(...lines.map(l => wOf(l, 11.5))), bh = lines.length * 15 + 2; let px = s.x + r + 6; const py = s.y - bh / 2; if (!free(px, py, bw, bh)) { px = s.x - r - 6 - bw; if (!free(px, py, bw, bh) && !on) continue; } lines.forEach((l, i) => txt(l, px, py + 8 + i * 15, { size: 11.5, color: c, alpha: a0 })); take(px, py, bw, bh); } }
  /* The whole world at a glance, because a globe hides its far side. */
  if (W > 560 && !playing && M.lands.length > 1) { const w = 150, h = 74, x0 = W - w - 12, y0 = 66; placed.push([x0 - 4, y0 - 4, w + 8, h + 8]); g.save(); g.globalAlpha = .92; g.fillStyle = C.stage; g.strokeStyle = C.muted; g.lineWidth = .6; g.beginPath(); g.roundRect(x0, y0, w, h, 9); g.fill(); g.stroke();
    const X = lon => x0 + 8 + ((wrap(lon - HOME) + Math.PI) / TAU) * (w - 16), Y = lat => y0 + h / 2 - lat / 1.1 * (h / 2 - 8);
    for (const l of M.lands) { const [lo, la] = lonlat(l.c), cx = X(lo), cy = Y(la), r = Math.max(3.5, (l.rto || l.rmax * .5) * 18); g.beginPath(); g.arc(cx, cy, r, 0, TAU); if (l.rto) { g.fillStyle = cssHue(l.hue, 62); g.globalAlpha = l.dim > .5 ? .9 : .25; g.fill(); } else { g.setLineDash([2, 2]); g.strokeStyle = cssHue(l.hue, 62); g.globalAlpha = .75; g.stroke(); g.setLineDash([]); }
      if (l.quiet || l.things.some(x => x.need) || l.finds.some(x => x.need)) { g.globalAlpha = 1; g.fillStyle = C.warn; g.beginPath(); g.arc(cx + r * .7, cy - r * .7, 2.8, 0, TAU); g.fill(); } hit(cx - r, cy - r, r * 2, r * 2, l, [l.name, l.unch ? 'Uncharted · click to start charting it' : 'Click to fly there']); }
    g.globalAlpha = 1; g.strokeStyle = C.ink; g.lineWidth = 1.2; g.beginPath(); g.arc(clamp(X(cam.lon), x0 + 4, x0 + w - 4), clamp(Y(cam.lat), y0 + 4, y0 + h - 4), clamp(cam.alt * 5, 4, 22), 0, TAU); g.stroke(); g.restore(); }
  if (show?.type === 'steps' && show.pos) { const s = proj(show.pos, 1.004); if (s.vis) { const u = ((t - show.stepAt) / 1400) % 1; g.save(); g.strokeStyle = C.accent; g.lineWidth = 1.6; g.globalAlpha = 1 - u; g.beginPath(); g.arc(s.x, s.y, 10 + u * 34, 0, TAU); g.stroke(); g.restore(); } } }
function flatMap(t, dd) { placed = []; hits = []; g.clearRect(0, 0, W, H); const top = TOP + 56, bot = H - 64, k = Math.min((W - 40) / TAU, (bot - top) / 2.2), cx = W / 2, cy = (top + bot) / 2, at = p => { const [lo, la] = lonlat(p); return [cx + wrap(lo - HOME) * k, cy - la * k]; };
  g.save(); g.strokeStyle = C.muted; g.globalAlpha = .25; g.strokeRect(cx - Math.PI * k, cy - 1.1 * k, TAU * k, 2.2 * k); g.restore();
  for (const l of M.lands) { const [x, y] = at(l.c), r = Math.max(10, (l.rto || l.rmax * .6) * k); g.save(); g.beginPath(); g.arc(x, y, r, 0, TAU); if (l.rto) { g.fillStyle = cssHue(l.hue, kit ? 60 : 32, kit ? .2 : .55); g.globalAlpha = l.dim > .5 ? 1 : .3; g.fill(); g.strokeStyle = cssHue(l.hue, 66); g.lineWidth = sel === l ? 2.5 : 1.5; g.stroke(); } else { g.setLineDash([3, 5]); g.strokeStyle = cssHue(l.hue, 66); g.globalAlpha = .7; g.stroke(); } g.restore();
    const name = l.name.toUpperCase(), w = wOf(name, 10.5, 700, 1.5); txt(name, x, y - r - 9, { size: 10.5, weight: 700, color: cssHue(l.hue, 74), align: 'center', track: 1.5, alpha: l.dim > .5 ? 1 : .4 }); if (l.quiet) alertDot(x + w / 2 + 10, y - r - 9); hit(x - w / 2, y - r - 18, w, 18, l, [l.name, l.unch ? 'Uncharted · click to start charting it' : 'Click to open']); }
  for (const f of M.finds) { if (f.from > dd || f.land.dim < .5) continue; const [x, y] = at(f.p); g.fillStyle = f.need ? C.warn : cssHue(f.land.hue, kit ? 30 : 82, .85); g.beginPath(); g.arc(x, y, f === sel ? 4 : 1.7, 0, TAU); g.fill(); }
  for (const th of M.things) { if (th.from > dd || th.land.dim < .5 || (S.q && !th.name.toLowerCase().includes(S.q)) || (F.needs && !th.need)) continue; const [x, y] = at(th.p), on = th === sel || th === hov; g.fillStyle = th.need ? C.warn : cssHue(th.land.hue, kit ? 38 : 72); g.beginPath(); g.arc(x, y, on ? 5.5 : 3, 0, TAU); g.fill(); hit(x - 6, y - 6, 12, 12, th, [th.name, th.land.name + ' · click to open']); if (on) txt(th.name, x + 9, y, { size: 12, color: C.accent }); }
  M.goals.forEach((G, i) => { const x = 18, y = top + 4 + i * 28, d = gdone(G, S.day); txt(`${G.name} · ${goalText(G)}`, x, y, { size: 11.5, color: sel === G ? C.accent : C.ink }); g.save(); g.fillStyle = C.muted; g.globalAlpha = .3; g.fillRect(x, y + 10, 170, 3); g.globalAlpha = 1; g.fillStyle = C.accent; g.fillRect(x, y + 10, 170 * d, 3); g.restore(); hit(x, y - 9, 270, 26, G, [G.name, 'Goal · click to open']); }); }
const FLABEL = { supported: 'Supported finding', unverified: 'Finding, not yet verified', challenged: 'Finding challenged by new evidence', needs_review: 'Finding due for review', out_of_date: 'Finding out of date' };

/* The one line read first: the nearest goal, and whether anything needs the person. */
function headline() { const f = M.feed, n = f.totals.attention, open = M.goals.filter(G => !G.reached && gval(G, S.day) != null).sort((a, b) => gdone(b, S.day) - gdone(a, S.day))[0], lit = M.things.filter(x => x.from <= S.day).length + M.finds.filter(x => x.from <= S.day).length, unch = M.lands.filter(l => l.unch).length, nd = n ? `${n} thing${n === 1 ? ' needs' : 's need'} you` : 'Nothing needs you';
  let b, s; if (!lit) { b = 'Your world starts here.'; s = unch ? 'Click an uncharted area to start charting it.' : 'What your AI saves will appear here as lights.'; }
  else if (open) { b = `${open.name}: ${goalText(open)}`; s = nd; } else if (M.goals.length && M.goals.every(G => G.reached)) { b = 'Every goal reached.'; s = nd; }
  else { b = `${lit} light${lit === 1 ? '' : 's'} on${M.days < 21 ? '. Your world is taking shape.' : '.'}`; s = M.goals.length ? nd : 'Add a goal with a number to give your world a ring · ' + nd; }
  const html = `<b>${safe(b)}</b><span>${safe(s)}</span>`; if (headEl._h !== html) { headEl._h = html; headEl.innerHTML = html; } }
function caption(c, ms) { clearTimeout(capT); if (!c) { capEl.classList.remove('on'); capOpen = null; return; } capEl.innerHTML = `<small>${safe(c.kicker || '')}</small><b>${safe(c.title)}</b>${c.sub ? `<span>${safe(c.sub)}</span>` : ''}`; capOpen = c.open || null; capEl.classList.toggle('go', !!capOpen); capEl.classList.add('on'); if (ms) capT = setTimeout(() => caption(null), ms); }
function stopShow() { touched = true; if (!show) return; const was = show; show = null; caption(null); if (was.type === 'play') { dirty = true; } playEl.textContent = '▶ Watch it light up'; }
function select(o, fly = true) { if (sel === o) return; sel = o || null; dirty = true; if (o && fly && !show) { if (o.kind === 'task') flyTo(o.land.c, 1.9); else if (o.p) flyTo(o.p, o.kind === 'decision' ? 1.3 : Math.min(cam.to.alt, o.kind === 'finding' ? .42 : .52)); else if (o.kindOf === 'land') flyTo(o.c, clamp(o.rmax * 3.4, .9, 1.6)); else if (o.kind === 'goal') { const fed = M.lands.filter(l => o.lands.includes(l.id)); if (fed.length) { const mid = new THREE.Vector3(); fed.forEach(l => mid.add(l.c)); flyTo(mid.lengthSq() > .01 ? mid.normalize() : fed[0].c, HOME_ALT); cam.to.lat = clamp(cam.to.lat, -.5, .5); } else home();
      ramp = { from: 0, to: S.day, t0: performance.now(), dur: 5200, goal: o.id }; caption({ kicker: fed.length ? 'What feeds this goal' : 'How this goal has moved', title: o.name, sub: fed.length ? `${goalText(o)} · fed by ${fed.map(l => l.name).slice(0, 3).join(', ')}` : `${goalText(o)} · nothing is linked to it yet` }, 5600); } } cb.select?.(sel); }
function tour() { stopShow(); select(null); const top = M.things.slice().sort((a, b) => b.changes - a.changes || b.seen - a.seen)[0], f = M.finds.find(x => !x.need), nd = [...M.things, ...M.finds].find(x => x.need), done = M.goals.filter(G => G.reached).length;
  const steps = [{ kicker: 'Your world', title: `This is ${M.name}.`, sub: 'Everything AURA keeps for you, drawn as one world.' },
    M.goals.length && { kicker: 'Rings', title: 'Each ring is a goal.', sub: `It fills as real progress is recorded. ${done} of ${M.goals.length} ${done === 1 ? 'is' : 'are'} complete.` },
    top && { pos: top.p, alt: .75, kicker: 'Lights', title: 'Each light is something you track.', sub: `This one is ${top.name}, in ${top.land.name}.` },
    f && { pos: f.p, alt: .5, kicker: 'Findings', title: 'Smaller lights are what you have learned.', sub: `“${f.name}”` },
    nd && { pos: nd.p, alt: .8, kicker: 'Amber', title: 'Amber means it needs a look.', sub: nd.name },
    { kicker: 'Yours to explore', title: 'Drag to turn it. Scroll to fly down.', sub: 'Click anything to open it.' }].filter(Boolean);
  show = { type: 'steps', steps, i: -1, stepAt: -1e9, pos: null }; cb.remember?.({ toured: '1' }); }
/* What changed: fly to each thing a check changed since the last visit (or in the last two weeks), newest first. */
function changed() { stopShow(); select(null); flat = false; barEl.querySelector('[data-w=flat]').setAttribute('aria-pressed', 'false'); const f = M.feed, from = sinceT || Date.parse(f.as_of) - 14 * 864e5, seen = new Set(), steps = [];
  for (const c of f.changes) { if (Date.parse(c.at) <= from || steps.length >= 5) continue; const key = c.land + '|' + c.item_id; if (seen.has(key)) continue; seen.add(key); const th = M.things.find(x => x.id === key), l = M.lands.find(z => z.id === c.land); if (!th && !l) continue;
    steps.push({ pos: th ? th.p : l.c, alt: th ? .6 : 1.4, kicker: 'Changed ' + new Date(c.at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }), title: c.title || (l && l.name) || 'A saved result', sub: l ? l.name : '', open: th ? () => select(th) : null }); }
  if (!steps.length) { caption({ kicker: sinceT ? 'Since your last visit' : 'In the last two weeks', title: 'Nothing has changed.' }, 2800); return; } show = { type: 'steps', steps, i: -1, stepAt: -1e9, pos: null }; }
function play() { stopShow(); select(null); S.day = 0; dday = 0; home(); dirty = true; show = { type: 'play', t0: performance.now(), dur: 16000, lon0: cam.to.lon, seen: new Set(), last: 0 }; playEl.textContent = '■ Stop'; caption({ kicker: dateOf(0), title: 'Day one.' }, 2200); }
function stepShow(t) { if (!show) return;
  if (show.type === 'steps') { if (t - show.stepAt > 4400) { show.i++; if (show.i >= show.steps.length) { show = null; caption(null); home(); return; } const s = show.steps[show.i]; show.stepAt = t; show.pos = s.pos || null; s.pos ? flyTo(s.pos, s.alt || .62) : home(); caption({ ...s, kicker: `${s.kicker} · ${show.i + 1} of ${show.steps.length}` }); } return; }
  const u = clamp((performance.now() - show.t0) / show.dur, 0, 1); S.day = M.T * u; dday = S.day; cam.to.lon = show.lon0 + u * TAU * .85; range.value = Math.round(u * 1000);
  for (const G of M.goals) if (!show.seen.has(G.id) && G.reached && gdone(G, S.day) >= 1) { show.seen.add(G.id); caption({ kicker: 'Goal reached', title: G.name }, 3000); }
  if (t - show.last > 200) { show.last = t; dirty = true; }
  if (u >= 1) { show = null; S.day = M.T; dirty = true; playEl.textContent = '▶ Watch it light up'; caption({ kicker: 'Today', title: `${M.things.length} tracked · ${M.finds.length} findings · ${M.goals.filter(G => G.reached).length} of ${M.goals.length} goals reached` }, 5000); } }

/* ------------------------------ Sharing: a still card and a replay clip, with nothing private on them ------------------------------ */
function still(px, alt = 4.4) { const keep = { lon: cam.lon, lat: cam.lat, alt: cam.alt }, pr = renderer.getPixelRatio(); renderer.setPixelRatio(1); renderer.setSize(px, px, false); camera.aspect = 1; applyCam({ lon: HOME, lat: .28, alt });
  const d0 = LU.uDay.value, a0 = LU.uAlt.value, s0 = LU.uScale.value; LU.uDay.value = S.day / Math.max(1, M.T / 140) + 40; LU.uAlt.value = alt; LU.uScale.value = px * .75; M.lands.forEach(l => { U.uR.value[l.i] = l.rto; U.uDim.value[l.i] = 1; }); rings.forEach(R => { ringBuild(R, gdone(R.G, S.day)); R.holder.visible = true; }); renderer.render(scene, camera);
  const c = document.createElement('canvas'); c.width = c.height = px; c.getContext('2d').drawImage(glc, 0, 0, px, px); LU.uDay.value = d0; LU.uAlt.value = a0; LU.uScale.value = s0; renderer.setPixelRatio(pr); fit(); applyCam(keep); rings.forEach(R => { R.built = -1; }); return c; }
const ageWord = () => M.days >= 365 ? `${Math.floor(M.days / 365)} year${M.days >= 730 ? 's' : ''}` : M.days >= 60 ? `${Math.round(M.days / 30)} months` : `${Math.max(1, Math.round(M.days))} day${Math.round(M.days) === 1 ? '' : 's'}`;
function card() { const c = document.createElement('canvas'), w = c.width = 1080, h = c.height = 1350, x = c.getContext('2d'), st = still(1080); x.fillStyle = C.stage; x.fillRect(0, 0, w, h); x.drawImage(st, 0, 20, 1080, 1080); x.textBaseline = 'middle';
  x.fillStyle = C.muted; x.font = `700 22px ${C.font}`; x.letterSpacing = '8px'; x.textAlign = 'left'; x.fillText('AURA', 64, 78); x.textAlign = 'right'; x.letterSpacing = '2px'; x.fillText(dateOf(S.day), w - 64, 78); x.letterSpacing = '0px'; x.textAlign = 'center';
  let size = 68; x.font = `800 ${size}px ${C.font}`; while (x.measureText(M.name).width > w - 120 && size > 34) { size -= 4; x.font = `800 ${size}px ${C.font}`; } x.fillStyle = C.ink; x.fillText(M.name, w / 2, 1084); x.fillStyle = C.muted; x.font = `500 27px ${C.font}`; x.fillText(`${ageWord()} with AURA`, w / 2, 1140);
  const stats = [[M.things.filter(q => q.from <= S.day).length, 'tracked'], [M.finds.filter(q => q.from <= S.day && q.label === 'supported').length, 'findings supported'], M.goals.length ? [`${M.goals.filter(G => G.reached).length} of ${M.goals.length}`, 'goals reached'] : [M.lands.filter(l => !l.unch).length, 'areas charted']];
  stats.forEach(([v, l], i) => { const cx = w / 2 + (i - 1) * 300; x.fillStyle = C.accent; x.font = `800 54px ${C.font}`; x.fillText(String(v), cx, 1232); x.fillStyle = C.muted; x.font = `500 21px ${C.font}`; x.fillText(l, cx, 1280); }); return c; }
function share() { const was = show?.type === 'play'; stopShow(); if (was) { S.day = M.T; dday = M.T; range.value = 1000; } sync(); const c = card(); shareEl.innerHTML = `<div class="world-sharecard"><div class="world-shareimg"></div><div class="world-shareside"><h3>Made to show, safe to post</h3><p>The picture is the real shape of what ${safe(M.name)} knows: every light is something tracked, every ring a goal.</p><p class="small-note">It shows the name, how long it has been built and three numbers. No results, findings or sources are named. Nothing is shared unless you download it and share it yourself.</p><div class="world-shareacts"><button type="button" class="primary" data-w="png">Download image</button><button type="button" class="secondary" data-w="clip">Record replay clip</button><button type="button" class="secondary" data-w="close">Close</button></div></div></div>`;
  shareEl.querySelector('.world-shareimg').appendChild(c); shareEl._c = c; shareEl.hidden = false; }
function poster() { const keep = S.day; S.day = M.T; sync(); const c = card(); S.day = keep; dirty = true; return c; }
const fileName = ext => (M.name || 'aura').replace(/[^\w -]+/g, '').trim() + ' world.' + ext;
function save(blob, name) { const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); }
function clip() { if (!window.MediaRecorder) { caption({ kicker: 'Sharing', title: 'This browser cannot record a clip.' }, 3000); return; } shareEl.hidden = true; const c = document.createElement('canvas'); c.width = c.height = 720; const x = c.getContext('2d'), chunks = [], type = MediaRecorder.isTypeSupported('video/webm;codecs=vp9') ? 'video/webm;codecs=vp9' : 'video/webm', mr = new MediaRecorder(c.captureStream(30), { mimeType: type });
  mr.ondataavailable = e => { if (e.data.size) chunks.push(e.data); }; mr.onstop = () => { save(new Blob(chunks, { type: 'video/webm' }), fileName('webm')); caption({ kicker: 'Sharing', title: 'Your replay clip is saved.' }, 3200); };
  rec = { mr, frame() { const sq = Math.min(glc.width, glc.height); x.fillStyle = C.stage; x.fillRect(0, 0, 720, 720); x.drawImage(glc, (glc.width - sq) / 2, (glc.height - sq) / 2, sq, sq, 0, 0, 720, 720); x.textAlign = 'center'; x.fillStyle = C.ink; x.font = `800 34px ${C.font}`; x.fillText(M.name, 360, 648); x.fillStyle = C.muted; x.font = `500 20px ${C.font}`; x.fillText(`${dateOf(S.day)} · ${M.things.filter(q => q.from <= S.day).length} tracked`, 360, 682); } }; mr.start(); play(); }

/* ------------------------------ Pointer, keys and the frame ------------------------------ */
const at = e => { const r = ui.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };
const under = p => p ? hits.filter(z => p.x >= z.x && p.x <= z.x + z.w && p.y >= z.y && p.y <= z.y + z.h).at(-1) : null;
ui.addEventListener('pointerdown', e => { stopShow(); pd = { x: e.clientX, y: e.clientY, x0: e.clientX, y0: e.clientY }; moved = false; cam.v = [0, 0]; ui.setPointerCapture(e.pointerId); });
ui.addEventListener('pointermove', e => { pointer = at(e); if (!pd) return; const dx = e.clientX - pd.x, dy = e.clientY - pd.y; pd.x = e.clientX; pd.y = e.clientY; if (!moved && Math.hypot(e.clientX - pd.x0, e.clientY - pd.y0) > 5) moved = true; if (!moved) return;
  const k = Math.min(.0062, 2 * TANH * cam.alt / H), dl = -dx * k / Math.max(.35, Math.cos(cam.lat)), da = dy * k; cam.to.lon += dl; cam.lon += dl; cam.to.lat = cam.lat = clamp(cam.lat + da, -1.35, 1.35); cam.v = [clamp(dl, -.02, .02), clamp(da, -.02, .02)]; });
ui.addEventListener('pointerup', e => { if (pd && !moved) { pointer = at(e); const h = under(pointer); select(h ? h.s : null); } pd = null; });
ui.addEventListener('pointerleave', () => { pointer = null; });
ui.addEventListener('wheel', e => { e.preventDefault(); stopShow(); const before = cam.to.alt; cam.to.alt = clamp(cam.to.alt * Math.exp(e.deltaY * .0017), ALT_MIN, ALT_MAX); if (cam.to.alt < before) { const p = pick(e.clientX, e.clientY); if (p) { const [lo, la] = lonlat(p); cam.to.lon += wrap(lo - cam.to.lon) * .2; cam.to.lat = clamp(cam.to.lat + (la - cam.to.lat) * .2, -1.35, 1.35); } } }, { passive: false });
ui.addEventListener('dblclick', e => { const p = pick(e.clientX, e.clientY); if (p && cam.alt > 1) flyTo(p, Math.max(.5, cam.alt * .38)); else home(); });
ui.addEventListener('keydown', e => { const k = { ArrowLeft: [-.12, 0], ArrowRight: [.12, 0], ArrowUp: [0, .1], ArrowDown: [0, -.1] }[e.key]; if (k) { e.preventDefault(); stopShow(); cam.to.lon += k[0]; cam.to.lat = clamp(cam.to.lat + k[1], -1.35, 1.35); } if (e.key === '+' || e.key === '=') cam.to.alt = clamp(cam.to.alt * .75, ALT_MIN, ALT_MAX); if (e.key === '-') cam.to.alt = clamp(cam.to.alt / .75, ALT_MIN, ALT_MAX); if (e.key === 'Home') home(); });
ui.tabIndex = 0; ui.setAttribute('role', 'img');
range.addEventListener('input', () => { stopShow(); S.day = M.T * range.value / 1000; dirty = true; });
barEl.addEventListener('click', e => { const w = e.target.closest('[data-w]')?.dataset.w; if (w === 'play') show?.type === 'play' ? stopShow() : play(); if (w === 'tour') tour(); if (w === 'changed') changed(); if (w === 'flat') { flat = !flat; e.target.closest('[data-w]').setAttribute('aria-pressed', String(flat)); stopShow(); } if (w === 'home') { stopShow(); select(null); home(); } if (w === 'share') share(); });
shareEl.addEventListener('click', e => { const w = e.target.closest('[data-w]')?.dataset.w; if (w === 'close' || e.target === shareEl) shareEl.hidden = true; if (w === 'png') shareEl._c.toBlob(b => save(b, fileName('png')), 'image/png'); if (w === 'clip') clip(); });
capEl.addEventListener('click', () => { if (capOpen) { const o = capOpen; stopShow(); o(); } });
function frame(t) { raf = 0; if (!stage || !stage.isConnected) { stage = null; return; } raf = requestAnimationFrame(frame); const dt = Math.min(50, t - (last || t)); last = t; const r = stage.getBoundingClientRect(); if (Math.abs(r.width - W) > .5 || Math.abs(r.height - H) > .5) fit(); theme(); if (dirty) sync();
  stepShow(t); const k = reduce ? 1 : 1 - Math.pow(.0025, dt / 1000); if (!pd) { cam.to.lon += cam.v[0]; cam.to.lat = clamp(cam.to.lat + cam.v[1], -1.35, 1.35); cam.v[0] *= .92; cam.v[1] *= .92; }
  cam.lon += (cam.to.lon - cam.lon) * k; cam.lat += (cam.to.lat - cam.lat) * k; cam.alt = Math.exp(Math.log(cam.alt) + (Math.log(cam.to.alt) - Math.log(cam.alt)) * k); applyCam();
  if (ramp) { const u = clamp((performance.now() - ramp.t0) / ramp.dur, 0, 1); dday = ramp.from + (ramp.to - ramp.from) * u * u * (3 - 2 * u); if (u >= 1) ramp = null; } else { dday += (S.day - dday) * (reduce ? 1 : 1 - Math.pow(.03, dt / 1000)); if (Math.abs(S.day - dday) < M.T / 1500) dday = S.day; }
  for (const l of M.lands) { U.uR.value[l.i] += (l.rto - U.uR.value[l.i]) * Math.min(1, dt / 260); U.uDim.value[l.i] += (l.dim - U.uDim.value[l.i]) * Math.min(1, dt / 200); }
  /* The preview measured time in days over two years; a young workspace is scaled so its first lights still fade in. */
  const span = Math.max(1, M.T / 140); U.uTime.value = t / 1000; U.uZoom.value = clamp(cam.alt, .18, 3); LU.uDay.value = dday / span + 5 * clamp(dday / M.T, 0, 1); LU.uAlt.value = cam.alt; LU.uScale.value = renderer.getDrawingBufferSize(new THREE.Vector2()).y * .75;
  rings.forEach(R => { const to = gdone(R.G, ramp && ramp.goal === R.G.id ? dday : S.day); R.shown += (to - R.shown) * Math.min(1, dt / 300); ringBuild(R, R.shown); const rf = sstep(1.0, 1.9, cam.alt); R.arc.material.opacity = rf; R.glow.material.opacity = .16 * rf; R.track.material.opacity = (kit ? .35 : .22) * rf; R.holder.visible = rf > .01; });
  running = cb.running?.() || []; { const loose = running.some(r => !r.land); for (const l of M.lands) U.uPulse.value[l.i] = running.some(r => r.land === l.id) ? 1 : loose ? .4 : 0; } glc.style.visibility = flat ? 'hidden' : '';
  if (flat) flatMap(t, dday); else { renderer.render(scene, camera); if (rec) { rec.frame(); if (show?.type !== 'play') { rec.mr.stop(); rec = null; } } overlay(t, dday); }
  const h = pointer && !pd ? under(pointer) : null, was = hov; hov = h ? h.s : null; ui.style.cursor = h ? 'pointer' : moved && pd ? 'grabbing' : 'grab'; if (h && h.tip) { tipEl.innerHTML = `${safe(h.tip[0])}<small>${safe(h.tip[1] || '')}</small>`; tipEl.style.opacity = 1; tipEl.style.left = Math.min(pointer.x + 16, W - 290) + 'px'; tipEl.style.top = Math.min(pointer.y + 16, H - 80) + 'px'; } else tipEl.style.opacity = 0; if (was !== hov) dirty = dirty || false;
  headEl.style.opacity = cam.alt > 3.4 && !show && !sel && shareEl.hidden ? 1 : 0; }

/* ------------------------------ What the rest of AURA calls ------------------------------ */
function mount(host, feed, callbacks = {}) { if (!renderer) return false; cb = callbacks; stage = host; host.replaceChildren(glc, ui, headEl, capEl, tipEl, barEl, shareEl); shareEl.hidden = true; load(feed); fit(); theme(); sync(); applyCam(); ui.setAttribute('aria-label', `${feed.business.name} drawn as a world: ${M.things.length} tracked results and ${M.finds.length} findings across ${M.lands.filter(l => !l.unch).length} areas. The same things are listed beside it.`);
  for (let i = 0; i < M.lands.length; i++) { U.uR.value[i] = M.lands[i].rto; }
  /* Scale birth days for the light shader the same way the frame does. */
  { const span = Math.max(1, M.T / 140), born = lights.geometry.attributes.aBorn; for (let i = 0; i < born.count; i++) born.array[i] /= span; born.needsUpdate = true; }
  if (!raf) raf = requestAnimationFrame(frame);
  const seen = cb.seen || null, toured = !!cb.toured; sinceT = seen ? Date.parse(seen) : 0; F = { lands: null, needs: false }; flat = false; barEl.querySelector('[data-w=flat]').setAttribute('aria-pressed', 'false'); cb.remember?.({ seen: feed.as_of });
  touched = false; if (!reduce && (M.things.length || M.finds.length)) setTimeout(() => { if (touched || show || sel || stage !== host) return; if (!toured) { tour(); return; }
    const since = seen ? Date.parse(seen) : Date.parse(feed.as_of) - 14 * 864e5, recent = feed.changes.filter(c => Date.parse(c.at) > since); if (!recent.length) return; const first = Math.min(...recent.map(c => (Date.parse(c.at) - M.date(0).getTime()) / 864e5));
    ramp = { from: Math.max(0, first - M.T / 60), to: M.T, t0: performance.now(), dur: 2800 }; caption({ kicker: seen ? 'Since your last visit' : 'In the last two weeks', title: `${recent.length} change${recent.length === 1 ? '' : 's'} noticed`, sub: [...new Set(recent.map(c => c.title))].slice(0, 3).join(' · ') }, 5200); }, 1100);
  return true; }
function find(kind, id) { if (!M) return null; return kind === 'land' ? M.lands.find(l => l.id === id) : kind === 'item' ? M.things.find(x => x.id === id) : kind === 'finding' ? M.finds.find(x => x.id === id) : kind === 'goal' ? M.goals.find(x => x.id === id) : kind === 'decision' ? M.decisions.find(x => x.id === id) : kind === 'task' ? M.tasks.find(x => x.id === id) : null; }
window.auraWorld = { available: !!renderer, mount, unmount() { stage = null; cb = {}; if (rec) { try { rec.mr.stop(); } catch {} rec = null; } }, focus(kind, id) { stopShow(); select(find(kind, id)); }, clear() { stopShow(); select(null); home(); }, search(q) { S.q = String(q || '').trim().toLowerCase(); dirty = true; }, filter(f) { F = { lands: f?.lands?.length ? f.lands : null, needs: !!f?.needs }; dirty = true; }, changed, tour, play, share, poster, model: () => M,
  /* For checks only: the cost of drawing one frame, in milliseconds, without waiting for the screen. */
  bench(n = 20) { const t0 = performance.now(); for (let i = 0; i < n; i++) { cancelAnimationFrame(raf); frame(performance.now()); } return (performance.now() - t0) / n; },
  /* For checks only: jump straight to where the camera is heading. */
  settle() { cam.lon = cam.to.lon; cam.lat = cam.to.lat; cam.alt = cam.to.alt; cam.v = [0, 0]; dday = S.day; ramp = null; if (M) for (const l of M.lands) { U.uR.value[l.i] = l.rto; U.uDim.value[l.i] = l.dim; } }, state: () => ({ alt: cam.alt, day: S.day, sel: sel ? { kind: sel.kind || sel.kindOf, id: sel.id } : null, show: show?.type || null, kit, hits: hits.length }) };
document.dispatchEvent(new Event('aura-world-ready'));
