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
  const RESEARCH='Research our business and fill in what you know about it. Find what we offer, who we serve, our main competitors and the claims we make, each with its source. Save what you find, keep unknowns as unknown, and tell me what you saved.';
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
  const share=k=>k.reviewed.with_date?k.reviewed.recent/k.findings:null;

  async function load(force=false){
    if(!state.business)return null;
    const k=scope()+'|'+(state.data?.records_revision||'');
    if(!force&&data&&key===k&&Date.now()-loadedAt<FRESH_MS)return data;
    if(pending&&pendingKey===k)return pending;  // several redraws while one read is in flight share it
    const asked=scope();pendingKey=k;
    pending=api('/api/summary?business='+encodeURIComponent(state.business))
      .then(result=>{if(asked!==scope()||pendingKey!==k)return null;data=result;key=k;loadedAt=Date.now();return data;})
      .finally(()=>{if(pendingKey===k)pending=null;});
    return pending;
  }

  /* The aura is the business's face: its colours come from the chosen focus areas, so it is recognisable
     wherever the business appears, and it moves only while your AI is working. Nothing else is encoded in it;
     what needs attention is said in words (Needs you, the status line), not in a picture to decode. */
  function aura(s,size=''){
    const hues=s.focus.map(a=>hue(a.id)).slice(0,3),working=s.running.length>0||(state.data?.running_chats||[]).length>0;
    const style=hues.length?`--hq-h1:${hues[0]};--hq-h2:${hues[1]??(hues[0]+40)%360};--hq-h3:${hues[2]??(hues[0]+320)%360}`:'';
    return `<button type="button" class="hq-aura ${size} ${hues.length?'':'plain'} ${working?'working':''}" style="${style}" data-hq-aura aria-label="Your aura. Open what it shows." title="What this shows"><span aria-hidden="true"></span></button>`;
  }
  function explain(){
    if(!data)return;
    const s=data,k=s.knowledge,by=k.by_status,working=s.running.length||(state.data?.running_chats||[]).length;
    const row=(name,value,why)=>`<div class="field"><strong>${esc(name)}</strong><p>${esc(value)}</p><p class="small-note">${esc(why)}</p></div>`;
    const facts=[k.findings?`${k.findings} finding${k.findings===1?'':'s'} saved${by.challenged?`, ${by.challenged} challenged by new evidence`:''}`:'',k.reviewed.with_date?`${k.reviewed.recent} reviewed in the last ${k.reviewed.within_days} days`:''].filter(Boolean).join('; ');
    details('Your aura',`<p class="shell-help">The face of this business in AURA, drawn only from what is saved.</p>
      ${row('Colour',s.focus.length?s.focus.map(a=>a.name).join(', '):'No focus areas chosen yet','Each focus area you chose adds its own colour, so the business looks the same wherever it appears.')}
      ${row('Movement',working?`${working} request${working===1?'':'s'} working now`:'Still','It moves only while your AI is working on this business.')}
      ${facts?row('What you know',facts,'Open Knowledge to read and review findings.'):''}
      <div class="inline-actions"><button type="button" class="secondary" data-view="business">Open Knowledge</button></div>`,'context');
  }

  function head(s){
    const b=s.business;
    const example=b.example?`<p class="hq-example"><span class="source-chip review">Example business</span> Everything here is made up, so you can look around freely. ${window.auraExample.origin()?'<button type="button" class="text-button" data-example-return>Return to my workspace</button>':'Choose your own workspace from the list at the top left.'}</p>`:'';
    return `<div class="hq-head">${aura(s)}<div class="hq-identity"><h1>${esc(b.name)}</h1>${b.description?`<p class="hq-description">${esc(b.description)}</p>`:'<p class="hq-description"><button type="button" class="text-button" data-action="edit-business">Say what your business does</button> to get suggestions that fit.</p>'}</div></div>${example}`;
  }
  /* A section is a heading and its rows: no box around it. Needs you is the one tinted section. */
  const section=(title,body,extra='',cls='')=>`<section class="hq-section ${cls}"><div class="hq-section-head"><h2>${esc(title)}</h2>${extra}</div>${body}</section>`;
  const open=c=>c.collection_id&&c.item_id?`data-hq-item="${esc(c.item_id)}" data-parent-collection="${esc(c.collection_id)}"`:c.collection_id?`data-collection="${esc(c.collection_id)}"`:`data-record="${esc(c.record)}"`;
  const row=(attrs,title,note='',side='',lead='')=>`<button type="button" class="hq-row" ${attrs}>${lead}<span class="hq-row-text"><strong>${esc(title)}</strong>${note?`<small>${esc(note)}</small>`:''}</span>${side?`<small class="hq-when">${esc(side)}</small>`:''}</button>`;

  function dueDate(value){
    const due=new Date(value),today=new Date(),tomorrow=new Date();
    tomorrow.setDate(today.getDate()+1);
    const day=due.toDateString(),label=day===today.toDateString()?'Today':day===tomorrow.toDateString()?'Tomorrow':'';
    return [label,due.toLocaleDateString(undefined,{month:'short',day:'numeric',year:'numeric'})].filter(Boolean).join(' · ');
  }
  function needs(s){
    if(!s.attention.length&&!s.deadlines.length)return '';
    const due=s.deadlines.map(d=>row(open(d),d.title,d.collection,'Due '+dueDate(d.due))).join('');
    const items=s.attention.map(a=>row(`data-record="${esc(a.id)}"`,a.title,a.reason)).join('');
    return section('Needs you',`<div class="hq-list">${due}${items}</div>`,s.totals.attention>s.attention.length?`<small>${s.totals.attention} open</small>`:'','hq-needs');
  }
  function team(s){
    const busy=new Set(s.running.map(r=>r.assistant_id).filter(Boolean)),loose=s.running.filter(r=>!r.assistant_id||!s.agents.some(a=>a.id===r.assistant_id));
    if(!s.agents.length&&!loose.length)return '';
    const agents=s.agents.map(a=>`<button type="button" class="hq-agent" data-assistant-open="${esc(a.id)}">${busy.has(a.id)?'<span class="activity-spinner" aria-label="Working now"></span>':''}<span>${esc(a.name)}</span>${a.tasks?`<small>${a.tasks} task${a.tasks===1?'':'s'}</small>`:''}</button>`).join('');
    const chats=loose.map(r=>`<button type="button" class="hq-agent" data-chat="${esc(r.chat_id)}"><span class="activity-spinner" aria-label="Working now"></span><span>${esc(r.title||'A chat')}</span>${r.progress?`<small>${esc(r.progress)}</small>`:''}</button>`).join('');
    return section(s.running.length?'Running now':'Agents',`<div class="hq-agents">${chats}${agents}</div>`,'<button type="button" class="text-button" data-view="assistants">All agents</button>');
  }
  function resume(s){
    const recent=state.homeRecent?.scope===scope()?state.homeRecent.chat:null;
    if(!recent&&!s.results.length)return '';
    const at=recent?.updated||recent?.created,stampAt=typeof at==='number'?new Date(at<1e12?at*1000:at).toISOString():at;  // chat times are seconds
    const chat=recent?row(`data-chat="${esc(recent.id)}"`,recent.title||'Recent chat','Chat',stampAt?when(stampAt):''):'';
    const results=s.results.map(r=>row(`data-record="${esc(r.id)}"`,r.title,'Result',r.updated_at?when(r.updated_at):'')).join('');
    return section('Pick up where you left off',`<div class="hq-list">${chat}${results}</div>`,'<button type="button" class="text-button" data-view="files">All files</button>');
  }
  function changed(s){
    if(!s.changes.length)return '';
    const title=s.changes_days===7?'This week':`Last ${s.changes_days} days`;
    return section(title,`<div class="hq-list">${s.changes.map(c=>{const [label,cls]=CHANGE[c.kind]||[human(c.kind),''];return row(open(c),c.title,c.reason,(c.collection?c.collection+' · ':'')+when(c.at),`<span class="source-chip ${cls}">${esc(label)}</span>`);}).join('')}</div>`,s.totals.changes>s.changes.length?`<small>${s.totals.changes} in all</small>`:'');
  }
  function goals(s){
    if(!s.goals.length)return '';
    return section('Goals',`<div class="hq-list">${s.goals.map(g=>{
      const tracked=typeof g.target==='number',has=tracked&&typeof g.latest==='number';
      const done=has?(g.direction==='lower_better'?(g.latest<=g.target?1:g.target/g.latest):Math.min(1,g.latest/(g.target||1))):0;
      const meter=tracked?`<span class="hq-meter ${g.reached?'reached':''}" role="img" aria-label="${has?esc(measure(g.latest,g.unit)+' of '+measure(g.target,g.unit)):'No measurement yet'}"><i style="width:${Math.round(Math.max(0,Math.min(1,done))*100)}%"></i></span>`:'';
      const note=tracked?(has?`${measure(g.latest,g.unit)} ${g.direction==='lower_better'?'· target '+measure(g.target,g.unit):'of '+measure(g.target,g.unit)}${g.reached?' · Reached':''}`:'No measurement yet'):'Not measured';
      return `<button type="button" class="hq-row stack" data-record="${esc(g.id)}"><span class="hq-row-text"><strong>${esc(g.name)}</strong><small>${esc(note)}</small></span>${meter}</button>`;}).join('')}</div>`,
      s.totals.goals>s.goals.length?`<small>${s.totals.goals} in all</small>`:'');
  }
  /* Collections in plain words: when each was last checked and what the check found. */
  function watches(s){
    if(!s.watches.length)return '';
    const checked=w=>!w.last_checked?'Not checked yet':(({partial:'Partly checked ',failed:'Check failed '})[w.coverage]||'Checked ')+when(w.last_checked).replace(/^(Today|Yesterday)/,m=>m.toLowerCase());
    return section('Collections',`<div class="hq-collections">${s.watches.map(w=>`<button type="button" class="hq-collection" data-collection="${esc(w.id)}"><span class="hq-collection-preview" data-collection-preview="${esc(w.id)}" aria-hidden="true"></span><strong>${esc(w.name)}</strong><span>${w.current} ${w.kind==='reports'?'report':'result'}${w.current===1?'':'s'}${w.last_changes?` · ${w.last_changes} change${w.last_changes===1?'':'s'}`:''}</span><small>${esc(checked(w))}</small></button>`).join('')}</div>`,'<button type="button" class="text-button" data-view="files">All files</button>');
  }
  /* What is known: how well-supported it is, and every area AURA has guidance for. Lit areas open their
     findings; the others prepare a first request (nothing runs until you send). */
  function knows(s){
    const k=s.knowledge,parts=STATUS.filter(([id])=>k.by_status[id]);
    const bar=k.findings?`<div class="hq-bar" role="img" aria-label="${esc(parts.map(([id,label])=>k.by_status[id]+' '+label.toLowerCase()).join(', '))}">${parts.map(([id])=>`<i class="${id}" style="flex:${k.by_status[id]}"></i>`).join('')}</div>
      <div class="hq-counts">${parts.map(([id,label,cls])=>`<span><strong>${k.by_status[id]}</strong><span class="source-chip ${cls}">${esc(label)}</span></span>`).join('')}</div>`:'';
    const list=k.by_area.filter(a=>a.id!=='core'||a.findings);
    const areas=`<div class="hq-areas">${list.map(a=>`<button type="button" class="hq-area ${a.findings?'lit':''}" ${a.findings?`data-hq-area="${esc(a.id)}"`:`data-prompt="${esc(AREA_START[a.id])}"`} title="${a.findings?'Read saved findings':'Prepare a first request'}"><i aria-hidden="true"></i><span>${esc(a.name)}</span>${a.findings?`<small>${a.findings}</small>`:''}</button>`).join('')}</div>`;
    const ask='<button class="text-button" data-prompt="Check what AI says about our business against our verified facts. Use the AI visibility and factual accuracy workflows. Identify each service sampled, the question, date, exact discrepancy and supporting source. Disclose any services you could not sample.">What does AI say about my business?</button>';
    return section(k.findings?'What we know':'What you can ask for',`${bar}${areas}<div class="hq-know-foot"><small class="small-note">${k.findings?'Open an area to read its findings. The others prepare a first request.':'Choose an area to prepare a first request.'}</small>${ask}</div>`,k.findings?'<button type="button" class="text-button" data-view="business">Knowledge</button>':'');
  }
  function openArea(id){
    const area=data?.knowledge.by_area.find(a=>a.id===id);
    if(!area)return;
    const findings=state.data.records.filter(r=>r.type==='Insight'&&r.data.domain===id&&!r.data.extensions?.businessos?.archive?.at&&!['superseded','archived'].includes(r.data.status));
    const status=f=>f.status==='contradicted'?'Challenged':Date.parse(f.extensions?.businessos?.review_after)<=Date.now()?'Needs review':({candidate:'Unverified',stale:'Out of date',supported:'Supported',active:'Supported'})[f.status]||'Unverified';
    const priority=f=>({'Challenged':0,'Needs review':1})[status(f)]??2;
    findings.sort((a,b)=>priority(a.data)-priority(b.data));
    details(area.name,findings.map(r=>`<button class="row" data-hq-finding="${esc(r.ref)}" data-area="${esc(id)}"><span class="row-text"><strong>${esc(r.data.statement)}</strong><small class="row-meta">${esc(status(r.data))}</small></span></button>`).join('')+`<button class="secondary" data-prompt="${esc('Review our saved findings about '+area.name+' and recommend a next step.')}">Ask about ${esc(area.name)}</button>`);
  }
  function start(){
    return `<section class="hq-section hq-start"><div><h2>Your business fills in here as you work</h2><p>What needs you, what changed, goals and findings appear here once they exist. Ask for anything above, or begin with one of these.</p></div><div class="inline-actions"><button type="button" class="secondary" data-hq-research>Research my business</button><button type="button" class="text-button" data-hq-example>See an example business</button></div></section>`;
  }

  function render(s){
    const host=$('#hq');if(!host)return;
    const top=$('#hq-head'),headHtml=head(s);
    if(top&&top.dataset.markup!==headHtml){top.innerHTML=headHtml;top.dataset.markup=headHtml;}
    const draft=s.business.example&&state.data.records?.find(r=>r.type==='Asset'&&r.data.location_reference?.endsWith('/outputs/grant-application-draft.md'));
    const story=draft?section('Try this',`<p class="hq-story">Is this grant application ready to submit? Review the bakery’s draft and see which answer still needs the owner.</p><div class="inline-actions"><button class="secondary" data-record="${esc(draft.ref)}">Read the grant draft</button>${window.auraExample.origin()?'<button class="text-button" data-example-try>Try this with my work</button>':''}</div>`):'';
    // Most important first: what needs you, what is running, where you were, what changed, then where things stand.
    const pair=goals(s)+watches(s);
    const html=(s.empty?start():'')+needs(s)+team(s)+story+resume(s)+changed(s)+(pair?`<div class="hq-pair">${pair}</div>`:'')+knows(s);
    if(host.dataset.markup!==html){host.innerHTML=html;host.dataset.markup=html;}
    fillPreviews(host);
  }
  async function paint(force=false){
    if(!visible())return;
    const host=$('#hq');
    if(data&&key.startsWith(scope()+'|'))render(data);
    else if(host){host.innerHTML='';host.dataset.markup='';const top=$('#hq-head');if(top){top.innerHTML='';top.dataset.markup='';}}  // never show one business's summary under another's name
    try{const s=await load(force);if(s&&visible())render(s);}
    catch(error){const host=$('#hq');if(host&&!host.innerHTML)host.innerHTML=`<div class="hq-card"><p class="small-note">Your business summary could not be read. ${esc(humanError(error))}</p></div>`;}
  }
  /* Called whenever the chat or page changes: home shows the business, a chat shows only the chat. */
  function sync(force=false){
    const host=$('#hq');if(!host)return;
    const on=visible();
    document.body.classList.toggle('has-hq',on);host.hidden=!on;const top=$('#hq-head');if(top)top.hidden=!on;
    if(!on){if(!state.business||(data&&!key.startsWith(scope()+'|'))){data=null;key='';host.innerHTML='';host.dataset.markup='';if(top){top.innerHTML='';top.dataset.markup='';}}return;}
    paint(force);
  }

  document.addEventListener('click',e=>{
    const target=e.target.closest('[data-hq-item],[data-hq-area]');
    if(target?.dataset.hqItem)attempt(()=>window.auraProjects.openItem(target.dataset.parentCollection,target.dataset.hqItem));
    if(target?.dataset.hqArea)openArea(target.dataset.hqArea);
    const finding=e.target.closest('[data-hq-finding]');
    if(finding){window.auraProjects.finding(finding.dataset.hqFinding,null);setDetailBack('Area findings',()=>openArea(finding.dataset.area));}
    if(e.target.closest('[data-example-return],[data-example-try]'))attempt(()=>window.auraExample.leave(!!e.target.closest('[data-example-try]')));
    if(e.target.closest('[data-hq-research]')){
      details('Research my business','<form id="hq-research" class="form-grid"><label>What are you trying to decide? (optional)<textarea name="decision" rows="2" placeholder="Should we expand wholesale?"></textarea></label><label>Business website (optional)<input name="website" placeholder="Your website"></label><button class="primary">Prepare request</button></form>');
      $('#hq-research').onsubmit=event=>{
        event.preventDefault();const form=new FormData(event.target),site=form.get('website').trim(),decision=form.get('decision').trim();
        const request=decision?'Research our business to help me decide: '+decision+'. Use relevant sources, save useful findings and identify what remains unknown.':RESEARCH;
        prompt(request+(site?' Start from our website: '+site:''));
      };
    }
    if(e.target.closest('[data-hq-aura]'))explain();
    if(e.target.closest('[data-hq-example]'))attempt(()=>window.auraExample?.open());
  });
  /* The same aura beside the workspace name in the sidebar, so the business is recognisable wherever you are. */
  function paintMark(){
    const hosts=['#sidebar-aura','#knowledge-aura'].map(id=>$(id)).filter(Boolean);if(!hosts.length)return;
    for(const host of hosts)if(!host.firstElementChild)host.innerHTML='<span></span>';
    if(!state.business){for(const host of hosts){host.className='hq-aura mini plain';host.removeAttribute('style');}return;}
    load().then(s=>{
      if(!s)return;
      const hues=s.focus.map(a=>hue(a.id)).slice(0,3),working=(state.data?.running_chats||[]).length>0;
      for(const host of hosts){
        if(!host.isConnected)continue;
        host.className=['hq-aura mini',hues.length?'':'plain',working?'working':''].filter(Boolean).join(' ');
        if(hues.length)host.setAttribute('style',`--hq-h1:${hues[0]};--hq-h2:${hues[1]??(hues[0]+40)%360};--hq-h3:${hues[2]??(hues[0]+320)%360}`);else host.removeAttribute('style');
      }
      window.paintAuraStatus?.();
    }).catch(()=>{});
  }
  /* A small picture of a collection's real results: a dot map when they have places, otherwise the first few
     names. Read once a minute at most, and drawn only from the saved results. */
  const previews=new Map();
  function preview(id){
    const hit=previews.get(id);if(hit&&Date.now()-hit.at<60000)return hit.promise;
    const promise=api('/api/collection-view?'+new URLSearchParams({business:state.business,id,view:'current'})).then(r=>{
      const items=(r.items||[]).filter(i=>!i.hidden),placed=items.filter(i=>Number.isFinite(i.lat)&&Number.isFinite(i.lng));
      if(placed.length>=2){
        const lats=placed.map(i=>i.lat),lngs=placed.map(i=>i.lng),[a,b,c,d]=[Math.min(...lats),Math.max(...lats),Math.min(...lngs),Math.max(...lngs)];
        const x=v=>8+84*(d===c?.5:(v-c)/(d-c)),y=v=>6+48*(b===a?.5:1-(v-a)/(b-a));
        return `<svg class="collection-dots" viewBox="0 0 100 60" role="img" aria-label="${placed.length} places on a map">${placed.slice(0,80).map(i=>`<circle cx="${x(i.lng).toFixed(1)}" cy="${y(i.lat).toFixed(1)}" r="${i.fields?.yours?3.2:2}" class="${i.fields?.yours?'yours':''}"/>`).join('')}</svg>`;
      }
      return items.length?`<ul class="collection-names">${items.slice(0,3).map(i=>`<li>${esc(i.title||'Untitled')}</li>`).join('')}</ul>`:'';
    }).catch(()=>'');
    previews.set(id,{at:Date.now(),promise});return promise;
  }
  function fillPreviews(root=document){
    if(typeof root?.querySelectorAll!=='function')return;
    for(const host of root.querySelectorAll('[data-collection-preview]:not([data-filled])')){
      host.dataset.filled='1';preview(host.dataset.collectionPreview).then(html=>{if(html&&host.isConnected){host.innerHTML=html;host.classList.add('has-preview');}});
    }
  }
  /* Real items waiting on the person: open attention records and upcoming deadlines in saved collections. */
  const needsCount=()=>data&&key.startsWith(scope()+'|')?(data.totals?.attention||0)+(data.deadlines?.length||0):0;
  return {sync,paint,visible,explain,paintMark,needsCount,fillPreviews,research:RESEARCH,cached:()=>data};
})();

/* The example business: a made-up organization in its own workspace, built the first time it is opened. */
window.auraExample={
  origin(){
    try{const origin=JSON.parse(sessionStorage.getItem('aura-example-return'));return origin?.example===state.data?.workspace?origin:null;}catch{return null;}
  },
  async leave(prepare){
    const origin=this.origin();if(!origin)return;
    await openStoredWorkspace(origin.path);
    if(state.data.workspace!==origin.path)return;
    if(origin.business&&state.data.businesses.some(b=>b.id===origin.business))await changeWorkspace(origin.business);
    if(state.business!==origin.business)return;
    await goHome();
    if(prepare)prompt('Review my document against the saved evidence. Which claims can I support, what is missing, and what should I confirm before sending it?');
  },
  async open(){
    if(state.navigating)return;
    const previous={path:state.data?.workspace,business:state.business};
    rememberChatDraft();state.navigating=true;chatControls();
    notice('Opening the example business. The first time takes a moment to prepare.');
    try{
      await api('/api/example',{});detachChatView();
      for(const dialog of document.querySelectorAll('dialog[open]'))dialog.close();
      state.business='';state.chat=[];state.chatMeta=null;state.liveJob=null;state.hydrated=false;state.library=[];state.catalog=null;state.files=[];state.connectionChecks=null;state.setupPrompted=new Set();state.setupStep='welcome';
      $('#request').value='';state.home=true;state.view='home';await refresh();
      if(previous.business&&previous.path!==state.data.workspace){
        try{sessionStorage.setItem('aura-example-return',JSON.stringify({...previous,example:state.data.workspace}));}catch{}
        window.auraHQ.sync();
      }
      recordShellRoute();
      notice('This is AURA’s example business. Everything in it is made up. Switch back to your own workspace from the list at the top left.');
    }finally{state.navigating=false;chatControls();}
  }
};
