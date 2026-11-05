/* Exercise the shipped composer module without another browser/build dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const nodes=new Map(),events={},calls=[],pending=[],newChats=[];let formValues=[['name','Finish the offer brief'],['target','A useful brief']],copied='',slowResolve=null,slowGoal=null,reusedGoal='',reusedNewGoal,failGoalLink=false;
function node(id){
 if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',hidden:id==='#composer-menu',isConnected:true,value:'',dataset:{},selectionStart:0,attributes:{},listeners:{},
  addEventListener(name,fn){(this.listeners[name]??=[]).push(fn);},querySelectorAll(){return [];},querySelector(s){return node(id+' '+s);},
  setAttribute(k,v){this.attributes[k]=v;},removeAttribute(k){delete this.attributes[k];},focus(){},close(){this.open=false;},
  insertAdjacentHTML(where,text){this.innerHTML+=text;},setRangeText(text,start,end){this.value=this.value.slice(0,start)+text+this.value.slice(end);this.selectionStart=start+text.length;}});
 return nodes.get(id);
}
const state={business:'studio',data:{workspace:'A',connection:{selected:'configured'},records:[{ref:'obj_goal',type:'Objective',title:'Launch',data:{id:'obj_goal',name:'Launch',status:'active'}},{ref:'obj_effort',type:'Objective',title:'Proposal',data:{id:'obj_effort',name:'Proposal',status:'active',extensions:{businessos:{goal:{scope:'chat',workspace_goal_ref:'obj_goal'}}}}}]},chatMeta:null,chat:[],selectedFiles:[],fileDetailTicket:0};
const fixture={kind:'file',id:'attachments/studio/research.txt',label:'Research',description:'Workspace file'};
state.pendingComposerDraft={references:[fixture],goal_id:'obj_goal'};
const context={setDetailBack(label,run){context.detailBack=run;},appName:id=>id,humanError:error=>error?.message||String(error),window:{},state,URLSearchParams,TextEncoder,Uint8Array,crypto:crypto.webcrypto,setTimeout,clearTimeout,
 FormData:class{constructor(){return formValues[Symbol.iterator]();}},cache:{clear(){}},refresh:async()=>{},
 document:{querySelector:()=>null,addEventListener:(name,fn)=>(events[name]??=[]).push(fn)},$:node,
 esc:v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),
 pretty:v=>typeof v==='string'?v:JSON.stringify(v),human:v=>v,empty:v=>`<p>${v}</p>`,notice(){},
 goalInfo:g=>g?.extensions?.businessos?.goal||{},workspaceGoalRecords:()=>state.data.records.filter(r=>r.type==='Objective'&&r.data),
 navigator:{clipboard:{writeText:async text=>{copied=text;}}},
 chatScope:()=>JSON.stringify([state.data.workspace,state.business,state.chatMeta?.id||'']),
 rememberChatDraft(){},renderComposerFiles(){context.window.auraCompose?.render();},composerConnection:()=>({kind:'configured',model:'fixture'}),
 details:(title,html)=>{state.fileDetailTicket++;node('#detail').open=true;node('#detail-content').innerHTML=html;},
 attempt:fn=>{const p=Promise.resolve().then(fn);pending.push(p);return p;},
 newShellChat:async draft=>{newChats.push(draft);state.chatMeta=null;node('#request').value=draft?.text||'';},
 api:async(path,data)=>{calls.push({path,data});
  if(path.startsWith('/api/context?')){if(path.includes('q=slow'))return new Promise(resolve=>{slowResolve=resolve;});return {items:[fixture],total:1};}
  if(path==='/api/context/message')return {text:state.chat[data.index].text,files:[],references:[fixture],goal_id:reusedGoal,new_chat_goal_id:reusedNewGoal,connection:{kind:'configured'}};
  if(path.startsWith('/api/goals?'))return new Promise(resolve=>{slowGoal=resolve;});
  if(path==='/api/schedules')return {items:[{id:'task',name:'Review',description:'basis'}],notes:[]};
  if(path==='/api/goals'&&data.action==='save')return {goal:{id:data.id||'obj_created'}};
  if(path==='/api/goals'&&data.action==='link_chat'&&failGoalLink)throw new Error('Link unavailable');
  return {};
 },
};
vm.createContext(context);vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),context);
const ui=context.window.auraCompose,flush=()=>new Promise(r=>setImmediate(r)),delay=()=>new Promise(r=>setTimeout(r,170));
function click(dataset,id=''){for(const fn of events.click||[])fn({target:{closest:selector=>selector==='button'?{id,dataset,hasAttribute:name=>Object.hasOwn(dataset,name.replace(/^data-/, '').replace(/-([a-z])/g,(_,c)=>c.toUpperCase()))}:selector==='#chat-form'?{}:null}});}
function input(text){const el=node('#request');el.value=text;el.selectionStart=text.length;for(const fn of el.listeners.input||[])fn({});}
(async()=>{
 assert.equal(ui.draft().references[0].id,fixture.id,'A composer module loaded after initial hydration must restore selected context');
 ui.restore({references:[{...fixture,label:'<Research>'}],goal_id:'obj_goal'});assert.equal(ui.draft().references.length,1);assert.match(node('#composer-contexts').innerHTML,/&lt;Research&gt;/);
 ui.restore({goal_id:'obj_effort'});assert.match(node('#composer-contexts').innerHTML,/Chat goal: Proposal/);assert.match(node('#composer-contexts').innerHTML,/Workspace goal: Launch/);
 state.contextReferences=[];ui.restore({});await ui.choose();
 node('#compose-found').onclick({target:{closest:()=>({dataset:{composePick:'0'}})}});await Promise.all(pending);assert.equal(state.contextReferences[0].id,fixture.id);
 input('owner@example.com');await delay();assert.equal(node('#composer-menu').hidden,true,'Email addresses must stay ordinary text');
 input('/unrecognized');await delay();assert.equal(node('#composer-menu').hidden,true,'Unknown slash text must not execute an Aura action');
 input('/new');await delay();assert.equal(node('#composer-menu').hidden,false);
 let prevented=false;for(const fn of node('#request').listeners.keydown||[])fn({key:'Enter',preventDefault(){prevented=true;},stopImmediatePropagation(){}});
 await flush();await Promise.all(pending);assert.equal(prevented,true);assert.equal(newChats.length,1,'Selecting the shortcut calls the existing action once');
 input('@slow');await delay();assert.ok(slowResolve);ui.closeMenu();slowResolve({items:[fixture]});await flush();assert.equal(node('#composer-menu').hidden,true,'A late lookup must not reopen a dismissed picker');
 state.chatMeta={id:'chat',agent:'configured'};state.chat=[{role:'user',text:'Original **prompt**\nKeep this formatting.'}];
 assert.match(ui.actions(state.chat[0],0),/aria-label="Copy prompt"/);assert.doesNotMatch(ui.actions(state.chat[0],0),/Reuse prompt|Use in new chat|>Copy</);assert.equal(ui.actions({role:'assistant'},1),'');
 click({messageCopy:'0'});await Promise.all(pending);assert.equal(copied,state.chat[0].text);
 node('#request').value='Keep my draft';await ui.reuse(0);assert.equal(node('#request').value,'Keep my draft');
 node('#reuse-add').onclick();assert.match(node('#request').value,/Keep my draft\n\nOriginal/);
 await ui.reuse(0,true);assert.equal(newChats.at(-1).text,state.chat[0].text);assert.equal(newChats.at(-1).references[0].id,fixture.id);
 state.chatMeta={id:'chat',agent:'configured'};reusedGoal='obj_effort';reusedNewGoal='obj_goal';await ui.reuse(0,true);assert.equal(newChats.at(-1).goal_id,'obj_goal','A new chat must use only the shared goal, not another chat’s effort');
 state.chatMeta={id:'chat',agent:'configured'};reusedNewGoal='';await ui.reuse(0,true);assert.equal(newChats.at(-1).goal_id,'','An explicitly unavailable transfer must not fall back to the original effort');reusedNewGoal=undefined;
 assert.equal(calls.some(c=>c.path==='/api/chat'),false,'Reuse never submits model work');
 state.chatMeta={id:'chat',goal_id:'obj_current'};node('#request').value='';reusedGoal='obj_old';await ui.reuse(0);
 assert.equal(node('#request').value,'','A different original goal must require an explicit reuse choice');
 assert.match(node('#detail-content').innerHTML,/different goal/);node('#reuse-add').onclick();assert.equal(state.chatMeta.goal_id,'obj_current');
 state.contextReferences=Array.from({length:12},(_,i)=>({kind:'file',id:'file'+i}));node('#request').value='Keep context';await ui.reuse(0);node('#reuse-add').onclick();assert.equal(node('#request').value,'Keep context','Reference limits must not partly modify a draft');
 const opening=ui.openGoal('obj_slow');await flush();context.details('A newer panel','Keep this panel');slowGoal({goal:{name:'Old goal'}});await opening;
 assert.equal(node('#detail-content').innerHTML,'Keep this panel','Late goal reads must not replace a newer panel');
 const many=ui.openGoal('obj_many');await flush();slowGoal({goal:{name:'Launch'},goal_basis:'basis',assets:[],chats:Array.from({length:25},(_,i)=>({id:'chat'+i,title:'Work '+i,status:'working'})),running_chats:[],task_links:{task:'obj_many'}});await many;
 assert.equal((node('#goal-chats').innerHTML.match(/data-chat=/g)||[]).length,20);assert.match(node('#goal-chats').innerHTML,/Last observed working/);
 node('#goal-chats-more').onclick();assert.equal((node('#goal-chats').innerHTML.match(/data-chat=/g)||[]).length,25);
 assert.equal(state.schedules.items[0].id,'task','Goal task links must populate the existing task-detail inventory');
 state.chatMeta={id:'chat',goal_id:'obj_goal'};node('#request').value='Draft remains';ui.prepareContinuation();assert.equal(node('#request').value,'Draft remains');
 node('#add-continuation-draft').onclick();assert.match(node('#request').value,/without repeating completed external actions/);
 state.chatMeta={id:'chat'};click({},'choose-goal');await flush();await Promise.all(pending);
 assert.match(node('#detail-content').innerHTML,/Goal|accomplish/);assert.doesNotMatch(node('#detail-content').innerHTML,/name="horizon"|name="status"|compose-kind/);
 const form=node('#compose-goal-form'),submit=()=>form.onsubmit({preventDefault(){},currentTarget:form});
 failGoalLink=true;submit();await flush();await Promise.all(pending);assert.equal(state.chatMeta.goal_id,undefined);
 failGoalLink=false;submit();await flush();await Promise.all(pending);
 assert.equal(state.chatMeta.goal_id,'obj_created','Creating a chat goal must link it to that chat');
 const saves=calls.filter(c=>c.path==='/api/goals'&&c.data.action==='save');assert.equal(saves.at(-2).data.status,'active');assert.equal(saves.at(-1).data.id,'obj_created','Retrying a failed link must not create duplicate goals');
 assert.equal(saves.at(-2).data.scope,'chat');assert.equal(saves.at(-2).data.chat_id,'chat','Chat-created goals must carry their scope and owner');
 assert.equal(calls.some(c=>c.path==='/api/chat'),false,'Creating a goal must not submit a model request');
 const manager=ui.manageGoals();await flush();slowGoal({items:[{id:'obj_goal',name:'Launch',status:'active'},{...state.data.records[1].data,status:'completed'}],deleted_items:[{id:'obj_removed',name:'Old effort',status:'paused',extensions:{businessos:{goal:{scope:'chat',deleted_at:1}}}}]});await manager;
 assert.match(node('#goal-manager-list').innerHTML,/Launch/);assert.doesNotMatch(node('#goal-manager-list').innerHTML,/Proposal|Old effort/);
 node('#goal-manager-show').value='completed';node('#goal-manager-show').onchange();assert.match(node('#goal-manager-list').innerHTML,/Proposal/);assert.doesNotMatch(node('#goal-manager-list').innerHTML,/data-compose-goal="obj_goal"/);
 node('#goal-manager-scope').value='workspace';node('#goal-manager-scope').onchange();assert.doesNotMatch(node('#goal-manager-list').innerHTML,/obj_effort/);node('#goal-manager-scope').value='all';
 node('#goal-manager-show').value='deleted';node('#goal-manager-show').onchange();assert.match(node('#goal-manager-list').innerHTML,/Old effort/);
 node('#goal-manager-show').value='current';node('#goal-manager-scope').value='workspace';node('#goal-manager-find').value='Launch';node('#goal-manager-find').oninput();
 node('#detail-content').scrollTop=145;const inspectGoal=ui.openGoal('obj_goal');await flush();slowGoal({goal:state.data.records[0].data,chats:[],assets:[],task_links:{},running_chats:[],chat_goals:[state.data.records[1].data]});await inspectGoal;
 assert.match(node('#detail-content').innerHTML,/Connected chat goals/);node('#detail-content').scrollTop=0;click({goalBack:''});await flush();slowGoal({items:state.data.records.map(r=>r.data),deleted_items:[]});await Promise.all(pending);
 assert.equal(node('#detail-content').scrollTop,145);assert.equal(node('#goal-manager-find').value,'Launch');assert.equal(node('#goal-manager-scope').value,'workspace','Returning to the list must preserve scope and search');
 const taskHost=node('#assignment'),assignment=ui.assignTask({id:'task'},taskHost);await flush();slowGoal({items:[state.data.records[0].data],task_links:{task:'obj_goal'}});await assignment;
 const callCount=calls.length;node('#task-goal').value='obj_goal';node('#task-goal').onchange();assert.equal(calls.length,callCount,'Picking a task goal must not launch an update');assert.equal(node('#task-goal-update').disabled,false,'An explicit update can refresh an existing goal preflight');
 const deletes=calls.filter(c=>c.data?.action==='delete').length;click({goalDelete:'obj_effort',linkedTasks:'0'});await flush();assert.match(node('#detail-content').innerHTML,/data-confirm-delete-goal=/);assert.equal(calls.filter(c=>c.data?.action==='delete').length,deletes,'Opening deletion confirmation must not delete the goal');
 const promotes=calls.filter(c=>c.data?.scope==='workspace').length;click({goalPromote:'obj_effort'});await flush();assert.match(node('#detail-content').innerHTML,/connection to the existing workspace goal will be removed/);assert.equal(calls.filter(c=>c.data?.scope==='workspace').length,promotes,'Promotion must explain the removed parent connection before changing scope');
 // Workspace goal controls must never silently target a background chat.
 state.view='business';state.chatMeta={id:'background',goal_id:'obj_goal'};
 const goalData={goal:{...state.data.records[0].data,target:{metric:'Published landing page',value:1}},chats:[],assets:[],task_links:{},running_chats:[],chat_goals:[]};
 const pageGoal=ui.openGoal('obj_goal');await flush();slowGoal(goalData);await pageGoal;
 assert.match(node('#detail-content').innerHTML,/data-goal-start=/);assert.doesNotMatch(node('#detail-content').innerHTML,/data-goal-connect=|Remove from this chat/);
 const editStructured=ui.editGoal('obj_goal');await flush();slowGoal(goalData);await editStructured;
 assert.match(node('#detail-content').innerHTML,/textarea name="target"/);assert.match(node('#detail-content').innerHTML,/Published landing page/);
 formValues=[['name','Launch'],['target',JSON.stringify(goalData.goal.target)]];
 node('#compose-goal-form').onsubmit({preventDefault(){},currentTarget:node('#compose-goal-form')});await flush();
 assert.equal(calls.filter(c=>c.path==='/api/goals'&&c.data.action==='save').at(-1).data.target,undefined,'Editing another field must preserve structured completion criteria');
 slowGoal(goalData);await Promise.all(pending);
 const localGoal=ui.openGoal('obj_effort');await flush();slowGoal({...goalData,goal:{...state.data.records[1].data,extensions:{businessos:{goal:{scope:'chat',chat_id:'background'}}}},chats:[{id:'background',title:'Background chat'}]});await localGoal;
 assert.match(node('#detail-content').innerHTML,/data-chat="background">Open chat/,'A chat goal viewed from Business & memory must offer its owner even when it is the background chat');
 assert.doesNotMatch(node('#detail-content').innerHTML,/data-goal-use=|Remove from this chat/);
 state.view='home';state.chatMeta=null;
 // Exercise refresh completion, failure and navigation against the shipped functions.
 const appSource=fs.readFileSync(require('node:path').join(require('node:path').dirname(process.argv[2]),'app.js'),'utf8');
 const opened=[],recordContext={state:{data:{records:[{ref:'asset_local',type:'Asset',data:{location_reference:'attachments/studio/work.txt'}},{ref:'obj_goal',type:'Objective',data:{}}]}},attempt:fn=>fn(),openFileWorkspace:ref=>opened.push(ref),window:{auraCompose:{openGoal:ref=>opened.push(ref)}}};
 vm.createContext(recordContext);vm.runInContext(appSource.slice(appSource.indexOf('function recordDetails('),appSource.indexOf('async function openFileWorkspace(')),recordContext);
 recordContext.recordDetails('asset_local');recordContext.recordDetails('obj_goal');assert.deepEqual(opened,['asset/asset_local','obj_goal'],'Memory records must open the same file and goal views as their other entry points');
 let finishRead,failRead,refreshMessage='',refreshScope='chat';
 const refreshState={chatMeta:{id:'chat'},chat:[{role:'user',text:'Saved'}],busy:false},refreshNodes={};
 const refreshContext={humanError:error=>error?.message||String(error),state:refreshState,AbortSignal,encodeURIComponent,window:{auraContinuity:{acceptRecovery(){}}},
  $:s=>refreshNodes[s]??={value:'Keep this draft',disabled:false},chatScope:()=>refreshScope,
  api:()=>new Promise((resolve,reject)=>{finishRead=resolve;failRead=reject;}),
  renderComposerConnection(){},taskStatus(){},notice:text=>{refreshMessage=text;},showMessages(){},chatControls(){},attempt(){},pollJob(){}};
 vm.createContext(refreshContext);vm.runInContext(appSource.slice(appSource.indexOf('async function refreshChat(){'),appSource.indexOf('async function saveProfilePicture')),refreshContext);
 let reading=refreshContext.refreshChat();assert.equal(refreshState.refreshingChat,true);assert.equal(refreshContext.$('#request').disabled,false);
 finishRead({messages:[{text:'Latest'}],chat:{id:'chat'},job:null});await reading;
 assert.equal(refreshState.refreshingChat,false);assert.equal(refreshState.chat[0].text,'Latest');assert.equal(refreshMessage,'Chat is up to date.');assert.equal(refreshContext.$('#request').value,'Keep this draft');
 reading=refreshContext.refreshChat();failRead(new Error('Native app unavailable'));await reading;
 assert.equal(refreshState.refreshingChat,false);assert.match(refreshMessage,/unavailable/);
 reading=refreshContext.refreshChat();refreshScope='another-chat';finishRead({messages:[{text:'Wrong chat'}],chat:{id:'chat'}});await reading;assert.equal(refreshState.chat[0].text,'Latest');
 refreshScope='chat';reading=refreshContext.refreshChat();refreshState.chat=[{text:'A newer turn'}];finishRead({messages:[{text:'Older read'}],chat:{id:'chat'}});await reading;assert.equal(refreshState.chat[0].text,'A newer turn');
 console.log('Composer UI passed: context chips, email handling, explicit shortcuts, stale lookups, draft-safe reuse and manual continuation.');
})().catch(error=>{console.error(error);process.exitCode=1;});
