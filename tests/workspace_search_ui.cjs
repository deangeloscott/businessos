/* Search behavior against the real shell functions, without a browser dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2],'utf8'),nodes=new Map();
const node=id=>{if(!nodes.has(id))nodes.set(id,{value:'',innerHTML:'',textContent:'',hidden:false,scrollTop:0,focus(){this.focused=true;},close(){this.open=false;},querySelectorAll(){return [];},showModal(){this.open=true;}});return nodes.get(id);};
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const records=[{title:'Customer guide',type:'Asset',ref:'Asset/guide',data:{topic:'retention'}}];
const context={window:{auraFiles:{detach(){}}},libraryPrefs:()=>({favorites:['file:attachments/guide.md','guide-0']}),fileFavoriteKey:ref=>'file:'+ref,libraryGuidance:item=>['Workflow','Recipe','Skill'].includes(item.kind),state:{business:'studio',data:{workspace:'A',records}},shellSearchData:null,shellSearchTicket:0,$:node,
  goalInfo:value=>value?.extensions?.businessos?.goal||{},closeAnchoredSurface(){},esc,empty:(title,detail)=>esc(title+' '+detail),appName:id=>id,shareType:type=>type,
  usefulFile:file=>!file.path.startsWith('instances/'),chatDescription:chat=>chat.description||''};
vm.createContext(context);
vm.runInContext(source.slice(source.indexOf('function fileFavoriteKey('),source.indexOf('function favoriteControl(')),context);
vm.runInContext(source.slice(source.indexOf("let shellSearchFilter='all'"),source.indexOf('// A deliberately small Markdown renderer')),context);
const chats={items:[{id:'chat',title:'Customer guide',description:'Retention plan',updated:100},{id:'old',title:'Hidden archived chat',archived:true,updated:900}]};
const files={items:[{name:'Customer guide.md',path:'attachments/guide.md',modified:300},{name:'Asset.json',path:'instances/studio/assets/Asset.json'}]};
const library=Array.from({length:78},(_,i)=>({title:'Guide '+String(i).padStart(2,'0'),key:'guide-'+i,kind:'Workflow',description:'retention'}));
library.push({title:'Opaque plugin',key:'plugin',kind:'Plugin'},{title:'Opaque tool',key:'tool',kind:'Tool'});
library.push({title:'<script>guide</script>',key:'unsafe',kind:'Skill'});
context.api=async()=>chats;context.cachedApi=async path=>path.startsWith('/api/files')?files:library;
(async()=>{
  records.push({title:'Hidden deleted goal',type:'Objective',ref:'obj_deleted',data:{extensions:{businessos:{goal:{deleted_at:500}}}}});
  await context.openShellSearch();
  assert(!node('#shell-search-results').innerHTML.includes('Hidden'));
  assert(node('#shell-search-results').innerHTML.indexOf('data-search-file=')<node('#shell-search-results').innerHTML.indexOf('data-chat='),'Empty search uses dates across types');
  assert.match(node('#shell-search-status').textContent,/50 of 82 results/);
  assert.doesNotMatch(node('#shell-search-results').innerHTML,/Asset.json|See all matching|Opaque plugin|Opaque tool/);
  node('#shell-search').value='Customer guide';context.paintShellSearch();
  const mixed=node('#shell-search-results').innerHTML;
  for(const label of ['Chat','File','Memory'])assert(mixed.includes('search-result-type">'+label));
  assert(mixed.indexOf('data-chat=')<mixed.indexOf('data-search-file='),'Exact title precedes a partial title');
  vm.runInContext("shellSearchFilter='files'",context);context.paintShellSearch();
  assert.match(node('#shell-search-status').textContent,/^1 result$/);assert(!node('#shell-search-results').innerHTML.includes('data-chat='));
  assert.equal(node('#shell-search').value,'Customer guide','Filtering preserves the query');
  vm.runInContext("shellSearchFilter='all';shellSearchLimit=100",context);node('#shell-search').value='guide';context.paintShellSearch();
  assert.match(node('#shell-search-results').innerHTML,/&lt;script&gt;guide&lt;\/script&gt;/);assert.equal(node('#shell-search-more').hidden,true);
  vm.runInContext("shellSearchFavorites=true",context);node('#shell-search').value='';context.paintShellSearch();
  assert.match(node('#shell-search-status').textContent,/^2 results$/,'The same favorites collection covers files and guidance');
  assert.match(node('#shell-search-results').innerHTML,/data-search-file=/);assert.match(node('#shell-search-results').innerHTML,/data-search-library="guide-0"/);
  node('#shell-search-results').scrollTop=123;node('#search-dialog').open=true;
  const picked={hasAttribute:a=>a==='data-search-file',getAttribute:a=>a==='data-search-file'?'attachments/guide.md':null};
  context.rememberSearchResult(picked);node('#search-dialog').close();context.backToSearchResults();
  assert.equal(node('#search-dialog').open,true);assert.equal(node('#shell-search-results').scrollTop,123);
  assert.match(node('#shell-search-status').textContent,/^2 results$/,'Back preserves the favorites filter');
  node('#shell-search').value='Customer';context.rememberSearchResult(picked);node('#search-dialog').close();context.backToSearchResults();assert.equal(node('#shell-search').value,'Customer');
  context.cachedApi=async path=>{if(path==='/api/library')throw Error('unavailable');return files;};
  await context.openShellSearch();assert.match(node('#shell-search-status').textContent,/3 results · Couldn’t search Library/);
  assert.match(node('#shell-search-results').innerHTML,/data-chat="chat"/);
  let resolveChats;context.api=()=>new Promise(resolve=>resolveChats=resolve);
  const stale=context.openShellSearch();context.state.business='other';node('#shell-search-results').innerHTML='Other workspace';resolveChats(chats);await stale;
  assert.equal(node('#shell-search-results').innerHTML,'Other workspace');
  // First-open inventory and child navigation use the actual Library renderer.
  const detailNodes=new Map(),detailNode=id=>{if(!detailNodes.has(id))detailNodes.set(id,{open:false,scrollTop:0});return detailNodes.get(id);};
  const child={key:'tool:child',kind:'Tool',title:'Python',description:'Run Python',sources:[{app:'hermes',status:'Reported by app'}]};
  const parent={key:'tool:parent',kind:'Tool',title:'Execution',description:'Execution tools',sources:[{app:'hermes',status:'Enabled in app'}],members:[child]};
  const playbook={key:'workflow:playbook:article',kind:'Workflow',subtype:'Playbook',title:'Article Production',description:'Short summary'};
  const documents={['tool:parent']:{item:parent,text:'',location:''},['tool:child']:{item:child,text:'',location:''},[playbook.key]:{item:playbook,text:'# Article Production\n\nShort summary\n\nExample request: Write an article.',location:'/product/operating_knowledge.py'}};
  const detailContext={state:{business:'studio',data:{workspace:'A'},library:[parent,playbook]},$:detailNode,esc,appName:id=>id,encodeURIComponent,
    favoriteControl:()=>'<button data-library-favorite></button>',setDetailTitleActions(html){detailContext.titleActions=html;},libraryGuidance:item=>['Workflow','Recipe','Skill'].includes(item.kind),rememberLibraryOpen(){},libraryMarked:()=>false,composerConnection:()=>({kind:'hermes'}),chatMarkdown:text=>text,
    api:async path=>documents[new URL('http://local'+path).searchParams.get('key')],
    details(title,html){detailContext.state.fileDetailTicket=(detailContext.state.fileDetailTicket||0)+1;detailNode('#detail').open=true;detailContext.title=title;detailContext.html=html;},
    setDetailBack(label,run){detailContext.back=run;detailContext.backLabel=label;}};
  vm.createContext(detailContext);vm.runInContext(source.slice(source.indexOf('async function openLibrary('),source.indexOf('function quickMethods()')),detailContext);
  await detailContext.openLibrary(parent.key);assert.match(detailContext.html,/Included items/);assert(!detailContext.html.includes('Your AI app chooses'));
  assert.match(detailContext.titleActions,/data-library-favorite/,'Inventory favorites belong beside the title');assert.doesNotMatch(detailContext.html,/Favorited|Favorite/);
  detailNode('#detail-content').scrollTop=85;await detailContext.openLibrary(child.key);assert.equal(detailContext.backLabel,'Execution');await detailContext.back();assert.equal(detailContext.title,'Execution');assert.equal(detailNode('#detail-content').scrollTop,85);
  detailNode('#detail').open=false;await detailContext.openLibrary(playbook.key);assert.match(detailContext.html,/item-location/);assert.match(detailContext.html,/Playbook/);assert.equal((detailContext.html.match(/Short summary/g)||[]).length,1);assert(!detailContext.html.includes('# Article Production'));
  // Registering a previously unregistered file during archive must keep its favorite.
  const archivedAsset={ref:'ast_guide',type:'Asset',title:'Customer guide',data:{location_reference:'attachments/guide.md'}};
  context.state.data.records=[archivedAsset];
  let prefs={favorites:['file:attachments/guide.md']};context.libraryPrefs=()=>prefs;
  context.saveLibrary=async value=>{prefs=value;};context.renderQuickFiles=()=>{};
  vm.runInContext(source.match(/^async function toggleFileFavorite\(.*$/m)[0],context);
  const assetFile={name:'Customer guide.md',path:'asset/ast_guide/guide.md',asset_id:'ast_guide'};
  assert(context.fileMarked(assetFile.path),'The same physical file keeps its favorite after registration');
  const once=context.indexShellSearch({files:[assetFile],records:[archivedAsset],chats:[],library:[]});
  assert.equal(once.length,1,'A registered file must not also appear as a memory result');
  assert(once[0].favoriteKeys.includes('file:attachments/guide.md'));
  await context.toggleFileFavorite(assetFile.path);assert(!context.fileMarked(assetFile.path),'Unfavorite removes the earlier path alias too');
  await context.toggleFileFavorite(assetFile.path);assert(context.fileMarked('attachments/guide.md'),'Both entry paths use the same favorite');
  console.log('Workspace search passed: one labeled list, ranking, filters, all-result pagination, escaping, shared favorites, search return, partial availability, and stale-workspace isolation.');
})().catch(error=>{console.error(error);process.exitCode=1;});
