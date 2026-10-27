'use strict';
const $ = (s) => document.querySelector(s);
const token = $('meta[name="aura-token"]').content;
const state = {data:null, view:'home', business:new URLSearchParams(location.search).get('business') || '', library:[], files:[], chat:[], busy:false, urls:[], setupStep:'welcome', welcome:null, setupPrompted:new Set(), catalog:null, catalogLoading:false, chatMeta:null, polling:false, hydrated:false, tour:false, apiReturn:'', apiChanged:false};
const systemTheme=matchMedia('(prefers-color-scheme: dark)');
const nativeApps=['codex','claude','pi','omp','hermes','antigravity'];
function applyAppearance(value) { document.documentElement.dataset.theme=value==='system'?(systemTheme.matches?'dark':'light'):value; }
systemTheme.addEventListener('change',()=>applyAppearance(state.data?.appearance||'system'));
applyAppearance('system');
const esc = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const human = (s) => String(s).replace(/([a-z])([A-Z])/g,'$1 $2').replaceAll('_',' ').replace(/^./, c=>c.toUpperCase());
const pretty = (value) => typeof value === 'object' && value !== null ? (Array.isArray(value) ? value.map(pretty).join('\n') : Object.entries(value).map(([k,v])=>`${human(k)}: ${pretty(v)}`).join('\n')) : String(value ?? '');
const rows = (...types) => (state.data?.records || []).filter(r=>types.includes(r.type));
const stamp = value => value ? new Date(value).toLocaleDateString(undefined,{month:'short',day:'numeric'}) : 'Date not recorded';
const size = bytes => bytes < 1024 ? `${bytes} B` : bytes < 1048576 ? `${(bytes/1024).toFixed(0)} KB` : `${(bytes/1048576).toFixed(1)} MB`;
const clockTime = value => value ? new Date(typeof value==='number'?value*1000:value).toLocaleTimeString(undefined,{hour:'numeric',minute:'2-digit'}) : '';

async function api(path, data) {
  const response = await fetch(path,{method:data ? 'POST':'GET',headers:{'X-Aura-Token':token,...(data?{'Content-Type':'application/json'}:{})},...(data?{body:JSON.stringify(data)}:{})});
  const body = await response.json();
  if(!response.ok) {const error=new Error(body.error || 'Something could not be completed. Refresh and try again.');error.status=response.status;throw error;}
  return body;
}
function notice(text, error=false) {
  $('#notice').textContent=text; $('#notice').classList.toggle('error',error); $('#notice').hidden=!text;
  if(!error) document.querySelectorAll('.dialog-error').forEach(message=>message.remove());
  const dialog=document.querySelector('dialog[open]');
  if(error && dialog) {
    let message=dialog.querySelector('.dialog-error');
    if(!message) { message=document.createElement('p'); message.className='dialog-error'; message.setAttribute('role','alert'); dialog.append(message); }
    message.textContent=text;
  }
}
async function attempt(fn) { try { await fn(); } catch(error) { notice(error.message,true); } }
function empty(title, text, prompt) { return `<div class="empty"><strong>${esc(title)}</strong>${esc(text)}${prompt?`<div class="empty-cta"><button class="text-button" data-prompt="${esc(prompt)}">Ask your AI to help ↗</button></div>`:''}</div>`; }
function recordRow(r) { return `<button class="row" data-record="${esc(r.ref)}"><span class="row-icon">${r.type==='Asset'?'▧':r.type==='Objective'?'↗':'◈'}</span><span class="row-text"><span class="row-title">${esc(r.title)}</span><span class="row-meta">${esc(({Objective:'Goal',SourceRecord:'Saved source',PreferenceProfile:'Preferences',Observation:'Finding',ProofRecord:'Evidence',MetricObservation:'Measurement'})[r.type]||human(r.type))}${r.data.status?' · '+esc(human(r.data.status)):''}${r.data.updated_at?' · '+stamp(r.data.updated_at):''}</span></span><span class="arrow">↗</span></button>`; }
function heading(title, subtitle='') { return `<div class="section-head"><div><h2>${title}</h2>${subtitle?`<p>${subtitle}</p>`:''}</div></div>`; }

async function refresh() {
  $('#refresh').disabled=true;
  try {
    state.data=await api('/api/state'+(state.business?'?business='+encodeURIComponent(state.business):''));
    state.business=state.data.business_id || '';
    $('.composer').hidden=!state.business;
    $('#connection').disabled=!state.business;
    $('#chats').disabled=!state.business||state.busy;
    const workspaceOptions='<option value="" disabled>Choose a workspace</option>'+state.data.businesses.map(b=>`<option value="${esc(b.id)}">${esc(b.name)}</option>`).join('')+'<option value="__add__">＋ Add or open a workspace</option>';
    $('#business').innerHTML=workspaceOptions;$('#setup-workspace-select').innerHTML=workspaceOptions;
    $('#business').value=state.business;
    const business=rows('Business')[0];
    $('#business-name').textContent=business?.title || 'Your workspace';
    $('#setup-workspace-select').value=state.business;
    $('#business').hidden=false;$('#business-name').hidden=true;
    if(state.business){const url=new URL(location.href);url.searchParams.set('business',state.business);history.replaceState(null,'',url);}
    $('#version').textContent='AURA '+state.data.version;
    $('#appearance').value=state.data.appearance;
    applyAppearance(state.data.appearance);
    const connection=state.data.connection;
    $('#connection').disabled=false;$('#model-settings').disabled=false;
    $('#connection').disabled=!state.business;
    $('#model-settings').textContent=connection.model_controls?(connection.model?`${connection.model} · ${human(connection.effort||'App default')}${connection.selected==='codex'?(connection.workspace_write?' · Can edit files':' · Read only'):''}`:'Choose model & effort'):(connection.connected?'AI app settings':'Choose AI & model');
    $('#notification-bell').hidden=!state.business;
    $('#composer-context').textContent=connection.connected?'Uses your saved business context.':connection.mode==='copy'?'Requests are copied to your existing AI chat.':'Connect your AI to send requests from here.';
    $('#new-chat').disabled=!state.business||state.busy;
    $('#send').innerHTML=connection.connected?'Send <span>↑</span>':connection.mode==='copy'?'Copy request <span>↗</span>':'Connect AI <span>→</span>';
    const previousChoice=$('#agent-choice').value;
    $('#agent-choice').innerHTML=connection.choices.length?connection.choices.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}${c.available?'':' — needs setup'}</option>`).join(''):'<option value="">No supported app found</option>';
    if(connection.selected) $('#agent-choice').value=connection.selected;
    else if(previousChoice&&connection.choices.some(c=>c.id===previousChoice)) $('#agent-choice').value=previousChoice;
    else $('#agent-choice').value=connection.choices.find(c=>c.available)?.id||connection.choices[0]?.id||'';
    connectionChoice();
    $('#request').disabled=!state.business || !state.hydrated;
    $('#send').disabled=!state.business || !state.hydrated || state.stopping;
    if(state.data.diagnostics.length) notice('Some saved records could not be read. Ask your agent to inspect them before relying on a complete overview.',true);
    await render();
    if(state.business&&!state.hydrated) {state.hydrated=true;await hydrateConversation();}
    chatControls();
    if(state.business&&!state.data.onboarding.seen&&!state.setupPrompted.has(state.business)) {
      state.setupPrompted.add(state.business); openConnection();
    }
    await syncNotifications();
  } finally { $('#refresh').disabled=false; }
}

const providerLabel=id=>({openai:'OpenAI',anthropic:'Anthropic',google:'Google',xai:'xAI / Grok',openrouter:'OpenRouter',local:'Local models',other:'Other'})[id]||human(id);
const modelProvider=model=>model.access==='openrouter'?'openrouter':model.access==='local'?'local':model.access==='google-app'?'google':['openai','anthropic','google','xai'].includes(model.provider)?model.provider:'other';
const providerKey=model=>'connection:'+modelProvider(model);
const catalogModels=()=>state.catalog?.models||[];
const chosenModel=()=>catalogModels().find(m=>m.id===$('#model-choice').value);
const selectedRoute=()=>chosenModel()?.routes.find(r=>r.agent===$('#agent-choice').value);
const modelSource=model=>!model?'':model.access==='signin'?providerLabel(model.provider)+' sign-in':model.access==='api'?providerLabel(model.provider)+' API':model.access==='provider'?providerLabel(model.provider)+' connection':({openrouter:'OpenRouter',local:'Local model','google-app':'Google Antigravity'})[model.access]||'Configured in '+(model.routes.find(r=>r.agent===$('#agent-choice').value)?.app||'your AI app');
function connectionChoice() {
  const choice=state.data.connection.choices.find(c=>c.id===$('#agent-choice').value), route=selectedRoute();
  const native=nativeApps.includes(choice?.id), models=catalogModels();
  $('#choose-agent').disabled=!choice?.available||state.busy||state.checkingConnections;
  $('#connect-agent').disabled=state.busy||state.checkingConnections||state.catalogLoading||state.effortsLoading||!!state.modelError||(native?!route:!choice?.available);
  for(const id of ['model-fields','model-picker-controls','model-providers','favorite-model'])$('#'+id).hidden=!models.length;
  $('#favorite-model').hidden=!chosenModel();
  $('#refresh-models').hidden=!native;$('#refresh-models').disabled=state.catalogLoading||state.busy;
  $('#refresh-models').textContent=state.modelReload?'Reload page':state.modelError?'Try again':'Refresh';
  $('#model-app-name').textContent=choice?.name||'Your AI app';
  $('#agent-help').textContent=!choice||!choice.available?'Let’s finish connecting '+(choice?.name||'your AI app')+'.':'';
  $('#connection-guide').hidden=!!choice?.available||!choice?.guide;
  $('#connection-guide').innerHTML=choice?.guide?`<p>${esc(choice.guide[1])}</p><a class="text-button" href="${esc(choice.guide[0])}" target="_blank" rel="noopener noreferrer">Open ${esc(choice.name)} setup guide ↗</a><p class="small-note">When you’re signed in, click Check again below. If the app was just installed, reopen AURA so it can find the new command.</p>`:'';
  $('#model-help').textContent=state.catalogLoading?'Finding your models…':state.effortsLoading?'Reading effort levels…':state.modelError||(!models.length&&native?(state.catalog?.unavailable[0]?`${choice.name}: ${state.catalog.unavailable[0].reason} Try again or go Back to choose another app.`:'No models found. Add a key, or go Back to choose an AI app.'):'');
  $('#model-help').hidden=!$('#model-help').textContent;
  $('#model-help').classList.toggle('error',!!state.modelError);$('#model-help').setAttribute('role',state.modelError?'alert':'status');
  $('#connect-agent').textContent=state.data.onboarding.seen&&!state.tour?'Save & close':'Continue →';
}
async function loadAgentOptions(refresh=false) {
  const current=$('#model-choice').value;
  await pickerSave;
  state.modelError='';state.modelReload=false;state.catalogLoading=true;connectionChoice();
  try {
    const kind=$('#agent-choice').value;
    const [services,catalog]=await Promise.all([api('/api/connections'),!nativeApps.includes(kind)?Promise.resolve({kind,models:[],picker:{view:'all',favorites:[],providers:[],efforts:{}},unavailable:[]}):state.catalog?.kind===kind&&!refresh?Promise.resolve(state.catalog):api('/api/model-catalog?kind='+encodeURIComponent(kind)+(refresh?'&refresh=1':''))]);
    if($('#agent-choice').value!==kind)return;
    state.catalog=catalog;state.data.model_picker??={};
    if(!state.data.model_picker.all)state.data.model_picker.all={...structuredClone(catalog.picker),providers:[...new Set(catalog.models.map(providerKey))]};
    const added=services.items.filter(r=>r.category==='models'&&r.status!=='Not added').length;
    $('#model-api-connections').textContent='LLM connections'+(added?' · '+added+' added':' · Add key');
    const preferred=$('#agent-choice').value,saved=state.data.connection;
    const active=catalog.models.find(m=>m.routes.some(r=>r.agent===saved.selected&&r.model===saved.model));
    const defaultModel=catalog.models.find(m=>m.routes.some(r=>r.agent===preferred&&r.current));
    const selected=catalog.models.find(m=>m.id===current)||active||defaultModel||(preferred==='configured'?null:catalog.models[0]);
    renderModelChoices(selected?.id||'');await selectModel();
  } catch(error) {modelFailure(error);}
  finally {state.catalogLoading=false;connectionChoice();}
}
function modelFailure(error) {
  const text=error.message.toLowerCase();state.modelReload=error.status===403||error.status===404;
  state.modelError=state.modelReload?'This page needs refreshing. Reload AURA, then try again.':/sign.in|authentication|unauthorized|credentials|401/.test(text)?'Sign in to your AI app, then try again.':/network|timeout|timed out|connection|fetch/.test(text)?'Couldn’t load models. Check your connection, then try again.':'Couldn’t load models. Try again, or go Back to choose another AI app.';
  connectionChoice();
}
function modelPicker(){
  state.data.model_picker??={};const picker=state.data.model_picker.all??={view:'all',favorites:[],providers:[...new Set(catalogModels().map(providerKey))],efforts:{}};
  // Old maker filters become direct-provider filters; favorites and effort keys stay intact.
  if(picker.providers.some(id=>!id.startsWith('connection:')))picker.providers=[...new Set(picker.providers.map(id=>'connection:'+(['openai','anthropic','google','xai','openrouter','local'].includes(id)?id:'other')))];
  return picker;
}
function filteredModels(){
  const picker=modelPicker(),query=$('#favorite-search').value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  return catalogModels().filter(m=>(picker.view!=='favorites'||picker.favorites.includes(m.id))&&picker.providers.includes(providerKey(m))&&query.every(term=>`${m.name} ${providerLabel(m.provider)} ${providerLabel(modelProvider(m))} ${modelSource(m)} ${m.routes.map(r=>r.model).join(' ')}`.toLowerCase().includes(term)));
}
function groupLabel(model){return providerLabel(modelProvider(model));}
function renderModelChoices(current=$('#model-choice').value){
  const models=catalogModels();if(!models.length)return;
  const picker=modelPicker(),visible=filteredModels(),retained=models.find(m=>m.id===current&&!visible.some(v=>v.id===m.id));
  const groups=Object.groupBy(visible,groupLabel);
  $('#model-choice').innerHTML=($('#agent-choice').value==='configured'?'<option value="">Use my app’s settings</option>':'')+(retained?`<optgroup label="Current selection"><option value="${esc(retained.id)}">${esc(retained.name)} · ${esc(groupLabel(retained))}</option></optgroup>`:'')+Object.entries(groups).map(([label,items])=>`<optgroup label="${esc(label)}">${items.map(m=>`<option value="${esc(m.id)}">${picker.favorites.includes(m.id)?'★ ':''}${esc(m.name)}</option>`).join('')}</optgroup>`).join('');
  if(!current||models.some(m=>m.id===current))$('#model-choice').value=current;
  $('#model-list-view').value=picker.view;
  $('#model-list-note').textContent=`${visible.length} ${picker.view==='favorites'?'favorite':'matching'} model${visible.length===1?'':'s'}`;
  $('#provider-checkboxes').innerHTML=[...new Set(models.map(providerKey))].sort().map(id=>`<label class="check-label"><input type="checkbox" data-model-provider="${esc(id)}" ${picker.providers.includes(id)?'checked':''}>${esc(providerLabel(id.slice('connection:'.length)))}</label>`).join('');
  favoriteButton();renderFavoriteList();
}
function favoriteButton(){const model=chosenModel(),yes=modelPicker().favorites.includes(model?.id);$('#favorite-model').textContent=yes?'★':'☆';$('#favorite-model').setAttribute('aria-pressed',String(yes));$('#favorite-model').setAttribute('aria-label',(yes?'Unfavorite':'Favorite')+' selected model');$('#selected-model-name').textContent=model?.name||'Use my app’s settings';$('#selected-model-source').textContent=modelSource(model);}
function renderFavoriteList(){
  const found=filteredModels(),picker=modelPicker(),shown=[...found].sort((a,b)=>modelProvider(a).localeCompare(modelProvider(b))||a.name.localeCompare(b.name));let group='';
  $('#favorite-model-list').innerHTML=shown.map(m=>{const title=groupLabel(m),heading=title!==group?`<h3 class="model-group-title">${esc(title)}</h3>`:'';group=title;const yes=picker.favorites.includes(m.id),source=modelSource(m);return heading+`<div class="model-result"><button type="button" data-pick-model="${esc(m.id)}" aria-pressed="${m.id===$('#model-choice').value}">${esc(m.name)}<small>${esc(source)}</small></button><button type="button" data-favorite="${esc(m.id)}" aria-label="${yes?'Unfavorite':'Favorite'} ${esc(m.name)} · ${esc(source)}" aria-pressed="${yes}">${yes?'★':'☆'}</button></div>`;}).join('');
  $('#favorite-results-note').textContent=found.length?'':picker.view==='favorites'?'No matching favorites. Choose All models to get started.':'No matching models. Change your filters or connect another provider.';
}
let pickerSave=Promise.resolve();
async function saveModelPicker(){const payload={kind:'all',...structuredClone(modelPicker())};pickerSave=pickerSave.catch(()=>{}).then(()=>api('/api/preferences',{model_picker:payload}));await pickerSave;}
async function toggleFavorite(id){const picker=modelPicker();picker.favorites=picker.favorites.includes(id)?picker.favorites.filter(v=>v!==id):[...picker.favorites,id];renderModelChoices();await saveModelPicker();}
async function selectModel(){
  state.modelError='';const model=chosenModel();if(!model){$('#effort-choice').innerHTML='<option value="">App default</option>';$('#effort-choice').disabled=true;connectionChoice();return;}
  await effortOptions();
}
async function effortOptions(){
  const route=selectedRoute(),id=$('#model-choice').value;if(!route)return;
  state.effortsLoading=true;$('#effort-choice').disabled=true;$('#model-change-note').textContent='';$('#model-change-note').hidden=true;connectionChoice();
  try {
    if(route.discover_efforts&&!route.efforts_loaded){Object.assign(route,await api('/api/agent-efforts?kind='+encodeURIComponent(route.agent)+'&model='+encodeURIComponent(route.model)));route.efforts_loaded=true;}
    if(selectedRoute()?.key!==route.key||$('#model-choice').value!==id)return;
    const saved=state.data.connection,preferred=modelPicker().efforts?.[route.key]??(saved.selected===route.agent&&saved.model===route.model?saved.effort:'');
    $('#effort-choice').innerHTML=route.efforts.map(e=>`<option value="${esc(e)}">${esc(({xhigh:'Extra high',max:'Maximum'})[e]||human(e))}</option>`).join('')||'<option value="">App default</option>';
    $('#effort-choice').value=route.efforts.includes(preferred)?preferred:route.default_effort||route.efforts[0]||'';
    $('#model-change-note').textContent=route.agent!==saved.selected&&state.chat.length?`Continuing with ${route.app} starts a new chat. Your current chat is in ${saved.name}.`:'';
    $('#model-change-note').hidden=!$('#model-change-note').textContent;
  } finally {if(selectedRoute()?.key===route.key&&$('#model-choice').value===id){state.effortsLoading=false;$('#effort-choice').disabled=false;connectionChoice();}}
}
function openConnection(restart=false, step='welcome') {
  if(!state.data)return;
  $('#more-dialog').close();
  if(restart&&!state.busy) { state.setupStep=step; state.welcome=null; }
  renderConnection();
  if(!$('#connect-dialog').open) $('#connect-dialog').showModal();
  if(state.setupStep==='models')loadAgentOptions().catch(modelFailure);
}
function renderConnection() {
  const step=state.setupStep, ready=step==='ready', failed=step==='failed', checking=step==='checking';
  const stages={welcome:[1,'Welcome to AURA'],connect:[2,'Connect your AI'],models:[3,'Models & favorites'],tour:[4,'A quick look around'],checking:[5,'Checking connections'],ready:[5,'You’re ready'],failed:[5,'Connection needs attention']};
  const [number,title]=stages[step]||stages.welcome;
  $('#setup-step').textContent=`QUICK SETUP · ${number} OF 5`;
  $('#connect-title').textContent=title;
  for(const section of ['welcome','connect','models','tour'])$('#setup-'+section).hidden=step!==section;
  $('#setup-result').hidden=!['checking','ready','failed'].includes(step);
  $('#setup-progress').textContent=checking?'Finishing setup…':ready?'Your workspace is ready. Continue whenever you like.':state.connectionChecks?.message||'Your AI connection needs attention. Go back to choose an app, or select Fix connection to try again.';
  const checks=state.connectionChecks?.items||state.data.connection.apps||[];
  $('#app-connection-status').innerHTML=connectionStatusRows(state.checkingConnections?checks.map(c=>({...c,status:'checking',detail:'Checking…',checked_at:null})):checks);
  $('#app-connection-status').classList.toggle('many-apps',checks.length>2);
  $('#app-status-panel').hidden=!checks.length&&!state.connectionChecks?.message;
  $('#app-connection-message').hidden=!!checks.length||!state.connectionChecks?.message;
  $('#app-connection-message').textContent=state.connectionChecks?.message||'';
  $('#setup-welcome-message').hidden=!ready;
  $('#setup-progress').classList.toggle('setup-error',failed);
  $('#setup-done').hidden=!ready; $('#setup-retry').hidden=!failed;
  $('#setup-result-back').disabled=state.busy||state.checkingConnections;
  $('#first-task').hidden=!ready||!state.data.connection.connected;
  $('#first-task').disabled=state.busy;
  $('#welcome-request').disabled=state.busy||state.checkingConnections; connectionChoice();
  $('#welcome-model').textContent=`Your requests will use ${state.data.connection.model||state.data.connection.name} · ${human(state.data.connection.effort||'App default')}`;
}
function connectionStatusRows(items) {
  return items.map(c=>`<div class="connection-status-row"><span class="connection-status-icon ${c.status==='ready'?'ready':c.status==='error'?'error':'unchecked'}" aria-label="${c.status==='ready'?'Ready to send':c.status==='error'?'Needs attention':'Not checked'}">${c.status==='ready'?'✓':c.status==='error'?'✕':'○'}</span><span><strong>${esc(c.name)}</strong><small>${esc(c.detail||'Not checked yet.')}${c.checked_at?' · '+clockTime(c.checked_at):''}</small></span></div>`).join('');
}
async function checkConnections(showResult=true) {
  if(state.busy||state.checkingConnections)return;
  const business=state.business;state.checkingConnections=true;state.welcome=null;state.sendingWelcome=false;
  if(showResult)state.setupStep='checking';
  renderConnection();
  $('#check-connections').disabled=true;$('#welcome-request').disabled=true;
  try {
    const result=await api('/api/connection-check?business='+encodeURIComponent(business));
    if(state.business!==business)return;
    state.connectionChecks=result;state.data.connection.apps=result.items;
    if(showResult)state.setupStep=result.ready?'ready':'failed';
  }catch(error){if(state.business===business){state.connectionChecks={items:[],ready:false,message:'AURA could not check your connection. Make sure this workspace is still open, then try again.'};if(showResult)state.setupStep='failed';}}
  finally{state.checkingConnections=false;$('#check-connections').disabled=false;renderConnection();}
}
function finishSetup() {
  const connection=state.data.connection;
  const current=(state.connectionChecks?.items||connection.apps||[]).find(c=>c.id===connection.selected);
  const ready=state.connectionChecks?.files_ready!==false&&(current?.status==='ready'||connection.mode==='copy');
  state.connectionChecks={...state.connectionChecks,ready,message:state.connectionChecks?.files_ready===false?state.connectionChecks.message:current?.detail||state.connectionChecks?.message};
  state.setupStep=ready?'ready':'failed';
  renderConnection();
}
function simpleSetupError(message='') {
  const text=message.toLowerCase();
  if(text.includes('could not confirm workspace access'))return message;
  if(/payment required|insufficient balance|insufficient credits|out of credits|billing|\b402\b/.test(text))return 'Your AI provider needs credits or a billing update. Check billing or choose another connection, then try again.';
  if(/quota|rate.limit|credits|usage limit|429/.test(text))return 'Your AI account has reached a usage limit. Try another model or try again later.';
  if(/invalid_grant|oauth refresh failed|refresh token expired|refresh token revoked|refresh token has already been used/.test(text))return 'Your AI app needs you to sign in. Open it, sign in, and try again.';
  if(/api.key|authentication|unauthorized|credentials|401/.test(text))return 'Your AI connection needs valid credentials. Check its sign-in or API key, then try again.';
  if(/sign.in|login expired|token expired|token has expired/.test(text))return 'Your AI app needs you to sign in. Open it, sign in, and try again.';
  if(/permission denied:\s*['"]?(?:[a-z]:[\\/]|[/\\])|eacces|read.only file|\b(?:file|folder|directory)\b.{0,80}(permission|denied|not readable)|(?:permission|denied).{0,80}\b(file|folder|directory)\b/.test(text))return 'Your AI could not access this folder. Allow access in your AI app and try again.';
  if(/model.{0,100}(access|permission|denied|forbidden|not allowed)|(?:access|permission|denied|forbidden|not allowed).{0,100}model|\b403\b/.test(text))return 'Your account cannot use this model. Choose another model or check access with your provider.';
  if(/service unavailable|overloaded|no available endpoints|no endpoints found|\b50[234]\b/.test(text))return 'The AI service is temporarily unavailable. Try again later or choose another connection.';
  if(/network|timeout|timed out|connection|could not connect|unreachable|fetch/.test(text))return 'Your AI app could not connect. Check your connection and try again.';
  if(/model.{0,100}(not found|not available|unavailable|unsupported|does not exist)|(?:unsupported|unknown|unavailable) model|model_not_found/.test(text))return 'The selected model is unavailable. Refresh the model choices and choose another one.';
  if(/permission|denied|forbidden/.test(text))return 'Your AI app denied this request. Open the app to check its permissions, then try again.';
  return 'Your AI app did not finish connecting. Open the app to check what needs attention, then try again.';
}

async function dismissSetup() {
  if(state.connectionChecks?.ready){await api('/api/preferences',{business:state.business,dismiss_setup:true});state.data.onboarding.seen=true;}
  state.tour=false;
  $('#connect-dialog').close();
  $('#request').focus();
}
function taskStatus(text,elapsed='') {$('#chat-status').hidden=!text;if($('#task-status').textContent!==text)$('#task-status').textContent=text;$('#task-elapsed').textContent=elapsed?' · '+elapsed:'';}
function usageLabel(usage) {
  if(!usage||!Number.isFinite(usage.input_tokens)||!Number.isFinite(usage.output_tokens))return '';
  $('#task-status').title=`Reported session totals; ${Number(usage.cached_input_tokens||0).toLocaleString()} cached input tokens. These counts are not a price estimate.`;
  return ` · Session: ${(usage.input_tokens+usage.output_tokens).toLocaleString()} tokens`;
}
function renderNotifications() {
  const inbox=state.inbox||{items:[],unread:0}, count=inbox.unread;
  const signature=JSON.stringify([inbox,state.busy,window.Notification?.permission]);
  if(state.inboxSignature===signature)return; // Keep keyboard focus when polling finds no change.
  state.inboxSignature=signature;
  $('#notification-count').hidden=!count;$('#notification-count').textContent=count>99?'99+':count;
  $('#notification-bell').setAttribute('aria-label',count?`Notifications, ${count} unread`:'Notifications');
  document.title=count?`(${count}) AURA`:'AURA';
  $('#notification-read-all').disabled=!count;
  $('#notification-list').innerHTML=inbox.items.length?[...inbox.items].reverse().map(n=>`<button class="notification-item ${n.read?'':'unread'}" data-notification="${esc(n.id)}" ${state.busy&&n.chat_id!==state.chatMeta?.id?'disabled':''}><span class="notification-dot" aria-hidden="true"></span><span><strong>${n.status==='error'?'Needs your attention':'Reply ready'}</strong>${n.title?'<span class="notification-subject">'+esc(n.title)+'</span>':''}<small>${esc(n.agent)} · <time datetime="${new Date(n.at*1000).toISOString()}">${esc(new Date(n.at*1000).toLocaleString(undefined,{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'}))}</time>${n.read?'':' · Unread'}</small></span><span aria-hidden="true">→</span></button>`).join(''):'<p class="notification-empty">You’re all caught up. New replies will appear here.</p>';
  const supported=!!window.Notification, blocked=supported&&Notification.permission==='denied', enabled=inbox.enabled&&supported&&Notification.permission==='granted';
  $('#notification-system').textContent=enabled?'Mute system alerts':blocked?'System alerts blocked':supported?'Notify me when away':'In-app notifications only';
  $('#notification-system').disabled=!supported||blocked;
  $('#notification-permission').hidden=!blocked;
  $('#notification-permission').textContent=blocked?'Allow notifications in your browser’s site settings to get system alerts.':'';
}
async function syncNotifications(deliver=false) {
  if(!state.business||state.notificationLoading)return;
  state.notificationLoading=true;const business=state.business;
  try {
    const foreground=!document.hidden&&document.hasFocus();
    const inbox=await api('/api/notifications?business='+encodeURIComponent(business)+(foreground?'&foreground=1':''));
    if(state.business!==business)return;
    if(state.inbox?.unread!==undefined&&inbox.unread>state.inbox.unread)$('#notification-announcement').textContent=`${inbox.unread} unread notification${inbox.unread===1?'':'s'}.`;
    state.inbox=inbox;renderNotifications();
    if(deliver&&!foreground&&inbox.enabled&&window.Notification?.permission==='granted') {
      const batch=await api('/api/notifications',{business,action:'claim'});
      if(batch.claimed.length) {
        try {
          const n=new Notification('AURA',{body:batch.claimed.length===1?(batch.claimed[0].status==='error'?'A request needs your attention.':'Your reply is ready.'):`${batch.claimed.length} updates are ready.`,tag:'aura-'+state.data.workspace+'-'+business,silent:true,renotify:false});
          state.systemAlert?.close();state.systemAlert=n;
          n.onclick=()=>{window.focus();n.close();if(!$('#notification-dialog').open)$('#notification-dialog').showModal();};
        } catch { /* The inbox remains available when system delivery is unsupported. */ }
      }
    }
  } finally {state.notificationLoading=false;}
}
function replyAlert(result) {
  taskStatus(`${result.status==='stopped'?'Stopped. You can continue this chat.':result.status==='complete'?'Reply ready':'Needs your attention'} · ${clockTime(result.updated)}${usageLabel(result.usage)}`);
  syncNotifications(true).catch(()=>{});
}
async function hydrateConversation() {
  const result=await api('/api/conversation?business='+encodeURIComponent(state.business));
  state.chat=result.messages; state.chatMeta=result.chat;state.liveJob=result.job;showMessages();
  if(result.history_note)notice(result.history_note);
  if(result.job?.status==='working') {state.busy=true;state.setupStep=result.job.welcome?'checking':state.setupStep;attempt(()=>pollJob(result.job));}
  else if(result.job?.status==='error') {notice(result.job.reply,true);taskStatus(`Needs your attention · ${clockTime(result.job.updated)}`);}
  else if(result.job?.status==='stopped'||result.chat?.status==='stopped')taskStatus('Stopped. You can continue this chat.');
  else if(result.chat?.status==='error')taskStatus('The previous request did not complete. Review this chat in your AI app before retrying.');
  else if(state.chat.length)taskStatus(`Latest reply · ${clockTime(state.chat.at(-1).at)}${usageLabel(result.usage)}`);
  else if(result.chat?.status==='working')taskStatus('This chat was left working. Open it in your AI app to check the outcome before sending again.');
}
async function pollJob(job) {
  if(state.polling)return;state.polling=true;state.busy=true;
  state.activeJob=job;state.liveJob=job;chatControls();$('#business').disabled=true;$('#new-chat').disabled=true;
  showMessages();
  let finished=false;
  try {
    for(;;) {
      const result=await api('/api/chat?business='+encodeURIComponent(state.business)+'&id='+encodeURIComponent(job.id));
      state.liveJob=result;
      if(result.status==='working') {
        state.stopping=!!result.stopping;
        const elapsed=Math.max(0,Math.floor(Date.now()/1000-result.created));
        taskStatus(result.progress||'Waiting for your AI app',elapsed<60?elapsed+'s':Math.floor(elapsed/60)+'m '+elapsed%60+'s');
        showMessages();chatControls();await new Promise(resolve=>setTimeout(resolve,1000));continue;
      }
      finished=true;
      if(job.welcome) {state.welcome=result;state.setupStep=result.status==='complete'?'ready':'failed';}
      if(state.data.connection.native_sessions) {const conversation=await api('/api/conversation?business='+encodeURIComponent(state.business));state.chat=conversation.messages;state.chatMeta=conversation.chat;}
      else if(result.reply)state.chat.push({role:'assistant',text:result.reply,at:new Date().toISOString(),agent:state.data.connection.name});
      if(result.status==='error'&&!job.welcome)notice(result.reply,true);
      if(result.preference_warning)notice(result.preference_warning,true);
      replyAlert(result);break;
    }
  } catch(error) {if(job.welcome){state.setupStep='failed';state.welcome={reply:error.message};}taskStatus('Connection interrupted. Reopen this chat before sending again.');if(!job.welcome)notice(error.message,true);}
  finally {
    state.busy=false;state.polling=false;state.stopping=false;state.activeJob=null;state.settling=true;
    $('#business').disabled=false;showMessages();
    try {await refresh();renderConnection();} finally {state.settling=false;chatControls();}
    const next=state.nextRequest;state.nextRequest=null;
    if(next){$('#request').value=next;if(finished)await submitRequest(next);else notice('Your update has not been sent. Reconnect to check the previous request, then send it when you’re ready.',true);}
  }
}
function chatControls() {
  $('#request').disabled=!state.business||state.stopping;
  $('#request').placeholder=state.busy?'Add a correction or change direction…':'Ask a question or describe what you need…';
  $('#send').disabled=!state.business||state.stopping||state.starting||state.settling;
  $('#send').textContent=state.stopping?'Stopping…':state.busy?'Stop & send ↑':'Send ↑';
  $('#stop-request').hidden=!state.busy;
  $('#stop-request').disabled=state.stopping;
  $('#stop-request').textContent=state.stopping?'Stopping…':'Stop';
}
async function stopRequest() {
  if(!state.activeJob||state.stopping)return;
  state.stopping=true;chatControls();
  try {await api('/api/chat/stop',{business:state.business,id:state.activeJob.id});}
  catch(error){state.stopping=false;state.nextRequest=null;chatControls();throw error;}
}
function goalSection(limit=4) {
  const goals=rows('Objective');
  return `<div class="section-head"><h2>Goals</h2><button class="text-button" data-action="add-goal">＋ Add</button></div><div class="card">${goals.length?goals.slice(0,limit).map(r=>`<button class="row" data-record="${esc(r.ref)}"><span class="row-text"><span class="row-title">${esc(r.title)}</span></span><span class="arrow">→</span></button>`).join(''):empty('What are you working toward?','Add a goal when you’re ready.')}</div>${goals.length>limit?'<button class="text-button" data-view="business">See all goals →</button>':''}`;
}
function usefulFile(f) {
  return !!f.location || f.path.startsWith('attachments/') || f.path.startsWith(`knowledge/${state.business}/notes/`) || rows('Asset').some(r=>r.data.location_reference===f.path);
}
async function overview() {
  const [fileData, libraryData, schedules]=await Promise.all([api('/api/files?business='+encodeURIComponent(state.business)),state.library.length?Promise.resolve(state.library):api('/api/library'),api('/api/schedules').catch(()=>({items:[],notes:['Schedules could not be read. Try refreshing.']}))]);
  state.files=fileData.items;state.fileLocations=fileData.locations||[]; state.library=libraryData;state.schedules=schedules;
  const recent=state.files.filter(usefulFile).sort((a,b)=>b.modified-a.modified).slice(0,3);
  const goals=rows('Objective');
  const context=rows('Brand','Offer','AudienceSegment','Competitor','Insight','Learning','PreferenceProfile','SourceRecord').filter(r=>r.data.source_type!=='organization_initialization_input');
  const watches=rows('SourceProfile').filter(r=>r.data.watch_status||r.data.next_check_at);
  const attention=rows('AttentionItem','WorkRequest','Incident').filter(r=>!['resolved','completed','archived','closed'].includes(r.data.status));
  const defaults=[state.library.find(r=>r.kind==='Workflow'&&r.title==='Pricing Intelligence'),state.library.find(r=>r.kind==='Workflow'&&/Brand Profile/i.test(r.title)),state.library.find(r=>r.kind==='Recipe')].filter(Boolean);
  $('#view').innerHTML=`<div class="workspace-heading"><h2>Your workspace</h2><p>Keep the context. Find the work. Choose what to do next.</p></div><div class="workspace-grid">
    <section class="workspace-card" aria-labelledby="business-card-title"><div class="card-heading"><h3 id="business-card-title">Business & memory</h3><button class="text-button" data-view="business">Open →</button></div><p class="card-description">Your goals, research, preferences, and decisions.</p><div class="mini-heading"><span>Goals</span><button class="text-button" data-action="add-goal">＋ Add</button></div>${goals.length?goals.slice(0,2).map(r=>`<button class="row compact" data-record="${esc(r.ref)}"><span class="row-text"><span class="row-title">${esc(r.title)}</span></span><span class="arrow">→</span></button>`).join(''):'<p class="muted">Add a goal to give your work a direction.</p>'}${context.length?`<div class="context-preview"><span class="muted">Saved context</span>${context.slice(0,1).map(recordRow).join('')}</div>`:'<button class="text-button card-link" data-prompt="Help me add the business context we need for our next task. Ask only what matters, use what is already saved, and remember my explicit facts and preferences in AURA.">Add business information →</button>'}</section>
    <section class="workspace-card" aria-labelledby="files-card-title"><div class="card-heading"><h3 id="files-card-title">Saved files & media</h3><button class="text-button" data-view="files">Browse →</button></div><p class="card-description">Open the notes, images, and work you’ve kept.</p>${recent.length?recent.map(f=>`<button class="row file-preview-row" data-file="${esc(f.path)}"><span class="preview-icon" data-thumbnail="${esc(f.path)}">${f.media?'◈':'▤'}</span><span class="row-text"><span class="row-title">${esc(f.name)}</span><span class="row-meta">${size(f.bytes)} · ${stamp(f.modified*1000)}</span></span><span class="arrow">→</span></button>`).join(''):'<p class="empty">Your saved work will appear here.</p>'}<button class="text-button card-link" data-add-location>＋ Add files or folder</button></section>
    <section class="workspace-card" aria-labelledby="methods-card-title"><div class="card-heading"><h3 id="methods-card-title">Workflows & recipes</h3><button class="text-button" data-view="work">Browse →</button></div><p class="card-description">Find a useful method, or let your AI choose.</p><label class="sr-only" for="quick-work-search">Find a workflow or recipe</label><input id="quick-work-search" class="search" type="search" placeholder="Try competitors, content, or a website…"><div class="library-choices"><button class="secondary" data-library-kind="Workflow"><strong>Workflows</strong><small>Steps for getting business work done</small></button><button class="secondary" data-library-kind="Recipe"><strong>Recipes</strong><small>Creative and production guidance</small></button></div><div id="quick-methods"></div></section>
    <section class="workspace-card" aria-labelledby="tasks-card-title"><div class="card-heading"><h3 id="tasks-card-title">Recurring tasks</h3><button class="text-button" data-view="tools">Open →</button></div><p class="card-description">See scheduled work across your AI apps.</p>${schedules.items.length?schedules.items.slice(0,2).map(scheduleRow).join(''):watches.length?watches.slice(0,2).map(recordRow).join(''):'<div class="recurring-empty"><span class="schedule-icon">↻</span><p>No recurring tasks yet.</p></div>'}<button class="secondary" data-view="tools">＋ Create a recurring task</button><p class="small-note">${schedules.notes.length?'Some schedules could not be read. Open to check.':watches.length&&!schedules.items.length?'Saved plans are not active schedules.':'Each task stays with the app that runs it.'}</p></section>
  </div>${attention.length?heading('Needs your attention')+`<div class="card">${attention.slice(0,2).map(recordRow).join('')}</div>`:''}`;
  state.overviewAt=state.data.refreshed;
  for(const file of recent.filter(f=>/\.(png|jpe?g|webp|gif|avif)$/i.test(f.path)&&f.bytes<=8*1048576)) {
    try {const url=await mediaBlob(file.path);const holder=[...$('#view').querySelectorAll('[data-thumbnail]')].find(el=>el.dataset.thumbnail===file.path);if(holder){const img=document.createElement('img');img.alt='';img.src=url;holder.replaceChildren(img);}} catch { /* Original file remains available. */ }
  }
}
function methodRow(method) {return `<button class="row compact" data-method="${esc(method.path)}"><span class="row-text"><span class="row-title">${esc(method.title)}</span><span class="row-meta">${esc(method.kind)}</span></span><span class="arrow">→</span></button>`;}
function quickMethods() {
  const q=($('#quick-work-search')?.value||'').trim().toLowerCase();
  if(!q){$('#quick-methods').innerHTML='';return;}
  const groups=['Workflow','Recipe'].map(kind=>({kind,items:state.library.filter(r=>r.kind===kind&&(r.title+' '+r.category+' '+r.group+' '+(r.id||'')).toLowerCase().includes(q))}));
  $('#quick-methods').innerHTML=groups.filter(g=>g.items.length).map(g=>`<h4>${g.kind==='Workflow'?'Workflows':'Recipes'}</h4>${g.items.slice(0,3).map(methodRow).join('')}<button class="text-button card-link" data-library-kind="${g.kind}">Browse ${g.kind==='Workflow'?'workflows':'recipes'} →</button>`).join('')||'<p class="muted">No match. You can still describe the job to your AI.</p>';
}
async function render() {
  state.urls.forEach(URL.revokeObjectURL); state.urls=[];
  if(!state.business){state.view='home';$('#section-dialog').close();}
  const view=state.view==='home'?$('#view'):$('#section-content');
  if(!state.business) {
    view.innerHTML=`<div class="setup-intro"><h1>What would you like to call your workspace?</h1><p class="muted">Your business name is a good place to start. You can change it later.</p><form id="setup-form" class="form-grid"><label>Workspace or business name<input name="name" required maxlength="160" autocomplete="organization"></label><button class="primary">Get started →</button></form><button class="text-button" id="open-existing-start">Open an existing workspace →</button></div>`;
    return;
  }
  if(state.view==='home'||state.overviewAt!==state.data.refreshed) await overview();
  if(state.view==='home') { $('#section-dialog').close(); return; }
  $('#section-title').textContent=({business:'Business & memory',files:'Saved files & media',work:'Workflows & recipes',tools:'Recurring tasks'})[state.view];
  if(!$('#section-dialog').open) $('#section-dialog').showModal();
  if(state.view==='business') {
    view.innerHTML=`<div class="section-head business-title"><h3>${esc(rows('Business')[0]?.title)}</h3><button class="text-button" data-action="edit-business">Edit name</button></div>`+goalSection(Number.MAX_SAFE_INTEGER)+`<div class="section-head"><h2>About your business</h2><button class="text-button" data-prompt="Help me add useful business context to AURA. Ask only what matters for our current work and preserve my explicit facts and preferences. Do not invent facts.">＋ Add information</button></div><input class="search" id="record-search" type="search" aria-label="Search business information" placeholder="Find something you’ve saved…"><div id="memory-list" class="card"></div><details><summary>All saved information</summary><div class="card">${state.data.records.map(recordRow).join('')}</div></details>`;
    renderMemory();
  } else if(state.view==='files') {
    const result=await api('/api/files?business='+encodeURIComponent(state.business)); state.files=result.items;state.fileLocations=result.locations||[];fileFilter='work';fileLocation='';
    view.innerHTML=`<div class="section-head"><p>Workspace files and the locations you’ve linked.</p><button class="secondary" data-add-location>＋ Add files or folder</button></div><div class="linked-locations">${state.fileLocations.map(l=>`<div class="linked-location"><button data-filelocation="${esc(l.id)}"><strong>${esc(l.name)}</strong><small>${l.missing?'Location missing':l.kind==='folder'?'Linked folder':'Linked file'}</small></button><button data-unlink-location="${esc(l.id)}" aria-label="Unlink ${esc(l.name)}">✕</button></div>`).join('')}</div><input class="search" id="file-search" type="search" aria-label="Search saved files" placeholder="Find a file…"><div class="filters"><button class="active" data-filefilter="work">All saved</button><button data-filefilter="media">Images & media</button><button id="file-all-locations" class="text-button" hidden>All locations</button></div><div id="file-list" class="file-grid"></div><details><summary>Browse workspace records</summary><button class="secondary" data-filefilter="all">Show workspace records too</button></details>${result.limited?'<p class="muted">This view is limited to the first 1,000 workspace files and 1,000 linked files. Your AI can search the original folders for more.</p>':''}`;
    renderFiles();
  } else if(state.view==='work') {
    if(!state.library.length) state.library=await api('/api/library');
    view.innerHTML=`<input class="search" id="work-search" type="search" aria-label="Search workflows and recipes" placeholder="Try competitor research, SEO, a website…"><div class="filters"><button class="${workFilter==='Workflow'?'active':''}" data-workfilter="Workflow">Workflows</button><button class="${workFilter==='Recipe'?'active':''}" data-workfilter="Recipe">Recipes</button></div><div class="section-head"><h3 id="work-category-title">Browse by topic</h3><button id="work-all-topics" class="text-button" hidden>All topics</button></div><div id="work-categories" class="topic-grid"></div><div id="work-list"></div>`;
    renderWork();
  } else if(state.view==='tools') {
    const watches=rows('SourceProfile').filter(r=>r.data.watch_status||r.data.next_check_at);
    const schedules=state.schedules||{items:[],notes:[]};
    view.innerHTML=`<div class="section-head"><p>Schedules across your AI apps, regardless of your current chat.</p><button class="text-button" id="refresh-schedules">Refresh</button></div><div id="schedule-list" class="card">${schedules.items.length?schedules.items.map(scheduleRow).join(''):empty('No native schedules found.','Create a recurring task below. Your AI will confirm when it is active.')}</div>${schedules.notes.length?`<p class="error">${schedules.notes.map(esc).join('<br>')}</p>`:''}<details class="schedule-support"><summary>Connected schedulers</summary><p class="muted">${esc(schedules.support||'Schedule discovery is unavailable.')}</p></details><h3>Create a recurring task</h3><form class="form-grid" id="schedule-form"><label>What should happen?<input name="job" required maxlength="2000" placeholder="Check competitor pricing"></label><label>When?<input name="when" required maxlength="300" placeholder="Every Monday at 9am"></label><button class="primary">Send to AI →</button></form>`+(watches.length?heading('Saved monitoring plans','These are business plans, not proof of an active schedule.')+`<div class="card">${watches.map(recordRow).join('')}</div>`:'');
  }
}

let fileFilter='work', fileLocation='', workFilter='Workflow', workCategory='';
function renderMemory() {
  const q=($('#record-search')?.value||'').toLowerCase();
  const list=state.data.records.filter(r=>!['Business','Objective'].includes(r.type)&&(q||r.data.source_type!=='organization_initialization_input')&&(r.title+' '+pretty(r.data)).toLowerCase().includes(q));
  $('#memory-list').innerHTML=list.length?list.map(recordRow).join(''):empty('Nothing saved here yet.','Add information, or let your AI learn through your work.');
}
function mediaURL(path) { return '/api/media?business='+encodeURIComponent(state.business)+'&path='+encodeURIComponent(path); }
async function mediaBlob(path) {
  const response=await fetch(mediaURL(path),{headers:{'X-Aura-Token':token}});
  if(!response.ok) throw new Error((await response.json()).error);
  const url=URL.createObjectURL(await response.blob()); state.urls.push(url); return url;
}
function renderFiles() {
  const q=($('#file-search')?.value||'').toLowerCase();
  const assets=new Set(rows('Asset').map(r=>r.data.location_reference));
  const matches=state.files.filter(f=>(!fileLocation||f.location===fileLocation)&&(fileFilter==='all'||(fileFilter==='media'?f.media:(f.location||f.path.startsWith('attachments/')||f.path.startsWith(`knowledge/${state.business}/notes/`)||assets.has(f.path))))&&(f.path+' '+f.name+' '+(f.location_name||'')).toLowerCase().includes(q));
  $('#file-list').innerHTML=matches.length?matches.map(f=>`<button class="file-card" data-file="${esc(f.path)}"><span class="file-thumb">${f.media?'◈':'▤'}</span><div class="file-info"><strong>${esc(f.name)}</strong><small>${esc(f.location_name||'Workspace')} · ${size(f.bytes)}</small></div></button>`).join(''):empty('No matching files here yet.','Link a file or folder, or save work in this workspace.');
  let loaded=0;
  const observer=new IntersectionObserver(entries=>entries.forEach(async entry=>{
    if(!entry.isIntersecting) return;
    observer.unobserve(entry.target);
    const file=state.files.find(f=>f.path===entry.target.dataset.file);
    if(loaded>=24||!file||file.bytes>8*1048576||! /\.(png|jpe?g|gif|webp|avif)$/i.test(file.path)) return;
    loaded++;
    try { const url=await mediaBlob(file.path); if(!entry.target.isConnected) return; const img=document.createElement('img'); img.alt=''; img.src=url; entry.target.querySelector('.file-thumb').replaceChildren(img); } catch { /* File location remains usable if a thumbnail is unavailable. */ }
  }));
  $('#file-list').querySelectorAll('.file-card').forEach(e=>observer.observe(e));
}
function renderWork() {
  $('#section-title').textContent=workFilter==='Recipe'?'Recipes':'Workflows';
  $('#work-search').setAttribute('aria-label',workFilter==='Recipe'?'Search recipes':'Search workflows');
  $('#work-search').placeholder=workFilter==='Recipe'?'Find a recipe…':'Find a workflow…';
  document.querySelectorAll('[data-workfilter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.workfilter===workFilter)));
  const q=($('#work-search')?.value||'').toLowerCase();
  const matches=state.library.filter(r=>r.kind===workFilter&&(r.title+' '+r.category+' '+r.group+' '+r.area+' '+(r.id||'')).toLowerCase().includes(q));
  const categories=Object.groupBy(matches,r=>r.category);
  $('#work-categories').hidden=!!workCategory;
  $('#work-categories').innerHTML=Object.entries(categories).sort(([a],[b])=>a.localeCompare(b)).map(([name,items])=>`<button class="topic-card ${name===workCategory?'active':''}" data-workcategory="${esc(name)}" aria-pressed="${name===workCategory}"><strong>${esc(name)}</strong><small>${items.length} ${workFilter==='Recipe'?'recipes':'workflows'}</small></button>`).join('');
  $('#work-category-title').textContent=workCategory||'Browse by topic';$('#work-all-topics').hidden=!workCategory;
  const shown=matches.filter(r=>!workCategory||r.category===workCategory);
  const groups=Object.groupBy(shown,r=>(workCategory?'':r.category+' · ')+r.group);
  $('#work-list').innerHTML=(!q&&!workCategory)?'':Object.entries(groups).sort(([a],[b])=>a.localeCompare(b)).map(([name,items])=>`<details class="method-group" ${q?'open':''}><summary>${esc(name)}<span>${items.length}</span></summary>${items.sort((a,b)=>a.title.localeCompare(b.title)).map(methodRow).join('')}</details>`).join('')||empty('No matching methods.','Try another topic or search.');
}

function addLocation() {
  details('Add files or a folder',`<p>Link something already on your computer. Your files stay where they are.</p><form id="location-form" class="form-grid"><div class="inline-actions"><button type="button" class="secondary" data-browse-location="folder">Choose folder</button><button type="button" class="secondary" data-browse-location="file">Choose file</button></div><label>File or folder location<input name="path" id="location-path" required maxlength="2000" placeholder="Or paste its full location"></label><label>Name <span class="muted">(optional)</span><input name="name" maxlength="100" placeholder="Ads, brand images, documents…"></label><button class="primary">Add to this workspace</button></form>`);
}
function scheduleRow(task) {
  return `<button class="row" data-schedule="${esc(task.id)}"><span class="row-text"><span class="row-title">${esc(task.name)}</span><span class="row-meta">${esc(task.app)} · ${esc(task.model||'App default model')} · ${esc(task.status)}</span><span class="row-meta">${esc(task.schedule||'Schedule managed in app')}</span></span><span>→</span></button>`;
}
function taskTiming(task) {
  const raw=task.schedule_raw||task.schedule||'', cron=raw.match(/^(\d{1,2}) (\d{1,2}) \* \* ([0-6]|\*)$/), interval=raw.match(/^every (\d+)(m|h|d)$/);
  const mode=cron?(cron[3]==='*'?'daily':'weekly'):interval?'interval':'custom';
  const time=cron?cron[2].padStart(2,'0')+':'+cron[1].padStart(2,'0'):'09:00';
  return `<input name="schedule" id="task-schedule-value" type="hidden" value="${esc(raw)}"><label>When<select id="task-cadence">${[['daily','Every day'],['weekly','Every week'],['interval','Repeat at an interval'],['custom','Custom schedule']].map(([value,name])=>`<option value="${value}" ${mode===value?'selected':''}>${name}</option>`).join('')}</select></label><div class="task-timing" id="task-clock-fields" ${['daily','weekly'].includes(mode)?'':'hidden'}><label id="task-day-field" ${mode==='weekly'?'':'hidden'}>Day<select id="task-day">${['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'].map((d,i)=>`<option value="${i}" ${String(i)===(cron?.[3]||'1')?'selected':''}>${d}</option>`).join('')}</select></label><label>Time<input type="time" id="task-time" value="${time}" required></label></div><div class="task-timing" id="task-interval-fields" ${mode==='interval'?'':'hidden'}><label>Every<input id="task-every" type="number" min="1" max="10000" value="${interval?.[1]||1}"></label><label>Unit<select id="task-unit">${[['m','Minutes'],['h','Hours'],['d','Days']].map(([v,n])=>`<option value="${v}" ${v===(interval?.[2]||'h')?'selected':''}>${n}</option>`).join('')}</select></label></div><label id="task-custom-field" ${mode==='custom'?'':'hidden'}>Schedule<input id="task-custom" value="${esc(raw)}" maxlength="500"></label><p class="small-note">Uses the scheduler’s timezone.</p>`;
}
function updateTaskTiming() {
  const mode=$('#task-cadence').value;
  $('#task-clock-fields').hidden=!['daily','weekly'].includes(mode);$('#task-day-field').hidden=mode!=='weekly';$('#task-interval-fields').hidden=mode!=='interval';$('#task-custom-field').hidden=mode!=='custom';
  const [hour,minute]=$('#task-time').value.split(':');
  $('#task-schedule-value').value=mode==='custom'?$('#task-custom').value:mode==='interval'?`every ${$('#task-every').value}${$('#task-unit').value}`:`${Number(minute)} ${Number(hour)} * * ${mode==='weekly'?$('#task-day').value:'*'}`;
}
async function scheduleDetails(id) {
  const task=state.schedules.items.find(t=>t.id===id);if(!task)return;
  state.editingTask=task;
  details(task.name,`<p class="muted">${esc(task.app)} · ${esc(task.status)}${task.next_run?' · Next: '+esc(task.next_run):''}</p><form id="task-edit-form" class="form-grid"><label>AI app<select name="app">${state.data.connection.choices.filter(c=>c.available||c.id===task.owner).map(c=>`<option value="${esc(c.id)}" ${c.id===task.owner?'selected':''}>${esc(c.name)}</option>`).join('')}</select></label><label>Task name<input name="name" value="${esc(task.name)}" maxlength="200" required></label>${taskTiming(task)}<label>Model<select name="model" id="task-model"><option value="">App default</option>${task.model?`<option value="${esc(task.provider?task.provider+':'+task.model:task.model)}" selected>${esc(task.model)}</option>`:''}</select><small class="muted" id="task-model-note"></small></label><div class="inline-actions"><button class="primary">${task.editable?'Save changes':'Ask AI to adjust'}</button>${task.editable?`<button type="button" class="secondary" data-task-status="${task.status==='paused'?'resume':'pause'}">${task.status==='paused'?'Resume':'Pause'}</button>`:''}</div><p class="small-note" id="task-edit-note">${task.editable?'Changes are saved through the native scheduler.':'This app requires its native scheduling controls. Your AI will need to confirm any change there.'}</p></form>`);
  await taskModels(task.owner);
}

async function taskModels(app) {
  const select=$('#task-model');if(!select)return;
  const current=app===state.editingTask.owner?select.value:'';select.disabled=true;$('#task-model-note').textContent='Finding models…';
  try {
    const options=await api('/api/agent-options?kind='+encodeURIComponent(app));
    if(!select.isConnected||$('#task-edit-form select[name=app]').value!==app)return;
    const retained=select.querySelector('option:checked')?.outerHTML||'';
    select.innerHTML='<option value="">App default</option>'+(current&&!options.models.some(m=>m.id===current)?retained:'')+options.models.map(m=>`<option value="${esc(m.id)}">${esc(m.name)}</option>`).join('');
    select.value=[...select.options].some(o=>o.value===current)?current:'';
    $('#task-model-note').textContent='';
  }catch{if(select.isConnected)$('#task-model-note').textContent='Couldn’t load other models. The current setting is unchanged.';}
  finally{if(select.isConnected&&$('#task-edit-form select[name=app]').value===app)select.disabled=false;}
}
function details(title, html) { $('#detail-title').textContent=title; $('#detail-content').innerHTML=html; $('#detail').showModal(); }
let apiConnections=[];
async function showApiConnections(origin=state.apiReturn) {
  state.apiReturn=origin;
  const result=await api('/api/connections');apiConnections=result.items;
  $('#more-dialog').close();
  const services=result.items.filter(r=>origin!=='models'||r.category==='models');
  const saved=services.filter(r=>r.status!=='Not added');
  details(origin==='models'?'LLM connections':'API connections',`${origin==='models'?'<button class="text-button" id="back-to-models">← Back to models</button>':''}<p>${origin==='models'?'Add a provider key, then return to your models.':'Add services your AI can use for research, writing, images, video, or audio. Provider usage may be billed separately.'}</p>
    ${saved.length?`<div class="card">${saved.map(r=>`<div class="row"><span class="row-text"><span class="row-title">${esc(r.name)}</span><span class="row-meta">${esc(r.status)} · Not verified</span></span>${r.saved?`<button class="text-button" data-remove-api="${esc(r.id)}">Remove</button>`:''}</div>`).join('')}</div>`:''}
    ${result.storage_note?`<p class="small-note" role="status">${esc(result.storage_note)}</p><button type="button" id="session-keys-only" class="secondary">Continue without saved keys</button>`:''}<form id="api-key-form" class="form-grid" autocomplete="off"><label>Service<select id="api-provider" name="provider" required><option value="">Choose a service</option>${services.filter(r=>!r.id.startsWith('custom-')).map(r=>`<option value="${esc(r.id)}">${esc(r.name)}</option>`).join('')}<option value="other">${origin==='models'?'Other LLM provider':'Other service'}</option></select></label><input type="hidden" name="category" value="${origin==='models'?'models':'tools'}">
    <div id="custom-api-fields" class="form-grid" hidden><label>Service name<input name="name" maxlength="80"></label><label>API key variable<input name="env" placeholder="SERVICE_API_KEY" spellcheck="false" autocomplete="off"></label></div>
    <p id="api-provider-help" class="small-note"></p><label>API key<input id="api-secret" name="key" type="password" required maxlength="8192" autocomplete="new-password" spellcheck="false" autocapitalize="none" placeholder="Paste your API key"></label>
    <label>Keep this key<select name="storage"><option value="computer" ${result.persistent?'':'disabled'}>${result.persistent?'On this computer · '+esc(result.storage_name):'On this computer · unavailable on this system'}</option><option value="session" ${!result.persistent||result.storage_note?'selected':''}>This session only</option></select></label>
    <button class="primary" type="submit">Save key</button></form>
    <p id="api-save-status" role="status"></p><details><summary>How this works</summary><p>Keys stay out of your business files and chat prompts. The local server passes them to agent tools as environment variables. The agent still needs suitable tools and provider access. Saving a key does not make a generation request or verify an account.</p><p>Choosing a model remains separate. Codex is an AI app; OpenAI is its provider. OpenRouter is a provider gateway, while OpenCode is a separate AI app. Existing app sign-ins and provider routing remain under that app’s control.</p><p>${result.persistent?'Keys are kept in '+esc(result.storage_name)+'. Your operating system controls access.':'Persistent protected storage is not available here; session keys disappear when the local server closes.'} Removing a key here does not revoke it at the provider or remove keys set outside AURA.</p></details>`);
}
function apiProviderHelp() {
  const id=$('#api-provider').value, item=apiConnections.find(r=>r.id===id);
  $('#custom-api-fields').hidden=id!=='other';
  $('#api-provider-help').innerHTML=item?`<a href="${esc(item.url)}" target="_blank" rel="noreferrer">Get or manage your ${esc(item.name)} API key ↗</a>${id==='higgsfield'?'<br>Paste the complete key exactly as copied.':''}`:id==='other'?'Use the environment variable documented by your service.':'';
}
function recordDetails(ref) {
  const r=state.data.records.find(r=>r.ref===ref); if(!r) return;
  if(r.type==='SourceRecord') {
    const text=r.data.extensions?.businessos_evidence?.captured_text;
    details(r.title,`${text?'<pre>'+esc(text)+'</pre>':'<p>'+esc(r.data.source_reference||'Saved source')+'</p>'}<button class="text-button" data-prompt="${esc(`Use the saved AURA source ${r.ref} to help with our current work. Read the actual source and distinguish its claims from established facts.`)}">Use with your AI →</button><details><summary>File details</summary><p>${esc(r.path)}</p><pre>${esc(JSON.stringify(r.data,null,2))}</pre></details>`);
    return;
  }
  const mechanical=new Set(['id','object_type','schema_version','business_id','lineage','created_at','updated_at','extensions']);
  const fields=Object.entries(r.data).filter(([k,v])=>!mechanical.has(k)&&!['name','title'].includes(k)&&v!==null&&!(Array.isArray(v)&&!v.length));
  details(r.title,`<p>${r.type==='Objective'?'Goal':esc(human(r.type))}</p>${fields.map(([k,v])=>`<div class="field"><strong>${esc(human(k))}</strong><p>${esc(pretty(v))}</p></div>`).join('')}${r.type==='Objective'?`<form id="edit-goal-form" class="form-grid" data-ref="${esc(r.ref)}"><label>Update this goal<input name="name" value="${esc(r.title)}" required maxlength="2000"></label><button class="primary">Save goal</button></form>`:''}<p><button class="text-button" data-prompt="${esc(`Help me work with the saved AURA record ${r.ref}: ${r.title}. Read the actual record and ask only what is necessary.`)}">Work with your AI ↗</button></p><details><summary>File details</summary><p>${esc(r.path)}</p><pre>${esc(JSON.stringify(r.data,null,2))}</pre></details>`);
}
async function fileDetails(path) {
  const f=state.files.find(f=>f.path===path); if(!f) return;
  details(f.name,`<div id="file-preview"><p>Opening preview…</p></div><details><summary>File location</summary><p>${esc(f.local_path||state.data.workspace+'/'+f.path)} · ${size(f.bytes)}</p><button class="secondary" id="copy-file-location">Copy file location</button></details>`);
  $('#copy-file-location').addEventListener('click',()=>attempt(async()=>{await navigator.clipboard.writeText(f.local_path||state.data.workspace+'/'+f.path); $('#copy-file-location').textContent='Location copied';}));
  if(f.media) {
    try {
      const url=await mediaBlob(f.path);
      const el=document.createElement(/\.(mp4|webm)$/i.test(f.path)?'video':/\.(mp3|wav|ogg)$/i.test(f.path)?'audio':'img');
      el.src=url; el.className='media-preview'; if(el.tagName==='IMG')el.alt=f.name; else el.controls=true;
      $('#file-preview').replaceChildren(el);
    } catch(e) { $('#file-preview').textContent=e.message; }
  } else {
    try { const r=await api('/api/file?business='+encodeURIComponent(state.business)+'&path='+encodeURIComponent(path)); $('#file-preview').innerHTML='<pre>'+esc(r.text)+'</pre>'; }
    catch(e) { $('#file-preview').textContent=e.message; }
  }
}
function prompt(text) { $('#detail').close(); $('#section-dialog').close(); state.view='home'; $('#request').value=text; $('#request').focus(); $('#request').scrollIntoView({block:'center',behavior:'auto'}); }

async function openStoredWorkspace(path) {
  const opened=await api('/api/workspaces/open',{path});
  for(const dialog of document.querySelectorAll('dialog[open]'))dialog.close();
  state.business='';state.chat=[];state.chatMeta=null;state.liveJob=null;state.hydrated=false;state.library=[];state.catalog=null;state.files=[];state.connectionChecks=null;state.setupPrompted=new Set();state.setupStep='welcome';
  const url=new URL(location.href);url.searchParams.delete('business');history.replaceState(null,'',url);
  $('#request').value='';await refresh();notice(opened.connection_note||'Your saved workspace is open.',!!opened.connection_note);
}
async function workspaceStorage() {
  $('#more-dialog').close();
  const input=(id,label,kind='folder')=>`<label>${label}<input id="${id}" name="${kind==='file'?'archive':'path'}" required placeholder="Paste a full folder${kind==='file'?' or file':''} location"></label><button type="button" class="secondary" data-storage-browse="${id}" data-kind="${kind}">Browse…</button>`;
  details('Back up or restore',`<p>Keep a verified copy of your saved business files. AI sign-ins and linked external folders are separate.</p>
    <form id="backup-workspace-form" class="form-grid">${input('backup-workspace-path','Save backup in')}<button class="primary">Create backup</button></form>
    <details class="restore-backup"><summary>Restore a backup</summary><p>Restore into a new or empty folder. Your current workspace stays in place.</p><form id="restore-workspace-form" class="form-grid">${input('restore-archive-path','AURA backup ZIP','file')}${input('restore-workspace-path','Restore into')}<button class="primary">Restore backup</button></form></details><div id="storage-result" role="status"></div>`);
}

async function addWorkspace() {
  $('#more-dialog').close();
  const r=await api('/api/workspaces'), recent=r.recent.filter(w=>w.path!==r.current);
  details('Add or open a workspace',`<section class="workspace-create"><h3>Create a new workspace</h3><p>Keep another business or project’s context and files separate.</p><form id="setup-form" class="form-grid"><label>Workspace name<input name="name" required maxlength="160" autocomplete="organization"></label><button class="primary">Create workspace →</button></form></section>
    <section class="workspace-open"><h3>Open saved work</h3><p>Choose your saved workspace or an older AURA folder.</p>
    ${recent.length?`<div class="card">${recent.map(w=>`<button class="row" data-open-workspace="${esc(w.path)}"><span class="row-text"><span class="row-title">${esc(w.name)}</span><span class="row-meta storage-path">${esc(w.path)}</span></span><span>→</span></button>`).join('')}</div>`:''}
    <form id="open-workspace-form" class="form-grid"><label>Workspace folder<input id="open-workspace-path" name="path" required placeholder="Paste the folder location"></label><div class="workspace-open-actions"><button type="button" class="secondary" data-storage-browse="open-workspace-path">Browse…</button><button class="primary">Open workspace →</button></div></form></section>`);
}
async function changeWorkspace(id) {
  if(state.busy){$('#business').value=state.business;$('#setup-workspace-select').value=state.business;return;}
  if(id==='__add__'){$('#business').value=state.business;$('#setup-workspace-select').value=state.business;await addWorkspace();return;}
  if(id===state.business)return;
  state.drafts??={};state.drafts[state.business]=$('#request').value;$('#request').value=state.drafts[id]||'';
  state.business=id;state.view='home';state.chat=[];state.chatMeta=null;state.hydrated=false;state.setupStep='welcome';state.welcome=null;state.connectionChecks=null;
  showMessages();notice('');await refresh();renderConnection();
}
function showMessages(latest=false) {
  const failed=!state.busy&&(state.chatMeta?.status==='error'||(!state.chatMeta&&state.liveJob?.status==='error'));
  $('#request-recovery').hidden=!failed;
  const detail=failed?((state.liveJob?.chat_id===state.chatMeta?.id?state.liveJob?.error_detail:'')||[...state.chat].reverse().find(m=>m.role==='assistant')?.error_detail||''):'';
  $('#request-error-details').hidden=!detail;$('#request-error-text').textContent=detail;
  const conversation=$('#conversation'), top=conversation.scrollTop, chat=state.chatMeta?.id||'';
  if(!state.busy&&state.liveJob&&((state.liveJob.business_id&&state.liveJob.business_id!==state.business)||(state.liveJob.chat_id&&state.liveJob.chat_id!==chat)))state.liveJob=null;
  const follow=latest||conversation.hidden||conversation.dataset.chat!==chat||conversation.scrollHeight-conversation.clientHeight-top<32;
  conversation.hidden=!state.chat.length&&!state.busy;conversation.dataset.chat=chat;
  const markup=state.chat.map(r=>`<div class="message ${r.role}"><strong>${r.role==='user'?'YOU':esc(r.agent||state.data?.connection.name||'YOUR AGENT')}${r.at?` <time>${esc(clockTime(r.at))}</time>`:''}${r.role==='assistant'&&r.model?` · ${esc(r.model)}${r.effort?' · '+esc(human(r.effort)):''}`:''}</strong>${esc(r.text)}</div>`).join('');
  if(state.messageMarkup!==markup){$('#messages').innerHTML=markup;state.messageMarkup=markup;}
  $('#working').hidden=!state.busy;
  $('#working-label').textContent=state.liveJob?.progress||'Starting your AI…';
  $('#live-reply').hidden=!state.busy||!state.liveJob?.reply;
  $('#live-reply-text').textContent=state.busy?state.liveJob?.reply||'':'';
  const activity=state.liveJob?.activity||[];
  $('#request-activity').hidden=!activity.length;
  const activitySignature=JSON.stringify(activity);
  if(state.activitySignature!==activitySignature){$('#activity-list').innerHTML=activity.map(a=>`<li><time>${esc(clockTime(a.at))}</time> ${esc(a.text)}</li>`).join('');state.activitySignature=activitySignature;}
  conversation.scrollTop=follow?conversation.scrollHeight:top;
}
async function submitRequest(text) {
  if(state.starting||state.stopping||state.settling)return;
  if(!text.trim()) { $('#request').focus(); return; }
  if(state.busy){state.nextRequest=text;await stopRequest();return;}
  if(!state.data.connection.connected && state.data.connection.mode!=='copy') { $('#request').value=text; openConnection(true); return; }
  if(state.data.connection.model_controls&&!state.data.connection.model){openConnection(true);return;}
  if(!state.data.connection.connected) {
    const request=await api('/api/request',{business:state.business,text,history:state.chat});
    details('Copy to your AI',`<p>Paste this into your existing AI chat to continue.</p><button class="primary" id="copy-handoff">Copy request</button><details><summary>See the request</summary><label class="sr-only" for="handoff-text">Request for your agent</label><textarea id="handoff-text" class="handoff" readonly></textarea></details>`);
    $('#handoff-text').value=request.text;
    $('#copy-handoff').addEventListener('click',()=>attempt(async()=>{await navigator.clipboard.writeText(request.text); $('#copy-handoff').textContent='Copied — paste into your agent';}));
    return;
  }
  let job;state.starting=true;chatControls();
  try {job=await api('/api/chat',{business:state.business,text,history:state.chat});}
  finally {state.starting=false;chatControls();}
  state.chat.push({role:'user',text,at:new Date().toISOString()}); $('#request').value='';notice('');showMessages(true);
  await pollJob(job);
}

document.addEventListener('click',event=>attempt(async()=>{
  const button=event.target.closest('button'); if(!button) return;
  if(button.id==='stop-request')await stopRequest();
  if(button.hasAttribute('data-add-location'))addLocation();
  if(button.dataset.browseLocation){button.disabled=true;try{const result=await api('/api/locations/browse',{kind:button.dataset.browseLocation});if(result.path&&$('#location-path'))$('#location-path').value=result.path;}finally{button.disabled=false;}}
  if(button.dataset.unlinkLocation){await api('/api/locations',{business:state.business,remove:button.dataset.unlinkLocation});await refresh();notice('Location unlinked. The original files are unchanged.');}
  if(button.dataset.filelocation){fileLocation=button.dataset.filelocation;$('#file-all-locations').hidden=false;document.querySelectorAll('[data-filelocation]').forEach(b=>b.classList.toggle('active',b===button));renderFiles();}
  if(button.id==='file-all-locations'){fileLocation='';button.hidden=true;document.querySelectorAll('[data-filelocation]').forEach(b=>b.classList.remove('active'));renderFiles();}
  if(button.dataset.libraryKind){workFilter=button.dataset.libraryKind;workCategory='';state.view='work';await render();}
  if(button.dataset.workcategory){workCategory=button.dataset.workcategory;if(state.view!=='work'){state.view='work';workFilter='Workflow';await render();}else renderWork();}
  if(button.id==='work-all-topics'){workCategory='';renderWork();}
  if(button.id==='refresh-schedules'){await refresh();}
  if(button.dataset.schedule)await scheduleDetails(button.dataset.schedule);
  if(button.dataset.taskStatus){button.disabled=true;try{await api('/api/schedules/update',{id:state.editingTask.id,action:button.dataset.taskStatus});$('#detail').close();await refresh();notice('Schedule updated in '+state.editingTask.app+'.');}finally{button.disabled=false;}}
  if(button.id==='close-section') {state.view='home';$('#section-dialog').close();}
  if(button.id==='new-chat'&&!state.busy) {await api('/api/chats/new',{business:state.business});state.chat=[];state.chatMeta=null;state.liveJob=null;$('#request').value='';showMessages();taskStatus('');$('#request').focus();notice('New chat. Your saved business context is still available.');}
  if(button.id==='chats') {
    const result=await api('/api/chats?business='+encodeURIComponent(state.business));
    details('Your chats',`<p>Conversations kept by your AI app for this business.</p><div class="card">${result.items.length?result.items.slice().reverse().map(c=>`<button class="row" data-chat="${esc(c.id)}" ${state.busy?'disabled':''}><span class="row-text"><span class="row-title">${esc(c.title)}</span><span class="row-meta">${esc(human(c.agent))} · ${esc(c.model)} · ${clockTime(c.updated)}${c.status==='working'?' · Check in your AI app':''}</span></span><span>→</span></button>`).join(''):empty('No saved native chats yet.','Supported native connections keep your conversations in your AI app.')}</div>${state.chatMeta?.native_id?`<button class="secondary" id="copy-native-chat">Copy command to open in ${esc(human(state.chatMeta.agent))}</button>`:''}`);
  }
  if(button.dataset.chat){const result=await api('/api/chats/open',{business:state.business,id:button.dataset.chat});state.chat=result.messages;state.chatMeta=result.chat;$('#detail').close();notice('');await refresh();showMessages();if(result.history_note)notice(result.history_note);taskStatus(result.history_note?'Saved display restored':'Chat restored from '+state.data.connection.name);}
  if(button.id==='copy-native-chat'){const c=state.chatMeta,commands={codex:'codex resume',pi:'pi --session',omp:'omp --resume',claude:'claude --resume',hermes:'hermes --resume',antigravity:'agy --conversation'};await navigator.clipboard.writeText(commands[c.agent]+' '+JSON.stringify(c.native_id));button.textContent='Copied';}
  if(button.dataset.close) $('#'+button.dataset.close).close();
  if(button.dataset.view) { $('#more-dialog').close(); if(!state.data.diagnostics.length)notice(''); state.view=button.dataset.view; fileFilter='all'; workFilter='Workflow';workCategory=''; await render(); }
  if(button.dataset.prompt) prompt(button.dataset.prompt);
  if(button.dataset.record) recordDetails(button.dataset.record);
  if(button.dataset.file) await fileDetails(button.dataset.file);
  if(button.dataset.filefilter) { fileFilter=button.dataset.filefilter; $('#section-content').querySelectorAll('[data-filefilter]').forEach(b=>b.classList.toggle('active',b===button)); renderFiles(); }
  if(button.dataset.workfilter) { workFilter=button.dataset.workfilter;workCategory=''; button.parentElement.querySelectorAll('button').forEach(b=>b.classList.toggle('active',b===button)); renderWork(); }
  if(button.dataset.method) {
    const method=state.library.find(m=>m.path===button.dataset.method); if(!method) return;
    const doc=await api('/api/document?path='+encodeURIComponent(method.path));
    const body=doc.text.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'');
    const purpose=body.match(/## Purpose\s+([\s\S]*?)(?=\n## |$)/)?.[1]?.trim()||body.split('\n').filter(s=>s.trim()&&!s.startsWith('#')).slice(0,2).join(' ');
    details(method.title,`<p>${esc(method.kind)} · Adapt this method to the actual outcome.</p><p>${esc(purpose)}</p><button class="primary" data-prompt="${esc(`Use ${method.kind.toLowerCase()} ${method.id||method.path} as useful guidance for our business. Help me define the outcome, use our actual AURA context and your available tools, and do the work. Adapt the method when helpful.`)}">Use with your AI ↗</button><details><summary>Read the full guidance</summary><pre>${esc(body)}</pre></details>`);
  }
  if(button.id==='more') $('#more-dialog').showModal();
  if(button.id==='api-connections')await showApiConnections('');
  if(button.id==='model-api-connections')await showApiConnections('models');
  if(button.id==='back-to-models')$('#detail').close();
  if(button.dataset.removeApi){await api('/api/connections/remove',{provider:button.dataset.removeApi});state.catalog=null;state.apiChanged=true;await showApiConnections();}
  if(button.id==='refresh-models'){if(state.modelReload){location.reload();return;}await loadAgentOptions(true);}
  if(button.id==='favorite-model')await toggleFavorite($('#model-choice').value);
  if(button.dataset.favorite)await toggleFavorite(button.dataset.favorite);
  if(button.dataset.pickModel){$('#model-choice').value=button.dataset.pickModel;favoriteButton();renderFavoriteList();try{await selectModel();}catch(error){modelFailure(error);}}
  if(button.dataset.action==='connect'||['connection','review-setup','model-settings'].includes(button.id)) {state.tour=button.id==='review-setup';openConnection(true,state.tour?'welcome':button.id==='model-settings'?'models':'connect');}
  if(button.id==='setup-start'||button.id==='models-back'){state.setupStep='connect';renderConnection();}
  if(button.id==='connect-back'){state.setupStep='welcome';renderConnection();}
  if(button.id==='choose-agent'||button.id==='setup-back'){state.setupStep='models';renderConnection();await loadAgentOptions();}
  if(button.id==='welcome-request')finishSetup();
  if(button.id==='setup-result-back'){state.setupStep='tour';renderConnection();}
  if(button.id==='setup-retry'){state.setupStep='connect';renderConnection();await checkConnections(false);if(state.connectionChecks?.ready)finishSetup();}
  if(button.id==='check-connections')await checkConnections(false);
  if(button.id==='first-task'){
    await dismissSetup();
    const request='Help me get started with this workspace. Start a friendly conversation by asking one short, plain-language question about what I want to accomplish. Wait for my answer. Do not research, create deliverables, or change files yet. We’ll choose what to work on together.';
    $('#request').value=request;await submitRequest(request);
  }
  if(button.id==='setup-done') await dismissSetup();
  if(button.id==='customize-view'){$('#more-dialog').close();details('Customize this workspace',`<p>You own the files and control this workspace. Ask your AI to change the layout, add a view, or simplify something. Your business files remain usable in other apps.</p><button class="primary" data-prompt="Help me customize my AURA visual workspace. Ask what I want to change, then follow the visual workspace guide to adapt an organization-owned copy of the interface. Preserve my files, native chats, and connection controls.">Ask my AI to customize it →</button>`);}
  if(button.id==='notification-bell') {await syncNotifications();$('#notification-dialog').showModal();}
  if(button.id==='notification-read-all') {state.inbox=await api('/api/notifications',{business:state.business,action:'read',all:true});renderNotifications();state.systemAlert?.close();}
  if(button.dataset.notification) {
    const item=state.inbox.items.find(n=>n.id===button.dataset.notification);if(!item)return;
    if(item.chat_id&&item.chat_id!==state.chatMeta?.id) {
      const result=await api('/api/chats/open',{business:state.business,id:item.chat_id});
      state.chat=result.messages;state.chatMeta=result.chat;await refresh();
      if(result.history_note)notice(result.history_note);
    }
    state.inbox=await api('/api/notifications',{business:state.business,action:'read',id:item.id});renderNotifications();
    $('#notification-dialog').close();state.systemAlert?.close();showMessages(true);
    if(item.chat_id&&!$('#conversation').hidden){$('#conversation').scrollIntoView({block:'nearest'});$('#conversation').focus();}
    else notice('Open your AI app to review this request.');
  }
  if(button.id==='notification-system') {
    const enabled=state.inbox?.enabled&&window.Notification?.permission==='granted';
    const permission=enabled?Notification.permission:await Notification.requestPermission();
    await api('/api/preferences',{notifications:!enabled&&permission==='granted'});
    await syncNotifications();if(enabled)state.systemAlert?.close();
  }
  if(button.dataset.action==='add-goal')details('Add a goal',`<form id="goal-form" class="form-grid"><label>What do you want to accomplish?<input name="name" required maxlength="2000" autofocus></label><button class="primary">Save goal</button></form>`);
  if(button.dataset.action==='edit-business') { const b=rows('Business')[0]; details('Workspace name',`<form id="business-form" class="form-grid"><label>Workspace name<input name="name" value="${esc(b.title)}" required maxlength="160"></label><button class="primary">Save name</button></form>`); }
  if(button.id==='session-keys-only'){await api('/api/connections/session-only',{});await showApiConnections();}
  if(['workspace-manager','open-existing-start'].includes(button.id))await addWorkspace();
  if(button.id==='workspace-backups')await workspaceStorage();
  if(button.dataset.openWorkspace)await openStoredWorkspace(button.dataset.openWorkspace);
  if(button.dataset.storageBrowse){const r=await api('/api/locations/browse',{kind:button.dataset.kind||'folder'});if(r.path)$('#'+button.dataset.storageBrowse).value=r.path;}
  if(button.dataset.copyPath){await navigator.clipboard.writeText(button.dataset.copyPath);button.textContent='Copied';}
  if(button.id==='retry-request'){const last=[...state.chat].reverse().find(m=>m.role==='user');if(last){$('#request').value=last.text;$('#request').focus();notice('Review what already finished, then send when you’re ready.');}}
  if(button.id==='fix-request-connection'){openConnection(true);state.setupStep='connect';renderConnection();await checkConnections(false);}
  if(button.id==='check-apps'){const kind=$('#agent-choice').value;button.disabled=true;try{await refresh();state.catalog=null;$('#agent-choice').value=kind;connectionChoice();const choice=state.data.connection.choices.find(c=>c.id===kind);$('#app-check-status').textContent=choice?.available?choice.name+' found. Continue when you’re ready.':'We can’t find this app yet. Finish setup, or reopen AURA after installing it.';}finally{button.disabled=false;}}
  if(button.id==='copy-connection-setup') {
    const instruction=`Connect my AURA visual workspace to the AI app I am using. Read ${state.data.product}/docs/visual-workspace.md and use this app's supported connection. Reuse my existing sign-in and permissions, then reopen the visual workspace connected to it. Do not substitute a different AI app just because it is installed. If this app cannot accept requests from a local interface, explain that clearly. AURA workspace: ${state.data.workspace}. Business ID: ${state.business}.`;
    await navigator.clipboard.writeText(instruction); $('#setup-copy-status').textContent='Copied. Paste this into your AI app to finish linking it.';
  }
  if(button.id==='refresh') {if(!state.busy)state.hydrated=false;await refresh();}
  if(button.id==='location') { await navigator.clipboard.writeText(state.data.workspace); $('#more-dialog').close(); notice('Folder location copied.'); }
}));
document.addEventListener('input',event=>{ if(event.target.id==='quick-work-search')quickMethods(); if(event.target.id==='record-search')renderMemory(); if(event.target.id==='file-search')renderFiles(); if(event.target.id==='work-search')renderWork();if(['task-time','task-every','task-custom'].includes(event.target.id))updateTaskTiming(); });
document.addEventListener('submit',event=>{
  event.preventDefault();
  attempt(async()=>{
    const form=event.target, data=new FormData(form); const submit=form.querySelector('[type=submit]')||form.querySelector('button.primary')||form.querySelector('button');
    if(form.id==='open-workspace-form'){submit.disabled=true;try{await openStoredWorkspace(data.get('path'));}finally{submit.disabled=false;}return;}
    if(form.id==='backup-workspace-form'||form.id==='restore-workspace-form'){
      submit.disabled=true;
      try{const restoring=form.id==='restore-workspace-form', r=await api('/api/workspaces/'+(restoring?'restore':'backup'),Object.fromEntries(data));
        $('#storage-result').innerHTML=`<p>${restoring?'Your files were restored and verified. Open the restored workspace to continue.':'Backup saved and verified.'}</p><p class="storage-path">${esc(r.path)}</p><button class="text-button" data-copy-path="${esc(r.path)}">Copy location</button>${restoring?`<button class="primary" data-open-workspace="${esc(r.path)}">Open restored workspace →</button>`:''}`;
      }finally{submit.disabled=false;}return;
    }
    if(form.id==='api-key-form'){
      submit.disabled=true;
      try{await api('/api/connections/save',Object.fromEntries(data));state.catalog=null;state.apiChanged=true;await showApiConnections();$('#api-save-status').textContent=state.apiReturn==='models'?'Key saved. Return to models.':'Key saved. Your next agent request can use it. Account access has not been verified.';}
      finally{const field=$('#api-secret');if(field)field.value='';submit.disabled=false;}
      return;
    }
    if(form.id==='connect-form') { $('#connect-agent').disabled=true; try { await pickerSave;const route=selectedRoute(),kind=route?.agent||$('#agent-choice').value;await api('/api/connect',{kind,model:route?.model||'',effort:$('#effort-choice').value,workspace_write:true});if(kind!==state.data.connection.selected&&state.business){await api('/api/chats/new',{business:state.business});state.chat=[];state.chatMeta=null;showMessages();} const tour=state.tour||!state.data.onboarding.seen;state.connectionChecks=null;state.welcome=null;await refresh();await checkConnections(false);if(tour){state.setupStep='tour';renderConnection();}else if(state.connectionChecks?.ready)$('#connect-dialog').close();else finishSetup();notice(''); } catch(error){state.modelError=simpleSetupError(error.message);} finally {connectionChoice();} return; }
    if(form.id==='chat-form') { await submitRequest($('#request').value); return; }
    if(submit)submit.disabled=true;
    try {
      if(form.id==='location-form'){await api('/api/locations',{business:state.business,path:data.get('path'),name:data.get('name')});$('#detail').close();state.view='files';await refresh();notice('Linked. Your AI can reference this location when it helps your work.');}
      if(form.id==='task-edit-form'){
        const task=state.editingTask, app=data.get('app');
        if(app===task.owner&&task.editable){
          const changes={id:task.id,action:'edit'};
          for(const key of ['name','schedule','model'])if(data.has(key)&&data.get(key)!==(key==='schedule'?(task.schedule_raw||task.schedule):key==='model'?(task.provider&&task.model?task.provider+':'+task.model:task.model):task[key]))changes[key]=data.get(key);
          await api('/api/schedules/update',changes);$('#detail').close();await refresh();notice('Changes saved in '+task.app+'.');
        }else{
          const request=`${app===task.owner?'Adjust':'Move'} the existing scheduled task ${JSON.stringify(task.name)}, owned by ${task.app}, profile ${task.profile}, native task ID ${JSON.stringify(task.native_id)}. Requested AI app: ${app}. Name: ${JSON.stringify(data.get('name'))}. Schedule: ${JSON.stringify(data.get('schedule'))}. Model: ${JSON.stringify(data.get('model')||'app default')}. Use supported native scheduling controls. Do not edit undocumented scheduler storage or create duplicate schedules. If moving, confirm the replacement is active before pausing the old task; report both actual states. Preserve other task settings, timezone and delivery preferences. If you cannot manage either scheduler, explain the exact remaining action without claiming success.`;
          prompt(request);await submitRequest(request);
        }
      }
      if(form.id==='setup-form') { const result=await api('/api/setup',{name:data.get('name')});state.drafts??={};state.drafts[state.business]=$('#request').value;$('#request').value=state.drafts[result.business_id]||'';state.business=result.business_id; state.view='home'; state.chat=[];state.chatMeta=null;state.hydrated=false; state.setupStep='welcome';state.connectionChecks=null;state.welcome=null;showMessages();$('#detail').close(); notice('Ready. What would you like to do?'); await refresh(); }
      if(['goal-form','edit-goal-form','business-form'].includes(form.id)) { await api('/api/save',{business:state.business,kind:form.id==='business-form'?'business':'goal',name:data.get('name'),ref:form.dataset.ref}); $('#detail').close(); notice('Saved.'); await refresh(); }
      if(form.id==='schedule-form') {
        const request=`Set up recurring work for our AURA business: ${data.get('job')}. Timing: ${data.get('when')}. Confirm timezone if needed. Check existing native tasks first to avoid duplicates. Use your actual supported scheduler or operating system; report the scheduler owner, native task ID, confirmation and next run. Save only useful business intent and a supported reference to the native task in AURA. If scheduling is unavailable, say so clearly. Do not claim that saving a plan creates a schedule.`;
        prompt(request); await submitRequest(request);
      }
    } finally { if(submit)submit.disabled=false; }
  });
});
for(const id of ['business','setup-workspace-select'])$('#'+id).addEventListener('change',event=>attempt(()=>changeWorkspace(event.target.value)));
$('#request').addEventListener('keydown',event=>{if(event.key==='Enter'&&!event.shiftKey&&!event.isComposing){event.preventDefault();$('#chat-form').requestSubmit();}});
$('#section-dialog').addEventListener('close',()=>{state.view='home';});
$('#agent-choice').addEventListener('change',()=>{$('#app-check-status').textContent='';connectionChoice();});
$('#model-choice').addEventListener('change',()=>attempt(async()=>{favoriteButton();renderFavoriteList();try{await selectModel();}catch(error){modelFailure(error);}}));
$('#effort-choice').addEventListener('change',()=>attempt(async()=>{const picker=modelPicker();picker.efforts??={};picker.efforts[selectedRoute().key]=$('#effort-choice').value;await saveModelPicker();}));
$('#model-list-view').addEventListener('change',()=>attempt(async()=>{modelPicker().view=$('#model-list-view').value;renderModelChoices();await saveModelPicker();}));
$('#provider-checkboxes').addEventListener('change',event=>attempt(async()=>{const id=event.target.dataset.modelProvider;if(!id)return;const picker=modelPicker();picker.providers=event.target.checked?[...new Set([...picker.providers,id])]:picker.providers.filter(v=>v!==id);renderModelChoices();await saveModelPicker();}));
$('#favorite-search').addEventListener('input',()=>renderModelChoices());
$('#favorite-search').addEventListener('keydown',event=>{if(event.key==='Enter')event.preventDefault();});
document.addEventListener('change',event=>{if(['task-cadence','task-day','task-time','task-every','task-unit','task-custom'].includes(event.target.id))updateTaskTiming();if(event.target.id==='api-provider')apiProviderHelp();if(event.target.name==='app'&&event.target.closest('#task-edit-form')){taskModels(event.target.value).catch(()=>{});const moved=event.target.value!==state.editingTask.owner;$('#task-edit-form button[type=submit],#task-edit-form .primary').textContent=moved?'Ask AI to move':state.editingTask.editable?'Save changes':'Ask AI to adjust';$('#task-edit-note').textContent=moved?'Your AI must confirm the new schedule before pausing the old one.':state.editingTask.editable?'Changes are saved through the native scheduler.':'This app requires its native scheduling controls.';}});
$('#detail').addEventListener('close',()=>{const field=$('#api-secret');if(field)field.value='';const reload=state.apiReturn==='models'&&state.apiChanged;state.apiReturn='';state.apiChanged=false;if(reload)loadAgentOptions(true).catch(modelFailure);});
document.addEventListener('visibilitychange',()=>{if(!document.hidden){state.systemAlert?.close();syncNotifications().catch(()=>{});}});
window.addEventListener('focus',()=>{state.systemAlert?.close();syncNotifications().catch(()=>{});});
setInterval(()=>syncNotifications(true).catch(()=>{}),8000);
$('#appearance').addEventListener('change',()=>attempt(async()=>{const value=$('#appearance').value;await api('/api/preferences',{appearance:value});state.data.appearance=value;applyAppearance(value);}));
for(const dialog of document.querySelectorAll('dialog')) {
  let beganOutside=false;
  const outside=event=>{const r=dialog.getBoundingClientRect();return event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom;};
  dialog.addEventListener('pointerdown',event=>{beganOutside=event.target===dialog&&outside(event);});
  dialog.addEventListener('click',event=>{if(beganOutside&&event.target===dialog&&outside(event))dialog.close();beganOutside=false;});
}
attempt(refresh);
