/* Context selection, message reuse and goals share the existing composer and APIs. */
'use strict';
window.auraCompose=(()=>{
  let lookupTicket=0,viewTicket=0,inlineItems=[],active=-1,inlineToken=null,timer=null;
  let goalPage=null,goalTrail=[],returningGoal=false;
  const cache=new Map(),scope=()=>JSON.stringify([state.data?.workspace,state.business]),refs=()=>state.contextReferences||[];
  const goal=()=>state.chatMeta?.goal_id||state.draftGoalId||'';
  const goalConnection=()=>state.view==='home'?composerConnection():{kind:state.data.connection.selected,model:state.data.connection.model||'',effort:state.data.connection.effort||''};
  function newChatGoal(){
    const id=goal(),saved=state.data.records.find(r=>r.ref===id)?.data;
    if(!saved||goalInfo(saved).deleted_at||(saved.status||'active')!=='active')return '';
    const info=goalInfo(saved),next=info.scope==='chat'?info.workspace_goal_ref:id;
    const target=state.data.records.find(r=>r.ref===next)?.data;
    return target&&!goalInfo(target).deleted_at&&(target.status||'active')==='active'?next:'';
  }
  const query=extra=>new URLSearchParams({business:state.business,...extra});
  const same=(key,ticket,host)=>key===scope()&&ticket===state.fileDetailTicket&&host.isConnected&&$('#detail').open;
  const compact=r=>({kind:r.kind,id:r.id,label:r.label,...(r.variant?{variant:r.variant}:{}),...(r.request_id?{request_id:r.request_id}:{})});
  const identity=r=>JSON.stringify([r.kind,r.id,r.variant||'',r.request_id||'']);
  const kinds={collection:'Saved results',file:'File',record:'Saved context',goal:'Goal',library:'Library',assistant:'Assistant',result:'Saved result'};
  const shortcuts=[{id:'new',label:'New chat',description:'Keep this draft and open a new chat'},{id:'attach',label:'Attach context',description:'Files, saved work and operating knowledge'},{id:'assistant',label:'Choose agent',description:'Start a chat with a named assistant'},{id:'goal',label:'Chat goal',description:'Set what this chat is working toward'}];
  const nativeCommands=()=>{const rows=state.liveJob?.native_commands||state.chatMeta?.native_commands||[];return rows.filter(c=>typeof c.name==='string'&&c.name&&!c.name.startsWith('aura-')).map(c=>({id:c.name.replace(/^\//,''),native:true,label:c.name.replace(/^\//,''),description:c.description||'AI app command'}));};
  const goalVersion=g=>JSON.stringify([g?.name,g?.status,g?.target,goalInfo(g).revision,goalInfo(g).deleted_at]);
  const goalStatus=g=>goalInfo(g).deleted_at?'Deleted':human(g?.status||'active');
  const goalLabel=g=>(goalInfo(g).scope==='chat'?'Chat goal':'Workspace goal')+(goalInfo(g).deleted_at||(g?.status||'active')!=='active'?' · '+goalStatus(g):'');
  function beginGoalPage(kind,id,title,open,mode='panel'){
    const prior=goalPage&&goalPage.ticket===state.fileDetailTicket&&$('#detail').open?goalPage:null;
    if(!returningGoal){if(prior&&(prior.kind!==kind||prior.id!==id)){prior.scroll=$('#detail-content').scrollTop;goalTrail.push(prior);if(goalTrail.length>12)goalTrail.shift();}else if(!prior)goalTrail=[];}
    returningGoal=false;details(title,'<p role="status">Reading goals…</p>',mode);goalPage={kind,id,title,open,ticket:state.fileDetailTicket};
  }
  function goalDetails(title,html,mode='panel'){
    details(title,html,mode);
    if(goalTrail.length)setDetailBack(goalTrail.at(-1).title||'Goals',backGoal);
    if(goalPage){goalPage.ticket=state.fileDetailTicket;goalPage.title=title;}
  }
  async function backGoal(){
    const prior=goalTrail.pop();if(!prior)return;returningGoal=true;await prior.open();
    if(goalPage?.kind===prior.kind&&goalPage?.id===prior.id)$('#detail-content').scrollTop=prior.scroll||0;
  }
  async function openRelatedGoal(kind,id){
    const prior=goalPage,key=scope(),scroll=$('#detail-content').scrollTop;
    if(kind==='file')await openFileWorkspace('asset/'+id);else await scheduleDetails(id);
    if(key!==scope()||!prior||!$('#detail').open)return;
    if(kind==='file'&&!$('#file-workspace')||kind==='task'&&(!$('#task-edit-form')||state.editingTask?.id!==id))return;
    $('#detail-content').insertAdjacentHTML('afterbegin','<button type="button" class="text-button goal-back" id="return-related-goal">← Back to goal</button>');
    $('#return-related-goal').onclick=()=>attempt(async()=>{if(key!==scope())return;returningGoal=true;await prior.open();if(key===scope())$('#detail-content').scrollTop=scroll;});
  }

  async function lookup(q='',kind='',assistant=''){
    const key=scope(),id=JSON.stringify([key,q.toLowerCase(),kind,assistant]),prior=cache.get(id);
    if(prior&&Date.now()-prior.at<5000)return prior.data;
    const data=await api('/api/context?'+query({q,kind,limit:30,...(assistant?{assistant}:{})}));
    if(key!==scope())return null;cache.set(id,{at:Date.now(),data});while(cache.size>30)cache.delete(cache.keys().next().value);return data;
  }
  function paintComposer(){
    const host=$('#composer-contexts');if(!host)return;
    const items=refs(),goalId=goal(),saved=state.data?.records?.find(r=>r.ref===goalId),info=goalInfo(saved?.data),name=saved?.title||'Unavailable goal',local=info.scope==='chat',parent=state.data?.records?.find(r=>r.ref===info.workspace_goal_ref);
    host.hidden=!items.length&&!goalId;
    const markup=(goalId?`<span class="context-chip goal-chip"><button type="button" data-compose-goal="${esc(goalId)}" title="Open goal">${esc(goalLabel(saved?.data))}: ${esc(name)}</button><button type="button" data-compose-clear-goal aria-label="Remove goal from this chat">×</button></span>`:'')+(goalId&&info.workspace_goal_ref?`<span class="context-chip"><button type="button" data-compose-goal="${esc(info.workspace_goal_ref)}">${esc(parent?goalLabel(parent.data):'Workspace goal')}: ${esc(parent?.title||'Unavailable')}</button><button type="button" data-goal-unlink-workspace="${esc(goalId)}" aria-label="Disconnect workspace goal">×</button></span>`:'')+items.map((r,i)=>`<span class="context-chip"><button type="button" data-compose-inspect="${i}" title="Review selected context">${esc(r.label||r.id)}</button><button type="button" data-compose-remove="${i}" aria-label="Remove ${esc(r.label||r.id)}">×</button></span>`).join('');
    if(host.innerHTML!==markup)host.innerHTML=markup;
    const button=$('#choose-goal');if(button){const label=button.querySelector('span');if(label)label.textContent=goalId?'Change goal':'Goal';else button.textContent=goalId?'Change goal':'Goal';}
  }
  function add(item){
    if(refs().some(r=>identity(r)===identity(item)))return true;
    if(refs().length+(state.selectedFiles||[]).length>=12){notice('Choose up to 12 context references.',true);return false;}
    state.contextReferences=[...refs(),compact(item)];rememberChatDraft();paintComposer();return true;
  }
  function closeMenu(){++lookupTicket;inlineItems=[];active=-1;inlineToken=null;const menu=$('#composer-menu');if(menu){menu.hidden=true;menu.innerHTML='';}$('#request').removeAttribute('aria-activedescendant');$('#request').setAttribute('aria-expanded','false');}
  function token(){
    const input=$('#request'),before=input.value.slice(0,input.selectionStart);
    const slash=before.match(/^\/([^\s]*)$/u);if(slash)return {type:'slash',q:slash[1],start:0,end:input.selectionStart};
    const mention=before.match(/(?:^|\s)@([^\n@]{0,80})$/);if(!mention)return null;
    if(refs().some(r=>mention[1]===(r.label||r.id)||mention[1].startsWith((r.label||r.id)+' ')))return null;
    return {type:'mention',q:mention[1],start:before.length-mention[1].length-1,end:input.selectionStart};
  }
  function paintMenu(){
    const menu=$('#composer-menu');menu.hidden=!inlineItems.length;$('#request').setAttribute('aria-expanded',String(!menu.hidden));
    menu.innerHTML=inlineItems.map((r,i)=>`<button type="button" role="option" id="composer-option-${i}" aria-selected="${i===active}" data-compose-option="${i}" class="${i===active?'selected':''}"><span>${r.native?esc('/'+r.id):(r.kind?'':esc('/aura-'+r.id)+' · ')+esc(r.label)}</span><small>${esc(r.kind?kinds[r.kind]:r.description)}${r.kind&&r.description?' · '+esc(r.description):''}</small></button>`).join('');
    if(active>=0)$('#request').setAttribute('aria-activedescendant','composer-option-'+active);
  }
  async function suggest(){
    const selected=token(),key=chatScope(),ticket=++lookupTicket;
    if(!selected){closeMenu();return;}
    const data=selected.type==='slash'?{items:[...nativeCommands(),...shortcuts].filter(c=>((c.native?'':'aura-')+c.id).toLowerCase().startsWith(selected.q.toLowerCase()))}:await lookup(selected.q);
    if(ticket!==lookupTicket||key!==chatScope()||JSON.stringify(selected)!==JSON.stringify(token())||!data)return;
    inlineToken=selected;inlineItems=data.items.slice(0,8);active=inlineItems.length?0:-1;paintMenu();
  }
  async function selectInline(index){
    const item=inlineItems[index],selected=inlineToken;if(!item||!selected)return;
    if(selected.type==='mention'&&item.kind!=='assistant'&&!add(item))return;
    const input=$('#request');input.setRangeText(item.native?'/'+item.id+' ':selected.type==='mention'&&item.kind!=='assistant'?'@'+item.label+' ':'',selected.start,selected.end,'end');closeMenu();rememberChatDraft();
    if(selected.type==='slash'&&!item.native)await command(item.id);
    else if(item.kind==='assistant')await choose('result',item.id);
    if(!document.querySelector('dialog:modal'))input.focus();
  }
  async function command(id){
    if(id==='new')return newShellChat({text:$('#request').value,files:state.selectedFiles||[],references:refs(),goal_id:newChatGoal(),connection:composerConnection()});
    if(id==='attach')return choose();
    if(id==='assistant')return chooseAssistant();
    if(id==='goal')return chatGoal();
  }
  async function choose(kind='',assistant='',linkGoal=false){
    closeMenu();const key=chatScope();details(linkGoal?'Connect a workspace goal':assistant?'Choose an assistant’s saved result':'Add context','<p role="status">Finding context…</p>');
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    host.innerHTML=`<label>${linkGoal?'Find a saved goal':'Find context'}<input id="compose-find" class="search" type="search" placeholder="Search by name…"></label>${!assistant&&!linkGoal?`<label>Type<select id="compose-kind"><option value="">All context</option>${Object.entries(kinds).map(([k,v])=>`<option value="${k}" ${k===kind?'selected':''}>${v}</option>`).join('')}</select></label>`:''}<div id="compose-found" role="status">Finding context…</div>`;
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
    if(linkGoal)host.insertAdjacentHTML('beforeend','<button type="button" class="text-button" data-compose-new-goal>Create a chat goal instead</button>');
    $('#compose-find').oninput=()=>{clearTimeout(timer);timer=setTimeout(()=>attempt(paint),150);};$('#compose-kind')?.addEventListener('change',()=>attempt(paint));await paint();if(same(scope(),ticket,host))$('#compose-find').focus();
  }
  async function chooseAssistant(){
    const key=chatScope(),data=await window.auraWork.load();if(!data||key!==chatScope())return;
    details('Choose agent',data.items.map(p=>`<button type="button" class="row" data-compose-assistant="${esc(p.id)}"><strong>${esc(p.name)}</strong></button>`).join('')||empty('Create an agent from Agents first.'));
  }
  function actions(row,index){
    if(row.role!=='user')return row.trace_id?`<div class="message-actions"><button type="button" class="text-button" data-request-activity="${esc(row.trace_id)}">Activity</button></div>`:'';
    return `<div class="message-actions"><button type="button" class="icon-button" data-message-copy="${index}" aria-label="Copy prompt" title="Copy prompt"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 8h12v13H8zM16 8V3H3v13h5"/></svg></button>${row.references?.length?`<button type="button" class="text-button" data-message-context="${index}">Context (${row.references.length})</button>`:''}</div>`;
  }
  async function reuse(index,inNew=false){
    const row=state.chat[index],key=chatScope(),request=++viewTicket,ticket=state.fileDetailTicket;if(!row||row.role!=='user'||!state.chatMeta)return;
    const chatId=state.chatMeta.id,business=state.business;
    const bytes=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(row.role+'\0'+row.text));
    const digest=[...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
    if(key!==chatScope())return;
    const saved=await api('/api/context/message',{business,chat_id:chatId,index,digest});if(key!==chatScope()||request!==viewTicket||ticket!==state.fileDetailTicket)return;
    const draft={text:saved.text,files:saved.files||[],references:saved.references||[],goal_id:saved.new_chat_goal_id??saved.goal_id??'',connection:saved.connection};
    if(inNew){await newShellChat(draft);return;}
    const apply=()=>{if(key!==chatScope())return;$('#request').value=saved.text;state.selectedFiles=saved.files||[];state.contextReferences=saved.references||[];renderComposerFiles();rememberChatDraft();$('#request').focus();};
    const differentGoal=(saved.goal_id||'')!==(goal()||'');
    if($('#request').value.trim()||differentGoal){
      details('Reuse this prompt',`<p>${differentGoal?'This message used a different goal. Add it here with this chat’s current goal, or start a new chat.':'Your current draft is saved. How would you like to use this prompt?'}</p><div class="inline-actions"><button type="button" class="primary" id="reuse-add">Add to draft</button><button type="button" class="secondary" id="reuse-new">Use in new chat</button></div>`);
      $('#reuse-add').onclick=()=>{if(key!==chatScope())return;const current=$('#request').value,next=[...refs(),...draft.references].filter((r,i,a)=>a.findIndex(v=>identity(v)===identity(r))===i),files=[...new Set([...(state.selectedFiles||[]),...draft.files])];if(next.length+files.length>12){notice('This would exceed 12 context references. Use a new chat or remove some context first.',true);return;}state.contextReferences=next;state.selectedFiles=files;$('#request').value=current+(current.trim()?'\n\n':'')+saved.text;renderComposerFiles();rememberChatDraft();$('#detail').close();$('#request').focus();};
      $('#reuse-new').onclick=()=>attempt(async()=>{if(key!==chatScope())return;await newShellChat(draft);});return;
    }
    apply();
  }
  async function inspect(item){
    if(item.kind==='collection')return window.auraProjects?.openCollection(item.id);
    if(item.kind==='file')return openFileWorkspace(item.id);
    if(item.kind==='record')return recordDetails(item.id);
    if(item.kind==='goal')return openGoal(item.id);
    if(item.kind==='library')return openLibrary(item.id,item.variant||'');
    const key=chatScope(),data=await api('/api/context/resolve',{business:state.business,references:[compact(item)]});if(key!==chatScope())return;
    const preview=data.previews?.[0];details(item.label||'Saved result',preview?`<div class="saved-result-preview">${chatMarkdown(preview.text)}</div>`:`<pre class="context-preview">${esc(data.text)}</pre>`,'context');
  }
  function receipt(index){
    const row=state.chat[index];if(!row)return;
    details('Context selected for this message',row.references.map((r,i)=>`<button type="button" class="row" data-receipt-item="${i}"><span><strong>${esc(r.label||r.id)}</strong><small class="row-meta">${esc(kinds[r.kind])}${r.selected_at?' · '+esc(new Date(r.selected_at*1000).toLocaleString()):''}</small></span></button>`).join('')+'<p class="small-note">This records the references selected at send time. Files are read by the native app when needed.</p>');
    const host=$('#detail-content');host.onclick=event=>{const b=event.target.closest('[data-receipt-item]');if(b)attempt(()=>inspect(row.references[Number(b.dataset.receiptItem)]));};
  }
  async function setGoal(id){
    if(state.starting)throw new Error('Wait for this request to start, then change its goal.');
    const key=chatScope();
    if(state.chatMeta){state.goalSetting=true;try{const linked=await api('/api/goals',{business:state.business,action:'link_chat',chat_id:state.chatMeta.id,goal_id:id});if(key!==chatScope())return;state.chatMeta.goal_id=id||'';if(id)state.chatMeta.goal_history=[...new Set([...(state.chatMeta.goal_history||[]),id,...(linked.workspace_goal?[linked.workspace_goal.id]:[])])];delete state.chatMeta.continuation;}finally{state.goalSetting=false;}}
    else state.draftGoalId=id||'';
    rememberChatDraft();paintComposer();
  }
  async function openGoal(id){
    const key=scope(),request=++viewTicket;beginGoalPage('goal',id,'Goal',()=>openGoal(id));
    const loading=state.fileDetailTicket,host=$('#detail-content');let data;
    try{data=await api('/api/goals?'+query({id,kind:goalConnection().kind}));}catch(error){
      if(request===viewTicket&&same(key,loading,host))goalDetails('Goal unavailable',`<p>${esc(humanError(error))}</p><div class="inline-actions"><button type="button" class="secondary" data-compose-goal="${esc(id)}">Try again</button>${state.view==='home'&&goal()===id?'<button type="button" class="text-button" data-compose-clear-goal>Remove from this chat</button>':''}<button type="button" class="text-button" data-goal-manager>All goals</button></div>`);return;
    }
    if(request!==viewTicket||!same(key,loading,host))return;
    const g=data.goal,info=goalInfo(g),local=data.scope==='chat'||info.scope==='chat',status=g.status||'active';
    if(goalPage){goalPage.basis=data.goal_basis;goalPage.recordVersion=goalVersion(g);}
    if(data.deleted||info.deleted_at){goalDetails(g.name,`<p>This goal was deleted. Its conversations and saved work are still available.</p><div class="inline-actions"><button type="button" class="primary" data-goal-restore="${esc(id)}">Restore goal</button><button type="button" class="text-button" data-goal-manager>All goals</button></div>`,'panel');setDetailTitleActions('<span class="goal-status" data-status="deleted">Deleted</span>');return;}
    const inChat=state.view==='home',current=inChat&&goal()===id,owner=info.chat_id,ownerAvailable=data.chats.some(c=>c.id===owner),connected=data.chat_goals||[];
    const linked=connected.length?`<section class="goal-connected"><h3>Connected chat goals</h3><p class="small-note">${connected.length} connected · ${connected.filter(g=>g.status==='completed').length} completed</p><div id="goal-efforts"></div><button type="button" class="text-button" id="goal-efforts-more" hidden>Show more chat goals</button></section>`:'';
    const work=local?(owner&&(!inChat||owner!==state.chatMeta?.id)?(ownerAvailable?`<button type="button" class="primary" data-chat="${esc(owner)}">Open chat</button>`:''):inChat&&!current?`<button type="button" class="primary" data-goal-use="${esc(id)}">Use in this chat</button>`:''):inChat&&state.chatMeta?`<button type="button" class="secondary" data-goal-connect="${esc(id)}" ${current?'disabled':''}>${current?'Linked to this chat':'Use in this chat'}</button>`:`<button type="button" class="primary" data-goal-start="${esc(id)}">Start a chat</button>`;
    const nativeSupport=data.native_goal_support,nativeState=data.native_goal;
    const nativeAction=local&&(!owner||ownerAvailable)&&status==='active'&&nativeSupport?.supported?`<button type="button" class="primary" data-goal-run="${esc(id)}" data-goal-budget="${!!nativeSupport.token_budget}" ${data.running_chats.includes(owner)?'disabled':''}>${data.running_chats.includes(owner)?'Working':'Work toward goal'}</button>`:'';
    const toolbar=`<div class="goal-actions"><div class="inline-actions">${nativeAction}${work}<button type="button" class="secondary" data-goal-edit="${esc(id)}">Edit</button><button type="button" class="secondary" data-goal-state="${esc(id)}" data-goal-status="${status==='completed'?'active':'completed'}">${status==='completed'?'Reopen':'Mark complete'}</button>${status!=='completed'?`<button type="button" class="text-button" data-goal-state="${esc(id)}" data-goal-status="${status==='paused'?'active':'paused'}">${status==='paused'?'Resume':'Pause'}</button>`:''}</div><button type="button" class="icon-button danger goal-delete" title="Delete goal" aria-label="Delete goal" data-goal-delete="${esc(id)}" data-linked-tasks="${Object.keys(data.task_links||{}).length}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15M10 10v7M14 10v7"/></svg></button></div><div class="inline-actions goal-context-actions">${current?'<button type="button" class="text-button" data-compose-clear-goal>Remove from this chat</button>':''}${local?`<button type="button" class="text-button" data-goal-promote="${esc(id)}">Make workspace goal</button>`:''}${current&&status==='active'&&['pi','omp'].includes(state.chatMeta?.agent)?'<button type="button" class="text-button" id="chat-continuation">Retry settings</button>':''}${state.view==='business'?'':`<button type="button" class="text-button" data-goal-manager ${local&&ownerAvailable?`data-chat-goals="${esc(owner)}"`:''}>${local&&ownerAvailable?'Chat goal history':'Browse goals'}</button>`}</div>`;
    goalDetails(g.name,`${toolbar}${local&&nativeSupport?`<p class="small-note">${nativeSupport.supported?(nativeState?`Native goal · ${esc(human(nativeState.status||'Not checked'))}${nativeState.reason?' · '+esc(nativeState.reason):''}`:'Work toward goal uses this chat’s native AI app.'):esc(nativeSupport.reason)}</p>`:''}<div class="goal-outcome"><h3>Done when</h3>${g.target!==undefined?`<p>${esc(pretty(g.target))}</p>`:`<button type="button" class="text-button" data-goal-edit="${esc(id)}">Add completion criteria</button>`}</div>${data.workspace_goal?`<p class="goal-parent">Contributes to <button type="button" class="text-button" data-compose-goal="${esc(data.workspace_goal.id)}">${esc(data.workspace_goal.name)}</button></p>`:info.workspace_goal_ref?'<p class="small-note">The connected workspace goal is unavailable. Edit this goal to change or remove its connection.</p>':''}${current?`<button type="button" class="text-button" data-new-chat-goal>${local?'Set a different chat goal':'Set a chat goal'}</button>`:''}${linked}<div class="section-head"><h3 class="goal-section-title">Chats</h3>${!local?`<button type="button" class="text-button" data-goal-link="${esc(id)}">＋ Link a chat</button>`:''}</div><label class="goal-chat-search" ${data.chats.length<=20?'hidden':''}>Find linked work<input id="goal-chat-find" type="search" class="search" placeholder="Search chats and next steps…"></label><div id="goal-chats"></div><button type="button" class="text-button" id="goal-chats-more" hidden>Show more chats</button><div class="section-head"><h3 class="goal-section-title">Saved files</h3><button type="button" class="text-button" data-goal-asset="${esc(id)}">＋ Link file</button></div>${data.assets.map(a=>`<div class="goal-result-row"><button type="button" class="row" data-goal-open-file="${esc(a.id)}"><span class="goal-linked-row"><strong>${esc(a.name)}</strong>${a.path?`<span class="goal-linked-summary">${esc(a.path)}</span>`:''}</span></button>${!a.goal_id||a.goal_id===id?`<button type="button" class="text-button" data-goal-unlink-asset="${esc(a.id)}" data-goal-id="${esc(id)}">Remove link</button>`:`<button type="button" class="text-button" data-compose-goal="${esc(a.goal_id)}">From ${esc(state.data.records.find(r=>r.ref===a.goal_id)?.title||'connected chat goal')}</button>`}</div>`).join('')||'<p class="small-note">No files linked yet.</p>'}${!local?`<div class="section-head"><h3 class="goal-section-title">Scheduled tasks</h3><button type="button" class="text-button" data-goal-task="${esc(id)}">＋ Add task</button></div><div id="goal-tasks">Reading linked tasks…</div>`:''}`,'panel');
    setDetailTitleActions(`<span class="goal-status" data-status="${esc(status)}" title="${local?'Chat goal':'Workspace goal'}">${esc(human(status))}</span>`);
    const ticket=state.fileDetailTicket;let limit=20,effortLimit=20;
    if(connected.length){const paint=()=>{$('#goal-efforts').innerHTML=connected.slice(0,effortLimit).map(g=>`<button type="button" class="row" data-compose-goal="${esc(g.id)}"><span><strong>${esc(g.name)}</strong><small class="row-meta">${esc(goalStatus(g))}</small></span></button>`).join('');$('#goal-efforts-more').hidden=connected.length<=effortLimit;};$('#goal-efforts-more').onclick=()=>{effortLimit+=20;paint();};paint();}
    const paintChats=()=>{const q=$('#goal-chat-find').value.trim().toLocaleLowerCase(),rows=data.chats.filter(c=>(c.title+' '+(c.summary||'')).toLocaleLowerCase().includes(q));$('#goal-chats').innerHTML=rows.slice(0,limit).map(c=>`<button type="button" class="row" data-chat="${esc(c.id)}"><span class="goal-linked-row"><strong>${esc(c.title)}</strong>${c.summary?`<span class="goal-linked-summary">${esc(c.summary)}</span>`:''}${data.running_chats.includes(c.id)||c.work_state==='waiting_for_usage'||c.status==='working'||c.status==='error'?`<span class="goal-linked-state">${data.running_chats.includes(c.id)?'Working':c.status==='error'?'Needs attention':c.work_state==='waiting_for_usage'?'Paused after usage limit':'Last observed working'}</span>`:''}</span></button>`).join('')||`<p class="small-note">${q?'No matching linked chats.':'No chats linked yet.'}</p>`;$('#goal-chats-more').hidden=rows.length<=limit;};
    $('#goal-chat-find').oninput=()=>{limit=20;paintChats();};$('#goal-chats-more').onclick=()=>{limit+=20;paintChats();};paintChats();
    if(local)return;
    try{const tasks=await api('/api/schedules');if(!same(key,ticket,host))return;state.schedules=tasks;
      $('#goal-tasks').innerHTML=tasks.items.filter(t=>data.task_links[t.id]===id).map(t=>`<button type="button" class="row" data-goal-open-task="${esc(t.id)}"><span class="goal-linked-row"><strong>${esc(t.name)}</strong>${t.schedule?`<span class="goal-linked-summary">${esc(t.schedule)}</span>`:''}${t.description?.includes(data.goal_basis)?'':'<span class="goal-linked-state">Review goal instructions</span>'}</span></button>`).join('')||'<p class="small-note">No scheduled tasks linked yet.</p>';
      if(tasks.notes?.length)$('#goal-tasks').insertAdjacentHTML('beforeend',`<p class="small-note">${tasks.notes.map(esc).join(' ')}</p>`);
    }catch(error){if(same(key,ticket,host))$('#goal-tasks').textContent=humanError(error);}
  }
  async function chatGoal(){
    if(goal())return openGoal(goal());
    return editGoal('',true);
  }
  async function editGoal(id='',forChat=false){
    const chatKey=chatScope();let savedId=id;
    const key=scope(),request=++viewTicket;beginGoalPage('edit',id||String(forChat),id?'Edit goal':forChat?'Goal for this chat':'New goal',()=>editGoal(id,forChat),'panel');
    const loading=state.fileDetailTicket,loadingHost=$('#detail-content');
    const data=id?await api('/api/goals?'+query({id})):null;if(request!==viewTicket||!same(key,loading,loadingHost))return;
    const g=data?.goal||{},info=goalInfo(g),local=id?info.scope==='chat':forChat;
    if(goalPage)goalPage.basis=data?.goal_basis;
    const current=state.data.records.find(r=>r.ref===goal())?.data;
    const parent=info.workspace_goal_ref||(!id&&forChat&&current?(goalInfo(current).scope==='chat'?goalInfo(current).workspace_goal_ref||'':goal()):'');
    const parents=workspaceGoalRecords(true).filter(r=>(r.data.status||'active')==='active'||r.ref===parent);
    const connection=local?`<details class="goal-connection" ${parent?'open':''}><summary>Connect to a workspace goal <span class="muted">Optional</span></summary><label>Workspace goal<select name="workspace_goal_id"><option value="">No connection</option>${parent&&!parents.some(r=>r.ref===parent)?`<option value="${esc(parent)}" selected>Unavailable workspace goal</option>`:''}${parents.map(r=>`<option value="${esc(r.ref)}" ${r.ref===parent?'selected':''}>${esc(r.title)}${r.data.status&&r.data.status!=='active'?' · '+esc(human(r.data.status)):''}</option>`).join('')}</select></label></details>`:'';
    const targetText=g.target===undefined?'':typeof g.target==='string'?g.target:pretty(g.target);
    goalDetails(id?local?'Edit chat goal':'Edit workspace goal':forChat?'Goal for this chat':'New goal',`${!id?`<p class="goal-intro">${forChat?'Set an outcome for this conversation. Optionally connect it to a shared workspace goal.':'Save an outcome you can work toward across chats.'}</p>`:''}<form id="compose-goal-form" class="form-grid"><label>What do you want to accomplish?<input name="name" required maxlength="2000" value="${esc(g.name||'')}"></label><label><span>Done when <span class="muted">Optional</span></span><textarea name="target" maxlength="5000" rows="3" placeholder="Add specific completion criteria if the goal needs more detail.">${esc(targetText)}</textarea></label>${connection}<div class="inline-actions"><button class="primary">${forChat?'Add to this chat':'Save goal'}</button>${forChat&&workspaceGoalRecords().length?'<button type="button" class="text-button" id="choose-saved-goal">Use an existing workspace goal</button>':''}</div><p id="goal-save-status" role="status"></p>${forChat&&state.chatMeta?.goal_history?.length?`<button type="button" class="text-button" data-goal-manager data-chat-goals="${esc(state.chatMeta.id)}">Goals from this chat</button>`:''}</form>`);
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    $('#compose-goal-form').onsubmit=event=>{event.preventDefault();const form=event.currentTarget;attempt(async()=>{
      if(!same(key,ticket,host)||forChat&&chatKey!==chatScope())return;
      const values=Object.fromEntries(new FormData(form));if(g.target!==undefined&&values.target===targetText)delete values.target;
      if(!savedId){values.status='active';values.scope=local?'chat':'workspace';if(local&&state.chatMeta)values.chat_id=state.chatMeta.id;}
      const button=form.querySelector('button');button.disabled=true;
      try{
        const saved=await api('/api/goals',{business:state.business,action:'save',...(savedId?{id:savedId,basis:data?.goal_basis}:{}),...values});savedId=saved.goal.id;
        if(!same(key,ticket,host)||forChat&&chatKey!==chatScope())return;cache.clear();if(forChat)await setGoal(savedId);await refresh(false,true);paintComposer();
        if(same(key,ticket,host)){if(forChat){$('#detail').close();$('#request').focus();notice('Goal added to this chat.');}else{if(goalTrail.at(-1)?.kind==='goal'&&goalTrail.at(-1)?.id===savedId)goalTrail.pop();returningGoal=true;await openGoal(savedId);}}
      }catch(error){if(same(key,ticket,host))$('#goal-save-status').textContent=humanError(error);}finally{if(button.isConnected)button.disabled=false;}
    });};
  }
  async function changeGoal(id,changes){
    const key=scope(),ticket=state.fileDetailTicket,current=goal(),parent=goalInfo(state.data.records.find(r=>r.ref===current)?.data).workspace_goal_ref;
    await api('/api/goals',{business:state.business,id,action:'save',...(goalPage?.id===id?{basis:goalPage.basis}:{}),...changes});if(key!==scope())return;
    cache.clear();if(state.chatMeta&&(current===id||parent===id))delete state.chatMeta.continuation;
    if(changes.action==='delete'){
      if(state.chatMeta?.goal_id===id)state.chatMeta.goal_id='';if(state.draftGoalId===id)state.draftGoalId='';
      state.contextReferences=refs().filter(r=>!(['goal','record'].includes(r.kind)&&r.id===id));
    }
    await refresh(false,true);if(key!==scope())return;paintComposer();rememberChatDraft();
    if(ticket===state.fileDetailTicket&&$('#detail').open)await openGoal(id);
    if(changes.action==='delete')notice('Goal deleted. Conversations and saved files are kept.');
    else if(changes.action==='restore')notice('Goal restored. Automatic continuation stays off.');
    else if(changes.status)notice((changes.status==='paused'?'Goal paused.':changes.status==='completed'?'Goal completed.':'Goal is active.')+(state.busy&&changes.status!=='active'?' Current work keeps running until you select Stop.':''));
    else if(changes.scope==='workspace')notice('Goal is now available across this workspace.');
    else if(changes.workspace_goal_id==='')notice('Workspace goal disconnected.');
  }
  function goalAction(button,id,changes){
    const label=button.textContent;button.disabled=true;button.setAttribute('aria-busy','true');
    if(label!=='×')button.textContent=changes.action==='delete'?'Deleting…':changes.action==='restore'?'Restoring…':'Updating…';
    attempt(()=>changeGoal(id,changes)).finally(()=>{if(button.isConnected){button.disabled=false;button.textContent=label;button.setAttribute('aria-busy','false');}});
  }
  function confirmDeleteGoal(id,tasks=0){
    const name=state.data.records.find(r=>r.ref===id)?.title||'this goal';
    goalDetails('Delete goal?',`<p>Delete <strong>${esc(name)}</strong>? Conversations and saved files stay available. You can restore the goal from Deleted goals.</p>${tasks?'<p class="small-note">Linked scheduled tasks will need review in their task settings.</p>':''}<div class="inline-actions"><button type="button" class="primary" data-confirm-delete-goal="${esc(id)}">Delete goal</button><button type="button" class="secondary" data-compose-goal="${esc(id)}">Cancel</button></div>`);
  }
  function promoteGoal(button,id){
    if(!goalInfo(state.data.records.find(r=>r.ref===id)?.data).workspace_goal_ref){goalAction(button,id,{scope:'workspace'});return;}
    goalDetails('Make workspace goal?',`<p>This goal will become available across the workspace. Its connection to the existing workspace goal will be removed. Conversations and saved files stay available.</p><div class="inline-actions"><button type="button" class="primary" data-confirm-promote-goal="${esc(id)}">Make workspace goal</button><button type="button" class="secondary" data-compose-goal="${esc(id)}">Cancel</button></div>`);
  }
  async function manageGoals(chatOnly=false,saved={}){
    const key=scope(),chat=typeof chatOnly==='string'?chatOnly:chatOnly?state.chatMeta?.id:'',request=++viewTicket;
    beginGoalPage('manager',chat||'',chat?'Goals from this chat':'All goals',()=>manageGoals(chat,saved),'panel');const ticket=state.fileDetailTicket,host=$('#detail-content');
    const data=await api('/api/goals?'+query({show:'all',scope:'all',...(chat?{chat_id:chat}:{})}));if(request!==viewTicket||!same(key,ticket,host))return;
    const items=[...data.items,...(data.deleted_items||[])];let limit=saved.limit||20;
    goalDetails(chat?'Goals from this chat':'All goals','<p class="goal-intro">Workspace goals are shared outcomes in Business & memory. Chat goals guide individual conversations and can contribute to them.</p><div class="goal-manager-filters"><input id="goal-manager-find" class="search" type="search" aria-label="Find a goal" placeholder="Find a goal…"><label>Scope<select id="goal-manager-scope"><option value="all">All goals</option><option value="workspace">Workspace goals</option><option value="chat">Chat goals</option></select></label><label>Status<select id="goal-manager-show"><option value="current">Current goals</option><option value="completed">Completed goals</option><option value="deleted">Deleted goals</option></select></label></div><div id="goal-manager-list"></div><button type="button" class="text-button" id="goal-manager-more" hidden>Show more goals</button>','panel');
    $('#goal-manager-find').value=saved.q||'';$('#goal-manager-scope').value=saved.scope||'all';$('#goal-manager-show').value=saved.show||'current';
    const paint=()=>{
      const q=$('#goal-manager-find').value.trim().toLowerCase(),show=$('#goal-manager-show').value||'current',which=$('#goal-manager-scope').value||'all';
      Object.assign(saved,{q:$('#goal-manager-find').value,show,scope:which,limit});
      const matches=items.filter(g=>{const gone=!!goalInfo(g).deleted_at;return (which==='all'||which===(goalInfo(g).scope||'workspace'))&&(show==='deleted'?gone:!gone&&(show==='completed'?g.status==='completed':g.status!=='completed'))&&[g.name,typeof g.target==='string'?g.target:''].join(' ').toLowerCase().includes(q);});
      $('#goal-manager-list').innerHTML=matches.slice(0,limit).map(g=>{
        const parent=goalInfo(g).workspace_goal_ref,linked=items.find(p=>p.id===parent),info=parent?'Contributes to '+(linked?linked.name+(goalInfo(linked).deleted_at?' · Deleted':''):'an unavailable workspace goal'):'';
        return `<button type="button" class="row" data-compose-goal="${esc(g.id)}"><span><strong>${esc(g.name)}</strong><small class="row-meta">${goalInfo(g).scope==='chat'?'Chat goal':'Workspace goal'} · ${show==='deleted'?'Deleted':esc(human(g.status||'active'))}</small>${info?`<small class="row-meta">${esc(info)}</small>`:''}</span></button>`;
      }).join('')||empty('No '+(show==='current'?'current':show)+' goals'+(q?' match your search.':'.'));
      $('#goal-manager-more').hidden=matches.length<=limit;
    };
    $('#goal-manager-find').oninput=()=>{limit=20;paint();};$('#goal-manager-show').onchange=()=>{limit=20;paint();};$('#goal-manager-scope').onchange=()=>{limit=20;paint();};$('#goal-manager-more').onclick=()=>{limit+=20;paint();};paint();
  }
  async function linkGoalChat(id){
    const key=scope();beginGoalPage('chat-link',id,'Link a chat',()=>linkGoalChat(id),'panel');
    const ticket=state.fileDetailTicket,host=$('#detail-content'),data=await api('/api/chats?'+query({}));
    if(!same(key,ticket,host))return;
    const chats=data.items.filter(c=>!c.archived);goalDetails('Link a chat','<input id="goal-link-chat-find" type="search" class="search" placeholder="Find a chat…" aria-label="Find a chat to link"><div id="goal-link-chat-list"></div>');
    const paint=()=>{const q=$('#goal-link-chat-find').value.toLowerCase();$('#goal-link-chat-list').innerHTML=chats.filter(c=>c.title.toLowerCase().includes(q)).map(c=>`<button type="button" class="row" data-goal-link-chat="${esc(c.id)}" ${c.goal_id===id?'disabled':''}><span class="row-text"><strong>${esc(c.title)}</strong><small class="row-meta">${esc(appName(c.agent))}${c.goal_id===id?' · Already linked':c.goal_id?' · Replaces its current goal':''}</small></span></button>`).join('')||empty('No matching chats.');};
    $('#goal-link-chat-find').oninput=paint;paint();
    $('#detail-content').onclick=event=>attempt(async()=>{const b=event.target.closest('[data-goal-link-chat]');if(!b||key!==scope())return;b.disabled=true;try{await api('/api/goals',{business:state.business,action:'link_chat',chat_id:b.dataset.goalLinkChat,goal_id:id});if(key!==scope())return;if(state.chatMeta?.id===b.dataset.goalLinkChat)state.chatMeta.goal_id=id;cache.clear();await refresh(false,true);if(key!==scope())return;if(goalTrail.at(-1)?.kind==='goal'&&goalTrail.at(-1)?.id===id)goalTrail.pop();returningGoal=true;await openGoal(id);}finally{if(b.isConnected)b.disabled=false;}});
  }
  async function linkAsset(id){
    const key=scope(),assets=state.data.records.filter(r=>r.type==='Asset');let limit=20;
    beginGoalPage('asset',id,'Link a saved file',()=>linkAsset(id),'panel');
    goalDetails('Link a saved file','<p class="goal-intro">Links the existing file without copying it. If it belongs to another goal, choosing it moves that link here.</p><input id="goal-asset-find" class="search" type="search" aria-label="Find a saved file" placeholder="Find a saved file…"><div id="goal-asset-list"></div><button type="button" class="text-button" id="goal-asset-more" hidden>Show more files</button>','panel');
    const paint=()=>{
      const q=$('#goal-asset-find').value.trim().toLowerCase(),found=assets.filter(a=>(a.title+' '+(a.data.location_reference||'')).toLowerCase().includes(q));
      $('#goal-asset-list').innerHTML=found.slice(0,limit).map(a=>{const owner=a.data.extensions?.businessos?.goal_ref,linked=state.data.records.find(r=>r.ref===owner);return `<button type="button" class="row" data-link-goal-asset="${esc(a.ref)}" ${owner===id?'disabled':''}><span><strong>${esc(a.title)}</strong>${owner?`<small class="row-meta">${owner===id?'Already linked here':esc('Linked to '+(linked?.title||'another goal'))+' · Move link here'}</small>`:''}</span></button>`;}).join('')||empty(q?'No matching saved files.':'No saved files available.');
      $('#goal-asset-more').hidden=found.length<=limit;
    };
    $('#goal-asset-find').oninput=()=>{limit=20;paint();};$('#goal-asset-more').onclick=()=>{limit+=20;paint();};paint();
    $('#detail-content').onclick=event=>attempt(async()=>{const b=event.target.closest('[data-link-goal-asset]');if(!b||key!==scope())return;await api('/api/goals',{business:state.business,action:'link_asset',goal_id:id,asset_id:b.dataset.linkGoalAsset});if(key===scope()){await refresh(false,true);if(key!==scope())return;if(goalTrail.at(-1)?.kind==='goal'&&goalTrail.at(-1)?.id===id)goalTrail.pop();returningGoal=true;await openGoal(id);}});
  }
  async function runGoal(id,budget){
    const key=scope(),basis=goalPage?.basis,record=state.data.records.find(r=>r.ref===id),name=record?.title||'Chat goal',owner=(state.chatList||[]).find(c=>c.id===goalInfo(record?.data).chat_id),connection=owner?{kind:owner.agent,model:owner.model||'',effort:owner.effort||''}:goalConnection();beginGoalPage('native-run',id,'Work toward goal',()=>runGoal(id,budget),'panel');
    goalDetails('Work toward goal',`<p><strong>${esc(name)}</strong></p><p class="row-meta">${esc(appName(connection.kind))}${connection.model?' · '+esc(connection.model):''}</p><p>Your AI app will work toward this goal until it finishes or you stop it. Its native limits and permissions apply.</p><form id="native-goal-form" class="form-grid">${budget?'<label><span>Token budget <span class="muted">Optional</span></span><input name="token_budget" type="number" min="1" step="1" placeholder="Use the AI app’s default"></label>':''}<button type="submit" class="primary">Start work</button><p id="native-goal-status" role="status"></p></form>`);
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    $('#native-goal-form').onsubmit=event=>{event.preventDefault();const form=event.currentTarget;attempt(async()=>{
      if(!same(key,ticket,host))return;const button=form.querySelector('button');button.disabled=true;
      try{const values=Object.fromEntries(new FormData(form)),data=await api('/api/goals',{business:state.business,action:'native_start',id,basis,connection,...(values.token_budget?{token_budget:Number(values.token_budget)}:{})});if(key!==scope())return;await openShellChat(data.chat_id);}
      catch(error){if(same(key,ticket,host))$('#native-goal-status').textContent=humanError(error);}
      finally{if(button.isConnected)button.disabled=false;}
    });};
  }
  async function continuation(){
    if(!state.chatMeta||!goal())return;const key=chatScope(),c=state.chatMeta,p=c.continuation||{},supported=['pi','omp'].includes(c.agent);
    details('Retry settings',`<form id="continuation-form" class="form-grid"><label>Native retries<select name="mode"><option value="manual" ${p.mode!=='native'?'selected':''}>Continue manually</option>${supported?`<option value="native" ${p.mode==='native'?'selected':''}>Allow native retries until expiry</option>`:''}</select></label>${supported?`<label>Allow retries until<input name="until" type="datetime-local" value="${new Date(p.until?p.until*1000:Date.now()+86400000).toLocaleString('sv-SE').slice(0,16).replace(' ','T')}"></label>`:''}<p class="small-note">${supported?'Uses retries already enabled by your native app. It may end the request instead of waiting for a quota reset.':'This connection requires manual continuation after quota interruptions.'} AURA and the native connection must remain running. Stop cancels automatic continuation.</p><button class="primary">Save</button><p id="continuation-status" role="status"></p></form>`);
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
    const key=scope(),data=await api('/api/goals?'+query({show:'all'}));if(key!==scope()||!host.isConnected)return;
    host.innerHTML=`<label>Workspace goal<select id="task-goal"><option value="">No workspace goal</option>${[...data.items,...(data.deleted_items||[])].filter(g=>(!goalInfo(g).deleted_at&&(g.status||'active')==='active')||data.task_links[task.id]===g.id).map(g=>`<option value="${esc(g.id)}" ${data.task_links[task.id]===g.id?'selected':''}>${esc(g.name)}${goalInfo(g).deleted_at?' · Deleted':g.status&&g.status!=='active'?' · '+esc(human(g.status)):''}</option>`).join('')}</select></label><p class="small-note">Selecting a goal updates the task’s native instructions through its existing AI connection.</p><button type="button" class="secondary" id="task-goal-update">Update goal instructions</button><p id="task-goal-status" role="status"></p>`;
    const update=()=>attempt(async()=>{
      const select=$('#task-goal'),button=$('#task-goal-update'),id=select.value;select.disabled=true;button.disabled=true;
      try{await scheduleOperation({action:'request',id:task.id,app:task.owner,goal_id:id,...(!id?{remove_goal:true}:{}),request:id?'Associate this task with the selected AURA goal. Preserve its timing, model, permissions and business work; add a current-goal preflight check to its instructions.':'Remove this task’s AURA goal association.'});}
      finally{if(select.isConnected)select.disabled=false;if(button.isConnected)button.disabled=false;}
      if(key===scope()&&host.isConnected)$('#task-goal-status').textContent=state.scheduleJob?.message||'Updating the native task…';
    });
    const saved=data.task_links[task.id]||'',active=new Set(data.items.filter(g=>!goalInfo(g).deleted_at&&(g.status||'active')==='active').map(g=>g.id));
    const ready=()=>{const id=$('#task-goal').value;$('#task-goal-update').disabled=id?!active.has(id):!saved;};
    $('#task-goal').onchange=ready;$('#task-goal-update').onclick=update;ready();
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
    if(b.hasAttribute('data-compose-clear-goal'))attempt(async()=>{await setGoal('');if($('#detail').open)$('#detail').close();notice('Goal removed from this chat. Its history is still available.');});
    if(b.id==='choose-goal')attempt(chatGoal);
    if(b.id==='choose-saved-goal')attempt(()=>choose('goal','',true));
    if(b.dataset.composeGoal)attempt(()=>openGoal(b.dataset.composeGoal));
    if(b.dataset.goalEdit)attempt(()=>editGoal(b.dataset.goalEdit));
    if(b.dataset.goalAsset)attempt(()=>linkAsset(b.dataset.goalAsset));
    if(b.dataset.goalUnlinkAsset)attempt(async()=>{const key=scope();await api('/api/goals',{business:state.business,action:'link_asset',goal_id:'',asset_id:b.dataset.goalUnlinkAsset});if(key===scope()){await refresh(false,true);if(key===scope())await openGoal(b.dataset.goalId);}});
    if(b.dataset.goalOpenFile)attempt(()=>openRelatedGoal('file',b.dataset.goalOpenFile));
    if(b.dataset.goalOpenTask)attempt(()=>openRelatedGoal('task',b.dataset.goalOpenTask));
    if(b.dataset.goalState)goalAction(b,b.dataset.goalState,{status:b.dataset.goalStatus});
    if(b.dataset.goalPromote)promoteGoal(b,b.dataset.goalPromote);
    if(b.dataset.confirmPromoteGoal)goalAction(b,b.dataset.confirmPromoteGoal,{scope:'workspace'});
    if(b.dataset.goalUnlinkWorkspace)goalAction(b,b.dataset.goalUnlinkWorkspace,{workspace_goal_id:''});
    if(b.dataset.goalDelete)confirmDeleteGoal(b.dataset.goalDelete,Number(b.dataset.linkedTasks)||0);
    if(b.dataset.confirmDeleteGoal)goalAction(b,b.dataset.confirmDeleteGoal,{action:'delete'});
    if(b.dataset.goalRestore)goalAction(b,b.dataset.goalRestore,{action:'restore'});
    if(b.hasAttribute('data-goal-back'))attempt(backGoal);
    if(b.hasAttribute('data-goal-manager'))attempt(()=>manageGoals(b.dataset.chatGoals||false));
    if(b.hasAttribute('data-new-chat-goal'))attempt(()=>editGoal('',true));
    if(b.dataset.goalUse)attempt(async()=>{await setGoal(b.dataset.goalUse);$('#detail').close();});
    if(b.id==='chat-continuation')attempt(continuation);
    if(b.hasAttribute('data-compose-new-goal'))attempt(()=>editGoal('',true));
    if(b.dataset.goalRun)attempt(()=>runGoal(b.dataset.goalRun,b.dataset.goalBudget==='true'));
    if(b.dataset.goalStart)attempt(async()=>{const id=b.dataset.goalStart;await newShellChat({text:'',files:[],references:[],goal_id:id,connection:composerConnection()});notice('Goal attached. Describe what you want to work on.');});
    if(b.dataset.goalLink)attempt(()=>linkGoalChat(b.dataset.goalLink));
    if(b.dataset.goalConnect&&state.view==='home')attempt(async()=>{const id=b.dataset.goalConnect,current=state.data.records.find(r=>r.ref===goal())?.data;if(current&&goalInfo(current).scope==='chat')await changeGoal(current.id,{workspace_goal_id:id});else if(state.chatMeta){await setGoal(id);$('#detail').close();}else await newShellChat({text:'Help me make the next useful step toward this goal. Check existing work first.',files:[],references:[],goal_id:id,connection:composerConnection()});});
    if(b.dataset.goalTask){$('#detail').close();state.scheduleDraft={name:'',description:'',when:'',goal_id:b.dataset.goalTask};state.scheduleAdding=true;state.view='tools';attempt(async()=>{await render();recordShellRoute();await renderShell();});}
    if(b.dataset.composeAssistant)attempt(()=>window.auraWork.startAssistant(b.dataset.composeAssistant,{text:$('#request').value,files:state.selectedFiles||[],references:refs(),goal_id:newChatGoal(),connection:composerConnection()}));
  });
  $('#composer-menu').setAttribute('aria-label','Commands and context');
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
  if(state.hydrated)queueMicrotask(()=>{state.formattedSource=null;showMessages();});
  async function sync(){
    paintComposer();
    const page=goalPage,record=state.data?.records?.find(r=>r.ref===page?.id);
    if(page?.kind!=='goal'||page.ticket!==state.fileDetailTicket||!$('#detail').open||!record||!page.recordVersion||page.recordVersion===goalVersion(record.data))return;
    const scroll=$('#detail-content').scrollTop;await openGoal(page.id);
    if(goalPage?.kind==='goal'&&goalPage.id===page.id&&$('#detail').open)$('#detail-content').scrollTop=scroll;
  }
  return {sync,render:paintComposer,add,actions,draft,restore,choose,openGoal,editGoal,closeMenu,assignTask,prepareContinuation,reuse,manageGoals};
})();
