/* Native activity and reusable references. Display never controls native execution. */
window.auraInsight=(()=>{
  let chatKey='';
  let pending='',loaded='',loadedAt=0,data=null,mode='',limit=40,owner='',selectedRequest='',paintKey='',memoryKey='';
  const scope=()=>JSON.stringify([state.data?.workspace,state.business,state.chatMeta?.id]);
  function view(){return owner?'full':mode||state.data?.profile?.activity_view||'highlights';}
  function paint(){
    const host=$('#native-activity');if(!host)return;
    const fallback=state.liveJob?.chat_id===state.chatMeta?.id?(state.liveJob.activity||[]).map((r,i)=>({id:'progress-'+i,kind:'commentary',title:r.text,owner:'',text:'',at:r.at})):[];
    const v=view(),rows=(data?.items?.length?data.items:fallback).filter(r=>(!owner||r.owner===owner)&&(v==='full'||r.kind==='plan'||r.kind==='file'||r.kind==='delegation'||['error','failed','errored'].includes(r.status)||r.kind==='commentary'));
    const children=state.liveJob?.chat_id===state.chatMeta?.id?state.liveJob?.subagents:state.chatMeta?.subagents;
    const names=new Map((children||[]).flatMap(c=>[[c.id,c.name],...(c.native_id?[[c.native_id,c.name]]:[])]));
    const shown=v==='highlights'?rows.slice(-6):rows.slice(-limit);
    const signature=JSON.stringify([scope(),v,shown,owner,limit,data?.truncated,data?.expired]);if(signature===paintKey)return;paintKey=signature;
    const opened=new Set([...host.querySelectorAll('details[open]')].map(e=>e.dataset.activityId));
    host.hidden=!state.chatMeta;
    host.innerHTML=`<div class="activity-heading"><span>Activity</span><label><span class="sr-only">Activity detail</span><select id="activity-view"><option value="highlights" ${v==='highlights'?'selected':''}>Highlights</option><option value="full" ${v==='full'?'selected':''}>Full</option><option value="off" ${v==='off'?'selected':''}>Off</option></select></label></div>${v==='off'?'':`${owner?'<button class="text-button" type="button" data-activity-all>← All activity</button>':''}<div class="native-activity-list">${shown.map(r=>`<details data-activity-id="${esc(r.id)}" ${opened.has(r.id)||r.kind==='plan'?'open':''}><summary><span>${r.owner?esc(names.get(r.owner)||'Subagent')+' · ':''}${esc(r.title)}</span>${r.status?`<small>${esc(human(r.status))}</small>`:''}</summary>${r.has_detail?`<pre data-activity-detail="${esc(r.id)}">${esc(r.text||'Open to load details.')}</pre>`:''}${r.truncated?'<p class="small-note">Showing an excerpt. Full output remains in the native app.</p>':''}</details>`).join('')||(state.busy?'<p class="small-note">Waiting for native activity…</p>':'')}</div>${v==='full'&&rows.length>limit?'<button type="button" class="text-button" data-activity-more>Show earlier activity</button>':''}${data?.expired?'<p class="small-note">These activity details are no longer saved in Aura. Earlier history remains in your AI app.</p>':''}${data?.truncated?'<p class="small-note">Showing recent activity. Older details remain in your AI app.</p>':''}`}`;
    host.querySelectorAll('details[data-activity-id]').forEach(el=>el.addEventListener('toggle',()=>{if(el.open)attempt(()=>detail(el));}));
    $('#activity-view').onchange=()=>attempt(async()=>{
      const chosen=$('#activity-view').value,prior=view(),key=scope();owner='';mode=chosen;paint();renderDelegationVisibility();
      try{const profile=await api('/api/profile',{activity_view:chosen});if(key===scope())state.data.profile=profile;}
      catch(error){mode=prior;paint();renderDelegationVisibility();throw error;}
      render();
    });
  }
  async function detail(el){
    const key=scope(),request=loaded.split('|').at(-1),ident=el.dataset.activityId,revision=data?.revision;if(!request||!el.open||el.dataset.loaded===String(revision))return;
    const result=await api('/api/chat/activity?'+new URLSearchParams({business:state.business,chat_id:state.chatMeta.id,request,item:ident}));
    if(key!==scope()||!el.isConnected||data?.revision!==revision||loaded.split('|').at(-1)!==request)return;const pre=el.querySelector('pre');if(pre)pre.textContent=(result.input?'Input\n'+result.input+'\n\n':'')+(result.text||'');el.dataset.loaded=String(revision);
  }
  function renderDelegationVisibility(){window.auraWork?.renderDelegation();if($('#delegated-work')&&view()==='off')$('#delegated-work').hidden=true;}
  function render(){
    const key=scope();if(chatKey!==key){chatKey=key;selectedRequest='';if($('#memory-feedback'))$('#memory-feedback').hidden=true;}
    const request=selectedRequest|| (state.liveJob?.chat_id===state.chatMeta?.id?state.liveJob?.trace_id:state.chatMeta?.trace_id);
    if(!loaded.startsWith(key+'|')){data=null;owner='';limit=40;paintKey='';loaded='';}
    paint();renderDelegationVisibility();
    if(view()==='off'||!request)return;
    const id=key+'|'+request;if(pending===id||loaded===id&&(!state.busy||Date.now()-loadedAt<2000))return;
    pending=id;
    api('/api/chat/activity?'+new URLSearchParams({business:state.business,chat_id:state.chatMeta.id,request,after:loaded===id?String(data?.revision||''):''})).then(result=>{
      if(key!==scope()||pending!==id)return;if(!result.unchanged)data=result;loaded=id;loadedAt=Date.now();paint();
    }).catch(()=>{/* Activity retrieval never interrupts work or approvals. */}).finally(()=>{if(pending===id)pending='';});
  }
  async function memory(){
    const key=scope(),job=state.liveJob;if(!$('#memory-feedback')||!job||job.chat_id!==state.chatMeta?.id||job.status==='working'||Date.now()/1000-job.updated>600)return;
    const id=key+'|'+job.id;if(memoryKey===id)return;memoryKey=id;
    const result=await api('/api/memory-feedback?'+new URLSearchParams({business:state.business,since:job.created}));if(key!==scope())return;
    const host=$('#memory-feedback');host.hidden=!result.items.length;
    host.innerHTML=result.items.map(r=>`<div class="memory-feedback-row" data-memory-id="${esc(r.id)}"><span>Saved to workspace: <strong>${esc(r.label)}</strong></span><div class="inline-actions"><button class="text-button" data-memory-action="keep">Keep</button><button class="text-button" data-memory-edit="${esc(r.object_ref)}">Edit</button><button class="text-button" data-memory-action="undo">Undo</button></div></div>`).join('');
  }
  async function editMemory(ref){
    const key=scope();await refresh(true);if(key!==scope())return;
    const record=state.data.records.find(r=>r.ref===ref);if(!record){notice('This memory is no longer available.',true);return;}
    details('Correct saved memory',`<p><strong>${esc(record.title)}</strong></p><p class="small-note">Your AI will read the current record and apply your correction.</p><form id="memory-correction" class="form-grid"><label>What should change?<textarea name="correction" rows="4" required></textarea></label><div class="inline-actions"><button class="primary">Apply correction</button><button type="button" class="text-button" data-close="detail">Cancel</button></div></form>`);
    $('#memory-correction').onsubmit=e=>{e.preventDefault();attempt(async()=>{
      if(key!==scope())return;const correction=new FormData(e.target).get('correction').trim();if(!correction)return;
      $('#detail').close();await submitRequest(`Correct the saved workspace memory "${record.title}" (${ref}). Read its current record at ${record.path}. Apply this correction through the existing Aura memory helper, preserve unrelated fields, and verify the save.\n\nUser correction:\n${correction}`);
    });};
  }
  function references(host,initial=[]){
    if(!host)return;
    let selected=initial.map(r=>({...r})),ticket=0,timer,edits=0;const key=JSON.stringify([state.data?.workspace,state.business]);
    host.innerHTML='<details class="saved-context"><summary>Saved context <span data-reference-count></span></summary><p class="small-note">Reuse files, memory, goals, or guidance when relevant.</p><div data-reference-selected></div><label>Find context<input type="search" data-reference-search placeholder="Search saved context…"></label><div data-reference-found></div></details>';
    const alive=()=>host.isConnected&&key===JSON.stringify([state.data?.workspace,state.business]);
    const paint=()=>{host.querySelector('[data-reference-count]').textContent=selected.length?`(${selected.length})`:'';host.querySelector('[data-reference-selected]').innerHTML=selected.map((r,i)=>`<div class="reference-item"><span>${esc(r.label||r.id)}</span><button type="button" class="text-button" data-reference-remove="${i}" aria-label="Remove ${esc(r.label||r.id)}">×</button></div>`).join('');};paint();
    host._references=()=>selected.map(r=>Object.fromEntries(Object.entries(r).filter(([k])=>['kind','id','variant','request_id'].includes(k))));
    host.onclick=e=>{const b=e.target.closest('[data-reference-remove]');if(b){edits++;selected.splice(Number(b.dataset.referenceRemove),1);paint();}};
    const input=host.querySelector('[data-reference-search]');
    input.oninput=()=>{clearTimeout(timer);const request=++ticket;timer=setTimeout(()=>attempt(async()=>{
      const result=await api('/api/context?'+new URLSearchParams({business:state.business,q:input.value,limit:12}));if(!alive()||request!==ticket)return;
      const list=host.querySelector('[data-reference-found]'),items=result.items.filter(r=>r.kind!=='assistant');
      list.innerHTML=items.map((r,i)=>`<button type="button" class="row" data-reference-pick="${i}"><span>${esc(r.label)}<small class="row-meta">${esc(human(r.kind))}${r.app?' · '+esc(r.app):''}</small></span></button>`).join('')||'<p class="small-note">No matching context.</p>';
      list.onclick=e=>{const button=e.target.closest('[data-reference-pick]');if(!button)return;const r=items[Number(button.dataset.referencePick)];if(selected.length>=12){notice('Choose up to 12 references.',true);return;}if(!selected.some(s=>JSON.stringify([s.kind,s.id,s.variant,s.request_id])===JSON.stringify([r.kind,r.id,r.variant,r.request_id])))selected.push(r);edits++;paint();input.value='';list.innerHTML='';};
    }),180);};
    if(selected.length)api('/api/context/resolve',{business:state.business,references:host._references()}).then(r=>{if(alive()&&!edits){selected=r.references;paint();}}).catch(()=>{});
  }
  document.addEventListener('click',e=>{
    const b=e.target.closest('[data-activity-more],[data-activity-all],[data-child-activity],[data-memory-action],[data-memory-edit],[data-request-activity]');if(!b)return;
    if(b.dataset.requestActivity){selectedRequest=b.dataset.requestActivity;loaded='';render();$('#native-activity').scrollIntoView({block:'nearest'});}
    if(b.hasAttribute('data-activity-more')){limit+=40;paint();}
    if(b.hasAttribute('data-activity-all')){owner='';paint();}
    if(b.dataset.childActivity){owner=b.dataset.childActivity;paint();$('#native-activity').scrollIntoView({block:'nearest'});}
    if(b.dataset.memoryEdit)attempt(()=>editMemory(b.dataset.memoryEdit));
    if(b.dataset.memoryAction)attempt(async()=>{b.disabled=true;const row=b.closest('[data-memory-id]');try{await api('/api/memory-feedback',{business:state.business,id:row.dataset.memoryId,action:b.dataset.memoryAction});row.remove();if(!$('#memory-feedback').children.length)$('#memory-feedback').hidden=true;if(b.dataset.memoryAction==='undo')await refresh(true);}finally{if(b.isConnected)b.disabled=false;}});
  });
  return {render,memory,references,view};
})();

queueMicrotask(()=>{window.auraInsight.render();window.auraInsight.memory().catch(()=>{});});
