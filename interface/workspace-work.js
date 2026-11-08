/* Views over existing native work and small saved assistant profiles. */
'use strict';
window.auraWork = (() => {
  let cache=null, scope='', delegationKey='', delegationChat='', delegationLimit=20, nativeSelection={scope:'',kind:''};
  const currentScope=()=>JSON.stringify([state.data?.workspace,state.business]);
  const endpoint=()=>'/api/agents?business='+encodeURIComponent(state.business);
  async function load(){const key=currentScope(),result=await api(endpoint());if(key!==currentScope())return null;cache=result;scope=key;return result;}
  const profile=id=>scope===currentScope()?cache?.items.find(p=>p.id===id):null;
  const taskOwner=(id)=>scope===currentScope()?cache?.items.find(p=>(p.task_ids||[]).includes(id)):null;
  const chatRows=(items,limit=20)=>items.length?items.slice(0,limit).map(c=>`<button type="button" class="row" data-chat="${esc(c.id)}"><span class="row-text"><span class="row-title">${esc(c.title)}</span><span class="row-meta">${esc(appName(c.agent))} · ${esc(c.status==='working'?((cache?.running||[]).includes(c.id)?'Working':'Check chat'):chatDate(c.updated))}</span></span></button>`).join(''):empty('No chats yet.');
  async function renderAssistants(host){
    host.innerHTML='<p role="status">Loading agents…</p>';
    const data=await load();if(!data||!host.isConnected||state.view!=='assistants')return;
    if(nativeSelection.scope!==currentScope())nativeSelection={scope:currentScope(),kind:state.data.connection.selected};
    host.innerHTML=`<div class="assistant-search-toolbar"><input type="search" class="search" id="assistant-search" aria-label="Find an agent" placeholder="Find an agent…"><button type="button" class="primary" data-assistant-new>Create agent</button></div><div id="assistant-list" class="assistant-list"></div><section class="native-agents-section"><h3>Native agents & delegation</h3><div class="inline-actions"><label>AI app<select id="native-agent-app">${state.data.connection.choices.filter(a=>a.available).map(a=>`<option value="${esc(a.id)}"${a.id===nativeSelection.kind?' selected':''}>${esc(a.name)}</option>`).join('')}</select></label><button type="button" class="secondary" id="native-agents-open">Browse agents</button><button type="button" class="text-button" id="native-delegation-open">Delegation settings</button></div></section>`;
    $('#native-agent-app').onchange=()=>{nativeSelection={scope:currentScope(),kind:$('#native-agent-app').value};};
    $('#native-agents-open').onclick=()=>attempt(()=>nativeAgents($('#native-agent-app').value));
    $('#native-delegation-open').onclick=()=>attempt(()=>delegationSettings($('#native-agent-app').value));
    const renderList=()=>{
      const query=$('#assistant-search').value.trim().toLowerCase();
      const items=data.items.filter(p=>(p.name+' '+(p.description||'')+' '+(p.instructions||'')).toLowerCase().includes(query));
      $('#assistant-list').innerHTML=items.map(p=>{
        const chats=data.chats.filter(c=>c.assistant_id===p.id),active=chats.filter(c=>(data.running||[]).includes(c.id)).length,tasks=(p.task_ids||[]).length;
        return `<article class="card assistant-card"><div class="section-head"><h3>${esc(p.name)}</h3><button type="button" class="secondary" data-assistant-open="${esc(p.id)}">Open agent</button></div><p>${esc(p.description||p.instructions||'Add instructions to give this agent a purpose.')}</p><p class="row-meta">${chats.length} ${chats.length===1?'chat':'chats'} · ${tasks} scheduled ${tasks===1?'task':'tasks'}${active?' · '+active+' working':''}${p.native_agent?' · '+esc(appName(p.app))+' agent':''}</p></article>`;
      }).join('')||empty(query?'No matching agents.':'Create an agent with a name and instructions, or connect a native agent.');
    };
    $('#assistant-search').oninput=renderList;renderList();
  }
  const nativeEndpoint=(kind,extra={})=>'/api/native-agents?'+new URLSearchParams({business:state.business,kind,...extra});
  async function nativeAgents(kind){
    const key=currentScope();details(appName(kind)+' agents','<p role="status">Loading native agents…</p>');
    const ticket=state.fileDetailTicket,data=await api(nativeEndpoint(kind));
    if(key!==currentScope()||ticket!==state.fileDetailTicket||!$('#detail').open)return;
    details(appName(kind)+' agents',`${data.note?`<p class="small-note">${esc(data.note)}</p>`:''}${data.editable?'<div class="inline-actions"><button type="button" class="primary" id="native-agent-new">Create native agent</button><button type="button" class="text-button" id="native-agent-settings">Delegation settings</button></div>':''}<div id="native-agent-list">${data.items.map((p,i)=>`<button type="button" class="row" data-native-index="${i}"><span class="row-text"><strong>${esc(p.name)}</strong><span>${esc(p.description)}</span><span class="row-meta">${p.scope==='project'?'Project':p.scope==='profile'?'Profile':p.scope==='native'?'Built in':'Personal'}${p.reported?' · Available now':''}${p.model?' · '+esc(Array.isArray(p.model)?p.model.join(', '):p.model):''}${p.shadowed?' · Overridden by project agent':''}</span></span></button>`).join('')||empty('No custom native agents found.')}</div>${data.notes?.length?`<p class="error" role="status">${data.notes.map(esc).join(' ')}</p>`:''}`);
    $('#native-agent-new')?.addEventListener('click',()=>attempt(()=>nativeEdit(kind)));
    $('#native-agent-settings')?.addEventListener('click',()=>attempt(()=>delegationSettings(kind)));
    $('#native-agent-list').onclick=event=>{const button=event.target.closest('[data-native-index]');if(button){const row=data.items[Number(button.dataset.nativeIndex)];if(row.readonly){details(row.name,`<p>${esc(row.description)}</p><p class="small-note">Available through ${esc(appName(kind))}’s native delegation tool.</p><div class="inline-actions"><button type="button" class="secondary" id="native-roster-settings">Delegation settings</button><button type="button" class="text-button" id="native-roster-back">Back to agents</button></div>`);$('#native-roster-settings').onclick=()=>attempt(()=>delegationSettings(kind));$('#native-roster-back').onclick=()=>attempt(()=>nativeAgents(kind));}else attempt(()=>nativeEdit(kind,row));}};
  }
  async function nativeEdit(kind,reference=null){
    const key=currentScope();details(reference?'Native agent':'Create native agent','<p role="status">Loading agent…</p>');
    const ticket=state.fileDetailTicket,p=reference?await api(nativeEndpoint(kind,{action:'read',scope:reference.scope,file:reference.file})):{};
    const isProfile=kind==='hermes',primary=isProfile||kind==='claude'||kind==='antigravity'&&p.settings?.mainAgent!==false;
    const capabilities=isProfile&&reference?[['skills','disabled_skills','Skills'],['toolsets','enabled_toolsets','Tools'],['mcp_servers','enabled_mcp_servers','MCP servers']].filter(([key])=>p.settings?.[key]?.length):[];
    if(key!==currentScope()||ticket!==state.fileDetailTicket||!$('#detail').open)return;
    details(reference?p.name:'Create native agent',`<form id="native-agent-form" class="form-grid"><p class="small-note">${esc(appName(kind))} owns this definition and its delegation behavior.</p>${isProfile?(reference?'<p class="row-meta">Native Hermes profile</p>':'<label class="check-label"><input name="include_skills" type="checkbox" checked> Include bundled Hermes skills</label>'):p.path?`<div class="native-agent-location"><span>${esc(p.path)}</span><button type="button" class="text-button" id="native-agent-copy">Copy path</button></div>`:`<label>Available in<select name="scope"><option value="project">This project</option><option value="user">All my projects</option></select></label>`}<label>Name<input name="name" maxlength="80" required value="${esc(p.name||'')}"${reference?' readonly':''}></label><label>When to use this agent<textarea name="description" rows="2" maxlength="1000"${isProfile?'':' required'}>${esc(p.description||'')}</textarea></label><label>Instructions<textarea name="instructions" rows="6" maxlength="20000">${esc(p.instructions||'')}</textarea></label><label>Model${kind==='antigravity'?`<select name="model">${['inherit','flash','pro'].map(m=>`<option${m===(p.model||'inherit')?' selected':''}>${m}</option>`).join('')}</select>`:`<div class="inline-actions"><input name="model" value="${esc(Array.isArray(p.model)?p.model.join(', '):p.model||'')}" placeholder="${isProfile?'Keep native model':'Inherit native settings'}"${isProfile&&reference&&p.model?' required':''}${Array.isArray(p.model)?' disabled':''}><button type="button" class="secondary" id="native-agent-pick-model"${Array.isArray(p.model)?' disabled':''}>Choose model</button></div>`}</label>${['codex','omp','claude'].includes(kind)?`<label>Effort<input name="effort" value="${esc(p.effort||'')}" placeholder="Native default"></label>`:''}${capabilities.map(([key,setting,label])=>`<details><summary>${label}</summary>${key==='toolsets'?`<label class="check-label"><input type="checkbox" id="native-tools-default"${p.settings.toolsets_pinned?'':' checked'}> Use native tool defaults</label>`:''}<div class="form-grid" data-capability="${setting}">${p.settings[key].map((r,i)=>`<label class="check-label"><input type="checkbox" data-capability-index="${i}"${r.enabled?' checked':''}><span class="native-capability-label">${esc(r.label||r.name)}${r.description?`<small>${esc(r.description)}</small>`:''}</span></label>`).join('')}</div></details>`).join('')}${p.source?`<details><summary>Native definition</summary><label>Edit full definition<textarea id="native-agent-source" rows="12" spellcheck="false">${esc(p.source)}</textarea></label></details>`:''}<div class="inline-actions"><button type="submit" class="primary">Save native agent</button>${reference?`<button type="button" class="secondary" id="native-agent-use">${primary?'Use native agent in AURA':'Use instructions in AURA'}</button>`:''}${isProfile&&reference?'<button type="button" class="text-button" id="native-profile-delegation">Delegation settings</button>':''}<button type="button" class="text-button" id="native-agent-back">Back to agents</button></div><p class="small-note" id="native-agent-status" role="status"></p>${reference?`<p class="small-note">${primary?'The native app loads this agent. Your explicit chat model and permissions still apply.':'Native model and tool settings apply when the harness delegates to this agent. AURA chats reuse its instructions with the chat’s selected model and permissions.'}</p>`:''}</form>`);
    const form=$('#native-agent-form'),current=()=>key===currentScope()&&form.isConnected&&$('#detail').open;
    $('#native-agent-pick-model')?.addEventListener('click',()=>attempt(()=>openChatModels({title:'Native agent model',modelOnly:true,anchor:$('#native-agent-pick-model'),connection:{kind,model:form.querySelector('[name=model]').value,effort:'',...(isProfile&&reference?{native_profile:p.file}:{})},current,onSelect:choice=>{form.querySelector('[name=model]').value=choice.model;}})));
    $('#native-agent-copy')?.addEventListener('click',()=>attempt(async()=>{await navigator.clipboard.writeText(p.path);if(current())$('#native-agent-status').textContent='Path copied.';}));
    const toolsDefault=$('#native-tools-default');if(toolsDefault){const paintTools=()=>form.querySelectorAll('[data-capability="enabled_toolsets"] input').forEach(input=>input.disabled=toolsDefault.checked);toolsDefault.onchange=paintTools;paintTools();}
    $('#native-agent-back').onclick=()=>attempt(()=>nativeAgents(kind));
    $('#native-profile-delegation')?.addEventListener('click',()=>attempt(()=>delegationSettings(kind,p.file)));
    $('#native-agent-source')?.addEventListener('input',event=>{const raw=event.target.value!==p.source;form.querySelectorAll('[name]').forEach(n=>n.disabled=raw||n.name==='model'&&Array.isArray(p.model));if($('#native-agent-pick-model'))$('#native-agent-pick-model').disabled=raw||Array.isArray(p.model);});
    $('#native-agent-use')?.addEventListener('click',()=>attempt(async()=>{
      const loaded=await load();if(!current()||!loaded)return;
      const binding={app:p.app||kind,scope:p.scope,file:p.file},existing=loaded.items.find(a=>a.app===kind&&['app','scope','file'].every(k=>a.native_agent?.[k]===binding[k]));
      if(existing){await overview(existing.id);return;}
      const result=await api('/api/agents',{business:state.business,name:p.name,description:p.description,app:kind,native_agent:binding});
      if(!current())return;cache=result;scope=key;const created=cache.items.at(-1);if(state.view==='assistants')await renderAssistants($('#section-content'));await overview(created.id);
    }));
    form.onsubmit=event=>{event.preventDefault();attempt(async()=>{
      const button=form.querySelector('[type="submit"]');button.disabled=true;
      try{
        const raw=$('#native-agent-source'),data=raw&&raw.value!==p.source?{source:raw.value}:Object.fromEntries(new FormData(form));
        if(isProfile){data.scope='profile';if(!reference)data.include_skills=form.querySelector('[name=include_skills]')?.checked!==false;for(const [key,setting] of capabilities){if(setting==='enabled_toolsets'&&toolsDefault?.checked){if(p.settings.toolsets_pinned)data.enabled_toolsets=[];continue;}const selected=[...form.querySelectorAll(`[data-capability="${setting}"] input`)].flatMap((input,i)=>(setting==='disabled_skills'?!input.checked:input.checked)?[p.settings[key][i].name]:[]);if(setting==='enabled_toolsets'&&!selected.length)throw new Error('Select at least one toolset, or use native tool defaults.');const prior=p.settings[key].filter(r=>setting==='disabled_skills'?!r.enabled:r.enabled).map(r=>r.name);if(JSON.stringify(selected)!==JSON.stringify(prior))data[setting]=selected;}}
        const result=await api('/api/native-agents',{business:state.business,kind,action:'save',...data,...(reference?{scope:p.scope,file:p.file,revision:p.revision}:{})});
        if(current()){await nativeEdit(kind,result);$('#native-agent-status').textContent='Saved in '+appName(kind)+'.';}
      }catch(error){if(current())$('#native-agent-status').textContent=humanError(error);}finally{if(button.isConnected)button.disabled=false;}
    });};
  }
  const routeRow=(type,row={})=>`<div class="card form-grid native-route" data-route-type="${type}"><label>Name<input data-route-name value="${esc(row.name||'')}"${row.name?' readonly':''} placeholder="research"></label><label>When to use<input data-route-description value="${esc(row.description||'')}"></label>${type==='models'?`<label>Model<div class="inline-actions"><input data-route-model value="${esc((row.provider?row.provider+':':'')+(row.model||''))}" placeholder="Inherit native provider"><button type="button" class="secondary" data-pick-route>Choose model</button></div></label>`:''}<button type="button" class="text-button danger" data-remove-route>Remove route</button></div>`;
  function routingForm(routing){
    if(!routing?.available)return routing?.note?`<p class="small-note">${esc(routing.note)} <a href="https://hermes-agent.nousresearch.com/marketplace/advanced-delegation" target="_blank" rel="noopener">Plugin details</a></p>`:'';
    return `<details><summary>Native routing</summary><div class="form-grid"><label>Delegation mode<select id="native-route-mode">${[['default','Native default'],['model_map','Named model routes'],['profile_routes','Named profile routes']].map(([v,label])=>`<option value="${v}"${v===routing.mode?' selected':''}>${label}</option>`).join('')}</select></label><p class="small-note">These optional routes are managed by Hermes. Native default keeps its usual model choices.</p>${['models','profiles'].map(type=>`<details><summary>${type==='models'?'Model routes':'Profile routes'}</summary><div data-routes="${type}" class="form-grid">${routing[type].map(r=>routeRow(type,r)).join('')}</div><button type="button" class="text-button" data-add-route="${type}">Add route</button><label>Default route<input data-route-default="${type}" value="${esc(routing[type==='models'?'model_default':'profile_default']||'')}" placeholder="Main model"></label></details>`).join('')}</div></details>`;
  }
  function collectRouting(form,routing){
    const result={mode:form.querySelector('#native-route-mode').value};
    for(const type of ['models','profiles']){
      result[type]=[...form.querySelectorAll(`[data-routes="${type}"] .native-route`)].map(row=>{
        const item={name:row.querySelector('[data-route-name]').value.trim(),description:row.querySelector('[data-route-description]').value.trim()};
        if(type==='models'){const choice=row.querySelector('[data-route-model]').value.trim(),split=choice.indexOf(':');item.provider=split<0?'':choice.slice(0,split);item.model=split<0?choice:choice.slice(split+1);}return item;
      });
      result[type==='models'?'model_default':'profile_default']=form.querySelector(`[data-route-default="${type}"]`).value.trim();
    }
    const before={mode:routing.mode,models:routing.models.map(r=>({name:r.name,description:r.description||'',provider:r.provider||'',model:r.model||''})),profiles:routing.profiles.map(r=>({name:r.name,description:r.description||''})),model_default:routing.model_default,profile_default:routing.profile_default};
    const changes={mode:result.mode};let changed=result.mode!==before.mode;for(const type of ['models','profiles']){const def=type==='models'?'model_default':'profile_default';if(JSON.stringify(result[type])!==JSON.stringify(before[type])||result[def]!==before[def]){changes[type]=result[type];changes[def]=result[def];changed=true;}}return changed?changes:null;
  }
  async function delegationSettings(kind,nativeProfile=null){
    const key=currentScope();details('Delegation settings','<p role="status">Reading native settings…</p>');
    const ticket=state.fileDetailTicket,data=await api('/api/delegation-settings?'+new URLSearchParams({business:state.business,kind,...(nativeProfile?{profile:nativeProfile}:{})}));
    if(key!==currentScope()||ticket!==state.fileDetailTicket||!$('#detail').open)return;
    details(appName(kind)+' delegation',`<p class="small-note">${esc(data.scope||'')}</p>${data.note?`<p class="small-note">${esc(data.note)}</p>`:''}<form id="delegation-settings-form" class="form-grid">${(data.fields||[]).map((r,i)=>`<div class="native-delegation-field"><span class="native-setting-label">${esc(r.name)}</span>${r.type==='model-map'?`<div class="native-model-map" data-native-map="${i}">${Object.entries(r.value||{}).map(([name,model])=>`<div class="native-model-pair"><input aria-label="Role or agent name" data-role value="${esc(name)}"><input aria-label="Model" data-model value="${esc(model)}"><button type="button" class="text-button" data-pick-role>Choose</button><button type="button" class="text-button" data-remove-role aria-label="Remove role">×</button></div>`).join('')}<button type="button" class="text-button" data-add-role>Add assignment</button></div>`:r.type==='select'?`<select aria-label="${esc(r.name)}" data-setting="${i}"${r.readonly?' disabled':''}>${r.options.map(o=>`<option value="${esc(JSON.stringify(o.value))}"${o.value===r.value?' selected':''}>${esc(o.name)}</option>`).join('')}</select>`:`<input aria-label="${esc(r.name)}" data-setting="${i}" type="${r.type==='number'?'number':'text'}" value="${esc(r.value??'')}" placeholder="Native default"${r.type==='number'?` min="${r.min}" step="${r.step}"`:''}${r.readonly?' disabled':''}>`}${r.readonly?'<small>Controlled by native project or profile settings.</small>':''}</div>`).join('')}${routingForm(data.routing)}${data.fields?.length||data.routing?.available?'<div class="inline-actions"><button type="submit" class="primary">Save native settings</button></div>':''}<p id="delegation-settings-status" role="status"></p></form>`);
    const form=$('#delegation-settings-form'),current=()=>key===currentScope()&&form.isConnected&&$('#detail').open;
    form.onclick=event=>{const addRoute=event.target.closest('[data-add-route]');if(addRoute)form.querySelector(`[data-routes="${addRoute.dataset.addRoute}"]`).insertAdjacentHTML('beforeend',routeRow(addRoute.dataset.addRoute));const removeRoute=event.target.closest('[data-remove-route]');if(removeRoute)removeRoute.closest('.native-route').remove();const routePicker=event.target.closest('[data-pick-route]');if(routePicker){const input=routePicker.closest('.native-route').querySelector('[data-route-model]');attempt(()=>openChatModels({title:'Native model route',modelOnly:true,anchor:routePicker,connection:{kind,model:input.value,effort:'',...(data.profile?{native_profile:data.profile}:{})},current,onSelect:choice=>{if(input.isConnected)input.value=choice.model;}}));}const picker=event.target.closest('[data-pick-role]');if(picker){const input=picker.closest('.native-model-pair').querySelector('[data-model]');attempt(()=>openChatModels({title:'Native model assignment',modelOnly:true,anchor:picker,connection:{kind,model:input.value,effort:''},current,onSelect:choice=>{if(input.isConnected)input.value=choice.model;}}));}if(event.target.closest('[data-remove-role]'))event.target.closest('.native-model-pair').remove();if(event.target.closest('[data-add-role]'))event.target.closest('[data-add-role]').insertAdjacentHTML('beforebegin','<div class="native-model-pair"><input aria-label="Role or agent name" data-role placeholder="research"><input aria-label="Model" data-model placeholder="provider/model"><button type="button" class="text-button" data-pick-role>Choose</button><button type="button" class="text-button" data-remove-role aria-label="Remove role">×</button></div>');};
    for(const [i,row] of (data.fields||[]).entries())if(row.readonly)form.querySelector(`[data-native-map="${i}"]`)?.querySelectorAll('input,button').forEach(n=>n.disabled=true);
    form.onsubmit=event=>{event.preventDefault();attempt(async()=>{
      const changes={};
      try{
        for(const [i,row] of data.fields.entries()){
          if(row.readonly)continue;let value;
          if(row.type==='model-map'){
            value={};for(const pair of form.querySelectorAll(`[data-native-map="${i}"] .native-model-pair`)){const name=pair.querySelector('[data-role]').value.trim(),model=pair.querySelector('[data-model]').value.trim();if(!name||!model||Object.hasOwn(value,name))throw new Error('Give each assignment a unique name and a model.');Object.defineProperty(value,name,{value:model,enumerable:true});}
          }else{const input=form.querySelector(`[data-setting="${i}"]`);value=input.value.trim()===''?null:row.type==='select'?JSON.parse(input.value):row.type==='number'?Number(input.value):input.value.trim();}
          if(JSON.stringify(value)!==JSON.stringify(row.value))changes[row.id]=value;
        }
        if(data.routing?.available){const routing=collectRouting(form,data.routing);if(routing)changes._routing=routing;}
        if(!Object.keys(changes).length){$('#delegation-settings-status').textContent='No changes to save.';return;}
        form.querySelector('[type="submit"]').disabled=true;
        const result=await api('/api/delegation-settings',{business:state.business,kind,changes,revision:data.revision,...(nativeProfile?{profile:nativeProfile}:{})});
        if(current()){await delegationSettings(kind,nativeProfile);$('#delegation-settings-status').textContent=result.message;}
      }catch(error){if(current()){$('#delegation-settings-status').textContent=humanError(error);form.querySelector('[type="submit"]').disabled=false;}}
    });};
  }
  async function overview(id){
    const key=currentScope(),view=state.view;details('Agent','<p role="status">Loading agent…</p>');
    const ticket=state.fileDetailTicket,current=()=>key===currentScope()&&view===state.view&&ticket===state.fileDetailTicket&&$('#detail').open;
    const data=await load(),p=profile(id);if(!data||!current())return;if(!p){notice('This agent was removed. Its chats, tasks, and results are still available.');return;}
    const schedules=await api('/api/schedules');if(!current())return;
    const tasks=schedules.items.filter(t=>(p.task_ids||[]).includes(t.id));state.schedules=schedules;
    const missing=(p.task_ids||[]).length-tasks.length;
    details(p.name,`<div class="assistant-toolbar"><button type="button" class="primary" data-assistant-chat="${esc(id)}">New chat with ${esc(p.name)}</button><button type="button" class="secondary" data-assistant-edit="${esc(id)}">Edit agent</button></div>${p.description?`<p>${esc(p.description)}</p>`:''}${p.native_agent?`<button type="button" class="text-button" id="assistant-overview-native">View native instructions</button>`:`<p class="assistant-instructions">${esc(p.instructions||'No saved instructions.')}</p>`}<p class="small-note">${esc(p.app?appName(p.app):'Current AI connection')}${p.model?' · '+esc(p.model):''}${p.child_model?' · Subagents: '+esc(p.child_model):''}</p><section><h3>Scheduled tasks</h3>${tasks.map(t=>scheduleRow(t)).join('')||empty((p.task_ids||[]).length?'Linked tasks are not currently available.':'No scheduled tasks assigned.')}<div class="inline-actions assistant-task-actions"><button type="button" class="secondary" data-assistant-existing-task="${esc(id)}">Assign existing task</button><button type="button" class="text-button" data-assistant-task="${esc(id)}">Create scheduled task</button><button type="button" class="text-button" data-view="tools">All scheduled tasks</button></div>${missing?'<p class="small-note">Some linked tasks are unavailable. Refresh them in their owning app.</p>':''}${schedules.notes?.length?`<p class="error" role="status">${schedules.notes.map(esc).join(' ')}</p>`:''}</section><section><h3>Conversations</h3><input type="search" id="assistant-chat-search" class="search" aria-label="Search this agent’s chat titles" placeholder="Find a chat by title…"><div id="assistant-chat-list"></div></section>`);
    $('#assistant-overview-native')?.addEventListener('click',()=>attempt(()=>nativeEdit(p.app,p.native_agent)));
    const chats=data.chats.filter(c=>c.assistant_id===id),host=$('#assistant-chat-list'),search=$('#assistant-chat-search');let limit=20;
    const renderChats=()=>{
      if(key!==currentScope()||!host.isConnected)return;
      const query=search.value.trim().toLowerCase(),matches=chats.filter(c=>(c.title||'').toLowerCase().includes(query));
      host.innerHTML=(matches.length?chatRows(matches,limit):empty(query?'No matching chats.':'No chats yet.'))+
        (matches.length?`<p class="small-note">${Math.min(limit,matches.length)} of ${matches.length} ${matches.length===1?'chat':'chats'}</p>`:'')+
        (matches.length>limit?'<button type="button" class="text-button" data-assistant-more-chats>Show more chats</button>':'');
    };
    search.oninput=()=>{limit=20;renderChats();};host.onclick=event=>{if(event.target.closest('[data-assistant-more-chats]')){limit+=20;renderChats();}};renderChats();
  }
  async function edit(id='',draft=null){
    if(!await load())return;const p=draft||(id?profile(id):{});if(!p)return;
    const key=currentScope(),apps=state.data.connection.choices.filter(c=>c.available||c.id===p.app);
    details(id?'Edit agent':'Create agent',`<form id="assistant-form" class="form-grid" data-detach-native="${draft?'true':'false'}"><input name="id" type="hidden" value="${esc(id)}"><label>Name<input name="name" maxlength="80" required value="${esc(p.name||'')}" placeholder="Jeff"></label><label>What this agent helps with<textarea name="description" maxlength="1000" rows="2" placeholder="Researches customers and returns findings with sources">${esc(p.description||'')}</textarea></label>${p.native_agent?`<p class="small-note">Instructions come from ${esc(appName(p.app))}.</p><button type="button" class="secondary" id="assistant-native-edit">Edit native agent</button><button type="button" class="text-button" id="assistant-native-detach">Use separate instructions</button>`:`<label>Instructions<textarea name="instructions" maxlength="20000" rows="4" placeholder="What should this agent help with?">${esc(p.instructions||'')}</textarea></label>`}<div id="agent-saved-context"></div><details ${p.app||p.model||p.child_model?'open':''}><summary>AI preferences</summary><div class="form-grid assistant-preferences"><label>AI app<select name="app" id="assistant-app"><option value="">Current connection</option>${apps.map(a=>`<option value="${esc(a.id)}" ${a.id===p.app?'selected':''}>${esc(a.name)}</option>`).join('')}</select></label><input type="hidden" name="model" id="assistant-model" value="${esc(p.model||'')}"><input type="hidden" name="effort" id="assistant-effort" value="${esc(p.effort||'')}"><input type="hidden" name="child_model" id="assistant-child-model" value="${esc(p.child_model||'')}"><div><label for="assistant-pick-model">Preferred model & effort</label><div class="inline-actions"><button type="button" class="secondary" id="assistant-pick-model" aria-haspopup="dialog"></button><button type="button" class="text-button" id="assistant-reset-model">Use app default</button></div></div><div><label for="assistant-pick-child">Subagent model</label><div class="inline-actions"><button type="button" class="secondary" id="assistant-pick-child" aria-haspopup="dialog"></button><button type="button" class="text-button" id="assistant-reset-child">Inherit native settings</button></div></div><p class="small-note" id="assistant-delegation-note"></p></div></details>${!p.native_agent?'<div id="assistant-native-publish"><label class="check-label"><input type="checkbox" name="publish_native"> <span id="assistant-publish-label">Also make available as a native subagent</span></label><label id="assistant-native-scope" hidden>Available in<select name="native_scope"><option value="project">This project</option><option value="user">All my projects</option></select></label></div>':''}<div class="inline-actions"><button class="primary">Save agent</button>${id?`<button type="button" class="text-button" data-assistant-open="${esc(id)}">Cancel</button><button type="button" class="text-button danger" data-assistant-remove="${esc(id)}">Archive agent</button>`:'<button type="button" class="text-button" data-assistant-cancel>Cancel</button>'}</div><p id="assistant-save-status" role="status"></p></form>`);
    $('#assistant-native-edit')?.addEventListener('click',()=>attempt(()=>nativeEdit(p.app,p.native_agent)));
    $('#assistant-native-detach')?.addEventListener('click',()=>attempt(async()=>{const previous=$('#assistant-form');let source=null;try{source=await api(nativeEndpoint(p.app,{action:'read',scope:p.native_agent.scope,file:p.native_agent.file}));}catch{}if(key!==currentScope()||!previous.isConnected)return;await edit(id,{...p,native_agent:null,instructions:source?.instructions||p.instructions||'',description:source?.description||p.description||''});if($('#assistant-save-status'))$('#assistant-save-status').textContent='Save to use separate instructions. The native definition stays available.';}));
    window.auraInsight?.references($('#agent-saved-context'),p.context_refs||[]);
    const form=$('#assistant-form'),app=$('#assistant-app'),model=$('#assistant-model'),effort=$('#assistant-effort'),child=$('#assistant-child-model');
    let kind=app.value||state.data.connection.selected;if(p.native_agent)app.disabled=true;
    const paint=()=>{
      $('#assistant-pick-model').textContent=model.value+(effort.value?' · '+human(effort.value):'')||'App default';
      $('#assistant-pick-child').textContent=child.value||'Inherit native settings';
      $('#assistant-pick-model').disabled=!nativeApps.includes(kind);$('#assistant-pick-child').disabled=!['codex','omp','claude'].includes(kind);
      $('#assistant-delegation-note').textContent=({codex:'Sets the native subagent default for this chat. Individual agent choices can take precedence.',omp:'Sets OMP’s general task model role for this chat. Named specialists keep their native assignments.',claude:'Sets the native subagent-model environment default for this chat.'})[kind]||'Set specialist models in Native agents & delegation. Existing saved subagent preferences are instructions only on this connection.';
      const publish=$('#assistant-native-publish');if(publish){publish.hidden=!['codex','omp','pi','claude','antigravity'].includes(kind);publish.querySelectorAll('input,select').forEach(n=>n.disabled=publish.hidden);$('#assistant-publish-label').textContent='Also make available to '+appName(kind)+' as a native subagent';$('#assistant-native-scope').hidden=!publish.querySelector('[name=publish_native]').checked;}
      $('#assistant-reset-model').hidden=!model.value&&!effort.value;$('#assistant-reset-child').hidden=!child.value;
    };
    const pick=modelOnly=>{const chosenKind=kind;return attempt(()=>openChatModels({title:modelOnly?'Subagent model':'Agent model & effort',modelOnly,anchor:$(modelOnly?'#assistant-pick-child':'#assistant-pick-model'),
      connection:{kind:chosenKind,model:modelOnly?child.value:model.value,effort:modelOnly?'':effort.value},
      current:()=>key===currentScope()&&form.isConnected&&$('#detail').open&&chosenKind===(app.value||state.data.connection.selected),
      onSelect:choice=>{app.value=choice.kind;kind=choice.kind;if(modelOnly)child.value=choice.model;else{model.value=choice.model;effort.value=choice.effort;}paint();}}));};
    $('#assistant-pick-model').onclick=()=>pick(false);$('#assistant-pick-child').onclick=()=>pick(true);
    $('#assistant-reset-model').onclick=()=>{model.value=effort.value='';paint();};$('#assistant-reset-child').onclick=()=>{child.value='';paint();};
    form.querySelector('[name=publish_native]')?.addEventListener('change',paint);
    app.onchange=()=>{const next=app.value||state.data.connection.selected;if(next!==kind){model.value=effort.value=child.value='';kind=next;}paint();};paint();
  }
  async function chooseTask(id){
    const key=currentScope();details('Assign a scheduled task','<p role="status">Finding scheduled tasks…</p>');
    const ticket=state.fileDetailTicket,host=$('#detail-content');
    const current=()=>key===currentScope()&&ticket===state.fileDetailTicket&&host.isConnected&&$('#detail').open;
    try{
      const [data,schedules]=await Promise.all([load(),api('/api/schedules?scope=workspace')]);if(!current()||!data)return;
      const p=profile(id);if(!p)throw new Error('This agent is no longer available.');
      state.schedules=schedules;
      host.innerHTML=`<p>Assign to <strong>${esc(p.name)}</strong>. Tasks keep their current schedule and instructions.</p><input id="assistant-task-search" class="search" type="search" aria-label="Find an existing scheduled task" placeholder="Find a scheduled task…"><div id="assistant-task-choices"></div><p id="assistant-task-status" role="status"></p><div class="inline-actions assistant-task-actions"><button type="button" class="text-button" data-assistant-open="${esc(id)}">Back to agent</button><button type="button" class="secondary" data-assistant-task="${esc(id)}">Create scheduled task</button></div>${schedules.notes?.length?`<p class="small-note">${schedules.notes.map(esc).join(' ')}</p>`:''}`;
      const available=schedules.items.filter(t=>!(p.task_ids||[]).includes(t.id));let limit=20,saving=false;
      const paint=()=>{
        if(!current())return;const q=$('#assistant-task-search').value.trim().toLowerCase();
        const matches=available.filter(t=>[t.name,t.description,appName(t.owner),taskOwner(t.id)?.name].join(' ').toLowerCase().includes(q));
        $('#assistant-task-choices').innerHTML=matches.slice(0,limit).map(t=>{
          const owner=taskOwner(t.id);
          return `<article class="assistant-task-choice"><div><strong>${esc(t.name)}</strong><p class="row-meta">${esc(appName(t.owner))}${owner?' · Assigned to '+esc(owner.name):''}</p></div><button type="button" class="secondary" data-assign-existing-task="${esc(t.id)}">${owner?'Move here':'Assign'}</button></article>`;
        }).join('')||empty(q?'No matching scheduled tasks.':available.length?'No matching scheduled tasks.':schedules.items.length?'All available tasks are already assigned to this agent.':'No scheduled tasks found.');
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
    host.innerHTML=`<label>Saved agent<select id="task-assistant"><option value="">No agent</option>${data.items.map(p=>`<option value="${esc(p.id)}" ${p.id===owner?.id?'selected':''}>${esc(p.name)}</option>`).join('')}</select></label><p class="small-note">Groups this task and its results. The task keeps its saved instructions.</p><p id="task-assistant-status" role="status"></p>`;
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
    const key=JSON.stringify([state.chatMeta?.id,children,delegationLimit]);host.hidden=!children.length||window.auraInsight?.view()==='off';
    if(key===delegationKey)return;delegationKey=key;
    const opened=new Set([...host.querySelectorAll('details[open]')].map(d=>d.dataset.child));
    const labels={working:'Working',pending:'Starting',complete:'Completed',error:'Failed',stopped:'Stopped',unconfirmed:'Check result',partial:'Partial result'};
    const parents=new Set(children.map(c=>c.parent_id)),leaves=children.filter(c=>!parents.has(c.id));
    const done=leaves.filter(c=>c.status==='complete').length;
    const ids=new Set(children.map(c=>c.id));
    host.innerHTML=`<h3>Delegated work <span class="muted">${done} of ${leaves.length} completed</span></h3>${children.slice(0,delegationLimit).map(c=>`<details class="child-agent ${ids.has(c.parent_id)?'child-agent-nested':''}" data-child="${esc(c.id)}" ${opened.has(c.id)?'open':''}><summary><span>${esc(c.name)}${c.model?' · '+esc(c.model):c.requested_model?' · Requested: '+esc(c.requested_model):''}</span><span class="child-status ${c.status==='working'?'working':''}">${esc(labels[c.status]||c.status)}</span></summary><div class="child-agent-body">${c.task?`<p class="assistant-instructions">${esc(c.task)}</p>`:''}<p class="small-note">${esc(c.activity||'Delegated work')}</p>${c.result?`<div>${chatMarkdown(c.result)}</div>`:'<p class="muted">No result reported yet.</p>'}${c.result_truncated==='true'||c.task_truncated==='true'?'<p class="small-note">Showing a saved excerpt.</p>':''}<button type="button" class="text-button" data-child-activity="${esc(c.native_id||c.id)}">Activity</button>${state.chatMeta?.agent==='codex'?`<button type="button" class="text-button" data-result-native="${esc(c.id)}" data-result-owner="codex">Open in Codex</button>`:''}</div></details>`).join('')}${children.length>delegationLimit?'<button type="button" class="text-button" data-delegation-more>Show more agents</button>':''}${children.length-active.size>=50?'<p class="small-note">Showing active agents and recent history. Older work stays in your AI app.</p>':''}`;
  }
  async function startAssistant(id,draft=null){
    if(!await load())return;const p=profile(id);if(!p)return;const key=currentScope();await newShellChat(draft);if(key!==currentScope())return;
    const destination=chatScope(),nativeProfile=p.native_agent?.app==='hermes'?await api(nativeEndpoint(p.app,{action:'read',scope:'profile',file:p.native_agent.file})):null;
    if(key!==currentScope()||destination!==chatScope())return;
    state.newAssistantId=p.id;state.newAssistantName=p.name;
    const known=state.data.connection.presets?.[p.app],base=!p.app||p.app===composerConnection().kind?composerConnection():{model:'',effort:''};
    state.newChatConnection={...base,...(known||{}),...(p.app?{kind:p.app}:{}),...(nativeProfile?{native_profile:p.native_agent.file,model:nativeProfile.model,effort:''}:{}),...Object.fromEntries(['model','effort'].filter(k=>p[k]).map(k=>[k,p[k]]))};
    rememberChatDraft();renderComposerConnection();$('#request').focus();
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
    if(b.dataset.assistantRemove){const id=b.dataset.assistantRemove;details('Archive agent?',`<p>Chats, scheduled tasks, files, and results will stay available.</p><button type="button" class="secondary" data-assistant-edit="${esc(id)}">Keep agent</button> <button type="button" class="primary" data-confirm-assistant-remove="${esc(id)}">Archive agent</button>`);}
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
    attempt(async()=>{const button=form.querySelector('.primary');button.disabled=true;try{const data=Object.fromEntries(new FormData(form));if(window.auraInsight)data.context_refs=$('#agent-saved-context')?._references?.()||[];if(form.dataset?.detachNative==='true')data.native_agent=null;if($('#assistant-app').disabled)data.app=$('#assistant-app').value;const result=await api('/api/assistants',{business:state.business,...data});if(key!==currentScope())return;cache=result;scope=key;const p=data.id?profile(data.id):cache.items.at(-1);if(state.view==='assistants')await renderAssistants($('#section-content'));if(p)await overview(p.id);}catch(error){if(form.isConnected)$('#assistant-save-status').textContent=humanError(error);}finally{if(button.isConnected)button.disabled=false;}});
  });
  return {load,startAssistant,renderAssistants,overview,assignTask,chooseTask,history,openResult,renderDelegation,composer};
})();
