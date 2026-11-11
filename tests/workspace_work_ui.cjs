/* DOM-independent view checks; no browser, network, or frontend dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const nodes=new Map(),listeners={};
function node(id){if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',hidden:false,isConnected:true,value:'',dataset:{},classes:{},classList:{toggle(name,on){this[name]=on;}},setAttribute(name,value){this[name]=value;},querySelectorAll:()=>[],querySelector:selector=>node(id+' '+selector),addEventListener(){},insertAdjacentHTML(where,text){this.innerHTML+=text;},showModal(){this.open=true;},close(){this.open=false;}});return nodes.get(id);}
const profiles={items:[{id:'jeff',name:'<Jeff>',instructions:'Find useful evidence.',task_ids:['weekly']}],chats:[],workspace:'A'};
const tasks={items:[{id:'weekly',name:'Weekly review',owner:'hermes'}],notes:[]};
const history={items:[{id:'report.md',name:'Weekly findings',status:'Saved result'}],limit:20,note:''};
let opened=null,nativePreview=null;
const context={URLSearchParams,humanError:error=>error?.message||String(error),window:{},document:{addEventListener:(name,callback)=>(listeners[name]??=[]).push(callback)},
  state:{data:{workspace:'A',connection:{choices:[],selected:'codex'}},business:'studio',view:'assistants',chatMeta:{id:'parent'}},
  $:node,esc:value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),
  empty:text=>`<p>${text}</p>`,appName:name=>name,chatDate:at=>String(at),chatMarkdown:text=>`<p>${text}</p>`,
  scheduleRow:t=>`<button data-schedule="${t.id}">${t.name}</button>`,
  details:(title,html)=>{opened={title,html};context.state.fileDetailTicket=(context.state.fileDetailTicket||0)+1;node('#detail-content').innerHTML=html;node('#detail').open=true;},notice:()=>{},nativeApps:['codex','pi','hermes'],
  api:async path=>(path.startsWith('/api/assistants')||path.startsWith('/api/agents'))?profiles:path.split('?')[0]==='/api/schedules'?tasks:path.startsWith('/api/schedules/history')?history:{name:'Weekly review',file:'Report',text:'Useful findings',owner:'codex',native_id:'native-run'},
  attempt:fn=>Promise.resolve().then(fn),addNativeChat:async(kind,id)=>{nativePreview={kind,id};},
};
vm.createContext(context);vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),context);
// Exercise the existing shared picker directly, without starting the app shell.
const appSource=fs.readFileSync(require('node:path').join(require('node:path').dirname(process.argv[2]),'app.js'),'utf8');
vm.runInContext(appSource.slice(appSource.indexOf('function nativeConnection('),appSource.indexOf('function applyAppearance(')),context);
const pickerStart=appSource.indexOf('let chatModelTicket=0;'),pickerEnd=appSource.indexOf("\ndocument.addEventListener('click',event=>attempt",pickerStart);
Object.assign(context,{cachedApi:(...args)=>context.api(...args),openAnchoredSurface:dialog=>{dialog.showModal();return true;},pickerSave:Promise.resolve(),structuredClone,human:s=>s[0].toUpperCase()+s.slice(1),
  modelPicker:()=>({favorites:['catalog-model']}),chatScope:()=>JSON.stringify([context.state.data.workspace,context.state.business,context.state.chatMeta?.id]),
  composerConnection:()=>({kind:'codex',model:'',effort:''})});
vm.runInContext(appSource.slice(pickerStart,pickerEnd),context);
vm.runInContext(appSource.slice(appSource.indexOf('function renderComposerPermissions(){'),appSource.indexOf('function renderComposerConnection(){')),context);
const originalPermissionChat=context.state.chatMeta;
context.state.data.full_access_modes=['full','bypassPermissions','yolo'];context.state.data.harness_permissions={codex:'full'};
context.renderComposerPermissions();assert.equal(node('#chat-permissions').classList['permission-unrestricted'],true,'An inherited explicit full-access default must stand out');
context.state.chatMeta={id:'scoped',permission_mode:'read-only'};context.renderComposerPermissions();assert.equal(node('#chat-permissions').classList['permission-unrestricted'],false);
context.state.data.harness_permissions={};context.state.chatMeta=originalPermissionChat;context.renderComposerPermissions();assert.equal(node('#chat-permissions').classList['permission-unrestricted'],false,'Unknown native settings must not be claimed to be full access');

(async()=>{
  const work=context.window.auraWork,host=node('host');
  await work.renderAssistants(host);
  assert(node('#assistant-list').innerHTML.includes('&lt;Jeff&gt;'));
  assert(!node('#assistant-list').innerHTML.includes('<Jeff>'));
  // HTML named controls can shadow form.id. A real submission must still save.
  const formApi=context.api;let submitted=0;
  context.FormData=class {constructor(form){return Object.entries(form.data);}};
  context.api=async(path,data)=>{
    if(path==='/api/assistants'&&data){submitted++;profiles.items.push({id:'saved-form',name:data.name,instructions:data.instructions,task_ids:[]});return profiles;}
    return formApi(path);
  };
  const form={id:{tagName:'INPUT',name:'id'},matches:selector=>selector==='form#assistant-form',
    data:{id:'',name:'Saved from form',instructions:'Useful instructions'},querySelector:()=>({disabled:false,isConnected:false}),isConnected:true};
  for(const handler of listeners.submit||[])handler({target:form,preventDefault(){}});
  await new Promise(resolve=>setImmediate(resolve));
  assert.equal(submitted,1,'A named id control prevented assistant submission');
  assert.match(opened.html,/Useful instructions/);
  context.api=formApi;profiles.items.pop();
  const savedProfiles=profiles.items;profiles.items=[];
  await work.assignTask({id:'weekly'},host);assert.equal(host.hidden,true,'Tasks must not show a selector without choices');
  profiles.items=savedProfiles;profiles.running=[];
  assert.equal(work.assignChat,undefined,'Whole-chat reassignment must not be exposed in the interface');
  const assignmentApi=context.api;let assignedRequest;
  tasks.items.push({id:'other',name:'Pricing review',owner:'hermes'});
  profiles.items.push({id:'janice',name:'Janice',task_ids:['other']});
  context.api=async(path,data)=>{if(data?.action==='assign_task'){assignedRequest=data;throw new Error('Could not save assignment');}return assignmentApi(path);};
  await work.chooseTask('jeff');assert.match(node('#assistant-task-choices').innerHTML,/Pricing review/);assert.match(node('#assistant-task-choices').innerHTML,/Assigned to Janice/);assert.match(node('#assistant-task-choices').innerHTML,/Move here/);
  assert.doesNotMatch(node('#assistant-task-choices').innerHTML,/data-assign-existing-task="weekly"/,'Tasks already assigned here are not offered again');
  const pickEvent={target:{closest:()=>({dataset:{assignExistingTask:'other'},hasAttribute:()=>false,isConnected:true})}};
  await node('#assistant-task-choices').onclick(pickEvent);assert.equal(node('#assistant-task-status').textContent,'Could not save assignment');assert.equal(profiles.items[1].task_ids[0],'other');
  context.api=async(path,data)=>{if(data?.action==='assign_task'){assignedRequest=data;profiles.items[1].task_ids=[];profiles.items[0].task_ids.push('other');return profiles;}return assignmentApi(path);};
  await node('#assistant-task-choices').onclick(pickEvent);assert.equal(assignedRequest.task_id,'other');assert.equal(assignedRequest.id,'jeff');assert.match(opened.html,/data-schedule="other"/,'Assigned tasks appear on the assistant page');
  context.api=assignmentApi;tasks.items.pop();profiles.items.pop();profiles.items[0].task_ids=['weekly'];
  await work.chooseTask('jeff');assert.match(node('#assistant-task-choices').innerHTML,/already assigned/);
  let releaseTasks;context.api=path=>path.split('?')[0]==='/api/schedules'?new Promise(resolve=>{releaseTasks=resolve;}):assignmentApi(path);
  const oldPicker=work.chooseTask('jeff');await new Promise(resolve=>setImmediate(resolve));context.details('A newer panel','Keep this panel');releaseTasks(tasks);await oldPicker;assert.equal(node('#detail-content').innerHTML,'Keep this panel','A late task read must not replace a newer panel');context.api=assignmentApi;
  assert.doesNotMatch(appSource,/auraWork\?\.assignChat/,'Chat details must not offer reassignment');
  await work.overview('jeff');assert(opened.html.includes('data-schedule="weekly"'));
  assert(opened.html.includes('New chat with &lt;Jeff&gt;'));
  profiles.chats=Array.from({length:25},(_,i)=>({id:'chat-'+i,title:'Work '+i,assistant_id:'jeff',agent:'codex',updated:i}));
  await work.overview('jeff');assert(node('#assistant-chat-list').innerHTML.includes('Show more chats'));
  assert(!node('#assistant-chat-list').innerHTML.includes('data-chat="chat-24"'));
  node('#assistant-chat-list').onclick({target:{closest:()=>({})}});
  assert(node('#assistant-chat-list').innerHTML.includes('data-chat="chat-24"'));
  node('#assistant-chat-search').value='Work 24';node('#assistant-chat-search').oninput();
  assert(node('#assistant-chat-list').innerHTML.includes('data-chat="chat-24"')&&!node('#assistant-chat-list').innerHTML.includes('data-chat="chat-0"'));
  vm.runInContext(appSource.slice(appSource.indexOf('function scheduleTimestamp('),appSource.indexOf('async function scheduleOperation(')),context);
  vm.runInContext(appSource.slice(appSource.indexOf('function taskSummary('),appSource.indexOf('function showScheduleExample(')),context);
  const due=Date.now()+86400000;
  const upcoming=context.taskSummary({app:'Hermes',next_run:due});
  assert(upcoming.includes('No previous run reported')&&upcoming.includes(new Date(due).toLocaleString()));
  const failed=context.taskSummary({app:'Hermes',last_status:'error',last_run:'1700000000',last_error:'Could not read <file>',status:'paused',next_run:due});
  assert(failed.includes('Failed')&&failed.includes('Could not read &lt;file&gt;')&&failed.includes('Paused')&&!failed.includes(new Date(due).toLocaleString()));
  assert.equal(context.taskLastRun({last_run:1700000000}),context.taskLastRun({last_run:1700000000000}));
  history.items.push({id:'earlier.md',name:'Earlier findings',status:'Saved result'});
  await work.history(tasks.items[0],host);assert(host.innerHTML.includes('Open latest saved result · Weekly findings'));
  assert(host.innerHTML.includes('Earlier results (1)')&&host.innerHTML.includes('data-task-run="report.md"'));history.items.pop();
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
  const catalogs=[],catalog=(kind,label=kind)=>({picker:{favorites:[]},unavailable:[],models:[{id:'catalog-model',name:label+' model',provider:'test',routes:[{agent:kind,model:kind+'-model',current:true,efforts:['low','high'],default_effort:'low'}]}]});
  context.api=async path=>path.startsWith('/api/model-catalog')?new Promise(resolve=>catalogs.push(resolve)):path.startsWith('/api/agent-efforts')?{efforts:['low','high'],default_effort:'low'}:originalApi(path);
  const first=context.openChatModels();await new Promise(resolve=>setImmediate(resolve));
  context.state.chatModelDraft.kind='hermes';const middle=context.loadChatModelOptions();await new Promise(resolve=>setImmediate(resolve));
  context.state.chatModelDraft.kind='codex';const newest=context.loadChatModelOptions();await new Promise(resolve=>setImmediate(resolve));
  catalogs[2](catalog('codex','new-codex'));await newest;
  catalogs[1](catalog('hermes'));await middle;catalogs[0](catalog('codex','old-codex'));await first;
  assert.equal(context.state.chatModelOptions.models[0].name,'new-codex model');
  // Assistant choices use that same picker; they never modify the current chat.
  let effortQueries=0;context.api=async path=>{if(path.startsWith('/api/agent-efforts')){effortQueries++;return {efforts:['low','high'],default_effort:'low'};}return path.startsWith('/api/model-catalog')?catalog('codex'):originalApi(path);};
  const create={dataset:{},hasAttribute:name=>name==='data-assistant-new'};
  for(const callback of listeners.click)callback({target:{closest:()=>create}});
  await new Promise(resolve=>setImmediate(resolve));
  await node('#assistant-pick-model').onclick();node('#chat-effort-choice').value='high';await context.saveChatModel();
  assert.equal(node('#assistant-model').value,'codex-model');assert.equal(node('#assistant-effort').value,'high');
  assert.equal(node('#assistant-app').value,'codex');assert.equal(context.state.newChatConnection,undefined);assert.equal(effortQueries,0,'Reported catalog efforts must not start another native metadata request');
  await node('#assistant-pick-child').onclick();await context.saveChatModel();
  assert.equal(node('#assistant-child-model').value,'codex-model');
  assert.equal(node('#assistant-model').value,'codex-model');assert.equal(node('#assistant-effort').value,'high');
  node('#assistant-app').value='hermes';node('#assistant-app').onchange();
  assert.equal(node('#assistant-model').value,'');assert.equal(node('#assistant-effort').value,'');assert.equal(node('#assistant-child-model').value,'');
  context.api=originalApi;
  // Late responses cannot populate the next workspace with previous profiles.
  let release;context.api=()=>new Promise(resolve=>{release=resolve;});
  const pending=work.renderAssistants(host);context.state.data.workspace='B';release(profiles);await pending;
  assert.equal(host.innerHTML,'<p role="status">Loading agents…</p>');
  context.state.chatMeta=null;context.state.liveJob=null;work.renderDelegation();assert.equal(node('#delegated-work').hidden,true,'A new chat without a job must render without freezing navigation');
  // A late trace from another chat/request must never populate the current view.
  context.queueMicrotask=()=>{};context.human=value=>String(value);context.state.busy=false;
  const traceReplies=[];context.api=path=>path.startsWith('/api/profile')?Promise.resolve({activity_view:'off'}):new Promise(resolve=>traceReplies.push(resolve));
  vm.runInContext(fs.readFileSync(require('node:path').join(require('node:path').dirname(process.argv[2]),'workspace-insight.js'),'utf8'),context);
  const insight=context.window.auraInsight;context.state.chatMeta=null;context.state.liveJob=undefined;insight.render();
  context.state.chatMeta={id:'one',trace_id:'request-one'};insight.render();
  context.state.chatMeta={id:'two',trace_id:'request-two'};insight.render();
  traceReplies[1]({revision:1,items:[{id:'1',kind:'commentary',title:'Current work',text:'<safe>',has_detail:true,owner:''}]});await new Promise(resolve=>setImmediate(resolve));
  traceReplies[0]({revision:1,items:[{id:'1',kind:'commentary',title:'Stale private work',text:'Wrong chat',owner:''}]});await new Promise(resolve=>setImmediate(resolve));
  assert.match(node('#native-activity').innerHTML,/Current work/);assert.doesNotMatch(node('#native-activity').innerHTML,/Stale private work/);assert.match(node('#native-activity').innerHTML,/&lt;safe&gt;/);
  // Switching requests within the same chat needs the same isolation.
  context.state.chatMeta={id:'three',trace_id:'old-request'};insight.render();
  context.state.chatMeta.trace_id='new-request';insight.render();
  traceReplies[3]({revision:1,items:[{id:'1',kind:'commentary',title:'New request',text:'Current',owner:''}]});await new Promise(resolve=>setImmediate(resolve));
  traceReplies[2]({revision:1,items:[{id:'1',kind:'commentary',title:'Old request',text:'Late',owner:''}]});await new Promise(resolve=>setImmediate(resolve));
  assert.match(node('#native-activity').innerHTML,/New request/);assert.doesNotMatch(node('#native-activity').innerHTML,/Old request/);
  node('#activity-view').value='off';await node('#activity-view').onchange();await new Promise(resolve=>setImmediate(resolve));
  assert.doesNotMatch(node('#native-activity').innerHTML,/New request/);assert.equal(node('#delegated-work').hidden,true);
  console.log('Work views passed: history navigation, shared model/effort picker, stale-request isolation, active-agent visibility, and honest read errors.');
})().catch(error=>{console.error(error);process.exitCode=1;});
