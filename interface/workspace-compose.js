/* Context selection, message reuse and goals share the existing composer and APIs. */
'use strict';
window.auraCompose=(()=>{
  let lookupTicket=0,viewTicket=0,inlineItems=[],active=-1,inlineToken=null,timer=null;
  const cache=new Map(),scope=()=>JSON.stringify([state.data?.workspace,state.business]),refs=()=>state.contextReferences||[];
  const goal=()=>state.chatMeta?.goal_id||state.draftGoalId||'';
  const query=extra=>new URLSearchParams({business:state.business,...extra});
  const same=(key,ticket,host)=>key===scope()&&ticket===state.fileDetailTicket&&host.isConnected&&$('#detail').open;
  const compact=r=>({kind:r.kind,id:r.id,label:r.label,...(r.variant?{variant:r.variant}:{}),...(r.request_id?{request_id:r.request_id}:{})});
  const identity=r=>JSON.stringify([r.kind,r.id,r.variant||'',r.request_id||'']);
  const kinds={file:'File',record:'Saved context',goal:'Goal',library:'Library',assistant:'Assistant',result:'Saved result'};
  const shortcuts=[{id:'new',label:'New chat',description:'Keep this draft and open a new chat'},{id:'attach',label:'Attach context',description:'Files, saved work and operating knowledge'},{id:'assistant',label:'Choose assistant',description:'Start a chat with a named assistant'},{id:'goal',label:'Choose goal',description:'Connect this chat to a goal'}];

  async function lookup(q='',kind='',assistant=''){
    const key=scope(),id=JSON.stringify([key,q.toLowerCase(),kind,assistant]),prior=cache.get(id);
    if(prior&&Date.now()-prior.at<5000)return prior.data;
    const data=await api('/api/context?'+query({q,kind,limit:30,...(assistant?{assistant}:{})}));
    if(key!==scope())return null;cache.set(id,{at:Date.now(),data});while(cache.size>30)cache.delete(cache.keys().next().value);return data;
  }
  function paintComposer(){
    const host=$('#composer-contexts');if(!host)return;
    const items=refs(),goalId=goal(),saved=state.data?.records?.find(r=>r.ref===goalId),name=saved?.title||'Selected goal';
    host.hidden=!items.length&&!goalId;
    const markup=(goalId?`<span class="context-chip goal-chip"><button type="button" data-compose-goal="${esc(goalId)}" title="Open goal">Goal: ${esc(name)}</button><button type="button" data-compose-clear-goal aria-label="Remove goal from this chat">×</button></span>`:'')+items.map((r,i)=>`<span class="context-chip"><button type="button" data-compose-inspect="${i}" title="Review selected context">${esc(r.label||r.id)}</button><button type="button" data-compose-remove="${i}" aria-label="Remove ${esc(r.label||r.id)}">×</button></span>`).join('');
    if(host.innerHTML!==markup)host.innerHTML=markup;
    const continuation=$('#chat-continuation');if(continuation)continuation.hidden=!goalId||!state.chatMeta;
    const button=$('#choose-goal');if(button)button.textContent=goalId?'Change goal':'Goal';
  }
  function add(item){
    if(refs().some(r=>identity(r)===identity(item)))return true;
    if(refs().length+(state.selectedFiles||[]).length>=12){notice('Choose up to 12 context references.',true);return false;}
    state.contextReferences=[...refs(),compact(item)];rememberChatDraft();paintComposer();return true;
  }
  function closeMenu(){++lookupTicket;inlineItems=[];active=-1;inlineToken=null;const menu=$('#composer-menu');if(menu){menu.hidden=true;menu.innerHTML='';}$('#request').removeAttribute('aria-activedescendant');$('#request').setAttribute('aria-expanded','false');}
  function token(){
    const input=$('#request'),before=input.value.slice(0,input.selectionStart);
    const slash=before.match(/^\/([a-z-]*)$/i);if(slash)return {type:'slash',q:slash[1],start:0,end:input.selectionStart};
    const mention=before.match(/(?:^|\s)@([^\n@]{0,80})$/);if(!mention)return null;
    if(refs().some(r=>mention[1]===(r.label||r.id)||mention[1].startsWith((r.label||r.id)+' ')))return null;
    return {type:'mention',q:mention[1],start:before.length-mention[1].length-1,end:input.selectionStart};
  }
  function paintMenu(){
    const menu=$('#composer-menu');menu.hidden=!inlineItems.length;$('#request').setAttribute('aria-expanded',String(!menu.hidden));
    menu.innerHTML=inlineItems.map((r,i)=>`<button type="button" role="option" id="composer-option-${i}" aria-selected="${i===active}" data-compose-option="${i}" class="${i===active?'selected':''}"><span>${esc(r.label)}</span><small>${esc(r.kind?kinds[r.kind]:r.description)}${r.kind&&r.description?' · '+esc(r.description):''}</small></button>`).join('');
    if(active>=0)$('#request').setAttribute('aria-activedescendant','composer-option-'+active);
  }
  async function suggest(){
    const selected=token(),key=chatScope(),ticket=++lookupTicket;
    if(!selected){closeMenu();return;}
    const data=selected.type==='slash'?{items:shortcuts.filter(c=>c.id.startsWith(selected.q.toLowerCase()))}:await lookup(selected.q);
    if(ticket!==lookupTicket||key!==chatScope()||JSON.stringify(selected)!==JSON.stringify(token())||!data)return;
    inlineToken=selected;inlineItems=data.items.slice(0,8);active=inlineItems.length?0:-1;paintMenu();
  }
  async function selectInline(index){
    const item=inlineItems[index],selected=inlineToken;if(!item||!selected)return;
    if(selected.type==='mention'&&item.kind!=='assistant'&&!add(item))return;
    const input=$('#request');input.setRangeText(selected.type==='mention'&&item.kind!=='assistant'?'@'+item.label+' ':'',selected.start,selected.end,'end');closeMenu();rememberChatDraft();
    if(selected.type==='slash')await command(item.id);
    else if(item.kind==='assistant')await choose('result',item.id);
    if(!document.querySelector('dialog:modal'))input.focus();
  }
  async function command(id){
    if(id==='new')return newShellChat({text:$('#request').value,files:state.selectedFiles||[],references:refs(),goal_id:goal(),connection:composerConnection()});
    if(id==='attach')return choose();
    if(id==='assistant')return chooseAssistant();
    if(id==='goal')return choose('goal','',true);
  }
  async function choose(kind='',assistant='',linkGoal=false){
    closeMenu();const key=chatScope();details(linkGoal?'Choose goal':assistant?'Choose an assistant’s saved result':'Add context','<p role="status">Finding context…</p>');
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    host.innerHTML=`<label>Find context<input id="compose-find" class="search" type="search" placeholder="Search by name…"></label>${!assistant?`<label>Type<select id="compose-kind"><option value="">All context</option>${Object.entries(kinds).map(([k,v])=>`<option value="${k}" ${k===kind?'selected':''}>${v}</option>`).join('')}</select></label>`:''}<div id="compose-found" role="status">Finding context…</div>`;
    if(linkGoal)$('#compose-kind').disabled=true;
    let request=0;
    const paint=async()=>{
      const local=++request,data=await lookup($('#compose-find').value,assistant?'result':linkGoal?'goal':$('#compose-kind').value,assistant);
      if(key!==chatScope()||!same(scope(),ticket,host)||local!==request||!data)return;
      const list=$('#compose-found');list.innerHTML=data.items.map((r,i)=>`<button type="button" class="row" data-compose-pick="${i}"><span><strong>${esc(r.label)}</strong><small class="row-meta">${esc(kinds[r.kind])}${r.description?' · '+esc(r.description):''}</small></span></button>`).join('')||empty(assistant?'No saved results available for this assistant.':'No matching context.');
      list.onclick=event=>attempt(async()=>{
        const button=event.target.closest('[data-compose-pick]');if(!button||key!==chatScope())return;
        const item=data.items[Number(button.dataset.composePick)];if(!item)return;
        if(item.kind==='assistant'){await choose('result',item.id);return;}
        if(linkGoal)await setGoal(item.id);else if(!add(item))return;
        if(key===chatScope()&&same(scope(),ticket,host)){$('#detail').close();$('#request').focus();}
      });
    };
    if(linkGoal)host.insertAdjacentHTML('beforeend','<button type="button" class="text-button" data-compose-new-goal>Create a goal</button>');
    $('#compose-find').oninput=()=>{clearTimeout(timer);timer=setTimeout(()=>attempt(paint),150);};$('#compose-kind')?.addEventListener('change',()=>attempt(paint));await paint();if(same(scope(),ticket,host))$('#compose-find').focus();
  }
  async function chooseAssistant(){
    const key=chatScope(),data=await window.auraWork.load();if(!data||key!==chatScope())return;
    details('Choose assistant',data.items.map(p=>`<button type="button" class="row" data-compose-assistant="${esc(p.id)}"><strong>${esc(p.name)}</strong></button>`).join('')||empty('Create an assistant from Assistants first.'));
  }
  function actions(row,index){
    return `<div class="message-actions"><button type="button" class="text-button" data-message-copy="${index}">Copy</button>${row.role==='user'?`<button type="button" class="text-button" data-message-reuse="${index}">Reuse prompt</button><button type="button" class="text-button" data-message-new="${index}">Use in new chat</button>`:''}${row.references?.length?`<button type="button" class="text-button" data-message-context="${index}">Context used (${row.references.length})</button>`:''}</div>`;
  }
  async function reuse(index,inNew=false){
    const row=state.chat[index],key=chatScope(),request=++viewTicket,ticket=state.fileDetailTicket;if(!row||row.role!=='user'||!state.chatMeta)return;
    const chatId=state.chatMeta.id,business=state.business;
    const bytes=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(row.role+'\0'+row.text));
    const digest=[...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
    if(key!==chatScope())return;
    const saved=await api('/api/context/message',{business,chat_id:chatId,index,digest});if(key!==chatScope()||request!==viewTicket||ticket!==state.fileDetailTicket)return;
    const draft={text:saved.text,files:saved.files||[],references:saved.references||[],goal_id:saved.goal_id||'',connection:saved.connection};
    if(inNew){await newShellChat(draft);return;}
    const apply=()=>{if(key!==chatScope())return;$('#request').value=saved.text;state.selectedFiles=saved.files||[];state.contextReferences=saved.references||[];renderComposerFiles();rememberChatDraft();$('#request').focus();};
    const differentGoal=(saved.goal_id||'')!==(goal()||'');
    if($('#request').value.trim()||differentGoal){
      details('Reuse this prompt',`<p>${differentGoal?'This message used a different goal. Add it here with this chat’s current goal, or use a new chat with its original goal.':'Your current draft is saved. How would you like to use this prompt?'}</p><div class="inline-actions"><button type="button" class="primary" id="reuse-add">Add to draft</button><button type="button" class="secondary" id="reuse-new">Use in new chat</button></div>`);
      $('#reuse-add').onclick=()=>{if(key!==chatScope())return;const current=$('#request').value,next=[...refs(),...draft.references].filter((r,i,a)=>a.findIndex(v=>identity(v)===identity(r))===i),files=[...new Set([...(state.selectedFiles||[]),...draft.files])];if(next.length+files.length>12){notice('This would exceed 12 context references. Use a new chat or remove some context first.',true);return;}state.contextReferences=next;state.selectedFiles=files;$('#request').value=current+(current.trim()?'\n\n':'')+saved.text;renderComposerFiles();rememberChatDraft();$('#detail').close();$('#request').focus();};
      $('#reuse-new').onclick=()=>attempt(async()=>{if(key!==chatScope())return;await newShellChat(draft);});return;
    }
    apply();
  }
  async function inspect(item){
    if(item.kind==='file')return openFileWorkspace(item.id);
    if(item.kind==='record')return recordDetails(item.id);
    if(item.kind==='goal')return openGoal(item.id);
    const key=chatScope(),data=await api('/api/context/resolve',{business:state.business,references:[compact(item)]});if(key!==chatScope())return;
    details(item.label||'Selected context',`<pre class="context-preview">${esc(data.text)}</pre>`,'context');
  }
  function receipt(index){
    const row=state.chat[index];if(!row)return;
    details('Context selected for this message',row.references.map((r,i)=>`<button type="button" class="row" data-receipt-item="${i}"><span><strong>${esc(r.label||r.id)}</strong><small class="row-meta">${esc(kinds[r.kind])}${r.selected_at?' · '+esc(new Date(r.selected_at*1000).toLocaleString()):''}</small></span></button>`).join('')+'<p class="small-note">This records the references selected at send time. Files are read by the native app when needed.</p>');
    const host=$('#detail-content');host.onclick=event=>{const b=event.target.closest('[data-receipt-item]');if(b)attempt(()=>inspect(row.references[Number(b.dataset.receiptItem)]));};
  }
  async function setGoal(id){
    if(state.starting){notice('Wait for this request to start, then change its goal.',true);return;}
    const key=chatScope();
    if(state.chatMeta){state.goalSetting=true;try{await api('/api/goals',{business:state.business,action:'link_chat',chat_id:state.chatMeta.id,goal_id:id});if(key!==chatScope())return;state.chatMeta.goal_id=id||'';delete state.chatMeta.continuation;}finally{state.goalSetting=false;}}
    else state.draftGoalId=id||'';
    rememberChatDraft();paintComposer();
  }
  async function openGoal(id){
    const key=scope(),request=++viewTicket;details('Goal','<p role="status">Reading goal…</p>','context');
    const loading=state.fileDetailTicket,host=$('#detail-content'),data=await api('/api/goals?'+query({id}));if(request!==viewTicket||!same(key,loading,host))return;
    const g=data.goal;details(g.name,`<div class="inline-actions"><button type="button" class="primary" data-goal-work="${esc(id)}">Work on this goal</button><button type="button" class="secondary" data-goal-edit="${esc(id)}">Edit goal</button></div><p class="row-meta">${esc(human(g.status||'active'))}${g.horizon?' · '+esc(g.horizon):''}</p>${g.target!==undefined?`<p class="goal-outcome">${esc(pretty(g.target))}</p>`:''}<h3>Chats & next steps</h3><label class="goal-chat-search" ${data.chats.length<=20?'hidden':''}>Find linked work<input id="goal-chat-find" type="search" class="search" placeholder="Search chats and next steps…"></label><div id="goal-chats"></div><button type="button" class="text-button" id="goal-chats-more" hidden>Show more chats</button><h3>Saved results</h3>${data.assets.map(a=>`<button type="button" class="row" data-file="asset/${esc(a.id)}">${esc(a.name)}</button><button type="button" class="text-button" data-goal-unlink-asset="${esc(a.id)}" data-goal-id="${esc(id)}">Unlink</button>`).join('')||empty('No saved results linked yet.')}<button type="button" class="text-button" data-goal-asset="${esc(id)}">Link a saved file</button><h3>Recurring tasks</h3><div id="goal-tasks">Reading linked tasks…</div><button type="button" class="text-button" data-goal-task="${esc(id)}">Add recurring task</button>`,'context');
    const ticket=state.fileDetailTicket;let limit=20;
    const paintChats=()=>{const q=$('#goal-chat-find').value.trim().toLocaleLowerCase(),rows=data.chats.filter(c=>(c.title+' '+(c.summary||'')).toLocaleLowerCase().includes(q));$('#goal-chats').innerHTML=rows.slice(0,limit).map(c=>`<button type="button" class="row" data-chat="${esc(c.id)}"><span><strong>${esc(c.title)}</strong><small class="row-meta">${esc(data.running_chats.includes(c.id)?'Working':c.work_state==='waiting_for_usage'?'Paused after usage limit':c.status==='working'?'Last observed working':human(c.status||'Saved'))}${c.summary?' · '+esc(c.summary):''}</small></span></button>`).join('')||empty(q?'No matching linked chats.':'No chats linked yet.');$('#goal-chats-more').hidden=rows.length<=limit;};
    $('#goal-chat-find').oninput=()=>{limit=20;paintChats();};$('#goal-chats-more').onclick=()=>{limit+=20;paintChats();};paintChats();
    try{const tasks=await api('/api/schedules');if(!same(key,ticket,host))return;state.schedules=tasks;
      $('#goal-tasks').innerHTML=tasks.items.filter(t=>data.task_links[t.id]===id).map(t=>`<button type="button" class="row" data-schedule="${esc(t.id)}">${esc(t.name)}${t.description?.includes(data.goal_basis)?'':'<small class="row-meta">Review goal instructions</small>'}</button>`).join('')||empty('No recurring tasks linked yet.');
      if(tasks.notes?.length)$('#goal-tasks').insertAdjacentHTML('beforeend',`<p class="small-note">${tasks.notes.map(esc).join(' ')}</p>`);
    }catch(error){if(same(key,ticket,host))$('#goal-tasks').textContent=error.message;}
  }
  async function editGoal(id=''){
    const key=scope(),request=++viewTicket;details(id?'Edit goal':'Add a goal','<p role="status">Reading goal…</p>');const loading=state.fileDetailTicket,loadingHost=$('#detail-content');
    const data=id?await api('/api/goals?'+query({id})):null;if(request!==viewTicket||!same(key,loading,loadingHost))return;const g=data?.goal||{};
    const simple=g.target===undefined||typeof g.target==='string'||typeof g.target==='number';
    details(id?'Edit goal':'Add a goal',`<form id="compose-goal-form" class="form-grid"><label>What do you want to accomplish?<input name="name" required maxlength="2000" value="${esc(g.name||'')}"></label>${simple?`<label>Desired outcome or target <span class="muted">Optional</span><textarea name="target" maxlength="5000" rows="2">${esc(g.target??'')}</textarea></label>`:`<p>${esc(pretty(g.target))}</p>`}<label>Timeframe <span class="muted">Optional</span><input name="horizon" maxlength="300" value="${esc(g.horizon||'')}" placeholder="For example, this quarter"></label><label>Status<select name="status">${['active','paused','completed'].map(v=>`<option value="${v}" ${(g.status||'active')===v?'selected':''}>${human(v)}</option>`).join('')}</select></label><button class="primary">Save goal</button><p id="goal-save-status" role="status"></p></form>`);
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    $('#compose-goal-form').onsubmit=event=>{event.preventDefault();const form=event.currentTarget;attempt(async()=>{
      const values=Object.fromEntries(new FormData(form));if(g.target!==undefined&&values.target===String(g.target))delete values.target;
      const button=form.querySelector('button');button.disabled=true;
      try{const saved=await api('/api/goals',{business:state.business,action:'save',...(id?{id}:{}),...values});if(!same(key,ticket,host))return;cache.clear();await refresh();if(same(key,ticket,host))await openGoal(saved.goal.id);}catch(error){if(same(key,ticket,host))$('#goal-save-status').textContent=error.message;}finally{if(button.isConnected)button.disabled=false;}
    });};
  }
  async function linkAsset(id){
    const key=scope();const assets=state.data.records.filter(r=>r.type==='Asset');details('Link a saved file',assets.map(a=>`<button type="button" class="row" data-link-goal-asset="${esc(a.ref)}">${esc(a.title)}</button>`).join('')||empty('Save a file to this business first.'));
    $('#detail-content').onclick=event=>attempt(async()=>{const b=event.target.closest('[data-link-goal-asset]');if(!b||key!==scope())return;await api('/api/goals',{business:state.business,action:'link_asset',goal_id:id,asset_id:b.dataset.linkGoalAsset});if(key===scope())await openGoal(id);});
  }
  async function continuation(){
    if(!state.chatMeta||!goal())return;const key=chatScope(),c=state.chatMeta,p=c.continuation||{},supported=['pi','omp'].includes(c.agent);
    details('Continuation',`<form id="continuation-form" class="form-grid"><label>After an interruption<select name="mode"><option value="manual" ${p.mode!=='native'?'selected':''}>Continue manually</option>${supported?`<option value="native" ${p.mode==='native'?'selected':''}>Allow native retries until expiry</option>`:''}</select></label>${supported?`<label>Automatic continuation expires<input name="until" type="datetime-local" value="${new Date(p.until?p.until*1000:Date.now()+86400000).toLocaleString('sv-SE').slice(0,16).replace(' ','T')}"></label>`:''}<p class="small-note">${supported?'Uses retries already enabled by your native app. It may end the request instead of waiting for a quota reset.':'This connection requires manual continuation after quota interruptions.'} Aura and the native connection must remain running. Stop cancels automatic continuation.</p><button class="primary">Save</button><p id="continuation-status" role="status"></p></form>`);
    const form=$('#continuation-form');form.onsubmit=event=>{event.preventDefault();attempt(async()=>{if(key!==chatScope())return;const values=Object.fromEntries(new FormData(form));await api('/api/goals',{business:state.business,action:'continuation',chat_id:c.id,mode:values.mode,until:values.until?new Date(values.until).getTime()/1000:null});if(key!==chatScope())return;c.continuation={mode:values.mode,until:values.until?new Date(values.until).getTime()/1000:null};$('#continuation-status').textContent='Saved. The current native request keeps its existing execution context.';});};
  }
  function prepareContinuation(){
    const text='Continue the current assignment toward the linked goal. First check the latest native conversation and saved files to see what already succeeded. Resume only the remaining work, without repeating completed external actions. If the assignment is already done or needs a decision, report that rather than inventing more work.';
    const key=chatScope();
    if($('#request').value.trim()){
      details('Continue this assignment','<p>Your current draft is saved.</p><button type="button" class="primary" id="add-continuation-draft">Add continuation request to draft</button>');
      $('#add-continuation-draft').onclick=()=>{if(key!==chatScope())return;$('#request').value+='\n\n'+text;rememberChatDraft();$('#detail').close();$('#request').focus();};return;
    }
    $('#request').value=text;rememberChatDraft();$('#request').focus();
  }
  async function assignTask(task,host){
    const key=scope(),data=await api('/api/goals?'+query({}));if(key!==scope()||!host.isConnected)return;
    host.innerHTML=`<label>Goal<select id="task-goal"><option value="">No goal selected</option>${data.items.map(g=>`<option value="${esc(g.id)}" ${data.task_links[task.id]===g.id?'selected':''}>${esc(g.name)}</option>`).join('')}</select></label><p class="small-note">Selecting a goal updates the task’s native instructions through its existing AI connection.</p><button type="button" class="secondary" id="task-goal-update">Update goal instructions</button><p id="task-goal-status" role="status"></p>`;
    const update=()=>attempt(async()=>{
      const select=$('#task-goal'),button=$('#task-goal-update'),id=select.value;select.disabled=true;button.disabled=true;
      try{await scheduleOperation({action:'request',id:task.id,app:task.owner,goal_id:id,...(!id?{remove_goal:true}:{}),request:id?'Associate this task with the selected Aura goal. Preserve its timing, model, permissions and business work; add a current-goal preflight check to its instructions.':'Remove this task’s Aura goal association.'});}
      finally{if(select.isConnected)select.disabled=false;if(button.isConnected)button.disabled=false;}
      if(key===scope()&&host.isConnected)$('#task-goal-status').textContent=state.scheduleJob?.message||'Updating the native task…';
    });
    $('#task-goal').onchange=update;$('#task-goal-update').onclick=update;
  }
  function draft(){return {references:refs(),goal_id:state.draftGoalId||''};}
  function restore(saved){state.contextReferences=Array.isArray(saved?.references)?saved.references.filter(r=>r&&kinds[r.kind]&&typeof r.id==='string'&&r.id).slice(0,12):[];state.draftGoalId=state.chatMeta?'':typeof saved?.goal_id==='string'?saved.goal_id:'';closeMenu();paintComposer();}
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b)return;
    if(b.dataset.composeOption!==undefined)attempt(()=>selectInline(Number(b.dataset.composeOption)));
    if(b.dataset.composeRemove!==undefined){state.contextReferences=refs().filter((r,i)=>i!==Number(b.dataset.composeRemove));rememberChatDraft();paintComposer();}
    if(b.dataset.composeInspect!==undefined)attempt(()=>inspect(refs()[Number(b.dataset.composeInspect)]));
    if(b.dataset.messageCopy!==undefined){const row=state.chat[Number(b.dataset.messageCopy)];if(row)attempt(async()=>{await navigator.clipboard.writeText(row.text);notice('Copied.');});}
    if(b.dataset.messageReuse!==undefined)attempt(()=>reuse(Number(b.dataset.messageReuse)));
    if(b.dataset.messageNew!==undefined)attempt(()=>reuse(Number(b.dataset.messageNew),true));
    if(b.dataset.messageContext!==undefined)receipt(Number(b.dataset.messageContext));
    if(b.hasAttribute('data-compose-clear-goal'))attempt(()=>setGoal(''));
    if(b.id==='choose-goal')attempt(()=>choose('goal','',true));
    if(b.dataset.composeGoal)attempt(()=>openGoal(b.dataset.composeGoal));
    if(b.dataset.goalEdit)attempt(()=>editGoal(b.dataset.goalEdit));
    if(b.dataset.goalAsset)attempt(()=>linkAsset(b.dataset.goalAsset));
    if(b.dataset.goalUnlinkAsset)attempt(async()=>{const key=scope();await api('/api/goals',{business:state.business,action:'link_asset',goal_id:'',asset_id:b.dataset.goalUnlinkAsset});if(key===scope())await openGoal(b.dataset.goalId);});
    if(b.id==='chat-continuation')attempt(continuation);
    if(b.hasAttribute('data-compose-new-goal'))attempt(()=>editGoal());
    if(b.dataset.goalWork)attempt(async()=>{const id=b.dataset.goalWork;await newShellChat({text:'Help me make the next useful step toward this goal. Check existing work first and explain what remains.',files:[],references:[],goal_id:id,connection:composerConnection()});});
    if(b.dataset.goalTask){state.scheduleDraft={name:'',description:'',when:'',goal_id:b.dataset.goalTask};state.scheduleAdding=true;state.view='tools';attempt(async()=>{await render();recordShellRoute();});}
    if(b.dataset.composeAssistant)attempt(()=>window.auraWork.startAssistant(b.dataset.composeAssistant,{text:$('#request').value,files:state.selectedFiles||[],references:refs(),goal_id:goal(),connection:composerConnection()}));
  });
  const input=$('#request');input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>attempt(suggest),120);});
  input.addEventListener('keydown',event=>{
    if(event.isComposing||$('#composer-menu').hidden)return;
    if(['ArrowDown','ArrowUp','Enter','Escape'].includes(event.key)){
      event.preventDefault();event.stopImmediatePropagation();
      if(event.key==='Escape')closeMenu();else if(event.key==='Enter')attempt(()=>selectInline(active));else{active=(active+(event.key==='ArrowDown'?1:-1)+inlineItems.length)%inlineItems.length;paintMenu();}
    }
  },true);
  document.addEventListener('click',event=>{if(!event.target.closest('#chat-form'))closeMenu();});
  if('pendingComposerDraft' in state)restore(state.pendingComposerDraft);
  return {render:paintComposer,actions,draft,restore,choose,openGoal,editGoal,closeMenu,assignTask,prepareContinuation,reuse};
})();
