/* DOM-independent view checks; no browser, network, or frontend dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const nodes=new Map(),listeners={};
function node(id){if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',hidden:false,isConnected:true,value:'',dataset:{},querySelectorAll:()=>[],querySelector:selector=>node(id+' '+selector),showModal(){this.open=true;},close(){this.open=false;}});return nodes.get(id);}
const profiles={items:[{id:'jeff',name:'<Jeff>',instructions:'Find useful evidence.',task_ids:['weekly']}],chats:[],workspace:'A'};
const tasks={items:[{id:'weekly',name:'Weekly review',owner:'hermes'}],notes:[]};
const history={items:[{id:'report.md',name:'Weekly findings',status:'Saved result'}],limit:20,note:''};
let opened=null,nativePreview=null;
const context={window:{},document:{addEventListener:(name,callback)=>(listeners[name]??=[]).push(callback)},
  state:{data:{workspace:'A',connection:{choices:[],selected:'codex'}},business:'studio',view:'assistants',chatMeta:{id:'parent'}},
  $:node,esc:value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),
  empty:text=>`<p>${text}</p>`,appName:name=>name,chatDate:at=>String(at),chatMarkdown:text=>`<p>${text}</p>`,
  scheduleRow:t=>`<button data-schedule="${t.id}">${t.name}</button>`,
  details:(title,html)=>{opened={title,html};node('#detail').open=true;},notice:()=>{},nativeApps:['codex','pi','hermes'],
  api:async path=>path.startsWith('/api/assistants')?profiles:path==='/api/schedules'?tasks:path.startsWith('/api/schedules/history')?history:{name:'Weekly review',file:'Report',text:'Useful findings',owner:'codex',native_id:'native-run'},
  attempt:fn=>Promise.resolve().then(fn),addNativeChat:async(kind,id)=>{nativePreview={kind,id};},
};
vm.createContext(context);vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),context);
// Exercise the existing shared picker directly, without starting the app shell.
const appSource=fs.readFileSync(require('node:path').join(require('node:path').dirname(process.argv[2]),'app.js'),'utf8');
const pickerStart=appSource.indexOf('let chatModelTicket=0;'),pickerEnd=appSource.indexOf("\ndocument.addEventListener('click',event=>attempt",pickerStart);
Object.assign(context,{pickerSave:Promise.resolve(),structuredClone,human:s=>s[0].toUpperCase()+s.slice(1),
  modelPicker:()=>({favorites:['catalog-model']}),chatScope:()=>JSON.stringify([context.state.data.workspace,context.state.business,context.state.chatMeta?.id]),
  composerConnection:()=>({kind:'codex',model:'',effort:''})});
vm.runInContext(appSource.slice(pickerStart,pickerEnd),context);
(async()=>{
  const work=context.window.auraWork,host=node('host');
  await work.renderAssistants(host);
  assert(node('#assistant-list').innerHTML.includes('&lt;Jeff&gt;'));
  assert(!node('#assistant-list').innerHTML.includes('<Jeff>'));
  const savedProfiles=profiles.items;profiles.items=[];
  await work.assignChat({id:'parent'},host);assert.equal(host.hidden,true);assert.equal(host.innerHTML,'','No profiles means no empty chat selector');
  await work.assignTask({id:'weekly'},host);assert.equal(host.hidden,true,'Tasks must not show a selector without choices either');
  profiles.items=savedProfiles;profiles.running=[];
  const assignedChat={id:'parent',status:'working'};
  await work.assignChat(assignedChat,host);assert.equal(host.hidden,false);assert.match(host.innerHTML,/Assign an assistant/);assert.doesNotMatch(host.innerHTML,/disabled/,'An old saved Working status must not disable assignment');
  node('#chat-assistant').value='jeff';await node('#chat-assistant').onchange();assert.equal(assignedChat.assistant_id,'jeff');assert.equal(context.state.chatMeta.assistant_name,'<Jeff>');
  const assignmentApi=context.api;context.api=async(path,data)=>{if(data?.action==='assign_chat')throw new Error('Could not save assignment');return profiles;};
  node('#chat-assistant').value='';await node('#chat-assistant').onchange();assert.equal(node('#chat-assistant').value,'jeff');assert.equal(assignedChat.assistant_id,'jeff','Failed assignment must preserve the saved assistant');context.api=assignmentApi;
  profiles.running=['parent'];await work.assignChat(assignedChat,host);assert.match(host.innerHTML,/&lt;Jeff&gt;/);assert.doesNotMatch(host.innerHTML,/<select/,'Running chats show the assigned name without an unavailable control');
  profiles.running=[];context.state.chatMeta={id:'parent'};
  await work.overview('jeff');assert(opened.html.includes('data-schedule="weekly"'));
  assert(opened.html.includes('New chat with &lt;Jeff&gt;'));
  profiles.chats=Array.from({length:25},(_,i)=>({id:'chat-'+i,title:'Work '+i,assistant_id:'jeff',agent:'codex',updated:i}));
  await work.overview('jeff');assert(node('#assistant-chat-list').innerHTML.includes('Show more chats'));
  assert(!node('#assistant-chat-list').innerHTML.includes('data-chat="chat-24"'));
  node('#assistant-chat-list').onclick({target:{closest:()=>({})}});
  assert(node('#assistant-chat-list').innerHTML.includes('data-chat="chat-24"'));
  node('#assistant-chat-search').value='Work 24';node('#assistant-chat-search').oninput();
  assert(node('#assistant-chat-list').innerHTML.includes('data-chat="chat-24"')&&!node('#assistant-chat-list').innerHTML.includes('data-chat="chat-0"'));
  await work.history(tasks.items[0],host);assert(host.innerHTML.includes('Latest · Weekly findings'));
  await work.openResult('weekly','report.md');assert(opened.html.includes('data-result-native="native-run"'));
  const button={dataset:{resultNative:'native-run',resultOwner:'codex'},hasAttribute:()=>false};
  for(const callback of listeners.click)callback({target:{closest:()=>button}});
  await new Promise(resolve=>setImmediate(resolve));assert.deepEqual(nativePreview,{kind:'codex',id:'native-run'});
  // The delegation tool groups children; it is not counted as an extra worker.
  context.state.liveJob={chat_id:'parent',subagents:[{id:'group',name:'Delegated work',status:'working'},
    {id:'one',parent_id:'group',name:'Research',status:'complete'},
    {id:'two',parent_id:'group',name:'Review',status:'working',result:'Still working'}]};
  work.renderDelegation();assert(node('#delegated-work').innerHTML.includes('1 of 2 completed'));
  context.state.chatMeta.subagents=[];context.state.liveJob.chat_id='another-chat';
  work.renderDelegation();assert.equal(node('#delegated-work').hidden,true);
  context.state.liveJob={chat_id:'parent',subagents:[...Array.from({length:50},(_,i)=>({id:'done-'+i,status:'complete',name:'Done'})),{id:'active',status:'working',name:'Active worker'}]};
  work.renderDelegation();assert(node('#delegated-work').innerHTML.includes('Active worker')&&node('#delegated-work').innerHTML.includes('Show more agents'));
  const more={dataset:{},hasAttribute:name=>name==='data-delegation-more'};
  for(const callback of listeners.click)callback({target:{closest:()=>more}});
  assert(node('#delegated-work').innerHTML.includes('data-child="done-15"'));
  // Native read errors remain distinguishable from a genuinely empty history.
  const originalApi=context.api;context.api=async()=>{throw new Error('Could not read native results.');};
  await work.history(tasks.items[0],host);
  assert(host.innerHTML.includes('Could not read native results.')&&host.innerHTML.includes('Try again')&&!host.innerHTML.includes('No saved results'));
  context.api=originalApi;await host.querySelector('button').onclick();assert(host.innerHTML.includes('Weekly findings'));
  // App A -> B -> A, resolving the newest A first: stale catalogs cannot win.
  context.state.chatMeta=null;context.state.data.connection.choices=[{id:'codex',name:'Codex',available:true},{id:'hermes',name:'Hermes',available:true}];
  context.state.data.connection.apps=[{id:'codex'},{id:'hermes'}];
  const catalogs=[],catalog=(kind,label=kind)=>({picker:{favorites:[]},unavailable:[],models:[{id:'catalog-model',name:label+' model',provider:'test',routes:[{agent:kind,model:kind+'-model',current:true}]}]});
  context.api=async path=>path.startsWith('/api/model-catalog')?new Promise(resolve=>catalogs.push(resolve)):path.startsWith('/api/agent-efforts')?{efforts:['low','high'],default_effort:'low'}:originalApi(path);
  const first=context.openChatModels();await new Promise(resolve=>setImmediate(resolve));
  context.state.chatModelDraft.kind='hermes';const middle=context.loadChatModelOptions();await new Promise(resolve=>setImmediate(resolve));
  context.state.chatModelDraft.kind='codex';const newest=context.loadChatModelOptions();await new Promise(resolve=>setImmediate(resolve));
  catalogs[2](catalog('codex','new-codex'));await newest;
  catalogs[1](catalog('hermes'));await middle;catalogs[0](catalog('codex','old-codex'));await first;
  assert.equal(context.state.chatModelOptions.models[0].name,'new-codex model');
  // Assistant choices use that same picker; they never modify the current chat.
  context.api=async path=>path.startsWith('/api/model-catalog')?catalog('codex'):path.startsWith('/api/agent-efforts')?{efforts:['low','high'],default_effort:'low'}:originalApi(path);
  const create={dataset:{},hasAttribute:name=>name==='data-assistant-new'};
  for(const callback of listeners.click)callback({target:{closest:()=>create}});
  await new Promise(resolve=>setImmediate(resolve));
  await node('#assistant-pick-model').onclick();node('#chat-effort-choice').value='high';await context.saveChatModel();
  assert.equal(node('#assistant-model').value,'codex-model');assert.equal(node('#assistant-effort').value,'high');
  assert.equal(node('#assistant-app').value,'codex');assert.equal(context.state.newChatConnection,undefined);
  await node('#assistant-pick-child').onclick();await context.saveChatModel();
  assert.equal(node('#assistant-child-model').value,'codex-model');
  assert.equal(node('#assistant-model').value,'codex-model');assert.equal(node('#assistant-effort').value,'high');
  node('#assistant-app').value='hermes';node('#assistant-app').onchange();
  assert.equal(node('#assistant-model').value,'');assert.equal(node('#assistant-effort').value,'');assert.equal(node('#assistant-child-model').value,'');
  context.api=originalApi;
  // Late responses cannot populate the next workspace with previous profiles.
  let release;context.api=()=>new Promise(resolve=>{release=resolve;});
  const pending=work.renderAssistants(host);context.state.data.workspace='B';release(profiles);await pending;
  assert.equal(host.innerHTML,'<p role="status">Loading assistants…</p>');
  context.state.chatMeta=null;context.state.liveJob=null;work.renderDelegation();assert.equal(node('#delegated-work').hidden,true,'A new chat without a job must render without freezing navigation');
  console.log('Work views passed: history navigation, shared model/effort picker, stale-request isolation, active-agent visibility, and honest read errors.');
})().catch(error=>{console.error(error);process.exitCode=1;});
