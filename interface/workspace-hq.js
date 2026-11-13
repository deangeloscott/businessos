/* Home: the business at a glance, under the message box. It only draws /api/summary (the CLI returns the
   same data), so every number is a count of saved records and every row opens the record behind it.
   Sections appear as real work fills them; nothing is shown as a placeholder for work that has not happened. */
window.auraHQ=(()=>{
  let data=null,key='',loadedAt=0,pending=null,pendingKey='';
  const FRESH_MS=30000;
  const scope=()=>JSON.stringify([state.business,state.data?.workspace]);
  const visible=()=>!!state.business&&!!state.home&&state.view==='home'&&!state.chatMeta&&!(state.chat||[]).length&&!state.busy&&!document.querySelector('#view .setup-intro');

  /* Each area gets one plain first step. It only fills the message box; nothing runs until you send. */
  const AREA_START={
    'competitor-intelligence':'Research our main competitors and tell me what actually matters. Save what you find.',
    'customer-intelligence':'Research what our customers need, what stops them buying, and the words they use. Save what you find.',
    'industry-intelligence':'Find the recent news, rules and changes in our industry that could affect us. Save what matters.',
    'seo-aeo':'Check how we show up in search and in AI answers, and list the most valuable fixes.',
    'content-synthesis':'Plan useful content for our audience from what we know, and draft the first piece.',
    'marketing-synthesis':'Review our offer and messaging, and suggest the strongest improvements.',
    'customer-optimization':'Find where customers drop off between their first visit and a repeat purchase, and what to fix first.',
    'funding-impact':'Find grants or funding we are eligible for and likely to win. Save a shortlist with deadlines.',
    'core':'What should we work on next? Use our saved context and separate evidence from assumptions.'};
  const RESEARCH='Research our business and fill in what you know about it. Start from our website: [paste your web address]. Find what we offer, who we serve, our main competitors and the claims we make, each with its source. Save what you find, keep unknowns as unknown, and tell me what you saved.';
  const STATUS=[['supported','Supported',''],['unverified','Unverified','unverified'],['challenged','Challenged','challenged'],['needs_review','Needs review','review'],['out_of_date','Out of date','review']];
  const CHANGE={new:['New',''],changed:['Changed','review'],closed:['Closed','unverified'],superseded:['Replaced','unverified'],challenged:['Challenged','challenged']};
  const HUES={'local-business':150,'multiple-locations':105,'ecommerce':212,'services-b2b':258,'nonprofit':342,'grants':42,'membership-community':300,'startup':18,'research':190,'creative-content':322};

  const when=value=>{
    if(!value)return 'Not checked yet';
    const date=new Date(value),now=new Date(),days=Math.floor((new Date(now.getFullYear(),now.getMonth(),now.getDate())-new Date(date.getFullYear(),date.getMonth(),date.getDate()))/86400000);
    if(Number.isNaN(date.getTime()))return '';
    const time=date.toLocaleTimeString(undefined,{hour:'numeric',minute:'2-digit'});
    return days<=0?'Today '+time:days===1?'Yesterday '+time:days<7?date.toLocaleDateString(undefined,{weekday:'short'}):stamp(value);
  };
  const number=value=>typeof value==='number'?value.toLocaleString(undefined,{maximumFractionDigits:2}):'';
  const measure=(value,unit)=>value===null||value===undefined?'':unit==='USD'?'$'+number(value):number(value);
  const hue=id=>id in HUES?HUES[id]:[...id].reduce((sum,c)=>(sum*31+c.charCodeAt(0))%360,7);
  const share=k=>k.reviewed.with_date?k.reviewed.recent/k.reviewed.with_date:null;

  async function load(force=false){
    if(!state.business)return null;
    const k=scope()+'|'+(state.data?.records_revision||'');
    if(!force&&data&&key===k&&Date.now()-loadedAt<FRESH_MS)return data;
    if(pending&&pendingKey===k)return pending;  // several redraws while one read is in flight share it
    const asked=scope();pendingKey=k;
    pending=api('/api/summary?business='+encodeURIComponent(state.business))
      .then(result=>{if(asked!==scope())return null;data=result;key=k;loadedAt=Date.now();return data;})
      .finally(()=>{if(pendingKey===k)pending=null;});
    return pending;
  }

  /* The aura is drawn only from saved state, and every trait can be explained. */
  function aura(s,size=''){
    const hues=s.focus.map(a=>hue(a.id)).slice(0,3),fresh=share(s.knowledge),working=s.running.length>0,challenged=s.knowledge.by_status.challenged;
    const style=[hues.length?`--hq-h1:${hues[0]};--hq-h2:${hues[1]??(hues[0]+40)%360};--hq-h3:${hues[2]??(hues[0]+320)%360}`:'',`--hq-glow:${fresh===null?.5:(.35+.65*fresh).toFixed(2)}`].filter(Boolean).join(';');
    return `<button type="button" class="hq-aura ${size} ${hues.length?'':'plain'} ${working?'working':''} ${challenged?'unsettled':''}" style="${style}" data-hq-aura aria-label="Your aura. Open what it shows." title="What this shows"><span aria-hidden="true"></span></button>`;
  }
  function explain(){
    if(!data)return;
    const s=data,k=s.knowledge,fresh=share(k),by=k.by_status;
    const row=(name,value,why)=>`<div class="field"><strong>${esc(name)}</strong><p>${esc(value)}</p><p class="small-note">${esc(why)}</p></div>`;
    details('Your aura',`<p class="shell-help">A picture of this business drawn only from what is saved. It shows how things stand without showing the details, so it is safe to share.</p>
      ${row('Colour',s.focus.length?s.focus.map(a=>a.name).join(', '):'No focus areas chosen yet','Each focus area you chose adds its own colour.')}
      ${row('Brightness',fresh===null?'Not shown yet':`${k.reviewed.recent} of ${k.reviewed.with_date} findings reviewed in the last ${k.reviewed.within_days} days`,fresh===null?'It brightens once findings record when they were last reviewed.':'Brighter means more of what you know was checked recently.')}
      ${row('Broken ring',by.challenged?`${by.challenged} challenged finding${by.challenged===1?'':'s'}`:'None','The ring breaks when new evidence challenges something you believed.')}
      ${row('Movement',s.running.length?`${s.running.length} request${s.running.length===1?'':'s'} working now`:'Still','It moves only while your AI is working on this business.')}
      <div class="inline-actions"><button type="button" class="secondary" data-view="business">Open Business &amp; memory</button></div>`,'context');
  }

  function head(s){
    const b=s.business;
    return `<header class="hq-card hq-head">${aura(s)}<div class="hq-identity">${b.example?'<p class="hq-example"><span class="source-chip review">Example business</span> Everything here is made up, so you can look around freely. Your own workspaces are in the list at the top left.</p>':''}<h2>${esc(b.name)}</h2>${b.description?`<p class="hq-description">${esc(b.description)}</p>`:'<p class="hq-description"><button type="button" class="text-button" data-action="edit-business">Say what your business does</button> to get suggestions that fit.</p>'}${s.focus.length?`<div class="focus-chips">${s.focus.map(a=>`<span class="focus-chip">${esc(a.name)}</span>`).join('')}</div>`:''}</div></header>`;
  }
  const tile=(title,body,extra='',cls='')=>`<section class="hq-card hq-tile ${cls}"><div class="hq-tile-head"><h3>${esc(title)}</h3>${extra}</div>${body}</section>`;
  const open=c=>c.collection_id?`data-collection="${esc(c.collection_id)}"`:`data-record="${esc(c.record)}"`;

  function changed(s){
    if(!s.changes.length)return '';
    return tile(`What changed · last ${s.changes_days} days`,`<div class="hq-list">${s.changes.map(c=>{const [label,cls]=CHANGE[c.kind]||[human(c.kind),''];return `<button type="button" class="hq-row" ${open(c)}><span class="source-chip ${cls}">${esc(label)}</span><span class="hq-row-text"><strong>${esc(c.title)}</strong><small>${esc(c.reason)}</small></span><small class="hq-when">${esc((c.collection?c.collection+' · ':'')+when(c.at))}</small></button>`;}).join('')}</div>`,s.totals.changes>s.changes.length?`<small>${s.totals.changes} in all</small>`:'','wide');
  }
  function needs(s){
    if(!s.attention.length&&!s.deadlines.length)return '';
    const due=s.deadlines.map(d=>`<button type="button" class="hq-row" data-collection="${esc(d.collection_id)}"><span class="source-chip review">Due</span><span class="hq-row-text"><strong>${esc(d.title)}</strong><small>${esc(d.collection)}</small></span><small class="hq-when">${d.days<1?'Today':d.days===1?'Tomorrow':d.days+' days'}</small></button>`).join('');
    const items=s.attention.map(a=>`<button type="button" class="hq-row" data-record="${esc(a.id)}"><span class="hq-row-text"><strong>${esc(a.title)}</strong><small>${esc(a.reason)}</small></span></button>`).join('');
    return tile('Needs you',`<div class="hq-list">${due}${items}</div>`,s.totals.attention>s.attention.length?`<small>${s.totals.attention} open</small>`:'');
  }
  function knows(s){
    const k=s.knowledge;if(!k.findings)return '';
    const parts=STATUS.filter(([id])=>k.by_status[id]);
    return tile('What we know',`<div class="hq-bar" role="img" aria-label="${esc(parts.map(([id,label])=>k.by_status[id]+' '+label.toLowerCase()).join(', '))}">${parts.map(([id])=>`<i class="${id}" style="flex:${k.by_status[id]}"></i>`).join('')}</div>
      <div class="hq-counts">${parts.map(([id,label,cls])=>`<span><strong>${k.by_status[id]}</strong><span class="source-chip ${cls}">${esc(label)}</span></span>`).join('')}</div>`,
      '<button type="button" class="text-button" data-view="business">Open</button>');
  }
  function goals(s){
    if(!s.goals.length)return '';
    return tile('Goals',`<div class="hq-list">${s.goals.map(g=>{
      const tracked=typeof g.target==='number',has=tracked&&typeof g.latest==='number';
      const done=has?(g.direction==='lower_better'?(g.latest<=g.target?1:g.target/g.latest):Math.min(1,g.latest/(g.target||1))):0;
      const meter=tracked?`<span class="hq-meter" role="img" aria-label="${has?esc(measure(g.latest,g.unit)+' of '+measure(g.target,g.unit)):'No measurement yet'}"><i style="width:${Math.round(Math.max(0,Math.min(1,done))*100)}%"></i></span>`:'';
      const note=tracked?(has?`${measure(g.latest,g.unit)} ${g.direction==='lower_better'?'· target '+measure(g.target,g.unit):'of '+measure(g.target,g.unit)}${g.reached?' · Reached':''}`:'No measurement yet'):'';
      return `<button type="button" class="hq-row stack" data-record="${esc(g.id)}"><span class="hq-row-text"><strong>${esc(g.name)}</strong>${note?`<small>${esc(note)}</small>`:''}</span>${meter}</button>`;}).join('')}</div>`,
      s.totals.goals>s.goals.length?`<small>${s.totals.goals} in all</small>`:'');
  }
  function watches(s){
    if(!s.watches.length)return '';
    return tile('Kept current',`<div class="hq-list">${s.watches.map(w=>`<button type="button" class="hq-row" data-collection="${esc(w.id)}"><span class="hq-row-text"><strong>${esc(w.name)}</strong><small>${w.current} current ${w.kind==='reports'?'report':'result'}${w.current===1?'':'s'}${w.last_changes?` · ${w.last_changes} change${w.last_changes===1?'':'s'} at last check`:''}</small></span><small class="hq-when">${esc(when(w.last_checked))}</small></button>`).join('')}</div>`);
  }
  function team(s){
    const busy=new Set(s.running.map(r=>r.assistant_id).filter(Boolean)),loose=s.running.filter(r=>!r.assistant_id||!s.agents.some(a=>a.id===r.assistant_id));
    if(!s.agents.length&&!loose.length)return '';
    const agents=s.agents.map(a=>`<button type="button" class="hq-agent" data-assistant-open="${esc(a.id)}">${busy.has(a.id)?'<span class="activity-spinner" aria-label="Working now"></span>':''}<span>${esc(a.name)}</span>${a.tasks?`<small>${a.tasks} task${a.tasks===1?'':'s'}</small>`:''}</button>`).join('');
    const chats=loose.map(r=>`<button type="button" class="hq-agent" data-chat="${esc(r.chat_id)}"><span class="activity-spinner" aria-label="Working now"></span><span>${esc(r.title||'A chat')}</span></button>`).join('');
    return tile(s.agents.length?'Agents':'Working now',`<div class="hq-agents">${agents}${chats}</div>`,'<button type="button" class="text-button" data-view="assistants">Open</button>','wide');
  }
  function results(s){
    if(!s.results.length)return '';
    return tile('Recent results',`<div class="hq-list">${s.results.map(r=>`<button type="button" class="hq-row" data-record="${esc(r.id)}"><span class="hq-row-text"><strong>${esc(r.title)}</strong></span><small class="hq-when">${esc(r.updated_at?stamp(r.updated_at):'')}</small></button>`).join('')}</div>`,'<button type="button" class="text-button" data-view="files">Open</button>');
  }
  /* The capability map: every area AURA has guidance for. Lit means findings are saved there. */
  function areas(s){
    const list=s.knowledge.by_area.filter(a=>a.id!=='core'||a.findings);
    return tile(s.empty?'What you can ask for':'What we know, by area',`<div class="hq-areas">${list.map(a=>{
      const ask=a.findings?`Summarise what we know about ${a.name.toLowerCase()} and what to do next. Say what is supported and what is still unverified.`:AREA_START[a.id];
      return `<button type="button" class="hq-area ${a.findings?'lit':''}" data-prompt="${esc(ask)}" title="${a.findings?'Ask about this area':'Start here'}"><i aria-hidden="true"></i><span>${esc(a.name)}</span><small>${a.findings?a.findings+' finding'+(a.findings===1?'':'s'):'Start'}</small></button>`;}).join('')}</div>
      <p class="small-note">A lit area has saved findings. Choosing any area fills the message box, and nothing runs until you send.</p>`,'','full');
  }
  function start(){
    return `<section class="hq-card hq-tile full hq-start"><div><h3>Your business fills in here as you work</h3><p>Findings, goals, what changed and what needs you will appear below once they exist. Ask for anything in the box above, or begin with one of these.</p></div><div class="inline-actions"><button type="button" class="secondary" data-prompt="${esc(RESEARCH)}">Research my business</button><button type="button" class="text-button" data-hq-example>See an example business</button></div></section>`;
  }

  function render(s){
    const host=$('#hq');if(!host)return;
    // Two columns when there is enough to fill both: what happened on the left, where things stand on the right.
    const main=changed(s)+goals(s)+team(s)+results(s),side=needs(s)+knows(s)+watches(s);
    const body=main&&side?`<div class="hq-columns"><div class="hq-column">${main}</div><div class="hq-column">${side}</div></div>`:`<div class="hq-grid">${main}${side}</div>`;
    const html=s.empty?head(s)+`<div class="hq-grid">${start()}${areas(s)}</div>`:head(s)+body+`<div class="hq-grid">${areas(s)}</div>`;
    if(host.dataset.markup!==html){host.innerHTML=html;host.dataset.markup=html;}
  }
  async function paint(force=false){
    if(!visible())return;
    const host=$('#hq');
    if(data&&key.startsWith(scope()+'|'))render(data);
    else if(host){host.innerHTML='';host.dataset.markup='';}  // never show one business's summary under another's name
    try{const s=await load(force);if(s&&visible())render(s);}
    catch(error){const host=$('#hq');if(host&&!host.innerHTML)host.innerHTML=`<div class="hq-card"><p class="small-note">Your business summary could not be read. ${esc(humanError(error))}</p></div>`;}
  }
  /* Called whenever the chat or page changes: home shows the business, a chat shows only the chat. */
  function sync(force=false){
    const host=$('#hq');if(!host)return;
    const on=visible();
    document.body.classList.toggle('has-hq',on);host.hidden=!on;
    if(!on){if(!state.business||(data&&!key.startsWith(scope()+'|'))){data=null;key='';host.innerHTML='';host.dataset.markup='';}return;}
    paint(force);
  }

  document.addEventListener('click',e=>{
    if(e.target.closest('[data-hq-aura]'))explain();
    if(e.target.closest('[data-hq-example]'))attempt(()=>window.auraExample?.open());
  });
  return {sync,paint,visible,explain,research:RESEARCH,cached:()=>data};
})();

/* The example business: a made-up organization in its own workspace, built the first time it is opened. */
window.auraExample={
  async open(){
    rememberChatDraft();detachChatView();state.navigating=true;chatControls();
    notice('Opening the example business. The first time takes a moment to prepare.');
    try{
      await api('/api/example',{});
      for(const dialog of document.querySelectorAll('dialog[open]'))dialog.close();
      state.business='';state.chat=[];state.chatMeta=null;state.liveJob=null;state.hydrated=false;state.library=[];state.catalog=null;state.files=[];state.connectionChecks=null;state.setupPrompted=new Set();state.setupStep='welcome';
      $('#request').value='';state.home=true;await refresh();recordShellRoute();
      notice('This is AURA’s example business. Everything in it is made up. Switch back to your own workspace from the list at the top left.');
    }finally{state.navigating=false;chatControls();}
  }
};
