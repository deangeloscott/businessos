/* The aura, opened: the organization drawn as a world (workspace-world.js), with the same things listed beside it.
   Everything shown comes from /api/world, which returns saved records only. Each thing opens the screen AURA
   already has for it; a next step opens an ordinary chat. Nothing leaves the computer unless the owner downloads
   a picture or clip and shares it. The list beside the world is also how it is read without sight or 3D. */
window.auraView=(()=>{
  const hq=()=>window.auraHQ,world=()=>window.auraWorld;
  const money=n=>'$'+Number(n).toLocaleString(undefined,{maximumFractionDigits:n<10?2:0});
  const value=(v,unit)=>unit==='USD'?money(v):Number(v).toLocaleString(undefined,{maximumFractionDigits:2})+(unit&&!['count','rank','USD'].includes(unit)?' '+unit:'');
  const records=type=>(state.data?.records||[]).filter(r=>r.type===type);
  const goals=()=>records('Objective').filter(r=>{const g=r.data.extensions?.businessos?.goal||{};return g.scope!=='chat'&&!g.deleted_at&&(r.data.status||'active')==='active';});
  const refOf=id=>(state.data?.records||[]).find(r=>r.data?.id===id)?.ref||'';
  const when=d=>d?new Date(d).toLocaleDateString(undefined,{month:'short',day:'numeric',year:'numeric'}):'';
  const count=(n,word)=>`${n} ${word}${n===1?'':'s'}`;
  let ctx=null,shiftTimer;

  /* A goal in words, from its saved measurements only. */
  const goalLine=g=>typeof g.target!=='number'?'No number yet':g.reached?'Reached':typeof g.latest!=='number'?'No measurement yet':g.direction==='lower_better'?`${value(g.latest,g.unit==='USD'?'USD':'')} · target ${value(g.target,g.unit)} or lower`:`${value(g.latest,g.unit==='USD'?'USD':'')} of ${value(g.target,g.unit)}`;
  const goalDone=g=>g.reached?1:typeof g.latest!=='number'||typeof g.target!=='number'?0:g.direction==='lower_better'?Math.min(1,g.target/Math.max(g.latest,1e-9)):Math.min(1,Math.max(0,g.latest)/(g.target||1));
  const FLABEL={supported:'Supported',unverified:'Not yet verified',challenged:'Challenged by new evidence',needs_review:'Due for review',out_of_date:'Out of date'};
  const row=(attrs,title,sub='',side='',hue=null)=>`<button type="button" class="world-row${attrs?'':' plain'}" ${attrs||'tabindex="-1"'}><i${hue!=null?` style="background:hsl(${Math.round(hue)},70%,55%)"`:''}></i><span><b>${esc(title)}</b>${sub?`<small>${esc(sub)}</small>`:''}</span><em>${esc(side)}</em></button>`;
  const hueOf=id=>world()?.model?.()?.lands.find(l=>l.id===id)?.hue??null;
  const landCounts=(f,l)=>{const n=l.items.length+(l.more||0),k=f.findings.filter(x=>x.land===l.id&&x.label!=='replaced').length;return [n?count(n,'tracked result').replace('tracked results','tracked').replace('tracked result','tracked'):'',k?count(k,'finding'):''].filter(Boolean).join(' · ');};

  function goalSection(){
    const pin=hq().pinned(),measured=goals().filter(g=>typeof g.measure?.target==='number'),current=state.data?.aura_preferences?.goal||'';
    if(!measured.length)return '<p class="small-note">Add a goal with a number and its progress can show as a ring around your aura icon.</p>';
    return `<p class="small-note">The ring around your aura icon fills as real progress on this goal is recorded.</p><label class="aura-goal-pick"><span class="sr-only">Main goal</span><select id="aura-goal"><option value="">No ring</option>${measured.map(g=>`<option value="${esc(g.ref)}" ${g.ref===current?'selected':''}>${esc(g.title)}</option>`).join('')}</select></label>${pin?`<p class="aura-goal-status">${esc(pin.reached?'Reached':typeof pin.measure.latest==='number'?value(pin.measure.latest,pin.measure.unit)+' of '+value(pin.measure.target,pin.measure.unit):'No measurement yet')}</p>`:''}`;
  }

  /* Beside the world with nothing selected: where things stand, then every way in. */
  /* What the latest work left on the world, goals first: saved changes and measurements since the last visit. */
  function latest(f,since){
    if(!since)return '';
    const names=Object.fromEntries(f.lands.map(l=>[l.id,l.name])),changes=f.changes.filter(c=>c.at>since),moved=f.goals.map(g=>{const pts=g.points||[],after=pts.filter(p=>p.at>since),before=pts.filter(p=>p.at<=since).at(-1);return after.length&&before&&after.at(-1).value!==before.value?{g,from:before.value,to:after.at(-1).value}:null;}).filter(Boolean);
    if(!changes.length&&!moved.length)return `<section><h3>Since your last visit</h3><p class="small-note">Nothing has changed since ${esc(when(since))}.</p></section>`;
    return `<section><h3>Since your last visit</h3>${moved.map(m=>row(`data-world-go="goal:${esc(m.g.id)}"`,m.g.name,`${value(m.from,m.g.unit==='USD'?'USD':'')} → ${value(m.to,m.g.unit)}`,m.g.reached?'Reached':'')).join('')}${changes.slice(0,5).map(c=>row(`data-world-go="item:${esc(c.land+'|'+c.item_id)}"`,c.title,names[c.land]||'',when(c.at),hueOf(c.land))).join('')}${changes.length>5?`<p class="small-note">and ${changes.length-5} more</p>`:''}${changes.length?'<button type="button" class="text-button" data-world-changed>Show me on the world</button>':''}</section>`;
  }
  const spark=tr=>{const pts=(tr?.points||[]).filter(p=>typeof p.value==='number');if(pts.length<2)return '';const vs=pts.map(p=>p.value),mn=Math.min(...vs),mx=Math.max(...vs);return `<div><svg class="world-spark" viewBox="0 0 140 30" role="img" aria-label="${esc(tr.field)} over time"><polyline points="${vs.map((v,i)=>`${(4+132*i/(vs.length-1)).toFixed(1)},${(25-20*(v-mn)/((mx-mn)||1)).toFixed(1)}`).join(' ')}"/></svg><p class="small-note">${esc(tr.field)}: ${esc(vs[0])} → ${esc(vs.at(-1))} over ${pts.length} checks</p></div>`;};
  /* Work that is running right now, and the area its chat is tied to. */
  const runningNow=()=>{if(!ctx)return [];const seen=new Set(),out=[];for(const r of [...(hq().cached?.()?.running||[]),...(state.data?.running_chats||[]).filter(j=>j.status!=='done'&&(!j.business_id||j.business_id===ctx.business))]){if(seen.has(r.chat_id))continue;seen.add(r.chat_id);out.push({land:ctx.feed.chat_lands?.[r.chat_id]||null,label:`${r.agent||'Your AI'} · working${r.title?' on '+r.title:''}`});}return out;};
  /* The places that belong to a goal, project, scheduled task or AI app, from saved links only. */
  function landsFor(f,by,projects=state.projects||[]){
    const [kind,...rest]=String(by||'').split(':'),id=rest.join(':');
    if(kind==='goal')return f.goals.find(g=>g.id===id)?.lands||[];
    if(kind==='task')return (f.tasks||[]).filter(k=>k.id===id&&k.land).map(k=>k.land);
    if(kind==='app')return (f.apps||[]).find(a=>a.name===id)?.lands||[];
    if(kind==='project'){const p=projects.find(x=>x.id===id),held=new Set((p?.members||[]).filter(m=>m.kind==='collection').map(m=>m.id));return f.lands.filter(l=>held.has(l.id)||(l.project_refs||[]).includes(id)).map(l=>l.id);}
    return [];
  }
  /* On the picture: find, filter, and the areas as a colour key. */
  function tools(f){
    const flt=ctx?.filter||{lands:[],needs:false,by:''};
    return `<label><span class="sr-only">Find in your world</span><input type="search" id="world-q" placeholder="Find anything…" autocomplete="off"></label>
      ${f.lands.length>1?`<div class="world-chips" role="group" aria-label="Show only these areas">${f.lands.filter(l=>l.kind!=='group').map(l=>`<button type="button" class="world-chip" data-world-chip="${esc(l.id)}" aria-pressed="${flt.lands.includes(l.id)}"><i${hueOf(l.id)!=null?` style="background:hsl(${Math.round(hueOf(l.id))},70%,55%)"`:''}></i>${esc(l.name)}</button>`).join('')}<button type="button" class="world-chip" data-world-needs aria-pressed="${!!flt.needs}">Needs a look</button></div>`:''}
      ${f.goals.some(g=>(g.lands||[]).length)||(state.projects||[]).length||(f.tasks||[]).length||(f.apps||[]).length?`<label class="world-by"><span>Show what belongs to</span><select id="world-by"><option value="">Everything</option>${[['Goals',f.goals.filter(g=>(g.lands||[]).length).map(g=>['goal:'+g.id,g.name])],['Projects',(state.projects||[]).map(p=>['project:'+p.id,p.name])],['Scheduled tasks',(f.tasks||[]).filter(k=>k.land).map(k=>['task:'+k.id,k.name||'Scheduled task'])],['AI apps',(f.apps||[]).map(a=>['app:'+a.name,a.name])]].filter(g=>g[1].length).map(([label,list])=>`<optgroup label="${label}">${list.map(([v,n])=>`<option value="${esc(v)}" ${flt.by===v?'selected':''}>${esc(n)}</option>`).join('')}</optgroup>`).join('')}</select></label>${flt.by&&!flt.lands.length?'<p class="small-note">Nothing on the world is tied to this yet.</p>':''}`:''}`;
  }
  function home(f){
    const names=Object.fromEntries(f.lands.map(l=>[l.id,l.name])),shift=Number.isInteger(state.data?.aura_preferences?.shift)?state.data.aura_preferences.shift:0;
    return `<div><div class="kind">Your world</div><h2>${esc(f.business.name)}</h2>${f.business.example?'<p class="small-note">AURA\'s made-up example business.</p>':''}</div>
      ${latest(f,ctx?.since)}
      <section><h3>Goals</h3>${f.goals.length?f.goals.map(g=>row(typeof g.target==='number'?`data-world-go="goal:${esc(g.id)}"`:refOf(g.id)?`data-record="${esc(refOf(g.id))}"`:'',g.name,goalLine(g))).join(''):'<p class="small-note">Add a goal with a number, such as "$50,000 in grants this year", and it becomes a ring around your world.</p>'}<button type="button" class="text-button" data-action="add-goal">Add goal</button></section>
      ${f.attention.length?`<section><h3>Needs you</h3>${f.attention.map(a=>row(refOf(a.id)?`data-record="${esc(refOf(a.id))}"`:'',a.title,a.reason)).join('')}</section>`:''}
      ${f.suggestions.length?`<section><h3>Next steps</h3>${f.suggestions.map(x=>row(`data-prompt="${esc(x.prompt)}"`,x.title,x.why)).join('')}</section>`:''}
      ${f.changes.length?`<section><h3>Changed lately</h3>${f.changes.slice(0,6).map(c=>row(`data-world-go="item:${esc(c.land+'|'+c.item_id)}"`,c.title,names[c.land]||'',when(c.at),hueOf(c.land))).join('')}</section>`:''}
      <section><h3>Areas</h3>${f.lands.map(l=>row(`data-world-go="land:${esc(l.id)}"`,l.name,landCounts(f,l)||'Nothing yet',l.quiet?'Gone quiet':'',hueOf(l.id))).join('')}${(f.uncharted||[]).map(a=>row(`data-world-go="land:new:${esc(a.id)}"`,a.name,'Uncharted','',hueOf('new:'+a.id))).join('')}${f.lands_more?`<p class="small-note">and ${f.lands_more} more collection${f.lands_more===1?'':'s'}, open from Files.</p>`:''}${f.findings_hidden?`<p class="small-note">${f.findings_hidden} more finding${f.findings_hidden===1?' is':'s are'} kept but not drawn here. Open Knowledge to see them all.</p>`:''}${f.lands.length||(f.uncharted||[]).length?'':'<p class="small-note">What your AI saves appears here: collections, their results, and findings with sources.</p>'}</section>
      <button type="button" class="text-button" data-world-tour>Take the tour</button>
      <details class="aura-colour"><summary>How to read your world</summary><p class="small-note">Each continent is one of your collections, or an area of findings, always in the same place; it grows as it fills. Each light is something you track there: brighter when it was checked recently, bigger when more is recorded about it. Smaller lights are findings (hollow means not yet verified; bigger the more often one has been given to your AI, and joined by a line to the result it rests on when the same source stands behind both) and the faintest are changes a check noticed. Rings are goals with a number. A clock marks a collection a scheduled task keeps current. Amber means it needs a look. Drag to turn the world, scroll to fly down, and use the arrow keys when it has focus.</p></details>
      <details class="aura-colour"><summary>Aura icon</summary>${goalSection()}<p class="small-note">Its colour comes from your focus areas. Adjust it here.</p><input type="range" id="aura-shift" min="-180" max="180" step="5" value="${shift}" aria-label="Colour"><button type="button" class="text-button" id="aura-shift-reset">Reset</button></details>`;
  }

  /* What stands between a goal and its number, read only from saved facts. Each comes with the request that would deal with it. */
  function goalGaps(f,g){
    const out=[];if(typeof g.target!=='number'||g.reached)return out;
    const last=(g.points||[]).at(-1),age=last?Math.floor((Date.parse(f.as_of)-Date.parse(last.at))/864e5):null,metric=g.metric||g.name;
    if(age===null)out.push(['No measurement has been saved yet',`Help me record the first number for "${metric}" toward our goal "${g.name}". If you can reach a source for it, use that; otherwise ask me.`]);
    else if(age>=21)out.push([`Not measured for ${age} days`,`Bring "${metric}" up to date for our goal "${g.name}". Use whatever source you can reach, and save the new number.`]);
    for(const id of g.lands||[]){const l=f.lands.find(x=>x.id===id);if(!l)continue;
      if(l.quiet)out.push([`${l.name} has gone quiet`,`Check "${l.name}" again and update it with what has changed since it was last checked.`]);
      const weak=f.findings.filter(x=>x.land===id&&['unverified','challenged','needs_review','out_of_date'].includes(x.label)).length;
      if(weak)out.push([`${count(weak,'finding')} in ${l.name} need${weak===1?'s':''} checking`,`Check the findings in "${l.name}" that are unverified, challenged or due for review, and update each with what you find.`]);}
    for(const k of f.tasks||[])if(k.goal===g.id&&['failed','missing','paused'].includes(k.health))out.push([`${k.name||'A scheduled task'} is not running`,`The scheduled task "${k.name||'for this goal'}" is not running (${k.status||'no report'}). Help me get it running again.`]);
    if(!(g.lands||[]).length)out.push(['Nothing is linked to this goal yet','']);
    return out;
  }
  /* Beside the world with something selected: what it is, whether it needs a look, and the way into its own screen. */
  function selected(f,o){
    const back='<button type="button" class="text-button world-back" data-world-clear>‹ Your world</button>',head=(kind,title)=>`<div><div class="kind">${esc(kind)}</div><h2>${esc(title)}</h2></div>`,facts=list=>`<dl class="world-facts">${list.filter(x=>x[1]!==''&&x[1]!=null).map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
    const ask=text=>`<button type="button" class="secondary" data-prompt="${esc(text)}">Ask about it</button>`;
    if(o.kindOf==='land'&&o.unch)return back+head('Uncharted',o.name)+`<p>Nothing is saved here yet. Ask your AI to look into it, and what it finds appears here as lights, with sources.</p><div class="world-acts"><button type="button" class="primary" data-prompt="${esc(`Start looking into ${o.name.toLowerCase()} for us. Find what matters most, save what you find with its sources, and tell me what you saved.`)}">Start charting ${esc(o.name)}</button></div>`;
    if(o.kind==='task'){const k=o.raw,bad=['failed','missing','paused'].includes(k.health);return back+head('Scheduled task',o.name)+(k.status?`<p${bad?' class="world-callout"':''}>${esc(k.status)}</p>`:'')+facts([['Runs',k.schedule||''],['In',k.app||''],['Keeps current',o.land.name],['Works toward',f.goals.find(g=>g.id===k.goal)?.name||'']])
      +`<div class="world-acts"><button type="button" class="primary" data-view="tools">Open schedules</button><button type="button" class="secondary" data-world-go="land:${esc(o.land.id)}">See ${esc(o.land.name)}</button></div>`;}
    if(o.kindOf==='land'&&o.kind==='group')return back+head('More collections',o.name)+'<p>These are kept in AURA and open as usual. They are drawn as one place so the world stays readable.</p>'+`<section><h3>Collections</h3>${(o.members||[]).map(m=>row(`data-collection="${esc(m.id)}"`,m.name,count(m.current,'result'))).join('')}</section>`;
    if(o.kindOf==='land'){const things=o.things.slice().sort((a,b)=>b.seen-a.seen),isCollection=o.kind==='collection';
      return back+head(isCollection?'Collection':'Findings',o.name)+(o.purpose?`<p>${esc(o.purpose)}</p>`:'')+(o.quiet?'<p class="world-callout">This was being kept current and has gone quiet.</p>':'')
        +facts([['Tracked',things.length+(o.more||0)||''],['Findings',o.finds.length||''],['Last checked',when(o.last_checked)],['Kept current by',o.task_linked?'A scheduled task':''],['Given to your AI',o.given?count(o.given,'time'):''],['Used by',o.uses?count(o.uses,'chat or task').replace('chat or tasks','chats and tasks'):'']])
        +`<div class="world-acts">${isCollection?`<button type="button" class="primary" data-collection="${esc(o.id)}">Open the collection</button>`:`<button type="button" class="primary" data-hq-area="${esc(o.id.replace(/^area:/,''))}">Open these findings</button>`}${ask(`Tell me where we stand on ${o.name}: what we know, what changed most recently, and what is worth doing next.`)}</div>`
        +(things.length?`<section><h3>Tracked</h3>${things.slice(0,8).map(x=>row(`data-world-go="item:${esc(x.id)}"`,x.name,Object.entries(x.raw.fields||{}).slice(0,2).map(([k,v])=>`${k}: ${v}`).join(' · '),x.need?'Review':'',o.hue)).join('')}${things.length>8?`<p class="small-note">and ${things.length-8+(o.more||0)} more in the collection</p>`:''}</section>`:'')
        +(o.finds.length?`<section><h3>Findings</h3>${o.finds.slice(0,8).map(x=>row(`data-world-go="finding:${esc(x.id)}"`,x.name,FLABEL[x.label]||'','',o.hue)).join('')}</section>`:'');}
    if(o.kind==='item'){const it=o.raw;return back+head(o.land.name,o.name)+(o.need?'<p class="world-callout">Due for review.</p>':'')+facts([...Object.entries(it.fields||{}),['First seen',when(it.first_seen)],['Last checked',when(it.last_seen||it.updated_at)],['Sources',it.sources||''],['Changes noticed',o.changes||'']])
+spark(it.trend)
      +`<div class="world-acts"><button type="button" class="primary" data-collection="${esc(o.land.id)}">Open in ${esc(o.land.name)}</button>${ask(`Tell me what we know about "${o.name}" in our collection "${o.land.name}": what changed most recently and where it came from.`)}</div>`;}
    if(o.kind==='finding'){const x=o.raw,ref=refOf(x.id)||x.id;return back+head('Finding',x.statement)+(o.need?`<p class="world-callout">${esc(FLABEL[o.label])}.</p>`:'')+facts([['Status',FLABEL[o.label]||''],['In',o.land.name],['Since',when(x.at)],['Supporting sources',x.sources||''],['Rests on',(o.tied||[]).map(t=>t.name).join(', ')],['Given to your AI',x.given?count(x.given,'time'):''],['Challenging sources',x.challenges||'']])
      +((x.evidence||[]).length?`<section><h3>Both sides</h3>${x.evidence.map(e=>row('',e.statement,e.relationship==='contradicts'?'Challenges it':'Supports it')).join('')}</section>`:'')
      +`<div class="world-acts">${ref?`<button type="button" class="primary" data-record="${esc(ref)}">Open the finding</button>`:''}${o.label==='challenged'?`<button type="button" class="secondary" data-prompt="${esc(`Two sources disagree about this finding: "${x.statement}". Check both, tell me which holds, and update the finding with what you find.`)}">Settle it</button>`:''}${ask(`Show me the evidence behind this finding and whether it still holds: "${x.statement}"`)}</div>`;}
    if(o.kind==='goal'){const g=o.raw,ref=refOf(g.id),gaps=goalGaps(f,g);return back+head('Goal',g.name)+`<p>${esc(goalLine(g))}</p><div class="world-meter"><span style="width:${Math.round(goalDone(g)*100)}%"></span></div>`+facts([['Measured by',g.metric||''],['Measurements saved',(g.points||[]).length||''],['Fed by',(g.lands||[]).map(id=>f.lands.find(l=>l.id===id)?.name).filter(Boolean).join(', ')]])+((g.lands||[]).length?'':'<p class="small-note">Nothing is linked to this goal yet. Put it in a project with a collection, and the world shows what feeds it.</p>')
      +`<div class="world-acts">${ref?`<button type="button" class="primary" data-record="${esc(ref)}">Open the goal</button>`:''}<button type="button" class="secondary" data-prompt="${esc(`Help me plan the next step toward our goal "${g.name}". Use what we already know and say what would move the number most.`)}">Plan the next step</button></div>${gaps.length?`<section><h3>What would move this</h3>${gaps.map(([title,prompt])=>row(prompt?`data-prompt="${esc(prompt)}"`:'',title,prompt?'Ask your AI to do it':'')).join('')}</section>`:''}<p class="small-note">Its ring fills from the measurements saved for it. Watch it replay on the world.</p>`;}
    if(o.kind==='decision'){const d=o.raw;return back+head(d.kind==='lesson'?'Lesson':'Decision',d.title)+facts([[d.kind==='lesson'?'Learned':'Made',when(d.at)],['Rests on',(o.basis||[]).map(b=>b.name).slice(0,3).join(' · ')]])+`<div class="world-acts"><button type="button" class="primary" data-record="${esc(refOf(d.id)||d.id)}">${d.kind==='lesson'?'Open the lesson':'Open the decision'}</button></div>`;}
    return back;
  }
  /* The other views of the same records. Each is plain page content in the current style, so it reads the same in every style. */
  const TABS=[['world','Your world'],['map','Connections'],['timeline','Time'],['effort','AI effort'],['poster','Year poster']];
  const compact=n=>n>=1e6?(n/1e6).toFixed(n>=1e7?0:1).replace(/\.0$/,'')+'M':n>=1e3?(n/1e3).toFixed(n>=1e4?0:1).replace(/\.0$/,'')+'K':String(Math.round(n));
  /* Map: work on the left, what is known in the middle, goals on the right. A line is a saved link, never a guess. */
  function mapLinks(f,projects){
    const links=[];
    for(const l of f.lands)for(const id of l.project_refs||[])links.push(['p:'+id,'l:'+l.id]);
    for(const k of f.tasks||[]){if(k.land)links.push(['t:'+k.id,'l:'+k.land]);if(k.goal)links.push(['t:'+k.id,'g:'+k.goal]);}
    for(const p of projects)for(const m of p.members||[]){if(m.kind==='collection')links.push(['p:'+p.id,'l:'+m.id]);if(m.kind==='goal')links.push(['p:'+p.id,'g:'+m.id]);}
    for(const g of f.goals)for(const id of g.lands||[])links.push(['l:'+id,'g:'+g.id]);
    for(const m of f.methods||[])for(const id of m.lands||[])links.push(['m:'+m.id,'l:'+id]);
    for(const a of f.apps||[])for(const id of a.lands||[])links.push(['a:'+a.name,'l:'+id]);
    return [...new Set(links.map(x=>x.join('\n')))].map(x=>x.split('\n'));
  }
  function mapView(f,projects=state.projects||[]){
    const node=(key,attrs,title,sub)=>`<button type="button" class="wm-node${attrs?'':' plain'}" data-key="${esc(key)}" ${attrs||'tabindex="-1"'}><b>${esc(title)}</b>${sub?`<small>${esc(sub)}</small>`:''}</button>`,col=(title,items)=>`<div class="wm-col"><h3>${title}</h3>${items||'<p class="small-note">Nothing yet.</p>'}</div>`;
    const work=[...projects.map(p=>node('p:'+p.id,`data-open-project="${esc(p.id)}"`,p.name,'Project')),...(f.tasks||[]).map(k=>node('t:'+k.id,k.land?`data-world-go="task:${esc(k.id)}"`:'',k.name||'Scheduled task',k.schedule||'Scheduled task'))].join('');
    return `<p class="small-note">How your work, what you know and your goals connect. A line is a saved link: a project that holds a collection or goal, a task that keeps a collection current, or a collection tied to a goal.</p><div class="wm" style="grid-template-columns:repeat(${3+((f.methods||[]).length?1:0)+((f.apps||[]).length?1:0)},minmax(0,1fr))" id="world-map"><svg class="wm-lines" aria-hidden="true"></svg>${(f.apps||[]).length?col('AI apps',f.apps.map(a=>node('a:'+a.name,'',a.name,count(a.requests,'request'))).join('')):''}${(f.methods||[]).length?col('Methods',f.methods.slice(0,12).map(m=>node('m:'+m.id,'',m.name,'Given to '+count(m.uses,'request'))).join('')):''}${col('Work',work)}${col('What you know',f.lands.map(l=>node('l:'+l.id,`data-world-go="land:${esc(l.id)}"`,l.name,landCounts(f,l)||'Nothing yet')).join(''))}${col('Goals',f.goals.map(g=>node('g:'+g.id,typeof g.target==='number'?`data-world-go="goal:${esc(g.id)}"`:'',g.name,goalLine(g))).join(''))}</div>${mapLinks(f,projects).length?'':'<p class="small-note">Nothing is linked yet. Put a collection and a goal in the same project, or give a scheduled task a collection to keep current, and the lines appear.</p>'}`;
  }
  function drawLinks(){
    const host=$('#world-map');if(!host||!ctx)return;const box=host.getBoundingClientRect(),svg=host.querySelector('svg'),pos={};
    host.querySelectorAll('[data-key]').forEach(el=>{const r=el.getBoundingClientRect();pos[el.dataset.key]={l:r.left-box.left,r:r.right-box.left,y:(r.top+r.bottom)/2-box.top};});
    svg.setAttribute('width',box.width);svg.setAttribute('height',box.height);
    svg.innerHTML=mapLinks(ctx.feed,state.projects||[]).filter(([a,b])=>pos[a]&&pos[b]).map(([a,b])=>{const x1=pos[a].r,x2=pos[b].l,m=(x1+x2)/2;return `<path d="M${x1},${pos[a].y} C${m},${pos[a].y} ${m},${pos[b].y} ${x2},${pos[b].y}"/>`;}).join('');
  }
  /* Timeline: one row per area, a mark for each thing saved, at the time it was saved. */
  function timelineView(f){
    const t=d=>Date.parse(d),end=t(f.as_of)||Date.now(),times=[t(f.business.since),...f.lands.flatMap(l=>l.items.map(i=>t(i.first_seen))),...f.findings.map(x=>t(x.at)),...f.changes.map(c=>t(c.at)),...f.goals.flatMap(g=>(g.points||[]).map(p=>t(p.at))),...f.decisions.map(d=>t(d.at))].filter(Number.isFinite);
    const coming=[...(f.tasks||[]).filter(k=>k.next_run).map(k=>[k.next_run,'Next run: '+(k.name||'Scheduled task'),k.land?'task:'+k.id:'']),...(f.deadlines||[]).map(d=>[d.due,'Due: '+d.title,'item:'+d.collection_id+'|'+d.item_id])].filter(c=>t(c[0])>end&&t(c[0])<end+45*864e5);
    const now=end,last=Math.max(now,...coming.map(c=>t(c[0]))),start=Math.min(now-864e5,...times),pct=d=>Math.max(0,Math.min(100,100*((typeof d==='number'?d:t(d))-start)/(last-start))).toFixed(2);
    const mark=(cls,d,title,go)=>Number.isFinite(t(d))?`<button type="button" class="wt-mark ${cls}" style="left:${pct(d)}%" title="${esc(title+' · '+when(d))}" aria-label="${esc(title+', '+when(d))}" ${go?`data-world-go="${esc(go)}"`:''}></button>`:'';
    const lane=(label,go,marks)=>`<div class="wt-row"><button type="button" class="wt-label${go?'':' plain'}" ${go?`data-world-go="${esc(go)}"`:'tabindex="-1"'}>${esc(label)}</button><div class="wt-strip">${marks}</div></div>`;
    const rows=f.lands.map(l=>lane(l.name,'land:'+l.id,l.items.map(i=>mark('item',i.first_seen,'Tracked: '+i.title,'item:'+l.id+'|'+i.id)).join('')+f.findings.filter(x=>x.land===l.id&&x.label!=='replaced').map(x=>mark('finding',x.at,'Finding: '+x.statement,'finding:'+x.id)).join('')+f.changes.filter(c=>c.land===l.id).map(c=>mark('change',c.at,'Changed: '+c.title,'item:'+l.id+'|'+c.item_id)).join('')));
    const measured=f.goals.filter(g=>(g.points||[]).length);
    if(measured.length)rows.push(lane('Goals','',measured.map(g=>g.points.map(p=>mark('measure',p.at,`${g.name}: ${value(p.value,g.unit==='USD'?'USD':'')}`,'goal:'+g.id)).join('')).join('')));
    if(f.decisions.length)rows.push(lane('Decisions','',f.decisions.map(d=>mark('decision',d.at,'Decided: '+d.title,'decision:'+d.id)).join('')));
    const weeks=(f.work||[]).filter(w=>w.requests),most=Math.max(1,...weeks.map(w=>w.requests));
    const split=(f.work_by||[]).filter(g=>g.weeks.some(Boolean)),tall=Math.max(1,...split.flatMap(g=>g.weeks));
    for(const g of split){const name=g.kind==='project'?(state.projects||[]).find(p=>p.id===g.id)?.name||'A project':g.kind==='land'?f.lands.find(l=>l.id===g.id)?.name||'A collection':'Other chats';
      rows.push(lane('Work: '+name,g.kind==='land'?'land:'+g.id:'',g.weeks.map((n,i)=>n&&f.work?.[i]?`<i class="wt-bar" style="left:${pct(t(f.work[i].start)+3.5*864e5)}%;height:${Math.max(12,Math.round(n/tall*100))}%" title="${esc(name+', week of '+when(f.work[i].start)+': '+count(n,'request'))}"></i>`:'').join('')));}
    if(weeks.length&&!split.length)rows.push(lane('AI requests','',weeks.map(w=>`<i class="wt-bar" style="left:${pct(t(w.start)+3.5*864e5)}%;height:${Math.max(12,Math.round(w.requests/most*100))}%" title="${esc('Week of '+when(w.start)+': '+count(w.requests,'request'))}"></i>`).join('')));
    if(coming.length)rows.push(lane('Coming up','',`<i class="wt-now" style="left:${pct(now)}%"></i>`+coming.map(c=>mark('change',c[0],c[1],c[2])).join('')));
    if(!rows.length)return '<p class="small-note">Nothing has been saved yet. Each thing your AI saves appears here at the time it was saved.</p>';
    return `<p class="small-note">What was saved, and when. Click a mark to see it on your world.</p><div class="wt">${rows.join('')}<div class="wt-row"><span class="wt-label plain"></span><div class="wt-axis"><span>${esc(when(new Date(start).toISOString()))}</span><span>${coming.length?esc(when(new Date(last).toISOString())):'Today'}</span></div></div></div><p class="wt-key small-note"><i class="wt-mark item"></i>tracked <i class="wt-mark finding"></i>finding <i class="wt-mark change"></i>change noticed <i class="wt-mark measure"></i>goal measurement <i class="wt-mark decision"></i>decision</p>`;
  }
  /* AI effort: where this month's requests went, exactly as each AI app reported them. */
  /* Blocks sized by share: split the list in two by weight, side by side then stacked, until each has its own block. */
  function blocks(items){
    const out=[],place=(list,x,y,w,h,flip)=>{if(!list.length)return;if(list.length===1){out.push({...list[0],x,y,w,h});return;}const total=list.reduce((s,i)=>s+i.value,0);let run=0,cut=0;while(cut<list.length-1&&run+list[cut].value<=total/2){run+=list[cut].value;cut++;}if(!cut){cut=1;run=list[0].value;}const share=run/total;
      if(flip){place(list.slice(0,cut),x,y,w,h*share,!flip);place(list.slice(cut),x,y+h*share,w,h*(1-share),!flip);}else{place(list.slice(0,cut),x,y,w*share,h,!flip);place(list.slice(cut),x+w*share,y,w*(1-share),h,!flip);}};
    place(items.filter(i=>i.value>0).sort((a,b)=>b.value-a.value),0,0,100,100,false);
    return `<div class="we-map">${out.map((b,i)=>`<div class="we-block" style="left:${b.x.toFixed(2)}%;top:${b.y.toFixed(2)}%;width:${b.w.toFixed(2)}%;height:${b.h.toFixed(2)}%;--we-h:${(i*67+200)%360}" title="${esc(b.name+' · '+b.sub)}"><b>${esc(b.name)}</b><small>${esc(b.sub)}</small></div>`).join('')}</div>`;
  }
  function effortRows(u,f){
    const by=(f?.effort||[]).filter(g=>g.requests),nameOf=g=>g.kind==='land'?f.lands.find(l=>l.id===g.id)?.name||'A collection':g.kind==='project'?(state.projects||[]).find(p=>p.id===g.id)?.name||'A project':'Chats not tied to a collection or project',top=Math.max(1,...by.map(g=>g.tokens||g.requests));
    const sub=g=>`${count(g.requests,'request')}${g.tokens?' · '+compact(g.tokens)+' tokens':''}${g.cost_usd?' · '+money(g.cost_usd):''}${g.missing_costs?` · cost not reported for ${g.missing_costs}`:''}`;
    const used=f?.methods||[],methods=used.length?'<h3>By method given to the request</h3>'+blocks(used.slice(0,12).map(m=>({name:m.name,value:m.uses,sub:count(m.uses,'request')}))):'';
    const tied=by.length?'<h3>By what the work was for</h3>'+blocks(by.map(g=>({name:nameOf(g),value:g.tokens||g.requests,sub:sub(g)}))):'';
    const groups=(u?.groups||[]).filter(g=>g.requests),tok=g=>(g.input_tokens||0)+(g.output_tokens||0);
    if(!groups.length)return '<p class="small-note">No AI requests have been recorded this month. They appear here by AI app as you work, with the tokens and cost each app reports.</p>';
    const tot=u.totals||{},all=(tot.input_tokens||0)+(tot.output_tokens||0);
    return `<p class="small-note">Where this month's AI requests went. Each block's size is its share of tokens, or of requests when an app reports no tokens. Only what each app reports is shown; a cost an app does not report is left out, not estimated.</p><dl class="world-facts"><dt>Requests</dt><dd>${u.requests}</dd>${all?`<dt>Tokens</dt><dd>${compact(all)}</dd>`:''}${typeof tot.cost_usd==='number'?`<dt>Reported cost</dt><dd>${money(tot.cost_usd)}</dd>`:''}</dl><h3>By AI app</h3>`
      +blocks(groups.map(g=>({name:g.name||'Unnamed app',value:tok(g)||g.requests,sub:sub({requests:g.requests,tokens:tok(g),cost_usd:g.cost_usd,missing_costs:g.missing_costs})})))+tied+methods;
  }
  /* Year poster: the world, the year's outcomes, and each day something was saved. */
  function posterView(f){
    const year=new Date(f.as_of).getFullYear(),first=new Date(year,0,1),day=d=>{const x=new Date(d);return x.getFullYear()===year?Math.floor((x-first)/864e5):-1;},n=new Array(366).fill(0),add=d=>{const i=day(d);if(i>=0)n[i]++;},inYear=d=>day(d)>=0;
    f.lands.forEach(l=>l.items.forEach(i=>add(i.first_seen)));f.findings.forEach(x=>add(x.at));f.changes.forEach(c=>add(c.at));
    const max=Math.max(1,...n),today=Math.max(0,day(f.as_of)),label=i=>new Date(year,0,1+i).toLocaleDateString(undefined,{month:'short',day:'numeric'});
    const cells=n.slice(0,today+1).map((v,i)=>`<i style="opacity:${v?(.35+.65*v/max).toFixed(2):.12}" title="${esc(label(i)+': '+(v?count(v,'thing')+' saved':'nothing saved'))}"></i>`).join('');
    const measured=f.goals.filter(g=>typeof g.target==='number');
    return `<div class="wp"><div class="wp-card" id="world-poster-card"></div><div class="wp-side"><div><div class="kind">${year} with AURA</div><h2>${esc(f.business.name)}</h2></div>
      <dl class="world-facts"><dt>Tracked this year</dt><dd>${f.lands.reduce((s,l)=>s+l.items.filter(i=>inYear(i.first_seen)).length,0)}</dd><dt>Findings this year</dt><dd>${f.findings.filter(x=>x.label!=='replaced'&&inYear(x.at)).length}</dd><dt>Changes noticed</dt><dd>${f.changes.filter(c=>inYear(c.at)).length}</dd>${measured.length?`<dt>Goals reached</dt><dd>${measured.filter(g=>g.reached).length} of ${measured.length}</dd>`:''}</dl>
      <div><h3>Each day something was saved</h3><div class="wp-grid">${cells}</div><p class="small-note">Stronger means more was saved that day: new results, findings and changes noticed. It counts saved records, not activity.</p></div>
      <div class="world-acts"><button type="button" class="primary" id="world-poster-dl">Download image</button></div></div></div>`;
  }
  function showTab(tab){
    if(!ctx||!$('#world-stage'))return;ctx.tab=tab;ctx.sel=null;document.querySelectorAll('[data-world-tab]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.worldTab===tab)));
    world()?.clear?.();world()?.lens?.(tab==='map'?'links':tab==='effort'?'effort':'');paintSide();
  }
  /* The last visit and the tour are kept with the other aura choices, so they follow the person between browsers. */
  const remember=patch=>{state.data.aura_preferences={...(state.data.aura_preferences||{}),...patch};api('/api/preferences',{business:state.business,aura:patch}).then(()=>{hq().paintMark?.();hq().paint?.(true);}).catch(()=>{});};
  function mountWorld(){
    const host=$('#world-stage');if(!host||!ctx)return;
    let ok=false;try{ok=!!world()?.available&&world().mount(host,ctx.feed,{select:o=>{if(ctx){ctx.sel=o;paintSide();}},seen:ctx.seen,toured:ctx.toured,remember,running:runningNow});if(ok)world().filter(ctx.filter);}catch(error){console.error(error);ok=false;}
    if(!ok)host.innerHTML='<p class="world-fallback">This computer cannot draw the 3D world. Everything in it is listed beside this, and in the other views.</p>';
    ctx.seen=ctx.feed.as_of;ctx.toured=true;paintSide();
  }
  function paintChrome(){
    if(!ctx||!$('#world-tools'))return;const q=$('#world-q')?.value||'',[top,keys='']=tools(ctx.feed).split('\u0001');
    $('#world-tools').innerHTML=top;$('#world-keys').innerHTML=keys;for(const el of [...$('#world-keys').querySelectorAll('.world-by,.small-note')])$('#world-tools').appendChild(el);if(q&&$('#world-q'))$('#world-q').value=q;
    const o=ctx.sel,about=o?(o.kindOf==='land'?o.name:o.kind==='item'?o.name:o.kind==='finding'?'this finding':o.kind==='goal'?o.raw.name:o.name):'';
    $('#world-ask-text').placeholder=about?`Ask about ${about}…`:'Ask your AI anything about your world…';
  }
  /* The list beside the world follows the lens: the world's own list, or the same records as connections, time, effort or the year. */
  function paintSide(){
    const host=$('#world-side');if(!host||!ctx)return;const f=ctx.feed,tab=ctx.tab;
    host.innerHTML=ctx.sel?selected(f,ctx.sel):tab==='map'?'<div><div class="kind">Connections</div><h2>How it connects</h2></div>'+mapView(f):tab==='timeline'?'<div><div class="kind">Time</div><h2>What was saved, and when</h2></div>'+timelineView(f):tab==='effort'?'<div><div class="kind">AI effort</div><h2>Where the work went</h2></div><div id="world-effort"><p class="small-note">Reading this month\'s AI use…</p></div>':tab==='poster'?posterView(f):home(f);
    if(ctx.sel)host.scrollTop=0;paintChrome();
    if(!ctx.sel&&tab==='effort')api('/api/usage?business='+encodeURIComponent(ctx.business)+'&period=month').catch(()=>null).then(u=>{const el=$('#world-effort');if(el)el.innerHTML=effortRows(u,ctx?.feed);});
    if(!ctx.sel&&tab==='poster'){const el=$('#world-poster-card'),c=world()?.available&&world().model()?world().poster():null;if(el&&c){el.appendChild(c);ctx.poster=c;}}
  }

  /* Opening the aura goes to its own section, like Knowledge or Files. */
  async function open(){state.view='aura';await render();if(typeof recordShellRoute==='function')recordShellRoute();if(typeof renderShell==='function')await renderShell();}
  async function draw(view,current=()=>true){
    const business=state.business;view.innerHTML='<div class="aura-view world-view"><p class="world-fallback">Drawing your world…</p></div>';
    const [s,feed]=await Promise.all([hq().summary(),api('/api/world?business='+encodeURIComponent(business))]);
    if(!s||!feed||business!==state.business||!current()||state.view!=='aura')return;
    const prefs=state.data?.aura_preferences||{};ctx={business,s,feed,sel:null,tab:'world',seen:prefs.seen||null,since:prefs.seen||null,toured:!!prefs.toured,filter:{lands:[],needs:false,by:''}};
    view.innerHTML=`<div class="aura-view world-view"><div class="world-main"><div class="world-stage" id="world-stage"><p class="world-fallback">Drawing your world…</p></div><div class="world-top"><div class="world-tabs" role="tablist" aria-label="Ways to look at your world">${TABS.map(([k,l])=>`<button type="button" role="tab" data-world-tab="${k}" aria-selected="${k==='world'}">${l}</button>`).join('')}</div><div class="world-tools" id="world-tools"></div></div><div class="world-keys" id="world-keys"></div><form class="world-ask" id="world-ask"><input type="text" id="world-ask-text" autocomplete="off" aria-label="Ask your AI"><button type="submit">Ask</button></form></div><aside class="world-side" id="world-side" aria-label="What is in your world"></aside></div>`;
    const start=()=>{if(ctx?.business===business&&ctx.tab==='world')mountWorld();};
    if(world())start();else{paintSide();document.addEventListener('aura-world-ready',start,{once:true});setTimeout(()=>{if(!world())start();},4000);}
  }

  function ask(text){
    const o=ctx?.sel,add=item=>window.auraCompose?.add(item),box=$('#request');if(!text.trim()||!box)return false;
    if(o?.kindOf==='land'&&o.kind==='collection')add({kind:'collection',id:o.id,label:o.name});
    else if(o?.kind==='item')add({kind:'collection',id:o.land.id,label:o.land.name});
    else if(o?.kind==='finding')add({kind:'record',id:refOf(o.raw.id)||o.raw.id,label:String(o.raw.statement).slice(0,80)});
    else if(o?.kind==='goal'&&refOf(o.raw.id))add({kind:'record',id:refOf(o.raw.id),label:o.raw.name});
    const about=o?.kind==='item'?`About "${o.name}" in our collection "${o.land.name}": `:'';
    box.value=about+text.trim();box.dispatchEvent(new Event('input',{bubbles:true}));$('#send')?.click();return true;
  }
  // In the aura the sidebar's own button opens and tucks it without changing the person's saved choice for the rest of AURA.
  document.addEventListener('click',e=>{if(!e.target.closest('#sidebar-collapse')||!document.body.classList.contains('in-aura')||matchMedia('(max-width:600px)').matches)return;e.stopImmediatePropagation();e.preventDefault();state.auraSidebarOpen=!state.auraSidebarOpen;document.body.classList.toggle('sidebar-collapsed',!state.auraSidebarOpen);},true);
  document.addEventListener('submit',e=>{if(e.target.id!=='world-ask')return;e.preventDefault();const input=$('#world-ask-text');if(ask(input.value)){input.value='';toast('Sent. Watch your world while it works.');}});
  /* When work that was running finishes, read the world again so what it saved arrives while you watch. */
  let wasRunning=0;
  setInterval(()=>{if(!ctx||state.view!=='aura'||!$('#world-stage'))return;const n=runningNow().length;if(wasRunning&&!n)api('/api/world?business='+encodeURIComponent(ctx.business)).then(feed=>{if(!ctx||!feed||feed.business?.id!==ctx.business)return;ctx.feed=feed;world()?.update?.(feed);paintSide();}).catch(()=>{});wasRunning=n;},1500);
  document.addEventListener('change',e=>{
    if(!ctx||ctx.business!==state.business)return;
    if(e.target.id==='world-by'){ctx.filter.by=e.target.value;ctx.filter.lands=landsFor(ctx.feed,e.target.value);world()?.filter(ctx.filter);paintSide();}
    if(e.target.id==='aura-goal'){const goal=e.target.value;state.data.aura_preferences={...(state.data.aura_preferences||{}),goal};attempt(async()=>{await api('/api/preferences',{business:state.business,aura:{goal}});hq().paintMark();hq().paint(true);paintSide();});}
  });
  const saveShift=shift=>{state.data.aura_preferences={...(state.data.aura_preferences||{}),shift};clearTimeout(shiftTimer);shiftTimer=setTimeout(()=>attempt(async()=>{await api('/api/preferences',{business:state.business,aura:{shift}});hq().paintMark();hq().paint(true);}),400);};
  document.addEventListener('input',e=>{if(!ctx)return;if(e.target.id==='aura-shift')saveShift(Number(e.target.value));if(e.target.id==='world-q')world()?.search(e.target.value);});
  document.addEventListener('click',e=>{
    if(!ctx)return;
    if(e.target.closest('#aura-shift-reset')){$('#aura-shift').value=0;saveShift(0);}
    const go=e.target.closest('.aura-view [data-world-go]');
    if(go){const [kind,...rest]=go.dataset.worldGo.split(':');if(world()?.available)world().focus(kind,rest.join(':'));else if(kind==='land'&&!rest[0].startsWith('new'))toast('Open it from Files to see what it holds.');}
    if(e.target.closest('.aura-view [data-world-clear]'))world()?.clear();
    const chip=e.target.closest('.aura-view [data-world-chip]'),needs=e.target.closest('.aura-view [data-world-needs]');
    if(chip||needs){if(chip){ctx.filter.by='';const id=chip.dataset.worldChip,on=ctx.filter.lands.includes(id);ctx.filter.lands=on?ctx.filter.lands.filter(x=>x!==id):[...ctx.filter.lands,id];}else ctx.filter.needs=!ctx.filter.needs;world()?.filter(ctx.filter);paintSide();}
    if(e.target.closest('.aura-view [data-world-changed]'))world()?.changed?.();
    if(e.target.closest('.aura-view [data-world-tour]'))world()?.tour?.();
    const tab=e.target.closest('.aura-view [data-world-tab]');if(tab)showTab(tab.dataset.worldTab);
    if(e.target.closest('#world-poster-dl')&&ctx.poster)ctx.poster.toBlob(blob=>{const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(ctx.feed.business.name||'aura').replace(/[^\w -]+/g,'').trim()+' year.png';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),2000);},'image/png');
  });
  return {open,render:draw,goalLine,goalDone,home,tools,goalGaps,selected,latest,landsFor,mapView,mapLinks,timelineView,effortRows,posterView};
})();
