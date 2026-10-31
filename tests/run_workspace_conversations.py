"""Independent real processes, exact Stop ownership, and cross-workspace recovery."""
from pathlib import Path
import json, os, sys, tempfile, time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))


def until(check):
    end=time.monotonic()+20
    while time.monotonic()<end:
        if check():return
        time.sleep(.03)
    raise AssertionError('Timed out waiting for the isolated conversation fixture')


def main():
    from setup import setup
    from workspace_ui import Workspace
    from _common import workspace_scope,workspace_root
    prior=dict(os.environ)
    with tempfile.TemporaryDirectory(prefix='aura-conversations-') as tmp:
        base=Path(tmp);a=base/'A';b=base/'B'
        os.environ.update(BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),LOCALAPPDATA=str(base/'local'))
        for root in (a,b):
            os.environ['BUSINESSOS_WORKSPACE']=str(root)
            setup(organization='Shared identifier')
        bid='shared-identifier';os.environ['BUSINESSOS_WORKSPACE']=str(a)
        agent=base/'agent.py'
        agent.write_text('''import os,re,sys,time
from pathlib import Path
text=sys.stdin.read();name=re.search(r'TURN ([A-Z_]+)',text).group(1)
root=Path(os.environ['BUSINESSOS_WORKSPACE']);(root/('started_'+name)).write_text(text)
while not (root/('release_'+name)).exists():time.sleep(.03)
print('## Reply '+name+'\\n\\nWorkspace: '+str(root))
''',encoding='utf-8')
        app=Workspace(agent={'name':'Isolated process','argv':[sys.executable,'-u',str(agent)]},settings_file=base/'a.json')
        app.preferences['connection']={'kind':'configured','model':'original-model','effort':''}
        identities={r:(r/'instances'/bid/'context/business.json').read_bytes() for r in (a,b)}
        try:
            try:app.start_chat(bid,None,[],chat_id='');raise AssertionError('Empty request accepted')
            except ValueError:pass
            first=app.start_chat(bid,'TURN FIRST',[],chat_id='')
            second=app.start_chat(bid,'TURN SECOND',[],chat_id='')
            until(lambda:(a/'started_FIRST').exists() and (a/'started_SECOND').exists())
            assert len(app.running_jobs())==2 and not app.update_idle()
            try:app.start_chat(bid,'TURN DUPLICATE',[],chat_id=first['chat_id']);raise AssertionError('A second turn entered a working chat')
            except ValueError:pass
            active=app.conversation(bid,first['chat_id']);assert active['job']['id']==first['id'] and 'TURN FIRST' in active['messages'][0]['text']
            app.preferences['connection']['model']='later-model';app.agent={'name':'Changed selection','argv':[sys.executable,'-u',str(agent)]}
            app.open_workspace(b)
            assert len(app.running_jobs())==2
            try:app.find_job(first['id'],bid);raise AssertionError('Another folder could access the request')
            except ValueError:pass
            third=app.start_chat(bid,'TURN THIRD',[],chat_id='')
            until(lambda:(b/'started_THIRD').exists())
            app.open_workspace(a)
            assert any(c['id']==first['chat_id'] for c in app.preferences['chats'])
            app.stop_chat(bid,first['id'])
            until(lambda:app.jobs[first['id']]['status']=='stopped')
            assert app.jobs[second['id']]['status']=='working' and app.jobs[third['id']]['status']=='working'
            (a/'release_SECOND').touch();(b/'release_THIRD').touch()
            until(lambda:not app.running_jobs())
            with app.lock:pass  # Completion includes its saved display, not only the process exit.
            second_chat=app.conversation(bid,second['chat_id'])
            assert second_chat['messages'][-1]['model']=='original-model'
            assert second_chat['messages'][-1]['agent']=='Isolated process'
            assert 'Reply SECOND' in second_chat['messages'][-1]['text'] and str(a) in second_chat['messages'][-1]['text']
            assert not any(c['id']==third['chat_id'] for c in app.preferences['chats'])
            assert any(n['chat_id']==second['chat_id'] for n in app.notifications(bid)['items'])
            app.open_workspace(b)
            third_chat=app.conversation(bid,third['chat_id'])
            assert 'Reply THIRD' in third_chat['messages'][-1]['text'] and str(b) in third_chat['messages'][-1]['text']
            assert not any(c['id']==second['chat_id'] for c in app.preferences['chats'])
            app.profile({'display_name':'Taylor','accent':'clay','text_size':16})
            assert app.profile()['display_name']=='Taylor'
            assert app.profile({'reset':True})['display_name']=='Taylor'
            assert app.profile()['accent']=='forest'
            diagnostic=json.dumps(app.diagnostics())
            assert str(base) not in diagnostic and 'TURN THIRD' not in diagnostic and 'Taylor' not in diagnostic
            # A persisted working marker is not proof that this new process owns it.
            chat=next(c for c in app.preferences['chats'] if c['id']==third['chat_id']);chat['status']='working';app.save_preferences()
            restored=Workspace(agent=app.configured_agent,settings_file=app.settings_file)
            result=restored.conversation(bid,third['chat_id']);assert result['job'] is None and result['chat']['status']=='working'
            try:restored.start_chat(bid,'TURN RETRY',[],chat_id=third['chat_id']);raise AssertionError('An uncertain request retried automatically')
            except ValueError:pass
            for root,data in identities.items():assert (root/'instances'/bid/'context/business.json').read_bytes()==data
            with workspace_scope(a):assert Path(workspace_root())==a
            assert Path(workspace_root())==b
        finally:
            for execution in app.executions.values():execution.stop()
            until(lambda:not app.running_jobs())
            os.environ.clear();os.environ.update(prior)
    print('Conversation isolation passed: parallel processes, individual Stop, immutable routing, A/B/A navigation, recovery, profile and safe diagnostics.')


if __name__=='__main__':main()
