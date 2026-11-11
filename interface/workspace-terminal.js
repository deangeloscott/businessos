/* Built-in terminals: a real shell on this computer, shown with xterm.js in a dock under the work area.
   Terminals keep running while you move around AURA and end when AURA stops. Output reaches the AI only when you add it to a chat. */
window.auraTerminal=(()=>{
  const tabs=new Map();let active='',lib=null,fitTimer=0,streaming=false,waiting=null;
  const dock=()=>$('#terminal-dock');
  const css=href=>{if(!document.querySelector(`link[href="${href}"]`)){const el=document.createElement('link');el.rel='stylesheet';el.href=href;document.head.append(el);}};
  async function library(){
    if(lib)return lib;css('/vendor/terminal-view.css');lib=await import('/vendor/terminal-view.js');return lib;
  }
  function withNonce(fn){
    // xterm.js draws with a few style elements. AURA's policy allows page styles only with its nonce, so styles
    // created while a terminal opens receive it; nothing else on the page changes.
    const nonce=document.querySelector('meta[name="aura-token"]')?.content,original=document.createElement;
    document.createElement=function(tag,options){const el=original.call(document,tag,options);if(nonce&&String(tag).toLowerCase()==='style')el.nonce=nonce;return el;};
    try{return fn();}finally{document.createElement=original;}
  }
  function theme(){
    const s=getComputedStyle(document.documentElement),v=name=>s.getPropertyValue(name).trim();
    return {background:v('--surface')||'#1e1e1e',foreground:v('--ink')||'#e6e6e6',cursor:v('--accent')||'#e6e6e6',cursorAccent:v('--surface'),
            selectionBackground:v('--accent-soft')||'rgba(127,127,127,.35)'};
  }
  function folderName(path){return String(path||'').split(/[\\/]/).filter(Boolean).pop()||path||'';}
  function paintTabs(){
    const host=$('#terminal-tabs');if(!host)return;
    host.innerHTML=[...tabs.values()].map(t=>`<span class="terminal-tab ${t.id===active?'active':''}"><button type="button" class="terminal-tab-name" data-terminal-tab="${esc(t.id)}" aria-pressed="${t.id===active}" title="${esc(t.info.cwd)}">${esc(t.info.title)}${t.ended?' · Ended':t.disconnected?' · Reconnecting':''}</button><button type="button" class="terminal-tab-close" data-terminal-close="${esc(t.id)}" aria-label="Close ${esc(t.info.title)}" title="Close">×</button></span>`).join('');
    const t=tabs.get(active);$('#terminal-place').textContent=t?folderName(t.info.cwd):'';
    $('#terminal-share').disabled=!t;
  }
  function select(id){
    active=id;for(const t of tabs.values())t.host.hidden=t.id!==id;paintTabs();
    const t=tabs.get(id);if(t){fit(t);t.term.focus();}
  }
  function fit(t){
    if(!t||dock().hidden||t.host.hidden)return;
    try{t.fit.fit();}catch{return;}
    if(t.term.cols!==t.cols||t.term.rows!==t.rows){t.cols=t.term.cols;t.rows=t.term.rows;if(!t.ended)api('/api/terminal',{action:'resize',id:t.id,cols:t.cols,rows:t.rows}).catch(()=>{});}
  }
  function ended(t,code,reason=''){
    t.ended=true;t.term.write(`\r\n\x1b[2m[${reason||('Ended'+(code!=null?' · exit code '+code:''))}]\x1b[0m\r\n`);paintTabs();
  }
  function restream(){waiting?.abort();if(!streaming)stream();}
  async function stream(){
    // One long-polling connection carries every terminal's output over AURA's token-protected local API.
    // Browsers allow only about six connections per address, so a connection per tab would stall the page.
    streaming=true;let failures=0;
    try{
      while(true){
        const live=[...tabs.values()].filter(t=>!t.ended);if(!live.length)return;
        const controller=new AbortController();waiting=controller;let r;
        try{r=await api('/api/terminal/output?streams='+live.map(t=>encodeURIComponent(t.id)+':'+t.offset).join(',')+'&wait=20',undefined,{signal:controller.signal});failures=0;}
        catch(error){
          if(controller.signal.aborted)continue;
          for(const t of live)t.disconnected=true;
          paintTabs();
          await new Promise(resolve=>setTimeout(resolve,Math.min(5000,1000*++failures)));
          continue;
        }finally{if(waiting===controller)waiting=null;}
        if(live.some(t=>t.disconnected)){for(const t of live)t.disconnected=false;paintTabs();}
        for(const item of r.items||[]){
          const t=tabs.get(item.id);if(!t||t.ended)continue;
          if(item.gone){ended(t,null,'This terminal is no longer available');continue;}
          if(item.reset)t.term.reset();
          if(item.data)t.term.write(item.data);
          t.offset=item.offset;
          if(!item.alive)ended(t,item.exit_code);
        }
      }
    }finally{streaming=false;}
  }
  async function create(){
    // The screen is drawn and measured first, so the program starts at the size it will be shown at.
    const {Terminal,FitAddon}=await library();
    const host=document.createElement('div');host.className='terminal-screen';$('#terminal-screens').append(host);
    for(const other of tabs.values())other.host.hidden=true;
    const term=new Terminal({cursorBlink:true,fontFamily:'ui-monospace, "Cascadia Mono", Consolas, "SF Mono", Menlo, monospace',fontSize:13,lineHeight:1.15,
                             theme:theme(),scrollback:5000,allowProposedApi:false,convertEol:false});
    const fitAddon=new FitAddon();term.loadAddon(fitAddon);withNonce(()=>term.open(host));
    // Ctrl+` belongs to AURA (show or hide the terminal), so the shell does not also receive it.
    term.attachCustomKeyEventHandler(event=>!(event.ctrlKey&&event.key==='`'));
    try{fitAddon.fit();}catch{}
    return {term,fit:fitAddon,host,discard(){term.dispose();host.remove();}};
  }
  async function attach(info,ui=null){
    // A terminal just started at the measured size needs no resize; a reattached one is resized to this screen.
    const started=!!ui;ui=ui||await create();
    const {term,fit:fitAddon,host}=ui;host.dataset.terminal=info.id;
    const t={id:info.id,info,term,fit:fitAddon,host,offset:0,ended:!info.alive,cols:started?term.cols:0,rows:started?term.rows:0,pending:'',sending:null};
    term.onData(data=>{
      if(t.ended||t.disconnected)return;t.pending+=data;
      // Typing is batched briefly so a fast typist does not send one request per key.
      clearTimeout(t.sending);t.sending=setTimeout(()=>{const chunk=t.pending;t.pending='';api('/api/terminal',{action:'input',id:t.id,data:chunk}).catch(error=>notice(humanError(error),true));},12);
    });
    tabs.set(t.id,t);select(t.id);restream();return t;
  }
  const HEIGHT_KEY='aura-terminal-height';
  function setHeight(px,save=false){
    const d=dock();if(!d)return;const h=Math.round(Math.max(140,Math.min(window.innerHeight*.8,px)));d.style.height=h+'px';
    if(save)try{localStorage.setItem(HEIGHT_KEY,String(h));}catch{}
    fit(tabs.get(active));
  }
  function savedHeight(){try{return Number(localStorage.getItem(HEIGHT_KEY))||0;}catch{return 0;}}
  function show(){
    const d=dock();if(!d)return;d.hidden=false;document.body.classList.add('terminal-open');
    const h=savedHeight();if(h)setHeight(h);
    const t=tabs.get(active);if(t)requestAnimationFrame(()=>fit(t));
  }
  function hide(){const d=dock();if(d){d.hidden=true;document.body.classList.remove('terminal-open');}}
  async function open(options={}){
    show();
    if(!tabs.size){try{const list=await api('/api/terminals');for(const info of list.items||[])if(!tabs.has(info.id)&&info.alive)await attach(info);}catch{}}
    if(options.existing&&tabs.has(options.existing)){select(options.existing);return tabs.get(options.existing);}
    if(options.reuse&&tabs.size&&!options.command&&!options.chat_id){select(active||[...tabs.keys()][0]);return tabs.get(active);}
    const ui=await create();let info;
    try{info=await api('/api/terminal',{business:state.business,action:'start',command:options.command||'shell',chat_id:options.chat_id||'',cols:ui.term.cols,rows:ui.term.rows});}
    catch(error){ui.discard();if(!tabs.size)hide();else select(active);throw error;}
    return attach(info,ui);
  }
  async function attachExisting(id){
    show();
    if(tabs.has(id)){select(id);return;}
    const list=await api('/api/terminals');const info=(list.items||[]).find(i=>i.id===id);if(info)await attach(info);
  }
  async function close(id){
    const t=tabs.get(id);if(!t)return;
    if(!t.ended&&!confirm(`Close “${t.info.title}”? Anything running in it stops.`))return;
    if(!t.ended){
      try{await api('/api/terminal',{action:'remove',id});}
      catch(error){notice(humanError(error),true);return;}
    }else{api('/api/terminal',{action:'remove',id}).catch(()=>{});}
    clearTimeout(t.sending);tabs.delete(id);t.term.dispose();t.host.remove();restream();
    if(active===id){const next=[...tabs.keys()].pop();if(next)select(next);else{active='';paintTabs();hide();}}else paintTabs();
  }
  function share(){
    const t=tabs.get(active);if(!t)return;
    const buffer=t.term.buffer.active;
    const lines=[];
    let length=0;
    const last=Math.min(buffer.length,buffer.viewportY+t.term.rows)-1;
    for(let i=last;i>=0&&length<6000;i--){
      const line=buffer.getLine(i);
      if(!line)continue;
      const text=line.translateToString(true);
      if(!lines.length&&!text)continue;
      lines.push({text,wrapped:line.isWrapped});length+=text.length+1;
    }
    const snapshot=t.term.getSelection()||lines.reverse().map((line,i)=>(i&&!line.wrapped?'\n':'')+line.text).join('');
    if(!snapshot.trim()){notice('There is no terminal output to add.');return;}
    const excerpt=Array.from(snapshot).slice(-6000).join('');
    if(window.auraCompose?.add({kind:'terminal',id:t.id,request_id:crypto.randomUUID(),label:'Terminal output',snapshot:excerpt})){
      returnToChat();notice('Terminal output attached. Select the attachment to review it.');
    }
  }
  document.addEventListener('click',event=>{
    const b=event.target.closest('[data-terminal-tab],[data-terminal-close],#terminal-new,#terminal-hide,#terminal-share,[data-terminal-run]');if(!b)return;
    if(b.dataset.terminalTab)select(b.dataset.terminalTab);
    if(b.dataset.terminalClose)close(b.dataset.terminalClose);
    if(b.id==='terminal-new')attempt(()=>open());
    if(b.id==='terminal-hide')hide();
    if(b.id==='terminal-share')share();
    if(b.dataset.terminalRun)attempt(()=>open({command:b.dataset.terminalRun}));
  });
  document.addEventListener('keydown',event=>{
    if(event.ctrlKey&&!event.altKey&&!event.metaKey&&event.key==='`'){event.preventDefault();if(dock()?.hidden)attempt(()=>open({reuse:true}));else hide();}
  });
  document.addEventListener('pointerdown',event=>{
    // Drag the dock's top edge; the height is remembered on this computer.
    if(event.target.id!=='terminal-resize')return;event.preventDefault();
    const start=event.clientY,height=dock().getBoundingClientRect().height,handle=event.target;try{handle.setPointerCapture(event.pointerId);}catch{}
    const move=e=>setHeight(height+(start-e.clientY));
    const up=e=>{handle.removeEventListener('pointermove',move);handle.removeEventListener('pointerup',up);setHeight(height+(start-e.clientY),true);};
    handle.addEventListener('pointermove',move);handle.addEventListener('pointerup',up);
  });
  document.addEventListener('keydown',event=>{
    if(event.target.id!=='terminal-resize'||!['ArrowUp','ArrowDown'].includes(event.key))return;event.preventDefault();
    setHeight(dock().getBoundingClientRect().height+(event.key==='ArrowUp'?24:-24),true);
  });
  window.addEventListener('resize',()=>{clearTimeout(fitTimer);fitTimer=setTimeout(()=>fit(tabs.get(active)),80);});
  new MutationObserver(()=>{for(const t of tabs.values())withNonce(()=>{t.term.options.theme=theme();});}).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme','data-style','data-accent']});
  if(window.ResizeObserver)new ResizeObserver(()=>fit(tabs.get(active))).observe(document.getElementById('terminal-screens')||document.body);
  return {open,attachExisting,hide,show,share};
})();
