/* Shared resizing: pointer cancellation, keyboard access, bounds and saved preferences. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2],'utf8'),nodes=new Map(),styles={},classes=new Set(),saves=[],errors=[];
const state={profile:{sidebar_width:null,panel_width:480,sidebar_collapsed:false},data:{profile:{sidebar_width:null,panel_width:480}}};
function element(id){
  if(!nodes.has(id))nodes.set(id,{hidden:false,dataset:{},open:false,attributes:{},listeners:{},capture:null,
    setAttribute(k,v){this.attributes[k]=v;},addEventListener(k,fn){this.listeners[k]=fn;},focus(){},
    setPointerCapture(id){this.capture=id;},hasPointerCapture(id){return this.capture===id;},releasePointerCapture(){this.capture=null;},
    getBoundingClientRect(){const nav=state.profile.sidebar_collapsed?74:parseFloat(styles['--sidebar-width'])||252;return {width:id==='#sidebar'?nav:Math.min(parseFloat(styles['--panel-width'])||480,Math.max(360,context.innerWidth-nav-420))};}
  });return nodes.get(id);
}
let observer,resize;
class MutationObserver{constructor(fn){observer=fn;}observe(){}}
const context=vm.createContext({state,$:element,innerWidth:1600,Math,Promise,Object,MutationObserver,
  window:{addEventListener(type,fn){if(type==='resize')resize=fn;}},
  document:{documentElement:{style:{setProperty(k,v){styles[k]=v;},removeProperty(k){delete styles[k];}}},body:{classList:{add(k){classes.add(k);},remove(k){classes.delete(k);}}}},
  api:async(path,data)=>{saves.push(data);if(context.fail)throw new Error('Save failed');return {...state.data.profile,...data};},humanError:e=>e.message,notice:message=>errors.push(message)});
vm.runInContext(source.slice(source.indexOf('const panelWidthOverrides='),source.indexOf('async function renderShell(')),context);
const fire=(id,type,extra={})=>element(id).listeners[type]({button:0,pointerId:1,clientX:252,preventDefault(){},...extra});
const flush=()=>vm.runInContext('panelWidthSave',context);
(async()=>{
  context.syncPanelSizes();assert.equal(styles['--sidebar-width'],undefined);
  assert.equal(element('#detail-resize').hidden,true);
  const detail=element('#detail');detail.open=true;detail.dataset.mode='context';observer();assert.equal(element('#detail-resize').hidden,false);
  fire('#sidebar-resize','pointerdown');fire('#sidebar-resize','pointermove',{clientX:340});
  assert.equal(state.profile.sidebar_width,340);assert.equal(saves.length,0,'Dragging must not send a request per pixel');
  fire('#sidebar-resize','pointerup');await flush();assert.equal(saves.length,1);assert.equal(state.data.profile.sidebar_width,340);assert.equal(classes.has('panel-resizing'),false);
  fire('#sidebar-resize','pointerdown',{clientX:340});fire('#sidebar-resize','pointermove',{clientX:9999});assert.equal(state.profile.sidebar_width,420);
  fire('#sidebar-resize','pointercancel');assert.equal(state.profile.sidebar_width,340);assert.equal(saves.length,1,'Cancelled drags must not save');
  fire('#detail-resize','keydown',{key:'ArrowLeft'});await flush();assert.equal(state.data.profile.panel_width,496,'Moving the right edge handle left must widen the panel');
  fire('#sidebar-resize','keydown',{key:'Home'});await flush();assert.equal(state.data.profile.sidebar_width,180);
  fire('#sidebar-resize','dblclick');await flush();assert.equal(state.data.profile.sidebar_width,null);assert.equal(styles['--sidebar-width'],undefined);
  fire('#detail-resize','dblclick');await flush();assert.equal(state.data.profile.panel_width,480);
  detail.dataset.expanded='true';observer();assert.equal(element('#detail-resize').hidden,true);delete detail.dataset.expanded;
  detail.dataset.mode='panel';observer();assert.equal(element('#detail-resize').hidden,true);detail.dataset.mode='context';
  state.profile.sidebar_collapsed=true;context.syncPanelSizes();assert.equal(element('#sidebar-resize').hidden,true);state.profile.sidebar_collapsed=false;
  context.setPanelSize('sidebar',420);context.innerWidth=650;resize();assert.equal(styles['--sidebar-width'],'230px','Small windows constrain display without losing the preferred width');assert.equal(state.profile.sidebar_width,420);
  context.innerWidth=390;resize();assert.equal(element('#sidebar-resize').hidden,true);assert.equal(element('#detail-resize').hidden,true);
  context.innerWidth=1600;resize();assert.equal(styles['--sidebar-width'],'420px');
  context.fail=true;context.savePanelSize('sidebar',context.setPanelSize('sidebar',320));await flush();assert.equal(state.profile.sidebar_width,null);assert.deepEqual(errors,['Save failed']);
  console.log('Panel resizing passed: pointer save/cancel, keyboard, reset, responsive bounds, shared visibility and save failure recovery.');
})().catch(error=>{console.error(error);process.exitCode=1;});
