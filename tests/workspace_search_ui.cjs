/* Search behavior against the real shell functions, without a browser dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2],'utf8'),nodes=new Map();
const node=id=>{if(!nodes.has(id))nodes.set(id,{value:'',innerHTML:'',textContent:'',hidden:false,focus(){},showModal(){this.open=true;}});return nodes.get(id);};
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const records=[{title:'Customer guide',type:'Asset',ref:'Asset/guide',data:{topic:'retention'}}];
const context={state:{business:'studio',data:{workspace:'A',records}},shellSearchData:null,shellSearchTicket:0,$:node,
  closeAnchoredSurface(){},esc,empty:(title,detail)=>esc(title+' '+detail),appName:id=>id,shareType:type=>type,
  usefulFile:file=>!file.path.startsWith('instances/'),chatDescription:chat=>chat.description||''};
vm.createContext(context);
vm.runInContext(source.slice(source.indexOf("let shellSearchFilter='all'"),source.indexOf('// A deliberately small Markdown renderer')),context);
const chats={items:[{id:'chat',title:'Customer guide',description:'Retention plan'}]};
const files={items:[{name:'Customer guide.md',path:'attachments/guide.md'},{name:'Asset.json',path:'instances/studio/assets/Asset.json'}]};
const library=Array.from({length:78},(_,i)=>({title:'Guide '+String(i).padStart(2,'0'),key:'guide-'+i,kind:'Workflow',description:'retention'}));
library.push({title:'<script>guide</script>',key:'unsafe',kind:'Skill'});
context.api=async()=>chats;context.cachedApi=async path=>path.startsWith('/api/files')?files:library;
(async()=>{
  await context.openShellSearch();
  assert.match(node('#shell-search-status').textContent,/50 of 82 results/);
  assert.doesNotMatch(node('#shell-search-results').innerHTML,/Asset.json|See all matching/);
  node('#shell-search').value='Customer guide';context.paintShellSearch();
  const mixed=node('#shell-search-results').innerHTML;
  for(const label of ['Chat','File','Memory'])assert(mixed.includes('search-result-type">'+label));
  assert(mixed.indexOf('data-chat=')<mixed.indexOf('data-search-file='),'Exact title precedes a partial title');
  vm.runInContext("shellSearchFilter='files'",context);context.paintShellSearch();
  assert.match(node('#shell-search-status').textContent,/^1 result$/);assert(!node('#shell-search-results').innerHTML.includes('data-chat='));
  assert.equal(node('#shell-search').value,'Customer guide','Filtering preserves the query');
  vm.runInContext("shellSearchFilter='all';shellSearchLimit=100",context);node('#shell-search').value='guide';context.paintShellSearch();
  assert.match(node('#shell-search-results').innerHTML,/&lt;script&gt;guide&lt;\/script&gt;/);assert.equal(node('#shell-search-more').hidden,true);
  context.cachedApi=async path=>{if(path==='/api/library')throw Error('unavailable');return files;};
  await context.openShellSearch();assert.match(node('#shell-search-status').textContent,/3 results · Couldn’t search Library/);
  assert.match(node('#shell-search-results').innerHTML,/data-chat="chat"/);
  let resolveChats;context.api=()=>new Promise(resolve=>resolveChats=resolve);
  const stale=context.openShellSearch();context.state.business='other';node('#shell-search-results').innerHTML='Other workspace';resolveChats(chats);await stale;
  assert.equal(node('#shell-search-results').innerHTML,'Other workspace');
  console.log('Workspace search passed: one labeled list, ranking, filters, all-result pagination, escaping, partial availability, and stale-workspace isolation.');
})().catch(error=>{console.error(error);process.exitCode=1;});
