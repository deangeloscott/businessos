"""The world feed: what the aura view draws. Read-only, bounded, and built only from saved records."""
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))


def fingerprint(root):
    """Every file under the workspace with its content hash, to prove the feed writes nothing."""
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(root).rglob('*')) if p.is_file()}


def main():
    # A new organization: nothing to draw yet, and the areas its focus points to are offered as places to chart.
    with tempfile.TemporaryDirectory(prefix='aura-world-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        from setup import setup
        import workspace_world as world
        bid=setup(organization='Harbor Bakery')['business_id']
        first=world.world(bid)
        assert first['empty'] and first['business']['name']=='Harbor Bakery' and first['business']['since']
        assert first['lands']==[] and first['findings']==[] and first['changes']==[] and first['goals']==[] and first['decisions']==[]
        assert first['uncharted'] and all(a['id']!='core' for a in first['uncharted']),'an empty world still shows where to start'
        assert first['totals']['items']==0
    # The example business: every light is a saved record, everything points at a place that exists, and nothing is written.
    code=r'''
import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import workspace_example,workspace_world
from _common import workspace_scope
built=workspace_example.build(sys.argv[2])
with workspace_scope(Path(built['path'])):print(json.dumps(workspace_world.world(built['business_id'])))
'''
    with tempfile.TemporaryDirectory(prefix='aura-world-') as t:
        base=Path(t);env={**os.environ,'BUSINESSOS_WORKSPACE_CONFIG':str(base/'pointer.json'),'AURA_STATE_DIR':str(base/'state')};env.pop('BUSINESSOS_WORKSPACE',None)
        w=json.loads(subprocess.run([sys.executable,'-c',code,str(ROOT/'scripts'),str(base/'example')],check=True,capture_output=True,text=True,encoding='utf-8',env=env).stdout)
        lands={l['id'] for l in w['lands']}
        assert not w['empty'] and w['business'].get('example') and len(w['lands'])>=4
        collections=[l for l in w['lands'] if l['kind']=='collection'];areas=[l for l in w['lands'] if l['kind']=='area']
        assert collections and all(l['items'] and l['more']==0 for l in collections),'each collection brings its current results'
        assert all(not l['items'] and l['id'].startswith('area:') for l in areas),'findings kept outside a collection get an area of their own'
        item=collections[0]['items'][0]
        assert set(item)=={'id','title','first_seen','updated_at','last_seen','needs_review','sources','fields','trend','history'} and len(item['fields'])<=3
        assert any(f['source_details'] for f in w['findings']), 'saved evidence and source records are available to the reader'
        assert all(detail['record'] == detail['id'] for finding in w['findings'] for detail in finding['source_details']), 'evidence opens by the same canonical ID used by the record viewer'
        assert all(set(f['lands']) <= lands for f in w['findings'])
        assert all(len(item['history'])<=24 for land in collections for item in land['items'])
        assert w['findings'] and all(f['land'] in lands for f in w['findings']),'every finding sits in a place that is drawn'
        assert all(f['label'] in {'supported','unverified','challenged','needs_review','out_of_date','replaced'} and f['statement'] for f in w['findings'])
        assert any(f['label']=='challenged' and f['challenges'] for f in w['findings']),'a challenged finding says what challenges it'
        ids={l['id']:{i['id'] for i in l['items']} for l in collections}
        assert w['changes'] and all(c['land'] in lands for c in w['changes']) and any(c['item_id'] in ids[c['land']] for c in w['changes'])
        assert w['changes']==sorted(w['changes'],key=lambda c:c['at'],reverse=True)
        measured=[g for g in w['goals'] if 'target' in g]
        assert measured and all(g['points'] and g['points'][-1]['value']==g['latest'] for g in measured),'a ring fills from saved measurements, ending at the latest'
        assert w['decisions'] and all(d['title'] and d['at'] for d in w['decisions'])
        assert all(isinstance(g['lands'],list) and set(g['lands'])<=lands for g in w['goals']) and w['lands_more']==0,'a goal names only the drawn collections saved work ties to it'
        assert all(isinstance(l['uses'],int) and isinstance(l['project_refs'],list) for l in w['lands'])
        assert w['attention'] and w['totals']['items']==sum(len(l['items']) for l in w['lands']) and w['totals']['findings']==len(w['findings'])
        assert w['uncharted']==[] or len(w['lands'])<8
        # Reading the world again changes nothing on disk.
        before=fingerprint(base/'example')
        again=r'''
import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import workspace_world
from _common import workspace_scope
with workspace_scope(Path(sys.argv[2])):workspace_world.world(sys.argv[3])
'''
        subprocess.run([sys.executable,'-c',again,str(ROOT/'scripts'),str(base/'example'),w['business']['id']],check=True,env=env)
        assert fingerprint(base/'example')==before,'the world feed is read-only'
    # Every stage of use: a new organization, a first week, a few months. Each draws only saved records, and limits group rather than drop.
    level=r'''
import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1]);sys.path.insert(0,sys.argv[2])
import world_levels,workspace_world
from _common import workspace_scope
built=world_levels.build(sys.argv[4],sys.argv[3])
with workspace_scope(Path(built['path'])):
    full=workspace_world.world(built['business_id']);workspace_world.MAX_LANDS=3;tight=workspace_world.world(built['business_id'])
print(json.dumps({'full':full,'tight':tight}))
'''
    for name in ('none','low','medium'):
        with tempfile.TemporaryDirectory(prefix='aura-level-') as t:
            base=Path(t);env={**os.environ,'BUSINESSOS_WORKSPACE_CONFIG':str(base/'pointer.json'),'AURA_STATE_DIR':str(base/'state')};env.pop('BUSINESSOS_WORKSPACE',None)
            out=json.loads(subprocess.run([sys.executable,'-c',level,str(ROOT/'scripts'),str(ROOT/'tests'),name,str(base/'w')],check=True,capture_output=True,text=True,encoding='utf-8',env=env).stdout)
            w=out['full'];places={l['id'] for l in w['lands']};collections=[l for l in w['lands'] if l['kind']=='collection']
            assert all(f['land'] in places for f in w['findings']) and all(c['land'] in places for c in w['changes']) and w['findings_hidden']==0,name
            if name=='none':assert w['empty'] and not w['lands'] and w['uncharted'] and not w['tasks'],'a new organization is an uncharted world'
            else:
                assert len(collections)=={'low':1,'medium':5}[name] and w['goals'] and w['tasks'],name
                task=w['tasks'][0];assert task['land'] in places and task['health']=='missing' and not task['available'],'a task whose app no longer has it says so'
                assert any(f['items'] for f in w['findings']) and all(set(f['items'])<={i['id'] for l in collections if l['id']==f['land'] for i in l['items']} for f in w['findings']),'a finding is tied only to results in its own collection that share its source'
                assert any(g['lands'] for g in w['goals']) and any(l['uses'] for l in collections) and all('trend' in i for l in collections for i in l['items']),name
            if name=='medium':
                assert sorted(l['slot'] for l in collections)==[9,10,11,12,13] and all(l['slot']<9 for l in w['lands'] if l['kind']=='area') and all(a['slot']<9 for a in w['uncharted']),'each area keeps its own place and collections take the next ones in the order they were made'
                assert any(f['evidence'] for f in w['findings'] if f['label']=='challenged') and all(not f['evidence'] for f in w['findings'] if f['label']!='challenged'),'a challenged finding carries both sides'
                assert w['decisions'] and all(d['at']<w['as_of'] for d in w['decisions']),'a decision sits at the time it was made'
                tight=out['tight'];group=next(l for l in tight['lands'] if l['kind']=='group')
                assert len(tight['lands'])==3 and tight['lands_more']==3 and len(group['members'])==3 and group['more']==sum(m['current'] for m in group['members']),'more collections than the world draws become one named group'
                shown={l['id'] for l in tight['lands']};assert all(f['land'] in shown for f in tight['findings']) and tight['findings_hidden']>0,'a finding whose place is not drawn is counted, not misplaced'
    # A task its app still has is reported in that app's own words; AI use is grouped by what each chat was for, with unreported costs left out.
    from datetime import datetime,timezone
    import workspace_world as ww,workspace_schedules
    native={'items':[{'id':'t-ok','name':'Weekly competitor check','app':'Codex','schedule':'0 6 * * 1','status':'active','last_run':'2026-11-10T06:00:00Z','next_run':'2026-11-17T06:00:00Z','last_status':'ok'},
                     {'id':'t-bad','name':'Grant watch','app':'Hermes','schedule':'0 7 * * *','status':'active','last_run':'2026-11-15T07:00:00Z','last_status':'failed','last_error':''}]}
    bound=[{'kind':'task','id':'t-ok','business_id':'b','collection_id':'col_1','goal_ref':'g1'},{'kind':'task','id':'t-bad','business_id':'b','collection_id':'col_2'},{'kind':'task','id':'t-gone','business_id':'b','collection_id':'col_1'},
           {'kind':'task','id':'t-loose','business_id':'b'},{'kind':'chat','id':'c1','business_id':'b','collection_id':'col_1'},{'kind':'chat','id':'c2','business_id':'b','project_refs':['prj_1']}]
    with patch.object(workspace_schedules,'inventory',return_value=native):tasks={k['id']:k for k in ww._tasks('b',bound,{'col_1','col_2'})}
    assert set(tasks)=={'t-ok','t-bad','t-gone'},'a task tied to nothing here is not drawn'
    assert tasks['t-ok']['health']=='ok' and tasks['t-ok']['name']=='Weekly competitor check' and tasks['t-ok']['app']=='Codex' and tasks['t-ok']['next_run'] and tasks['t-ok']['goal']=='g1' and tasks['t-ok']['schedule']
    assert tasks['t-bad']['health']=='failed' and 'failed' in tasks['t-bad']['status'] and tasks['t-gone']['health']=='missing' and not tasks['t-gone']['available']
    now=datetime(2026,11,16,tzinfo=timezone.utc);ts=now.timestamp()
    class App:preferences={'usage_receipts':[
        {'business_id':'b','chat_id':'c1','at':ts-3600,'input_tokens':1000,'output_tokens':200,'cost_usd':.02},{'business_id':'b','chat_id':'c1','at':ts-7200,'input_tokens':500,'output_tokens':100},
        {'business_id':'b','chat_id':'c2','at':ts-100,'input_tokens':50,'output_tokens':5,'cost_usd':.001},{'business_id':'b','chat_id':'cX','at':ts-50,'input_tokens':10,'output_tokens':1},
        {'business_id':'b','chat_id':'c1','at':ts-40*86400,'input_tokens':9e6,'output_tokens':0},{'business_id':'other','chat_id':'c1','at':ts-10,'input_tokens':9e6,'output_tokens':0}]}
    effort=ww._effort('b',App,bound,{'col_1','col_2'},now)
    assert [(g['kind'],g['id'],g['requests'],g['tokens'],g['missing_costs']) for g in effort]==[('land','col_1',2,1800,1),('project','prj_1',1,55,0),('other','',1,11,1)],effort
    # What each chat saved about its own requests is the only count of use: findings, collections and methods, never single results.
    views=Path(tempfile.mkdtemp(prefix='aura-views-'))
    (views/'c1.json').write_text(json.dumps([{'role':'user','references':[{'kind':'record','id':'ins_1'},{'kind':'collection','id':'col_1'},{'kind':'library','id':'pb_comp','label':'Competitor Research'},{'kind':'file','id':'x'}]},
        {'role':'user','references':[{'kind':'record','id':'ins_1'},{'kind':'library','id':'pb_comp','label':'Competitor Research'},{'kind':'collection','id':'col_9'}]},{'role':'assistant'}]),encoding='utf-8')
    (views/'broken.json').write_text('{not json',encoding='utf-8')
    class Chats:
        preferences={'chats':[{'id':'c1','business_id':'b'},{'id':'broken','business_id':'b'},{'id':'gone','business_id':'b'},{'id':'c1','business_id':'other'}][:3],'usage_receipts':App.preferences['usage_receipts']}
        @staticmethod
        def chat_display_path(ident):return views/(ident+'.json')
    given=ww._used('b',Chats,{'col_1','col_2'})
    assert given['records']=={'ins_1':2} and given['collections']=={'col_1':1,'col_9':1} and given['library']==[{'id':'pb_comp','name':'Competitor Research','uses':2,'lands':['col_1']}],given
    assert ww._used('b',None,set())=={'records':{},'collections':{},'library':[],'references':[]},'with no chats to read, nothing is claimed'
    from datetime import timedelta
    assert ww._work('b',Chats,now)==ww._work('b',Chats,now+timedelta(minutes=5)),'the same records give the same weeks all day, so an unchanged world is not sent again'
    weeks=ww._work('b',Chats,now);assert len(weeks)==26 and sum(w['requests'] for w in weeks)==5 and weeks[-1]['requests']==4 and ww._work('b',None,now) is None
    split=ww._work_by('b',App,bound,{'col_1','col_2'},now);assert [(g['kind'],g['id'],sum(g['weeks'])) for g in split]==[('land','col_1',3),('project','prj_1',1),('other','',1)] and all(len(g['weeks'])==26 for g in split),split
    App.preferences['usage_receipts'][0]['agent']='Codex';App.preferences['usage_receipts'][2]['agent']='Pi';apps=ww._apps('b',App,bound,{'col_1','col_2'})
    assert apps==[{'name':'Codex','requests':1,'lands':['col_1']},{'name':'Pi','requests':1,'lands':[]}] and ww._apps('b',None,bound,set())==[],apps
    assert abs(effort[0]['cost_usd']-.02)<1e-9 and ww._effort('b',None,bound,set(),now) is None,'last month and other organizations are left out; a missing cost is counted, never guessed'
    from workspace_world_links import relationships
    graph_feed = {'business': {'id': 'b'}, 'lands': [{'id': 'col_1', 'name': 'Research', 'items': [{'id': 'i', 'title': 'Result'}]}],
                  'goals': [{'id': 'g', 'name': 'Goal', 'lands': ['col_1']}], 'findings': [], 'decisions': [], 'tasks': [], 'methods': []}
    graph = relationships(graph_feed, {'projects': [
        {'business_id': 'b', 'id': 'p', 'name': 'Project', 'members': [{'kind': 'file', 'id': 'brief.md'}, {'kind': 'goal', 'id': 'g'}]},
        {'business_id': 'other', 'id': 'secret', 'name': 'Private', 'members': []}]},
        [{'kind': 'chat', 'id': 'c1', 'collection_id': 'col_1'}, {'kind': 'agent', 'id': 'researcher', 'collection_id': 'col_1'}],
        [], given['references'])
    keys = {n['key'] for n in graph['nodes']}
    links = {(e['source'], e['target'], e['type']) for e in graph['edges']}
    assert 'project:secret' not in keys and 'record:ins_1' not in keys, 'unknown and cross-business records stay out'
    assert ('file:x', 'chat:c1', 'attached') in links
    assert ('chat:c1', 'land:col_1', 'assigned') in links
    assert ('agent:researcher', 'land:col_1', 'assigned') in links
    assert ('project:p', 'file:brief.md', 'member') in links and ('land:col_1', 'goal:g', 'feeds') in links
    assert all(e['source'] in keys and e['target'] in keys for e in graph['edges'])
    assert len(links) == len(graph['edges']), 'repeated attachments do not duplicate edges'
    assert not any(e['type'] in {'saved', 'updated', 'into'} for e in graph['edges']), 'attachment never implies authorship'
    assert 'item:col_1|i' not in keys, 'a tracked result is in its collection by its key; it becomes a node only when something is recorded about it'
    produced = relationships({**graph_feed, 'changes': [{'land': 'col_1', 'item_id': 'i', 'by': {'kind': 'chat', 'id': 'c1'}}]}, {'projects': []}, [], [
        {'id': 'asset', 'object_type': 'Asset', 'business_role': 'Draft',
         'extensions': {'businessos': {'work': {'producer': {'kind': 'chat', 'id': 'c1'}}}}},
        {'id': 'src', 'object_type': 'SourceRecord', 'title': 'A source',
         'extensions': {'businessos': {'work': {'producer': {'kind': 'chat', 'id': 'c1'}}}}}
    ], [{'id': 'c1', 'title': 'Research', 'assistant_id': 'a1', 'references': [],
          'subagents': [{'id': 'child', 'name': 'Review'}]}], assistants=[{'id': 'a1', 'name': 'Researcher'}])
    made = {(e['source'], e['target'], e['type']) for e in produced['edges']}
    assert ('chat:c1', 'output:asset', 'saved') in made, 'an output AURA noted during a chat is linked to that chat, and named as an output'
    sessions = relationships(graph_feed, {'projects': []}, [], [
        {'id': 'found', 'object_type': 'Asset', 'business_role': 'Deck'},
        {'id': 'direct', 'object_type': 'Insight', 'statement': 'Seen directly',
         'extensions': {'businessos': {'work': {'producer': {'kind': 'session', 'app': 'Claude Code', 'id': 'cc-1'}}}}},
        {'id': 'continued', 'object_type': 'Insight', 'statement': 'Seen in an AURA chat',
         'extensions': {'businessos': {'work': {'producer': {'kind': 'session', 'app': 'Codex', 'id': 'native-9'}}}}}],
        [{'id': 'c9', 'title': 'Started in AURA', 'native_id': 'native-9', 'references': []}],
        origins={'found': {'kind': 'session', 'app': 'Codex', 'id': 'cx-2', 'title': 'Make the deck'}},
        library_types={'pb_comp': 'Playbook'})
    links3 = {(e['source'], e['target'], e['type']) for e in sessions['edges']}
    names = {n['key']: n for n in sessions['nodes']}
    assert ('session:cc-1', 'finding:direct', 'saved') in links3 and names['session:cc-1']['sub'] == 'Claude Code', 'work done directly in an app links to that app session'
    assert ('chat:c9', 'finding:continued', 'saved') in links3, 'a session AURA itself ran is that AURA conversation, not a second one'
    assert ('session:cx-2', 'output:found', 'saved') in links3 and names['session:cx-2']['name'] == 'Make the deck', 'an origin found later in an app log is drawn like one noted at save time'
    assert not any(t == 'record:src' for _, t, _ in made), 'raw sources stay behind their findings, not listed as outputs'
    assert ('chat:c1', 'item:col_1|i', 'updated') in made and ('chat:c1', 'land:col_1', 'into') in made, 'a check run during a chat links the result it changed, and the area'
    assert ('agent:a1', 'chat:c1', 'used') in made and ('chat:c1', 'agent:c1|child', 'delegated') in made
    # AURA notes where it started the work on its own saves; the AI is asked for nothing, and a replay keeps the first note.
    with tempfile.TemporaryDirectory(prefix='aura-producer-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        from setup import setup
        from _common import workspace_root
        from remember import remember
        import workspace_projects
        bid=setup(organization='Noted Bakery')['business_id']
        os.environ.pop('AURA_PRODUCER',None);os.environ.pop('CLAUDE_CODE_SESSION_ID',None)
        plain=workspace_projects.saved_during(bid,{'id':'x'})
        assert plain=={'id':'x'},'without a chat AURA started or an app session, nothing is added'
        os.environ['CLAUDE_CODE_SESSION_ID']='cc-test'
        direct=workspace_projects.saved_during(bid,{'id':'x'})['extensions']['businessos']['work']['producer']
        assert direct=={'kind':'session','app':'Claude Code','id':'cc-test'},'work done directly in an app that names its session says which'
        os.environ.pop('CLAUDE_CODE_SESSION_ID')
        os.environ['AURA_PRODUCER']=json.dumps({'kind':'chat','id':'chat-1','business_id':bid,'workspace':str(workspace_root().resolve())})
        saved=remember(bid,{'objects':[{'object_type':'Insight','content':{'domain':'core','insight_type':'research_insight','statement':'Weekend demand is higher.','status':'candidate','evidence_links':[]}}]})
        from _common import object_index
        insight=next(o for o,_ in object_index(bid).values() if o.get('object_type')=='Insight' and o.get('statement')=='Weekend demand is higher.')
        assert insight['extensions']['businessos']['work']['producer']=={'kind':'chat','id':'chat-1'},'a finding saved during a chat AURA started says so'
        assert set(insight['extensions']['businessos']['work'])=={'producer'},'it records where the save happened and claims no project or goal'
        import workspace_collections as wc
        made=wc.create(bid,{'key':'prices','name':'Prices'})
        wc.apply(bid,made['id'],{'revision':made['revision'],'run_id':'run-1','status':'complete','coverage':{'scope':'menus','checked':['menus']},'items':[{'id':'crumb','title':'Crumb & Co'}]})
        assert wc.read(bid,made['id'])['checks'][-1]['by']=={'kind':'chat','id':'chat-1'},'a check run during a chat AURA started records that chat'
        os.environ['AURA_PRODUCER']=json.dumps({'kind':'chat','id':'other','business_id':'someone-else','workspace':str(workspace_root().resolve())})
        assert workspace_projects.saved_during(bid,{'id':'x'})=={'id':'x'},"another organization's chat is never recorded here"
    # Where something was made, found afterwards in the apps' own logs: exact matches only, and no answer when unsure.
    with tempfile.TemporaryDirectory(prefix='aura-origins-') as t,patch.dict(os.environ):
        base=Path(t);os.environ.update(CLAUDE_CONFIG_DIR=str(base/'claude'),CODEX_HOME=str(base/'codex'),AURA_STATE_DIR=str(base/'state'))
        import importlib,workspace_origins as wo;importlib.reload(wo)
        claude=base/'claude/projects/proj';claude.mkdir(parents=True);codex=base/'codex/sessions/2026/11/17';codex.mkdir(parents=True)
        line=lambda **kw:json.dumps(kw)+chr(10)
        (claude/'cc-1.jsonl').write_text(line(type='user',timestamp='2026-11-17T10:00:00Z',message={'role':'user','content':'Research our competitors'})
            +line(type='user',timestamp='2026-11-17T10:05:00Z',message={'role':'user','content':[{'type':'tool_result','content':'{"id": "ins_abc", "operation": "created"}'}]})
            +line(type='assistant',timestamp='2026-11-17T10:06:00Z',message={'content':[{'type':'tool_use','name':'Write','input':{'file_path':'C:/w/out/deck.md'}}]}),encoding='utf-8')
        (codex/'rollout-2026-11-17T09-00-00-11111111-2222-3333-4444-555555555555.jsonl').write_text(
            line(timestamp='2026-11-17T09:00:00Z',type='response_item',payload={'type':'message','role':'user','content':[{'type':'input_text','text':'Build the pricing sheet'}]})
            +line(timestamp='2026-11-17T11:00:00Z',type='response_item',payload={'type':'custom_tool_call','name':'apply_patch','input':chr(10).join(['*** Begin Patch','*** Add File: out/prices.csv','+a,b','*** End Patch'])}),encoding='utf-8')
        found=wo.find(record_id='ins_abc',created_at='2026-11-17T10:05:00Z')
        assert found and found['app']=='Claude Code' and found['id']=='cc-1' and found['title']=='Research our competitors','a record is found by its id in the save that created it'
        assert wo.known()['ins_abc']['id']=='cc-1','a found origin is kept for the world'
        from datetime import datetime as dt
        at=lambda v:dt.fromisoformat(v.replace('Z','+00:00')).timestamp()
        sheet=wo.find(file_path='C:/w/out/prices.csv',file_time=at('2026-11-17T11:00:30Z'))
        assert sheet and sheet['app']=='Codex' and sheet['id']=='11111111-2222-3333-4444-555555555555' and sheet['title']=='Build the pricing sheet','a file is found by the app’s own write of it'
        assert wo.find(record_id='ins_abc',created_at='2026-11-18T10:05:00Z') is None,'outside the time of the save there is no answer'
        assert wo.find(file_path='C:/w/out/other.csv',file_time=at('2026-11-17T11:00:00Z')) is None,'a file no app wrote is not attributed'
        (claude/'cc-2.jsonl').write_text(line(type='user',timestamp='2026-11-17T10:07:00Z',message={'role':'user','content':'ins_abc again'}),encoding='utf-8')
        assert wo.find(record_id='ins_abc',created_at='2026-11-17T10:05:00Z') is None,'two sessions match: not certain, so no answer'
    import shutil
    if shutil.which('node'):subprocess.run(['node',str(ROOT/'tests/workspace_aura_ui.cjs'),str(ROOT/'interface/workspace-aura.js')],check=True)
    print('workspace world: ok')


if __name__=='__main__':main()
