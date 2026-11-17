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
    const findings=f.findings.filter(x=>x.label!=='replaced' && x.at>since);
    if(!changes.length&&!moved.length&&!findings.length)return `<section><h3>Since your last visit</h3><p class="small-note">No new findings, tracked changes or goal movement since ${esc(when(since))}.</p></section>`;
    return `<section><h3>Since your last visit</h3>${findings.slice(0,5).map(x=>row(`data-world-go="finding:${esc(x.id)}"`,x.statement,'New finding',when(x.at))).join('')}${moved.map(m=>row(`data-world-go="goal:${esc(m.g.id)}"`,m.g.name,`${value(m.from,m.g.unit==='USD'?'USD':'')} → ${value(m.to,m.g.unit)}`,m.g.reached?'Reached':'')).join('')}${changes.slice(0,5).map(c=>row(`data-world-go="item:${esc(c.land+'|'+c.item_id)}"`,c.title,names[c.land]||'',when(c.at),hueOf(c.land))).join('')}${changes.length>5?`<p class="small-note">and ${changes.length-5} more</p>`:''}${changes.length?'<button type="button" class="text-button" data-world-changed>Show me on the world</button>':''}</section>`;
  }
  const spark=tr=>{const pts=(tr?.points||[]).filter(p=>typeof p.value==='number');if(pts.length<2)return '';const vs=pts.map(p=>p.value),mn=Math.min(...vs),mx=Math.max(...vs);return `<div><svg class="world-spark" viewBox="0 0 140 30" role="img" aria-label="${esc(tr.field)} over time"><polyline points="${vs.map((v,i)=>`${(4+132*i/(vs.length-1)).toFixed(1)},${(25-20*(v-mn)/((mx-mn)||1)).toFixed(1)}`).join(' ')}"/></svg><p class="small-note">${esc(tr.field)}: ${esc(vs[0])} → ${esc(vs.at(-1))} over ${pts.length} checks</p></div>`;};
  /* Work that is running right now, and the area its chat is tied to. */
  const runningNow=()=>{if(!ctx)return [];const seen=new Set(),out=[];for(const r of [...(state.data?.running_chats||[]).filter(j=>j.status!=='done'&&(!j.business_id||j.business_id===ctx.business))]){if(seen.has(r.chat_id))continue;seen.add(r.chat_id);out.push({id:r.chat_id,land:ctx.feed.chat_lands?.[r.chat_id]||null,label:`${r.agent||'Your AI'} · working${r.title?' on '+r.title:''}`});}return out;};
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
      <section><h3>Goals</h3>${f.goals.length?f.goals.map(g=>row(`data-world-go="goal:${esc(g.id)}"`,g.name,goalLine(g))).join(''):'<p class="small-note">Add a goal with a number, such as "$50,000 in grants this year", and it becomes a ring around your world.</p>'}<button type="button" class="text-button" data-action="add-goal">Add goal</button></section>
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
    const back='<button type="button" class="text-button world-back" data-world-clear>Show everything</button>',head=(kind,title)=>`<div><div class="kind">${esc(kind)}</div><h2>${esc(title)}</h2></div>`,facts=list=>`<dl class="world-facts">${list.filter(x=>x[1]!==''&&x[1]!=null).map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
    const ask=text=>`<button type="button" class="secondary" data-prompt="${esc(text)}">Ask about it</button>`;
    if(o.relationship){
      const allowed=['record','file','method','chat','view','open-project','assistant-open'];
      const actions=Object.entries(o.raw.action || {}).filter(([name])=>allowed.includes(name)).map(([name,id])=>
        `<button type="button" class="secondary" data-${name}="${esc(id)}">Open ${esc(kindName(o.kind))}</button>`).join('');
      return back+head(kindName(o.kind),o.name)+'<div class="world-acts">'+actions+
        ask('Help me work with “'+o.name+'”.')+'</div>'+relationshipRows(f,o);
    }
    if(o.kindOf==='land'&&o.unch)return back+head('Uncharted',o.name)+`<p>Nothing is saved here yet. Ask your AI to look into it, and what it finds appears here as lights, with sources.</p><div class="world-acts"><button type="button" class="primary" data-prompt="${esc(`Start looking into ${o.name.toLowerCase()} for us. Find what matters most, save what you find with its sources, and tell me what you saved.`)}">Start charting ${esc(o.name)}</button></div>`;
    if (['project','app','method'].includes(o.kind)) return back + head({project:'Project',app:'AI app',method:'Method'}[o.kind],o.name)
      + (o.kind==='project' ? `<button class="primary" data-open-project="${esc(o.id)}">Open project</button>` : '')
      + (o.kind==='method' ? `<button class="secondary" data-method="${esc(o.id)}">Open in Library</button>` : '') + connections(f,o);
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
    if(o.kind==='finding'){const x=o.raw,ref=refOf(x.id)||x.id;return back+head('Finding',x.statement)+`<p class="world-finding-status" data-status="${esc(o.label)}"><span aria-hidden="true">${o.label==='supported'?'●':o.label==='unverified'?'○':o.label==='challenged'?'×':'△'}</span> ${esc(FLABEL[o.label] || o.label)}</p>`+(o.need?`<p class="world-callout">${esc(FLABEL[o.label])}.</p>`:'')+facts([['Status',FLABEL[o.label]||''],['In',o.land.name],['Since',when(x.at)],['Supporting sources',x.sources||''],['Rests on',(o.tied||[]).map(t=>t.name).join(', ')],['Given to your AI',x.given?count(x.given,'time'):''],['Challenging sources',x.challenges||'']])
      +((x.evidence||[]).length?`<section><h3>Both sides</h3>${x.evidence.map(e=>row('',e.statement,e.relationship==='contradicts'?'Challenges it':'Supports it')).join('')}</section>`:'')
      +`<div class="world-acts">${ref?`<button type="button" class="primary" data-record="${esc(ref)}">Open the finding</button>`:''}${o.label==='challenged'?`<button type="button" class="secondary" data-prompt="${esc(`Two sources disagree about this finding: "${x.statement}". Check both, tell me which holds, and update the finding with what you find.`)}">Settle it</button>`:''}${ask(`Show me the evidence behind this finding and whether it still holds: "${x.statement}"`)}</div>`;}
    if(o.kind==='goal'){const g=o.raw,ref=refOf(g.id),gaps=goalGaps(f,g);return back+head('Goal',g.name)+(typeof g.target==='number' ? `<p>${esc(goalLine(g))}</p><div class="world-meter"><span style="width:${Math.round(goalDone(g)*100)}%"></span></div>` : '')+facts([['Measured by',g.metric||''],['Measurements saved',(g.points||[]).length||''],['Fed by',(g.lands||[]).map(id=>f.lands.find(l=>l.id===id)?.name).filter(Boolean).join(', ')]])+((g.lands||[]).length?'':'<p class="small-note">No collection is linked to this goal yet.</p>')
      +`<div class="world-acts">${ref?`<button type="button" class="primary" data-record="${esc(ref)}">Open the goal</button>`:''}<button type="button" class="secondary" data-prompt="${esc(`Help me plan the next step toward our goal "${g.name}". Use what we already know and say what would move the number most.`)}">Plan the next step</button></div>${gaps.length?`<section><h3>What would move this</h3>${gaps.map(([title,prompt])=>row(prompt?`data-prompt="${esc(prompt)}"`:'',title,prompt?'Ask your AI to do it':'')).join('')}</section>`:''}`;}
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
    if(f.relationships)return relationshipMap(f);
    const node=(key,attrs,title,sub)=>`<button type="button" class="wm-node${attrs?'':' plain'}" data-key="${esc(key)}" ${attrs||'tabindex="-1"'}><b>${esc(title)}</b>${sub?`<small>${esc(sub)}</small>`:''}</button>`,col=(title,items)=>`<div class="wm-col"><h3>${title}</h3>${items||'<p class="small-note">Nothing yet.</p>'}</div>`;
    const work=[...projects.map(p=>node('p:'+p.id,`data-world-go="project:${esc(p.id)}"`,p.name,'Project')),...(f.tasks||[]).map(k=>node('t:'+k.id,k.land?`data-world-go="task:${esc(k.id)}"`:'',k.name||'Scheduled task',k.schedule||'Scheduled task'))].join('');
    return `<p class="small-note">How your work, what you know and your goals connect. A line is a saved link: a project that holds a collection or goal, a task that keeps a collection current, or a collection tied to a goal.</p><div class="wm" style="grid-template-columns:repeat(${3+((f.methods||[]).length?1:0)+((f.apps||[]).length?1:0)},minmax(0,1fr))" id="world-map"><svg class="wm-lines" aria-hidden="true"></svg>${(f.apps||[]).length?col('AI apps',f.apps.map(a=>node('a:'+a.name,`data-world-go="app:${esc(a.name)}"`,a.name,count(a.requests,'request'))).join('')):''}${(f.methods||[]).length?col('Methods',f.methods.slice(0,12).map(m=>node('m:'+m.id,`data-world-go="method:${esc(m.id)}"`,m.name,'Given to '+count(m.uses,'request'))).join('')):''}${col('Work',work)}${col('What you know',f.lands.map(l=>node('l:'+l.id,`data-world-go="land:${esc(l.id)}"`,l.name,landCounts(f,l)||'Nothing yet')).join(''))}${col('Goals',f.goals.map(g=>node('g:'+g.id,`data-world-go="goal:${esc(g.id)}"`,g.name,goalLine(g))).join(''))}</div>${mapLinks(f,projects).length?'':'<p class="small-note">Nothing is linked yet. Put a collection and a goal in the same project, or give a scheduled task a collection to keep current, and the lines appear.</p>'}`;
  }
  function drawLinks(){
    const host=$('#world-map');if(!host||!ctx)return;const box=host.getBoundingClientRect(),svg=host.querySelector('svg'),pos={};
    const focus = new Set();
    if (ctx.sel) {
      const scope = relatedFeed(ctx.feed,ctx.sel);
      for (const land of scope.lands) focus.add('l:'+land.id);
      for (const goal of scope.goals) focus.add('g:'+goal.id);
    }
    const graph=ctx.feed.relationships;
    const links = graph ? graph.edges.map(e=>[e.source,e.target,e.label]) : mapLinks(ctx.feed,state.projects||[]);
    if(graph && ctx.sel){focus.clear();focus.add(selectionKey(ctx.sel));}
    const neighbors = new Set(focus);
    for (const [a,b] of links) if (focus.has(a) || focus.has(b)) { neighbors.add(a); neighbors.add(b); }
    host.querySelectorAll('[data-key]').forEach(el => el.classList.toggle('world-dim',!!ctx.sel && !neighbors.has(el.dataset.key)));
    host.querySelectorAll('[data-key]').forEach(el=>{const r=el.getBoundingClientRect();pos[el.dataset.key]={l:r.left-box.left+host.scrollLeft,r:r.right-box.left+host.scrollLeft,y:(r.top+r.bottom)/2-box.top};});
    svg.setAttribute('width',Math.max(box.width,...Object.values(pos).map(p=>p.r)));svg.setAttribute('height',box.height);
    svg.innerHTML=links.filter(([a,b])=>pos[a]&&pos[b]).map(([a,b,label])=>{const x1=pos[a].r,x2=pos[b].l,m=(x1+x2)/2;return `<path class="${ctx.sel && !(focus.has(a) || focus.has(b)) ? 'world-dim' : ''}" d="M${x1},${pos[a].y} C${m},${pos[a].y} ${m},${pos[b].y} ${x2},${pos[b].y}"><title>${esc(label || "Recorded link")}</title></path>`;}).join('');
  }
  /* Timeline: one row per area, a mark for each thing saved, at the time it was saved. */
  function weekRecords(feed, start) {
    const from=Date.parse(start), end=from+7*864e5, events=[];
    function add(at,key,title,kind) {
      const time=Date.parse(at);
      if (time>=from && time<end) events.push({at,time,key,title,kind});
    }
    for (const land of feed.lands) for (const item of land.items)
      add(item.first_seen,'item:'+land.id+'|'+item.id,item.title,'Tracked');
    for (const f of feed.findings) if (f.label!=='replaced') add(f.at,'finding:'+f.id,f.statement,'Finding');
    for (const c of feed.changes) add(c.at,'item:'+c.land+'|'+c.item_id,c.title,'Changed');
    for (const d of feed.decisions) add(d.at,'decision:'+d.id,d.title,'Decision');
    for (const g of feed.goals) for (const point of g.points || [])
      add(point.at,'goal:'+g.id,g.name+' · '+value(point.value,g.unit),'Measured');
    return events.sort((a,b)=>a.time-b.time);
  }

  function timelineView(f){
    const t=d=>Date.parse(d),end=t(f.as_of)||Date.now(),times=[t(f.business.since),...f.lands.flatMap(l=>l.items.map(i=>t(i.first_seen))),...f.findings.map(x=>t(x.at)),...f.changes.map(c=>t(c.at)),...f.goals.flatMap(g=>(g.points||[]).map(p=>t(p.at))),...f.decisions.map(d=>t(d.at))].filter(Number.isFinite);
    const coming=[...(f.tasks||[]).filter(k=>k.next_run).map(k=>[k.next_run,'Next run: '+(k.name||'Scheduled task'),k.land?'task:'+k.id:'']),...(f.deadlines||[]).map(d=>[d.due,'Due: '+d.title,'item:'+d.collection_id+'|'+d.item_id])].filter(c=>t(c[0])>end&&t(c[0])<end+45*864e5);
    const now=end,last=Math.max(now,...coming.map(c=>t(c[0]))),start=Math.min(now-864e5,...times),pct=d=>Math.max(0,Math.min(100,100*((typeof d==='number'?d:t(d))-start)/(last-start))).toFixed(2);
    const mark=(cls,d,title,go)=>Number.isFinite(t(d))?`<button type="button" class="wt-mark ${cls}" style="left:${pct(d)}%" title="${esc(title+' · '+when(d))}" aria-label="${esc(title+', '+when(d))}" ${go?`data-world-go="${esc(go)}"`:''}></button>`:'';
    const lane=(label,go,marks)=>`<div class="wt-row"><button type="button" class="wt-label${go?'':' plain'}" ${go?`data-world-go="${esc(go)}"`:'tabindex="-1"'}>${esc(label)}</button><div class="wt-strip">${marks}</div></div>`;
    const rows=f.lands.map(land=>{
      const events=[
        ...land.items.map(i=>['item',i.first_seen,'Tracked: '+i.title,'item:'+land.id+'|'+i.id]),
        ...f.findings.filter(x=>x.land===land.id && x.label!=='replaced').map(x=>['finding',x.at,'Finding: '+x.statement,'finding:'+x.id]),
        ...f.changes.filter(c=>c.land===land.id).map(c=>['change',c.at,'Changed: '+c.title,'item:'+land.id+'|'+c.item_id])
      ];
      if(events.length<=45)return lane(land.name,'land:'+land.id,events.map(event=>mark(...event)).join(''));
      const buckets=new Map();
      for(const [,date] of events){
        if(!Number.isFinite(t(date)))continue;
        const monday=new Date(date);
        monday.setUTCHours(0,0,0,0);
        monday.setUTCDate(monday.getUTCDate()-(monday.getUTCDay()+6)%7);
        const key=monday.toISOString();
        buckets.set(key,(buckets.get(key)||0)+1);
      }
      return lane(land.name,'land:'+land.id,[...buckets].map(([date,n])=>
        `<button type="button" class="wt-bar" data-world-week="${esc(date)}" data-week-land="${esc(land.id)}" style="left:${pct(t(date)+3.5*864e5)}%;height:${Math.min(100,22+12*Math.log2(n))}%" title="${esc(land.name+' · '+count(n,'event')+' · week of '+when(date))}"></button>`).join(''));
    });
    const measured=f.goals.filter(g=>(g.points||[]).length);
    if(measured.length)rows.push(lane('Goals','',measured.map(g=>g.points.map(p=>mark('measure',p.at,`${g.name}: ${value(p.value,g.unit==='USD'?'USD':'')}`,'goal:'+g.id)).join('')).join('')));
    if(f.decisions.length)rows.push(lane('Decisions','',f.decisions.map(d=>mark('decision',d.at,'Decided: '+d.title,'decision:'+d.id)).join('')));
    const weeks=(f.work||[]).filter(w=>w.requests),most=Math.max(1,...weeks.map(w=>w.requests));
    const split=(f.work_by||[]).filter(g=>g.weeks.some(Boolean)),tall=Math.max(1,...split.flatMap(g=>g.weeks));
    for(const g of split){const name=g.kind==='project'?(state.projects||[]).find(p=>p.id===g.id)?.name||'A project':g.kind==='land'?f.lands.find(l=>l.id===g.id)?.name||'A collection':'Other chats';
      rows.push(lane('Work: '+name,g.kind==='land'?'land:'+g.id:'',g.weeks.map((n,i)=>n&&f.work?.[i]?`<button type="button" data-world-week="${esc(f.work[i].start)}" class="wt-bar" style="left:${pct(t(f.work[i].start)+3.5*864e5)}%;height:${Math.max(12,Math.round(n/tall*100))}%" title="${esc(name+', week of '+when(f.work[i].start)+': '+count(n,'request'))}"></button>`:'').join('')));}
    if(weeks.length&&!split.length)rows.push(lane('AI requests','',weeks.map(w=>`<button type="button" data-world-week="${esc(w.start)}" class="wt-bar" style="left:${pct(t(w.start)+3.5*864e5)}%;height:${Math.max(12,Math.round(w.requests/most*100))}%" title="${esc('Week of '+when(w.start)+': '+count(w.requests,'request'))}"></button>`).join('')));
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
    return `<div class="we-map">${out.map((b,i)=>{
      const tag = b.chats?.length ? 'button' : 'div';
      const action = tag === 'button' ? ` type="button" data-effort-key="${esc(b.key)}"` : '';
      return `<${tag} class="we-block"${action} style="left:${b.x.toFixed(2)}%;top:${b.y.toFixed(2)}%;width:${b.w.toFixed(2)}%;height:${b.h.toFixed(2)}%;--we-h:${(i*67+200)%360}" title="${esc(b.name+' · '+b.sub)}"><b>${esc(b.name)}</b><small>${esc(b.sub)}</small></${tag}>`;
    }).join('')}</div>`;
  }

  function effortChart(groups, metric) {
    const chart = groups.some(g=>g[metric]>0) ? blocks(groups.map(g => ({...g,value:g[metric] || 0}))) : '<p class="small-note">No positive reported values for this measure.</p>';
    const receipts = groups.filter(g=>g.chats?.length).map(g => {
      const chats = g.chats.map(c=>row(c.id ? `data-edit-chat="${esc(c.id)}"` : '', c.title,
        [c.agent,c.model,count(c.requests,'request'), c.tokens ? compact(c.tokens)+' tokens' : '',
         typeof c.cost_usd==='number' && c.missing_costs!==c.requests ? money(c.cost_usd) : '',c.missing_costs ? 'Some costs unreported' : ''].filter(Boolean).join(' · '))).join('');
      return `<details data-effort-details="${esc(g.key)}"><summary>${esc(g.name)} · ${esc(g.sub)}</summary>${chats}</details>`;
    }).join('');
    return chart + receipts;
  }
  function effortRows(u,f,heading='By AI app'){
    const groups = (u?.groups || []).filter(g => g.requests);
    if (!groups.length) return '<p>No AI requests have been recorded this month.</p>';
    const metric = ctx?.metric || 'requests';
    const allChats = (f?.effort || []).flatMap(g=>g.chats || []);
    function chartGroup(g, key, name, chats) {
      const tokens = g.tokens ?? ((g.input_tokens || 0) + (g.output_tokens || 0));
      const sub = [count(g.requests,'request'), tokens ? compact(tokens)+' tokens' : '',
        typeof g.cost_usd==='number' && g.missing_costs!==g.requests ? money(g.cost_usd) : '',
        g.missing_costs ? 'cost not reported for '+g.missing_costs : ''].filter(Boolean).join(' · ');
      return {...g, name, key, chats, tokens, sub};
    }
    const apps = groups.map((g,i)=>chartGroup(g,'app'+i,g.name || 'Unnamed app',g.chats || allChats.filter(c=>c.agent===g.name)));
    const tied = (f?.effort || []).map((g,i)=>{
      const name = g.kind==='land' ? f.lands.find(l=>l.id===g.id)?.name : g.kind==='project' ? (state.projects || []).find(p=>p.id===g.id)?.name : 'Other chats';
      return chartGroup(g,'work'+i,name || 'Linked work',g.chats);
    });
    const modelGroups=new Map();
    for(const chat of allChats){
      const name=chat.model || 'Model unreported';
      if(!modelGroups.has(name))modelGroups.set(name,{name,requests:0,tokens:0,cost_usd:0,missing_costs:0,chats:[]});
      const group=modelGroups.get(name);
      for(const field of ['requests','tokens','cost_usd','missing_costs'])group[field]+=chat[field] || 0;
      group.chats.push(chat);
    }
    const models=[...modelGroups.values()].map((g,i)=>chartGroup(g,'model'+i,g.name,g.chats));
    const options = [['requests','Requests'],['tokens','Reported tokens'],['cost_usd','Reported cost']];
    return `<label>Size blocks by <select id="world-effort-metric">${options.map(([key,title])=>`<option value="${key}" ${key===metric?'selected':''}>${title}</option>`).join('')}</select></label>
      <p class="small-note">${count(u.requests,'request')} this month. Only reported tokens and costs are included.</p><h3>${esc(heading)}</h3>`
      + effortChart(apps,metric) + (tied.length ? '<h3>By what the work was for</h3>'+effortChart(tied,metric) : '') + (models.length ? '<h3>By reported model</h3>'+effortChart(models,metric) : '');
  }
  /* Year poster: the world, the year's outcomes, and each day something was saved. */
  function posterData(f) {
    const today = new Date(f.as_of);
    const year = today.getFullYear();
    const day = date => {
      const d = new Date(date);
      return d.getFullYear() === year ? (Date.UTC(year,d.getMonth(),d.getDate()) - Date.UTC(year,0,1))/864e5 : -1;
    };
    const counts = Array(day(f.as_of)+1).fill(0);
    function tally(dates) {
      let count = 0;
      for (const date of dates) {
        const index = day(date);
        if (index >= 0 && index < counts.length) { counts[index]++; count++; }
      }
      return count;
    }
    const stats = [
      ['Tracked this year',tally(f.lands.flatMap(l=>l.items.map(i=>i.first_seen)))],
      ['Findings this year',tally(f.findings.filter(x=>x.label!=='replaced').map(x=>x.at))],
      ['Changes noticed',tally(f.changes.map(c=>c.at))]
    ];
    const goals=f.goals.filter(g=>typeof g.target==='number');
    if (goals.length) stats.push(['Goals reached',goals.filter(g=>g.reached).length+' of '+goals.length]);
    return {year,counts,stats};
  }

  function posterView(f){
    const {year,stats}=posterData(f);
    return `<div class="wp"><div class="wp-card" id="world-poster-card"></div><div class="wp-side">
      <div class="kind">${year} with AURA</div><h2>${esc(f.business.name)}</h2>
      <dl class="world-facts">${stats.map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>
      <p class="small-note">The calendar counts saved records, not activity. Goals show their current progress.</p>
      <button type="button" class="primary" id="world-poster-dl">Download image</button></div></div>`;
  }

  function drawPoster(f, host) {
    const {year,counts,stats}=posterData(f);
    const canvas=document.createElement('canvas'), width=canvas.width=1080;
    canvas.height=1260;
    const pen=canvas.getContext('2d'), style=getComputedStyle(host);
    const paper=style.getPropertyValue('--paper').trim() || '#15191c';
    const ink=style.color, accent=style.getPropertyValue('--accent').trim() || ink;
    pen.fillStyle=paper; pen.fillRect(0,0,width,canvas.height);
    const image=world()?.available && world().model() ? world().poster() : null;
    if(image) pen.drawImage(image,180,100,720,900,310,0,460,505);
    function line(text,y,size,color=ink) {
      pen.fillStyle=color; pen.font='600 '+size+'px '+style.fontFamily;
      pen.fillText(text,64,y,width-128);
    }
    line(year+' with AURA',510,28,accent); line(f.business.name,590,62);
    stats.forEach(([k,v],i)=>line(k+'   '+v,665+i*58,34));
    line('Saved records by day',956,30);
    const max=Math.max(1,...counts);
    const offset=new Date(year,0,1).getDay();
    counts.forEach((n,i)=>{
      const day=i+offset;
      pen.globalAlpha=n ? .4+.6*n/max : .12; pen.fillStyle=n ? accent : ink;
      pen.fillRect(64+Math.floor(day/7)*18,985+(day%7)*23,14,18);
    });
    pen.globalAlpha=1; line('January – '+new Date(f.as_of).toLocaleDateString(undefined,{month:'long',day:'numeric'}),1200,24);
    canvas.setAttribute('role','img'); canvas.setAttribute('aria-label',f.business.name+' · '+year+' year poster');
    host.replaceChildren(canvas); return canvas;
  }

  // One index per immutable feed; every lens reads the same recorded links.
  const relationshipIndexes = new WeakMap();
  function relationshipIndex(feed) {
    if (relationshipIndexes.has(feed)) return relationshipIndexes.get(feed);
    const graph=feed.relationships || {nodes:[],edges:[]};
    const nodes=new Map(graph.nodes.map(n=>[n.key,n])), adjacent=new Map();
    for(const edge of graph.edges) for(const key of [edge.source,edge.target]) {
      if(!adjacent.has(key)) adjacent.set(key,[]);
      adjacent.get(key).push(edge);
    }
    const index={nodes,adjacent,edges:graph.edges};
    relationshipIndexes.set(feed,index);return index;
  }
  const selectionKey=selection=>selection ? (selection.kindOf || selection.kind)+':'+selection.id : '';
  function relationshipAreas(feed, selection) {
    const index=relationshipIndex(feed),start=selectionKey(selection),seen=new Set([start]),areas=new Set();
    let frontier=[start];
    // Follow to the nearest places, without fanning back out through their contents.
    for(let depth=0;depth<5 && frontier.length;depth++) {
      const next=[];
      for(const key of frontier) {
        const node=index.nodes.get(key);
        for(const land of node?.lands || []) areas.add(land);
        if(key.startsWith('land:')) {areas.add(key.slice(5));continue;}
        for(const edge of index.adjacent.get(key) || []) {
          const other=edge.source===key?edge.target:edge.source;
          if(!seen.has(other)){seen.add(other);next.push(other);}
        }
      }
      if(areas.size) break;
      frontier=next;
    }
    return [...areas];
  }
  const kindName=kind=>({land:'Area',method:'Library item',item:'Tracked result',chat:'Conversation',app:'AI app',task:'Scheduled task',goal:'Goal',agent:'Agent',project:'Project',finding:'Finding',decision:'Decision',record:'Evidence',file:'File'}[kind] || kind);
  const incomingLabel={
    'Bound to goal':'Assigned to this goal','Bound to collection':'Assigned to this collection',
    'Bound to project':'Assigned to this project','Saved in collection':'Tracked here','Saved in area':'Finding in this area',
    'Attached to conversation':'Attached to this conversation','Linked in project':'Project containing this item',
    'Produced saved asset':'Created by','Conversation in app':'AI app used','Cited by decision':'Basis for this decision',
    'Source for tracked result':'Source for this result','Cited by evidence':'Source cited here'
  };
  function relationshipRows(feed, selection) {
    const index=relationshipIndex(feed),key=selectionKey(selection),edges=index.adjacent.get(key)||[];
    const rows=edges.map(edge=>{
      const outgoing=edge.source===key,other=index.nodes.get(outgoing?edge.target:edge.source);
      if(!other)return '';
      return row(`data-world-go="${esc(other.key)}"`,other.name,
        (outgoing?edge.label:incomingLabel[edge.label] || edge.label)+' · '+kindName(other.kind));
    });
    const first=rows.slice(0,30).join(''),rest=rows.slice(30);
    return first+
      (rest.length?'<details><summary>'+rest.length+' more connections</summary>'+rest.join('')+'</details>':'')+
      (!rows.length?'<p>No direct relationship has been recorded for this selection.</p>':'');
  }
  function relationshipMap(feed) {
    const index=relationshipIndex(feed),key=selectionKey(ctx?.sel);
    const wanted=new Set(key?[key]:[...index.nodes.values()].filter(n=>['app','project','land','goal','task','agent'].includes(n.kind)).map(n=>n.key));
    if(key)for(const edge of index.adjacent.get(key)||[]){wanted.add(edge.source);wanted.add(edge.target);}
    const all=[...wanted].map(k=>index.nodes.get(k)).filter(Boolean);
    const shown=all.slice(0,90),groups=[['Inputs',['file','record','method','app']],['Work',['chat','agent','task','project']],['Saved work',['land','item','finding','decision']],['Goals',['goal']]].filter(([,kinds])=>shown.some(node=>kinds.includes(node.kind)));
    return '<p class="small-note">Select a connection to follow it.</p>'+
      '<div class="wm" id="world-map" style="grid-template-columns:repeat('+Math.max(1,groups.length)+',minmax(150px,1fr))"><svg class="wm-lines" aria-hidden="true"></svg>'+groups.map(([title,kinds])=>
        '<div class="wm-col"><h3>'+title+'</h3>'+shown.filter(n=>kinds.includes(n.kind)).map(n=>
          `<button type="button" class="wm-node" data-key="${esc(n.key)}" data-world-go="${esc(n.key)}" aria-pressed="${n.key===key}"><b>${esc(n.name)}</b><small>${esc(kindName(n.kind))}</small></button>`).join('')+'</div>').join('')+'</div>'+
      (all.length>shown.length?'<p class="small-note">Showing '+shown.length+' of '+all.length+' nodes. Select an area to narrow the diagram; all direct links remain in the list below.</p>':'');
  }

  function recordFor(feed, kind, id) {
    const groups={project:state.projects,method:feed.methods,app:feed.apps};
    if (groups[kind]) {
      const raw=groups[kind].find(x=>(kind==='app' ? x.name : x.id)===id);
      if(raw)return {kind,id,raw,name:raw.name};
    }
    const goal = kind === 'goal' && feed.goals.find(g => g.id === id);
    if (goal) return {kind, id, name:goal.name, raw:goal};
    const decision = kind === 'decision' && feed.decisions.find(d => d.id === id);
    if (decision) return {kind, id, name:decision.title, raw:decision};
    const area = kind === 'land' && feed.uncharted?.find(a => 'new:' + a.id === id);
    if (area) return {...area, id, kindOf:'land', unch:true};
    const selectedFinding=kind==='finding' && feed.findings.find(f=>f.id===id);
    const selectedTask=kind==='task' && feed.tasks?.find(t=>t.id===id);
    for (const land of feed.lands) {
      if(kind==='finding' && selectedFinding?.land!==land.id) continue;
      if(kind==='task' && selectedTask?.land!==land.id) continue;
      if(kind==='land' && land.id!==id) continue;
      if(!['item','finding','task','land'].includes(kind)) break;
      if (kind==='item' && !id.startsWith(land.id+'|')) continue;
      const things = land.items.map(raw => ({kind:'item', id:land.id+'|'+raw.id, name:raw.title, land, raw, need:raw.needs_review, seen:Date.parse(raw.last_seen || raw.first_seen)}));
      const finds = feed.findings.filter(f => f.land === land.id && f.label !== 'replaced')
        .map(raw => ({kind:'finding', id:raw.id, name:raw.statement, label:raw.label, raw, land}));
      if (kind === 'land' && id === land.id) return {...land, kindOf:'land', things, finds};
      const item = [...things, ...finds].find(x => x.kind === kind && x.id === id);
      if (item) return item;
      const task = kind === 'task' && feed.tasks?.find(t => t.id === id && t.land === land.id);
      if (task) return {kind, id, name:task.name, raw:task, land};
    }
    const node=relationshipIndex(feed).nodes.get(kind+':'+id);
    return node ? {kind,id,name:node.name,raw:node,relationship:true} : null;
  }

  function savePlace() {
    if (!ctx) return;
    try {
      sessionStorage.setItem('aura-view:'+JSON.stringify([ctx.workspace,ctx.business]),JSON.stringify({
        tab:ctx.tab, selection:ctx.sel ? {kind:ctx.sel.kindOf || ctx.sel.kind,id:ctx.sel.id} : null,
        camera:world()?.cameraState?.(),compare:ctx.compare,compareOpen:ctx.compareOpen
      }));
    } catch { /* Browsers may disable session storage. Navigation still works. */ }
  }

  function selectionChanged(selection, remember=true) {
    if (remember && ctx.sel && selection && (ctx.sel.id!==selection.id || ctx.sel.kind!==selection.kind)) {
      const history=ctx.history || [];
      ctx.history=[...history,{kind:ctx.sel.kindOf || ctx.sel.kind,id:ctx.sel.id,camera:world()?.cameraState?.(),tab:ctx.tab}].slice(-20);
      ctx.previous=ctx.history.at(-1);
    }
    ctx.sel=selection;
    paintSide();
  }

  function selectRecord(kind, id, fly = true) {
    const selection=recordFor(ctx.feed,kind,id);
    if (!selection) {
      ctx.sel=null;
      world()?.clear?.();
      paintSide();
      return;
    }
    const prior=ctx.sel;
    const camera=world()?.cameraState?.();
    ctx.restoring=!fly;
    world()?.filter?.(ctx.filter);
    if (world()?.available && world().focus(kind, id, fly)) {ctx.restoring=false;return;}
    world()?.clear?.();
    ctx.sel=prior;
    selectionChanged(selection,fly);
    if (ctx.previous && fly) ctx.previous.camera=camera;
    world()?.filter?.({lands:relatedFeed(ctx.feed,selection).lands.map(l=>l.id),scoped:true});
    ctx.restoring=false;
  }

  function relatedFeed(feed, selection) {
    if (!selection) return feed;
    const graphAreas=feed.relationships ? relationshipAreas(feed,selection) : null;
    const areas = new Set(graphAreas || (selection.kind === 'finding' ? selection.raw.lands || [selection.land?.id] : selection.kind === 'project' ? landsFor(feed,'project:'+selection.id) :
      ['goal','method','app'].includes(selection.kind) ? selection.raw.lands :
      [selection.kindOf === 'land' ? selection.id : selection.land?.id]));
    const lands = feed.lands.filter(l => areas.has(l.id));
    const findings = feed.findings.filter(x => areas.has(x.land) || x.lands?.some(id=>areas.has(id)));
    const findingIds = new Set(findings.map(f => f.id));
    return {...feed, lands, findings,
      changes:feed.changes.filter(c => areas.has(c.land)),
      decisions:feed.decisions.filter(d => d.id === selection.id || d.basis?.some(id => findingIds.has(id))),
      goals:feed.goals.filter(g => g.id === selection.id || g.lands?.some(id => areas.has(id))),
      tasks:(feed.tasks || []).filter(t => t.goal === selection.id || areas.has(t.land)),
      deadlines:(feed.deadlines || []).filter(d => areas.has(d.collection_id)),
      effort:(feed.effort || []).filter(g => (g.kind === 'land' && areas.has(g.id)) || (g.kind==='project' && selection.kind==='project' && g.id===selection.id)),
      work_by:(feed.work_by || []).filter(g => (g.kind === 'land' && areas.has(g.id)) || (g.kind==='project' && selection.kind==='project' && g.id===selection.id)),
      work:(feed.work || []).map(w => ({...w, requests:0})),
    };
  }

  function evidenceRows(finding) {
    const labels={supports:'Supports this finding',derived_from:'This finding was derived from',extends:'Extends this finding',contradicts:'Challenges this finding'};
    return (finding.source_details || []).map(e => {
      const evidence=row(e.record ? `data-record="${esc(e.record)}"` : '',e.statement,labels[e.relationship] || 'Linked evidence');
      const sources=(e.sources || []).map(source=>row(source.record ? `data-record="${esc(source.record)}"` : '',source.title,'Source cited by this evidence')).join('');
      return '<div class="world-evidence">'+evidence+sources+'</div>';
    }).join('');
  }

  function changesSince(feed, date) {
    const since=Date.parse(date), end=Date.parse(feed.as_of);
    if (!Number.isFinite(since) || since>end) return [];
    const changes=[];
    for (const land of feed.lands) for (const item of land.items) {
      const key='item:'+land.id+'|'+item.id;
      if (Date.parse(item.first_seen)>since) changes.push({key,title:item.title,detail:'Added '+when(item.first_seen),at:item.first_seen});
      const points=(item.history || []).filter(p=>Number.isFinite(Date.parse(p.at))).sort((a,b)=>Date.parse(a.at)-Date.parse(b.at));
      const before=points.filter(p=>Date.parse(p.at)<=since).at(-1);
      const after=points.filter(p=>Date.parse(p.at)>since && Date.parse(p.at)<=end).at(-1);
      if (before && after) for (const [field, current] of Object.entries(after.values)) {
        const previous=before.values[field];
        if (typeof previous==='number' && typeof current==='number' && previous!==current)
          changes.push({key,title:item.title,detail:field+': '+value(previous)+' → '+value(current),at:after.at});
      }
    }
    for (const f of feed.findings) {
      if (Date.parse(f.at)>since) changes.push({key:'finding:'+f.id,title:f.statement,detail:f.label==='replaced'?'Finding superseded':'Finding saved · '+(FLABEL[f.label] || f.label),at:f.at});
      else if (Date.parse(f.updated_at)>since) changes.push({key:'finding:'+f.id,title:f.statement,detail:'Finding updated · '+(FLABEL[f.label] || f.label),at:f.updated_at});
    }
    for (const c of feed.changes) if (Date.parse(c.at)>since)
      changes.push({key:'item:'+c.land+'|'+c.item_id,title:c.title,detail:c.reason || c.kind || 'Saved details changed',at:c.at,land:c.land});
    for (const g of feed.goals) {
      const points=(g.points || []).slice().sort((a,b)=>Date.parse(a.at)-Date.parse(b.at));
      const before=points.filter(p=>Date.parse(p.at)<=since).at(-1),after=points.filter(p=>Date.parse(p.at)>since).at(-1);
      if (before && after && before.value!==after.value)
        changes.push({key:'goal:'+g.id,title:g.name,detail:value(before.value,g.unit)+' → '+value(after.value,g.unit),at:after.at});
    }
    for (const d of feed.decisions) if (Date.parse(d.at)>since)
      changes.push({key:'decision:'+d.id,title:d.title,detail:d.kind==='lesson'?'Lesson saved':'Decision recorded',at:d.at});
    return changes.sort((a,b)=>Date.parse(b.at)-Date.parse(a.at));
  }

  function comparisonFeed(feed, selection) {
    if (!selection) return feed;
    if (selection.kind==='goal') return {...feed,goals:feed.goals.filter(g=>g.id===selection.id)};
    if (!['item','finding'].includes(selection.kind)) return feed;
    const itemKeys = new Set(selection.kind==='item' ? [selection.id] :
      (selection.raw.related_items || (selection.raw.items || []).map(id=>({id,land:selection.land.id}))).map(ref=>ref.land+'|'+ref.id));
    const findings=feed.findings.filter(f=>f.id===selection.id ||
      (f.related_items || (f.items || []).map(id=>({land:f.land,id}))).some(ref=>itemKeys.has(ref.land+'|'+ref.id)));
    const ids=new Set(findings.map(f=>f.id));
    return {...feed,lands:feed.lands.map(l=>({...l,items:l.items.filter(item=>itemKeys.has(l.id+'|'+item.id))})),
      findings,changes:feed.changes.filter(c=>itemKeys.has(c.land+'|'+c.item_id)),goals:[],
      decisions:feed.decisions.filter(d=>d.basis?.some(id=>ids.has(id)))};
  }

  function comparisonView(feed) {
    const date=ctx.compare || new Date(Date.parse(feed.as_of)-7*864e5).toISOString().slice(0,10);
    const changes=changesSince(comparisonFeed(feed,ctx.sel),date);
    const visible=changes.slice(0,ctx.compareLimit || 60);
    const entries=visible.map(change=>{
      const [kind,...id]=change.key.split(':');
      const existing=recordFor(ctx.feed,kind,id.join(':'));
      const action=existing ? `data-world-go="${esc(change.key)}"` : change.land ? `data-collection="${esc(change.land)}"` : '';
      return row(action,change.title,change.detail,when(change.at));
    }).join('');
    return `<section class="world-comparison"><label>Changes since <input id="world-compare-date" type="date" value="${esc(date)}" max="${esc(feed.as_of.slice(0,10))}"></label>
      <p class="small-note">Saved changes and measurements through ${esc(when(feed.as_of))}. Earlier values appear where a dated measurement was kept.</p>
      ${entries || '<p>No saved changes in this selection for this period.</p>'}
      ${changes.length>visible.length?`<button class="text-button" data-world-more-changes>Show more changes (${changes.length-visible.length} remaining)</button>`:''}</section>`;
  }

  function connections(feed, selection) {
    if (!selection) return mapView(feed);
    if(feed.relationships)return relationshipRows(feed,selection);
    const scoped = relatedFeed(feed, selection);
    const links = [];
    if (selection.kind==='finding') links.push(evidenceRows(selection.raw));
    for (const goal of scoped.goals) if (goal.id !== selection.id)
      links.push(row(`data-world-go="goal:${esc(goal.id)}"`, goal.name, 'Goal linked to this area'));
    for (const land of scoped.lands) if (land.id !== selection.id)
      links.push(row(`data-world-go="land:${esc(land.id)}"`, land.name, selection.kind === 'goal' ? 'Collection linked to this goal' : 'Saved in this area'));
    if (selection.kind==='finding') for (const reference of selection.raw.related_items || (selection.raw.items || []).map(id=>({id,land:selection.land.id}))) {
      const land=feed.lands.find(l=>l.id===reference.land),item=land?.items.find(i=>i.id===reference.id);
      if(item) links.push(row(`data-world-go="item:${esc(reference.land+'|'+item.id)}"`,item.title,'Shares a saved source · '+land.name));
    }
    for (const finding of scoped.findings) if (finding.id !== selection.id && finding.label !== 'replaced')
      links.push(row(`data-world-go="finding:${esc(finding.id)}"`, finding.statement, 'Finding saved in this area'));
    for (const task of scoped.tasks) if (task.id !== selection.id)
      links.push(row(task.land ? `data-world-go="task:${esc(task.id)}"` : 'data-view="tools"', task.name, task.goal === selection.id ? 'Scheduled for this goal' : 'Keeps this collection current'));
    for (const decision of scoped.decisions) if (decision.id !== selection.id)
      links.push(row(`data-world-go="decision:${esc(decision.id)}"`, decision.title, 'Cites a finding in this area'));
    const areas = new Set(scoped.lands.map(l => l.id));
    for (const project of state.projects || []) {
      if (selection.kind==='project' && selection.id===project.id) continue;
      if (project.members?.some(m => (m.kind==='collection' && areas.has(m.id)) || (m.kind==='goal' && selection.kind==='goal' && m.id===selection.id)))
        links.push(row(`data-open-project="${esc(project.id)}"`,project.name,'Project containing this work'));
    }
    for (const app of feed.apps || []) if (selection.id!==app.name && app.lands?.some(id=>areas.has(id)))
      links.push(row(`data-world-go="app:${esc(app.name)}"`,app.name,'Chat linked to this area'));
    for (const method of feed.methods || []) if (selection.id!==method.id && method.lands?.some(id=>areas.has(id)))
      links.push(row(`data-world-go="method:${esc(method.id)}"`,method.name,'Attached alongside this collection'));
    return links.join('') || (selection.kind === 'goal'
      ? `<p>No evidence linked to this goal yet.</p><button class="primary" data-prompt="${esc('Find evidence for our goal “'+selection.name+'”. Check what we have already saved and tell me what supports it and what is still missing.')}">Find evidence for this goal</button>`
      : '<p>No saved links here yet.</p>');
  }

  function showTab(tab){
    if(!ctx||!$('#world-stage'))return;ctx.tab=tab;ctx.expanded=false;document.querySelectorAll('[data-world-tab]').forEach(button=>{
      const selected=button.dataset.worldTab===tab;
      button.setAttribute('aria-selected',String(selected));
      button.tabIndex=selected?0:-1;
    });
    world()?.lens?.(tab==='map'?'links':tab==='effort'?'effort':'');paintSide();
  }
  /* The last visit and the tour are kept with the other aura choices, so they follow the person between browsers. */
  const remember=patch=>{state.data.aura_preferences={...(state.data.aura_preferences||{}),...patch};api('/api/preferences',{business:state.business,aura:patch}).then(()=>{hq().paintMark?.();hq().paint?.(true);}).catch(()=>{});};
  function mountWorld(){
    const host=$('#world-stage');if(!host||!ctx)return;
    let ok=false;try{ok=!!world()?.available&&world().mount(host,ctx.feed,{select:o=>{if(ctx){world()?.filter?.(ctx.filter);selectionChanged(o,!ctx.restoring);}},seen:ctx.seen,toured:ctx.toured,remember,running:runningNow});if(ok)world().filter(ctx.filter);}catch(error){console.error(error);ok=false;}
    if(!ok)host.innerHTML='<p class="world-fallback">This computer cannot draw the 3D world. Everything in it is listed beside this, and in the other views.</p>';
    ctx.seen=ctx.feed.as_of;ctx.toured=true;world()?.lens?.(ctx.tab==='map'?'links':ctx.tab==='effort'?'effort':'');paintSide();
  }
  function paintChrome(){
    if(!ctx||!$('#world-tools'))return;const q=$('#world-q')?.value||'',[top,keys='']=tools(ctx.feed).split('\u0001');
    $('#world-tools').innerHTML=top;$('#world-keys').innerHTML=keys;for(const el of [...$('#world-keys').querySelectorAll('.world-by,.small-note')])$('#world-tools').appendChild(el);if(q&&$('#world-q'))$('#world-q').value=q;

  }
  /* The list beside the world follows the lens: the world's own list, or the same records as connections, time, effort or the year. */
  function paintSide(){
    const host=$('#world-side');if(!host||!ctx)return;const f=ctx.feed,tab=ctx.tab;
    const scoped = relatedFeed(f, ctx.sel);
    const scope = ctx.sel && tab !== 'world' && tab !== 'poster'
      ? `<p><b>${esc(ctx.sel.name)}</b> <button class="text-button" data-world-details>Open details</button> <button class="text-button" data-world-clear>Show everything</button></p>` : '';
    const expand = ['map','timeline','effort','poster'].includes(tab)
      ? `<button type="button" class="text-button" data-world-expand>${ctx.expanded ? 'Back to globe' : 'Expand view'}</button>` : '';
    host.parentElement.classList.toggle('world-expanded', !!ctx.expanded);
    host.parentElement.classList.toggle('world-focused', !!ctx.sel);
    if (tab==='timeline' && ctx.compareOpen) {
      const since=ctx.compare || new Date(Date.parse(f.as_of)-7*864e5).toISOString().slice(0,10);
      world()?.compare?.(changesSince(comparisonFeed(scoped,ctx.sel),since).map(c=>c.key));
    } else if(tab==='timeline' && ctx.week)world()?.compare?.(weekRecords(scoped,ctx.week).map(r=>r.key));
    else world()?.compare?.(null);
    if (tab === 'map') host.innerHTML = expand + '<h2>Connections</h2>' + scope + (ctx.expanded && ctx.sel ? mapView(f) : '') + connections(f, ctx.sel);
    else if (tab === 'timeline') {
      host.innerHTML = expand + '<h2>Time</h2>' + scope + '<div class="world-time-modes"><button type="button" data-world-time="timeline" aria-pressed="'+!ctx.compareOpen+'">Timeline</button><button type="button" data-world-time="compare" aria-pressed="'+!!ctx.compareOpen+'">Compare changes</button></div>' + (ctx.compareOpen ? comparisonView(scoped) : timelineView(scoped));
      if (ctx.week && !ctx.compareOpen) {
        const records=weekRecords(scoped,ctx.week);
        host.insertAdjacentHTML('beforeend',`<section id="world-week" tabindex="-1"><h3>Week of ${esc(when(ctx.week))}</h3><button class="text-button" data-world-end-week>Show all dates</button>
          ${records.map(r=>row(`data-world-go="${esc(r.key)}"`,r.title,r.kind,when(r.at))).join('') || '<p>No saved records in this selection that week.</p>'}</section>`);
      }
    }
    else if (tab === 'poster') host.innerHTML = expand + posterView(f);
    else if (tab === 'effort') {
      host.innerHTML = expand + '<h2>AI effort this month</h2>' + scope + '<div id="world-effort">Reading usage…</div>';
      const target = host.querySelector('#world-effort');
      if (ctx.sel?.kind === 'method') {
        target.textContent='AURA records when a method is attached. Tokens and cost are reported for the whole request.';
      } else if (ctx.sel?.kind === 'chat') {
        const chats=(f.effort || []).flatMap(g=>g.chats || []).filter(c=>c.id===ctx.sel.id);
        target.innerHTML=effortRows({requests:chats.reduce((n,c)=>n+c.requests,0),
          groups:chats.map(c=>({...c,name:[c.agent,c.model].filter(Boolean).join(' · '),chats:[c]}))},null,'This conversation');
      } else if (ctx.sel?.kind === 'app') {
        const chats=(f.effort || []).flatMap(g=>g.chats || []).filter(c=>c.agent===ctx.sel.id);
        const total=chats.reduce((sum,c)=>sum+c.requests,0);
        target.innerHTML=chats.length ? effortRows({requests:total,groups:chats.map(c=>({...c,name:c.title,chats:[c]}))},null,'By chat') : '<p>No attributed requests this month.</p>';
      } else if (ctx.sel) {
        const groups = scoped.effort.map(g => ({...g, name:g.kind==='project' ? state.projects?.find(p=>p.id===g.id)?.name : f.lands.find(l => l.id === g.id)?.name, input_tokens:g.tokens}));
        target.innerHTML = groups.length ? effortRows({groups, requests:groups.reduce((n,g)=>n+g.requests,0)}, null, 'By linked collection')
          : '<p>No AI usage was attributed to the linked collections this month.</p>';
      } else api('/api/usage?business='+encodeURIComponent(ctx.business)+'&period=month')
        .then(u => { if (target.isConnected) target.innerHTML = effortRows(u, f); })
        .catch(() => { if (target.isConnected) target.textContent = 'Usage could not be loaded.'; });
    } else host.innerHTML = ctx.sel ? selected(f,ctx.sel) : home(f);
    if (ctx.sel && tab==='world') {
      const relationButton='<button type="button" class="text-button" data-world-tab="map">Explore connections</button>';
      host.insertAdjacentHTML('beforeend',relationButton+'<button type="button" class="text-button" data-world-compare>What changed here?</button>');
      if(ctx.sel.kind==='finding' && ctx.sel.raw.source_details?.length)
        host.insertAdjacentHTML('beforeend','<section><h3>Evidence and sources</h3>'+evidenceRows(ctx.sel.raw)+'</section>');
    }
    if (ctx.previous && ctx.sel) host.insertAdjacentHTML('afterbegin','<button class="text-button" data-world-previous>‹ Previous selection</button>');
    ctx.mapObserver?.disconnect();
    const map = host.querySelector('#world-map');
    if (map && ctx.expanded) {
      ctx.mapObserver=new ResizeObserver(()=>requestAnimationFrame(drawLinks));
      ctx.mapObserver.observe(map);
    }
    if(ctx.outcome) host.insertAdjacentHTML('afterbegin',`<div class="world-outcome" role="status">${esc(ctx.outcome)} <button type="button" class="text-button" data-world-dismiss>Dismiss</button></div>`);
    if (ctx.arrivedSince) host.insertAdjacentHTML('afterbegin','<button class="world-arrived text-button" data-world-arrived>Saved work changed · See changes</button>');
    savePlace();
    paintChrome();
    if (tab==='poster') ctx.poster=drawPoster(f,$('#world-poster-card'));
  }

  function updateWorld(feed) {
    const previous=ctx.feed, selection=ctx.sel;
    const outcomes=[];
    for(const goal of feed.goals){
      const old=previous.goals.find(g=>g.id===goal.id);
      if(old && !old.reached && goal.reached) outcomes.push('Target reached · '+goal.name);
    }
    if(selection?.kind==='item' && selection.raw.needs_review){
      const updated=recordFor(feed,'item',selection.id);
      if(updated && !updated.raw.needs_review) outcomes.push('Review cleared · '+updated.name);
    }
    if(selection?.kind==='finding'){
      const updated=feed.findings.find(f=>f.id===selection.id);
      if(updated && updated.label!==selection.raw.label)
        outcomes.push((FLABEL[updated.label] || updated.label)+' · '+updated.statement);
    }
    if(outcomes.length)ctx.outcome=outcomes.join(' · ');
    if(changesSince(relatedFeed(feed,selection),previous.as_of).length)ctx.arrivedSince=previous.as_of;
    ctx.feed=feed;
    world()?.update?.(feed);
    if(selection)selectRecord(selection.kindOf || selection.kind,selection.id,false);
    else paintSide();
  }

  /* Opening the aura goes to its own section, like Knowledge or Files. */
  async function open(){state.view='aura';await render();if(typeof recordShellRoute==='function')recordShellRoute();if(typeof renderShell==='function')await renderShell();}
  async function draw(view,current=()=>true){
    const business = state.business;
    if (ctx?.business === business && ctx.workspace === state.data.workspace && view.querySelector('#world-stage')) {
      const owner = ctx;
      const feed = await api('/api/world?business=' + encodeURIComponent(business));
      if (ctx !== owner || !current() || state.view !== 'aura' || world()?.replaying?.()) return;
      ctx.checked=Date.now();
      updateWorld(feed);
      return;
    }
    ctx?.mapObserver?.disconnect();
    view.innerHTML='<div class="aura-view world-view"><p class="world-fallback">Drawing your world…</p></div>';
    const feed=await api('/api/world?business='+encodeURIComponent(business));
    if(!feed||business!==state.business||!current()||state.view!=='aura')return;
    const previous = ctx?.business===business && ctx.workspace===state.data.workspace ? ctx : null;
    const prefs=state.data?.aura_preferences||{};ctx={business,workspace:state.data.workspace,feed,checked:Date.now(),sel:null,tab:'world',seen:prefs.seen||null,since:prefs.seen||null,toured:!!prefs.toured,filter:{lands:[],needs:false,by:''}};
    let resume;
    if (!previous) {
      try {resume=JSON.parse(sessionStorage.getItem('aura-view:'+JSON.stringify([state.data.workspace,business])) || 'null');} catch {}
      if (resume) {
        if(TABS.some(([key])=>key===resume.tab)) ctx.tab=resume.tab;
        if(resume.selection) ctx.sel=recordFor(feed,resume.selection.kind,resume.selection.id);
        if(/^\d{4}-\d{2}-\d{2}$/.test(resume.compare || ''))ctx.compare=resume.compare;
        ctx.compareOpen=!!resume.compareOpen;
      }
    }
    if (previous) {
      for (const key of ['tab','expanded','metric','chat','filter','previous','since','compare','compareOpen','history','arrivedSince']) ctx[key]=previous[key];
      if (previous.sel) ctx.sel=recordFor(feed,previous.sel.kindOf || previous.sel.kind,previous.sel.id);
    }
    view.innerHTML=`<div class="aura-view world-view"><div class="world-main"><div class="world-stage" id="world-stage"><p class="world-fallback">Drawing your world…</p></div><div class="world-top"><div class="world-tabs" role="tablist" aria-label="Ways to look at your world">${TABS.map(([k,l])=>`<button type="button" role="tab" data-world-tab="${k}" tabindex="${k===ctx.tab?0:-1}" aria-selected="${k===ctx.tab}">${l}</button>`).join('')}</div><div class="world-tools" id="world-tools"></div></div><div class="world-keys" id="world-keys"></div><div class="world-ask"><button type="button" id="world-chat">Open chat</button></div></div><aside class="world-side" id="world-side" aria-label="What is in your world"></aside></div>`;
    paintSide();
    const owner = ctx;
    try { if (!world()) await import('/workspace-world.js'); }
    catch { /* The readable view works without the renderer. */ }
    if (ctx === owner && current() && state.view === 'aura') {
      const selection = ctx.sel;
      mountWorld();
      world()?.setEffortMetric?.(ctx.metric || 'requests');
      if (selection) selectRecord(selection.kindOf || selection.kind, selection.id,false);
      world()?.restoreCamera?.(resume?.camera);
    }
  }

  function setChat(open) {
    ctx.chat = open;
    document.body.classList.toggle('world-chat-open', open);
    $('#main').inert = !open;
    if (open) $('#request').focus();
    else $('#world-chat')?.focus();
  }

  function openChat(promptText = '') {
    const o = ctx.sel;
    const box = $('#request');
    let reference;
    if (o?.kindOf === 'land' && o.kind === 'collection') {
      reference = {kind:'collection', id:o.id, label:o.name};
    } else if (o?.kind === 'item') {
      reference = {kind:'collection', id:o.land.id, label:o.land.name};
      if (!promptText) promptText = 'About “' + o.name + '” in ' + o.land.name + ': ';
    } else if (o && ['file','record','method'].includes(o.kind)) {
      reference={kind:o.kind==='method'?'library':o.kind,id:o.raw?.action?.record || o.id,label:o.name};
    } else if (o?.raw && ['goal','finding','decision'].includes(o.kind)) {
      const ref = o.raw.record || refOf(o.raw.id);
      if (ref) reference = {kind:'record', id:ref, label:o.name};
      else if (!promptText) promptText = 'About “' + o.name + '”: ';
    }
    if(o && !reference && !promptText)promptText='About “'+o.name+'”: ';
    if (reference && !window.auraCompose?.add(reference)) { setChat(true); return; }
    if (promptText && !box.value.endsWith(promptText)) {
      box.value += (box.value.trim() ? '\n\n' : '') + promptText;
      box.dispatchEvent(new Event('input', {bubbles:true}));
    }
    setChat(true);
  }

  // In the aura the sidebar's own button opens and tucks it without changing the person's saved choice for the rest of AURA.
  document.addEventListener('click',e=>{if(!e.target.closest('#sidebar-collapse')||!document.body.classList.contains('in-aura')||matchMedia('(max-width:600px)').matches)return;e.stopImmediatePropagation();e.preventDefault();state.auraSidebarOpen=!state.auraSidebarOpen;document.body.classList.toggle('sidebar-collapsed',!state.auraSidebarOpen);},true);
  document.addEventListener('click', event => {
    if (state.view !== 'aura' || !ctx || ctx.business!==state.business) return;
    if (event.target.closest('#world-chat-back')) setChat(false);
    const button = event.target.closest('.aura-view [data-prompt], #world-chat');
    if (!button) return;
    event.stopImmediatePropagation();
    openChat(button.dataset.prompt);
  }, true);

  // Refresh after individual chats finish, even when another chat is still running.
  setInterval(async () => {
    const current = ctx;
    if (!current || current.business!==state.business || current.workspace!==state.data.workspace || state.view !== 'aura' || !$('#world-stage') || document.hidden) return;
    const active = new Set(runningNow().map(job => job.id));
    if (current.running && [...current.running].some(id => !active.has(id))) current.needsRefresh = true;
    current.running = active;
    if (current.refreshing || (!current.needsRefresh && Date.now() - current.checked < 60000)) return;
    if (world()?.replaying?.()) return;
    current.needsRefresh = false;
    current.refreshing = true;
    current.checked = Date.now();
    try {
      const feed = await api('/api/world?business=' + encodeURIComponent(current.business));
      if (ctx !== current || current.business!==state.business || current.workspace!==state.data.workspace || state.view !== 'aura' || !$('#world-stage') || world()?.replaying?.()) return;
      // as_of advances even when no underlying records have changed.
      const {as_of:oldTime,...oldRecords} = current.feed;
      const {as_of:newTime,...newRecords} = feed;
      if (String(oldTime).slice(0,10)===String(newTime).slice(0,10) && JSON.stringify({...oldRecords,work:oldRecords.work?.map(w=>w.requests)}) === JSON.stringify({...newRecords,work:newRecords.work?.map(w=>w.requests)})) return;
      updateWorld(feed);
    } catch { /* Retry on the next refresh. */ }
    finally { current.refreshing = false; }
  }, 1500);
  document.addEventListener('keydown',event=>{
    const tab=event.target.closest?.('.world-tabs [role="tab"]');
    if(!tab || !ctx || !['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();
    const tabs=[...tab.parentElement.querySelectorAll('[role="tab"]')];
    let index=tabs.indexOf(tab);
    if(event.key==='Home')index=0;
    else if(event.key==='End')index=tabs.length-1;
    else index=(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
    showTab(tabs[index].dataset.worldTab);
    tabs[index].focus();
  });
  document.addEventListener('change',e=>{
    if(!ctx||ctx.business!==state.business)return;
    if(e.target.id==='world-compare-date'){ctx.compare=e.target.value;paintSide();}
    if(e.target.id==='world-effort-metric'){ ctx.metric=e.target.value; world()?.setEffortMetric?.(ctx.metric); paintSide(); }
    if(e.target.id==='world-by'){ctx.filter.by=e.target.value;ctx.filter.lands=landsFor(ctx.feed,e.target.value);world()?.filter(ctx.filter);paintSide();}
    if(e.target.id==='aura-goal'){const goal=e.target.value;state.data.aura_preferences={...(state.data.aura_preferences||{}),goal};attempt(async()=>{await api('/api/preferences',{business:state.business,aura:{goal}});hq().paintMark();hq().paint(true);paintSide();});}
  });
  const saveShift=shift=>{state.data.aura_preferences={...(state.data.aura_preferences||{}),shift};clearTimeout(shiftTimer);shiftTimer=setTimeout(()=>attempt(async()=>{await api('/api/preferences',{business:state.business,aura:{shift}});hq().paintMark();hq().paint(true);}),400);};
  document.addEventListener('input',e=>{if(!ctx)return;if(e.target.id==='aura-shift')saveShift(Number(e.target.value));if(e.target.id==='world-q')world()?.search(e.target.value);});
  document.addEventListener('click',e=>{
    if(!ctx || ctx.business!==state.business || state.view!=='aura')return;
    if(e.target.closest('#aura-shift-reset')){$('#aura-shift').value=0;saveShift(0);}
    const go=e.target.closest('.aura-view [data-world-go]');
    if(go){
      const [kind,...rest]=go.dataset.worldGo.split(':');
      selectRecord(kind,rest.join(':'));
      const selected=[...document.querySelectorAll('#world-side [data-world-go]')].find(el=>el.dataset.worldGo===go.dataset.worldGo);
      if(selected)selected.focus({preventScroll:true});
      else {const heading=$('#world-side h2');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}}
    }
    if(e.target.closest('[data-world-dismiss]')){ctx.outcome=null;paintSide();}
    const mode=e.target.closest('[data-world-time]');
    if(mode){ctx.compareOpen=mode.dataset.worldTime==='compare';paintSide();}
    const week=e.target.closest('[data-world-week]');
    if(e.target.closest('[data-world-more-changes]')){ctx.compareLimit=(ctx.compareLimit || 60)+60;paintSide();}
    if(e.target.closest('[data-world-end-week]')){ctx.week=null;paintSide();}
    if (week) {if(week.dataset.weekLand) selectRecord('land',week.dataset.weekLand);ctx.week=week.dataset.worldWeek; paintSide(); $('#world-week')?.focus();}
    const block = e.target.closest('[data-effort-key]');
    if (block) { const details = [...document.querySelectorAll('[data-effort-details]')].find(el=>el.dataset.effortDetails===block.dataset.effortKey); if(details){details.open=true;details.querySelector('summary').focus();} }
    if(e.target.closest('[data-world-arrived]')){
      ctx.compare=ctx.arrivedSince.slice(0,10);ctx.arrivedSince=null;ctx.compareOpen=true;showTab('timeline');
    }
    if (e.target.closest('[data-world-compare]')) {ctx.compareOpen=true;showTab('timeline');}
    if (e.target.closest('[data-world-details]')) showTab('world');
    if (e.target.closest('[data-world-previous]') && ctx.previous) {
      const previous = ctx.history?.pop() || ctx.previous;
      ctx.previous=ctx.history?.at(-1) || null;
      if (previous.tab) ctx.tab=previous.tab;
      selectRecord(previous.kind,previous.id,false);
      world()?.restoreCamera?.(previous.camera);
    }
    if(e.target.closest('[data-world-expand]')) { ctx.expanded = !ctx.expanded; paintSide(); $('#world-side [data-world-expand]')?.focus(); }
    if(e.target.closest('.aura-view [data-world-clear]')) { ctx.sel=null;ctx.history=[];ctx.previous=null; world()?.clear(); world()?.filter?.(ctx.filter); paintSide(); }
    const chip=e.target.closest('.aura-view [data-world-chip]'),needs=e.target.closest('.aura-view [data-world-needs]');
    if(chip||needs){if(chip){ctx.filter.by='';const id=chip.dataset.worldChip,on=ctx.filter.lands.includes(id);ctx.filter.lands=on?ctx.filter.lands.filter(x=>x!==id):[...ctx.filter.lands,id];}else ctx.filter.needs=!ctx.filter.needs;world()?.filter(ctx.filter);paintSide();}
    if(e.target.closest('.aura-view [data-world-changed]'))world()?.changed?.();
    if(e.target.closest('.aura-view [data-world-tour]'))world()?.tour?.();
    const tab=e.target.closest('.aura-view [data-world-tab]');if(tab)showTab(tab.dataset.worldTab);
    if(e.target.closest('#world-poster-dl')&&ctx.poster)ctx.poster.toBlob(blob=>{const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(ctx.feed.business.name||'aura').replace(/[^\w -]+/g,'').trim()+' year.png';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),2000);},'image/png');
  });
  window.addEventListener?.('pagehide',savePlace);
  return {relationshipIndex,relationshipAreas,relationshipRows,relationshipMap,changesSince,comparisonFeed,evidenceRows,focusChat:()=>setChat(true),leave(){savePlace();if(ctx){ctx.chat=false;ctx.mapObserver?.disconnect();}world()?.unmount?.();},relatedFeed,recordFor,chatOpen:()=>!!ctx?.chat,open,render:draw,goalLine,goalDone,home,tools,goalGaps,selected,latest,landsFor,mapView,mapLinks,timelineView,effortRows,posterView};
})();
