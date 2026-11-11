"""Watches keep knowledge current: findings fold in, change notices fire once, and other workspaces are read-only."""
import json,os,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import workspace_scope
from setup import setup
from remember import remember
from workspace_ui import Workspace
import workspace_projects as projects
import workspace_collections as collections
import workspace_views as views
import workspace_reading as reading


def rejects(fn,words=''):
    try:fn()
    except ValueError as error:
        assert words in str(error),str(error);return
    raise AssertionError('An invalid change was accepted')


def finding(bid,statement,status,col,**bos):
    """A finding saved the way the method says: quoted source, observation, then the finding linked to its watch."""
    from persist_research_bundle import persist
    bundle={'method_type':'model_created','domain':'industry-intelligence',
            'sources':[{'source_type':'research_paper','origin':'public web','access_scope':'public','source_reference':'https://arxiv.org/abs/2501.0'+str(abs(hash(statement))%10000).zfill(4),
                        'acquisition_method':'direct_page_read','captured_text':statement}],
            'observations':[{'statement':'The paper reports: '+statement,'source_indexes':[0]}],
            'insights':[{'statement':statement,'observation_indexes':[0],'status':status,'insight_type':'finding','extensions':{'businessos':{'collection_refs':[col],**bos}}}]}
    written,_=persist(bid,bundle)
    return next(obj['id'] for obj,_ in written if obj['object_type']=='Insight')


def main():
    with tempfile.TemporaryDirectory(prefix='aura-knowledge-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace';state=base/'state'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(state))
        bid=setup(organization='Research desk')['business_id'];app=Workspace()

        # Sources are kept as links and quotes unless the person chooses full copies.
        made=collections.create(bid,{'key':'papers','name':'Agent research','purpose':'Track what is known about coding agents'})
        shown=collections.show(bid,made['id'])
        assert shown['source_copies']=='quotes' and shown['findings']==[] and shown['findings_total']==0
        rejects(lambda:collections.create(bid,{'key':'bad','name':'Bad','source_copies':'everything'}),'full copies')
        changed=collections.configure(bid,made['id'],{'revision':shown['revision'],'source_copies':'full'})
        assert collections.show(bid,made['id'])['source_copies']=='full'
        assert 'full copy or snapshot' in collections.instructions(bid,made['id'])
        changed=collections.configure(bid,made['id'],{'revision':changed['revision'],'source_copies':'quotes'})
        text=collections.instructions(bid,made['id'])
        assert 'keeping-knowledge-current.md' in text and 'fold it into the linked findings' in text and 'exact short quotes' in text and '"upkeep": true' in text
        cli=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_collections.py'),'instructions','--workspace',str(root),'--business-id',bid,'--id',made['id']],capture_output=True,text=True,check=True)
        assert json.loads(cli.stdout)['instructions'].startswith('[Aura results]'),'the CLI must print the same run instructions a bound task receives'

        # Upkeep is recorded on the run that did it, and only as true or false.
        rejects(lambda:collections.apply(bid,made['id'],{'revision':changed['revision'],'run_id':'bad','upkeep':'yes','items':[]}),'Upkeep')
        first=collections.apply(bid,made['id'],{'revision':changed['revision'],'run_id':'run-1','status':'complete','coverage':{'scope':'arXiv cs.AI','checked':['arxiv']},
                                               'items':[{'id':'arxiv:2501.00001','title':'A paper','source_refs':['https://arxiv.org/abs/2501.00001']}]})
        assert first['change_count']==1 and 'last_upkeep_at' not in collections.read(bid,made['id'])
        second=collections.apply(bid,made['id'],{'revision':first['revision'],'run_id':'run-2','status':'complete','coverage':{'scope':'arXiv cs.AI','checked':['arxiv']},'items':[],'upkeep':True})
        shown=collections.show(bid,made['id'])
        assert shown['last_upkeep_at'] and shown['latest_check']['upkeep'] is True and second['no_change_verified']

        # Findings: challenged first, replaced ones kept as history, due reviews counted, archived and unlinked ones excluded.
        old=finding(bid,'Agents solve 30% of benchmark tasks.','supported',made['id'])
        new=finding(bid,'Agents solve 45% of benchmark tasks.','supported',made['id'],supersedes=old)
        remember(bid,{'objects':[{'object_ref':old,'content':{'status':'superseded'}}]})
        challenged=finding(bid,'Longer context always helps.','contradicted',made['id'])
        due=finding(bid,'Tool use reduces errors.','candidate',made['id'],review_after='2020-01-01T00:00:00Z')
        finding(bid,'Unrelated finding.','supported','col_00000000000000000000')
        archived=finding(bid,'Archived finding.','supported',made['id'])
        remember(bid,{'objects':[{'object_ref':archived,'content':{'extensions':{'businessos':{'collection_refs':[made['id']],'archive':{'at':1.0}}}}}]})
        shown=collections.show(bid,made['id'])
        order=[f['id'] for f in shown['findings']]
        assert order[0]==challenged and set(order)=={challenged,new,due},order
        assert shown['challenged']==1 and shown['needs_review']==1 and shown['findings_total']==3
        assert [f['id'] for f in shown['replaced']]==[old] and shown['replaced'][0]['superseded_by']==new
        assert next(f for f in shown['findings'] if f['id']==new)['supersedes']==old

        # Source memory that belongs to a watch is listed with it.
        remember(bid,{'objects':[{'object_type':'SourceProfile','content':{'source_reference':'https://arxiv.org/list/cs.AI/new','source_kind':'publication','topic_tags':['agents'],
                     'watch_status':'active','attention_priority':'medium','fact_type_assessments':[],'display_name':'arXiv cs.AI',
                     'extensions':{'businessos':{'collection_refs':[made['id']]}}}}]})
        assert [s['name'] for s in collections.show(bid,made['id'])['source_memory']]==['arXiv cs.AI']

        # What keeps a collection current comes from the saved task binding.
        projects.bind(bid,'task','t-papers',[],made['id'])
        projects.bind(bid,'task','t-other',[])
        tasks={'items':[{'id':'t-papers','name':'Agent research watch','app':'Codex','schedule':'0 9 * * 1','status':'active','last_run':'','last_status':''},
                        {'id':'t-other','name':'Other','app':'Codex','schedule':'0 9 * * 1','status':'active'}]}
        with patch('workspace_schedules.inventory',return_value=tasks):
            keeping=views.running(app,bid,collection_id=made['id'])
        assert [i['id'] for i in keeping['items']]==['t-papers'] and 'Results go to' not in keeping['items'][0]['text']
        assert keeping['items'][0]['text'].startswith('Every Monday at 9:00 AM, Codex runs “Agent research watch”.')
        rejects(lambda:views.running(app,bid,project_id='x',collection_id=made['id']))

        pending=collections.coverage({'status':'complete','coverage':{'checked':['arxiv'],'deferred':['paper-B']}},{})
        assert pending['status']=='partial' and pending['deferred']==['paper-B']
        prior={'checks':[{'coverage':pending}]}
        assert collections.coverage({'coverage':{}},prior)['deferred']==['paper-B']
        assert collections.coverage({'coverage':{'deferred':[]}},prior)['deferred']==[]
        # Change notices: earlier history is not news, a run with changes rings once, routine runs stay quiet.
        app.preferences['notification_items']=[]
        app.check_collection_changes()
        assert app.preferences['notification_items']==[],'existing history must not flood the bell'
        latest=collections.read(bid,made['id'])
        third=collections.apply(bid,made['id'],{'revision':collections.revision(latest),'run_id':'run-3','status':'complete','coverage':{'scope':'arXiv cs.AI','checked':['arxiv']},
                                               'items':[{'id':'arxiv:2501.00002','title':'Another paper'},{'id':'arxiv:2501.00003','title':'A third paper'}]})
        app.check_collection_changes();app.check_collection_changes()
        notes=[n for n in app.preferences['notification_items'] if n['kind']=='changes']
        assert len(notes)==1 and 'Another paper' in notes[0]['title'] and '+1 more' in notes[0]['title'] and notes[0]['collection_id']==made['id'],notes
        collections.apply(bid,made['id'],{'revision':third['revision'],'run_id':'run-4','status':'complete','coverage':{'scope':'arXiv cs.AI','checked':['arxiv']},'items':[]})
        app.check_collection_changes()
        assert len([n for n in app.preferences['notification_items'] if n['kind']=='changes'])==1,'a run without material changes must stay quiet'

        # Reading across workspaces: off by default, set per workspace, read-only and labelled.
        other=base/'library'
        with workspace_scope(other):
            os.environ['BUSINESSOS_WORKSPACE']=str(other)
            lib=setup(organization='My research library')['business_id']
            finding(lib,'Retrieval-augmented agents cut hallucinated citations.','supported','col_11111111111111111111')
        os.environ['BUSINESSOS_WORKSPACE']=str(root)
        state.mkdir(parents=True,exist_ok=True)
        (state/'recent-workspaces.json').write_text(json.dumps([{'path':str(root),'name':'Research desk'},{'path':str(other),'name':'My research library'},{'path':str(base/'missing'),'name':'Gone'}]),encoding='utf-8')
        assert reading.allowed() is False and reading.readable_workspaces()==[]
        assert reading.search('hallucinated citations')==[],'a workspace must stay private until it allows reading'
        reading.set_allowed(True,other)
        assert reading.allowed(other) and [w['name'] for w in reading.readable_workspaces()]==['My research library']
        rejects(lambda:reading.set_allowed('yes'))
        hits=reading.search('hallucinated citations')
        assert hits and hits[0]['workspace']=='My research library' and hits[0]['business_id']==lib and Path(hits[0]['path']).is_file()
        from enter import prepare_work
        result=prepare_work('What do we know about hallucinated citations?',bid)
        assert result['retrieval']['other_workspaces']['items'][0]['workspace']=='My research library' and 'never write' in result['retrieval']['other_workspaces']['read_only']
        with workspace_scope(other):
            assert reading.readable_workspaces()==[],'the switch lets others read this workspace; it does not open the others'
        reading.set_allowed(False,other)
        assert prepare_work('What do we know about hallucinated citations?',bid)['retrieval']['other_workspaces'] is None

        # Every watch starter keeps knowledge current.
        import workspace_focus
        loaded,problems=workspace_focus.areas()
        assert not problems and len(loaded)==10,problems
        for area in (ROOT/'focus-areas').glob('*.md'):
            if area.name.lower()=='readme.md':continue
            watch=area.read_text(encoding='utf-8').split('kind: watch',1)
            if len(watch)==2:assert 'Keep what we know current' in watch[1].split('\n  - ',1)[0],area.name
    print('Knowledge currency passed: sources kept as chosen, upkeep recorded, findings ordered and replaced as history, keepers shown, one change notice per run, reading across workspaces opt-in and read-only, starters current.')


if __name__=='__main__':main()
