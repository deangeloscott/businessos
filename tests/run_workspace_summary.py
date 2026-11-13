"""The business summary: a bounded, read-only picture built only from saved records, the same through CLI and API."""
import json,os,subprocess,sys,tempfile
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from setup import setup
from remember import remember
from upsert_attention import upsert
import workspace_collections as collections
import workspace_focus as focus
import workspace_goals as goals
import workspace_summary as summary


def finding(bid,statement,status,domain,**bos):
    from persist_research_bundle import persist
    bundle={'method_type':'model_created','domain':domain,
            'sources':[{'source_type':'research_paper','origin':'public web','access_scope':'public','source_reference':'https://arxiv.org/abs/2501.0'+str(abs(hash(statement))%10000).zfill(4),
                        'acquisition_method':'direct_page_read','captured_text':statement}],
            'observations':[{'statement':'The paper reports: '+statement,'source_indexes':[0]}],
            'insights':[{'statement':statement,'observation_indexes':[0],'status':status,'insight_type':'finding',**({'extensions':{'businessos':bos}} if bos else {})}]}
    written,_=persist(bid,bundle)
    return next(obj['id'] for obj,_ in written if obj['object_type']=='Insight')


def main():
    with tempfile.TemporaryDirectory(prefix='aura-summary-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid=setup(organization='Harbor Bakery')['business_id']
        now=datetime.now(timezone.utc);iso=lambda d:d.isoformat(timespec='seconds').replace('+00:00','Z')

        # A new organization is reported as empty, with every area listed and nothing invented.
        first=summary.summary(bid)
        assert first['empty'] and first['business']['name']=='Harbor Bakery' and first['knowledge']['findings']==0
        assert [a['name'] for a in first['knowledge']['by_area']][:2]==['Competitors','Customers'] and len(first['knowledge']['by_area'])==9
        assert first['changes']==[] and first['goals']==[] and first['watches']==[] and first['attention']==[]
        assert 'Nothing has been saved yet' in summary.text(first)
        with patch.object(summary,'_agents',return_value=[{'id':'writer','name':'Writer','tasks':0}]):
            with_agent=summary.summary(bid)
            assert not with_agent['empty'] and 'Agents: Writer' in summary.text(with_agent)

        # Findings count by the interface's status words and by area; a passed review date means "needs review".
        focus.save(bid,['local-business','grants'])
        finding(bid,'Regulars order sourdough on Saturdays','supported','customer-intelligence')
        finding(bid,'A rival may open on Main Street','candidate','competitor-intelligence')
        challenged=finding(bid,'Our sourdough is the cheapest in town','contradicted','competitor-intelligence')
        finding(bid,'The city grant favours food businesses','supported','funding-impact',review_after=iso(now-timedelta(days=2)))
        finding(bid,'An older note about flour prices','superseded','industry-intelligence')
        s=summary.summary(bid);k=s['knowledge']
        assert k['findings']==4,'replaced findings are history, not current knowledge'
        assert k['by_status']=={'supported':1,'unverified':1,'challenged':1,'needs_review':1,'out_of_date':0},k['by_status']
        areas={a['id']:a['findings'] for a in k['by_area']}
        assert areas['competitor-intelligence']==2 and areas['customer-intelligence']==1 and areas['funding-impact']==1 and areas['content-synthesis']==0
        assert [a['name'] for a in s['focus']]==['Local business','Grants'] and not s['empty']
        assert any(c['kind']=='challenged' and c['record']==challenged for c in s['changes']),'a newly challenged finding is a change worth seeing'

        # Freshness is reported only among findings that record a review date.
        assert k['reviewed']=={'with_date':0,'within_days':30,'recent':0}

        # Attention items: open ones only, most severe first.
        upsert(bid,'grant-revenue','missing_fact','high','Confirm 2025 revenue for the grant form','The application needs it.','Reply with the figure.')
        upsert(bid,'price-test','decision','low','Approve the weekend price test','A test is ready.')
        s=summary.summary(bid)
        assert [a['title'] for a in s['attention']]==['Confirm 2025 revenue for the grant form','Approve the weekend price test']

        # Goals that track a number come first and report the latest recorded value, never an estimate.
        goals.save(bid,{'name':'Keep the shop tidy','scope':'workspace'})
        g=goals.save(bid,{'name':'Reach 100 Google reviews','scope':'workspace','measure':{'name':'Google reviews','target':'100','unit':'reviews','direction':'higher_better'}})
        s=summary.summary(bid);goal=s['goals'][0]
        assert goal['name']=='Reach 100 Google reviews' and goal['target']==100 and goal['latest'] is None and not goal['reached']
        remember(bid,{'objects':[{'object_type':'MetricObservation','content':{'metric_ref':g['metric_refs'][0],'value':87,'source_ref':'Google Business Profile','window_start':'2026-11-01T00:00:00Z','window_end':'2026-11-10T00:00:00Z'}}]})
        assert summary.summary(bid)['goals'][0]['latest']==87
        assert '87 of 100' in summary.text(summary.summary(bid))

        # Watches report their latest check, and a run's material changes appear as recent changes.
        made=collections.create(bid,{'key':'grants','name':'Grants','purpose':'Grants we could win'})
        collections.apply(bid,made['id'],{'revision':made['revision'],'run_id':'run-1','items':[
            {'id':'city-grant','title':'City small-business grant','expires_at':iso(now+timedelta(days=6)),'change_reason':'New eligible grant'}]})
        s=summary.summary(bid)
        watch=s['watches'][0]
        assert watch['name']=='Grants' and watch['current']==1 and watch['last_changes']==1 and watch['last_checked']
        assert not any(c.get('collection')=='Grants' for c in s['changes']),'filling a collection for the first time is not a change'
        collections.apply(bid,made['id'],{'revision':collections.show(bid,made['id'])['revision'],'run_id':'run-2','items':[
            {'id':'state-fund','title':'State main-street fund','change_reason':'New eligible grant'}]})
        s=summary.summary(bid)
        change=next(c for c in s['changes'] if c.get('collection')=='Grants')
        assert s['totals']['changes']==len(s['changes'])==2
        assert change['item_id']=='state-fund'
        assert change['kind']=='new' and change['title']=='State main-street fund' and change['reason']=='New eligible grant'
        assert s['deadlines'] and s['deadlines'][0]['title']=='City small-business grant' and s['deadlines'][0]['days'] in (5,6)

        # "What changed" looks back a bounded number of days.
        old=summary.summary(bid,at=now+timedelta(days=30),days=7)
        assert not any(c.get('collection')=='Grants' for c in old['changes']),'old changes drop out of the recent list'
        assert summary.summary(bid,days=1000)['changes_days']==90

        # Bounded: many findings never make the summary large.
        for n in range(30):upsert(bid,f'item-{n}','reminder','low',f'Item {n}','Reason')
        s=summary.summary(bid)
        assert len(s['attention'])==5 and s['totals']['attention']==32 and len(json.dumps(s))<12000

        # The CLI returns the same data, and plain words on request.
        cli=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_summary.py'),'--workspace',str(root),'--business-id',bid],capture_output=True,text=True,check=True)
        data=json.loads(cli.stdout)
        assert data['knowledge']==s['knowledge'] and data['totals']==s['totals']
        words=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_summary.py'),'--workspace',str(root),'--business-id',bid,'--text'],capture_output=True,text=True,check=True).stdout
        assert 'What we know: 4 findings' in words and 'Needs someone:' in words and 'Counts are of saved records only' in words
        bad=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_summary.py'),'--workspace',str(root),'--business-id','missing'],capture_output=True,text=True)
        assert bad.returncode!=0

        # The interface reads the same summary and adds only what this running view is working on.
        from workspace_ui import Workspace,handler_for
        import threading,urllib.request
        from http.server import ThreadingHTTPServer
        app=Workspace();server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));port=server.server_port
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            request=urllib.request.Request(f'http://127.0.0.1:{port}/api/summary?business={bid}',headers={'X-Aura-Token':app.token})
            with urllib.request.urlopen(request,timeout=10) as response:api=json.loads(response.read())
            assert api['running']==[] and api['knowledge']['findings']==4 and api['business']['name']=='Harbor Bakery'
            try:urllib.request.urlopen(f'http://127.0.0.1:{port}/api/summary?business={bid}',timeout=10)
            except urllib.error.HTTPError as error:assert error.code in (400,403)
            else:raise AssertionError('The summary must need the page token.')
        finally:server.shutdown();server.server_close()
    # The home page draws only what the summary holds.
    import shutil
    if shutil.which('node'):subprocess.run(['node',str(ROOT/'tests/workspace_hq_ui.cjs'),str(ROOT/'interface/workspace-hq.js')],check=True)
    print('workspace summary: ok')


if __name__=='__main__':main()
