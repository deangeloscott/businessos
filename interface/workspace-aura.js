/* The aura, opened: the organization drawn as a world (workspace-world.js), with the same things listed beside it.
   Everything shown comes from /api/world, which returns saved records only. Relationships are read through
   workspace-links.js, the one place that walks them, so the world, this panel and the Connections diagram agree.
   Each thing opens the screen AURA already has for it; a next step opens an ordinary chat. Nothing leaves the
   computer unless the owner downloads a picture or clip and shares it. The list is also how it is read without 3D. */
window.auraView=(()=>{
  const hq=()=>window.auraHQ,world=()=>window.auraWorld,links=()=>window.auraLinks;
  const money=n=>'$'+Number(n).toLocaleString(undefined,{maximumFractionDigits:n<10?2:0});
  const value=(v,unit)=>unit==='USD'?money(v):Number(v).toLocaleString(undefined,{maximumFractionDigits:2})+(unit&&!['count','rank','USD'].includes(unit)?' '+unit:'');
  const records=type=>(state.data?.records||[]).filter(r=>r.type===type);
  const goals=()=>records('Objective').filter(r=>{const g=r.data.extensions?.businessos?.goal||{};return g.scope!=='chat'&&!g.deleted_at&&(r.data.status||'active')==='active';});
  const refOf=id=>(state.data?.records||[]).find(r=>r.data?.id===id)?.ref||'';
  const when=d=>d?new Date(d).toLocaleDateString(undefined,{month:'short',day:'numeric',year:'numeric'}):'';
  const count=(n,word)=>`${n} ${word}${n===1?'':'s'}`;
  const hash=s=>{let h=2166136261;for(const c of String(s)){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;};
  let ctx=null,shiftTimer;

  /* A goal in words, from its saved measurements only. */
  const goalLine=g=>typeof g.target!=='number'?'No number yet':g.reached?'Reached':typeof g.latest!=='number'?'No measurement yet':g.direction==='lower_better'?`${value(g.latest,g.unit==='USD'?'USD':'')} · target ${value(g.target,g.unit)} or lower`:`${value(g.latest,g.unit==='USD'?'USD':'')} of ${value(g.target,g.unit)}`;
  const goalDone=g=>g.reached?1:typeof g.latest!=='number'||typeof g.target!=='number'?0:g.direction==='lower_better'?Math.min(1,g.target/Math.max(g.latest,1e-9)):Math.min(1,Math.max(0,g.latest)/(g.target||1));
  const FLABEL={supported:'Supported',unverified:'Not yet verified',challenged:'Challenged by new evidence',needs_review:'Due for review',out_of_date:'Out of date'};
  /* One small mark per kind of thing, in the text colour, so a row or a box says what it is at a glance. */
  const ICON={app:'<rect x="2.5" y="3.5" width="11" height="9" rx="2"/><path d="M5 7h6M5 9.5h4"/>',method:'<path d="M3 3.5h4v9.5H3zM9 3.5h4v9.5H9z"/>',file:'<path d="M4 2.5h5l3 3v8H4zM9 2.5v3h3"/>',
    record:'<path d="M3.5 5h9M3.5 8h9M3.5 11h5.5"/>',output:'<path d="M4 2.5h8v11H4zM6 6h4M6 9h4"/>',chat:'<path d="M3 3.5h10v6.5H7.5L4.5 13v-3H3z"/>',session:'<path d="M3 3.5h10v6.5H7.5L4.5 13v-3H3z"/>',
    agent:'<circle cx="8" cy="5.5" r="2.5"/><path d="M3.5 13.5a4.5 4.5 0 0 1 9 0"/>',task:'<circle cx="8" cy="8" r="5.5"/><path d="M8 5v3l2 1.5"/>',project:'<path d="M2.5 4.5h4l1.5 1.5h5.5v7H2.5z"/>',
    land:'<circle cx="8" cy="8" r="5.5"/><path d="M4.5 7.5c1.5-1.5 2.5.5 4-.5s2.5 1 3 2"/>',item:'<circle cx="8" cy="8" r="2.6" fill="currentColor"/>',finding:'<circle cx="8" cy="8" r="3"/>',
    decision:'<path d="M8 3l5 5-5 5-5-5z"/>',goal:'<circle cx="8" cy="8" r="5.5"/><circle cx="8" cy="8" r="2"/>'};
  const icon=kind=>ICON[kind]?`<svg class="kind-icon" viewBox="0 0 16 16" aria-hidden="true">${ICON[kind]}</svg>`:'';
  const row=(attrs,title,sub='',side='',hue=null,kind='')=>`<button type="button" class="world-row${attrs?'':' plain'}" ${attrs||'tabindex="-1"'}>${kind&&ICON[kind]?icon(kind):`<i${hue!=null?` style="background:hsl(${Math.round(hue)},70%,55%)"`:''}></i>`}<span><b>${esc(title)}</b>${sub?`<small>${esc(sub)}</small>`:''}</span><em>${esc(side)}</em></button>`;
  const hueOf=id=>world()?.model?.()?.lands.find(l=>l.id===id)?.hue??null;
  const landCounts=(f,l)=>{const n=l.items.length+(l.more||0),k=f.findings.filter(x=>x.land===l.id&&x.label!=='replaced').length;return [n?`${n} tracked`:'',k?count(k,'finding'):''].filter(Boolean).join(' · ');};
  const go=key=>`data-world-go="${esc(key)}"`;

  function goalSection(){
    const pin=hq().pinned(),measured=goals().filter(g=>typeof g.measure?.target==='number'),current=state.data?.aura_preferences?.goal||'';
    if(!measured.length)return '<p class="small-note">Add a goal with a number and its progress can show as a ring around your aura icon.</p>';
    return `<p class="small-note">The ring around your aura icon fills as real progress on this goal is recorded.</p><label class="aura-goal-pick"><span class="sr-only">Main goal</span><select id="aura-goal"><option value="">No ring</option>${measured.map(g=>`<option value="${esc(g.ref)}" ${g.ref===current?'selected':''}>${esc(g.title)}</option>`).join('')}</select></label>${pin?`<p class="aura-goal-status">${esc(pin.reached?'Reached':typeof pin.measure.latest==='number'?value(pin.measure.latest,pin.measure.unit)+' of '+value(pin.measure.target,pin.measure.unit):'No measurement yet')}</p>`:''}`;
  }

  /* What changed, once: since the last visit, or over the last two weeks for a first look. Goal numbers first. */
  const fallbackSince=f=>new Date((Date.parse(f.as_of)||Date.now())-14*864e5).toISOString();
  function whatChanged(f,since){
    const from=since||fallbackSince(f),list=changesSince(f,from).sort((a,b)=>(b.key.startsWith('goal:')-a.key.startsWith('goal:'))||Date.parse(b.at)-Date.parse(a.at));
    const title=since?'Since your last visit':'In the last two weeks';
    if(!list.length)return `<section><h3>${title}</h3><p class="small-note">No new findings, tracked changes or goal movement since ${esc(when(from))}.</p></section>`;
    return `<section><h3>${title}</h3>${list.slice(0,6).map(c=>row(go(c.key),c.title,c.detail,when(c.at),c.land?hueOf(c.land):null,c.key.split(':')[0])).join('')}${list.length>6?`<p class="small-note">and ${list.length-6} more</p>`:''}<button type="button" class="text-button" data-world-since="${esc(from.slice(0,10))}">See it over time</button></section>`;
  }
  const spark=tr=>{const pts=(tr?.points||[]).filter(p=>typeof p.value==='number');if(pts.length<2)return '';const vs=pts.map(p=>p.value),mn=Math.min(...vs),mx=Math.max(...vs);return `<div><svg class="world-spark" viewBox="0 0 140 30" role="img" aria-label="${esc(tr.field)} over time"><polyline points="${vs.map((v,i)=>`${(4+132*i/(vs.length-1)).toFixed(1)},${(25-20*(v-mn)/((mx-mn)||1)).toFixed(1)}`).join(' ')}"/></svg><p class="small-note">${esc(tr.field)}: ${esc(vs[0])} → ${esc(vs.at(-1))} over ${pts.length} checks</p></div>`;};
  /* Work that is running right now, and the area its chat is tied to. */
  const runningNow=()=>{if(!ctx)return [];const seen=new Set(),out=[];for(const r of (state.data?.running_chats||[]).filter(j=>j.status!=='done'&&(!j.business_id||j.business_id===ctx.business))){if(seen.has(r.chat_id))continue;seen.add(r.chat_id);const chat=(state.chatList||[]).find(c=>c.id===r.chat_id)||{};out.push({id:r.chat_id,land:ctx.feed.chat_lands?.[r.chat_id]||null,app:r.agent||'',agent:r.assistant_id||chat.assistant_id||'',title:r.title||chat.title||'',label:`${r.agent||'Your AI'} · working${r.title?' on '+r.title:''}`});}return out;};
  /* The places a goal, project, scheduled task or AI app touches, from its recorded chain. */
  const landsFor=(f,by)=>by?links().places(f,String(by)):[];
  /* On the picture: find and filter at the top; the areas as a colour key along the bottom. */
  function tools(f){
    const flt=ctx?.filter||{lands:[],needs:false,by:''};
    const options=[['Goals',f.goals.map(g=>['goal:'+g.id,g.name])],['Projects',(state.projects||[]).map(p=>['project:'+p.id,p.name])],['Scheduled tasks',(f.tasks||[]).map(k=>['task:'+k.id,k.name||'Scheduled task'])],['AI apps',(f.apps||[]).map(a=>['app:'+a.name,a.name])]].filter(g=>g[1].length);
    const top=`<label><span class="sr-only">Find in your world</span><input type="search" id="world-q" placeholder="Find anything…" autocomplete="off"></label>${options.length?`<label class="world-by"><span>Show what belongs to</span><select id="world-by"><option value="">Everything</option>${options.map(([label,list])=>`<optgroup label="${label}">${list.map(([v,n])=>`<option value="${esc(v)}" ${flt.by===v?'selected':''}>${esc(n)}</option>`).join('')}</optgroup>`).join('')}</select></label>${flt.by&&!flt.lands.length?'<p class="small-note">Nothing on the world is tied to this yet.</p>':''}`:''}`;
    const keys=f.lands.length>1?`<div class="world-chips" role="group" aria-label="Show only these areas">${f.lands.filter(l=>l.kind!=='group').map(l=>`<button type="button" class="world-chip" data-world-chip="${esc(l.id)}" aria-pressed="${flt.lands.includes(l.id)}"><i${hueOf(l.id)!=null?` style="background:hsl(${Math.round(hueOf(l.id))},70%,55%)"`:''}></i>${esc(l.name)}</button>`).join('')}<button type="button" class="world-chip" data-world-needs aria-pressed="${!!flt.needs}">Needs a look</button></div>`:'';
    return {top,keys};
  }
  function home(f){
    const shift=Number.isInteger(state.data?.aura_preferences?.shift)?state.data.aura_preferences.shift:0;
    return `<div><div class="kind">Your world</div><h2>${esc(f.business.name)}</h2>${f.business.example?'<p class="small-note">AURA\'s made-up example business.</p>':''}</div>
      <section><h3>Goals</h3>${f.goals.length?f.goals.map(g=>row(go('goal:'+g.id),g.name,goalLine(g))).join(''):'<p class="small-note">Add a goal with a number, such as "$50,000 in grants this year", and it becomes a ring around your world.</p>'}<button type="button" class="text-button" data-action="add-goal">Add goal</button></section>
      ${f.attention.length?`<section><h3>Needs you</h3>${f.attention.map(a=>row(refOf(a.id)?`data-record="${esc(refOf(a.id))}"`:'',a.title,a.reason)).join('')}</section>`:''}
      ${f.suggestions.length?`<section><h3>Next steps</h3>${f.suggestions.map(x=>row(`data-prompt="${esc(x.prompt)}"`,x.title,x.why)).join('')}</section>`:''}
      ${f.lands.length||f.findings.length?whatChanged(f,ctx?.since):''}
      <section><h3>Areas</h3>${f.lands.map(l=>row(go('land:'+l.id),l.name,landCounts(f,l)||'Nothing yet',l.quiet?'Gone quiet':'',hueOf(l.id))).join('')}${(f.uncharted||[]).map(a=>row(go('land:new:'+a.id),a.name,'Uncharted','',hueOf('new:'+a.id))).join('')}${f.lands_more?`<p class="small-note">and ${f.lands_more} more collection${f.lands_more===1?'':'s'}, open from Files.</p>`:''}${f.findings_hidden?`<p class="small-note">${f.findings_hidden} more finding${f.findings_hidden===1?' is':'s are'} kept but not drawn here. Open Knowledge to see them all.</p>`:''}${f.lands.length||(f.uncharted||[]).length?'':'<p class="small-note">What your AI saves appears here: collections, their results, and findings with sources.</p>'}</section>
      <button type="button" class="text-button" data-world-tour>Take the tour</button>
      <details class="aura-colour"><summary>How to read your world</summary><p class="small-note">Each continent is one of your collections, or an area of findings, always in the same place; it grows as it fills. Each light is something you track; smaller lights are findings (hollow means not yet verified), joined by a line to the result they rest on when the same source stands behind both. The faintest are changes a check noticed. The glow around an area grows when something there changed recently, so a settled area stays calm. Rings are goals with a number. A clock marks a scheduled task. Amber means it needs a look. Drag to turn the world, scroll to fly down, and use the arrow keys when it has focus.</p></details>
      <details class="aura-colour"><summary>Aura icon</summary>${goalSection()}<p class="small-note">Its colour comes from your focus areas. Adjust it here.</p><input type="range" id="aura-shift" min="-180" max="180" step="5" value="${shift}" aria-label="Colour"><button type="button" class="text-button" id="aura-shift-reset">Reset</button></details>`;
  }

  /* What stands between a goal and its number, read only from saved facts. Each comes with the request that would deal with it. */
  function goalGaps(f,g){
    const out=[];if(typeof g.target!=='number'||g.reached)return out;
    const last=(g.points||[]).at(-1),age=last?Math.floor((Date.parse(f.as_of)-Date.parse(last.at))/864e5):null,metric=g.metric||g.name;
    if(age===null)out.push(['No measurement has been saved yet',`Help me record the first number for "${metric}" toward our goal "${g.name}". If you can reach a source for it, use that; otherwise ask me.`]);
    else if(age>=21)out.push([`Not measured for ${age} days`,`Bring "${metric}" up to date for our goal "${g.name}".`]);
    for(const id of g.lands||[]){const l=f.lands.find(x=>x.id===id);if(!l)continue;
      if(l.quiet)out.push([`${l.name} has gone quiet`,`Check "${l.name}" again and update it with what has changed since it was last checked.`]);
      const weak=f.findings.filter(x=>x.land===id&&['unverified','challenged','needs_review','out_of_date'].includes(x.label)).length;
      if(weak)out.push([`${count(weak,'finding')} in ${l.name} need${weak===1?'s':''} checking`,`Check the findings in "${l.name}" that are unverified, challenged or due for review, and update each with what you find.`]);}
    for(const k of f.tasks||[])if(k.goal===g.id&&['failed','missing','paused'].includes(k.health))out.push([`${k.name||'A scheduled task'} is not running`,`The scheduled task "${k.name||'for this goal'}" is not running (${k.status||'no report'}). Help me get it running again.`]);
    if(!(g.lands||[]).length)out.push(['Nothing is linked to this goal yet','']);
    return out;
  }
  /* Where a saved record or file was made, when AURA did not see it at the time: read on request from the AI apps' own logs. */
  function origin(f,key,ref){
    if(!ref||(links().index(f).into.get(key)||[]).some(e=>e.type==='saved'))return '';
    const found=ctx?.origins?.[key];
    if(found==='looking')return '<p class="small-note">Looking in the AI apps’ own records on this computer…</p>';
    if(found===false)return '<p class="small-note">Not found in the AI apps’ own records on this computer, so where this was made is not recorded.</p>';
    if(found)return `<p class="small-note">Made in ${esc(found.app)}${found.title?` · “${esc(found.title)}”`:''} · ${esc(when(found.at))}</p>`;
    return `<button type="button" class="text-button" data-world-origin="${esc(key)}" ${ref.file?`data-origin-file="${esc(ref.file)}"`:`data-origin-record="${esc(ref.record)}"`}>Where was this made?</button>`;
  }
  /* Beside the world with something selected: what it is, whether it needs a look, and the way into its own screen. */
  function selected(f,o){
    const back='<button type="button" class="text-button world-back" data-world-clear>Show everything</button>',head=(kind,title)=>`<div><div class="kind">${esc(kind)}</div><h2>${esc(title)}</h2></div>`,facts=list=>`<dl class="world-facts">${list.filter(x=>x[1]!==''&&x[1]!=null).map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
    const ask=text=>`<button type="button" class="secondary" data-prompt="${esc(text)}">Ask about it</button>`;
    if(o.relationship){
      const allowed=['record','file','method','chat','view','open-project','assistant-open'];
      const actions=Object.entries(o.raw.action||{}).filter(([name])=>allowed.includes(name)).map(([name,id])=>
        `<button type="button" class="secondary" data-${name}="${esc(id)}">Open ${esc(links().KIND[o.kind]||o.kind)}</button>`).join('');
      const made=o.raw.action?.record?origin(f,links().key(o),{record:o.raw.action.record}):o.raw.action?.file?origin(f,links().key(o),{file:o.raw.action.file}):'';
      const session=o.kind==='session'?`<p class="small-note">Work done directly in ${esc(o.raw.sub||'an AI app')}, outside AURA's chat. Its own session record on this computer is where it came from.</p>`:'';
      return back+head(links().KIND[o.kind]||o.kind,o.name)+session+'<div class="world-acts">'+actions+ask('Help me work with “'+o.name+'”.')+'</div>'+made+connections(f,o);
    }
    if(o.kindOf==='land'&&o.unch)return back+head('Uncharted',o.name)+`<p>Nothing is saved here yet. Ask your AI to look into it, and what it finds appears here as lights, with sources.</p><div class="world-acts"><button type="button" class="primary" data-prompt="${esc(`Start looking into ${o.name.toLowerCase()} for us. Find what matters most, save what you find with its sources, and tell me what you saved.`)}">Start charting ${esc(o.name)}</button></div>`;
    if(o.kind==='task'){const k=o.raw,bad=['failed','missing','paused'].includes(k.health);return back+head('Scheduled task',o.name)+(k.status?`<p${bad?' class="world-callout"':''}>${esc(k.status)}</p>`:'')+facts([['Runs',k.schedule||''],['In',k.app||''],['Keeps current',o.land.name],['Works toward',f.goals.find(g=>g.id===k.goal)?.name||'']])
      +`<div class="world-acts"><button type="button" class="primary" data-view="tools">Open schedules</button><button type="button" class="secondary" ${go('land:'+o.land.id)}>See ${esc(o.land.name)}</button></div>`;}
    if(o.kindOf==='land'&&o.kind==='group')return back+head('More collections',o.name)+'<p>These are kept in AURA and open as usual. They are drawn as one place so the world stays readable.</p>'+`<section><h3>Collections</h3>${(o.members||[]).map(m=>row(`data-collection="${esc(m.id)}"`,m.name,count(m.current,'result'))).join('')}</section>`;
    if(o.kindOf==='land'){const things=o.things.slice().sort((a,b)=>b.seen-a.seen),isCollection=o.kind==='collection';
      return back+head(isCollection?'Collection':'Findings',o.name)+(o.purpose?`<p>${esc(o.purpose)}</p>`:'')+(o.quiet?'<p class="world-callout">This was being kept current and has gone quiet.</p>':'')
        +facts([['Tracked',things.length+(o.more||0)||''],['Findings',o.finds.length||''],['Last checked',when(o.last_checked)],['Kept current by',o.task_linked?'A scheduled task':''],['Given to your AI',o.given?count(o.given,'time'):''],['Used by',o.uses?count(o.uses,'chat or task').replace('chat or tasks','chats and tasks'):'']])
        +`<div class="world-acts">${isCollection?`<button type="button" class="primary" data-collection="${esc(o.id)}">Open the collection</button>`:`<button type="button" class="primary" data-hq-area="${esc(o.id.replace(/^area:/,''))}">Open these findings</button>`}${ask(`Tell me where we stand on ${o.name}: what we know, what changed most recently, and what is worth doing next.`)}</div>`
        +(things.length?`<section><h3>Tracked</h3>${things.slice(0,8).map(x=>row(go('item:'+x.id),x.name,Object.entries(x.raw.fields||{}).slice(0,2).map(([k,v])=>`${k}: ${v}`).join(' · '),x.need?'Review':'',o.hue)).join('')}${things.length>8?`<p class="small-note">and ${things.length-8+(o.more||0)} more in the collection</p>`:''}</section>`:'')
        +(o.finds.length?`<section><h3>Findings</h3>${o.finds.slice(0,8).map(x=>row(go('finding:'+x.id),x.name,FLABEL[x.label]||'','',o.hue)).join('')}</section>`:'');}
    if(o.kind==='item'){const it=o.raw;return back+head(o.land.name,o.name)+(o.need?'<p class="world-callout">Due for review.</p>':'')+facts([...Object.entries(it.fields||{}),['First seen',when(it.first_seen)],['Last checked',when(it.last_seen||it.updated_at)],['Sources',it.sources||''],['Changes noticed',o.changes||'']])
      +spark(it.trend)
      +`<div class="world-acts"><button type="button" class="primary" data-collection="${esc(o.land.id)}">Open in ${esc(o.land.name)}</button>${ask(`Tell me what we know about "${o.name}" in our collection "${o.land.name}": what changed most recently and where it came from.`)}</div>`;}
    if(o.kind==='finding'){const x=o.raw,ref=refOf(x.id)||x.id;return back+head('Finding',x.statement)+`<p class="world-finding-status" data-status="${esc(o.label)}"><span aria-hidden="true">${o.label==='supported'?'●':o.label==='unverified'?'○':o.label==='challenged'?'×':'△'}</span> ${esc(FLABEL[o.label]||o.label)}</p>`+facts([['In',o.land.name],['Since',when(x.at)],['Supporting sources',x.sources||''],['Rests on',(o.tied||[]).map(t=>t.name).join(', ')],['Given to your AI',x.given?count(x.given,'time'):''],['Challenging sources',x.challenges||'']])
      +((x.evidence||[]).length?`<section><h3>Both sides</h3>${x.evidence.map(e=>row('',e.statement,e.relationship==='contradicts'?'Challenges it':'Supports it')).join('')}</section>`:'')
      +`<div class="world-acts">${ref?`<button type="button" class="primary" data-record="${esc(ref)}">Open the finding</button>`:''}${o.label==='challenged'?`<button type="button" class="secondary" data-prompt="${esc(`Two sources disagree about this finding: "${x.statement}". Check both, tell me which holds, and update the finding with what you find.`)}">Settle it</button>`:''}${ask(`Show me the evidence behind this finding and whether it still holds: "${x.statement}"`)}</div>`+origin(f,'finding:'+x.id,{record:x.id});}
    if(o.kind==='goal'){const g=o.raw,ref=refOf(g.id),gaps=goalGaps(f,g);return back+head('Goal',g.name)+(typeof g.target==='number'?`<p>${esc(goalLine(g))}</p><div class="world-meter"><span style="width:${Math.round(goalDone(g)*100)}%"></span></div>`:'')+facts([['Measured by',g.metric||''],['Measurements saved',(g.points||[]).length||''],['Fed by',(g.lands||[]).map(id=>f.lands.find(l=>l.id===id)?.name).filter(Boolean).join(', ')]])+((g.lands||[]).length?'':'<p class="small-note">No collection is linked to this goal yet.</p>')
      +`<div class="world-acts">${ref?`<button type="button" class="primary" data-record="${esc(ref)}">Open the goal</button>`:''}<button type="button" class="secondary" data-prompt="${esc(`Help me plan the next step toward our goal "${g.name}". Use what we already know and say what would move the number most.`)}">Plan the next step</button></div>${gaps.length?`<section><h3>What would move this</h3>${gaps.map(([title,prompt])=>row(prompt?`data-prompt="${esc(prompt)}"`:'',title,prompt?'Ask your AI to do it':'')).join('')}</section>`:''}`;}
    if(o.kind==='decision'){const d=o.raw;return back+head(d.kind==='lesson'?'Lesson':'Decision',d.title)+facts([[d.kind==='lesson'?'Learned':'Made',when(d.at)],['Rests on',(o.basis||[]).map(b=>b.name).slice(0,3).join(' · ')]])+`<div class="world-acts"><button type="button" class="primary" data-record="${esc(refOf(d.id)||d.id)}">${d.kind==='lesson'?'Open the lesson':'Open the decision'}</button></div>`+origin(f,'decision:'+d.id,{record:d.id});}
    return back;
  }

  /* The other views of the same records. Each is plain page content in the current style, so it reads the same in every style. */
  const TABS=[['world','Your world'],['map','Connections'],['timeline','Time'],['effort','AI effort']];
  const compact=n=>n>=1e6?(n/1e6).toFixed(n>=1e7?0:1).replace(/\.0$/,'')+'M':n>=1e3?(n/1e3).toFixed(n>=1e4?0:1).replace(/\.0$/,'')+'K':String(Math.round(n));

  /* Connections, as a list: what fed the selected thing and what it led to. Direct links say how; the rest say how many. */
  function connections(f,sel){
    const L=links(),ix=L.index(f),k=L.key(sel);
    if(!sel)return overviewList(f);
    if(!ix.nodes.has(k))return '<p>No links are recorded for this.</p>';
    const s=L.sides(f,k),kind=n=>L.KIND[n.kind]||n.kind;
    const further=list=>{if(!list.length)return '';const by={};for(const n of list)by[kind(n)]=(by[kind(n)]||0)+1;
      return `<details><summary>Further along: ${esc(Object.entries(by).map(([w,n])=>count(n,w.replace(/^[A-Z](?=[a-z])/,c=>c.toLowerCase()))).join(', '))}</summary>${list.slice(0,60).map(n=>row(go(n.key),n.name,kind(n),'',null,n.kind)).join('')}${list.length>60?`<p class="small-note">and ${list.length-60} more</p>`:''}</details>`;};
    const side=(title,i)=>s.direct[i].length||s.further[i].length?`<section><h3>${title}</h3>${s.direct[i].slice(0,30).map(({node,how})=>row(go(node.key),node.name,how+' · '+kind(node),'',null,node.kind)).join('')}${s.direct[i].length>30?`<p class="small-note">and ${s.direct[i].length-30} more directly</p>`:''}${further(s.further[i])}</section>`:'';
    const kept=s.kept?`<p class="small-note">Also keeps ${count(s.kept,'finding')}${sel.things?.length?` and ${sel.things.length+(sel.more||0)} tracked results`:''}, listed in its details.</p>`:'';
    const body=side('What fed this',0)+side('What it led to',1);
    if(body)return body+kept;
    return (sel.kind==='goal'?`<p>Nothing recorded feeds this goal yet.</p><button class="primary" data-prompt="${esc('Find evidence for our goal “'+sel.name+'”. Check what we have already saved and tell me what supports it and what is still missing.')}">Find evidence for this goal</button>`:'<p>No links are recorded for this yet.</p>')+kept;
  }
  /* With nothing selected: the busiest things in each part of the flow, as a way in. */
  function overviewList(f){
    const L=links(),ix=L.index(f),o=L.overview(f),cols=L.COLUMNS.map(()=>[]);
    for(const [k] of [...o.score].sort((a,b)=>b[1]-a[1])){const n=o.node(k);if(n&&!n.virtual&&L.COLUMN[n.kind]!=null)cols[L.COLUMN[n.kind]].push(n);}
    const body=cols.map((list,i)=>list.length?`<section><h3>${L.COLUMNS[i]}</h3>${list.slice(0,6).map(n=>row(go(n.key),n.name,L.KIND[n.kind],'',null,n.kind)).join('')}${list.length>6?`<p class="small-note">and ${list.length-6} more</p>`:''}</section>`:'').join('');
    return `<p class="small-note">How your work flows: what your AI used, the work it did, what that saved, and the goals it serves. Select anything to follow its whole chain.</p>`+(body||'<p>Nothing is linked yet. Give a chat or scheduled task a collection to keep current, or put a collection and a goal in the same project, and the links appear.</p>');
  }
  /* What the lines can carry. Saved work by default; AI use as each app reported it. */
  const FLOWS=[['saved','Saved work'],['requests','Requests'],['tokens','Reported tokens'],['cost_usd','Reported cost']];
  const amount=(w,flow)=>flow==='saved'?count(w,'saved record'):flow==='requests'?count(w,'request'):flow==='tokens'?compact(w)+' reported tokens':money(w)+' reported';
  /* Connections, as a diagram with room: the selected chain, or the whole flow with conversations folded into one step.
     Columns hold groups like the prototype's Map; thicker lines carried more of what "Lines show" names. */
  function mapView(f){
    const L=links(),ix=L.index(f),k=L.key(ctx?.sel),traced=k&&ix.nodes.has(k),flow=ctx?.flow||'saved',M=L.measures(f);
    let keys,lines,node=key=>ix.nodes.get(key);
    if(traced){const t=L.trace(f,k);keys=[...t.all];lines=t.edges.map(e=>({...e,weight:M.weigh(e,flow)}));}
    else{const o=L.overview(f,flow);node=o.node;keys=[...o.score.keys()];lines=o.edges;}
    const score=new Map();for(const e of lines)for(const x of [e.source,e.target])score.set(x,(score.get(x)||0)+(e.weight||0));
    const cols=L.COLUMNS.map(()=>new Map()),open=ctx?.mapOpen||{},shown=new Set();
    for(const key of keys){const n=node(key);if(!n||L.COLUMN[n.kind]==null)continue;const g=L.group(n),col=cols[L.COLUMN[n.kind]];if(!col.has(g))col.set(g,[]);col.get(g).push(n);}
    const sub=n=>{if(n.kind!=='land')return n.kind==='method'?n.sub||'Library item':n.kind==='session'?n.sub||'AI app session':L.KIND[n.kind];const l=f.lands.find(x=>x.id===n.key.slice(5));return l?landCounts(f,l)||'Area':'Area';};
    const box=n=>n.virtual?`<div class="wm-node plain" data-key="${esc(n.key)}" title="Select an app, Library item or area to see which conversations">${icon('chat')}<span><b>${esc(n.name)}</b><small>Folded together</small></span></div>`
      :`<button type="button" class="wm-node" data-key="${esc(n.key)}" ${go(n.key)} aria-pressed="${n.key===k}">${icon(n.kind)}<span><b>${esc(n.name)}</b><small>${esc(sub(n))}</small></span></button>`;
    const html=cols.map((groups,i)=>{if(!groups.size)return '';
      const parts=[...groups].sort((a,b)=>L.ORDER.indexOf(a[0])-L.ORDER.indexOf(b[0])).map(([g,list])=>{
        list.sort((a,b)=>(b.key===k)-(a.key===k)||(score.get(b.key)||0)-(score.get(a.key)||0)||a.name.localeCompare(b.name));
        const cap=open[g]?list.length:8,visible=list.slice(0,cap),type=list[0].kind==='method'?list[0].sub:null,total=type&&f.library_totals?.[type];visible.forEach(n=>shown.add(n.key));
        return `<div class="wm-group"><h4>${esc(g)}</h4>${visible.map(box).join('')}${list.length>cap||total?`<p class="wm-more">${list.length>cap?`<button type="button" class="text-button" data-map-more="${esc(g)}">+ ${list.length-cap} more used</button>`:''}${total?`<button type="button" class="text-button" data-view="work">${total} in Library</button>`:''}</p>`:''}</div>`;}).join('');
      return `<div class="wm-col"><h3>${L.COLUMNS[i]}</h3>${parts}</div>`;}).filter(Boolean);
    if(ctx){ctx.mapLines=lines.filter(e=>shown.has(e.source)&&shown.has(e.target));ctx.mapNode=node;}
    if(!html.length)return '<p>Nothing is linked yet.</p>';
    const what=FLOWS.find(x=>x[0]===flow)[1].toLowerCase();
    return `<div class="world-acts"><label class="world-flow">Lines show <select id="world-flow">${FLOWS.map(([v,t])=>`<option value="${v}" ${v===flow?'selected':''}>${t}</option>`).join('')}</select></label></div>
      <p class="small-note">${traced?'Everything recorded as flowing into this, and everything it flowed into.':'How your work flows.'} Thicker lines carried more ${esc(what)}${flow==='saved'?' (records saved or changed along them)':' this month'}; dashed lines are recorded links with none along them yet. Point at anything to trace it; point at a line to read it.</p>
      <div class="wm" id="world-map" style="grid-template-columns:repeat(${html.length},minmax(160px,1fr))"><svg class="wm-lines" aria-hidden="true"></svg>${html.join('')}</div>`;
  }
  function drawLinks(){
    const host=$('#world-map');if(!host||!ctx)return;const box=host.getBoundingClientRect(),svg=host.querySelector('svg'),pos={},ix=links().index(ctx.feed),flow=ctx.flow||'saved',live=ctx.liveSet||new Set();
    host.querySelectorAll('[data-key]').forEach(el=>{const r=el.getBoundingClientRect();pos[el.dataset.key]={l:r.left-box.left+host.scrollLeft,r:r.right-box.left+host.scrollLeft,y:(r.top+r.bottom)/2-box.top+host.scrollTop};});
    const lines=ctx.mapLines||[],most=Math.max(1e-9,...lines.map(e=>e.weight||0));
    svg.setAttribute('width',Math.max(host.scrollWidth,box.width));svg.setAttribute('height',Math.max(host.scrollHeight,box.height));
    svg.innerHTML=lines.filter(e=>pos[e.source]&&pos[e.target]).map(e=>{const a=pos[e.source],b=pos[e.target];let d;
      // Same column: a loop out to the right. Otherwise from the facing sides.
      if(Math.abs(a.l-b.l)<4){const x=a.r+28+Math.min(60,Math.abs(a.y-b.y)/6);d=`M${a.r},${a.y} C${x},${a.y} ${x},${b.y} ${b.r},${b.y}`;}
      else{const forward=a.l<b.l,x1=forward?a.r:a.l,x2=forward?b.l:b.r,m=(x1+x2)/2;d=`M${x1},${a.y} C${m},${a.y} ${m},${b.y} ${x2},${b.y}`;}
      const look=ctx.mapNode||(key=>ix.nodes.get(key)),A=look(e.source),B=look(e.target),w=e.weight||0;
      const tip=(e.type?links().sentence(A,e,B):`${A.name} → ${B.name}`)+' · '+(w?amount(w,flow):'nothing recorded along this yet');
      const cls=[w?'':'idle',live.has(e.source)&&live.has(e.target)?'live':''].filter(Boolean).join(' ');
      return `<path d="${d}" data-a="${esc(e.source)}" data-b="${esc(e.target)}"${cls?` class="${cls}"`:''} style="stroke-width:${(w?1.4+5*Math.sqrt(w/most):1).toFixed(1)}px"><title>${esc(tip)}</title></path>`;}).join('');
  }
  /* Pointing at a box traces its chain in the diagram without selecting it, as the prototype's Map did. */
  function highlight(key){
    const host=$('#world-map');if(!host||!ctx)return;const L=links();let lit=null;
    if(key&&key!==L.CHATS&&L.index(ctx.feed).nodes.has(key)){lit=L.trace(ctx.feed,key).all;if([...lit].some(x=>/^(chat|session):/.test(x)))lit.add(L.CHATS);}
    else if(key)lit=new Set([key,...(ctx.mapLines||[]).filter(e=>e.source===key||e.target===key).flatMap(e=>[e.source,e.target])]);
    host.querySelectorAll('[data-key]').forEach(el=>el.classList.toggle('world-dim',!!lit&&!lit.has(el.dataset.key)));
    host.querySelectorAll('path[data-a]').forEach(path=>path.classList.toggle('world-dim',!!lit&&!(lit.has(path.dataset.a)&&lit.has(path.dataset.b))));
  }
  /* Find anything AURA links: areas, results, findings, conversations, files, agents, Library items. */
  function found(f,q){
    q=String(q||'').trim().toLowerCase();if(q.length<2)return '';
    const L=links(),out=[],seen=new Set(),take=n=>{if(!seen.has(n.key)){seen.add(n.key);out.push(n);}};
    for(const n of L.index(f).nodes.values()){if(out.length>=40)break;if(n.name.toLowerCase().includes(q))take(n);}
    for(const l of f.lands)for(const it of l.items)if(out.length<40&&it.title.toLowerCase().includes(q))take({key:'item:'+l.id+'|'+it.id,kind:'item',name:it.title});
    if(!out.length)return `<section class="world-found"><h3>Found</h3><p class="small-note">Nothing named “${esc(q)}”.</p></section>`;
    return `<section class="world-found"><h3>Found</h3>${out.slice(0,12).map(n=>row(go(n.key),n.name,L.KIND[n.kind]||'','',null,n.kind)).join('')}${out.length>12?`<p class="small-note">${out.length-12} more; keep typing to narrow it.</p>`:''}</section>`;
  }

  /* Time: one row per area, a mark for each thing saved at the time it was saved; dense rows become weekly bars. */
  function weekRecords(feed,start){
    const from=Date.parse(start),end=from+7*864e5,events=[];
    const add=(at,key,title,kind)=>{const time=Date.parse(at);if(time>=from&&time<end)events.push({at,time,key,title,kind});};
    for(const land of feed.lands)for(const item of land.items)add(item.first_seen,'item:'+land.id+'|'+item.id,item.title,'Tracked');
    for(const f of feed.findings)if(f.label!=='replaced')add(f.at,'finding:'+f.id,f.statement,'Finding');
    for(const c of feed.changes)add(c.at,'item:'+c.land+'|'+c.item_id,c.title,'Changed');
    for(const d of feed.decisions)add(d.at,'decision:'+d.id,d.title,'Decision');
    for(const g of feed.goals)for(const point of g.points||[])add(point.at,'goal:'+g.id,g.name+' · '+value(point.value,g.unit),'Measured');
    return events.sort((a,b)=>a.time-b.time);
  }
  function timelineView(f){
    const t=d=>Date.parse(d),end=t(f.as_of)||Date.now(),times=[t(f.business.since),...f.lands.flatMap(l=>l.items.map(i=>t(i.first_seen))),...f.findings.map(x=>t(x.at)),...f.changes.map(c=>t(c.at)),...f.goals.flatMap(g=>(g.points||[]).map(p=>t(p.at))),...f.decisions.map(d=>t(d.at))].filter(Number.isFinite);
    const coming=[...(f.tasks||[]).filter(k=>k.next_run).map(k=>[k.next_run,'Next run: '+(k.name||'Scheduled task'),k.land?'task:'+k.id:'']),...(f.deadlines||[]).map(d=>[d.due,'Due: '+d.title,'item:'+d.collection_id+'|'+d.item_id])].filter(c=>t(c[0])>end&&t(c[0])<end+45*864e5);
    const now=end,last=Math.max(now,...coming.map(c=>t(c[0]))),start=Math.min(now-864e5,...times),pct=d=>Math.max(0,Math.min(100,100*((typeof d==='number'?d:t(d))-start)/(last-start))).toFixed(2);
    const mark=(cls,d,title,key)=>Number.isFinite(t(d))?`<button type="button" class="wt-mark ${cls}" style="left:${pct(d)}%" title="${esc(title+' · '+when(d))}" aria-label="${esc(title+', '+when(d))}" ${key?go(key):''}></button>`:'';
    const lane=(label,key,marks)=>`<div class="wt-row"><button type="button" class="wt-label${key?'':' plain'}" ${key?go(key):'tabindex="-1"'}>${esc(label)}</button><div class="wt-strip">${marks}</div></div>`;
    const bar=(date,land,height,title)=>`<button type="button" class="wt-bar" data-world-week="${esc(date)}"${land?` data-week-land="${esc(land)}"`:''} style="left:${pct(t(date)+3.5*864e5)}%;height:${height}%" title="${esc(title)}"></button>`;
    const rows=f.lands.map(land=>{
      const events=[...land.items.map(i=>['item',i.first_seen,'Tracked: '+i.title,'item:'+land.id+'|'+i.id]),
        ...f.findings.filter(x=>x.land===land.id&&x.label!=='replaced').map(x=>['finding',x.at,'Finding: '+x.statement,'finding:'+x.id]),
        ...f.changes.filter(c=>c.land===land.id).map(c=>['change',c.at,'Changed: '+c.title,'item:'+land.id+'|'+c.item_id])];
      if(events.length<=45)return lane(land.name,'land:'+land.id,events.map(e=>mark(...e)).join(''));
      const buckets=new Map();
      for(const [,date] of events){if(!Number.isFinite(t(date)))continue;const monday=new Date(date);monday.setUTCHours(0,0,0,0);monday.setUTCDate(monday.getUTCDate()-(monday.getUTCDay()+6)%7);const key=monday.toISOString();buckets.set(key,(buckets.get(key)||0)+1);}
      return lane(land.name,'land:'+land.id,[...buckets].map(([date,n])=>bar(date,land.id,Math.min(100,22+12*Math.log2(n)),land.name+' · '+count(n,'event')+' · week of '+when(date))).join(''));
    });
    const measured=f.goals.filter(g=>(g.points||[]).length);
    if(measured.length)rows.push(lane('Goals','',measured.map(g=>g.points.map(p=>mark('measure',p.at,`${g.name}: ${value(p.value,g.unit==='USD'?'USD':'')}`,'goal:'+g.id)).join('')).join('')));
    if(f.decisions.length)rows.push(lane('Decisions','',f.decisions.map(d=>mark('decision',d.at,'Decided: '+d.title,'decision:'+d.id)).join('')));
    const weeks=(f.work||[]).filter(w=>w.requests),most=Math.max(1,...weeks.map(w=>w.requests));
    const split=(f.work_by||[]).filter(g=>g.weeks.some(Boolean)),tall=Math.max(1,...split.flatMap(g=>g.weeks));
    for(const g of split){const name=g.kind==='project'?(state.projects||[]).find(p=>p.id===g.id)?.name||'A project':g.kind==='land'?f.lands.find(l=>l.id===g.id)?.name||'A collection':'Other chats';
      rows.push(lane('Work: '+name,g.kind==='land'?'land:'+g.id:'',g.weeks.map((n,i)=>n&&f.work?.[i]?bar(f.work[i].start,'',Math.max(12,Math.round(n/tall*100)),name+', week of '+when(f.work[i].start)+': '+count(n,'request')):'').join('')));}
    if(weeks.length&&!split.length)rows.push(lane('AI requests','',weeks.map(w=>bar(w.start,'',Math.max(12,Math.round(w.requests/most*100)),'Week of '+when(w.start)+': '+count(w.requests,'request'))).join('')));
    if(coming.length)rows.push(lane('Coming up','',`<i class="wt-now" style="left:${pct(now)}%"></i>`+coming.map(c=>mark('change',c[0],c[1],c[2])).join('')));
    if(!rows.length)return '<p class="small-note">Nothing has been saved yet. Each thing your AI saves appears here at the time it was saved.</p>';
    return `<p class="small-note">What was saved, and when. Click a mark to see it on your world, or a bar for that week.</p><div class="wt">${rows.join('')}<div class="wt-row"><span class="wt-label plain"></span><div class="wt-axis"><span>${esc(when(new Date(start).toISOString()))}</span><span>${coming.length?esc(when(new Date(last).toISOString())):'Today'}</span></div></div></div><p class="wt-key small-note"><i class="wt-mark item"></i>tracked <i class="wt-mark finding"></i>finding <i class="wt-mark change"></i>change noticed <i class="wt-mark measure"></i>goal measurement <i class="wt-mark decision"></i>decision</p>`;
  }

  /* AI effort: this month's reported use, one chart grouped one way at a time. Blocks are sized by share. */
  function blocks(items){
    const out=[],place=(list,x,y,w,h,flip)=>{if(!list.length)return;if(list.length===1){out.push({...list[0],x,y,w,h});return;}const total=list.reduce((s,i)=>s+i.value,0);let run=0,cut=0;while(cut<list.length-1&&run+list[cut].value<=total/2){run+=list[cut].value;cut++;}if(!cut){cut=1;run=list[0].value;}const share=run/total;
      if(flip){place(list.slice(0,cut),x,y,w,h*share,!flip);place(list.slice(cut),x,y+h*share,w,h*(1-share),!flip);}else{place(list.slice(0,cut),x,y,w*share,h,!flip);place(list.slice(cut),x+w*share,y,w*(1-share),h,!flip);}};
    place(items.filter(i=>i.value>0).sort((a,b)=>b.value-a.value),0,0,100,100,false);
    return `<div class="we-map">${out.map(b=>`<button type="button" class="we-block" data-effort-key="${esc(b.key)}" aria-pressed="${ctx?.effortOpen===b.key}" style="left:${b.x.toFixed(2)}%;top:${b.y.toFixed(2)}%;width:${b.w.toFixed(2)}%;height:${b.h.toFixed(2)}%;--we-h:${Math.round(b.hue)}" title="${esc(b.name+' · '+b.sub)}"><b>${esc(b.name)}</b><small>${esc(b.sub)}</small></button>`).join('')}</div>`;
  }
  /* What a conversation saved, from the links AURA noted while it ran. */
  function produced(f,chatId){
    const n={finding:0,item:0,decision:0,other:0},ix=links().index(f);
    for(const e of ix.from.get('chat:'+chatId)||[])if(e.type==='saved'||e.type==='updated'){const kind=ix.nodes.get(e.target)?.kind;n[kind in n?kind:'other']++;}
    return [n.finding?count(n.finding,'finding'):'',n.item?count(n.item,'result')+' changed':'',n.decision?count(n.decision,'decision'):'',n.other?count(n.other,'other saved item'):''].filter(Boolean).join(', ');
  }
  function effortView(f,sel){
    const L=links(),metric=ctx?.metric||'requests',by=ctx?.effortBy||'app',all=(f.effort||[]).flatMap(g=>(g.chats||[]).map(c=>({...c,group:g})));
    let chats=all,note='';
    if(sel){const t=L.trace(f,L.key(sel));chats=all.filter(c=>c.id&&t.all.has('chat:'+c.id));if(sel.kind==='method')note='Tokens and cost are reported for the whole requests this was given to.';}
    if(!chats.length)return sel?'<p>No AI use this month is recorded for anything in this chain.</p>':'<p>No AI requests have been recorded this month.</p>';
    const landName=id=>f.lands.find(l=>l.id===id)?.name,projectName=id=>(state.projects||[]).find(p=>p.id===id)?.name;
    const keyOf=c=>by==='model'?c.model||'Model unreported':by==='work'?(c.group.kind==='land'?'land:'+c.group.id:c.group.kind==='project'?'project:'+c.group.id:'other'):c.agent||'Unnamed app';
    const nameOf=k=>by!=='work'?k:k==='other'?'Not tied to anything':k.startsWith('land:')?landName(k.slice(5))||'A collection':projectName(k.slice(8))||'A project';
    const groups=new Map();
    for(const c of chats){const k=keyOf(c);if(!groups.has(k))groups.set(k,{key:k,name:nameOf(k),requests:0,tokens:0,cost_usd:0,missing_costs:0,missing_tokens:0,chats:[]});const g=groups.get(k);for(const field of ['requests','tokens','cost_usd','missing_costs','missing_tokens'])g[field]+=c[field]||0;g.chats.push(c);}
    const sum=field=>chats.reduce((s,c)=>s+(c[field]||0),0),requests=sum('requests'),tokens=sum('tokens'),cost=sum('cost_usd'),noCost=sum('missing_costs');
    const sub=g=>[count(g.requests,'request'),g.tokens?compact(g.tokens)+' tokens':'',g.missing_costs!==g.requests&&g.cost_usd?money(g.cost_usd):'',g.missing_costs?'cost not reported for '+g.missing_costs:''].filter(Boolean).join(' · ');
    const list=[...groups.values()].map(g=>({...g,sub:sub(g),value:g[metric]||0,hue:g.key.startsWith('land:')?(hueOf(g.key.slice(5))??hash(g.key)%360):hash(g.key)%360}));
    if(ctx)ctx.effortGroups=new Map(list.map(g=>[g.key,{chats:g.chats.filter(c=>c.id).map(c=>c.id),apps:[...new Set(g.chats.map(c=>c.agent).filter(Boolean))].map(n=>'app:'+n),node:by==='app'?'app:'+g.key:by==='work'&&g.key!=='other'?g.key:null}]));
    const chart=list.some(g=>g.value>0)?blocks(list):'<p class="small-note">Nothing reported for this measure. Try another.</p>';
    const open=list.find(g=>g.key===ctx?.effortOpen),follow=open&&ctx.effortGroups.get(open.key)?.node,detail=open?`<section><h3>${esc(open.name)}</h3>${follow?`<button type="button" class="text-button" data-effort-follow="${esc(follow)}">Follow in Connections</button>`:''}${open.chats.sort((a,b)=>b[metric]-a[metric]).map(c=>row(c.id?`data-edit-chat="${esc(c.id)}"`:'',c.title,[by!=='app'?c.agent:'',by!=='model'?c.model:'',count(c.requests,'request'),c.tokens?compact(c.tokens)+' tokens':'',c.missing_costs!==c.requests&&c.cost_usd?money(c.cost_usd):'',c.id?produced(f,c.id):''].filter(Boolean).join(' · '))).join('')}</section>`:'<p class="small-note">Select a block to see the conversations behind it and what they saved.</p>';
    const select=(id,label,options,current)=>`<label>${label} <select id="${id}">${options.map(([k,t])=>`<option value="${k}" ${k===current?'selected':''}>${t}</option>`).join('')}</select></label>`;
    return `<div class="world-acts">${select('world-effort-by','Group by',[['app','AI app'],['work','What it was for'],['model','Model']],by)}${select('world-effort-metric','Size by',[['requests','Requests'],['tokens','Reported tokens'],['cost_usd','Reported cost']],metric)}</div>
      <p class="small-note">${count(requests,'request')} this month${tokens?' · '+compact(tokens)+' reported tokens':''}${cost?' · '+money(cost)+' reported':''}${noCost?' · cost not reported for '+noCost:''}. Only what each app reported is counted.${note?' '+note:''}</p>`+chart+detail;
  }

  /* The year poster: the world, the year's outcomes, and each day something was saved. It is made from Share. */
  function posterData(f){
    const today=new Date(f.as_of),year=today.getFullYear();
    const day=date=>{const d=new Date(date);return d.getFullYear()===year?(Date.UTC(year,d.getMonth(),d.getDate())-Date.UTC(year,0,1))/864e5:-1;};
    const counts=Array(day(f.as_of)+1).fill(0);
    const tally=dates=>{let n=0;for(const date of dates){const i=day(date);if(i>=0&&i<counts.length){counts[i]++;n++;}}return n;};
    const stats=[['Tracked this year',tally(f.lands.flatMap(l=>l.items.map(i=>i.first_seen)))],['Findings this year',tally(f.findings.filter(x=>x.label!=='replaced').map(x=>x.at))],['Changes noticed',tally(f.changes.map(c=>c.at))]];
    const measured=f.goals.filter(g=>typeof g.target==='number');
    if(measured.length)stats.push(['Goals reached',measured.filter(g=>g.reached).length+' of '+measured.length]);
    return {year,counts,stats};
  }
  function drawPoster(f,styleFrom){
    const {year,counts,stats}=posterData(f),canvas=document.createElement('canvas'),width=canvas.width=1080;canvas.height=1260;
    const pen=canvas.getContext('2d'),style=getComputedStyle(styleFrom),paper=style.getPropertyValue('--paper').trim()||'#15191c',ink=style.color,accent=style.getPropertyValue('--accent').trim()||ink;
    pen.fillStyle=paper;pen.fillRect(0,0,width,canvas.height);
    const image=world()?.available&&world().model()?world().card():null;
    if(image)pen.drawImage(image,180,100,720,900,310,0,460,505);
    const line=(text,y,size,color=ink)=>{pen.fillStyle=color;pen.font='600 '+size+'px '+style.fontFamily;pen.fillText(text,64,y,width-128);};
    line(year+' with AURA',510,28,accent);line(f.business.name,590,62);
    stats.forEach(([k,v],i)=>line(k+'   '+v,665+i*58,34));
    line('Saved records by day',956,30);
    const max=Math.max(1,...counts),offset=new Date(year,0,1).getDay();
    counts.forEach((n,i)=>{const d=i+offset;pen.globalAlpha=n?.4+.6*n/max:.12;pen.fillStyle=n?accent:ink;pen.fillRect(64+Math.floor(d/7)*18,985+(d%7)*23,14,18);});
    pen.globalAlpha=1;line('January – '+new Date(f.as_of).toLocaleDateString(undefined,{month:'long',day:'numeric'}),1200,24);
    canvas.setAttribute('role','img');canvas.setAttribute('aria-label',f.business.name+' · '+year+' year poster');
    return canvas;
  }

  /* A selection: a record the world draws, or anything else the recorded links know about. */
  function recordFor(feed,kind,id){
    const goal=kind==='goal'&&feed.goals.find(g=>g.id===id);
    if(goal)return {kind,id,name:goal.name,raw:goal};
    const decision=kind==='decision'&&feed.decisions.find(d=>d.id===id);
    if(decision)return {kind,id,name:decision.title,raw:decision};
    const area=kind==='land'&&feed.uncharted?.find(a=>'new:'+a.id===id);
    if(area)return {...area,id,kindOf:'land',unch:true};
    if(['item','finding','task','land'].includes(kind)){
      const finding=kind==='finding'&&feed.findings.find(f=>f.id===id),task=kind==='task'&&feed.tasks?.find(t=>t.id===id);
      for(const land of feed.lands){
        if(kind==='finding'&&finding?.land!==land.id)continue;
        if(kind==='task'&&task?.land!==land.id)continue;
        if(kind==='land'&&land.id!==id)continue;
        if(kind==='item'&&!id.startsWith(land.id+'|'))continue;
        const things=land.items.map(raw=>({kind:'item',id:land.id+'|'+raw.id,name:raw.title,land,raw,need:raw.needs_review,seen:Date.parse(raw.last_seen||raw.first_seen)}));
        const finds=feed.findings.filter(f=>f.land===land.id&&f.label!=='replaced').map(raw=>({kind:'finding',id:raw.id,name:raw.statement,label:raw.label,raw,land}));
        if(kind==='land')return {...land,kindOf:'land',things,finds};
        if(kind==='task')return {kind,id,name:task.name,raw:task,land};
        const found=[...things,...finds].find(x=>x.kind===kind&&x.id===id);
        if(found)return found;
      }
    }
    const node=links().index(feed).nodes.get(kind+':'+id);
    return node?{kind,id,name:node.name,raw:node,relationship:true}:null;
  }

  function savePlace(){
    if(!ctx)return;
    try{sessionStorage.setItem('aura-view:'+JSON.stringify([ctx.workspace,ctx.business]),JSON.stringify({tab:ctx.tab,selection:ctx.sel?{kind:ctx.sel.kindOf||ctx.sel.kind,id:ctx.sel.id}:null,camera:world()?.cameraState?.(),compare:ctx.compare,timeMode:ctx.timeMode}));}
    catch{/* Browsers may disable session storage. Navigation still works. */}
  }
  function selectionChanged(selection,remember=true){
    if(remember&&ctx.sel&&selection&&(ctx.sel.id!==selection.id||ctx.sel.kind!==selection.kind)){
      ctx.history=[...(ctx.history||[]),{kind:ctx.sel.kindOf||ctx.sel.kind,id:ctx.sel.id,camera:world()?.cameraState?.(),tab:ctx.tab}].slice(-20);
    }
    ctx.sel=selection;paintSide();
  }
  function selectRecord(kind,id,fly=true){
    const selection=recordFor(ctx.feed,kind,id);
    if(!selection){ctx.sel=null;world()?.release?.();paintSide();return;}
    const camera=world()?.cameraState?.();
    ctx.restoring=!fly;
    world()?.filter?.(ctx.filter);
    if(world()?.available&&world().focus(kind,id,fly)){ctx.restoring=false;return;}
    // Not drawn on the world (a conversation, file, agent…): keep the camera where it is and light the places its chain touches.
    world()?.release?.();
    selectionChanged(selection,fly);
    if(fly&&ctx.history?.length)ctx.history.at(-1).camera=camera;
    const lands=relatedFeed(ctx.feed,selection).lands.map(l=>l.id);
    world()?.filter?.({lands,scoped:true});
    if(fly)world()?.reveal?.(lands);
    ctx.restoring=false;
  }
  /* The same feed, narrowed to the places a selection touches. An area is itself; anything else is its chain's places. */
  function relatedFeed(feed,selection){
    if(!selection)return feed;
    const areas=new Set(selection.kindOf==='land'?[selection.id]:landsFor(feed,links().key(selection)));
    if(!areas.size&&selection.land?.id)areas.add(selection.land.id);
    const lands=feed.lands.filter(l=>areas.has(l.id)),findings=feed.findings.filter(x=>areas.has(x.land)||x.lands?.some(id=>areas.has(id))),findingIds=new Set(findings.map(f=>f.id));
    return {...feed,lands,findings,changes:feed.changes.filter(c=>areas.has(c.land)),
      decisions:feed.decisions.filter(d=>d.id===selection.id||d.basis?.some(id=>findingIds.has(id))),
      goals:feed.goals.filter(g=>g.id===selection.id||g.lands?.some(id=>areas.has(id))),
      tasks:(feed.tasks||[]).filter(t=>t.goal===selection.id||areas.has(t.land)),
      deadlines:(feed.deadlines||[]).filter(d=>areas.has(d.collection_id)),
      work_by:(feed.work_by||[]).filter(g=>g.kind==='land'&&areas.has(g.id)),work:(feed.work||[]).map(w=>({...w,requests:0}))};
  }
  function evidenceRows(finding){
    const labels={supports:'Supports this finding',derived_from:'This finding was derived from',extends:'Extends this finding',contradicts:'Challenges this finding'};
    return (finding.source_details||[]).map(e=>'<div class="world-evidence">'+row(e.record?`data-record="${esc(e.record)}"`:'',e.statement,labels[e.relationship]||'Linked evidence')
      +(e.sources||[]).map(source=>row(source.record?`data-record="${esc(source.record)}"`:'',source.title,'Source cited by this evidence')).join('')+'</div>').join('');
  }
  /* Everything saved or measured after a date, from the saved records and their kept history only. */
  function changesSince(feed,date){
    const since=Date.parse(date),end=Date.parse(feed.as_of);
    if(!Number.isFinite(since)||since>end)return [];
    const changes=[];
    for(const land of feed.lands)for(const item of land.items){
      const key='item:'+land.id+'|'+item.id;
      if(Date.parse(item.first_seen)>since)changes.push({key,land:land.id,title:item.title,detail:'Added to '+land.name,at:item.first_seen});
      const points=(item.history||[]).filter(p=>Number.isFinite(Date.parse(p.at))).sort((a,b)=>Date.parse(a.at)-Date.parse(b.at));
      const before=points.filter(p=>Date.parse(p.at)<=since).at(-1),after=points.filter(p=>Date.parse(p.at)>since&&Date.parse(p.at)<=end).at(-1);
      if(before&&after)for(const [field,current] of Object.entries(after.values)){const previous=before.values[field];
        if(typeof previous==='number'&&typeof current==='number'&&previous!==current)changes.push({key,land:land.id,title:item.title,detail:field+': '+value(previous)+' → '+value(current),at:after.at});}
    }
    for(const f of feed.findings){
      if(Date.parse(f.at)>since)changes.push({key:'finding:'+f.id,land:f.land,title:f.statement,detail:f.label==='replaced'?'Finding superseded':'New finding · '+(FLABEL[f.label]||f.label),at:f.at});
      else if(Date.parse(f.updated_at)>since)changes.push({key:'finding:'+f.id,land:f.land,title:f.statement,detail:'Finding updated · '+(FLABEL[f.label]||f.label),at:f.updated_at});
    }
    for(const c of feed.changes)if(Date.parse(c.at)>since)changes.push({key:'item:'+c.land+'|'+c.item_id,land:c.land,title:c.title,detail:c.reason||c.kind||'Saved details changed',at:c.at});
    for(const g of feed.goals){
      const points=(g.points||[]).slice().sort((a,b)=>Date.parse(a.at)-Date.parse(b.at)),before=points.filter(p=>Date.parse(p.at)<=since).at(-1),after=points.filter(p=>Date.parse(p.at)>since).at(-1);
      if(after&&(!before||before.value!==after.value))changes.push({key:'goal:'+g.id,title:g.name,detail:before?value(before.value,g.unit==='USD'?'USD':'')+' → '+value(after.value,g.unit):'First measurement: '+value(after.value,g.unit),at:after.at});
    }
    for(const d of feed.decisions)if(Date.parse(d.at)>since)changes.push({key:'decision:'+d.id,title:d.title,detail:d.kind==='lesson'?'Lesson saved':'Decision recorded',at:d.at});
    return changes.sort((a,b)=>Date.parse(b.at)-Date.parse(a.at));
  }
  function comparisonFeed(feed,selection){
    if(!selection)return feed;
    if(selection.kind==='goal')return {...feed,goals:feed.goals.filter(g=>g.id===selection.id)};
    if(!['item','finding'].includes(selection.kind))return feed;
    const itemKeys=new Set(selection.kind==='item'?[selection.id]:(selection.raw.related_items||(selection.raw.items||[]).map(id=>({id,land:selection.land.id}))).map(ref=>ref.land+'|'+ref.id));
    const findings=feed.findings.filter(f=>f.id===selection.id||(f.related_items||(f.items||[]).map(id=>({land:f.land,id}))).some(ref=>itemKeys.has(ref.land+'|'+ref.id)));
    const ids=new Set(findings.map(f=>f.id));
    return {...feed,lands:feed.lands.map(l=>({...l,items:l.items.filter(item=>itemKeys.has(l.id+'|'+item.id))})),findings,changes:feed.changes.filter(c=>itemKeys.has(c.land+'|'+c.item_id)),goals:[],decisions:feed.decisions.filter(d=>d.basis?.some(id=>ids.has(id)))};
  }
  const sinceDate=f=>ctx?.compare||(ctx?.since||fallbackSince(f)).slice(0,10);
  function comparisonView(feed){
    const date=sinceDate(feed),changes=changesSince(comparisonFeed(feed,ctx.sel),date),visible=changes.slice(0,ctx.compareLimit||60);
    const entries=visible.map(c=>{const [kind,...id]=c.key.split(':');return row(recordFor(ctx.feed,kind,id.join(':'))?go(c.key):c.land?`data-collection="${esc(c.land)}"`:'',c.title,c.detail,when(c.at),c.land?hueOf(c.land):null,kind);}).join('');
    return `<section class="world-comparison"><label>Changes since <input id="world-compare-date" type="date" value="${esc(date)}" max="${esc(feed.as_of.slice(0,10))}"></label>
      <p class="small-note">Lit on the world. Earlier values appear where a dated measurement was kept.</p>
      ${changes.length?`<button type="button" class="text-button" data-world-fly>Fly through them</button>`:''}
      ${entries||'<p>No saved changes in this selection for this period.</p>'}
      ${changes.length>visible.length?`<button class="text-button" data-world-more-changes>Show more changes (${changes.length-visible.length} remaining)</button>`:''}</section>`;
  }

  function showTab(tab){
    if(!ctx||!$('#world-stage'))return;ctx.tab=tab;ctx.expanded=false;
    document.querySelectorAll('[data-world-tab]').forEach(button=>{const on=button.dataset.worldTab===tab;button.setAttribute('aria-selected',String(on));button.tabIndex=on?0:-1;});
    world()?.lens?.(tab==='map'?'links':tab==='effort'?'effort':'');paintSide();
  }
  /* The last visit and the tour are kept with the other aura choices, so they follow the person between browsers. */
  const remember=patch=>{state.data.aura_preferences={...(state.data.aura_preferences||{}),...patch};api('/api/preferences',{business:state.business,aura:patch}).then(()=>{hq().paintMark?.();hq().paint?.(true);}).catch(()=>{});};
  function mountWorld(){
    const host=$('#world-stage');if(!host||!ctx)return;
    let ok=false;try{ok=!!world()?.available&&world().mount(host,ctx.feed,{select:o=>{if(ctx){world()?.filter?.(ctx.filter);selectionChanged(o,!ctx.restoring);}},seen:ctx.seen,toured:ctx.toured,remember,running:runningNow,poster:()=>drawPoster(ctx.feed,host),go:key=>{const [kind,...rest]=String(key).split(':');selectRecord(kind,rest.join(':'));},links:()=>ctx?.feed});if(ok)world().filter(ctx.filter);}catch(error){console.error(error);ok=false;}
    if(!ok)host.innerHTML='<p class="world-fallback">This computer cannot draw the 3D world. Everything in it is listed beside this, and in the other views.</p>';
    ctx.seen=ctx.feed.as_of;ctx.toured=true;world()?.lens?.(ctx.tab==='map'?'links':ctx.tab==='effort'?'effort':'');paintSide();
  }
  function paintChrome(){
    if(!ctx||!$('#world-tools'))return;const {top,keys}=tools(ctx.feed);
    if(ctx.toolsHTML!==top){const q=$('#world-q')?.value||'';$('#world-tools').innerHTML=top;ctx.toolsHTML=top;if(q&&$('#world-q'))$('#world-q').value=q;}
    if(ctx.keysHTML!==keys){$('#world-keys').innerHTML=keys;ctx.keysHTML=keys;}
  }
  /* One line at the top for what just arrived: what a piece of work saved, a goal reached, or new saved work. */
  function notices(){
    const out=[];
    for(const [i,r] of (ctx.receipts||[]).entries())out.push(`<div class="world-outcome" role="status">${esc(r.text)} <button type="button" class="text-button" data-world-receipt="${i}">${ctx.receiptOpen===i?'Hide':r.items.length===1?'See it':'See them'}</button> <button type="button" class="text-button" data-world-dismiss>Dismiss</button></div>`
      +(ctx.receiptOpen===i?`<section>${r.items.slice(0,20).map(k=>{const [kind,...id]=k.split(':'),o=recordFor(ctx.feed,kind,id.join(':'));return o?row(go(k),o.name,links().KIND[kind]||kind):'';}).join('')}</section>`:''));
    if(ctx.outcome)out.push(`<div class="world-outcome" role="status">${esc(ctx.outcome)} <button type="button" class="text-button" data-world-dismiss>Dismiss</button></div>`);
    if(ctx.arrivedSince&&!out.length)out.push('<button class="world-arrived text-button" data-world-arrived>New saved work · See what changed</button>');
    return out.join('');
  }
  /* The list beside the world follows the lens: the world's own list, or the same records as connections, time or effort. */
  function paintSide(){
    const host=$('#world-side');if(!host||!ctx)return;const f=ctx.feed,tab=ctx.tab,scoped=relatedFeed(f,ctx.sel);
    const scope=ctx.sel&&tab!=='world'?`<p><b>${esc(ctx.sel.name)}</b> <button class="text-button" data-world-details>Details</button> <button class="text-button" data-world-clear>Show everything</button></p>`:'';
    const expand=tab!=='world'?`<button type="button" class="text-button" data-world-expand>${ctx.expanded?'Back to the world':'Give it the whole screen'}</button>`:'';
    const back=ctx.history?.length&&ctx.sel?'<button class="text-button" data-world-previous>‹ Back</button>':'';
    host.parentElement.classList.toggle('world-expanded',!!ctx.expanded);host.parentElement.classList.toggle('world-focused',!!ctx.sel);
    let body;
    if(tab==='map')body='<h2>Connections</h2>'+scope+(ctx.expanded?mapView(f)+(ctx.sel?connections(f,ctx.sel):''):connections(f,ctx.sel));
    else if(tab==='timeline'){
      const mode=ctx.timeMode||'since';
      body='<h2>Time</h2>'+scope+`<div class="world-time-modes"><button type="button" data-world-time="since" aria-pressed="${mode==='since'}">What changed</button><button type="button" data-world-time="timeline" aria-pressed="${mode==='timeline'}">Timeline</button></div>`+(mode==='since'?comparisonView(scoped):timelineView(scoped));
      if(ctx.week&&mode==='timeline'){const list=weekRecords(scoped,ctx.week);body+=`<section id="world-week" tabindex="-1"><h3>Week of ${esc(when(ctx.week))}</h3><button class="text-button" data-world-end-week>Show all dates</button>${list.map(r=>row(go(r.key),r.title,r.kind,when(r.at),null,r.key.split(':')[0])).join('')||'<p>No saved records in this selection that week.</p>'}</section>`;}
    }
    else if(tab==='effort')body='<h2>AI effort this month</h2>'+scope+effortView(f,ctx.sel);
    else body=ctx.sel?selected(f,ctx.sel)+`<div class="world-acts"><button type="button" class="text-button" data-world-tab="map">Follow its connections</button><button type="button" class="text-button" data-world-compare>Changes over time</button></div>`+(ctx.sel.kind==='finding'&&ctx.sel.raw.source_details?.length?'<section><h3>Evidence and sources</h3>'+evidenceRows(ctx.sel.raw)+'</section>':''):home(f);
    if(tab==='map'&&ctx.expanded)ctx.liveSet=links().live(f,runningNow().map(r=>r.id));
    host.innerHTML=notices()+found(f,ctx.q)+back+expand+body;
    // The world lights what this lens is talking about: a period's changes, a week, or a piece of work's output.
    const receipt=ctx.receipts?.[ctx.receiptOpen];
    if(receipt)world()?.compare?.(receipt.items);
    else if(tab==='timeline'&&(ctx.timeMode||'since')==='since')world()?.compare?.(changesSince(comparisonFeed(scoped,ctx.sel),sinceDate(f)).map(c=>c.key));
    else if(tab==='timeline'&&ctx.week)world()?.compare?.(weekRecords(scoped,ctx.week).map(r=>r.key));
    else world()?.compare?.(null);
    ctx.mapObserver?.disconnect();
    const map=host.querySelector('#world-map');
    if(map&&ctx.expanded){ctx.mapObserver=new ResizeObserver(()=>requestAnimationFrame(drawLinks));ctx.mapObserver.observe(map);}
    savePlace();paintChrome();
  }
  /* What a piece of work saved since the last read, from the links AURA noted while it ran. */
  function receipts(previous,feed){
    const L=links(),before=new Set((previous.relationships?.edges||[]).filter(e=>e.type==='saved').map(e=>e.source+'>'+e.target)),by=new Map();
    const add=(source,target,kind)=>{if(!by.has(source))by.set(source,{items:new Set(),kinds:{}});const r=by.get(source);if(!r.items.has(target)){r.items.add(target);r.kinds[kind]=(r.kinds[kind]||0)+1;}};
    const ix=L.index(feed);
    for(const e of feed.relationships?.edges||[])if(e.type==='saved'&&!before.has(e.source+'>'+e.target))add(e.source,e.target,ix.nodes.get(e.target)?.kind==='land'?'collection':ix.nodes.get(e.target)?.kind||'record');
    for(const c of feed.changes)if(c.by&&c.at>previous.as_of)add(c.by.kind+':'+c.by.id,'item:'+c.land+'|'+c.item_id,'changed');
    const words={finding:['finding','saved'],decision:['decision','saved'],collection:['collection','saved'],record:['record','saved'],item:['result','saved'],changed:['tracked result','changed']};
    return [...by].map(([source,r])=>{const saved=[],changed=[];for(const [k,n] of Object.entries(r.kinds)){const [noun,verb]=words[k]||['record','saved'];(verb==='changed'?changed:saved).push(count(n,noun));}
      const node=ix.nodes.get(source),app=(ix.into.get(source)||[]).map(e=>ix.nodes.get(e.source)).find(n=>n?.kind==='app')?.name,title=node?.kind==='chat'&&node.name?` · “${node.name.length>48?node.name.slice(0,47)+'…':node.name}”`:'';
      const who=app||(node?.kind==='session'?node.sub:node?.kind==='chat'?'Your AI':node?.name)||'Your AI';
      return {source,items:[...r.items],text:`${who} ${[saved.length?'saved '+saved.join(', '):'',changed.length?'changed '+changed.join(', '):''].filter(Boolean).join(' and ')}${title}.`};});
  }
  function updateWorld(feed,quiet=false){
    const previous=ctx.feed,selection=ctx.sel,outcomes=[];
    for(const goal of feed.goals){const old=previous.goals.find(g=>g.id===goal.id);if(old&&!old.reached&&goal.reached)outcomes.push('Target reached · '+goal.name);}
    if(selection?.kind==='item'&&selection.raw.needs_review){const updated=recordFor(feed,'item',selection.id);if(updated&&!updated.raw.needs_review)outcomes.push('Review cleared · '+updated.name);}
    if(selection?.kind==='finding'){const updated=feed.findings.find(f=>f.id===selection.id);if(updated&&updated.label!==selection.raw.label)outcomes.push((FLABEL[updated.label]||updated.label)+' · '+updated.statement);}
    if(outcomes.length)ctx.outcome=outcomes.join(' · ');
    const arrived=quiet?[]:receipts(previous,feed);
    if(arrived.length)ctx.receipts=[...(ctx.receipts||[]),...arrived].slice(-3);
    else if(changesSince(relatedFeed(feed,selection),previous.as_of).length)ctx.arrivedSince=previous.as_of;
    ctx.feed=feed;world()?.update?.(feed);
    if(selection)selectRecord(selection.kindOf||selection.kind,selection.id,false);else paintSide();
  }

  /* Opening the aura goes to its own section, like Knowledge or Files. */
  async function open(){state.view='aura';await render();if(typeof recordShellRoute==='function')recordShellRoute();if(typeof renderShell==='function')await renderShell();}
  const fetchWorld=(business,known)=>api('/api/world?business='+encodeURIComponent(business)+(known?'&known='+encodeURIComponent(known):''));
  async function draw(view,current=()=>true){
    const business=state.business;
    if(ctx?.business===business&&ctx.workspace===state.data.workspace&&view.querySelector('#world-stage')){
      const owner=ctx,feed=await fetchWorld(business,ctx.feed.revision);
      if(ctx!==owner||!current()||state.view!=='aura'||world()?.replaying?.())return;
      ctx.checked=Date.now();if(!feed.unchanged)updateWorld(feed);return;
    }
    ctx?.mapObserver?.disconnect();
    view.innerHTML='<div class="aura-view world-view"><p class="world-fallback">Drawing your world…</p></div>';
    const feed=await fetchWorld(business);
    if(!feed||business!==state.business||!current()||state.view!=='aura')return;
    const previous=ctx?.business===business&&ctx.workspace===state.data.workspace?ctx:null;
    const prefs=state.data?.aura_preferences||{};ctx={business,workspace:state.data.workspace,feed,checked:Date.now(),sel:null,tab:'world',seen:prefs.seen||null,since:prefs.seen||null,toured:!!prefs.toured,filter:{lands:[],needs:false,by:''}};
    let resume;
    if(!previous){
      try{resume=JSON.parse(sessionStorage.getItem('aura-view:'+JSON.stringify([state.data.workspace,business]))||'null');}catch{}
      if(resume){if(TABS.some(([key])=>key===resume.tab))ctx.tab=resume.tab;if(resume.selection)ctx.sel=recordFor(feed,resume.selection.kind,resume.selection.id);if(/^\d{4}-\d{2}-\d{2}$/.test(resume.compare||''))ctx.compare=resume.compare;if(['since','timeline'].includes(resume.timeMode))ctx.timeMode=resume.timeMode;}
    }
    if(previous){for(const key of ['tab','expanded','metric','effortBy','flow','origins','mapOpen','chat','filter','since','compare','timeMode','history','receipts','arrivedSince'])ctx[key]=previous[key];if(previous.sel)ctx.sel=recordFor(feed,previous.sel.kindOf||previous.sel.kind,previous.sel.id);}
    view.innerHTML=`<div class="aura-view world-view"><div class="world-main"><div class="world-stage" id="world-stage"><p class="world-fallback">Drawing your world…</p></div><div class="world-top"><div class="world-tabs" role="tablist" aria-label="Ways to look at your world">${TABS.map(([k,l])=>`<button type="button" role="tab" data-world-tab="${k}" tabindex="${k===ctx.tab?0:-1}" aria-selected="${k===ctx.tab}">${l}</button>`).join('')}</div><div class="world-tools" id="world-tools"></div></div><div class="world-keys" id="world-keys"></div><div class="world-ask"><button type="button" id="world-chat">Open chat</button></div></div><aside class="world-side" id="world-side" aria-label="What is in your world"></aside></div>`;
    paintSide();
    const owner=ctx;
    try{if(!world())await import('/workspace-world.js');}catch{/* The readable view works without the renderer. */}
    if(ctx===owner&&current()&&state.view==='aura'){
      const selection=ctx.sel;mountWorld();world()?.setEffortMetric?.(ctx.metric||'requests');
      if(selection)selectRecord(selection.kindOf||selection.kind,selection.id,false);
      world()?.restoreCamera?.(resume?.camera);
    }
  }

  function setChat(open){ctx.chat=open;document.body.classList.toggle('world-chat-open',open);$('#main').inert=!open;if(open)$('#request').focus();else $('#world-chat')?.focus();}
  function openChat(promptText=''){
    const o=ctx.sel,box=$('#request');let reference;
    if(o?.kindOf==='land'&&o.kind==='collection')reference={kind:'collection',id:o.id,label:o.name};
    else if(o?.kind==='item'){reference={kind:'collection',id:o.land.id,label:o.land.name};if(!promptText)promptText='About “'+o.name+'” in '+o.land.name+': ';}
    else if(o&&['file','record','method'].includes(o.kind))reference={kind:o.kind==='method'?'library':o.kind,id:o.raw?.action?.record||o.raw?.action?.file||o.raw?.action?.method||o.id,label:o.name};
    else if(o?.raw&&['goal','finding','decision'].includes(o.kind)){const ref=o.raw.record||refOf(o.raw.id);if(ref)reference={kind:'record',id:ref,label:o.name};else if(!promptText)promptText='About “'+o.name+'”: ';}
    if(o&&!reference&&!promptText)promptText='About “'+o.name+'”: ';
    if(reference&&!window.auraCompose?.add(reference)){setChat(true);return;}
    if(promptText&&!box.value.endsWith(promptText)){box.value+=(box.value.trim()?'\n\n':'')+promptText;box.dispatchEvent(new Event('input',{bubbles:true}));}
    setChat(true);
  }

  // In the aura the sidebar's own button opens and tucks it without changing the person's saved choice for the rest of AURA.
  document.addEventListener('click',e=>{if(!e.target.closest('#sidebar-collapse')||!document.body.classList.contains('in-aura')||matchMedia('(max-width:600px)').matches)return;e.stopImmediatePropagation();e.preventDefault();state.auraSidebarOpen=!state.auraSidebarOpen;document.body.classList.toggle('sidebar-collapsed',!state.auraSidebarOpen);},true);
  document.addEventListener('click',event=>{
    if(state.view!=='aura'||!ctx||ctx.business!==state.business)return;
    if(event.target.closest('#world-chat-back'))setChat(false);
    const button=event.target.closest('.aura-view [data-prompt], #world-chat');
    if(!button)return;
    event.stopImmediatePropagation();openChat(button.dataset.prompt);
  },true);

  // Refresh when a chat finishes, and otherwise once a minute; an unchanged world is not sent again.
  setInterval(async()=>{
    const current=ctx;
    if(!current||current.business!==state.business||current.workspace!==state.data.workspace||state.view!=='aura'||!$('#world-stage')||document.hidden)return;
    const active=new Set(runningNow().map(job=>job.id)),changed=!current.running||active.size!==current.running.size||[...active].some(id=>!current.running.has(id));
    if(current.running&&[...current.running].some(id=>!active.has(id)))current.needsRefresh=true;
    current.running=active;
    if(changed&&current.tab==='map'&&current.expanded)paintSide();
    const wait=active.size?(current.slow?15000:5000):60000;
    if(current.refreshing||(!current.needsRefresh&&Date.now()-current.checked<wait))return;
    if(world()?.replaying?.())return;
    current.needsRefresh=false;current.refreshing=true;current.checked=Date.now();
    try{
      const began=Date.now(),feed=await fetchWorld(current.business,current.feed.revision);current.slow=Date.now()-began>800;
      if(ctx!==current||current.business!==state.business||current.workspace!==state.data.workspace||state.view!=='aura'||!$('#world-stage')||world()?.replaying?.())return;
      if(!feed.unchanged)updateWorld(feed);
    }catch{/* Retry on the next refresh. */}
    finally{current.refreshing=false;}
  },1500);
  document.addEventListener('keydown',event=>{
    const tab=event.target.closest?.('.world-tabs [role="tab"]');
    if(!tab||!ctx||!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();const tabs=[...tab.parentElement.querySelectorAll('[role="tab"]')];let index=tabs.indexOf(tab);
    if(event.key==='Home')index=0;else if(event.key==='End')index=tabs.length-1;else index=(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
    showTab(tabs[index].dataset.worldTab);tabs[index].focus();
  });
  document.addEventListener('change',e=>{
    if(!ctx||ctx.business!==state.business)return;
    if(e.target.id==='world-compare-date'){ctx.compare=e.target.value;paintSide();}
    if(e.target.id==='world-effort-metric'){ctx.metric=e.target.value;world()?.setEffortMetric?.(ctx.metric);paintSide();}
    if(e.target.id==='world-flow'){ctx.flow=e.target.value;paintSide();}
    if(e.target.id==='world-effort-by'){ctx.effortBy=e.target.value;ctx.effortOpen=null;paintSide();}
    if(e.target.id==='world-by'){ctx.filter.by=e.target.value;ctx.filter.lands=landsFor(ctx.feed,e.target.value);world()?.filter(ctx.filter);paintSide();}
    if(e.target.id==='aura-goal'){const goal=e.target.value;state.data.aura_preferences={...(state.data.aura_preferences||{}),goal};attempt(async()=>{await api('/api/preferences',{business:state.business,aura:{goal}});hq().paintMark();hq().paint(true);paintSide();});}
  });
  const saveShift=shift=>{state.data.aura_preferences={...(state.data.aura_preferences||{}),shift};clearTimeout(shiftTimer);shiftTimer=setTimeout(()=>attempt(async()=>{await api('/api/preferences',{business:state.business,aura:{shift}});hq().paintMark();hq().paint(true);}),400);};
  document.addEventListener('input',e=>{if(!ctx)return;if(e.target.id==='aura-shift')saveShift(Number(e.target.value));if(e.target.id==='world-q'){world()?.search(e.target.value);ctx.q=e.target.value;clearTimeout(ctx.searchTimer);ctx.searchTimer=setTimeout(paintSide,150);}});
  document.addEventListener('pointerover',e=>{const box=e.target.closest?.('#world-map [data-key]');if(box&&ctx)highlight(box.dataset.key);});
  /* Pointing at a row, a timeline mark or an effort block shows where it is on the world, in every lens. */
  const peekFor=key=>{const L=links(),graph=L.index(ctx.feed).nodes.has(key);return {key,lands:graph?L.places(ctx.feed,key):[],docks:graph?[...L.trace(ctx.feed,key).up].filter(k=>k.startsWith('app:')||(k.startsWith('agent:')&&!k.includes('|'))):[]};};
  const blockPeek=key=>{const g=ctx.effortGroups?.get(key);if(!g)return null;const L=links(),lands=new Set();for(const id of g.chats)for(const l of L.places(ctx.feed,'chat:'+id))lands.add(l);return {lands:[...lands],docks:g.apps};};
  document.addEventListener('pointerover',e=>{if(!ctx||state.view!=='aura')return;const item=e.target.closest?.('#world-side [data-world-go], #world-side [data-effort-key]');if(!item)return;
    world()?.peek?.(item.dataset.worldGo?peekFor(item.dataset.worldGo):blockPeek(item.dataset.effortKey));});
  document.addEventListener('pointerout',e=>{if(ctx&&e.target.closest?.('#world-side [data-world-go], #world-side [data-effort-key]')&&!e.relatedTarget?.closest?.('#world-side [data-world-go], #world-side [data-effort-key]'))world()?.peek?.(null);});
  document.addEventListener('pointerout',e=>{if(ctx&&e.target.closest?.('#world-map [data-key]')&&!e.relatedTarget?.closest?.('#world-map [data-key]'))highlight(null);});
  document.addEventListener('click',e=>{
    if(!ctx||ctx.business!==state.business||state.view!=='aura')return;
    const on=selector=>e.target.closest(selector);
    if(on('#aura-shift-reset')){$('#aura-shift').value=0;saveShift(0);}
    const goTo=on('.aura-view [data-world-go]');
    if(goTo){
      if(goTo.closest('.world-found')){ctx.q='';if($('#world-q'))$('#world-q').value='';world()?.search('');}
      const [kind,...rest]=goTo.dataset.worldGo.split(':');selectRecord(kind,rest.join(':'));
      const again=[...document.querySelectorAll('#world-side [data-world-go]')].find(el=>el.dataset.worldGo===goTo.dataset.worldGo);
      if(again)again.focus({preventScroll:true});else{const heading=$('#world-side h2');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}}
    }
    const where=on('[data-world-origin]');
    if(where){const key=where.dataset.worldOrigin,record=where.dataset.originRecord,owner=ctx;ctx.origins={...(ctx.origins||{}),[key]:'looking'};paintSide();
      api('/api/origin?business='+encodeURIComponent(ctx.business)+(record?'&record='+encodeURIComponent(record):'&file='+encodeURIComponent(where.dataset.originFile)))
        .then(async r=>{if(ctx!==owner)return;ctx.origins[key]=r.origin||false;if(r.origin&&record){const feed=await fetchWorld(ctx.business);if(ctx===owner&&!feed.unchanged){updateWorld(feed,true);return;}}paintSide();})
        .catch(()=>{if(ctx===owner){ctx.origins[key]=false;paintSide();}});}
    if(on('[data-world-dismiss]')){ctx.outcome=null;ctx.receipts=[];ctx.receiptOpen=null;paintSide();}
    const receipt=on('[data-world-receipt]');if(receipt){const i=Number(receipt.dataset.worldReceipt);ctx.receiptOpen=ctx.receiptOpen===i?null:i;paintSide();}
    const mode=on('[data-world-time]');if(mode){ctx.timeMode=mode.dataset.worldTime;paintSide();}
    if(on('[data-world-more-changes]')){ctx.compareLimit=(ctx.compareLimit||60)+60;paintSide();}
    if(on('[data-world-end-week]')){ctx.week=null;paintSide();}
    const week=on('[data-world-week]');if(week){if(week.dataset.weekLand)selectRecord('land',week.dataset.weekLand);ctx.week=week.dataset.worldWeek;paintSide();$('#world-week')?.focus();}
    const block=on('[data-effort-key]');if(block){ctx.effortOpen=ctx.effortOpen===block.dataset.effortKey?null:block.dataset.effortKey;const shown=ctx.effortOpen&&blockPeek(ctx.effortOpen);
      if(shown?.lands.length){world()?.filter?.({lands:shown.lands,scoped:true});world()?.reveal?.(shown.lands);}else world()?.filter?.(ctx.filter);paintSide();}
    const follow=on('[data-effort-follow]');if(follow){const flow={requests:'requests',tokens:'tokens',cost_usd:'cost_usd'}[ctx.metric||'requests'];ctx.flow=flow;ctx.effortOpen=null;world()?.filter?.(ctx.filter);showTab('map');const [kind,...rest]=follow.dataset.effortFollow.split(':');selectRecord(kind,rest.join(':'));}
    const more=on('[data-map-more]');if(more){ctx.mapOpen={...(ctx.mapOpen||{}),[more.dataset.mapMore]:true};paintSide();}
    if(on('[data-world-arrived]')){ctx.compare=ctx.arrivedSince.slice(0,10);ctx.arrivedSince=null;ctx.timeMode='since';showTab('timeline');}
    const since=on('[data-world-since]');if(since){ctx.compare=since.dataset.worldSince;ctx.timeMode='since';showTab('timeline');}
    if(on('[data-world-compare]')){ctx.timeMode='since';showTab('timeline');}
    if(on('[data-world-fly]'))world()?.visit?.(changesSince(comparisonFeed(relatedFeed(ctx.feed,ctx.sel),ctx.sel),sinceDate(ctx.feed)).map(c=>c.key));
    if(on('[data-world-details]'))showTab('world');
    if(on('[data-world-previous]')&&ctx.history?.length){const previous=ctx.history.pop();if(previous.tab)ctx.tab=previous.tab;selectRecord(previous.kind,previous.id,false);world()?.restoreCamera?.(previous.camera);}
    if(on('[data-world-expand]')){ctx.expanded=!ctx.expanded;paintSide();$('#world-side [data-world-expand]')?.focus();}
    if(on('.aura-view [data-world-clear]')){ctx.sel=null;ctx.history=[];world()?.clear();world()?.filter?.(ctx.filter);paintSide();}
    const chip=on('.aura-view [data-world-chip]'),needs=on('.aura-view [data-world-needs]');
    if(chip||needs){if(chip){ctx.filter.by='';const id=chip.dataset.worldChip,active=ctx.filter.lands.includes(id);ctx.filter.lands=active?ctx.filter.lands.filter(x=>x!==id):[...ctx.filter.lands,id];}else ctx.filter.needs=!ctx.filter.needs;world()?.filter(ctx.filter);paintSide();}
    if(on('.aura-view [data-world-tour]'))world()?.tour?.();
    const tab=on('.aura-view [data-world-tab]');if(tab){if(ctx.effortOpen){ctx.effortOpen=null;world()?.filter?.(ctx.filter);}world()?.peek?.(null);showTab(tab.dataset.worldTab);}
  });
  window.addEventListener?.('pagehide',savePlace);
  return {focusChat:()=>setChat(true),leave(){savePlace();if(ctx){ctx.chat=false;ctx.mapObserver?.disconnect();}world()?.unmount?.();},chatOpen:()=>!!ctx?.chat,open,render:draw,
    relatedFeed,recordFor,changesSince,comparisonFeed,evidenceRows,goalLine,goalDone,home,tools,goalGaps,selected,whatChanged,landsFor,connections,mapView,timelineView,effortView,posterData,receipts,found,
    go:key=>{if(!ctx)return;const [kind,...rest]=String(key).split(':');selectRecord(kind,rest.join(':'));}};
})();
