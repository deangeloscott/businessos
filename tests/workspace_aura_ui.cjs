/* The list beside the world: goals in their saved numbers, every way in, and nothing that is not in the feed. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const records=[
  {ref:'biz',type:'Business',title:'Bakery',data:{id:'biz',created_at:'2026-03-02T00:00:00Z'}},
  {ref:'g1',type:'Objective',title:'Reach 100 reviews',data:{id:'G1',metric_refs:['m1'],extensions:{businessos:{goal:{scope:'workspace'}}}},measure:{metric:'Google reviews',unit:'reviews',direction:'higher_better',target:100,latest:87,reached:false}},
  {ref:'f1',type:'Insight',title:'S',data:{id:'F1'}}];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const context={state:{business:'bakery',projects:[],data:{records,aura_preferences:{}}},esc,$:()=>null,document:{addEventListener(){},body:{}},setTimeout,clearTimeout,setInterval:()=>0,ResizeObserver:class{observe(){}},
  window:{auraHQ:{pinned:()=>null}}};
context.window.window=context.window;vm.createContext(context);
vm.runInContext(fs.readFileSync(process.argv[2],'utf8')+';this.view=window.auraView;',context);
const v=context.view;
const G1={id:'G1',name:'Reach 100 reviews',metric:'Google reviews',unit:'reviews',direction:'higher_better',target:100,latest:87,reached:false,points:[{at:'a',value:64},{at:'b',value:87}]};
const G2={id:'G2',name:'Top 3',unit:'place',direction:'lower_better',target:3,latest:4,reached:false},G3={id:'G3',name:'Be loved locally'},G4={id:'G4',name:'Grants',unit:'USD',direction:'higher_better',target:20000,latest:5000};
assert.equal(v.goalLine(G1),'87 of 100 reviews','the unit is said once');
assert.equal(v.goalLine(G2),'4 · target 3 place or lower');
assert.equal(v.goalLine(G3),'No number yet');assert.equal(v.goalLine(G4),'$5,000 of $20,000');
assert.equal(v.goalLine({...G1,latest:null}),'No measurement yet');assert.equal(v.goalLine({...G1,reached:true}),'Reached');
assert.equal(v.goalDone(G1),.87);assert.equal(v.goalDone(G2),.75);assert.equal(v.goalDone(G3),0);assert.equal(v.goalDone({...G2,reached:true}),1);
const feed={business:{id:'bakery',name:'Bakery'},
  lands:[{id:'col_1',name:'Local competitors',kind:'collection',items:[{id:'a',title:'Crumb & Co',fields:{rank:1}}],more:0,quiet:true}],
  findings:[{id:'F1',land:'col_1',label:'supported',statement:'S'},{id:'F0',land:'col_1',label:'replaced',statement:'Old'}],
  changes:[{at:'2026-10-10T00:00:00Z',land:'col_1',item_id:'a',title:'Crumb & Co'}],goals:[G1,G3],decisions:[],uncharted:[{id:'funding-impact',name:'Funding'}],
  attention:[{id:'att1',title:'Confirm revenue',reason:'Needed for the grant form'}],suggestions:[{title:'Update Google reviews',why:'Last recorded 20 days ago.',prompt:'Bring "Google reviews" up to date'}],totals:{}};
const home=v.home(feed);
assert.ok(home.includes('data-world-go="goal:G1"')&&home.includes('87 of 100 reviews'),'a goal with a number flies to its ring');
assert.ok(home.includes('data-world-go="goal:G3"'),'a goal without a ring can still be explored');
assert.ok(home.includes('data-prompt="Bring &quot;Google reviews&quot; up to date"'),'a next step starts an ordinary chat with its saved prompt');
assert.ok(home.includes('data-world-go="item:col_1|a"')&&home.includes('data-world-go="land:col_1"')&&home.includes('Gone quiet'));
assert.ok(home.includes('1 tracked · 1 finding'),'replaced findings are not counted');
assert.ok(home.includes('data-world-go="land:new:funding-impact"')&&home.includes('Uncharted'));
assert.ok(home.includes('Confirm revenue')&&!home.includes('data-record="att1"'),'an attention item with no record here is shown without a dead link');
const empty=v.home({...feed,lands:[],findings:[],changes:[],goals:[],uncharted:[],attention:[],suggestions:[]});
assert.ok(empty.includes('it becomes a ring around your world')&&empty.includes('What your AI saves appears here')&&!empty.includes('Needs you')&&!empty.includes('Changed lately'),'an empty world says how to begin and pads nothing');
const land={kindOf:'land',kind:'collection',id:'col_1',name:'Local competitors',hue:120,quiet:true,task_linked:true,last_checked:'2026-10-10T00:00:00Z',more:0,things:[],finds:[]};
const thing={kind:'item',id:'col_1|a',name:'Crumb & Co',land,raw:{fields:{rank:1},sources:2,first_seen:'2026-09-01T00:00:00Z'},need:true,changes:3,seen:1};land.things=[thing];
const opened=v.selected(feed,thing);
assert.ok(opened.includes('data-collection="col_1"')&&opened.includes('Due for review')&&opened.includes('<dt>rank</dt><dd>1</dd>')&&opened.includes('Changes noticed'));
const place=v.selected(feed,land);
assert.ok(place.includes('gone quiet')&&place.includes('A scheduled task')&&place.includes('data-world-go="item:col_1|a"')&&place.includes('data-collection="col_1"'));
const unch=v.selected(feed,{kindOf:'land',unch:true,name:'Funding'});
assert.ok(unch.includes('Start charting Funding')&&unch.includes('data-prompt="Start looking into funding for us.'),'an uncharted area offers one way to start');
const finding=v.selected(feed,{kind:'finding',label:'challenged',need:true,land,raw:{id:'F1',statement:'S',challenges:1,at:'2026-10-01T00:00:00Z'}});
assert.ok(finding.includes('data-record="f1"')&&finding.includes('Challenged by new evidence'),'a finding opens its own record');
const goal=v.selected(feed,{kind:'goal',raw:G1});
assert.ok(goal.includes('data-record="g1"')&&goal.includes('width:87%')&&goal.includes('Plan the next step'));
/* The other views draw the same feed: saved links only, things at the time they were saved, and usage exactly as reported. */
const linked={...feed,as_of:'2026-10-20T00:00:00Z',business:{...feed.business,since:'2026-09-01T00:00:00Z'},
  lands:[{...feed.lands[0],task_linked:true,project_refs:['prj_1'],items:[{id:'a',title:'Crumb & Co',first_seen:'2026-09-11T00:00:00Z',fields:{rank:1}}]}],
  findings:[{id:'F1',land:'col_1',label:'supported',statement:'S',at:'2026-10-01T00:00:00Z'},{id:'F0',land:'col_1',label:'replaced',statement:'Old',at:'2026-09-20T00:00:00Z'}],
  goals:[{...G1,lands:['col_1'],points:[{at:'2026-09-15T00:00:00Z',value:64},{at:'2026-10-15T00:00:00Z',value:87}]},G3],decisions:[{id:'D1',title:'Hold the price',at:'2026-10-05T00:00:00Z'}],deadlines:[],
  tasks:[{id:'tk1',name:'Weekly check',land:'col_1',goal:'G1',schedule:'Every week',health:'failed',status:'Last run failed yesterday.',next_run:'2026-10-25T00:00:00Z'}]};
const projects=[{id:'prj_1',name:'Local visibility',members:[{kind:'goal',id:'G1'},{kind:'collection',id:'col_1'}]}];
const links=v.mapLinks(linked,projects).map(l=>l.join('>'));
assert.equal([...links].sort().join(),'l:col_1>g:G1,p:prj_1>g:G1,p:prj_1>l:col_1,t:tk1>g:G1,t:tk1>l:col_1','each line is a saved link, drawn once');
const map=v.mapView(linked,projects);
assert.ok(map.includes('data-world-go="project:prj_1"')&&map.includes('data-key="t:tk1"')&&map.includes('Weekly check')&&map.includes('data-world-go="goal:G1"')&&!map.includes('Nothing is linked yet'));
assert.ok(v.mapView(feed,[]).includes('Nothing is linked yet'),'with no saved links the map says how they appear');
const time=v.timelineView(linked);
assert.ok(time.includes('class="wt-mark item"')&&time.includes('data-world-go="item:col_1|a"')&&time.includes('data-world-go="finding:F1"')&&!time.includes('finding:F0'),'replaced findings are left off the timeline');
assert.ok(time.includes('Reach 100 reviews: 87')&&time.includes('Decided: Hold the price')&&/class="wt-mark change" style="left:\d/.test(time));
assert.ok(v.timelineView({...linked,lands:[],findings:[],changes:[],goals:[],decisions:[],tasks:[]}).includes('Nothing has been saved yet'));
assert.ok(v.effortRows(null).includes('No AI requests have been recorded this month'));
const effort=v.effortRows({requests:9,totals:{input_tokens:300000,output_tokens:2000,cost_usd:.5},groups:[{name:'Claude Code',requests:7,input_tokens:290000,output_tokens:1500,cost_usd:.5,missing_costs:0},{name:'Pi',requests:2,input_tokens:10000,output_tokens:500,missing_costs:2},{name:'Idle',requests:0}]});
assert.ok(effort.includes('Claude Code')&&effort.includes('292K tokens')&&effort.includes('cost not reported for 2')&&!effort.includes('Idle')&&effort.includes('$0.5'),'usage is shown as each app reported it; a missing cost is said, not estimated');
const poster=v.posterView(linked);
assert.ok(poster.includes('2026 with AURA')&&poster.includes('<dt>Tracked this year</dt><dd>1</dd>')&&poster.includes('<dt>Findings this year</dt><dd>1</dd>')&&poster.includes('<dt>Goals reached</dt><dd>0 of 1</dd>')&&poster.includes('saved records, not activity'));
const fed=v.selected(linked,{kind:'goal',raw:linked.goals[0]});
assert.ok(fed.includes('<dt>Fed by</dt><dd>Local competitors</dd>')&&v.selected(feed,{kind:'goal',raw:G1}).includes('Nothing is linked to this goal yet'));
assert.ok(time.includes('Coming up')&&time.includes('Next run: Weekly check'),'what is scheduled next sits to the right of today');
assert.equal(v.latest(feed,null),'','with no earlier visit there is nothing to compare against');
const since=v.latest(linked,'2026-10-10T00:00:00Z');
assert.ok(since.includes('Since your last visit')&&since.includes('64 → 87 reviews')&&!since.includes('Crumb'),'only what was saved after the last visit is listed, goal numbers first');
assert.ok(v.latest(linked,'2026-10-19T00:00:00Z').includes('No new findings, tracked changes or goal movement since'));
const task=v.selected(linked,{kind:'task',name:'Weekly check',land,raw:linked.tasks[0]});
assert.ok(task.includes('world-callout')&&task.includes('Last run failed yesterday.')&&task.includes('<dt>Works toward</dt><dd>Reach 100 reviews</dd>')&&task.includes('Open schedules'));
const group=v.selected(feed,{kindOf:'land',kind:'group',name:'3 more collections',members:[{id:'col_9',name:'Suppliers',current:4}]});
assert.ok(group.includes('data-collection="col_9"')&&group.includes('4 results'));
const trend=v.selected(feed,{...thing,raw:{...thing.raw,trend:{field:'rank',points:[{value:3},{value:2},{value:1}]}}});
assert.ok(trend.includes('world-spark')&&trend.includes('rank: 3 → 1 over 3 checks'));
const tied=v.effortRows({requests:3,totals:{},groups:[{name:'Pi',requests:3}]},{...feed,effort:[{kind:'land',id:'col_1',requests:3,tokens:1000,cost_usd:0,missing_costs:3}]});
assert.ok(tied.includes('By what the work was for')&&tied.includes('Local competitors')&&tied.includes('cost not reported for 3'));
assert.ok(home.includes('data-world-chip')===false&&v.tools({...feed,lands:[feed.lands[0],{...feed.lands[0],id:'col_2',name:'Grants'}]}).includes('data-world-chip="col_2"'),'area chips appear once there is more than one area');
assert.ok(effort.includes('class="we-block"')&&effort.includes('By AI app')&&tied.includes('class="we-map"'),'AI effort is drawn as blocks sized by share');
const lesson=v.selected(feed,{kind:'decision',raw:{id:'L1',kind:'lesson',title:'Posts at 7am do better',at:'2026-10-01T00:00:00Z'},basis:[]});
assert.ok(lesson.includes('>Lesson<')&&lesson.includes('Open the lesson')&&lesson.includes('<dt>Learned</dt>'));
const sides=v.selected(feed,{kind:'finding',label:'challenged',need:true,land,tied:[],raw:{id:'F1',statement:'S',challenges:1,evidence:[{relationship:'supports',statement:'The page says 2pm.'},{relationship:'contradicts',statement:'The listing says 3pm.'}]}});
assert.ok(sides.includes('Both sides')&&sides.includes('The listing says 3pm.')&&sides.includes('Challenges it')&&sides.includes('Settle it'),'a challenged finding shows both sides and one way to settle it');
const split=v.timelineView({...linked,work:[{start:'2026-10-05T00:00:00Z',requests:3,tokens:0}],work_by:[{kind:'land',id:'col_1',weeks:[3]}]});
assert.ok(split.includes('Work: Local competitors')&&split.includes('wt-bar')&&!split.includes('>AI requests<'),'work is drawn per project or collection when AURA can tell which it was for');
const withApps={...linked,apps:[{name:'Codex',requests:4,lands:['col_1']}]};
assert.equal(v.landsFor(withApps,'goal:G1').join(),'col_1');assert.equal(v.landsFor(withApps,'task:tk1').join(),'col_1');assert.equal(v.landsFor(withApps,'app:Codex').join(),'col_1');
assert.equal(v.landsFor(withApps,'project:prj_1',projects).join(),'col_1');assert.equal(v.landsFor(withApps,'goal:G3').length,0,'a filter shows only what saved links tie to it');
const appsMap=v.mapView(withApps,projects);assert.ok(appsMap.includes('AI apps')&&appsMap.includes('data-key="a:Codex"')&&v.mapLinks(withApps,projects).some(l=>l.join('>')==='a:Codex>l:col_1'),'the Map shows each AI app and the collections its chats were tied to');
const quietGoal={...G1,lands:['col_1'],points:[{at:'2026-09-01T00:00:00Z',value:64}]},gapFeed={...linked,findings:[{id:'F9',land:'col_1',label:'unverified',statement:'U'}],tasks:[{...linked.tasks[0]}]};
const gaps=v.goalGaps(gapFeed,quietGoal).map(g=>g[0]);
assert.equal(gaps.join(' | '),'Not measured for 49 days | Local competitors has gone quiet | 1 finding in Local competitors needs checking | Weekly check is not running','what stands between a goal and its number comes only from saved facts');
assert.equal(v.goalGaps(gapFeed,{...quietGoal,reached:true}).length,0);assert.equal(v.goalGaps(gapFeed,G3).length,0,'a goal with no number has no gaps to claim');
assert.ok(v.selected(gapFeed,{kind:'goal',raw:quietGoal}).includes('What would move this')&&v.tools(withApps).includes('id="world-by"')&&v.tools(feed).includes('id="world-q"'));
console.log('aura ui: ok');

assert.equal(v.relatedFeed(linked,v.recordFor(linked,'goal','G3')).lands.length,0);
assert.ok(v.relatedFeed(linked,v.recordFor(linked,'goal','G1')).findings.some(f=>f.id==='F1'));
assert.equal(v.recordFor(linked,'item','col_1|a').raw.title,'Crumb & Co');

const newerFinding={...linked,findings:[{id:'new',land:'col_1',statement:'New evidence',at:'2026-10-20T00:00:00Z',label:'supported'}]};
assert.ok(v.latest(newerFinding,'2026-10-19T00:00:00Z').includes('New evidence'),'new findings must prevent a false nothing-changed message');
const missingTokens=v.effortRows({requests:101,groups:[{name:'Reports tokens',requests:1,input_tokens:10000},{name:'No token report',requests:100}]});
assert.ok(missingTokens.includes('width:99.01%'),'request-sized blocks compare requests even when token reporting differs');
assert.equal(v.recordFor(linked,'finding','F1').raw.statement,'S','the non-3D reader can select a finding');

const comparison={...linked,lands:[{...linked.lands[0],items:[{id:'a',title:'Crumb & Co',first_seen:'2026-09-01T00:00:00Z',history:[{at:'2026-10-01T00:00:00Z',values:{price:49}},{at:'2026-10-15T00:00:00Z',values:{price:59}}]}]}]};
const changed=v.changesSince(comparison,'2026-10-10');
assert.ok(changed.some(c=>c.detail==='price: 49 → 59'),'comparison uses saved measurements');
assert.ok(!v.changesSince(comparison,'2026-09-01').some(c=>c.detail.includes('price:')),'no invented baseline when no earlier measurement exists');
assert.equal(v.changesSince(comparison,'2027-01-01').length,0);
const proof=v.evidenceRows({source_details:[{record:'evidence/path',relationship:'contradicts',statement:'A <different> price',sources:[{record:'source/path',title:'Original source'}]}]});
assert.ok(proof.includes('Challenges this finding')&&proof.includes('data-record="source/path"')&&proof.includes('&lt;different&gt;'),'readable trace opens saved source records and escapes source text');

const relationshipFeed={...linked,relationships:{nodes:[
 {key:'file:brief.md',kind:'file',id:'brief.md',name:'Brief',action:{file:'brief.md'},lands:[]},
 {key:'chat:c',kind:'chat',id:'c',name:'Research chat',lands:[]},
 {key:'land:col_1',kind:'land',id:'col_1',name:'Research',lands:['col_1']}],edges:[
 {source:'file:brief.md',target:'chat:c',label:'Attached to conversation'},
 {source:'chat:c',target:'land:col_1',label:'Bound to collection'}]}};
const fileSelection=v.recordFor(relationshipFeed,'file','brief.md');
assert.equal(fileSelection.name,'Brief');
assert.equal(v.relationshipAreas(relationshipFeed,fileSelection).join(','),'col_1');
assert.ok(v.relationshipRows(relationshipFeed,fileSelection).includes('Attached to conversation'));
assert.ok(v.relationshipRows(relationshipFeed,fileSelection).includes('data-world-go="chat:c"'));
assert.ok(v.selected(relationshipFeed,fileSelection).includes('data-file="brief.md"'));
assert.equal(v.relatedFeed(relationshipFeed,fileSelection).lands.length,1);
assert.ok(v.relationshipMap(relationshipFeed).includes('world-map'));
