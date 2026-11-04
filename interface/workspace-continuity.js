/* Local continuity over shared operations. Presentation never owns a native grant. */
'use strict';
window.auraContinuity=(()=>{
  let requestScope='',requestKey='',viewTicket=0,viewDetailTicket=0;
  const drafts=new Map();
  const scope=()=>JSON.stringify([state.data?.workspace,state.business]);
  const params=extra=>new URLSearchParams({business:state.business,...extra});
  const current=(key,ticket,host)=>key===scope()&&ticket===viewTicket&&viewDetailTicket===state.fileDetailTicket&&host?.isConnected&&$('#detail').open;
  let recoveryTicket=0,recoveryPending='',recoveryLast='',recoveryAt=0,recoveryError='',recoveryMarkup='';

  function acceptRecovery(result){
    state.recovery=result.recovery||null;
    state.needsCheck=!state.busy&&(result.chat?.status==='working'||state.recovery&&['running_elsewhere','interrupted','uncertain'].includes(state.recovery.state));
  }
  function renderRecovery(){
    let host=$('#chat-reconnect');if(!host){host=document.createElement('div');host.id='chat-reconnect';host.className='chat-recovery';host.setAttribute('role','status');$('#request-recovery').after(host);}
    if(host.className!=='chat-recovery')host.className='chat-recovery';
    host.setAttribute('role','status');
    const key=chatScope(),r=state.recovery,pending=recoveryPending===key;
    const show=!state.busy&&(state.needsCheck||state.connectionInterrupted||pending);
    host.hidden=!show;if(!show){host.innerHTML='';recoveryMarkup='';return;}
    const message=pending?'Checking the latest work…':recoveryError||r?.message||'The connection ended. Check the latest work before continuing.';
    const action=!pending&&r?.can_continue?`<button type="button" class="secondary" id="recovery-continue">${r.state==='uncertain'?'I’ve reviewed · Continue':'Continue chat'}</button>`:'';
    const html=`<p>${esc(message)}</p><div class="inline-actions">${action}<button type="button" class="text-button" id="recovery-check" ${pending?'disabled':''}>${pending?'Checking…':state.connectionInterrupted?'Reconnect':'Check again'}</button></div>`;
    if(html!==recoveryMarkup){const focus=host.contains(document.activeElement)?document.activeElement.id:'';host.innerHTML=html;recoveryMarkup=html;if(focus)$('#'+focus)?.focus({preventScroll:true});}
    $('#request-recovery').hidden=true;
  }
  async function checkRecovery(force=false){
    if(state.busy||state.navigating||!state.chatMeta||document.hidden)return;
    const key=chatScope();if(recoveryPending===key||!force&&recoveryLast===key&&Date.now()-recoveryAt<10000)return;
    if(!force&&!state.needsCheck&&!state.connectionInterrupted&&!['working','error'].includes(state.chatMeta.status))return;
    const ticket=++recoveryTicket;recoveryPending=key;recoveryError='';renderRecovery();
    try{
      const result=await api('/api/chats/recovery?'+params({id:state.chatMeta.id}));
      if(key!==chatScope()||ticket!==recoveryTicket||state.busy||result.workspace!==state.data.workspace)return;
      const view=$('#conversation'),top=view.scrollTop,follow=view.scrollHeight-view.clientHeight-top<48;
      state.chat=result.messages;state.chatMeta=result.chat;state.liveJob=result.job;state.busy=result.job?.status==='working';state.activeJob=state.busy?result.job:null;
      state.connectionInterrupted=false;acceptRecovery(result);recoveryLast=key;recoveryAt=Date.now();
      showMessages(follow);if(!follow)view.scrollTop=top;chatControls();renderShell();
      if(state.busy)attempt(()=>pollJob(result.job));else if(result.recovery.state==='complete')taskStatus('Recovered reply');else if(state.needsCheck)taskStatus('');
    }catch{if(key===chatScope()&&ticket===recoveryTicket)recoveryError='The latest work couldn’t be checked. Reopen Aura or your AI app, then try again.';}
    finally{if(ticket===recoveryTicket){recoveryPending='';renderRecovery();}}
  }
  async function continueRecovery(){
    const key=chatScope(),r=state.recovery;if(!r?.can_continue||recoveryPending===key)return;
    const ticket=++recoveryTicket;recoveryPending=key;recoveryError='';renderRecovery();
    try{
      const result=await api('/api/chats/recovery',{business:state.business,id:state.chatMeta.id,action:'prepare',revision:r.revision,reviewed:r.state==='uncertain'});
      if(key!==chatScope()||ticket!==recoveryTicket||state.busy||result.workspace!==state.data.workspace)return;
      state.chat=result.messages;state.chatMeta=result.chat;state.connectionInterrupted=false;acceptRecovery(result);
      if(!$('#request').value.trim()){
        $('#request').value=result.draft;
        if(result.context&&!(state.selectedFiles?.length||state.contextReferences?.length)){
          state.selectedFiles=result.context.files||[];state.contextReferences=result.context.references||[];renderComposerFiles();
        }
      }
      rememberChatDraft();showMessages();chatControls();renderShell();taskStatus('Ready to continue');$('#request').focus();
    }catch(error){if(key===chatScope()&&ticket===recoveryTicket)recoveryError=error.status===400?'This chat changed. Check its latest work before continuing.':'Aura couldn’t reconnect. Try again when it’s available.';}
    finally{if(ticket===recoveryTicket){recoveryPending='';renderRecovery();}}
  }

  function renderRequests(){
    const host=$('#native-requests');if(!host)return;
    const job=state.liveJob,chat=state.chatMeta?.id||'';
    const key=JSON.stringify([scope(),chat,job?.id]);
    const rows=job?.chat_id===chat&&job?.workspace===state.data?.workspace?(job.requests||[]):[];
    const signature=JSON.stringify(rows);
    if(key===requestScope&&signature===requestKey)return;
    const active=document.activeElement,form=active?.closest?.('form[data-native-request]');
    const focus=key===requestScope&&form&&host.contains(form)?{id:form.dataset.nativeRequest,index:[...form.querySelectorAll('input,textarea,button')].indexOf(active),start:active.selectionStart,end:active.selectionEnd}:null;
    host.querySelectorAll('form[data-native-request]').forEach(form=>{const a=readAnswers(form);form.querySelectorAll('input[type=password]').forEach(i=>delete a[i.closest('[data-question]').dataset.question]);drafts.set(form.dataset.nativeRequest,a);});
    requestScope=key;requestKey=signature;host.hidden=!rows.length;
    host.innerHTML=rows.map(r=>`<article class="native-request ${esc(r.status)}"><div class="section-head"><h3>${esc(r.title)}</h3><span class="row-meta">${r.status==='pending'?'Needs your input':r.status==='answered'?'Answer sent':'Request ended'}</span></div>${r.detail?`<details><summary>Requested operation</summary><pre>${esc(r.detail)}</pre></details>`:''}${r.status==='pending'?`<form data-native-request="${esc(r.id)}">${r.questions.map(q=>`<fieldset data-question="${esc(q.id)}" data-multiple="${q.multiple?'1':''}"><legend>${esc(q.text)}</legend>${q.options.map((o,i)=>`<label class="native-option"><input type="${q.multiple?'checkbox':'radio'}" name="answer-${esc(q.id)}" value="${esc(o.value)}"><span>${esc(o.label)}${o.description?`<small>${esc(o.description)}</small>`:''}</span></label>`).join('')}${q.text?`<label class="native-free">${q.options.length?'Or write an answer':'Your answer'}<${q.secret?'input type="password" autocomplete="off"':'textarea rows="2"'} data-native-text maxlength="12000" aria-label="${esc(q.text)}">${q.secret?'':'</textarea>'}</label>`:''}</fieldset>`).join('')}<div class="inline-actions"><button type="submit" class="primary">Submit answer</button><span class="small-note" data-request-status role="status"></span></div></form>`:''}</article>`).join('');
    host.querySelectorAll('form[data-native-request]').forEach(form=>{
      const saved=drafts.get(form.dataset.nativeRequest)||{};
      form.querySelectorAll('[data-question]').forEach(field=>{
        const values=saved[field.dataset.question]||[];
        field.querySelectorAll('input[value]').forEach(input=>{input.checked=values.includes(input.value);});
        const text=field.querySelector('[data-native-text]');if(text&&text.type!=='password')text.value=values.filter(v=>![...field.querySelectorAll('input[value]')].some(i=>i.value===v)).join('\n');
      });
      form.onsubmit=event=>{event.preventDefault();attempt(async()=>{
        if(key!==requestScope)return;
        const button=form.querySelector('button'),status=form.querySelector('[data-request-status]');button.disabled=true;status.textContent='Sending…';
        try{
          await api('/api/chat/answer',{business:state.business,chat_id:chat,job_id:job.id,id:form.dataset.nativeRequest,answers:readAnswers(form)});
          drafts.delete(form.dataset.nativeRequest);
          if(key!==requestScope||!form.isConnected)return;
          status.textContent='Answer sent.';form.querySelectorAll('input,textarea,button').forEach(el=>{el.disabled=true;});
        }catch(error){if(form.isConnected){status.textContent=humanError(error);button.disabled=false;}}
      });};
    });
    if(focus){
      const form=[...host.querySelectorAll('form[data-native-request]')].find(f=>f.dataset.nativeRequest===focus.id);
      const target=form?.querySelectorAll('input,textarea,button')[focus.index];
      if(target){target.focus({preventScroll:true});if(typeof focus.start==='number')target.setSelectionRange?.(focus.start,focus.end);}
    }
    rows.filter(r=>r.status!=='pending').forEach(r=>drafts.delete(r.id));
    while(drafts.size>100)drafts.delete(drafts.keys().next().value);
  }

  function readAnswers(form){
    const answers={};form.querySelectorAll('[data-question]').forEach(field=>{
      const text=field.querySelector('[data-native-text]')?.value.trim();
      const selected=[...field.querySelectorAll('input:checked')].map(i=>i.value);
      answers[field.dataset.question]=text?[...(field.dataset.multiple?selected:[]),text]:selected;
    });return answers;
  }

  async function permissions(forChat=true,selectedKind=''){
    if(!state.data)return;
    if(forChat&&anchoredSurface?.anchor===$('#chat-permissions')){closeAnchoredSurface();return;}
    const key=scope(),ticket=++viewTicket,chat=forChat?state.chatMeta?.id:'',kind=selectedKind||(forChat?state.chatMeta?.agent:'')||composerConnection().kind||state.data.connection.selected;
    $('#more-dialog').close();details(forChat?'Permissions for this chat':'AI permissions','<p role="status">Reading permission choices…</p>','panel',forChat?$('#chat-permissions'):null);
    viewDetailTicket=state.fileDetailTicket;const host=$('#detail-content');
    const data=await api('/api/permissions?'+params({kind,...(chat?{chat_id:chat}:{})}));
    if(!current(key,ticket,host))return;
    const connected=state.data.connection.choices.filter(a=>a.available);
    const appField=!forChat?`<label>AI app<select id="permissions-app">${connected.map(a=>`<option value="${esc(a.id)}" ${a.id===kind?'selected':''}>${esc(a.name)}</option>`).join('')}</select></label>`:'';
    const bindApp=()=>$('#permissions-app')?.addEventListener('change',event=>permissions(false,event.target.value));
    if(data.choices.length===1){
      host.innerHTML=`${appField}<p>${esc(data.note||'This connection uses its own permission settings. It does not expose a permission mode that Aura can change.')}</p><button type="button" class="secondary" data-close="detail">Done</button>`;bindApp();return;
    }
    const override=chat?data.override:forChat&&state.newChatPermission?.kind===kind?state.newChatPermission.mode:'';
    host.innerHTML=`<form id="permissions-form" class="form-grid">${appField}<label>${forChat?(chat?'This chat':'This new chat'):'Default for this AI app'}<select id="permissions-mode">${forChat?`<option value="inherit" ${!override?'selected':''}>Use default (${esc(data.choices.find(c=>c.id===data.default)?.name||'AI app settings')})</option>`:''}${data.choices.map(c=>`<option value="${esc(c.id)}" ${(forChat?override:data.mode)===c.id?'selected':''}>${esc(c.name)}</option>`).join('')}</select></label><p id="permissions-native" class="small-note"></p><p class="small-note">${esc(data.note||'Applies to the next request in Aura. Running requests keep their current permissions.')}</p><div class="inline-actions"><button class="primary">Save permissions</button><span id="permissions-status" role="status"></span></div></form>`;
    const select=$('#permissions-mode'),paint=()=>{
      const choice=data.choices.find(c=>c.id===(select.value==='inherit'?data.default:select.value));
      $('#permissions-native').textContent=choice?.description||'Use the permission settings configured in your AI app.';
      select.classList.toggle('permission-unrestricted',!!choice?.unrestricted);$('#permissions-native').classList.toggle('permission-warning',!!choice?.unrestricted);
    };paint();select.onchange=paint;bindApp();
    $('#permissions-form').onsubmit=event=>{event.preventDefault();const form=event.currentTarget;attempt(async()=>{
      if(!current(key,ticket,host))return;const button=form.querySelector('button');button.disabled=true;
      try{
        if(forChat&&!chat){state.newChatPermission=select.value==='inherit'?null:{kind,mode:select.value};rememberChatDraft();}
        else{
          await api('/api/permissions',{business:state.business,kind,mode:select.value,...(chat?{chat_id:chat}:{})});
          if(!current(key,ticket,host))return;
          if(chat){if(select.value==='inherit')delete state.chatMeta.permission_mode;else state.chatMeta.permission_mode=select.value;}
          else{state.data.harness_permissions??={};state.data.harness_permissions[kind]=select.value;}
        }
        if(current(key,ticket,host)){$('#permissions-status').textContent=chat?'Saved for the next request.':forChat?'Saved for this new chat.':'Default saved. Inheriting chats use it on their next request.';renderComposerPermissions();}
      }finally{if(button.isConnected)button.disabled=false;}
    });};
  }

  async function activity(){
    const key=scope(),ticket=++viewTicket;details('Other work','<p role="status">Reading workspace activity…</p>');viewDetailTicket=state.fileDetailTicket;const host=$('#detail-content');
    const data=await api('/api/activity?'+params({limit:100,exclude_chat:state.chatMeta?.id||''}));if(!current(key,ticket,host))return;
    host.innerHTML='<p>Work observed in this workspace across connected AI apps.</p><input class="search" id="work-activity-search" type="search" placeholder="Find work…" aria-label="Find workspace activity"><div id="work-activity-list"></div><p class="small-note">Status is last observed. Work started outside Aura may not appear.</p>';
    const list=$('#work-activity-list');let limit=20;
    const paint=()=>{
      const q=$('#work-activity-search').value.trim().toLowerCase(),rows=data.items.filter(r=>[r.title,r.summary,r.assistant,r.agent,r.status].join(' ').toLowerCase().includes(q));
      list.innerHTML=rows.slice(0,limit).map(r=>`<article class="work-activity-row"><div class="section-head"><h3>${esc(r.title)}</h3><button type="button" class="text-button" data-chat="${esc(r.chat_id)}">Open chat</button></div><p>${esc(r.summary||r.progress||'')}</p><p class="row-meta">${esc(r.agent)}${r.assistant?' · '+esc(r.assistant):''} · ${r.needs_input&&data.running_chats.includes(r.chat_id)?'Needs input':r.status==='working'?(data.running_chats.includes(r.chat_id)?'Working':r.last_needs_input||r.needs_input?'Previously needed input':'Last observed working'):esc(human(r.status))} · ${esc(chatDate(r.observed_at))}</p></article>`).join('')||empty(q?'No matching work.':'No other work has been observed yet.');
      if(rows.length>limit)list.insertAdjacentHTML('beforeend','<button type="button" class="text-button" data-activity-more>Show more</button>');
    };$('#work-activity-search').oninput=()=>{limit=20;paint();};list.onclick=event=>{if(event.target.closest('[data-activity-more]')){limit+=20;paint();}};paint();
  }

  async function history(){
    $('#more-dialog').close();const key=scope(),ticket=++viewTicket;details('Version history','<p role="status">Reading local file history…</p>');viewDetailTicket=state.fileDetailTicket;const host=$('#detail-content');
    const data=await api('/api/history?'+params({}));if(!current(key,ticket,host))return;
    host.innerHTML='<p>Earlier versions of workspace files, saved on this computer.</p><input id="history-search" class="search" type="search" aria-label="Find a file in history" placeholder="Find a file…"><div id="history-list"></div><div id="history-review"></div><p class="small-note">Up to 20 versions per file and 256 MB per business. File recovery does not undo external actions.</p>';
    let limit=20,selection=0;
    const paint=()=>{
      const query=$('#history-search').value.trim().toLowerCase(),groups=new Map();
      data.items.filter(r=>r.path.toLowerCase().includes(query)).forEach(r=>{if(!groups.has(r.path))groups.set(r.path,[]);groups.get(r.path).push(r);});
      const rows=[...groups.entries()];$('#history-list').innerHTML=rows.slice(0,limit).map(([path,versions])=>`<details class="history-file"><summary>${esc(path)} <span class="row-meta">${versions.length} versions</span></summary>${versions.map(r=>`<div class="section-head"><span>${esc(new Date(r.at*1000).toLocaleString())}<small class="small-note">${esc(r.reason)} · ${Math.ceil(r.bytes/1024)} KB</small></span><button class="text-button" type="button" data-history-review="${esc(r.id)}">Review</button></div>`).join('')}</details>`).join('')||empty(query?'No matching files.':'Versions appear when you save changes or run work through Aura.');
      if(rows.length>limit)$('#history-list').insertAdjacentHTML('beforeend','<button type="button" class="text-button" data-history-more>Show more files</button>');
    };$('#history-search').oninput=()=>{limit=20;paint();};
    $('#history-list').onclick=event=>attempt(async()=>{
      if(event.target.closest('[data-history-more]')){limit+=20;paint();return;}
      const button=event.target.closest('[data-history-review]');if(!button)return;button.disabled=true;const reviewId=++selection;$('#history-review').textContent='Reading saved version…';
      try{
        const selected=await api('/api/history/version?'+params({id:button.dataset.historyReview}));if(!current(key,ticket,host)||reviewId!==selection)return;
        const review=$('#history-review');review.innerHTML=`<section class="history-review"><h3>${esc(selected.path)}</h3><p>Saved ${esc(new Date(selected.at*1000).toLocaleString())}</p>${selected.text?`<details open><summary>Saved content</summary><pre>${esc(selected.text)}</pre></details>`:`<p>${Math.ceil(selected.bytes/1024)} KB · Preview unavailable for this file.</p>`}<p>Restore this version to this file? Its current contents will be kept in history.</p><button type="button" class="primary" id="history-restore">Restore this version</button><p id="history-restore-status" role="status"></p></section>`;
        $('#history-restore').onclick=()=>attempt(async()=>{
          if(!current(key,ticket,host)||reviewId!==selection)return;const restore=$('#history-restore');restore.disabled=true;
          try{const result=await api('/api/history/restore',{business:state.business,id:selected.id,expected_revision:selected.current_revision});if(current(key,ticket,host)){$('#history-restore-status').textContent=(result.warning||'Restored.')+' Reopen the file to see it.';}}
          catch(error){if(current(key,ticket,host)){$('#history-restore-status').textContent=humanError(error);restore.disabled=false;}}
        });review.scrollIntoView({block:'nearest',behavior:'smooth'});
      }finally{if(button.isConnected)button.disabled=false;}
    });paint();
  }

  document.addEventListener('click',event=>{
    const id=event.target.closest('button')?.id;
    if(id==='chat-permissions')attempt(()=>permissions(true));
    if(id==='harness-permissions')attempt(()=>permissions(false));
    if(id==='other-work')attempt(activity);
    if(id==='workspace-history')attempt(history);
    if(id==='recovery-check')attempt(()=>checkRecovery(true));
    if(id==='recovery-continue')attempt(continueRecovery);
  });
  if(state.hydrated)queueMicrotask(()=>{acceptRecovery({chat:state.chatMeta,recovery:state.recovery});renderRecovery();attempt(()=>checkRecovery());});
  return {renderRequests,history,renderRecovery,acceptRecovery,checkRecovery};
})();
