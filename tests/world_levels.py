"""Made-up workspaces at five sizes, for checking the aura at every stage of someone's use of AURA.

Each is built through the same saves a real workspace goes through (the example builder), so the world feed
and the interface are exercised on real records: `none` is a new organization, `low` a first week, `medium`
a few months, `high` a busy year, and `max` more than the world draws at once, to prove the limits hold.
"""
import json,os,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

# collections, results in each, findings tied to each, findings outside any collection, goals, checks of each collection, decisions, days of history
LEVELS={'none':(0,0,0,0,0,0,0,1),'low':(1,3,2,0,1,2,0,6),'medium':(5,12,8,10,3,4,2,90),'high':(12,60,24,40,6,6,6,300),'max':(30,320,20,60,8,3,10,420)}
AREAS=['competitor-intelligence','customer-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization','funding-impact']
NAMES=['Local competitors','Wholesale prospects','Grants','Review themes','Search terms','Content calendar','Suppliers','Press mentions','Events','Partners','Regulations','Pricing watch']


def seed(level):
    cols,per,tied,loose,goals,runs,decisions,days=LEVELS[level]
    day=lambda n:'{{now-%dd@06:30}}'%max(0,n) if n>0 else '{{now-1h}}'
    collections=[];research=[]
    for c in range(cols):
        key=f'c{c}';name=NAMES[c] if c<len(NAMES) else f'Watch {c+1}'
        history=[]
        for r in range(runs):
            # Each check sees a few more results than the last, and a tenth of them changed.
            seen=per if runs==1 else max(1,round(per*(r+1)/runs))
            items=[{'id':f'{key}-i{i}','title':f'{name} result {i+1}','summary':f'Result {i+1} kept in {name}.','fields':{'score':(i*7+(r if i%10==r%10 else 0))%100,'status':['Watching','Active','Review'][i%3]},**({'source_refs':[f'https://arxiv.org/abs/25{c%12+1:02d}.{10000+c*400+i:05d}']} if i<tied else {})} for i in range(seen)]
            history.append({'at':day(round(days*(runs-1-r)/max(1,runs))+(1 if r<runs-1 else 0)),'items':items})
        collections.append({'key':key,'name':name,'purpose':f'Made-up {name.lower()} for checking the aura.','runs':history})
        if tied:
            research.append({'method_type':'model_created','domain':AREAS[c%len(AREAS)],
                'sources':[{'source_type':'research_paper','origin':'public web','access_scope':'public','source_reference':f'https://arxiv.org/abs/25{c%12+1:02d}.{10000+c*400+f:05d}','acquisition_method':'direct_page_read','captured_text':f'Source text {f} for {name}.'} for f in range(tied)],
                'observations':[{'statement':f'The source says point {f+1} about {name.lower()}.','source_indexes':[f]} for f in range(tied)],
                'insights':[{'statement':f'{name}: finding {f+1} from what was checked.','observation_indexes':[f],'status':['supported','supported','candidate','supported','contradicted'][f%5] if f%5!=4 or f==4 else 'supported','insight_type':'finding',
                             'extensions':{'businessos':{'collection_refs':['{{collection:%s}}'%key]}}} for f in range(tied)]})
    for start in range(0,loose,20):
        n=min(20,loose-start);area=AREAS[(start//20)%len(AREAS)]
        research.append({'method_type':'model_created','domain':area,
            'sources':[{'source_type':'research_paper','origin':'public web','access_scope':'public','source_reference':f'https://arxiv.org/abs/2412.{50000+start+f:05d}','acquisition_method':'direct_page_read','captured_text':f'Loose source {start+f}.'} for f in range(n)],
            'observations':[{'statement':f'The source says loose point {start+f+1}.','source_indexes':[f]} for f in range(n)],
            'insights':[{'statement':f'A finding kept on its own, number {start+f+1}.','observation_indexes':[f],'status':'supported' if f%4 else 'candidate','insight_type':'finding'} for f in range(n)]})
    measured=[]
    for g in range(goals):
        points=4 if days>30 else 2;target=100+g*50;reached=g%3==2
        measured.append({'name':f'Reach {target} on measure {g+1}','measure':{'name':f'Measure {g+1}','target':str(target),'unit':'count','direction':'higher_better'},
            'measurements':[{'value':round(target*(.35+.65*(p+1)/points)*(1.02 if reached else .82)),'source_ref':'Made-up source','window_start':day(round(days*(points-p)/points)),'window_end':day(round(days*(points-1-p)/points))} for p in range(points)]})
    memory=[{'objects':[{'object_type':'DecisionRecord','content':{'decision':f'Decision {d+1}: keep going with plan {d+1}.','made_by':'The owner (made up)','made_at':day(round(days*(d+1)/(decisions+1))),'status':'current','applies_to':[f'Plan {d+1}']}} for d in range(decisions)]}] if decisions else []
    attention=[{'key':f'{level}-need-{n}','type':'decision_needed','severity':'medium','title':f'Something that needs you, number {n+1}','reason':'Made up, to check how the aura shows it.','recommended_action':'Open it.'} for n in range(min(3,cols))]
    return {'name':f'{level.title()} test workspace','description':f'A made-up workspace at the "{level}" size, for checking the aura.','focus':[],'collections':collections,'memory':[],'research':research,'memory_after':memory,'goals':measured,'attention':attention,'agents':[]}


def build(destination,level):
    """Build one level in an empty folder and return {'path','business_id'}. Sets this process's workspace, like the example builder."""
    import workspace_example
    with tempfile.TemporaryDirectory(prefix='aura-level-') as folder:
        (Path(folder)/'example.json').write_text(json.dumps(seed(level)),encoding='utf-8')
        original=workspace_example.seed_folder
        workspace_example.seed_folder=lambda name=None:Path(folder)
        try:built=workspace_example.build(destination,'level-'+level)
        finally:workspace_example.seed_folder=original
    # Saved links: a task that keeps a collection current and works toward a goal, and chats bound to collections.
    import workspace_world,workspace_collections as collections
    from _common import workspace_scope
    with workspace_scope(Path(built['path'])):
        bid=built['business_id'];feed=workspace_world.world(bid);goals=[g['id'] for g in feed['goals']];lands=[l['id'] for l in feed['lands'] if l['kind']=='collection']
        for n,land in enumerate(lands[:max(1,len(lands)//2)] if lands else []):
            collections.projects.bind(bid,'task',f'level-task-{n}',collection=land,goal_id=goals[n%len(goals)] if goals else None)
            for chat in range(n%3):collections.projects.bind(bid,'chat',f'level-chat-{n}-{chat}',collection=land)
    return built


if __name__=='__main__':
    level,destination=sys.argv[1],sys.argv[2]
    print(json.dumps(build(destination,level)))
