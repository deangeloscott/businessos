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
        assert set(item)=={'id','title','first_seen','updated_at','last_seen','needs_review','sources','fields','trend'} and len(item['fields'])<=3
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
    assert ww._used('b',None,set())=={'records':{},'collections':{},'library':[]},'with no chats to read, nothing is claimed'
    weeks=ww._work('b',Chats,now);assert len(weeks)==26 and sum(w['requests'] for w in weeks)==5 and weeks[-1]['requests']==4 and ww._work('b',None,now) is None
    split=ww._work_by('b',App,bound,{'col_1','col_2'},now);assert [(g['kind'],g['id'],sum(g['weeks'])) for g in split]==[('land','col_1',3),('project','prj_1',1),('other','',1)] and all(len(g['weeks'])==26 for g in split),split
    assert abs(effort[0]['cost_usd']-.02)<1e-9 and ww._effort('b',None,bound,set(),now) is None,'last month and other organizations are left out; a missing cost is counted, never guessed'
    import shutil
    if shutil.which('node'):subprocess.run(['node',str(ROOT/'tests/workspace_aura_ui.cjs'),str(ROOT/'interface/workspace-aura.js')],check=True)
    print('workspace world: ok')


if __name__=='__main__':main()
