"""Map, chart, board and running views: the parts where a mistake would leak data, mislead, or break offline."""
import io,json,os,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from setup import setup
from remember import remember
from workspace_ui import Workspace
import workspace_projects as projects
import workspace_collections as collections
import workspace_goals as goals
import workspace_views as views


class Reply(io.BytesIO):
    def __enter__(self):return self
    def __exit__(self,*a):return False


def main():
    with tempfile.TemporaryDirectory(prefix='aura-views-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid=setup(organization='Towson Dental')['business_id'];app=Workspace()
        made=collections.create(bid,{'key':'map-pack','name':'Competitors','purpose':'Who shows up for dentist in Towson'})
        items=[{'id':'us','title':'Towson Dental','fields':{'rank':2,'rating':4.8,'latitude':39.40,'longitude':-76.60,'yours':True,'type':'You'}},
               {'id':'a','title':'Smile Studio','fields':{'rank':1,'rating':4.6,'address':'1 York Rd, Towson, MD','type':'Competitor'}},
               {'id':'b','title':'Bright Teeth','fields':{'rank':3,'rating':4.1,'address':'9 Unknown Lane','type':'Competitor'}},
               {'id':'c','title':'Online-only clinic','fields':{'rating':3.9,'type':'Competitor'}}]
        collections.apply(bid,made['id'],{'revision':made['revision'],'run_id':'check-1','items':items})
        shown=collections.show(bid,made['id'])
        assert shown['views']=={'map':True,'chart':['rank','rating'],'board':['type']},shown['views']

        # Places: coordinates are used as given; an address is asked once and remembered, never re-sent.
        sent=[]
        def lookup(request,timeout=0):
            sent.append(request.full_url);assert 'ViralTrac-AURA' in request.headers['User-agent']
            return Reply(json.dumps([{'lat':'39.401','lon':'-76.602'}] if 'York' in request.full_url else []).encode())
        rows=views.rows(bid,made['id'])
        assert rows['pending']==2 and [r['id'] for r in rows['unplaced']]==['c']
        assert next(r for r in rows['items'] if r['id']=='us')['placed_by']=='result'
        with patch.object(views.urllib.request,'urlopen',lookup),patch.object(views.time,'sleep'):
            result=views.place(bid,made['id'])
            assert result=={'placed':1,'remaining':0},result
            again=views.place(bid,made['id'])
        assert len(sent)==2 and again=={'placed':0,'remaining':0},'an address was looked up twice'
        rows=views.rows(bid,made['id'])
        assert next(r for r in rows['items'] if r['id']=='a')['placed_by']=='address' and rows['pending']==0
        assert {r['id']:r['reason'] for r in rows['unplaced']}=={'b':'Address not found','c':'No address or coordinates'}
        # Offline: lookups stop with an explanation instead of failing the map.
        collections.apply(bid,made['id'],{'revision':collections.show(bid,made['id'])['revision'],'run_id':'check-2','items':[{'id':'d','title':'New clinic','fields':{'address':'5 Main St'}}]})
        with patch.object(views.urllib.request,'urlopen',side_effect=OSError('offline')),patch.object(views.time,'sleep'):
            stopped=views.place(bid,made['id'])
        assert stopped['remaining']==1 and 'internet' in stopped['stopped']

        # Map imagery: viewed areas are kept and still served offline; nothing is fetched for a bad area.
        for bad in ((20,0,0),(3,8,0),(3,0,-1)):
            try:views.tile(*bad);raise AssertionError('an invalid map area was requested')
            except ValueError:pass
        with patch.object(views.urllib.request,'urlopen',return_value=Reply(b'png')) as fetch:
            assert views.tile(5,9,12)==b'png' and views.tile(5,9,12)==b'png' and fetch.call_count==1,'fresh imagery was downloaded again'
        old=time.time()-views.TILE_FRESH-60;os.utime(base/'state/map-tiles/5/9/12.png',(old,old))
        with patch.object(views.urllib.request,'urlopen',side_effect=OSError('offline')):
            assert views.tile(5,9,12)==b'png','offline imagery that was viewed before disappeared'
            try:views.tile(5,9,13);raise AssertionError('missing offline imagery should explain itself')
            except ValueError as error:assert 'internet' in str(error)

        # What's running: facts from saved links, health stated plainly, other projects excluded.
        project=projects.change(bid,{'action':'create','name':'Local marketing'})['project']
        other=projects.change(bid,{'action':'create','name':'Hiring'})['project']
        goal=goals.save(bid,{'name':'10 new patients a week','scope':'workspace'})
        projects.change(bid,{'action':'link','id':project['id'],'reference':{'kind':'goal','id':goal['id']}})
        projects.bind(bid,'task','t-map',[project['id']],made['id'],goal['id'])
        projects.bind(bid,'task','t-ads',[project['id']])
        projects.bind(bid,'task','t-gone',[project['id']])
        projects.bind(bid,'task','t-jobs',[other['id']])
        tasks={'items':[{'id':'t-map','name':'Check map pack','app':'Claude','schedule':'RRULE:FREQ=DAILY;BYHOUR=8;BYMINUTE=0','status':'active','last_run':time.time()-60,'last_status':'success'},
                        {'id':'t-ads','name':'Summarise ads','app':'Codex','schedule':'0 9 * * 1','status':'active','last_run':'','last_status':'error','last_error':'Plan limit reached\nmore detail'},
                        {'id':'t-jobs','name':'Post jobs','app':'Codex','schedule':'0 9 * * *','status':'paused'}]}
        with patch('workspace_schedules.inventory',return_value=tasks):
            summary=views.running(app,bid,project_id=project['id'])
            by={i['id']:i for i in summary['items']}
            assert set(by)=={'t-map','t-ads','t-gone'},'another project’s task appeared'
            assert by['t-map']['text'].startswith('Every day at 8:00 AM, Claude runs “Check map pack”. Results go to Competitors (') and 'waiting for review' in by['t-map']['text']
            assert 'Working toward: 10 new patients a week.' in by['t-map']['text'] and by['t-map']['health']=='ok'
            assert by['t-ads']['health']=='failed' and by['t-ads']['text'].endswith('Last run failed: Plan limit reached') and 'Every Monday at 9:00 AM' in by['t-ads']['text']
            assert by['t-gone']['health']=='missing' and summary['attention']==2 and summary['goals']==['10 new patients a week']
            assert summary['text'].startswith('What’s running for Local marketing:')
            for_goal=views.running(app,bid,goal_id=goal['id'])
            assert [i['id'] for i in for_goal['items']]==['t-map'] and 'Working toward' not in for_goal['items'][0]['text']
        try:views.running(app,bid);raise AssertionError('running needs a project or goal')
        except ValueError:pass

        # Goal progress: only numeric measurements linked to the goal, oldest first, with their source.
        metric=remember(bid,{'objects':[{'object_type':'MetricDefinition','content':{'name':'New patients','unit':'patients','direction':'higher_better','objective_refs':[goal['id']]}}]})['objects'][0]['id']
        unrelated=remember(bid,{'objects':[{'object_type':'MetricDefinition','content':{'name':'Clicks','unit':'clicks','direction':'higher_better'}}]})['objects'][0]['id']
        week=lambda d:{'window_start':f'2026-10-{d:02d}T00:00:00Z','window_end':f'2026-10-{d+6:02d}T23:59:00Z'}
        remember(bid,{'objects':[{'object_type':'MetricObservation','content':{'metric_ref':metric,'value':7,'source_ref':'Booking system',**week(12)}},
                                 {'object_type':'MetricObservation','content':{'metric_ref':metric,'value':5,'source_ref':'Booking system',**week(5)}},
                                 {'object_type':'MetricObservation','content':{'metric_ref':metric,'value':'unknown','source_ref':'Booking system',**week(19)}},
                                 {'object_type':'MetricObservation','content':{'metric_ref':unrelated,'value':900,'source_ref':'Ads',**week(12)}}]})
        progress=views.progress(bid,goal['id'])
        assert [m['name'] for m in progress['metrics']]==['New patients']
        assert [p['value'] for p in progress['metrics'][0]['points']]==[5,7] and progress['metrics'][0]['points'][-1]['source']=='Booking system'
        app.native_sessions.close()
    print('Views passed: map places asked once and kept offline, imagery kept, running summaries scoped and plain, goal progress linked and sourced.')


if __name__=='__main__':
    main()
