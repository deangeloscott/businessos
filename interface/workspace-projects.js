/* Shared project resources and maintained results. Native apps own scheduled work. */
window.auraProjects=(()=>{
  let ticket=0,current=null,selection=null,parentProject='',timer;
  const scope=()=>JSON.stringify([state.business,state.data?.workspace]);
  function panelRequest(){
    const id=++ticket,panel=state.fileDetailTicket,wasOpen=$('#detail').open;
    return ()=>id===ticket&&panel===state.fileDetailTicket&&(!wasOpen||$('#detail').open);
  }
  const url=(route,values={})=>route+'?'+new URLSearchParams({business:state.business,...values});
  const label=kind=>({asset:'File',record:'Memory',goal:'Goal',file:'File',task:'Scheduled task',collection:'Saved results',result:'Chat result',library:'Library'})[kind]||human(kind);
  async function refreshSavedWork(key){
    invalidateReads();await refresh(true,true);if(key!==scope())return;
    if(state.view==='files'){const data=await cachedApi(url('/api/files'));if(key!==scope())return;state.files=data.items;state.fileProjects=data.projects||[];renderFiles();}
  }
  function checked(check){
    if(!check)return '<span class="small-note">No check recorded yet</span>';
    const c=check.coverage,status=c.status==='complete'?'Checked':c.status==='partial'?'Partly checked':c.status==='failed'?'Check failed':'Coverage unknown';
    return `<span class="result-coverage ${['partial','failed'].includes(c.status)?'needs-review':''}">${esc(status)}${c.expected?` · ${c.checked} of ${c.expected} sources`:c.checked?` · ${c.checked} source${c.checked===1?'':'s'}`:''} · ${esc(stamp(check.at))}</span>${check.no_change_verified?'<p class="small-note">No material changes reported.</p>':''}${c.failed?.length||c.missing?.length?`<details class="result-source-status"><summary>Sources needing another check</summary><p>${esc([...new Set([...(c.failed||[]),...(c.missing||[])])].join(', '))}</p></details>`:''}`;
  }
  async function project(id){
    const key=scope(),valid=panelRequest();
    const [data,collections,files]=await Promise.all([api(url('/api/project-resources',{id})),api(url('/api/collections',{project:id})),api(url('/api/files',{project:id,limit:50}))]);
    if(key!==scope()||!valid())return;
    parentProject=data.project.id;current=null;
    const resources=data.items.filter(r=>r.kind!=='collection'),folder=data.project.folder;
    details(data.project.name,`${data.project.description?`<p>${esc(data.project.description)}</p>`:''}<div class="project-work-actions"><button class="secondary" data-create-collection="${esc(id)}">New collection or reports</button><button class="text-button" data-project-add="${esc(id)}">Add existing work</button>${folder?`<button class="text-button" data-project-open="${esc(data.project.name)}">Open folder</button>`:''}</div><div id="project-add-context" hidden></div><section class="project-resource-group"><h3>What’s running</h3><div id="project-running"><p class="small-note">Reading scheduled work…</p></div></section><section class="project-resource-group"><h3>Saved results</h3>${collections.items.map(c=>`<button class="row" data-collection="${esc(c.id)}" data-collection-project="${esc(id)}"><span><strong>${collectionUpdated(c.id)?'<span class="chat-indicator ready" aria-label="New changes"></span>':''}${esc(c.name)}</strong><small class="row-meta">${c.unavailable?'Unavailable':c.mode==='series'?'Dated reports':`${c.current_count} current ${c.current_count===1?'result':'results'}`}</small></span><span aria-hidden="true">→</span></button>`).join('')||'<p class="small-note">Keep a useful list current, or collect dated reports here.</p>'}</section><section class="project-resource-group"><h3>Linked work</h3>${resources.map((r,i)=>`<div class="project-linked-row"><button class="row" data-project-resource="${i}"><span><strong>${esc(r.label)}</strong><small class="row-meta">${label(r.kind)}${r.available===false?' · Unavailable':''}</small></span><span aria-hidden="true">→</span></button><button class="text-button" data-project-unlink="${i}" aria-label="Remove ${esc(r.label)} from project">×</button></div>`).join('')||'<p class="small-note">Link goals, files, memory, or guidance when useful.</p>'}</section><section class="project-resource-group"><h3>Files</h3>${files.items.filter(f=>!f.collection_id).map(f=>`<button class="row" ${f.collection_id?`data-collection="${esc(f.collection_id)}"`:`data-file="${esc(f.path)}"`}><span>${esc(f.name)}<small class="row-meta">${esc(f.location_name||'Workspace')}</small></span></button>`).join('')||'<p class="small-note">Files saved for this project appear here.</p>'}${files.total>files.items.length?'<p class="small-note">Open Files & media and select this project to see more.</p>':''}</section>`,'context');
    window.auraViews.running($('#project-running'),{project:id});
    $('#detail-content').querySelectorAll('[data-project-resource]').forEach(b=>b.onclick=()=>attempt(async()=>{
      const ref=resources[Number(b.dataset.projectResource)];if(key!==scope())return;
      if(['record','asset'].includes(ref.kind))recordDetails(ref.id);
      else if(ref.kind==='goal')await window.auraCompose.openGoal(ref.id);
      else if(ref.kind==='file')await openFileWorkspace(ref.id);
      else if(ref.kind==='task')await scheduleDetails(ref.id);
      else if(ref.kind==='result')await openShellChat(ref.id);
      else if(ref.kind==='library')await openLibrary(ref.id,ref.variant||'');
    }));
    $('#detail-content').querySelectorAll('[data-project-unlink]').forEach(b=>b.onclick=()=>attempt(async()=>{await api('/api/project-resources',{business:state.business,id,action:'unlink',reference:resources[Number(b.dataset.projectUnlink)]});if(key===scope())await project(id);}));
    const add=$('[data-project-add]');if(add)add.onclick=()=>{
      const host=$('#project-add-context');host.hidden=!host.hidden;if(host.hidden)return;
      window.auraInsight.references(host,[]);host.insertAdjacentHTML('beforeend','<button type="button" class="secondary" id="save-project-resources">Add to project</button>');
      $('#save-project-resources').onclick=()=>attempt(async()=>{const refs=host._references();for(const ref of refs){if(key!==scope())return;await api('/api/project-resources',{business:state.business,id,action:'link',reference:ref});}if(key===scope())await project(id);});
    };
  }
  /* Where a result came from, said the same way everywhere: your correction, its sources and when they were checked, or no source. */
  function provenance(r){
    if(r.source_count===undefined&&!r.corrected)return '';
    const chips=[];if(r.corrected)chips.push('<span class="source-chip yours">Your correction</span>');
    if(r.source_count)chips.push(`<span class="source-chip">${r.source_count} source${r.source_count===1?'':'s'}${r.checked_at?' · checked '+esc(stamp(r.checked_at)):''}</span>`);
    else if(!r.corrected)chips.push('<span class="source-chip missing">No source</span>');
    return `<p class="provenance">${chips.join('')}</p>`;
  }
  /* Findings: what a watch's results add up to, with their status and evidence, said the same way everywhere. */
  const findingLabel=(status,due)=>status==='contradicted'?['Challenged','challenged']:due?['Needs review','review']:({supported:['Supported',''],active:['Supported',''],candidate:['Unverified','unverified'],stale:['Out of date','review'],superseded:['Replaced','unverified'],archived:['Archived','unverified']})[status]||[human(status||'unknown'),'unverified'];
  function findingRow(f){
    const [label,cls]=findingLabel(f.status,f.needs_review),e=f.evidence||{};
    const parts=[e.supports?`${e.supports} supporting`:'',e.extends?`${e.extends} extending`:'',e.contradicts?`${e.contradicts} challenging`:''].filter(Boolean);
    return `<button type="button" class="row finding-row" data-finding="${esc(f.id)}"><span class="row-text"><strong class="row-title">${esc(f.statement)}</strong><small class="row-meta"><span class="source-chip ${cls}">${esc(label)}</span><span>${esc(parts.join(' · ')||'No evidence linked')}${f.supersedes?' · Replaces an earlier finding':''}${f.updated_at?' · '+esc(stamp(f.updated_at)):''}</span></small></span></button>`;
  }
  function findingsMarkup(d){
    if(!d.findings_total&&!d.replaced_total&&!d.source_memory?.length)return '';
    const summary=[d.challenged?`${d.challenged} challenged`:'',d.needs_review?`${d.needs_review} due for review`:''].filter(Boolean).join(' · ');
    return `<section class="collection-findings" aria-labelledby="collection-findings-title"><div class="mini-heading"><h3 id="collection-findings-title">What we know</h3>${summary?`<small>${esc(summary)}</small>`:''}</div>${d.findings.map(findingRow).join('')||'<p class="small-note">No current findings.</p>'}${d.findings_total>d.findings.length?`<p class="small-note">Showing ${d.findings.length} of ${d.findings_total} findings. Ask your AI about the rest.</p>`:''}${d.replaced_total?`<details class="collection-replaced"><summary>Replaced findings (${d.replaced_total})</summary>${d.replaced.map(findingRow).join('')}</details>`:''}${d.source_memory?.length?`<p class="small-note">Sources it remembers: ${d.source_memory.map(s=>`<button type="button" class="text-button" data-finding="${esc(s.id)}">${esc(s.name)}</button>`).join(', ')}</p>`:''}</section>`;
  }
  let findingBack=null;
  function finding(ref,back=findingBack){
    const r=state.data?.records?.find(x=>x.ref===ref);if(!r)return;
    if(r.type!=='Insight'){recordDetails(ref);return;}
    findingBack=back;
    const f=r.data,bos=f.extensions?.businessos||{},records=new Map(state.data.records.map(x=>[x.ref,x]));
    const [label,cls]=findingLabel(f.status,!!bos.review_after&&new Date(bos.review_after)<=new Date());
    const relation={supports:'Supports',derived_from:'Supports',extends:'Extends',contradicts:'Challenges',contextualizes:'Context'};
    const evidence=(f.evidence_links||[]).map(l=>{
      const e=records.get(l.ref),source=e?.type==='Observation'?(e.data.source_refs||[]).map(s=>records.get(s)).find(Boolean):e?.type==='SourceRecord'?e:null;
      const quote=source?.data.extensions?.businessos_evidence?.captured_text,link=source?.data.source_reference;
      return `<li class="finding-evidence"><span class="source-chip ${l.relationship==='contradicts'?'challenged':''}">${esc(relation[l.relationship]||human(l.relationship))}</span> ${e?`<button type="button" class="text-button" data-finding-evidence="${esc(source?.ref||l.ref)}">${esc(source?.title||(e.type==='Observation'?e.data.statement:e.title))}</button>`:'<span class="small-note">Evidence not found in this workspace</span>'}${l.reason?`<p class="small-note">${esc(l.reason)}</p>`:''}${quote?`<blockquote>${esc(quote.slice(0,600))}${quote.length>600?'…':''}</blockquote>`:''}${link&&/^https?:\/\//i.test(link)?`<a href="${esc(link)}" target="_blank" rel="noopener noreferrer">${esc(link)}</a>`:''}</li>`;
    }).join('');
    const link=r=>`<button class="text-button" data-record="${esc(r.ref)}">${esc(r.title)}</button>`;
    const decisions=state.data.records.filter(r=>r.type==='DecisionRecord'&&r.data.basis_refs?.includes(ref));
    const actions=decisions.map(d=>{
      const changes=state.data.records.filter(r=>r.type==='ChangeEvent'&&r.data.decision_refs?.includes(d.ref));
      return `<li>${link(d)}${changes.length?`<ul>${changes.map(c=>`<li>${link(c)} · ${esc(human(c.data.status||'unknown'))} ${(c.data.result_refs||[]).map(id=>records.get(id)).filter(Boolean).map(link).join(' · ')}</li>`).join('')}</ul>`:''}</li>`;
    }).join('');
    const replaces=bos.supersedes&&records.get(bos.supersedes),replacedBy=state.data.records.find(x=>x.type==='Insight'&&x.data.extensions?.businessos?.supersedes===ref);
    details('Finding',`${back?`<button class="text-button" data-collection="${esc(back.id)}">← Back to ${esc(back.name)}</button>`:''}<p class="item-type">Finding · Memory</p><p class="finding-statement">${esc(f.statement)}</p><p class="finding-meta"><span class="source-chip ${cls}">${esc(label)}</span>${f.reviewed_at?`<small>Reviewed ${esc(stamp(f.reviewed_at))}</small>`:''}${bos.review_after?`<small>Review after ${esc(stamp(bos.review_after))}</small>`:''}</p>${replaces?`<p class="small-note">Replaces <button type="button" class="text-button" data-finding="${esc(replaces.ref)}">an earlier finding</button>.</p>`:''}${replacedBy?`<p class="small-note">Replaced by <button type="button" class="text-button" data-finding="${esc(replacedBy.ref)}">a newer finding</button>.</p>`:''}<h3 class="finding-heading">Evidence</h3>${evidence?`<ul class="finding-evidence-list">${evidence}</ul>`:'<p class="small-note">No evidence linked yet, so this stays unverified.</p>'}${actions?`<h3>Decisions based on this finding</h3><ul>${actions}</ul>`:''}<div class="inline-actions"><button type="button" class="primary" data-add-record="${esc(ref)}" data-label="${esc(String(f.statement).slice(0,80))}">Add to chat</button><button type="button" class="text-button" data-share-record="${esc(ref)}" data-share-scope="${esc(sharingScope())}">Share a copy →</button></div><details><summary>Record data</summary><pre>${esc(JSON.stringify(f,null,2))}</pre></details>`,'context');
    setDetailTitleActions(archiveControl('record',ref));
  }
  const copiesField=value=>`<label>Keep sources as<select name="source_copies"><option value="quotes" ${value!=='full'?'selected':''}>Links and key quotes (recommended)</option><option value="full" ${value==='full'?'selected':''}>Also keep full copies</option></select></label><p class="small-note">Full copies help when sources may change or disappear. AURA keeps a copy of fragile sources either way.</p>`;
  async function openCollection(id,view='current',q='',offset=0){
    const key=scope(),valid=panelRequest(),focused=document.activeElement?.id==='collection-search',position=$('#collection-search')?.selectionStart;
    const d=await api(url('/api/collections',{id,view,q,offset,limit:30}));
    if(key!==scope()||!valid())return;
    selection={id,view,q,offset,key};current={...d,view,q,offset,key};
    const v=d.views||{},shapes=[['list','List'],...(v.map?[['map','Map']]:[]),...(v.chart?.length?[['chart','Chart']]:[]),...(v.board?.length?[['board','Board']]:[])];
    window.auraViews.release();let shape=window.auraViews.saved(id)||'';
    if(!shape){const preferred=window.auraFocus?await window.auraFocus.views():[];shape=preferred.find(v=>shapes.some(([s])=>s===v))||'list';if(key!==scope()||!valid())return;}
    if(!shapes.some(([s])=>s===shape))shape='list';
    details(d.name,`${parentProject?`<button class="text-button" data-open-project="${esc(parentProject)}">← Back to project</button>`:''}${d.purpose?`<p>${esc(d.purpose)}</p>`:''}<div class="inline-actions"><button type="button" class="secondary" data-collection-add>Add to chat</button>${resultOrigin(state.data.records.find(r=>r.ref===d.asset_id))}${view==='saved'&&d.total?`<button type="button" class="text-button" data-share-results="${esc(id)}">Copy ${d.total} saved ${d.total===1?'result':'results'} for sharing</button>`:''}<button type="button" class="text-button" data-edit-collection>Edit collection</button></div><div class="collection-check"><div id="collection-running" class="collection-running"></div>${checked(d.latest_check)}${d.last_upkeep_at?`<p class="small-note">Findings last reviewed ${esc(stamp(d.last_upkeep_at))}.</p>`:''}</div>${findingsMarkup(d)}<div class="collection-toolbar"><label class="sr-only" for="collection-search">Search results</label><input type="search" id="collection-search" placeholder="Find a result…" value="${esc(q)}"><label class="sr-only" for="collection-view">Show results</label><select id="collection-view">${[['current',d.mode==='series'?'Reports':'Current'],['changes','Changes to review'],['saved','Saved'],['review','Needs review'],['handled','Handled'],['all','All']].map(([v,n])=>`<option value="${v}" ${view===v?'selected':''}>${n}</option>`).join('')}</select>${shapes.length>1?`<label class="sr-only" for="collection-shape">Show as</label><select id="collection-shape">${shapes.map(([s,n])=>`<option value="${s}" ${shape===s?'selected':''}>${n}</option>`).join('')}</select>`:''}</div><div id="collection-visual" ${shape==='list'?'hidden':''}></div><div id="collection-items" ${shape==='list'?'':'hidden'}>${d.items.map(r=>`<article class="collection-item" data-result-id="${esc(r.id)}"><div class="collection-item-title"><h3>${esc(r.title)}</h3><button type="button" class="favorite-star ${r.saved?'active':''}" data-result-action="save" aria-label="${r.saved?'Unsave':'Save'} ${esc(r.title)}" aria-pressed="${!!r.saved}">${r.saved?'★':'☆'}</button></div><div class="result-labels">${r.display_state!=='active'?`<span>${esc(human(r.display_state))}</span>`:''}${r.needs_review?'<span>Needs review</span>':''}${r.disposition==='acknowledged'?'<span>Seen</span>':''}${r.corrected?'<span>Corrected by you</span>':''}${r.correction_conflict?'<span class="needs-review">Source differs from your correction</span>':''}${r.changed_since_handled?'<span>Changed since you handled it</span>':''}</div>${r.changed_since_handled&&r.change_reason?`<p class="small-note">${esc(r.change_reason)}</p>`:''}${r.summary?`<p>${esc(r.summary)}</p>`:''}${Object.keys(r.fields||{}).length?`<dl class="result-fields">${Object.entries(r.fields).map(([k,v])=>`<div><dt>${esc(human(k))}</dt><dd>${esc(typeof v==='object'?JSON.stringify(v):v)}</dd></div>`).join('')}</dl>`:''}${d.mode==='series'?`<p class="small-note">Saved ${esc(stamp(r.first_seen))}</p>`:''}${r.expires_at?`<p class="small-note">Deadline: ${esc(new Date(r.expires_at).toLocaleString(undefined,{year:'numeric',month:'short',day:'numeric',hour:'numeric',minute:'2-digit',timeZoneName:'short'}))}</p>`:''}${provenance(r)}<details data-result-details="${esc(r.id)}"><summary>Sources & details</summary><div class="result-full"></div></details><div class="result-actions">${attachItem(d.id,r)}<button class="text-button" data-result-action="${r.hidden?'restore':'dismiss'}">${r.hidden?'Show again':'Dismiss'}</button><button class="text-button" data-result-action="acknowledge">Mark seen</button><button class="text-button" data-result-correct>Correct</button><button class="text-button" data-result-snooze>Snooze until tomorrow</button>${r.corrected?'<button class="text-button" data-result-action="clear-correction">Remove correction</button>':''}</div></article>`).join('')||'<p class="small-note">No results in this view.</p>'}</div><div class="collection-pagination" ${shape==='list'?'':'hidden'}><span class="small-note">${d.total?offset+1:0}–${Math.min(offset+d.items.length,d.total)} of ${d.total}</span>${offset?'<button class="text-button" data-collection-page="previous">Previous</button>':''}${offset+d.items.length<d.total?'<button class="text-button" data-collection-page="next">Next</button>':''}</div><details class="collection-history"><summary>Check history</summary><div class="collection-history-content">${d.history_count?'Open to read recent checks.':'No checks recorded.'}</div></details><p class="small-note collection-search-scope">${esc(d.search_scope)}</p>`,'context');
    findingBack={id:d.id,name:d.name};
    if(collectionUpdated(id))attempt(async()=>{state.inbox=await api('/api/notifications',{business:state.business,action:'read',collection_id:id});renderNotifications();if($('#file-list'))renderFiles();});window.auraViews.running($('#collection-running'),{collection:id},d);
    const history=$('#detail-content .collection-history');history.addEventListener('toggle',()=>{if(!history.open||history.dataset.loaded||!d.history_count)return;history.dataset.loaded='true';attempt(async()=>{try{const response=await api(url('/api/collections',{id,limit:1,history:1}));if(key!==scope()||!history.isConnected)return;history.querySelector('.collection-history-content').innerHTML=response.history.map(c=>`<div>${checked(c)}<p class="small-note">${c.change_count} material ${c.change_count===1?'change':'changes'} reported</p>${c.changes?.length?`<ul class="small-note">${c.changes.map(change=>`<li><strong>${esc(change.title)}</strong>: ${esc(change.reason)}</li>`).join('')}</ul>`:''}${c.change_count>c.changes.length?`<p class="small-note">Showing ${c.changes.length} of ${c.change_count} changes.</p>`:''}</div>`).join('');}catch(error){delete history.dataset.loaded;throw error;}});});
    if(d.asset_id)setDetailTitleActions(fileFavoriteButton('asset/'+d.asset_id,d.name)+archiveControl('collection',d.asset_id));
    $('#collection-search').oninput=e=>{clearTimeout(timer);const value=e.target.value,panel=state.fileDetailTicket;timer=setTimeout(()=>{if(panel===state.fileDetailTicket&&$('#detail').open)attempt(()=>openCollection(id,view,value));},180);};
    if(focused){$('#collection-search').focus();$('#collection-search').setSelectionRange(position??q.length,position??q.length);}
    $('#collection-view').onchange=e=>attempt(()=>openCollection(id,e.target.value,q));
    const shapeChoice=$('#collection-shape');if(shapeChoice)shapeChoice.onchange=e=>{window.auraViews.choice(id,e.target.value);attempt(()=>openCollection(id,view,q));};
    if(shape!=='list')attempt(()=>window.auraViews.show($('#collection-visual'),d,shape,view,q,title=>{window.auraViews.choice(id,'list');attempt(()=>openCollection(id,view,title));},()=>openCollection(id,view,q)));
    $('#detail-content').querySelectorAll('[data-result-details]').forEach(el=>el.addEventListener('toggle',()=>{if(!el.open||el.dataset.loaded)return;el.dataset.loaded='true';attempt(async()=>{
      const response=await api(url('/api/collections',{id,item:el.dataset.resultDetails}));if(key!==scope()||!el.isConnected)return;const r=response.item;
      el.querySelector('.result-full').innerHTML=resultDetails(r);
    });}));
  }
  function resultDetails(r){return `${r.change_reason?`<p><strong>What changed</strong> · ${esc(r.change_reason)}</p>`:''}${r.source_refs?.length?'<dl>'+r.source_refs.map(s=>`<div><dt>${/^https?:\/\//i.test(s.reference)?`<a href="${esc(s.reference)}" target="_blank" rel="noopener noreferrer">${esc(s.reference)}</a>`:esc(s.reference)}</dt><dd>${s.published_at?'Published: '+esc(stamp(s.published_at))+' · ':''}${s.data_as_of?'Data as of: '+esc(stamp(s.data_as_of))+' · ':''}${s.last_checked_at?'Checked: '+esc(stamp(s.last_checked_at)):''}</dd></div>`).join('')+'</dl>':'<p class="small-note">No source reference supplied.</p>'}${r.summary?`<p>${esc(r.summary)}</p>`:''}${r.correction_note?`<p>${esc(r.correction_note)}</p>`:''}<pre>${esc(JSON.stringify(r.fields||{},null,2))}</pre>${r.corrected?`<details><summary>As reported by the source</summary><pre>${esc(JSON.stringify(r.reported,null,2))}</pre></details>`:''}`;}
  async function previewShare(id,item,q){
    const key=scope(),valid=panelRequest();
    const preview=await api(url('/api/collections',{id,item,q,preview:'share'}));
    if(key!==scope()||!valid())return;
    details('Copy for sharing',`<label class="form-grid">Text to copy<textarea id="share-result-text" rows="12"></textarea></label><details><summary>Add a public setup link</summary><label class="check-label"><input type="checkbox" id="share-report-method"><span>Weekly client reporting · example and reusable method</span></label></details><div class="inline-actions"><button type="button" class="primary" id="copy-result-text">Copy text</button><button type="button" class="text-button" id="share-result-back">Back to results</button></div><p class="small-note" role="status" id="result-copy-status"></p>`);
    const field=$('#share-result-text'),toggle=$('#share-report-method'),status=$('#result-copy-status');
    const footer='\n\nTry the weekly client reporting setup: '+reportingExampleUrl;
    field.value=preview.text;
    toggle.onchange=()=>{field.value=field.value.replace(footer,'')+(toggle.checked?footer:'');status.textContent='';};
    field.oninput=()=>{toggle.checked=field.value.includes(footer);status.textContent='';};
    $('#share-result-back').onclick=()=>attempt(()=>item?openItem(id,item):openCollection(id,'saved',q));
    $('#copy-result-text').onclick=async()=>{
      try{await navigator.clipboard.writeText(field.value);status.textContent='Copied.';}
      catch{field.focus();field.select();status.textContent='Text selected. Use your usual Copy command.';}
    };
  }
  function attachItem(collection,item){
    return `<button type="button" class="text-button" data-attach-item="${esc(item.id)}" data-parent-collection="${esc(collection)}" data-label="${esc(item.title)}">Add to chat</button><button type="button" class="text-button" data-share-results="${esc(collection)}" data-share-item="${esc(item.id)}">Copy for sharing</button>`;
  }
  async function openItem(id,item){
    const key=scope(),valid=panelRequest();
    const response=await api(url('/api/collections',{id,item}));
    if(key!==scope()||!valid())return;
    const r=response.item;
    details(r.title,`${r.expires_at?`<p>Deadline: ${esc(new Date(r.expires_at).toLocaleString())}</p>`:''}${resultDetails(r)}${attachItem(id,r)}<button type="button" class="text-button" id="deadline-collection">Open collection</button>`,'context');
    $('#deadline-collection').onclick=()=>attempt(()=>openCollection(id));
  }
  async function feedback(choice,item,extra={}){
    const d=current;if(!d||d.key!==scope())return;
    await api('/api/collections',{business:state.business,id:d.id,action:'feedback',choice,item_id:item,revision:d.revision,...extra});
    if(d.key===scope()&&selection?.id===d.id&&$('#detail').open&&($('#collection-view')||$('#correct-result'))){const next=selection;await openCollection(next.id,next.view,next.q,next.offset);}
  }
  function newCollection(projectId=''){
    const key=scope(),collectionKey='collection-'+crypto.randomUUID();details('Save useful results',`<form id="new-collection" class="form-grid"><label>Name<input name="name" maxlength="160" required placeholder="Grant shortlist"></label><label>Keep as<select name="mode"><option value="collection">A maintained collection</option><option value="series">Dated reports</option></select></label><label>What should this help you do?<textarea name="purpose" rows="3" maxlength="2000" placeholder="Find relevant grants and keep their deadlines current"></textarea></label>${copiesField('quotes')}<div class="inline-actions"><button class="primary">Create</button><button type="button" class="text-button" data-close="detail">Cancel</button></div></form>`);
    $('#new-collection').onsubmit=e=>{e.preventDefault();const form=e.target;if(form.dataset.saving)return;form.dataset.saving='true';form.querySelector('button.primary').disabled=true;attempt(async()=>{try{const values=Object.fromEntries(new FormData(form));const result=await api('/api/collections',{business:state.business,action:'create',...values,key:collectionKey,project_refs:projectId?[projectId]:[]});if(key!==scope())return;await refreshSavedWork(key);if(key!==scope())return;parentProject=projectId;await openCollection(result.id);}finally{delete form.dataset.saving;if(form.isConnected)form.querySelector('button.primary').disabled=false;}});};
  }
  async function assignTask(task,host){
    const key=scope();const [data,binding]=await Promise.all([api(url('/api/collections')),api(url('/api/project-binding',{kind:'task',id:task.id}))]);if(key!==scope()||!host.isConnected)return;
    const collection=data.items.find(c=>c.id===binding.collection_id&&!c.unavailable);
    const link=$('#detail-content [data-task-collection]');
    if(link&&collection)link.innerHTML=`<button type="button" class="secondary" data-collection="${esc(collection.id)}">Open results collection · ${esc(collection.name)}</button>`;
    host.innerHTML=`<label>Save results to<select id="task-results-destination"><option value="">Native task results</option>${data.items.filter(c=>!c.unavailable).map(c=>`<option value="${esc(c.id)}" ${c.id===binding.collection_id?'selected':''}>${esc(c.name)}</option>`).join('')}</select></label><p class="small-note">A collection keeps useful entries current. Dated reports remain separate installments.</p><button type="button" class="text-button" id="apply-task-destination">Apply to scheduled task</button>`;
    $('#apply-task-destination').onclick=()=>attempt(()=>scheduleOperation({id:task.id,app:task.owner,action:'edit',collection_id:$('#task-results-destination').value}));
  }
  async function openForFile(ref){
    const row=state.data?.records?.find(r=>r.type==='Asset'&&(ref.split('/')[1]===r.ref||r.data.location_reference===ref)),id=row?.data.extensions?.businessos?.collection?.id;
    if(!id)return false;parentProject='';await openCollection(id);setDetailTitleActions(fileFavoriteButton(ref,row.title)+archiveControl('collection',row.ref));return true;
  }
  document.addEventListener('click',event=>{
    const b=event.target.closest('[data-finding],[data-finding-evidence],[data-open-project],[data-collection],[data-create-collection],[data-result-action],[data-result-correct],[data-result-snooze],[data-collection-page],[data-edit-collection],[data-collection-add],[data-attach-item],[data-share-results]');if(!b)return;
    if(b.dataset.shareResults){attempt(()=>previewShare(b.dataset.shareResults,b.dataset.shareItem||'',b.dataset.shareItem?'':current?.q||''));return;}
    if(b.dataset.attachItem){
      if(window.auraCompose?.add({kind:'collection',id:b.dataset.parentCollection,variant:b.dataset.attachItem,label:b.dataset.label})){returnToChat();notice('Item added to your draft.');}
      return;
    }
    if(b.dataset.finding){attempt(()=>finding(b.dataset.finding));return;}
    if(b.dataset.findingEvidence){attempt(()=>recordDetails(b.dataset.findingEvidence));return;}
    if(b.dataset.openProject)attempt(()=>project(b.dataset.openProject));
    if(b.hasAttribute('data-create-collection'))newCollection(b.dataset.createCollection||'');
    if(b.dataset.collection){parentProject=b.dataset.collectionProject||'';attempt(()=>openCollection(b.dataset.collection));}
    const item=b.closest('[data-result-id]')?.dataset.resultId;
    if(b.dataset.resultAction)attempt(()=>feedback(b.dataset.resultAction,item));
    if(b.hasAttribute('data-result-correct')){
      const d=current,key=scope(),valid=panelRequest();attempt(async()=>{const r=(await api(url('/api/collections',{id:d.id,item}))).item;if(key!==scope()||!valid())return;
        details('Correct saved result',`<form id="correct-result" class="form-grid"><label>Title<input name="title" value="${esc(r.title)}" required maxlength="500"></label><label>Summary<textarea name="summary" rows="3">${esc(r.summary||'')}</textarea></label>${Object.entries(r.fields||{}).filter(([,v])=>v===null||typeof v!=='object').map(([k,v],i)=>`<label>${esc(human(k))}<input name="field-${i}" value="${esc(v??'')}" ${typeof v==='number'?'type="number" step="any"':''}></label>`).join('')}<label>Note (optional)<input name="note" maxlength="2000" placeholder="What supports this correction?"></label><div class="inline-actions"><button class="primary">Save correction</button><button type="button" class="text-button" id="cancel-result-correction">Cancel</button></div></form>`);
        $('#cancel-result-correction').onclick=()=>attempt(()=>openCollection(d.id,d.view,d.q,d.offset));
        $('#correct-result').onsubmit=e=>{e.preventDefault();attempt(async()=>{const v=Object.fromEntries(new FormData(e.target));const fields={};Object.entries(r.fields||{}).filter(([,value])=>value===null||typeof value!=='object').forEach(([k,value],i)=>{const entered=v['field-'+i];if(entered===String(value??''))return;if(typeof value==='number'){fields[k]=Number(entered);if(!Number.isFinite(fields[k]))throw new Error('Enter a valid number for '+human(k)+'.');}else if(typeof value==='boolean'){if(!['true','false'].includes(entered))throw new Error('Use true or false for '+human(k)+'.');fields[k]=entered==='true';}else fields[k]=entered;});const correction={};if(v.title!==r.title)correction.title=v.title;if(v.summary!==(r.summary||''))correction.summary=v.summary;if(Object.keys(fields).length)correction.fields=fields;if(!Object.keys(correction).length)throw new Error('Change a value before saving a correction.');await feedback('correct',item,{correction,note:v.note});});};
      });
    }
    if(b.hasAttribute('data-collection-add')&&current&&window.auraCompose?.add({kind:'collection',id:current.id,label:current.name})){returnToChat();notice('Context added. Tell your AI what you want to do.');}
    if(b.hasAttribute('data-edit-collection')&&current){
      const d=current,key=scope();details('Edit collection',`<form id="edit-collection" class="form-grid"><label>Name<input name="name" value="${esc(d.name)}" maxlength="160" required></label><label>Purpose<textarea name="purpose" rows="3" maxlength="2000">${esc(d.purpose||'')}</textarea></label>${copiesField(d.source_copies)}<div class="inline-actions"><button class="primary">Save</button><button type="button" class="text-button" id="cancel-collection-edit">Cancel</button></div></form>`);
      $('#cancel-collection-edit').onclick=()=>attempt(()=>openCollection(d.id,d.view,d.q,d.offset));
      $('#edit-collection').onsubmit=e=>{e.preventDefault();attempt(async()=>{await api('/api/collections',{business:state.business,id:d.id,action:'configure',revision:d.revision,...Object.fromEntries(new FormData(e.target))});if(key===scope()){await refreshSavedWork(key);if(key===scope())await openCollection(d.id,d.view,d.q,d.offset);}});};
    }
    if(b.hasAttribute('data-result-snooze')){const until=new Date(Date.now()+86400000).toISOString();attempt(()=>feedback('snooze',item,{until}));}
    if(b.dataset.collectionPage&&current)attempt(()=>openCollection(current.id,current.view,current.q,Math.max(0,current.offset+(b.dataset.collectionPage==='next'?30:-30))));
  });
  $('#detail').addEventListener('close',()=>{if(!$('#detail').open){clearTimeout(timer);window.auraViews.release();current=null;selection=null;parentProject='';}});
  document.addEventListener('change',event=>{if(event.target.id==='file-project-filter'){state.fileProject=event.target.value;const create=$('[data-create-collection]');if(create)create.dataset.createCollection=event.target.value;state.fileLimit=100;renderFiles();}});
  return {project,openItem,openCollection,newCollection,assignTask,openForFile,finding};
})();
