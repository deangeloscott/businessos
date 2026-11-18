"""Keeping up with the AI apps: their versions, a check after each update, what is new, updates they report, models they
no longer offer, and an app that is gone. AURA never updates an app itself, and makes no AI request for any of this."""
import json,os,sys,tempfile,textwrap
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import workspace_scope


FAKE=textwrap.dedent('''
    import json,os,sys
    state=json.load(open(os.environ['FAKE_APP_STATE']))
    if sys.argv[1:]==['--version']:print(state['banner'])
    elif sys.argv[1:]==['update','--check']:print('Current version: '+state['version']);print('New version available: '+state['latest']) if state.get('latest') else print('Up to date')
''')


def main():
    import workspace_app_updates as ups
    assert ups.news('Codex','0.164.0',{'commands':['/review','/plan'],'models':['gpt-x']})=='New in Codex 0.164.0: 2 commands (/review, /plan); 1 model (gpt-x)'
    assert ups.added(['a','b'],['b','c','a','d'])==['c','d']
    with tempfile.TemporaryDirectory(prefix='aura-app-updates-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace';fake=base/'fake_app.py';fake.write_text(FAKE,encoding='utf-8');state=base/'app.json'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'),FAKE_APP_STATE=str(state))
        def app_state(**values):state.write_text(json.dumps(values),encoding='utf-8')
        app_state(banner='omp/18.18.6',version='18.18.6',latest='')
        from setup import setup
        import workspace_ui
        bid=setup(organization='Update studio')['business_id']
        agents=[{'id':'omp','name':'OMP','argv':[sys.executable,str(fake)]}]
        with workspace_scope(root),patch('workspace_ui.installed_agents',return_value=agents):
            app=workspace_ui.Workspace();app.preferences['connected_apps']={'omp':{'kind':'omp','model':'m-old'}}
            models={'models':[{'id':'m-old'},{'id':'m-two'}]}
            with patch.object(app,'agent_options',side_effect=lambda kind,refresh=False,profile=None:app.option_cache.setdefault(kind,json.loads(json.dumps(models)))):
                app.check_apps(force=True)
                saved=app.preferences['app_versions']['omp']
                assert saved['version']=='18.18.6' and saved['lists']['models']==['m-old','m-two'],'the first look records the version and what the app offers, quietly'
                assert not [n for n in app.preferences['notification_items'] if n['kind'].startswith('app')],'nothing to say on the first look'

                # The app updated itself: AURA checks it still works with it and says what is new, once.
                app_state(banner='omp/18.22.2',version='18.22.2',latest='');models['models']=[{'id':'m-two'},{'id':'m-three'}];app.option_cache.clear()
                with patch('workspace_agents.check_signin'):app.check_apps(force=True)
                new=[n for n in app.preferences['notification_items'] if n['kind']=='app_new']
                assert len(new)==1 and new[0]['title']=='New in OMP 18.22.2: 1 model (m-three)',new
                assert app.preferences['app_versions']['omp']['problems']==[] and not [n for n in app.preferences['notification_items'] if n['kind']=='app_problem']
                app.observe_app('omp','commands',['/plan','/review'])  # commands seen on the first request after the update
                app.observe_app('omp','commands',['/plan','/review','/goal'])
                assert len([n for n in app.preferences['notification_items'] if n['kind']=='app_new'])==1,'one note per version, kept up to date'

                # A saved choice naming a model the app no longer offers is said once, with where to fix it.
                retired=[n for n in app.preferences['notification_items'] if n['kind']=='retired']
                assert len(retired)==1 and retired[0]['title']=='OMP default uses m-old, which OMP no longer offers. Choose another model.',retired
                app.check_retired();assert len([n for n in app.preferences['notification_items'] if n['kind']=='retired'])==1

                # An update the app itself reports is offered once, through the app's own update command.
                app_state(banner='omp/18.22.2',version='18.22.2',latest='18.30.0')
                with patch('workspace_agents.check_signin'):app.check_apps(force=True);app.check_apps(force=True)
                offers=[n for n in app.preferences['notification_items'] if n['kind']=='app_update']
                assert len(offers)==1 and offers[0]['title']=='OMP 18.30.0 is available.' and offers[0]['item_id']=='omp',offers
                assert app.terminal_command('omp-update')[0][-1]=='update',"the button runs the app's own update"
                status=app.app_status()['apps'][0]
                assert status['version']=='18.22.2' and status['latest']=='18.30.0' and status['update']=='omp-update'

                # After an update that breaks what AURA relies on, one plain line says what.
                app_state(banner='omp/19.0.0',version='19.0.0',latest='');models['models']=[];app.option_cache.clear()
                with patch('workspace_agents.check_signin',side_effect=ValueError('no')):app.check_apps(force=True)
                problem=[n for n in app.preferences['notification_items'] if n['kind']=='app_problem']
                assert len(problem)==1 and problem[0]['title']=="OMP updated to 19.0.0, and AURA can't list its models or reach it yet.",problem

        # An app that is gone is named plainly, with the way forward.
        with workspace_scope(root),patch('workspace_ui.installed_agents',return_value=[]):
            assert app.missing_app('codex')=="codex isn't installed on this computer anymore. Reinstall it, or continue this chat in another app."
    print('App updates passed: versions read, checks after an update, what is new, offered updates, retired models, missing apps.')


if __name__=='__main__':main()
