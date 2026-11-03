/* Exercise the shipped composer module without another browser/build dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const nodes=new Map(),events={},calls=[],pending=[],newChats=[];let copied='',slowResolve=null,slowGoal=null,reusedGoal='',failGoalLink=false;
function node(id){
 if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',hidden:id==='#composer-menu',isConnected:true,value:'',dataset:{},selectionStart:0,attributes:{},listeners:{},
  addEventListener(name,fn){(this.listeners[name]??=[]).push(fn);},querySelectorAll(){return [];},querySelector(s){return node(id+' '+s);},
  setAttribute(k,v){this.attributes[k]=v;},removeAttribute(k){delete this.attributes[k];},focus(){},close(){this.open=false;},
  insertAdjacentHTML(where,text){this.innerHTML+=text;},setRangeText(text,start,end){this.value=this.value.slice(0,start)+text+this.value.slice(end);this.selectionStart=start+text.length;}});
 return nodes.get(id);
}
const state={business:'studio',data:{workspace:'A',connection:{selected:'configured'},records:[{ref:'obj_goal',type:'Objective',title:'Launch'}]},chatMeta:null,chat:[],selectedFiles:[],fileDetailTicket:0};
const fixture={kind:'file',id:'attachments/studio/research.txt',label:'Research',description:'Workspace file'};
state.pendingComposerDraft={references:[fixture],goal_id:'obj_goal'};
const context={window:{},state,URLSearchParams,TextEncoder,Uint8Array,crypto:crypto.webcrypto,setTimeout,clearTimeout,
 FormData:class{constructor(){return [['name','Finish the offer brief'],['target','A useful brief']][Symbol.iterator]();}},cache:{clear(){}},refresh:async()=>{},
 document:{querySelector:()=>null,addEventListener:(name,fn)=>(events[name]??=[]).push(fn)},$:node,
 esc:v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),
 pretty:v=>typeof v==='string'?v:JSON.stringify(v),human:v=>v,empty:v=>`<p>${v}</p>`,notice(){},
 navigator:{clipboard:{writeText:async text=>{copied=text;}}},
 chatScope:()=>JSON.stringify([state.data.workspace,state.business,state.chatMeta?.id||'']),
 rememberChatDraft(){},renderComposerFiles(){context.window.auraCompose?.render();},composerConnection:()=>({kind:'configured',model:'fixture'}),
 details:(title,html)=>{state.fileDetailTicket++;node('#detail').open=true;node('#detail-content').innerHTML=html;},
 attempt:fn=>{const p=Promise.resolve().then(fn);pending.push(p);return p;},
 newShellChat:async draft=>{newChats.push(draft);state.chatMeta=null;node('#request').value=draft?.text||'';},
 api:async(path,data)=>{calls.push({path,data});
  if(path.startsWith('/api/context?')){if(path.includes('q=slow'))return new Promise(resolve=>{slowResolve=resolve;});return {items:[fixture],total:1};}
  if(path==='/api/context/message')return {text:state.chat[data.index].text,files:[],references:[fixture],goal_id:reusedGoal,connection:{kind:'configured'}};
  if(path.startsWith('/api/goals?'))return new Promise(resolve=>{slowGoal=resolve;});
  if(path==='/api/schedules')return {items:[{id:'task',name:'Review',description:'basis'}],notes:[]};
  if(path==='/api/goals'&&data.action==='save')return {goal:{id:data.id||'obj_created'}};
  if(path==='/api/goals'&&data.action==='link_chat'&&failGoalLink)throw new Error('Link unavailable');
  return {};
 },
};
vm.createContext(context);vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),context);
const ui=context.window.auraCompose,flush=()=>new Promise(r=>setImmediate(r)),delay=()=>new Promise(r=>setTimeout(r,170));
function click(dataset,id=''){for(const fn of events.click||[])fn({target:{closest:selector=>selector==='button'?{id,dataset,hasAttribute:()=>false}:selector==='#chat-form'?{}:null}});}
function input(text){const el=node('#request');el.value=text;el.selectionStart=text.length;for(const fn of el.listeners.input||[])fn({});}
(async()=>{
 assert.equal(ui.draft().references[0].id,fixture.id,'A composer module loaded after initial hydration must restore selected context');
 ui.restore({references:[{...fixture,label:'<Research>'}],goal_id:'obj_goal'});assert.equal(ui.draft().references.length,1);assert.match(node('#composer-contexts').innerHTML,/&lt;Research&gt;/);
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
 assert.equal(calls.some(c=>c.path==='/api/chat'),false,'Creating a goal must not submit a model request');
 // Exercise refresh completion, failure and navigation against the shipped functions.
 const appSource=fs.readFileSync(require('node:path').join(require('node:path').dirname(process.argv[2]),'app.js'),'utf8');
 let finishRead,failRead,refreshMessage='',refreshScope='chat';
 const refreshState={chatMeta:{id:'chat'},chat:[{role:'user',text:'Saved'}],busy:false},refreshNodes={};
 const refreshContext={state:refreshState,AbortSignal,encodeURIComponent,window:{auraContinuity:{acceptRecovery(){}}},
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
