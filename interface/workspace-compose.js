/* Context selection, message reuse and goals share the existing composer and APIs. */
'use strict';
window.auraCompose=(()=>{
  let lookupTicket=0,viewTicket=0,inlineItems=[],active=-1,inlineToken=null,timer=null;
  const cache=new Map(),scope=()=>JSON.stringify([state.data?.workspace,state.business]),refs=()=>state.contextReferences||[];
  const goal=()=>{const id=state.chatMeta?.goal_id||state.draftGoalId||'',saved=state.data?.records?.find(r=>r.ref===id)?.data;return goalInfo(saved).deleted_at?'':id;};
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
  const kinds={file:'File',record:'Saved context',goal:'Goal',library:'Library',assistant:'Assistant',result:'Saved result'};
  const shortcuts=[{id:'new',label:'New chat',description:'Keep this draft and open a new chat'},{id:'attach',label:'Attach context',description:'Files, saved work and operating knowledge'},{id:'assistant',label:'Choose assistant',description:'Start a chat with a named assistant'},{id:'goal',label:'Chat goal',description:'Set what this chat is working toward'}];

  async function lookup(q='',kind='',assistant=''){
    const key=scope(),id=JSON.stringify([key,q.toLowerCase(),kind,assistant]),prior=cache.get(id);
    if(prior&&Date.now()-prior.at<5000)return prior.data;
    const data=await api('/api/context?'+query({q,kind,limit:30,...(assistant?{assistant}:{})}));
    if(key!==scope())return null;cache.set(id,{at:Date.now(),data});while(cache.size>30)cache.delete(cache.keys().next().value);return data;
  }
  function paintComposer(){
    const host=$('#composer-contexts');if(!host)return;
    const items=refs(),goalId=goal(),saved=state.data?.records?.find(r=>r.ref===goalId),info=goalInfo(saved?.data),name=saved?.title||'Selected goal',local=info.scope==='chat',parent=state.data?.records?.find(r=>r.ref===info.workspace_goal_ref&&!goalInfo(r.data).deleted_at);
    host.hidden=!items.length&&!goalId;
    const markup=(goalId?`<span class="context-chip goal-chip"><button type="button" data-compose-goal="${esc(goalId)}" title="Open goal">${local?'Chat goal':'Workspace goal'}: ${esc(name)}</button><button type="button" data-compose-clear-goal aria-label="Remove goal from this chat">×</button></span>`:'')+(goalId&&parent?`<span class="context-chip"><button type="button" data-compose-goal="${esc(parent.ref)}">Workspace goal: ${esc(parent.title)}</button><button type="button" data-goal-unlink-workspace="${esc(goalId)}" aria-label="Disconnect workspace goal">×</button></span>`:'')+items.map((r,i)=>`<span class="context-chip"><button type="button" data-compose-inspect="${i}" title="Review selected context">${esc(r.label||r.id)}</button><button type="button" data-compose-remove="${i}" aria-label="Remove ${esc(r.label||r.id)}">×</button></span>`).join('');
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
    details('Choose assistant',data.items.map(p=>`<button type="button" class="row" data-compose-assistant="${esc(p.id)}"><strong>${esc(p.name)}</strong></button>`).join('')||empty('Create an assistant from Assistants first.'));
  }
  function actions(row,index){
    if(row.role!=='user')return '';
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
    if(state.chatMeta){state.goalSetting=true;try{await api('/api/goals',{business:state.business,action:'link_chat',chat_id:state.chatMeta.id,goal_id:id});if(key!==chatScope())return;state.chatMeta.goal_id=id||'';delete state.chatMeta.continuation;}finally{state.goalSetting=false;}}
    else state.draftGoalId=id||'';
    rememberChatDraft();paintComposer();
  }
  async function openGoal(id){
    const key=scope(),request=++viewTicket;details('Goal','<p role="status">Reading goal…</p>','context');
    const loading=state.fileDetailTicket,host=$('#detail-content'),data=await api('/api/goals?'+query({id}));if(request!==viewTicket||!same(key,loading,host))return;
    const g=data.goal,info=goalInfo(g),local=data.scope==='chat'||info.scope==='chat',status=g.status||'active';
    if(data.deleted||info.deleted_at){details(g.name,`<p>This goal was deleted. Its conversations and saved work are still available.</p><div class="inline-actions"><button type="button" class="primary" data-goal-restore="${esc(id)}">Restore goal</button><button type="button" class="text-button" data-goal-manager>Manage goals</button></div>`,'context');return;}
    const current=goal()===id,owner=info.chat_id,ownerAvailable=data.chats.some(c=>c.id===owner);
    const work=local?(owner&&owner!==state.chatMeta?.id?(ownerAvailable?`<button type="button" class="text-button" data-chat="${esc(owner)}">Open original chat</button>`:''):!current?`<button type="button" class="text-button" data-goal-use="${esc(id)}">Use in this chat</button>`:''):`<button type="button" class="text-button" data-goal-connect="${esc(id)}">${state.chatMeta?'Connect to this chat':'Start a chat toward this goal'}</button>`;
    const toolbar=`<div class="inline-actions goal-actions"><button type="button" class="primary" data-goal-state="${esc(id)}" data-goal-status="${status==='active'?'completed':'active'}">${status==='completed'?'Reopen goal':status==='paused'?'Resume goal':'Complete goal'}</button><button type="button" class="secondary" data-goal-edit="${esc(id)}">Edit goal</button>${work}</div><details class="goal-options"><summary>More options</summary><div class="inline-actions">${status==='active'?`<button type="button" class="text-button" data-goal-state="${esc(id)}" data-goal-status="paused">Pause goal</button>`:''}${current?'<button type="button" class="text-button" data-compose-clear-goal>Remove from this chat</button>':''}${local?`<button type="button" class="text-button" data-goal-promote="${esc(id)}">Make workspace goal</button>`:''}${current&&status==='active'?'<button type="button" class="text-button" id="chat-continuation">Continuation settings</button>':''}<button type="button" class="text-button danger" data-goal-delete="${esc(id)}" data-linked-tasks="${Object.keys(data.task_links||{}).length}">Delete goal</button><button type="button" class="text-button" data-goal-manager ${local&&ownerAvailable?`data-chat-goals="${esc(owner)}"`:''}>${local&&ownerAvailable?'Chat goal history':'Manage goals'}</button></div></details>`;
    details(g.name,`${toolbar}<p class="row-meta">${local?'Chat goal':'Workspace goal'} · ${esc(human(status))}</p>${g.target!==undefined?`<div class="goal-outcome"><h3>Done when</h3><p>${esc(pretty(g.target))}</p></div>`:''}${data.workspace_goal?`<p class="goal-parent">Contributes to <button type="button" class="text-button" data-compose-goal="${esc(data.workspace_goal.id)}">${esc(data.workspace_goal.name)}</button></p>`:info.workspace_goal_ref?'<p class="small-note">The connected workspace goal is unavailable. Edit this goal to change or remove its connection.</p>':''}${local&&current?'<button type="button" class="text-button" data-new-chat-goal>Set a different chat goal</button>':''}<h3>Related conversations</h3><label class="goal-chat-search" ${data.chats.length<=20?'hidden':''}>Find linked work<input id="goal-chat-find" type="search" class="search" placeholder="Search chats and next steps…"></label><div id="goal-chats"></div><button type="button" class="text-button" id="goal-chats-more" hidden>Show more chats</button><h3>Saved results</h3>${data.assets.map(a=>`<button type="button" class="row" data-file="asset/${esc(a.id)}">${esc(a.name)}</button><button type="button" class="text-button" data-goal-unlink-asset="${esc(a.id)}" data-goal-id="${esc(id)}">Unlink</button>`).join('')||'<p class="small-note">No saved results linked yet.</p>'}<button type="button" class="text-button" data-goal-asset="${esc(id)}">Link a saved file</button>${!local?`<h3>Recurring tasks</h3><div id="goal-tasks">Reading linked tasks…</div><button type="button" class="text-button" data-goal-task="${esc(id)}">Add recurring task</button>`:''}`,'context');
    const ticket=state.fileDetailTicket;let limit=20;
    const paintChats=()=>{const q=$('#goal-chat-find').value.trim().toLocaleLowerCase(),rows=data.chats.filter(c=>(c.title+' '+(c.summary||'')).toLocaleLowerCase().includes(q));$('#goal-chats').innerHTML=rows.slice(0,limit).map(c=>`<button type="button" class="row" data-chat="${esc(c.id)}"><span><strong>${esc(c.title)}</strong><small class="row-meta">${esc(data.running_chats.includes(c.id)?'Working':c.work_state==='waiting_for_usage'?'Paused after usage limit':c.status==='working'?'Last observed working':c.status==='complete'?'Reply ready':human(c.status||'Saved'))}${c.summary?' · '+esc(c.summary):''}</small></span></button>`).join('')||empty(q?'No matching linked chats.':'No chats linked yet.');$('#goal-chats-more').hidden=rows.length<=limit;};
    $('#goal-chat-find').oninput=()=>{limit=20;paintChats();};$('#goal-chats-more').onclick=()=>{limit+=20;paintChats();};paintChats();
    if(local)return;
    try{const tasks=await api('/api/schedules');if(!same(key,ticket,host))return;state.schedules=tasks;
      $('#goal-tasks').innerHTML=tasks.items.filter(t=>data.task_links[t.id]===id).map(t=>`<button type="button" class="row" data-schedule="${esc(t.id)}">${esc(t.name)}${t.description?.includes(data.goal_basis)?'':'<small class="row-meta">Review goal instructions</small>'}</button>`).join('')||empty('No recurring tasks linked yet.');
      if(tasks.notes?.length)$('#goal-tasks').insertAdjacentHTML('beforeend',`<p class="small-note">${tasks.notes.map(esc).join(' ')}</p>`);
    }catch(error){if(same(key,ticket,host))$('#goal-tasks').textContent=error.message;}
  }
  async function chatGoal(){
    if(goal())return openGoal(goal());
    return editGoal('',true);
  }
  async function editGoal(id='',forChat=false){
    const chatKey=chatScope();let savedId=id;
    const key=scope(),request=++viewTicket;details(id?'Edit goal':forChat?'Goal for this chat':'New workspace goal','<p role="status">Reading goal…</p>');
    const loading=state.fileDetailTicket,loadingHost=$('#detail-content');
    const data=id?await api('/api/goals?'+query({id})):null;if(request!==viewTicket||!same(key,loading,loadingHost))return;
    const g=data?.goal||{},info=goalInfo(g),local=id?info.scope==='chat':forChat;
    const current=state.data.records.find(r=>r.ref===goal())?.data;
    const parent=info.workspace_goal_ref||(!id&&forChat&&current?(goalInfo(current).scope==='chat'?goalInfo(current).workspace_goal_ref||'':goal()):'');
    const parents=workspaceGoalRecords(true).filter(r=>(r.data.status||'active')==='active'||r.ref===parent);
    const connection=local?`<details class="goal-connection" ${parent?'open':''}><summary>Connect to a workspace goal <span class="muted">Optional</span></summary><label>Workspace goal<select name="workspace_goal_id"><option value="">No connection</option>${parent&&!parents.some(r=>r.ref===parent)?`<option value="${esc(parent)}" selected>Unavailable workspace goal</option>`:''}${parents.map(r=>`<option value="${esc(r.ref)}" ${r.ref===parent?'selected':''}>${esc(r.title)}${r.data.status&&r.data.status!=='active'?' · '+esc(human(r.data.status)):''}</option>`).join('')}</select></label></details>`:'';
    const simple=g.target===undefined||typeof g.target==='string'||typeof g.target==='number';
    details(id?local?'Edit chat goal':'Edit workspace goal':forChat?'Goal for this chat':'New workspace goal',`<form id="compose-goal-form" class="form-grid"><label>What do you want to accomplish?<input name="name" required maxlength="2000" value="${esc(g.name||'')}"></label>${simple?`<label><span>What does done look like? <span class="muted">Optional</span></span><textarea name="target" maxlength="5000" rows="3">${esc(g.target??'')}</textarea></label>`:`<p>${esc(pretty(g.target))}</p>`}${connection}<div class="inline-actions"><button class="primary">${forChat?'Add to this chat':'Save goal'}</button>${forChat?'<button type="button" class="text-button" id="choose-saved-goal">Use a workspace goal only</button>':''}</div><p id="goal-save-status" role="status"></p>${forChat&&state.chatMeta?.goal_history?.length?`<button type="button" class="text-button" data-goal-manager data-chat-goals="${esc(state.chatMeta.id)}">Goals from this chat</button>`:''}</form>`);
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    $('#compose-goal-form').onsubmit=event=>{event.preventDefault();const form=event.currentTarget;attempt(async()=>{
      if(!same(key,ticket,host)||forChat&&chatKey!==chatScope())return;
      const values=Object.fromEntries(new FormData(form));if(g.target!==undefined&&values.target===String(g.target))delete values.target;
      if(!savedId){values.status='active';values.scope=local?'chat':'workspace';if(local&&state.chatMeta)values.chat_id=state.chatMeta.id;}
      const button=form.querySelector('button');button.disabled=true;
      try{
        const saved=await api('/api/goals',{business:state.business,action:'save',...(savedId?{id:savedId}:{}),...values});savedId=saved.goal.id;
        if(!same(key,ticket,host)||forChat&&chatKey!==chatScope())return;cache.clear();if(forChat)await setGoal(savedId);await refresh();paintComposer();
        if(same(key,ticket,host)){if(forChat){$('#detail').close();$('#request').focus();notice('Goal added to this chat.');}else await openGoal(savedId);}
      }catch(error){if(same(key,ticket,host))$('#goal-save-status').textContent=error.message;}finally{if(button.isConnected)button.disabled=false;}
    });};
  }
  async function changeGoal(id,changes){
    const key=scope(),ticket=state.fileDetailTicket,current=goal(),parent=goalInfo(state.data.records.find(r=>r.ref===current)?.data).workspace_goal_ref;
    await api('/api/goals',{business:state.business,id,action:'save',...changes});if(key!==scope())return;
    cache.clear();if(state.chatMeta&&(current===id||parent===id))delete state.chatMeta.continuation;
    if(changes.action==='delete'){
      if(state.chatMeta?.goal_id===id)state.chatMeta.goal_id='';if(state.draftGoalId===id)state.draftGoalId='';
      state.contextReferences=refs().filter(r=>!(['goal','record'].includes(r.kind)&&r.id===id));
    }
    await refresh();if(key!==scope())return;paintComposer();rememberChatDraft();
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
    details('Delete goal?',`<p>Delete <strong>${esc(name)}</strong>? Conversations and saved files stay available. You can restore the goal from Deleted goals.</p>${tasks?'<p class="small-note">Linked recurring tasks will need review in their task settings.</p>':''}<div class="inline-actions"><button type="button" class="primary" data-confirm-delete-goal="${esc(id)}">Delete goal</button><button type="button" class="secondary" data-compose-goal="${esc(id)}">Cancel</button></div>`);
  }
  function promoteGoal(button,id){
    if(!goalInfo(state.data.records.find(r=>r.ref===id)?.data).workspace_goal_ref){goalAction(button,id,{scope:'workspace'});return;}
    details('Make workspace goal?',`<p>This goal will become available across the workspace. Its connection to the existing workspace goal will be removed. Conversations and saved files stay available.</p><div class="inline-actions"><button type="button" class="primary" data-confirm-promote-goal="${esc(id)}">Make workspace goal</button><button type="button" class="secondary" data-compose-goal="${esc(id)}">Cancel</button></div>`);
  }
  async function manageGoals(chatOnly=false){
    const key=scope(),chat=typeof chatOnly==='string'?chatOnly:chatOnly?state.chatMeta?.id:'',request=++viewTicket;
    details(chat?'Goals from this chat':'Manage goals','<p role="status">Reading goals…</p>');const ticket=state.fileDetailTicket,host=$('#detail-content');
    const data=await api('/api/goals?'+query({show:'all',scope:'all',...(chat?{chat_id:chat}:{})}));if(request!==viewTicket||!same(key,ticket,host))return;
    const items=[...data.items,...(data.deleted_items||[])];let limit=20;
    host.innerHTML='<div class="goal-manager-filters"><input id="goal-manager-find" class="search" type="search" aria-label="Find a goal" placeholder="Find a goal…"><label>Show<select id="goal-manager-show"><option value="current">Current goals</option><option value="completed">Completed goals</option><option value="deleted">Deleted goals</option></select></label></div><div id="goal-manager-list"></div><button type="button" class="text-button" id="goal-manager-more" hidden>Show more goals</button>';
    const paint=()=>{
      const q=$('#goal-manager-find').value.trim().toLowerCase(),show=$('#goal-manager-show').value||'current';
      const matches=items.filter(g=>{const gone=!!goalInfo(g).deleted_at;return (show==='deleted'?gone:!gone&&(show==='completed'?g.status==='completed':g.status!=='completed'))&&[g.name,typeof g.target==='string'?g.target:''].join(' ').toLowerCase().includes(q);});
      $('#goal-manager-list').innerHTML=matches.slice(0,limit).map(g=>`<button type="button" class="row" data-compose-goal="${esc(g.id)}"><span><strong>${esc(g.name)}</strong><small class="row-meta">${goalInfo(g).scope==='chat'?'Chat goal':'Workspace goal'} · ${show==='deleted'?'Deleted':esc(human(g.status||'active'))}</small></span></button>`).join('')||empty('No '+(show==='current'?'current':show)+' goals'+(q?' match your search.':'.'));
      $('#goal-manager-more').hidden=matches.length<=limit;
    };
    $('#goal-manager-find').oninput=()=>{limit=20;paint();};$('#goal-manager-show').onchange=()=>{limit=20;paint();};$('#goal-manager-more').onclick=()=>{limit+=20;paint();};paint();
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
    const key=scope(),data=await api('/api/goals?'+query({show:'all'}));if(key!==scope()||!host.isConnected)return;
    host.innerHTML=`<label>Workspace goal<select id="task-goal"><option value="">No workspace goal</option>${[...data.items,...(data.deleted_items||[])].filter(g=>(!goalInfo(g).deleted_at&&(g.status||'active')==='active')||data.task_links[task.id]===g.id).map(g=>`<option value="${esc(g.id)}" ${data.task_links[task.id]===g.id?'selected':''}>${esc(g.name)}${goalInfo(g).deleted_at?' · Deleted':g.status&&g.status!=='active'?' · '+esc(human(g.status)):''}</option>`).join('')}</select></label><p class="small-note">Selecting a goal updates the task’s native instructions through its existing AI connection.</p><button type="button" class="secondary" id="task-goal-update">Update goal instructions</button><p id="task-goal-status" role="status"></p>`;
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
    if(b.hasAttribute('data-compose-clear-goal'))attempt(async()=>{await setGoal('');if($('#detail').open)$('#detail').close();notice('Goal removed from this chat. Its history is still available.');});
    if(b.id==='choose-goal')attempt(chatGoal);
    if(b.id==='choose-saved-goal')attempt(()=>choose('goal','',true));
    if(b.dataset.composeGoal)attempt(()=>openGoal(b.dataset.composeGoal));
    if(b.dataset.goalEdit)attempt(()=>editGoal(b.dataset.goalEdit));
    if(b.dataset.goalAsset)attempt(()=>linkAsset(b.dataset.goalAsset));
    if(b.dataset.goalUnlinkAsset)attempt(async()=>{const key=scope();await api('/api/goals',{business:state.business,action:'link_asset',goal_id:'',asset_id:b.dataset.goalUnlinkAsset});if(key===scope())await openGoal(b.dataset.goalId);});
    if(b.dataset.goalState)goalAction(b,b.dataset.goalState,{status:b.dataset.goalStatus});
    if(b.dataset.goalPromote)promoteGoal(b,b.dataset.goalPromote);
    if(b.dataset.confirmPromoteGoal)goalAction(b,b.dataset.confirmPromoteGoal,{scope:'workspace'});
    if(b.dataset.goalUnlinkWorkspace)goalAction(b,b.dataset.goalUnlinkWorkspace,{workspace_goal_id:''});
    if(b.dataset.goalDelete)confirmDeleteGoal(b.dataset.goalDelete,Number(b.dataset.linkedTasks)||0);
    if(b.dataset.confirmDeleteGoal)goalAction(b,b.dataset.confirmDeleteGoal,{action:'delete'});
    if(b.dataset.goalRestore)goalAction(b,b.dataset.goalRestore,{action:'restore'});
    if(b.hasAttribute('data-goal-manager'))attempt(()=>manageGoals(b.dataset.chatGoals||false));
    if(b.hasAttribute('data-new-chat-goal'))attempt(()=>editGoal('',true));
    if(b.dataset.goalUse)attempt(async()=>{await setGoal(b.dataset.goalUse);$('#detail').close();});
    if(b.id==='chat-continuation')attempt(continuation);
    if(b.hasAttribute('data-compose-new-goal'))attempt(()=>editGoal('',true));
    if(b.dataset.goalConnect)attempt(async()=>{const id=b.dataset.goalConnect,current=state.data.records.find(r=>r.ref===goal())?.data;if(current&&goalInfo(current).scope==='chat')await changeGoal(current.id,{workspace_goal_id:id});else if(state.chatMeta){await setGoal(id);$('#detail').close();}else await newShellChat({text:'Help me make the next useful step toward this goal. Check existing work first.',files:[],references:[],goal_id:id,connection:composerConnection()});});
    if(b.dataset.goalTask){state.scheduleDraft={name:'',description:'',when:'',goal_id:b.dataset.goalTask};state.scheduleAdding=true;state.view='tools';attempt(async()=>{await render();recordShellRoute();});}
    if(b.dataset.composeAssistant)attempt(()=>window.auraWork.startAssistant(b.dataset.composeAssistant,{text:$('#request').value,files:state.selectedFiles||[],references:refs(),goal_id:newChatGoal(),connection:composerConnection()}));
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
  if(state.hydrated)queueMicrotask(()=>{state.formattedSource=null;showMessages();});
  return {render:paintComposer,actions,draft,restore,choose,openGoal,editGoal,closeMenu,assignTask,prepareContinuation,reuse,manageGoals};
})();
