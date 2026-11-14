/* Home view checks without a browser: it draws only what the summary holds, escapes it, and stays out of the way of a chat. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const nodes=new Map(),bodyClasses={};
function node(id){if(!nodes.has(id))nodes.set(id,{innerHTML:'',hidden:true,dataset:{},open:false,close(){this.open=false;}});return nodes.get(id);}
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let summary=null,calls=0,opened=null;
const context={encodeURIComponent,Date,Math,JSON,Promise,Set,Number,String,
  window:{},state:{business:'bakery',data:{workspace:'A',records_revision:'r1'},view:'home',home:true,chat:[],chatMeta:null,busy:false},
  document:{body:{classList:{toggle(name,on){bodyClasses[name]=on;}}},querySelector:()=>null,querySelectorAll:()=>[],addEventListener(){}},
  $:node,esc,human:s=>String(s),stamp:()=>'Nov 12',humanError:e=>e?.message||String(e),attempt:fn=>fn(),
  api:async()=>{calls++;return summary;},details:(title,html)=>{opened={title,html};}};
context.window=context;vm.createContext(context);
vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),context);
const hq=context.auraHQ,flush=()=>new Promise(r=>setTimeout(r,5));
const base={business:{id:'bakery',name:'Harbor <Bakery>',description:''},focus:[],as_of:'2026-11-12T10:00:00Z',changes_days:7,
  knowledge:{findings:0,by_status:{supported:0,unverified:0,challenged:0,needs_review:0,out_of_date:0},
    by_area:[{id:'competitor-intelligence',name:'Competitors',findings:0},{id:'funding-impact',name:'Funding',findings:0},{id:'core',name:'General',findings:0}],
    reviewed:{with_date:0,within_days:30,recent:0}},
  changes:[],attention:[],deadlines:[],goals:[],watches:[],results:[],agents:[],running:[],
  totals:{findings:0,changes:0,attention:0,goals:0,watches:0,results:0,agents:0},empty:true};

(async()=>{
  // A new business: first steps and the areas it can ask about, with no placeholder tiles and nothing invented.
  summary=structuredClone(base);hq.sync();await flush();
  let html=node('#hq').innerHTML;
  assert.equal(node('#hq').hidden,false);assert.equal(bodyClasses['has-hq'],true);
  assert.match(html,/Research my business/);assert.match(html,/See an example business/);assert.match(html,/What you can ask for/);
  const head=()=>node('#hq-head').innerHTML;
  assert.match(head(),/Harbor &lt;Bakery&gt;/,'saved text is escaped');assert.doesNotMatch(head(),/<Bakery>/);
  for(const absent of ['This week','Needs you','Goals','Collections','Running now','Agents','Pick up where you left off'])assert.doesNotMatch(html,new RegExp(absent),absent+' must not show with nothing saved');
  assert.doesNotMatch(html,/General/,'the general area only appears once it has findings');
  assert.match(html,/data-prompt="Research our main competitors/,'an unlit area prepares a first request');

  // A filled business: each section shows its saved rows, and each row opens what is behind it.
  summary=structuredClone(base);Object.assign(summary,{empty:false,focus:[{id:'local-business',name:'Local business'}],
    changes:[{kind:'changed',title:'Crumb & Co',reason:'Cut sourdough to $7.50',at:'2026-11-12T05:40:00Z',collection_id:'col_1',collection:'Local competitors'},
             {kind:'challenged',title:'We are the cheapest',reason:'New evidence challenges this finding.',at:'2026-11-12T05:41:00Z',record:'ins_1'}],
    attention:[{id:'att_1',title:'Confirm revenue',reason:'Needed for the grant.',severity:'high',recommended_action:''}],
    deadlines:[{collection_id:'col_2',collection:'Grants',item_id:'g1',title:'City grant',due:'2026-11-18T00:00:00Z',days:5}],
    goals:[{id:'obj_1',name:'Reach 100 reviews',metric:'Reviews',unit:'reviews',direction:'higher_better',target:100,latest:87,reached:false},{id:'obj_2',name:'Tidy shop'}],
    watches:[{id:'col_1',name:'Local competitors',kind:'results',current:5,last_checked:'2026-11-12T05:40:00Z',last_changes:1}],
    results:[{id:'ast_1',title:'Landing page',type:'landing_page',updated_at:'2026-11-11T00:00:00Z'}],
    agents:[{id:'agt_1',name:'Competitor analyst',tasks:1}],running:[{chat_id:'c1',title:'Price check',agent:'codex',assistant_id:'agt_1'}]});
  summary.knowledge.findings=5;summary.knowledge.by_status={supported:3,unverified:1,challenged:1,needs_review:0,out_of_date:0};
  summary.knowledge.by_area[0].findings=4;summary.knowledge.reviewed={with_date:4,within_days:30,recent:3};
  summary.totals={findings:5,changes:2,attention:1,goals:2,watches:1,results:1,agents:1};
  context.state.data.records_revision='r2';hq.sync();await flush();html=node('#hq').innerHTML;
  for(const shown of ['This week','Needs you','What we know','Goals','Collections','Running now','Pick up where you left off'])assert.match(html,new RegExp(shown),shown);
  assert.doesNotMatch(html,/Research my business/);
  assert.match(html,/data-collection="col_1"/);assert.match(html,/data-record="ins_1"/);assert.match(html,/data-record="att_1"/);assert.match(html,/data-record="obj_1"/);assert.match(html,/data-assistant-open="agt_1"/);
  assert.match(html,/data-hq-item="g1"/);assert.match(html,/data-parent-collection="col_2"/);
  assert.match(html,/87 of 100/);assert.match(html,/Crumb &amp; Co/);assert.match(html,/activity-spinner/,'an agent with a running chat shows it is working');
  assert.match(html,/hq-area lit[^>]*data-hq-area="competitor-intelligence/);
  assert.doesNotMatch(head(),/unsettled/,'the aura encodes only colour and movement');assert.match(head(),/working/,'the aura moves while work is running');

  // The aura explains itself with the same saved counts.
  hq.explain();assert.equal(opened.title,'Your aura');
  assert.match(opened.html,/5 findings saved, 1 challenged by new evidence/);assert.match(opened.html,/3 reviewed in the last 30 days/);assert.match(opened.html,/Local business/);assert.match(opened.html,/1 request working now/);

  // An unchanged business is not fetched again; a chat or a clear new chat hides Home entirely.
  const before=calls;hq.sync();await flush();assert.equal(calls,before,'no second read while nothing changed');
  context.state.chatMeta={id:'c1'};hq.sync();assert.equal(node('#hq').hidden,true);assert.equal(bodyClasses['has-hq'],false);
  context.state.chatMeta=null;context.state.home=false;hq.sync();assert.equal(node('#hq').hidden,true,'New chat stays clear');
  context.state.home=true;context.state.busy=true;hq.sync();assert.equal(node('#hq').hidden,true);

  // Switching business never shows the previous business's summary.
  context.state.busy=false;context.state.business='other';summary={...structuredClone(base),business:{id:'other',name:'Other',description:''}};hq.sync();
  assert.doesNotMatch(node('#hq').innerHTML+head(),/Crumb|Harbor/);await flush();assert.match(head(),/Other/);
  console.log('workspace hq ui: ok');
})().catch(error=>{console.error(error);process.exit(1);});
