/* Views over existing native work and small saved assistant profiles. */
'use strict';
window.auraWork = (() => {
  let cache=null, scope='', delegationKey='', delegationChat='', delegationLimit=20;
  const currentScope=()=>JSON.stringify([state.data?.workspace,state.business]);
  const endpoint=()=>'/api/assistants?business='+encodeURIComponent(state.business);
  async function load(){const key=currentScope(),result=await api(endpoint());if(key!==currentScope())return null;cache=result;scope=key;return result;}
  const profile=id=>scope===currentScope()?cache?.items.find(p=>p.id===id):null;
  const taskOwner=(id)=>scope===currentScope()?cache?.items.find(p=>(p.task_ids||[]).includes(id)):null;
  const chatRows=(items,limit=20)=>items.length?items.slice(0,limit).map(c=>`<button type="button" class="row" data-chat="${esc(c.id)}"><span class="row-text"><span class="row-title">${esc(c.title)}</span><span class="row-meta">${esc(appName(c.agent))} · ${esc(c.status==='working'?((cache?.running||[]).includes(c.id)?'Working':'Check chat'):chatDate(c.updated))}</span></span></button>`).join(''):empty('No chats yet.');
  async function renderAssistants(host){
    host.innerHTML='<p role="status">Loading assistants…</p>';
    const data=await load();if(!data||!host.isConnected||state.view!=='assistants')return;
    host.innerHTML=`<div class="assistant-search-toolbar"><input type="search" class="search" id="assistant-search" aria-label="Find an assistant" placeholder="Find an assistant…"><button type="button" class="primary" data-assistant-new>Create assistant</button></div><div id="assistant-list" class="assistant-list"></div>`;
    const renderList=()=>{
      const query=$('#assistant-search').value.trim().toLowerCase();
      const items=data.items.filter(p=>(p.name+' '+(p.instructions||'')).toLowerCase().includes(query));
      $('#assistant-list').innerHTML=items.map(p=>{
        const chats=data.chats.filter(c=>c.assistant_id===p.id),active=chats.filter(c=>(data.running||[]).includes(c.id)).length;
        return `<article class="card assistant-card"><div class="section-head"><h3>${esc(p.name)}</h3><button type="button" class="secondary" data-assistant-open="${esc(p.id)}">Open assistant</button></div><p>${esc(p.instructions||'Add instructions to give this assistant a purpose.')}</p><p class="row-meta">${chats.length} chats · ${(p.task_ids||[]).length} recurring tasks${active?' · '+active+' working':''}</p></article>`;
      }).join('')||empty(query?'No matching assistants.':'Create an assistant with a name and the instructions you want to reuse.');
    };
    $('#assistant-search').oninput=renderList;renderList();
  }
  async function overview(id){
    const key=currentScope(),view=state.view;details('Assistant','<p role="status">Loading assistant…</p>');
    const ticket=state.fileDetailTicket,current=()=>key===currentScope()&&view===state.view&&ticket===state.fileDetailTicket&&$('#detail').open;
    const data=await load(),p=profile(id);if(!data||!current())return;if(!p){notice('This assistant was removed. Its chats, tasks, and results are still available.');return;}
    const schedules=await api('/api/schedules');if(!current())return;
    const tasks=schedules.items.filter(t=>(p.task_ids||[]).includes(t.id));state.schedules=schedules;
    const missing=(p.task_ids||[]).length-tasks.length;
    details(p.name,`<div class="assistant-toolbar"><button type="button" class="primary" data-assistant-chat="${esc(id)}">New chat with ${esc(p.name)}</button><button type="button" class="secondary" data-assistant-edit="${esc(id)}">Edit assistant</button></div><p class="assistant-instructions">${esc(p.instructions||'No saved instructions.')}</p><p class="small-note">${esc(p.app?appName(p.app):'Current AI connection')}${p.model?' · '+esc(p.model):''}${p.child_model?' · Subagents: '+esc(p.child_model):''}</p><section><h3>Recurring tasks</h3>${tasks.map(t=>scheduleRow(t)).join('')||empty((p.task_ids||[]).length?'Linked tasks are not currently available.':'No recurring tasks assigned.')}<div class="inline-actions assistant-task-actions"><button type="button" class="secondary" data-assistant-existing-task="${esc(id)}">Assign existing task</button><button type="button" class="text-button" data-assistant-task="${esc(id)}">Create recurring task</button><button type="button" class="text-button" data-view="tools">All recurring tasks</button></div>${missing?'<p class="small-note">Some linked tasks are unavailable. Refresh them in their owning app.</p>':''}${schedules.notes?.length?`<p class="error" role="status">${schedules.notes.map(esc).join(' ')}</p>`:''}</section><section><h3>Conversations</h3><input type="search" id="assistant-chat-search" class="search" aria-label="Search this assistant’s chat titles" placeholder="Find a chat by title…"><div id="assistant-chat-list"></div></section>`);
    const chats=data.chats.filter(c=>c.assistant_id===id),host=$('#assistant-chat-list'),search=$('#assistant-chat-search');let limit=20;
    const renderChats=()=>{
      if(key!==currentScope()||!host.isConnected)return;
      const query=search.value.trim().toLowerCase(),matches=chats.filter(c=>(c.title||'').toLowerCase().includes(query));
      host.innerHTML=(matches.length?chatRows(matches,limit):empty(query?'No matching chats.':'No chats yet.'))+
        (matches.length?`<p class="small-note">${Math.min(limit,matches.length)} of ${matches.length} chats</p>`:'')+
        (matches.length>limit?'<button type="button" class="text-button" data-assistant-more-chats>Show more chats</button>':'');
    };
    search.oninput=()=>{limit=20;renderChats();};host.onclick=event=>{if(event.target.closest('[data-assistant-more-chats]')){limit+=20;renderChats();}};renderChats();
  }
  async function edit(id=''){
    if(!await load())return;const p=id?profile(id):{};if(!p)return;
    const key=currentScope(),apps=state.data.connection.choices.filter(c=>c.available||c.id===p.app);
    details(id?'Edit assistant':'Create assistant',`<form id="assistant-form" class="form-grid"><input name="id" type="hidden" value="${esc(id)}"><label>Name<input name="name" maxlength="80" required value="${esc(p.name||'')}" placeholder="Jeff"></label><label>Instructions<textarea name="instructions" maxlength="20000" rows="4" placeholder="What should this assistant help with?">${esc(p.instructions||'')}</textarea></label><details ${p.app||p.model||p.child_model?'open':''}><summary>AI preferences</summary><div class="form-grid assistant-preferences"><label>AI app<select name="app" id="assistant-app"><option value="">Current connection</option>${apps.map(a=>`<option value="${esc(a.id)}" ${a.id===p.app?'selected':''}>${esc(a.name)}</option>`).join('')}</select></label><input type="hidden" name="model" id="assistant-model" value="${esc(p.model||'')}"><input type="hidden" name="effort" id="assistant-effort" value="${esc(p.effort||'')}"><input type="hidden" name="child_model" id="assistant-child-model" value="${esc(p.child_model||'')}"><div><label for="assistant-pick-model">Preferred model & effort</label><div class="inline-actions"><button type="button" class="secondary" id="assistant-pick-model" aria-haspopup="dialog"></button><button type="button" class="text-button" id="assistant-reset-model">Use app default</button></div></div><div><label for="assistant-pick-child">Subagent model</label><div class="inline-actions"><button type="button" class="secondary" id="assistant-pick-child" aria-haspopup="dialog"></button><button type="button" class="text-button" id="assistant-reset-child">Inherit native settings</button></div></div><p class="small-note">Subagent preferences use the native app’s delegation capabilities.</p></div></details><div class="inline-actions"><button class="primary">Save assistant</button>${id?`<button type="button" class="text-button" data-assistant-open="${esc(id)}">Cancel</button><button type="button" class="text-button danger" data-assistant-remove="${esc(id)}">Remove assistant</button>`:'<button type="button" class="text-button" data-assistant-cancel>Cancel</button>'}</div><p id="assistant-save-status" role="status"></p></form>`);
    const form=$('#assistant-form'),app=$('#assistant-app'),model=$('#assistant-model'),effort=$('#assistant-effort'),child=$('#assistant-child-model');
    let kind=app.value||state.data.connection.selected;
    const paint=()=>{
      $('#assistant-pick-model').textContent=model.value+(effort.value?' · '+human(effort.value):'')||'App default';
      $('#assistant-pick-child').textContent=child.value||'Inherit native settings';
      $('#assistant-pick-model').disabled=$('#assistant-pick-child').disabled=!nativeApps.includes(kind);
      $('#assistant-reset-model').hidden=!model.value&&!effort.value;$('#assistant-reset-child').hidden=!child.value;
    };
    const pick=modelOnly=>{const chosenKind=kind;return attempt(()=>openChatModels({title:modelOnly?'Subagent model':'Assistant model & effort',modelOnly,
      connection:{kind:chosenKind,model:modelOnly?child.value:model.value,effort:modelOnly?'':effort.value},
      current:()=>key===currentScope()&&form.isConnected&&$('#detail').open&&chosenKind===(app.value||state.data.connection.selected),
      onSelect:choice=>{app.value=choice.kind;kind=choice.kind;if(modelOnly)child.value=choice.model;else{model.value=choice.model;effort.value=choice.effort;}paint();}}));};
    $('#assistant-pick-model').onclick=()=>pick(false);$('#assistant-pick-child').onclick=()=>pick(true);
    $('#assistant-reset-model').onclick=()=>{model.value=effort.value='';paint();};$('#assistant-reset-child').onclick=()=>{child.value='';paint();};
    app.onchange=()=>{const next=app.value||state.data.connection.selected;if(next!==kind){model.value=effort.value=child.value='';kind=next;}paint();};paint();
  }
  async function chooseTask(id){
    const key=currentScope();details('Assign a recurring task','<p role="status">Finding recurring tasks…</p>');
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    const current=()=>key===currentScope()&&ticket===state.fileDetailTicket&&host.isConnected&&$('#detail').open;
    try{
      const [data,schedules]=await Promise.all([load(),api('/api/schedules?scope=workspace')]);if(!current()||!data)return;
      const p=profile(id);if(!p)throw new Error('This assistant is no longer available.');
      state.schedules=schedules;
      host.innerHTML=`<p>Assign to <strong>${esc(p.name)}</strong>. Tasks keep their current schedule and instructions.</p><input id="assistant-task-search" class="search" type="search" aria-label="Find an existing recurring task" placeholder="Find a recurring task…"><div id="assistant-task-choices"></div><p id="assistant-task-status" role="status"></p><div class="inline-actions assistant-task-actions"><button type="button" class="text-button" data-assistant-open="${esc(id)}">Back to assistant</button><button type="button" class="secondary" data-assistant-task="${esc(id)}">Create recurring task</button></div>${schedules.notes?.length?`<p class="small-note">${schedules.notes.map(esc).join(' ')}</p>`:''}`;
      const available=schedules.items.filter(t=>!(p.task_ids||[]).includes(t.id));let limit=20,saving=false;
      const paint=()=>{
        if(!current())return;const q=$('#assistant-task-search').value.trim().toLowerCase();
        const matches=available.filter(t=>[t.name,t.description,appName(t.owner),taskOwner(t.id)?.name].join(' ').toLowerCase().includes(q));
        $('#assistant-task-choices').innerHTML=matches.slice(0,limit).map(t=>{
          const owner=taskOwner(t.id);
          return `<article class="assistant-task-choice"><div><strong>${esc(t.name)}</strong><p class="row-meta">${esc(appName(t.owner))}${owner?' · Assigned to '+esc(owner.name):''}</p></div><button type="button" class="secondary" data-assign-existing-task="${esc(t.id)}">${owner?'Move here':'Assign'}</button></article>`;
        }).join('')||empty(q?'No matching recurring tasks.':available.length?'No matching recurring tasks.':schedules.items.length?'All available tasks are already assigned to this assistant.':'No recurring tasks found.');
        if(matches.length>limit)$('#assistant-task-choices').insertAdjacentHTML('beforeend','<button type="button" class="text-button" data-more-existing-tasks>Show more tasks</button>');
      };
      $('#assistant-task-search').oninput=()=>{limit=20;paint();};
      $('#assistant-task-choices').onclick=event=>attempt(async()=>{
        const button=event.target.closest('button');if(!button||!current()||saving)return;
        if(button.hasAttribute('data-more-existing-tasks')){limit+=20;paint();return;}
        const task=available.find(t=>t.id===button.dataset.assignExistingTask);if(!task)return;
        saving=true;button.disabled=true;$('#assistant-task-status').textContent='Assigning task…';
        try{
          const result=await api('/api/assistants',{business:state.business,action:'assign_task',task_id:task.id,id});
          if(!current())return;cache=result;scope=key;await overview(id);
        }catch(error){if(current())$('#assistant-task-status').textContent=humanError(error);}
        finally{saving=false;if(button.isConnected)button.disabled=false;}
      });paint();
    }catch(error){if(current()){host.innerHTML=`<p class="error" role="status">${esc(humanError(error))}</p><button type="button" class="secondary" id="assistant-task-retry">Try again</button>`;$('#assistant-task-retry').onclick=()=>attempt(()=>chooseTask(id));}}
  }
  async function assignTask(task,host){
    const data=await load();if(!data||!host.isConnected)return;
    const owner=taskOwner(task.id);
    host.hidden=!data.items.length&&!owner;if(host.hidden){host.innerHTML='';return;}
    host.innerHTML=`<label>Saved assistant<select id="task-assistant"><option value="">No assistant</option>${data.items.map(p=>`<option value="${esc(p.id)}" ${p.id===owner?.id?'selected':''}>${esc(p.name)}</option>`).join('')}</select></label><p class="small-note">Groups this task and its results. The task keeps its saved instructions.</p><p id="task-assistant-status" role="status"></p>`;
    let saved=owner?.id||'';
    $('#task-assistant').onchange=()=>attempt(async()=>{const choice=$('#task-assistant'),key=currentScope();choice.disabled=true;try{const result=await api('/api/assistants',{business:state.business,action:'assign_task',task_id:task.id,id:choice.value});if(key!==currentScope()||!choice.isConnected)return;cache=result;scope=key;saved=choice.value;$('#task-assistant-status').textContent='Assignment saved.';}catch(error){if(key===currentScope()&&choice.isConnected){choice.value=saved;$('#task-assistant-status').textContent=humanError(error);}}finally{if(choice.isConnected)choice.disabled=false;}});
  }
  async function history(task,host){
    const key=currentScope();host.textContent='Loading results…';
    try{const result=await api('/api/schedules/history?id='+encodeURIComponent(task.id));if(key!==currentScope()||!host.isConnected)return;
      host.innerHTML=`<h3>Results</h3>${result.items.length?`<div class="task-results">${result.items.map((r,i)=>`<button type="button" class="row" data-task-run="${esc(r.id)}" data-task-source="${esc(task.id)}"><span class="row-text"><span class="row-title">${i===0?'Latest · ':''}${esc(r.name)}</span><span class="row-meta">${esc(r.status)}${r.at?' · '+esc(chatDate(Number(r.at)>1e12?Number(r.at)/1000:Number(r.at))):''}</span></span></button>`).join('')}</div>`:'<p class="muted">No saved results available here yet.</p>'}${result.note?`<p class="small-note">${esc(result.note)}</p>`:''}${result.items.length===result.limit?'<p class="small-note">Showing the 20 most recent results.</p>':''}`;
    }catch(error){if(key!==currentScope()||!host.isConnected)return;host.innerHTML=`<h3>Results</h3><p class="error" role="status">${esc(humanError(error))}</p><button type="button" class="secondary">Try again</button>`;host.querySelector('button').onclick=()=>history(task,host);}
  }
  async function openResult(taskId,runId){
    const key=currentScope(),r=await api('/api/schedules/result?id='+encodeURIComponent(taskId)+(runId?'&run_id='+encodeURIComponent(runId):''));if(key!==currentScope())return;
    details(r.name,`<div class="inline-actions"><button type="button" class="text-button" data-schedule="${esc(taskId)}">← Back to task</button>${r.native_id?`<button type="button" class="secondary" data-result-native="${esc(r.native_id)}" data-result-owner="${esc(r.owner)}">Open conversation</button>`:''}</div><p class="small-note">${esc(r.file)}</p><div class="task-result-body">${chatMarkdown(r.text)}</div>${r.note?`<p class="small-note">${esc(r.note)}</p>`:''}`);
  }
  function renderDelegation(){
    const host=$('#delegated-work');if(!host)return;
    const rows=(state.liveJob&&state.liveJob.chat_id===state.chatMeta?.id?state.liveJob.subagents:state.chatMeta?.subagents)||[];
    const indexed=new Map(rows.map(c=>[c.id,c])),active=new Set(rows.filter(c=>['working','pending'].includes(c.status)).map(c=>c.id)),pending=[...active];
    while(pending.length){const parent=indexed.get(pending.pop())?.parent_id;if(indexed.has(parent)&&!active.has(parent)){active.add(parent);pending.push(parent);}}
    const children=[...rows.filter(c=>active.has(c.id)),...rows.filter(c=>!active.has(c.id)).reverse()];
    if(delegationChat!==state.chatMeta?.id){delegationChat=state.chatMeta?.id;delegationLimit=20;}
    const key=JSON.stringify([state.chatMeta?.id,children,delegationLimit]);host.hidden=!children.length;
    if(key===delegationKey)return;delegationKey=key;
    const opened=new Set([...host.querySelectorAll('details[open]')].map(d=>d.dataset.child));
    const labels={working:'Working',pending:'Starting',complete:'Completed',error:'Failed',stopped:'Stopped',unconfirmed:'Outcome not reported',partial:'Partial result'};
    const parents=new Set(children.map(c=>c.parent_id)),leaves=children.filter(c=>!parents.has(c.id));
    const done=leaves.filter(c=>c.status==='complete').length;
    const ids=new Set(children.map(c=>c.id));
    host.innerHTML=`<h3>Delegated work <span class="muted">${done} of ${leaves.length} completed</span></h3>${children.slice(0,delegationLimit).map(c=>`<details class="child-agent ${ids.has(c.parent_id)?'child-agent-nested':''}" data-child="${esc(c.id)}" ${opened.has(c.id)?'open':''}><summary><span>${esc(c.name)}${c.model?' · '+esc(c.model):''}</span><span class="child-status ${c.status==='working'?'working':''}">${esc(labels[c.status]||c.status)}</span></summary><div class="child-agent-body">${c.task?`<p class="assistant-instructions">${esc(c.task)}</p>`:''}<p class="small-note">${esc(c.activity||'Native delegation')}${c.started&&c.updated?' · '+Math.max(0,Math.round(c.updated-c.started))+'s observed':''}</p>${c.result?`<div>${chatMarkdown(c.result)}</div>`:'<p class="muted">No result reported yet.</p>'}${c.result_truncated==='true'||c.task_truncated==='true'?'<p class="small-note">Showing a saved excerpt.</p>':''}${state.chatMeta?.agent==='codex'?`<button type="button" class="text-button" data-result-native="${esc(c.id)}" data-result-owner="codex">View native chat</button>`:''}</div></details>`).join('')}${children.length>delegationLimit?'<button type="button" class="text-button" data-delegation-more>Show more agents</button>':''}${children.length-active.size>=50?'<p class="small-note">Showing active agents and recent history. Older work stays in the native chat.</p>':''}`;
  }
  async function startAssistant(id,draft=null){
    if(!await load())return;const p=profile(id);if(!p)return;const key=currentScope();await newShellChat(draft);if(key!==currentScope())return;state.newAssistantId=p.id;state.newAssistantName=p.name;const known=state.data.connection.presets?.[p.app],base=!p.app||p.app===composerConnection().kind?composerConnection():{model:'',effort:''};state.newChatConnection={...base,...(known||{}),...(p.app?{kind:p.app}:{}),...Object.fromEntries(['model','effort'].filter(k=>p[k]).map(k=>[k,p[k]]))};rememberChatDraft();renderComposerConnection();$('#request').focus();
  }
  function composer(){
    const host=$('#assistant-context');if(!host)return;
    const p=state.chatMeta?.assistant_id?profile(state.chatMeta.assistant_id):profile(state.newAssistantId);
    const name=p?.name||state.chatMeta?.assistant_name||state.newAssistantName||'';
    host.hidden=!name;host.textContent=name;host.dataset.assistantOpen=state.chatMeta?.assistant_id||state.newAssistantId||'';
  }
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b)return;
    if(b.hasAttribute('data-assistant-new'))attempt(()=>edit());
    if(b.dataset.assistantOpen)attempt(()=>overview(b.dataset.assistantOpen));
    if(b.dataset.assistantEdit)attempt(()=>edit(b.dataset.assistantEdit));
    if(b.hasAttribute('data-assistant-cancel'))$('#detail').close();
    if(b.dataset.assistantExistingTask)attempt(()=>chooseTask(b.dataset.assistantExistingTask));
    if(b.dataset.assistantTask)attempt(async()=>{const p=profile(b.dataset.assistantTask);if(!p)return;state.scheduleDraft={name:'',description:'',when:'',assistant_id:p.id,app:p.app||state.data.connection.selected,model:p.model||'',effort:p.effort||''};state.scheduleAdding=true;state.view='tools';await render();recordShellRoute();await renderShell();});
    if(b.dataset.assistantChat)attempt(()=>startAssistant(b.dataset.assistantChat));
    if(b.dataset.assistantRemove){const id=b.dataset.assistantRemove;details('Remove assistant?',`<p>Chats, recurring tasks, files, and results will stay available.</p><button type="button" class="secondary" data-assistant-edit="${esc(id)}">Keep assistant</button> <button type="button" class="primary" data-confirm-assistant-remove="${esc(id)}">Remove assistant</button>`);}
    if(b.dataset.confirmAssistantRemove)attempt(async()=>{await api('/api/assistants',{business:state.business,action:'remove',id:b.dataset.confirmAssistantRemove});$('#detail').close();state.view='assistants';await render();});
    if(b.hasAttribute('data-delegation-more')){delegationLimit+=20;renderDelegation();}
    if(b.dataset.taskRun)attempt(()=>openResult(b.dataset.taskSource,b.dataset.taskRun));
    if(b.dataset.resultNative)attempt(()=>addNativeChat(b.dataset.resultOwner,b.dataset.resultNative));
  });
  document.addEventListener('change',event=>{if(event.target.id==='schedule-assistant'){const p=profile(event.target.value);if(!p)return;state.scheduleDraft.assistant_id=p.id;if(p.app){$('#schedule-app').value=p.app;state.scheduleDraft.app=p.app;}state.scheduleDraft.model=p.model||'';state.scheduleDraft.effort=p.effort||'';loadScheduleModels();}});
  document.addEventListener('DOMContentLoaded',()=>{
    if(state.view==='assistants'&&state.data&&!$('#section-content').textContent.trim())attempt(()=>renderAssistants($('#section-content')));
  });
  document.addEventListener('submit',event=>{
    if(!event.target.matches('form#assistant-form'))return;event.preventDefault();const form=event.target,key=currentScope();
    attempt(async()=>{const button=form.querySelector('.primary');button.disabled=true;try{const data=Object.fromEntries(new FormData(form));const result=await api('/api/assistants',{business:state.business,...data});if(key!==currentScope())return;cache=result;scope=key;const p=data.id?profile(data.id):cache.items.at(-1);if(state.view==='assistants')await renderAssistants($('#section-content'));if(p)await overview(p.id);}catch(error){if(form.isConnected)$('#assistant-save-status').textContent=humanError(error);}finally{if(button.isConnected)button.disabled=false;}});
  });
  return {load,startAssistant,renderAssistants,overview,assignTask,chooseTask,history,openResult,renderDelegation,composer};
})();
