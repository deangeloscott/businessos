/* The list beside the world: goals in their saved numbers, every way in, and nothing that is not in the feed.
   Relationships are read through workspace-links.js, loaded first, exactly as the page loads them. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const records=[
  {ref:'biz',type:'Business',title:'Bakery',data:{id:'biz',created_at:'2026-03-02T00:00:00Z'}},
  {ref:'g1',type:'Objective',title:'Reach 100 reviews',data:{id:'G1',metric_refs:['m1'],extensions:{businessos:{goal:{scope:'workspace'}}}},measure:{metric:'Google reviews',unit:'reviews',direction:'higher_better',target:100,latest:87,reached:false}},
  {ref:'f1',type:'Insight',title:'S',data:{id:'F1'}}];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const context={state:{business:'bakery',projects:[],data:{records,aura_preferences:{}}},esc,$:()=>null,document:{addEventListener(){},body:{}},setTimeout,clearTimeout,setInterval:()=>0,ResizeObserver:class{observe(){}},
  window:{auraHQ:{pinned:()=>null}}};
context.window.window=context.window;vm.createContext(context);
const aura=process.argv[2];
vm.runInContext(fs.readFileSync(path.join(path.dirname(aura),'workspace-links.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(aura,'utf8')+';this.view=window.auraView;this.links=window.auraLinks;',context);
const v=context.view,L=context.links;

/* Goals in words, from saved numbers only. */
const G1={id:'G1',name:'Reach 100 reviews',metric:'Google reviews',unit:'reviews',direction:'higher_better',target:100,latest:87,reached:false,points:[{at:'a',value:64},{at:'b',value:87}]};
const G2={id:'G2',name:'Top 3',unit:'place',direction:'lower_better',target:3,latest:4,reached:false},G3={id:'G3',name:'Be loved locally'},G4={id:'G4',name:'Grants',unit:'USD',direction:'higher_better',target:20000,latest:5000};
assert.equal(v.goalLine(G1),'87 of 100 reviews','the unit is said once');
assert.equal(v.goalLine(G2),'4 · target 3 place or lower');
assert.equal(v.goalLine(G3),'No number yet');assert.equal(v.goalLine(G4),'$5,000 of $20,000');
assert.equal(v.goalLine({...G1,latest:null}),'No measurement yet');assert.equal(v.goalLine({...G1,reached:true}),'Reached');
assert.equal(v.goalDone(G1),.87);assert.equal(v.goalDone(G2),.75);assert.equal(v.goalDone(G3),0);assert.equal(v.goalDone({...G2,reached:true}),1);

/* A small bakery: one collection, a goal it feeds, a finding with evidence, a decision, a task and a chat that used a file. */
const feed={business:{id:'bakery',name:'Bakery',since:'2026-09-01T00:00:00Z'},as_of:'2026-10-20T00:00:00Z',
  lands:[{id:'col_1',name:'Local competitors',kind:'collection',quiet:true,task_linked:true,project_refs:['prj_1'],items:[{id:'a',title:'Crumb & Co',first_seen:'2026-09-11T00:00:00Z',fields:{rank:1}}],more:0}],
  findings:[{id:'F1',land:'col_1',label:'supported',statement:'S',at:'2026-10-01T00:00:00Z'},{id:'F0',land:'col_1',label:'replaced',statement:'Old',at:'2026-09-20T00:00:00Z'}],
  changes:[{at:'2026-10-10T00:00:00Z',land:'col_1',item_id:'a',title:'Crumb & Co',reason:'Price changed'}],
  goals:[{...G1,lands:['col_1'],points:[{at:'2026-09-15T00:00:00Z',value:64},{at:'2026-10-15T00:00:00Z',value:87}]},G3],
  decisions:[{id:'D1',title:'Hold the price',at:'2026-10-05T00:00:00Z',basis:['F1']}],deadlines:[],uncharted:[{id:'funding-impact',name:'Funding'}],
  tasks:[{id:'tk1',name:'Weekly check',land:'col_1',goal:'G1',schedule:'Every week',health:'failed',status:'Last run failed yesterday.',next_run:'2026-10-25T00:00:00Z'}],
  attention:[{id:'att1',title:'Confirm revenue',reason:'Needed for the grant form'}],suggestions:[{title:'Update Google reviews',why:'Last recorded 20 days ago.',prompt:'Bring "Google reviews" up to date'}],totals:{},
  apps:[{name:'Codex',requests:4,lands:['col_1']}],
  effort:[{kind:'land',id:'col_1',requests:3,tokens:1800,cost_usd:.02,missing_costs:1,missing_tokens:0,chats:[{id:'c1',title:'Research chat',agent:'Codex',model:'m-1',requests:3,tokens:1800,cost_usd:.02,missing_costs:1,missing_tokens:0}]},
          {kind:'other',id:'',requests:2,tokens:0,cost_usd:0,missing_costs:2,missing_tokens:2,chats:[{id:'',title:'Unlinked request',agent:'Pi',model:'Model unreported',requests:2,tokens:0,cost_usd:0,missing_costs:2,missing_tokens:2}]}],
  relationships:{nodes:[
    {key:'land:col_1',kind:'land',name:'Local competitors',lands:['col_1']},{key:'goal:G1',kind:'goal',name:'Reach 100 reviews',lands:['col_1']},{key:'goal:G3',kind:'goal',name:'Be loved locally'},
    {key:'finding:F1',kind:'finding',name:'S',action:{record:'F1'},lands:['col_1']},{key:'decision:D1',kind:'decision',name:'Hold the price'},
    {key:'record:ev1',kind:'record',name:'The menu says $8',action:{record:'ev1'}},{key:'task:tk1',kind:'task',name:'Weekly check',lands:['col_1']},
    {key:'chat:c1',kind:'chat',name:'Research chat',action:{chat:'c1'}},{key:'app:Codex',kind:'app',name:'Codex'},
    {key:'file:brief.md',kind:'file',name:'Brief',action:{file:'brief.md'}},{key:'project:prj_1',kind:'project',name:'Local visibility',action:{'open-project':'prj_1'}},
    {key:'chat:c2',kind:'chat',name:'Unrelated chat'},{key:'file:other.md',kind:'file',name:'Other'}],
  edges:[
    {source:'land:col_1',target:'goal:G1',type:'feeds'},{source:'finding:F1',target:'land:col_1',type:'in'},{source:'record:ev1',target:'finding:F1',type:'supports'},
    {source:'finding:F1',target:'decision:D1',type:'basis'},{source:'task:tk1',target:'land:col_1',type:'assigned'},{source:'task:tk1',target:'goal:G1',type:'assigned'},
    {source:'app:Codex',target:'chat:c1',type:'used'},{source:'file:brief.md',target:'chat:c1',type:'attached'},{source:'chat:c1',target:'finding:F1',type:'saved'},{source:'chat:c1',target:'land:col_1',type:'into'},
    {source:'project:prj_1',target:'land:col_1',type:'member'},{source:'project:prj_1',target:'goal:G1',type:'member'},{source:'project:prj_1',target:'file:other.md',type:'member'},
    {source:'app:Codex',target:'chat:c2',type:'used'}]}};
const projects=[{id:'prj_1',name:'Local visibility',members:[{kind:'goal',id:'G1'},{kind:'collection',id:'col_1'}]}];context.state.projects=projects;

/* The chain: everything that flowed into a thing and everything it flowed into, never sideways through a shared hub. */
const fileChain=L.trace(feed,'file:brief.md');
assert.ok(['chat:c1','finding:F1','land:col_1','goal:G1','decision:D1'].every(k=>fileChain.down.has(k)),'a file follows through the chat it was given to, to what it saved and the goal that serves');
assert.ok(!fileChain.all.has('chat:c2'),'another conversation in the same app is not part of this chain');
const goalChain=L.trace(feed,'goal:G1');
assert.ok(['land:col_1','task:tk1','project:prj_1'].every(k=>goalChain.up.has(k)),'a goal is fed by its collection, the task keeping it current and the project holding it');
assert.ok(!goalChain.up.has('finding:F1'),'an area is not fed by everything kept in it');
assert.ok(!goalChain.all.has('file:other.md'),'a project’s other members are not part of the goal’s chain');
assert.ok(L.trace(feed,'project:prj_1').down.has('file:other.md'),'selecting the project itself shows what it holds');
assert.equal(L.places(feed,'file:brief.md').join(),'col_1','a file lights the places its chain reaches');
assert.equal(v.landsFor(feed,'goal:G3').length,0,'a filter shows only what recorded links tie to it');
assert.equal(v.landsFor(feed,'app:Codex').join(),'col_1');
const sides=L.sides(feed,'finding:F1');
assert.ok(sides.direct[0].some(x=>x.node.key==='chat:c1'&&x.how==='Where this was saved'),'a direct link says how, from the selected thing’s side');
assert.ok(sides.direct[0].some(x=>x.node.key==='record:ev1'&&x.how==='Supports this'));
assert.ok(sides.direct[1].some(x=>x.node.key==='decision:D1'&&x.how==='Rests on this'));
assert.ok(sides.further[0].some(n=>n.key==='file:brief.md'),'what came before the direct links is listed as further along');
assert.equal(L.sentence({name:'Research chat'},{type:'saved'},{name:'S'}),'Research chat saved S');
const overview=L.overview(feed);
assert.ok(overview.edges.some(e=>e.source==='app:Codex'&&e.target==='chats:all')&&overview.edges.some(e=>e.source==='chats:all'&&e.target==='land:col_1'),'with nothing selected, apps flow into the conversations and they flow to where their work went');
assert.equal(overview.node('chats:all').name,'1 conversation','conversations are one step in the flow, counted, not drawn one by one');
assert.ok(!overview.edges.some(e=>e.source==='chat:c2'||e.target==='chat:c2'),'a conversation whose work went nowhere recorded is not drawn');
/* Saved work within a period, and by kind. */
const dated={...feed,relationships:{...feed.relationships,edges:feed.relationships.edges.map(e=>e.type==='saved'?{...e,at:'2026-10-01T00:00:00Z'}:e)}};
assert.equal(L.measures(dated,{from:Date.parse('2026-10-15'),to:Date.parse('2026-10-20')}).carried('chat:c1','saved'),0,'saved work outside the period is not counted');
assert.equal(L.measures(dated,{from:Date.parse('2026-09-15'),to:Date.parse('2026-10-20')}).carried('chat:c1','saved'),1);
assert.deepEqual({...L.measures(dated).kinds('chat:c1')},{finding:1},'saved work is named by kind');
assert.ok(v.takeaways(feed,'timeline').includes('class="world-takeaways"'),'each view opens with plain takeaways');
/* A connected service a conversation called is one of what fed that work, and of the places it reached. */
const called={...feed,relationships:{nodes:[...feed.relationships.nodes,{key:'service:stripe',kind:'service',name:'Stripe'},{key:'service:gmail',kind:'service',name:'Gmail'}],
  edges:[...feed.relationships.edges,{source:'service:stripe',target:'chat:c1',type:'called',calls:5},{source:'service:gmail',target:'chat:c1',type:'called',calls:2},{source:'service:gmail',target:'chat:c2',type:'called',calls:9}]}};
assert.equal(L.services(called,'land:col_1').map(s=>s.name+':'+s.calls).join(),'Stripe:5,Gmail:2','a place relies on the services its own work called, busiest first, not on other conversations’ calls');
assert.ok(L.sides(called,'chat:c1').direct[0].some(x=>x.node.key==='service:stripe'&&x.how==='Connected service it called'));
assert.ok(L.overview(called).edges.some(e=>e.source==='service:stripe'&&e.target==='chats:all'),'services flow into the conversations, beside the apps');

/* The panel. */
const home=v.home(feed);
assert.ok(home.includes('data-world-go="goal:G1"')&&home.includes('87 of 100 reviews'),'a goal with a number flies to its ring');
assert.ok(home.includes('data-world-go="goal:G3"'),'a goal without a ring can still be explored');
assert.ok(home.includes('data-prompt="Bring &quot;Google reviews&quot; up to date"'),'a next step starts an ordinary chat with its saved prompt');
assert.ok(home.includes('data-world-go="land:col_1"')&&home.includes('Gone quiet')&&home.includes('1 tracked · 1 finding'),'replaced findings are not counted');
assert.ok(home.includes('data-world-go="land:new:funding-impact"')&&home.includes('Uncharted'));
assert.ok(home.includes('Confirm revenue')&&!home.includes('data-record="att1"'),'an attention item with no record here is shown without a dead link');
assert.ok(home.includes('In the last two weeks')&&home.includes('64 → 87 reviews')&&!home.includes('Changed lately'),'what changed is said once, goal numbers first');
const since=v.whatChanged(feed,'2026-10-12T00:00:00Z');
assert.ok(since.includes('Since your last visit')&&since.includes('64 → 87 reviews')&&!since.includes('Price changed')&&since.includes('data-world-since="2026-10-12"'),'only what came after the last visit, with one way to see it over time');
assert.ok(v.whatChanged(feed,'2026-10-19T00:00:00Z').includes('No new findings, tracked changes or goal movement since'));
const empty=v.home({...feed,lands:[],findings:[],changes:[],goals:[],uncharted:[],attention:[],suggestions:[]});
assert.ok(empty.includes('it becomes a ring around your world')&&empty.includes('What your AI saves appears here')&&!empty.includes('Needs you')&&!empty.includes('In the last two weeks'),'an empty world says how to begin and pads nothing');
const land={...v.recordFor(feed,'land','col_1'),hue:120};
const thing=land.things[0];thing.need=true;thing.changes=3;
const opened=v.selected(feed,thing);
assert.ok(opened.includes('data-collection="col_1"')&&opened.includes('Due for review')&&opened.includes('<dt>rank</dt><dd>1</dd>')&&opened.includes('Changes noticed'));
const place=v.selected(feed,land);
assert.ok(place.includes('gone quiet')&&place.includes('A scheduled task')&&place.includes('data-world-go="item:col_1|a"')&&place.includes('data-collection="col_1"'));
assert.ok(v.selected(feed,{kindOf:'land',unch:true,name:'Funding'}).includes('data-prompt="Start looking into funding for us.'),'an uncharted area offers one way to start');
const finding=v.selected(feed,{kind:'finding',label:'challenged',need:true,land,tied:[],raw:{id:'F1',statement:'S',challenges:1,at:'2026-10-01T00:00:00Z',evidence:[{relationship:'supports',statement:'The page says 2pm.'},{relationship:'contradicts',statement:'The listing says 3pm.'}]}});
assert.ok(finding.includes('data-record="f1"')&&finding.includes('Challenged by new evidence')&&finding.includes('Both sides')&&finding.includes('Settle it'),'a challenged finding shows both sides and one way to settle it');
const goal=v.selected(feed,v.recordFor(feed,'goal','G1'));
assert.ok(goal.includes('data-record="g1"')&&goal.includes('width:87%')&&goal.includes('Plan the next step')&&goal.includes('<dt>Fed by</dt><dd>Local competitors</dd>'));
assert.ok(v.selected(feed,{kind:'goal',raw:G1}).includes('Nothing is linked to this goal yet'));
const task=v.selected(feed,v.recordFor(feed,'task','tk1'));
assert.ok(task.includes('world-callout')&&task.includes('Last run failed yesterday.')&&task.includes('<dt>Works toward</dt><dd>Reach 100 reviews</dd>')&&task.includes('Open schedules'));
assert.ok(v.selected(feed,{kindOf:'land',kind:'group',name:'3 more collections',members:[{id:'col_9',name:'Suppliers',current:4}]}).includes('data-collection="col_9"'));
const trend=v.selected(feed,{...thing,raw:{...thing.raw,trend:{field:'rank',points:[{value:3},{value:2},{value:1}]}}});
assert.ok(trend.includes('world-spark')&&trend.includes('rank: 3 → 1 over 3 checks'));
const lesson=v.selected(feed,{kind:'decision',raw:{id:'L1',kind:'lesson',title:'Posts at 7am do better',at:'2026-10-01T00:00:00Z'},basis:[]});
assert.ok(lesson.includes('>Lesson<')&&lesson.includes('Open the lesson')&&lesson.includes('<dt>Learned</dt>'));
const file=v.recordFor(feed,'file','brief.md');
assert.ok(file.relationship&&v.selected(feed,file).includes('data-file="brief.md"')&&v.selected(feed,file).includes('Conversation this was given to'),'anything the links know about opens with its own action and its chain');
assert.equal(v.relatedFeed(feed,file).lands.length,1,'a file narrows the world to the places its chain reaches');
assert.equal(v.relatedFeed(feed,v.recordFor(feed,'goal','G3')).lands.length,0);
const conn=v.connections(feed,v.recordFor(feed,'finding','F1'));
assert.ok(conn.includes('What fed this')&&conn.includes('What it led to')&&conn.includes('Further along: 1 AI app, 1 file'),'the panel says what fed it, what it led to and how much lies further along');
assert.ok(v.connections(feed,null).includes('How your work flows'),'with nothing selected the panel starts from the busiest parts of the flow');
assert.ok(v.connections(feed,v.recordFor(feed,'goal','G3')).includes('Find evidence for this goal'),'a goal with nothing feeding it offers one way to start');
assert.ok(v.connections(feed,land).includes('Also keeps 1 finding and 1 tracked results'),'what an area keeps is a count, not a line each');
const gapFeed={...feed,findings:[{id:'F9',land:'col_1',label:'unverified',statement:'U'}]},quiet={...feed.goals[0],points:[{at:'2026-09-01T00:00:00Z',value:64}]};
assert.equal(v.goalGaps(gapFeed,quiet).map(g=>g[0]).join(' | '),'Not measured for 49 days | Local competitors has gone quiet | 1 finding in Local competitors needs checking | Weekly check is not running','what stands between a goal and its number comes only from saved facts');
assert.equal(v.goalGaps(gapFeed,{...quiet,reached:true}).length,0);assert.equal(v.goalGaps(gapFeed,G3).length,0,'a goal with no number has no gaps to claim');
const tools=v.tools({...feed,lands:[feed.lands[0],{...feed.lands[0],id:'col_2',name:'Grants'}]});
assert.ok(tools.keys.includes('data-world-chip="col_2"')&&tools.top.includes('id="world-q"')&&!tools.top.includes('<select'),'the key along the bottom, find at the top; selecting something shows what belongs to it');
const many=v.tools({...feed,lands:Array.from({length:12},(_,i)=>({...feed.lands[0],id:'col_'+i,name:'Area '+i,items:Array(i).fill(feed.lands[0].items[0])}))});
assert.ok(many.keys.includes('+6 more')&&many.keys.includes('data-world-chip="col_11"')&&!many.keys.includes('data-world-chip="col_0"'),'many areas show the busiest few and fold the rest into one chip');
assert.equal(v.tools(feed).keys,'','area chips appear once there is more than one area');

/* Time. */
const time=v.timelineView(feed);
assert.ok(time.includes('class="tl-mark item"')&&time.includes('data-world-go="item:col_1|a"')&&time.includes('data-world-go="finding:F1"')&&!time.includes('finding:F0'),'replaced findings are left off the timeline');
assert.ok(time.includes('Reach 100 reviews: 87')&&time.includes('Decided: Hold the price')&&time.includes('Next run: Weekly check')&&time.includes('class="tl-today"'),'goals, decisions, what is coming and today are on one timeline');
assert.ok(time.indexOf('>Goals<')<time.indexOf('>Scheduled tasks<')&&time.indexOf('>Scheduled tasks<')<time.indexOf('>Places<'),'rows are grouped: goals, work, scheduled tasks, places');
assert.ok(v.timelineView({...feed,lands:[],findings:[],changes:[],goals:[],decisions:[],tasks:[]}).includes('Nothing has been saved yet'));
const split=v.timelineView({...feed,work:[{start:'2026-10-05T00:00:00Z',requests:3,tokens:0}],work_by:[{kind:'land',id:'col_1',weeks:[3]}]});
assert.ok(split.includes('>Work<')&&split.includes('tl-bar')&&!split.includes('>AI requests<'),'work is drawn per project or collection when AURA can tell which it was for');
const comparison={...feed,lands:[{...feed.lands[0],items:[{id:'a',title:'Crumb & Co',first_seen:'2026-09-01T00:00:00Z',history:[{at:'2026-10-01T00:00:00Z',values:{price:49}},{at:'2026-10-15T00:00:00Z',values:{price:59}}]}]}]};
assert.ok(v.changesSince(comparison,'2026-10-10').some(c=>c.detail==='price: 49 → 59'),'comparison uses saved measurements');
assert.ok(!v.changesSince(comparison,'2026-09-01').some(c=>c.detail.includes('price:')),'no invented baseline when no earlier measurement exists');
assert.equal(v.changesSince(comparison,'2027-01-01').length,0);
assert.ok(v.changesSince({...feed,findings:[{id:'new',land:'col_1',statement:'New evidence',at:'2026-10-20T00:00:00Z',label:'supported'}]},'2026-10-19').some(c=>c.title==='New evidence'),'a new finding prevents a false nothing-changed');
const proof=v.evidenceRows({source_details:[{record:'evidence/path',relationship:'contradicts',statement:'A <different> price',sources:[{record:'source/path',title:'Original source'}]}]});
assert.ok(proof.includes('Challenges this finding')&&proof.includes('data-record="source/path"')&&proof.includes('&lt;different&gt;'),'readable trace opens saved source records and escapes source text');

/* AI effort: one chart, grouped one way at a time, only what apps reported. */
const effort=v.effortView(feed,null);
assert.ok(effort.includes('5 requests ')&&effort.includes('cost not reported for 3')&&effort.includes('class="we-block"')&&effort.includes('Codex')&&effort.includes('Pi'),'by AI app by default, a missing cost is said, not estimated');
assert.ok(effort.includes('id="world-effort-by"')&&effort.includes('data-effort-metric="saved"')&&effort.includes('Select a block'),'one grouping at a time, with the conversations behind a block on request');
const lastMonth={...feed,effort_last:[{kind:'land',id:'col_1',chats:[{id:'c1',title:'Research chat',agent:'Codex',model:'m-1',requests:1,tokens:100,cost_usd:.01,missing_costs:0,missing_tokens:0}]}]};
assert.ok(v.effortView(lastMonth,null).includes('before: 1 request'),'the period is compared with the one before it');
assert.ok(v.effortSide(lastMonth,null).includes('class="we-bar"')&&v.effortSide(lastMonth,null).includes('on the period before'),'beside the chart, ranked bars say how each changed');
assert.ok(v.effortView(feed,v.recordFor(feed,'goal','G1')).includes('3 requests '),'a selection counts only the conversations in its chain');
assert.ok(v.effortView(feed,v.recordFor(feed,'goal','G3')).includes('No AI use')&&v.effortView(feed,v.recordFor(feed,'goal','G3')).includes('is recorded for anything in this chain'));
assert.ok(v.effortView({...feed,effort:[]},null).includes('No AI requests have been recorded'));

/* A receipt: what a piece of work saved since the world was last read, in its own words. */
const before={...feed,as_of:'2026-10-09T00:00:00Z',relationships:{...feed.relationships,edges:feed.relationships.edges.filter(e=>e.type!=='saved')}};
const after={...feed,changes:[{...feed.changes[0],by:{kind:'chat',id:'c1'}}]};
const [receipt]=v.receipts(before,after);
assert.equal(receipt.text,'Codex saved 1 finding and changed 1 tracked result · “Research chat”.');
assert.equal([...receipt.items].sort().join(),'finding:F1,item:col_1|a');
assert.equal(v.receipts(feed,feed).length,0,'nothing new, nothing to report');

/* The year poster is made from the same records, with outcomes not activity. */
const poster=v.posterData(feed);
assert.equal(poster.year,2026);assert.equal(poster.stats.map(s=>s.join(': ')).join(' | '),'Tracked this year: 1 | Findings this year: 1 | Changes noticed: 1 | Goals reached: 0 of 1');
console.log('aura ui: ok');
