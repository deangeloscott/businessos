"""Focus and focus areas: valid built-ins, safe overrides, bounded context, and measurable goals that notify once."""
import os,sys,tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from setup import setup
from remember import remember
from workspace_ui import Workspace
import workspace_focus as focus
import workspace_goals as goals
from _common import object_index


def rejects(fn,words):
    try:fn()
    except ValueError as error:assert words in str(error),error;return
    raise AssertionError('accepted: '+words)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-focus-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid=setup(organization='Harbor Food Bank')['business_id'];app=Workspace()

        # Every built-in area is valid and points only at knowledge that exists.
        built,problems=focus.areas()
        assert not problems and len(built)==10,problems
        for area in built:
            assert area['summary'] and area['guidance'] and len(area['quick_starts'])<=3,area['id']
            for link in area['knowledge']:assert (ROOT/link).exists(),f'{area["id"]} links to missing {link}'

        # Suggestions come from the description; saving keeps the chosen order and rejects unknown areas.
        assert focus.suggest("We're a dental practice in Towson, MD")==['local-business']
        assert set(focus.suggest('Nonprofit food bank funded by grants and donors'))=={'nonprofit','grants'}
        rejects(lambda:focus.save(bid,['grants','made-up']),'no longer available')
        saved=focus.save(bid,['nonprofit','grants','local-business'])
        assert [a['id'] for a in saved['areas']]==['nonprofit','grants','local-business']
        business=next(o for o,_ in object_index(bid).values() if o['object_type']=='Business')
        assert business['extensions']['businessos']['focus_areas']==['nonprofit','grants','local-business']
        starts=focus.quick_starts(saved)
        assert len(starts)==3 and [s['area'] for s in starts]==['Nonprofit','Grants','Local business'],'quick starts should take each area in turn'

        # A workspace file replaces a built-in area there; a broken file is reported without hiding the others.
        own=root/'knowledge/focus-areas';own.mkdir(parents=True)
        (own/'grants.md').write_text('---\nname: Grants (ours)\nsummary: State arts grants only.\n---\nOur funders are state arts councils.\n',encoding='utf-8')
        (own/'broken.md').write_text('no front matter',encoding='utf-8')
        areas,problems=focus.areas()
        mine=next(a for a in areas if a['id']=='grants')
        assert mine['name']=='Grants (ours)' and mine['customized'] and mine['origin']=='yours'
        assert len(areas)==10 and any('broken.md' in p for p in problems)

        # The AI gets a short note, inside the request and from enter.py; saved facts take priority.
        note=focus.context(bid)
        assert 'Nonprofit' in note and 'Grants (ours)' in note and 'take priority' in note and len(note)<=1800
        assert note in app.request_text(bid,'Plan this month')
        from enter import prepare_work
        assert prepare_work('Plan this month',bid)['organization_focus']==note
        focus.save(bid,[]);assert focus.context(bid)=='' and focus.context(bid) not in ('None',)

        # Measurable goals reuse a metric by name, show progress, and notify once when reached.
        g=goals.save(bid,{'name':'Grow monthly donors to 100','scope':'workspace','measure':{'name':'Monthly donors','target':'100','unit':'donors','direction':'higher_better'}})
        metric=g['metric_refs'][0]
        assert g['extensions']['businessos']['goal']['target_value']==100
        other=goals.save(bid,{'name':'Keep donors growing','scope':'workspace','measure':{'name':'monthly donors','target':120}})
        assert other['metric_refs']==[metric],'the same measure should reuse its metric'
        rejects(lambda:goals.save(bid,{'name':'Bad','scope':'workspace','measure':{'name':'X','target':'lots'}}),'number')
        def record(value,end):
            remember(bid,{'objects':[{'object_type':'MetricObservation','content':{'metric_ref':metric,'value':value,'source_ref':'Donor system','window_start':end[:8]+'01T00:00:00Z','window_end':end}}]})
        record(80,'2026-09-30T23:59:00Z')
        import workspace_views as views
        assert views.goal_targets([o for o,_ in object_index(bid).values()])[g['id']]['reached'] is False
        app.check_goals_reached();assert not [n for n in app.preferences['notification_items'] if n.get('kind')=='goal']
        record(104,'2026-10-31T23:59:00Z')
        state=views.goal_targets([o for o,_ in object_index(bid).values()])[g['id']]
        assert state['reached'] and state['latest']==104
        app.check_goals_reached();app.check_goals_reached()
        reached=[n for n in app.preferences['notification_items'] if n.get('kind')=='goal']
        # Only the goal whose target (100) was met notifies, and only once; the 120 target is not yet reached.
        assert [n['goal_id'] for n in reached]==[g['id']],reached
        assert 'Grow monthly donors to 100' in reached[0]['title'] and '104 donors' in reached[0]['title']
        # Clearing the measure removes the target and the link; nothing else about the goal changes.
        cleared=goals.save(bid,{'id':g['id'],'measure':''})
        assert 'metric_refs' not in cleared and 'target_value' not in cleared['extensions']['businessos']['goal'] and cleared['name']==g['name']
        app.native_sessions.close()
    print('Focus passed: valid built-ins, suggestions, safe overrides, bounded AI context, and measurable goals that notify once.')


if __name__=='__main__':
    main()
