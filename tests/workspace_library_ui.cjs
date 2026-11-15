/* Default Library scope must keep native inventory out of the guidance browse view. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2],'utf8'),nodes=new Map();
const node=id=>{if(!nodes.has(id))nodes.set(id,{value:'',innerHTML:'',textContent:'',hidden:false,parentElement:{hidden:false}});return nodes.get(id);};
const tabs=[{dataset:{libraryTab:'methods'},attrs:{},classList:{toggle(){}},setAttribute(k,v){this.attrs[k]=v;}},{dataset:{libraryTab:'apps'},attrs:{},classList:{toggle(){}},setAttribute(k,v){this.attrs[k]=v;}}];
const pressed=()=>tabs.find(t=>t.attrs['aria-pressed']==='true')?.dataset.libraryTab;
const library=[
  {key:'playbook',kind:'Workflow',subtype:'Playbook',title:'Plan a campaign',category:'Marketing'},
  {key:'workflow',kind:'Workflow',title:'Research competitors',category:'Research'},
  {key:'recipe',kind:'Recipe',title:'A clear comparison',category:'Content creation'},
  {key:'skill',kind:'Skill',title:'Native skill',category:'Development'},
  {key:'tool',kind:'Tool',title:'Native tool',category:'Apps & capabilities'},
  {key:'plugin',kind:'Plugin',title:'Disabled plugin',category:'Apps & capabilities'}
];
const context=vm.createContext({state:{view:'work',business:'fixture',library,libraryNotes:['A tool catalog could not be read.'],data:{library_preferences:{favorites:['recipe','tool'],recent:['tool','workflow']}}},
  $:node,document:{querySelectorAll:sel=>sel==='[data-library-tab]'?tabs:[]},human:String,esc:String,
  librarySuggestions(show){node('#library-suggested').hidden=!show;},
  methodRow:item=>`<div>${item.key}:${item.kind}</div>`,empty:(title,detail)=>title+' '+detail});
vm.runInContext(source.slice(source.indexOf('const libraryType='),source.indexOf('function appName(')),context);
vm.runInContext(source.slice(source.indexOf('function libraryPrefs('),source.indexOf('let librarySave=')),context);
const declaration=source.indexOf("let fileFilter=");
vm.runInContext(source.slice(declaration,source.indexOf('\n',declaration)),context);
vm.runInContext(source.slice(source.indexOf('function libraryQuery('),source.indexOf('async function refreshLibrary(')),context);
vm.runInContext(source.slice(source.indexOf('function renderWork()'),source.indexOf('function addLocation()')),context);
function filter(type){vm.runInContext(`workFilter=${JSON.stringify(type)};workCategory='';libraryView='all'`,context);node('#work-search').value='';context.renderWork();}
context.renderWork();
assert.equal(pressed(),'methods','A fresh Library must open on playbooks and workflows');
assert.match(node('#work-list').innerHTML,/library-topic-grid/);
for(const category of ['Marketing','Research','Content creation'])assert.ok(node('#work-list').innerHTML.includes('data-workcategory="'+category+'"'));
for(const category of ['Development','Apps & capabilities'])assert.ok(!node('#work-list').innerHTML.includes('data-workcategory="'+category+'"'));
assert.equal(node('#library-topics').hidden,true,'Overview must not repeat topic cards as chips');
assert.equal(node('#work-category-title').textContent,'Browse by topic');assert.equal(node('#library-note').textContent,'');
assert.equal(node('#library-connections').hidden,true);assert.equal(node('#library-suggested').hidden,false);
vm.runInContext("workCategory='Marketing'",context);context.renderWork();
assert.match(node('#work-list').innerHTML,/library-result-group/);assert.match(node('#work-list').innerHTML,/playbook:Workflow/);
assert.equal(node('#library-topics').hidden,false,'Topics remain available within a topic');
assert.equal(node('#library-suggested').hidden,true);
for(let i=0;i<12;i++)library.push({key:'extra'+i,kind:'Workflow',title:'Task '+i,category:'Marketing'});
context.renderWork();
assert.equal((node('#work-list').innerHTML.match(/extra\d+:/g)||[]).length,4,'Large groups show a small preview');
assert.match(node('#work-list').innerHTML,/data-library-expand="Workflow"/);
vm.runInContext("workFilter='Workflow'",context);context.renderWork();
assert.equal((node('#work-list').innerHTML.match(/extra\d+:/g)||[]).length,12,'See all retains the chosen topic and reveals its items');
assert.equal(node('#work-category-title').textContent,'Marketing · Workflows (12)');assert.equal(node('#work-all-topics').hidden,false,'One type shown offers the way back');
library.splice(6);
filter('methods');node('#work-search').value='Native';context.renderWork();assert.match(node('#work-list').innerHTML,/No matching items/,'Search must respect the selected type');
filter('all');assert.equal(node('#work-category-title').textContent,'Browse by topic');assert.match(node('#library-note').textContent,/catalogs/);
assert.ok(node('#work-list').innerHTML.includes('Apps & capabilities'));assert.equal(node('#library-connections').hidden,false);
node('#work-search').value='Native';context.renderWork();assert.match(node('#work-category-title').textContent,/\(2\)$/);
assert.ok(node('#work-list').innerHTML.includes('skill:'));assert.ok(node('#work-list').innerHTML.includes('tool:'));
for(const [kind,key,category] of [['Skill','skill','Development'],['Tool','tool','Apps & capabilities'],['Plugin','plugin','Apps & capabilities']]){
  filter(kind);assert.equal(pressed(),'apps');
  // One topic needs no topic cards: the items show directly.
  if(kind==='Skill')assert.ok(node('#work-list').innerHTML.includes('skill:'));else assert.match(node('#work-list').innerHTML,/library-topic-card|tool:|plugin:/);
  vm.runInContext('workCategory='+JSON.stringify(category),context);context.renderWork();assert.ok(node('#work-list').innerHTML.includes(key+':'));
}
filter('methods');vm.runInContext("libraryView='favorites'",context);context.renderWork();assert.match(node('#work-category-title').textContent,/\(1\)$/);assert.ok(node('#work-list').innerHTML.includes('recipe:'));assert.ok(!node('#work-list').innerHTML.includes('tool:'));
vm.runInContext("libraryView='recent'",context);context.renderWork();assert.match(node('#work-category-title').textContent,/\(1\)$/);assert.ok(node('#work-list').innerHTML.includes('workflow:'));
filter('all');vm.runInContext("libraryView='favorites'",context);context.renderWork();assert.match(node('#work-category-title').textContent,/\(2\)$/,'Capability favorites must remain available when explicitly requested');
filter('methods');vm.runInContext("workCategory='Apps & capabilities'",context);context.renderWork();assert.equal(node('#library-topic').value,'','A hidden capability topic must not leave the default view empty');
console.log('Library UI passed: topic overview, bounded type previews, complete topic lists, deliberate capabilities, and scoped search/favorites/recent.');
