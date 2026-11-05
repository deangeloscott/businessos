/* Real view functions with a small DOM fixture; no browser or frontend dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const nodes=new Map(),listeners={},calls=[];let pending=[];
function node(id){if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',hidden:false,isConnected:true,classList:{toggle(){}},value:'native',dataset:{},querySelectorAll:()=>[],querySelector:s=>node(id+' '+s),contains:()=>false,addEventListener(){},scrollIntoView(){},setAttribute(){},focus(){},close(){this.open=false;}});return nodes.get(id);}
const state={data:{workspace:'A',connection:{selected:'codex',choices:[{id:'codex',name:'Codex',available:true}]}},business:'studio',chatMeta:{id:'chat',agent:'codex'},fileDetailTicket:0};
const context={appName:id=>id||'AI app',anchoredSurface:null,closeAnchoredSurface(){},renderComposerPermissions(){},humanError:error=>error?.message||String(error),window:{},document:{activeElement:null,addEventListener:(name,fn)=>(listeners[name]??=[]).push(fn)},state,$:node,
  esc:v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),
  human:v=>v,chatDate:v=>String(v),empty:v=>`<p>${v}</p>`,URLSearchParams,composerConnection:()=>({kind:'codex'}),
  details:(title,html)=>{state.fileDetailTicket++;node('#detail').open=true;node('#detail-content').innerHTML=html;},
  attempt:fn=>{const p=Promise.resolve().then(fn);pending.push(p);return p;},
  api:(path,data)=>new Promise((resolve,reject)=>calls.push({path,data,resolve,reject})),
  chatScope:()=>JSON.stringify([state.data.workspace,state.business,state.chatMeta?.id||'']),
  rememberChatDraft(){},showMessages(){},chatControls(){},renderShell(){},taskStatus(){},pollJob(){},
};
vm.createContext(context);vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),context);
const flush=()=>new Promise(resolve=>setImmediate(resolve));
function click(id){for(const fn of listeners.click||[])fn({target:{closest:()=>({id})}});}
const permission={choices:[{id:'native',name:'Use harness settings',native:'No override',description:'Follow the settings in your AI app.'},{id:'full',name:'Full access',native:'danger-full-access · never',description:'Allow actions without asking for approval.',unrestricted:true}],mode:'native',default:'native',interactive:true};
(async()=>{
  state.liveJob={id:'job',chat_id:'chat',workspace:'A',requests:[{id:'request',status:'pending',title:'<Approval>',detail:'echo <unsafe>',questions:[{id:'q',text:'Choose?',multiple:true,text:true,options:[{label:'A',value:'A'}]}]}]};
  const host=node('#native-requests');context.window.auraContinuity.renderRequests();
  assert.match(host.innerHTML,/&lt;Approval&gt;/);assert.match(host.innerHTML,/type="checkbox"/);assert.match(host.innerHTML,/Submit answer/);
  host.innerHTML='keep focused editor';context.window.auraContinuity.renderRequests();assert.equal(host.innerHTML,'keep focused editor','Unchanged polling must not replace question inputs');
  state.data.workspace='B';context.window.auraContinuity.renderRequests();assert.equal(host.hidden,true,'A different workspace must not display actionable requests');state.data.workspace='A';
  click('chat-permissions');await flush();assert.match(calls.at(-1).path,/chat_id=chat/);
  context.details('Different page','Keep this page');calls.at(-1).resolve(permission);await Promise.all(pending);pending=[];
  assert.equal(node('#detail-content').innerHTML,'Keep this page','An older permission read must not overwrite another panel');
  click('harness-permissions');await flush();calls.at(-1).resolve(permission);await Promise.all(pending);pending=[];
  assert.match(node('#detail-content').innerHTML,/Default for this AI app/);assert.equal(node('#permissions-native').hidden,true,'Native inheritance does not need boilerplate');
  node('#permissions-mode').value='full';node('#permissions-mode').onchange();assert.match(node('#permissions-native').textContent,/without asking for approval/);const form=node('#permissions-form');form.onsubmit({preventDefault(){},currentTarget:form});await flush();
  assert.equal(calls.at(-1).data.mode,'full');assert.equal(calls.at(-1).data.kind,'codex');assert.equal(calls.at(-1).data.chat_id,undefined,'Editing defaults must not mutate an individual chat');calls.at(-1).resolve({saved:true});await Promise.all(pending);pending=[];
  const originalChat=state.chatMeta;state.chatMeta=null;
  click('chat-permissions');await flush();calls.at(-1).resolve(permission);await Promise.all(pending);pending=[];
  node('#permissions-mode').value='full';const draftForm=node('#permissions-form'),beforeSave=calls.length;
  draftForm.onsubmit({preventDefault(){},currentTarget:draftForm});await Promise.all(pending);pending=[];
  assert.equal(calls.length,beforeSave,'A new chat choice must not write the app-wide default');assert.equal(state.newChatPermission.mode,'full');
  state.chatMeta=originalChat;
  click('other-work');await flush();const old=calls.at(-1);state.business='other';old.resolve({items:[],running_chats:[]});await Promise.all(pending);
  assert.match(node('#detail-content').innerHTML,/Reading workspace activity/,'Results from another business must not be rendered');
  pending=[];state.business='studio';node('#work-activity-search').value='';click('other-work');await flush();
  const observed={chat_id:'chat',title:'Question',status:'working',needs_input:true,agent:'Pi',observed_at:1};
  calls.at(-1).resolve({items:[observed],running_chats:[]});await Promise.all(pending);pending=[];
  assert.match(node('#work-activity-list').innerHTML,/Previously needed input/);
  click('other-work');await flush();calls.at(-1).resolve({items:[observed],running_chats:['chat']});await Promise.all(pending);pending=[];
  assert.match(node('#work-activity-list').innerHTML,/Needs input/);
  node('#history-search').value='';click('workspace-history');await flush();calls.at(-1).resolve({items:[{id:'version',path:'attachments/studio/notes.txt',at:1,bytes:8,reason:'Saved'}]});await Promise.all(pending);pending=[];
  const reviewButton=node('review-version');reviewButton.dataset.historyReview='version';
  node('#history-list').onclick({target:{closest:selector=>selector==='[data-history-review]'?reviewButton:null}});await flush();
  calls.at(-1).resolve({id:'version',path:'attachments/studio/notes.txt',at:1,bytes:8,text:'Earlier',current_revision:'reviewed'});await Promise.all(pending);pending=[];
  node('#history-restore').onclick();await flush();
  assert.equal(calls.at(-1).data.expected_revision,'reviewed');
  calls.at(-1).resolve({restored:true,warning:'Restored successfully, but local history could not be updated.'});await Promise.all(pending);
  assert.match(node('#history-restore-status').textContent,/Restored successfully, but local history/);
  assert.equal(node('#history-restore').disabled,true,'Successful restore with a warning must not invite duplicate submission');
  pending=[];state.needsCheck=true;state.busy=false;state.recovery={state:'interrupted',can_continue:true,message:'Review recent work.',revision:'same'};
  context.window.auraContinuity.renderRecovery();assert.match(node('#chat-reconnect').innerHTML,/Continue chat/);assert.doesNotMatch(node('#chat-reconnect').innerHTML,/Traceback|PID|request_id/);
  node('#request').value='Keep my current draft';click('recovery-continue');await flush();
  assert.equal(calls.at(-1).data.action,'prepare');calls.at(-1).resolve({workspace:'A',messages:[],chat:{id:'chat',agent:'codex',status:'stopped'},recovery:{state:'stopped'},draft:'Continue remaining work.'});await Promise.all(pending);
  assert.equal(node('#request').value,'Keep my current draft','Recovery must not replace an unsent draft');assert.equal(calls.some(c=>c.path==='/api/chat'),false,'Recovery must never submit a prompt');
  pending=[];state.needsCheck=true;click('recovery-check');await flush();const slow=calls.at(-1);state.business='another';slow.resolve({workspace:'A',messages:[{text:'Wrong business'}],chat:{id:'chat'},recovery:{state:'complete'}});await Promise.all(pending);
  assert.equal(state.chat.length,0,'Late recovery must not replace another workspace or business');
  console.log('Continuity views passed: escaped native requests, stable inputs, scope isolation, stale-panel protection, and explicit native defaults.');
})().catch(error=>{console.error(error);process.exitCode=1;});
