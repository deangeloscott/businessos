/* Exercise shipped floating-surface behavior: viewport bounds and lifecycle, without another dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2],'utf8'),listeners={},viewportListeners={};
const state={data:{workspace:'fixture'},business:'business',view:'home',chatMeta:null,home:true};
const viewport={width:800,height:600,offsetLeft:0,offsetTop:0,addEventListener:(type,fn)=>viewportListeners[type]=fn};
let focus=null,observer;
function element(id,rect={left:300,top:100,width:30,height:30}){
  return {id,rect,isConnected:true,open:false,dataset:{},attributes:{},parentNode:null,nextSibling:null,naturalHeight:250,inert:false,
    style:{removeProperty(key){delete this[key.replace(/-([a-z])/g,(_,c)=>c.toUpperCase())];}},
    setAttribute(key,value){this.attributes[key]=value;},getAttribute(key){return this.attributes[key]??null;},
    closest(selector){return selector==='[inert]'&&this.inert?{}:null;},
    focus(){focus=this;},show(){this.open=true;},close(){this.open=false;},
    getBoundingClientRect(){const r=this.rect;if(!this.open&&id.startsWith('panel'))return {left:0,top:0,right:0,bottom:0,width:0,height:0};
      const width=parseFloat(this.style.width)||r.width,height=this.open?Math.min(this.naturalHeight,parseFloat(this.style.maxHeight)??Infinity):r.height;
      const left=parseFloat(this.style.left)??r.left,top=parseFloat(this.style.top)??r.top;
      return {left:Number.isNaN(left)?r.left:left,top:Number.isNaN(top)?r.top:top,width,height,right:(Number.isNaN(left)?r.left:left)+width,bottom:(Number.isNaN(top)?r.top:top)+height};}
  };
}
class ResizeObserver{constructor(callback){this.callback=callback;this.disconnected=false;this.observed=[];observer=this;}observe(el){this.observed.push(el);}disconnect(){this.disconnected=true;}}
const context=vm.createContext({state,window:{visualViewport:viewport,addEventListener(){}},innerWidth:800,innerHeight:600,ResizeObserver,
  document:{addEventListener(type,fn){(listeners[type]??=[]).push(fn);}},JSON,Date,Math});
vm.runInContext(source.slice(source.indexOf('let anchoredSurface=null;'),source.indexOf('function setDetailBack('))+'\nthis.ui={openAnchoredSurface,closeAnchoredSurface,positionAnchoredSurface};',context);
const ui=context.ui;
function open(rect,options={}){const anchor=element('anchor',rect),panel=element('panel');assert.equal(ui.openAnchoredSurface(panel,anchor,options),true);return {anchor,panel};}
function bounded(panel){const r=panel.getBoundingClientRect();assert.ok(r.left>=viewport.offsetLeft+12-0.1,JSON.stringify(r));assert.ok(r.right<=viewport.offsetLeft+viewport.width-12+0.1,JSON.stringify(r));assert.ok(r.top>=viewport.offsetTop+12-0.1,JSON.stringify(r));assert.ok(r.bottom<=viewport.offsetTop+viewport.height-12+0.1,JSON.stringify(r));}

let current=open({left:740,top:35,width:35,height:30},{width:340,align:'end'});
bounded(current.panel);assert.ok(current.panel.getBoundingClientRect().top>=current.anchor.getBoundingClientRect().bottom+8,'A trigger near the top must open downward');
assert.equal(current.anchor.attributes['aria-expanded'],'true');
current=open({left:4,top:550,width:35,height:30},{width:340});
bounded(current.panel);assert.ok(current.panel.getBoundingClientRect().bottom<=542,'A trigger near the bottom must open upward');
current.panel.naturalHeight=1500;observer.callback();bounded(current.panel);assert.ok(parseFloat(current.panel.style.maxHeight)<1500,'Tall contents must be scroll-constrained');

viewport.width=320;viewport.height=240;viewport.offsetLeft=25;viewport.offsetTop=70;
current=open({left:300,top:160,width:25,height:30},{width:420});bounded(current.panel);
assert.equal(parseFloat(current.panel.style.width),296,'Narrow screens must constrain width');
assert.ok(current.panel.getBoundingClientRect().height>=180,'Short windows must retain a usable scrolling area instead of a tiny strip');
current=open({left:300,top:280,width:25,height:20},{width:420,placement:'side'});bounded(current.panel);
viewport.width=800;viewport.height=600;viewport.offsetLeft=viewport.offsetTop=0;

for(const [object,key,value] of [[state,'view','business'],[state,'business','another'],[state.data,'workspace','another'],[state,'chatMeta',{id:'another'}],[state,'home',false]]){
  current=open({left:300,top:100,width:30,height:30});const old=object[key],observed=observer;
  object[key]=value;ui.positionAnchoredSurface();assert.equal(current.panel.open,false,`Changing ${key} must close the old surface`);
  assert.equal(current.anchor.attributes['aria-expanded'],'false');assert.equal(observed.disconnected,true);object[key]=old;
}
for(const change of [anchor=>anchor.isConnected=false,anchor=>anchor.inert=true,anchor=>anchor.rect.left=-100,anchor=>anchor.rect.top=900]){
  current=open({left:300,top:100,width:30,height:30});change(current.anchor);ui.positionAnchoredSurface();assert.equal(current.panel.open,false,'An unavailable trigger must dismiss its surface');
}
const unavailable=element('anchor',{left:100,top:100,width:0,height:0}),unopened=element('panel');
assert.equal(ui.openAnchoredSurface(unopened,unavailable),false);assert.equal(observer.observed.length,0,'A dismissed surface must not restart observation');
current=open({left:300,top:100,width:30,height:30});const previous=current;
current=open({left:500,top:100,width:30,height:30});assert.equal(previous.panel.open,false,'Only one anchored surface may remain open');
assert.equal(previous.anchor.attributes['aria-expanded'],'false');
let prevented=false;
listeners.keydown[0]({key:'Escape',preventDefault(){prevented=true;},stopImmediatePropagation(){}});
assert.equal(current.panel.open,false);assert.equal(focus,current.anchor);assert.equal(prevented,true);
assert.equal(typeof viewportListeners.scroll,'function','Visual viewport scrolling must reposition surfaces');
assert.equal(typeof viewportListeners.resize,'function','Visual viewport resizing must reposition surfaces');
console.log('Floating surfaces passed: upward/downward/side placement, narrow and short viewports, growing content, navigation scope, unavailable triggers, replacement, and Escape.');
