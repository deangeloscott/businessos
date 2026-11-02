"""Independent real processes, exact Stop ownership, and cross-workspace recovery."""
from pathlib import Path
import json, os, sys, tempfile, time, threading
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from unittest.mock import patch

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
            # Browsing uses the saved display; model changes stay in one idle chat.
            import workspace_ui as ui
            native={'id':'native-model-check','business_id':bid,'agent':'codex','native_id':'native-same','workspace':str(b),'title':'Model check','model':'first-model','effort':'low','status':'complete','created':time.time(),'updated':time.time()}
            app.preferences['chats'].append(native);app.preferences['active_chats'][bid]=native['id']
            app.option_cache['codex']={'models':[{'id':'first-model','efforts':['low'],'default_effort':'low'},{'id':'next-model','efforts':['high'],'default_effort':'high'}]}
            app.save_chat_turn(native,{'id':'saved','created':time.time(),'updated':time.time(),'reply':'Saved native display','status':'complete'},'Read this saved chat',final=True)
            defaults=dict(app.preferences['connection'])
            server=ThreadingHTTPServer(('127.0.0.1',0),ui.handler_for(app));worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            def call(path,data=None,expected=200):
                request=Request('http://127.0.0.1:'+str(server.server_port)+path,data=json.dumps(data).encode() if data is not None else None,headers={'X-Aura-Token':app.token,'X-Aura-Workspace':str(b),'Content-Type':'application/json'})
                try:
                    with urlopen(request) as response:assert response.status==expected;return json.load(response)
                except HTTPError as exc:
                    assert exc.code==expected,(exc.code,exc.read());return {}
            try:
                with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Codex fixture','argv':['fixture','exec','-']}]),patch('workspace_codex.history',side_effect=AssertionError('Browsing must not launch native metadata')):
                    opened=call('/api/chats/open',{'business':bid,'id':native['id']})
                    assert opened['messages'][-1]['text']=='Saved native display'
                    defaults=dict(app.preferences['connection'])
                    updated=call('/api/chats/model',{'business':bid,'id':native['id'],'kind':'codex','model':'next-model','effort':'high'})
                    assert updated['chat']['model']=='next-model' and updated['chat']['native_id']=='native-same'
                    assert updated['chat']['model_choice_pending'] and app.preferences['connection']==defaults
                    call('/api/chats/model',{'business':bid,'id':native['id'],'kind':'claude','model':'next-model','effort':'high'},400)
                    call('/api/chats/model',{'business':bid,'id':native['id'],'model':'next-model','effort':'invented'},400)
                    call('/api/chats/model',{'business':'wrong-business','id':native['id'],'model':'next-model','effort':'high'},400)
                    native['status']='working'
                    call('/api/chats/model',{'business':bid,'id':native['id'],'model':'next-model','effort':'high'},400)
                    native.update(status='complete',agent='hermes')
                    call('/api/chats/model',{'business':bid,'id':native['id'],'model':'next-model','effort':'high'},400)
                    native['agent']='codex'
                with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Codex fixture','argv':['fixture','exec','-']}]),patch('workspace_codex.history',return_value={'messages':[{'role':'assistant','text':'Native refreshed display'}],'model':'first-model','effort':'low'}) as history:
                    fresh=call('/api/conversation?business='+bid+'&chat_id='+native['id']+'&refresh=1')
                    assert history.call_count==1 and fresh['messages'][0]['text']=='Native refreshed display'
                    assert fresh['chat']['model']=='next-model','Native metadata must not overwrite a pending next-turn model'
                    cached=call('/api/conversation?business='+bid+'&chat_id='+native['id'])
                    assert history.call_count==1 and cached['messages'][0]['text']=='Native refreshed display'
                # Slow native history must not lock the UI or replace a newer choice.
                entered=threading.Event();release=threading.Event();results=[];errors=[]
                def slow_conversation(*args):
                    entered.set();assert release.wait(10)
                    return {'messages':[{'role':'assistant','text':'Stale native display'}],'model':'first-model','usage':{'input_tokens':1}}
                def refresh_conversation():
                    try:results.append(call('/api/conversation?business='+bid+'&chat_id='+native['id']+'&refresh=1'))
                    except Exception as exc:errors.append(exc)
                with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Codex fixture','argv':['fixture','exec','-']}]),patch('workspace_codex.history',side_effect=slow_conversation):
                    reader=threading.Thread(target=refresh_conversation);reader.start()
                    try:
                        assert entered.wait(10)
                        start=time.monotonic()
                        call('/api/chats/model',{'business':bid,'id':native['id'],'model':'first-model','effort':'low'})
                        assert time.monotonic()-start<1,'Native history held the UI lock'
                        release.set();reader.join(10)
                        assert not reader.is_alive() and not errors,errors
                        assert results[0]['chat']['model']=='first-model'
                        assert results[0]['messages'][0]['text']=='Native refreshed display','Stale history replaced the saved display'
                        assert not app.preferences.get('usage_chats',{}).get(native['id']),'Stale usage was committed'
                    finally:release.set();reader.join(15)
                with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Codex fixture','argv':['fixture','exec','-']}]),patch('workspace_codex.history',return_value={'messages':[{'role':'assistant','text':'Fresh display'}],'usage':{'input_tokens':100}}):
                    call('/api/conversation?business='+bid+'&chat_id='+native['id']+'&refresh=1')
                    assert json.loads(app.settings_file.read_text(encoding='utf-8'))['usage_chats'][native['id']]['input_tokens']==100,'Native usage was not persisted'
                # Native discovery/import is explicit, bounded and uses the same saved session.
                native_store=base/'native-sessions';native_store.mkdir()
                rows=[]
                for i in range(7):
                    path=native_store/('native-recent-'+str(i)+'.jsonl')
                    path.write_text(json.dumps({'type':'session_meta','payload':{'id':'native-recent-'+str(i),'cwd':str(b)}})+'\n',encoding='utf-8')
                    rows.append({'id':'native-recent-'+str(i),'preview':'Native idea '+str(i),'cwd':str(b),'path':str(path),'updatedAt':time.time()})
                def native_catalog(command,calls,cwd,env):return calls(lambda method,params:{'data':rows,'nextCursor':None})
                def native_history(command,cwd,ident):
                    path=native_store/(ident+'.jsonl');return {'native_id':ident,'title':'Native idea','summary':'A native summary','model':'next-model','effort':'high','source_file':str(path),'native_workspace':str(b),'messages':[{'role':'assistant','text':'Changed outside' if path.stat().st_size>150 else 'Original native reply'}],'usage':{'input_tokens':50}}
                with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Codex fixture','argv':['fixture','exec','-']}]),patch('workspace_native_chats.storage',return_value=native_store),patch('workspace_codex.rpc',side_effect=native_catalog),patch('workspace_codex.history',side_effect=native_history) as history:
                    found=call('/api/chats/native?business='+bid+'&kind=codex');assert len(found['items'])==5
                    active_before=dict(app.preferences['active_chats']);count_before=len(app.preferences['chats'])
                    preview=call('/api/chats/native?business='+bid+'&kind=codex&id=native-recent-0')
                    assert preview['title']=='Native idea' and len(app.preferences['chats'])==count_before and app.preferences['active_chats']==active_before
                    call('/api/chats/import',{'business':bid,'kind':'codex','id':'native-recent-0'},400)
                    added=call('/api/chats/import',{'business':bid,'kind':'codex','id':'native-recent-0','confirmed':True})
                    assert call('/api/chats/import',{'business':bid,'kind':'codex','id':'native-recent-0','confirmed':True})==added
                    assert app.preferences['active_chats']==active_before and len(app.preferences['chats'])==count_before+1
                    assert not any(r['native_id']=='native-recent-0' for r in call('/api/chats/native?business='+bid+'&kind=codex')['items'])
                    calls_before=history.call_count
                    assert not call('/api/chats/changes?business='+bid+'&id='+added['id'])['changed'] and history.call_count==calls_before
                    path=native_store/'native-recent-0.jsonl';path.write_text(path.read_text()+' '*250,encoding='utf-8')
                    change=call('/api/chats/changes?business='+bid+'&id='+added['id'])
                    assert change['changed'] and change['conversation']['messages'][0]['text']=='Changed outside'
                    assert not call('/api/chats/changes?business='+bid+'&id='+added['id'])['changed']
                    def own_turn(*args):
                        path.write_text(path.read_text()+' '*50,encoding='utf-8')
                        return {'native_id':'native-recent-0','reply':'Owned reply','usage':{}}
                    with patch('workspace_codex.run',side_effect=own_turn):
                        owned=app.start_chat(bid,'Continue this imported session',[],chat_id=added['id'])
                        until(lambda:app.jobs[owned['id']]['status']=='complete')
                        with app.lock:pass
                    calls_before=history.call_count
                    assert not call('/api/chats/changes?business='+bid+'&id='+added['id'])['changed'] and history.call_count==calls_before,'Aura-owned completion caused a redundant native refresh'
                    call('/api/chats/native?business='+bid+'&kind=codex&id=../private',expected=400)
                # Preparing personalization is metadata-only and reuses one scoped chat.
                app.preferences['connected_apps']['configured']={'kind':'configured','model':'','effort':''}
                connection={'kind':'configured','model':'','effort':''}
                active_before=dict(app.preferences['active_chats']);jobs_before=set(app.jobs)
                custom=call('/api/chats/personalization',{'business':bid,'connection':connection})
                again=call('/api/chats/personalization',{'business':bid,'connection':connection})
                assert custom==again and set(app.jobs)==jobs_before
                assert app.preferences['active_chats']==active_before,'Preparing must not redirect an existing chat'
                target=next(c for c in app.preferences['chats'] if c['id']==custom['id'])
                assert target['purpose']=='personalization' and target['title_edited'] and target['native_id'] is None
                assert target['workspace']==str(b) and target['business_id']==bid
                assert call('/api/chats/open',{'business':bid,'id':custom['id']})['messages']==[]
                restarted=Workspace(agent=app.configured_agent,settings_file=app.settings_file)
                assert restarted.personalization_chat(bid,connection)==custom
                fourth=call('/api/chat',{'business':bid,'chat_id':'','text':'TURN FOURTH','history':[],'connection':connection},202)
                until(lambda:(b/'started_FOURTH').exists())
                assert call('/api/chats/personalization',{'business':bid,'connection':connection})==custom
                assert app.preferences['active_chats'][bid]==fourth['chat_id'] and app.jobs[fourth['id']]['status']=='working'
                (b/'release_FOURTH').touch();until(lambda:app.jobs[fourth['id']]['status']!='working')
                with app.lock:pass
                call('/api/chats/personalization',{'business':'wrong-business','connection':connection},400)
                app.open_workspace(a)
                other=app.personalization_chat(bid,connection)
                assert other['id']!=custom['id'],'Separate workspace folders keep separate personalization histories'
                app.open_workspace(b)
                # Slow usage refresh survives A/B/A and cannot replace a newer turn.
                from _common import workspace_root as scoped_root
                entered=threading.Event();inspect=threading.Event();checked=threading.Event();release=threading.Event();usage_results=[];usage_errors=[];account_calls=[]
                native.update(status='complete',updated=time.time(),model='next-model',effort='high')
                app.preferences['active_chats'][bid]=native['id']
                app.preferences['connected_apps']['codex']={'kind':'codex','model':'next-model','effort':'high'}
                app.preferences['usage_chats'][native['id']]={'input_tokens':100,'output_tokens':10}
                app.usage_refresh['checked']=0
                def metadata(command,calls,cwd,env):
                    assert Path(cwd)==b;account_calls.append(True)
                    return calls(lambda method,params:{'account':None})
                def slow_history(*args):
                    entered.set();assert inspect.wait(10)
                    assert Path(scoped_root())==b and Path(args[1])==b
                    checked.set();assert release.wait(15)
                    return {'usage':{'input_tokens':1,'output_tokens':1}}
                def refresh_usage():
                    try:usage_results.append(app.usage(bid,refresh=True))
                    except Exception as exc:usage_errors.append(exc)
                with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Codex fixture','argv':['fixture','exec','-']}]),patch('workspace_codex.rpc',side_effect=metadata),patch('workspace_codex.history',side_effect=slow_history),patch('workspace_codex.run',return_value={'reply':'Newer reply','usage':{'input_tokens':900,'output_tokens':60}}):
                    reader=threading.Thread(target=refresh_usage);reader.start()
                    try:
                        assert entered.wait(10)
                        start=time.monotonic();cached=app.usage(bid,refresh=True)
                        assert time.monotonic()-start<1 and cached['refreshing'] and len(account_calls)==1,'Cached usage blocked or started a duplicate native refresh'
                        app.open_workspace(a);inspect.set();assert checked.wait(10)
                        app.open_workspace(b)
                        newer=app.start_chat(bid,'A newer native turn',[],chat_id=native['id'])
                        until(lambda:app.jobs[newer['id']]['status']=='complete')
                        with app.lock:pass
                        release.set();reader.join(15)
                        assert not reader.is_alive() and not usage_errors,usage_errors
                        assert usage_results[0]['workspace']==str(b) and usage_results[0]['chat']['input_tokens']==1000
                        assert app.preferences['usage_chats'][native['id']]['input_tokens']==1000,'Late history replaced newer usage'
                        assert native['id'] not in app.workspace_views[str(a)]['preferences'].get('usage_chats',{})
                        app.usage(bid,refresh=True);assert len(account_calls)==1,'Cooldown was lost through A/B/A'
                    finally:inspect.set();release.set();reader.join(20)
                # Stopping a Hermes transport does not claim its gateway stopped.
                from workspace_execution import Stopped
                hermes=dict(native,id='hermes-stop-check',agent='hermes',status='complete',model='first-model',effort='low')
                app.preferences['chats'].append(hermes);app.preferences['connected_apps']['hermes']={'kind':'hermes','model':'first-model','effort':'low'}
                with patch('workspace_ui.installed_agents',return_value=[{'id':'hermes','name':'Hermes fixture','argv':['fixture','chat','--print']}]),patch('workspace_agents.run',side_effect=Stopped()):
                    stopped=app.start_chat(bid,'A request with uncertain gateway outcome',[],chat_id=hermes['id'])
                    until(lambda:app.jobs[stopped['id']]['status']=='stopped')
                    with app.lock:pass
                    assert hermes['status']=='working' and app.jobs[stopped['id']]['stop_note']
                    call('/api/chats/recover',{'business':bid,'id':hermes['id']})
                    assert hermes['status']=='stopped'
                call('/api/profile',{'avatar':'data:image/svg+xml;base64,PHN2Zz48L3N2Zz4='},400)
                with urlopen('http://127.0.0.1:'+str(server.server_port)) as response:assert 'img-src' in response.headers['Content-Security-Policy'] and 'data:' in response.headers['Content-Security-Policy']
            finally:server.shutdown();server.server_close();worker.join()
            for root,data in identities.items():assert (root/'instances'/bid/'context/business.json').read_bytes()==data
            with workspace_scope(a):assert Path(workspace_root())==a
            assert Path(workspace_root())==b
        finally:
            for execution in app.executions.values():execution.stop()
            until(lambda:not app.running_jobs())
            os.environ.clear();os.environ.update(prior)
    print('Conversation isolation passed: parallel processes, individual Stop, immutable routing, A/B/A navigation, recovery, cached browsing, per-chat models, profile and safe diagnostics.')


if __name__=='__main__':main()
