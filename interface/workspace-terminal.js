/* Built-in terminals: a real shell on this computer, shown with xterm.js in a dock under the work area.
   Terminals keep running while you move around AURA and end when AURA stops. Output reaches the AI only when you add it to a chat. */
window.auraTerminal=(()=>{
  const tabs=new Map();let active='',lib=null,fitTimer=0;
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
    host.innerHTML=[...tabs.values()].map(t=>`<span class="terminal-tab ${t.id===active?'active':''}"><button type="button" class="terminal-tab-name" data-terminal-tab="${esc(t.id)}" aria-pressed="${t.id===active}" title="${esc(t.info.cwd)}">${esc(t.info.title)}${t.ended?' · Ended':''}</button><button type="button" class="terminal-tab-close" data-terminal-close="${esc(t.id)}" aria-label="Close ${esc(t.info.title)}" title="Close">×</button></span>`).join('');
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
  async function pump(t){
    // Long polling over AURA's token-protected local API; no extra service or socket.
    while(tabs.has(t.id)){
      let r;try{r=await api(`/api/terminal/output?id=${encodeURIComponent(t.id)}&since=${t.offset}&wait=20`);}
      catch(error){if(!tabs.has(t.id))return;t.term.write(`\r\n\x1b[2m[${humanError(error)}]\x1b[0m\r\n`);t.ended=true;paintTabs();return;}
      if(!tabs.has(t.id))return;
      if(r.reset)t.term.reset();
      if(r.data)t.term.write(r.data);
      t.offset=r.offset;
      if(!r.alive){t.ended=true;t.term.write(`\r\n\x1b[2m[Ended${r.exit_code!=null?' · exit code '+r.exit_code:''}]\x1b[0m\r\n`);paintTabs();return;}
    }
  }
  async function create(){
    // The screen is drawn and measured first, so the program starts at the size it will be shown at.
    const {Terminal,FitAddon}=await library();
    const host=document.createElement('div');host.className='terminal-screen';$('#terminal-screens').append(host);
    for(const other of tabs.values())other.host.hidden=true;
    const term=new Terminal({cursorBlink:true,fontFamily:'ui-monospace, "Cascadia Mono", Consolas, "SF Mono", Menlo, monospace',fontSize:13,lineHeight:1.15,
                             theme:theme(),scrollback:5000,allowProposedApi:false,convertEol:false});
    const fitAddon=new FitAddon();term.loadAddon(fitAddon);withNonce(()=>term.open(host));
    try{fitAddon.fit();}catch{}
    return {term,fit:fitAddon,host,discard(){term.dispose();host.remove();}};
  }
  async function attach(info,ui=null){
    // A terminal just started at the measured size needs no resize; a reattached one is resized to this screen.
    const started=!!ui;ui=ui||await create();
    const {term,fit:fitAddon,host}=ui;host.dataset.terminal=info.id;
    const t={id:info.id,info,term,fit:fitAddon,host,offset:0,ended:!info.alive,cols:started?term.cols:0,rows:started?term.rows:0,pending:'',sending:null};
    term.onData(data=>{
      if(t.ended)return;t.pending+=data;
      // Typing is batched briefly so a fast typist does not send one request per key.
      clearTimeout(t.sending);t.sending=setTimeout(()=>{const chunk=t.pending;t.pending='';api('/api/terminal',{action:'input',id:t.id,data:chunk}).catch(error=>notice(humanError(error),true));},12);
    });
    tabs.set(t.id,t);select(t.id);pump(t);return t;
  }
  function show(){
    const d=dock();if(!d)return;d.hidden=false;document.body.classList.add('terminal-open');
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
    tabs.delete(id);t.term.dispose();t.host.remove();
    api('/api/terminal',{action:'remove',id}).catch(()=>{});
    if(active===id){const next=[...tabs.keys()].pop();if(next)select(next);else{active='';paintTabs();hide();}}else paintTabs();
  }
  function share(){
    const t=tabs.get(active);if(!t)return;
    if(window.auraCompose?.add({kind:'terminal',id:t.id,label:'Terminal output'})){returnToChat();notice('Terminal output added. Your AI sees the latest output when you send.');}
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
  window.addEventListener('resize',()=>{clearTimeout(fitTimer);fitTimer=setTimeout(()=>fit(tabs.get(active)),80);});
  new MutationObserver(()=>{for(const t of tabs.values())withNonce(()=>{t.term.options.theme=theme();});}).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme','data-style','data-accent']});
  if(window.ResizeObserver)new ResizeObserver(()=>fit(tabs.get(active))).observe(document.getElementById('terminal-screens')||document.body);
  return {open,attachExisting,hide,show,share};
})();
