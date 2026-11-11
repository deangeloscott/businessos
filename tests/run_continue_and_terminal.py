"""Continue in another app and the built-in terminal: real terminals, honest handoffs, verified imports, linked chats."""
import json,os,sys,tempfile,textwrap,threading,time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import workspace_scope
from setup import setup
import workspace_ui
import workspace_context
import workspace_terminal as terminals


def rejects(fn,words=''):
    try:fn()
    except ValueError as error:
        assert words in str(error),str(error);return
    raise AssertionError('An invalid request was accepted')


FAKE_IMPORTER=textwrap.dedent('''
    import json,os,sys,time
    # Stands in for an app's interactive importer: shows a list, takes the typed chat ID, writes its copy, closes on Ctrl+D.
    print("Pick a chat to import   [enter select]",flush=True)
    typed=""
    while not typed.endswith("\\n") and not typed.endswith("\\r"):
        ch=sys.stdin.read(1)
        if not ch:sys.exit(1)
        typed+=ch
    source=typed.strip()
    folder=os.environ["FAKE_SESSIONS"];os.makedirs(folder,exist_ok=True)
    ident="omp-copy-"+source[:8]
    with open(os.path.join(folder,ident+".jsonl"),"w",encoding="utf-8") as f:
        f.write(json.dumps({"type":"session","id":ident,"cwd":os.getcwd()})+"\\n")
        f.write(json.dumps({"type":"custom","customType":"foreign_session_import","data":{"source":"codex","sourceId":source}})+"\\n")
    print("Imported "+source,flush=True)
    while True:
        ch=sys.stdin.read(1)
        if not ch or ch=="\\x04":break
''')


def main():
    # A real terminal on this computer: start, type, read, resize, exit.
    assert terminals.available(),'This computer should support built-in terminals'
    pool=terminals.Terminals()
    echo=pool.start([sys.executable,'-c','import sys;print("ready",flush=True);print("got",sys.stdin.readline().strip(),flush=True)'],str(ROOT),cols=90,rows=20)
    assert terminals.wait_for(echo,r'ready',20),echo.screen()
    echo.write('hello\r');assert terminals.wait_for(echo,r'got hello',20),echo.screen()
    echo.resize(120,40);assert (echo.cols,echo.rows)==(120,40)
    end=time.monotonic()+20
    while echo.alive and time.monotonic()<end:echo.output(echo.offset,.5)
    assert not echo.alive and echo.exit_code==0,(echo.alive,echo.exit_code)
    rejects(lambda:echo.write('more'),'ended')
    out=echo.output(0,0);assert 'got hello' in terminals.plain(out['data']) and not out['alive']
    assert terminals.plain('\x1b[31mred\x1b[0m line\r\nnext\rover')=='red line\nover',terminals.plain('\x1b[31mred\x1b[0m line\r\nnext\rover')
    rejects(lambda:pool.start(None,str(ROOT/'missing-folder')),'unavailable')
    rejects(lambda:pool.get('nope'),'no longer available')
    with patch.object(terminals,'MAX_TERMINALS',1):
        held=pool.start([sys.executable,'-c','import time;time.sleep(30)'],str(ROOT))
        rejects(lambda:pool.start([sys.executable,'-c','pass'],str(ROOT)),'Close a terminal')
        pool.remove(held.id)
    # One waiting connection serves every terminal: it returns as soon as any of them has output.
    first=pool.start([sys.executable,'-c','import sys;print("one",flush=True);sys.stdin.readline();print("later",flush=True)'],str(ROOT))
    second=pool.start([sys.executable,'-c','import time;time.sleep(30)'],str(ROOT))
    assert terminals.wait_for(first,r'one',20)
    quiet=pool.output_many({first.id:first.offset,second.id:second.offset},0)
    assert quiet['items']==[],quiet
    threading.Timer(.8,lambda:first.write('go'+chr(13))).start()
    began=time.monotonic();woke=pool.output_many({first.id:first.offset,second.id:second.offset,'gone-id':0},10)
    by={i['id']:i for i in woke['items']}
    assert by['gone-id']=={'id':'gone-id','gone':True},woke
    woke=pool.output_many({first.id:first.offset,second.id:second.offset},10)
    assert first.id in {i['id'] for i in woke['items']} and second.id not in {i['id'] for i in woke['items']},woke
    assert time.monotonic()-began<10,'a change in one terminal must wake the shared wait'
    pool.stop_all()

    with tempfile.TemporaryDirectory(prefix='aura-continue-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace';sessions=base/'omp-sessions';project=base/'repo';project.mkdir()
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'),
                          PI_CODING_AGENT_DIR=str(sessions.parent/'omp-home'),FAKE_SESSIONS=str(base/'omp-home'/'sessions'))
        bid=setup(organization='Continue studio')['business_id']
        importer=base/'fake_importer.py';importer.write_text(FAKE_IMPORTER,encoding='utf-8')
        agents=[{'id':'codex','argv':[sys.executable,'-c','pass']},{'id':'omp','argv':[sys.executable,str(importer)]},{'id':'claude','argv':[sys.executable,'-c','pass']}]
        with workspace_scope(root),patch('workspace_ui.installed_agents',return_value=agents):
            app=workspace_ui.Workspace()
            app.preferences['connected_apps']={k:{'kind':k,'model':'m-'+k,'effort':''} for k in ('codex','omp','claude')}
            source={'id':'chat-codex','business_id':bid,'agent':'codex','title':'Find missing projects','native_id':'01a1c14d-5a6c-74b2-b32c-55c64fde402a',
                    'workspace':str(root.resolve()),'native_workspace':str(project),'model':'gpt-x','summary':'Projects exist in the database but the sidebar is empty.','created':time.time()}
            app.preferences['chats']=[source]
            display=app.chat_display_path(source['id']);display.parent.mkdir(parents=True,exist_ok=True)
            display.write_text(json.dumps([{'role':'user','text':'Where did my projects go?'},{'role':'assistant','text':'They are in state_5.sqlite.'},
                                           {'role':'user','text':'Keep this chat’s cache warm.'},{'role':'assistant','text':'ok'},
                                           {'role':'user','text':'Did the other fix work?'},{'role':'assistant','text':'Only partly: the wrong branch was repaired.'},
                                           {'role':'user','text':'Try again'},{'role':'assistant','text':'','status':'error'}]),encoding='utf-8')

            # The handoff carries where it stands and the latest exchanges, oldest first, and asks for a check before acting.
            brief=workspace_context.handoff_brief(app,bid,source['id'])['text']
            assert 'Codex (gpt-x)' in brief and 'Where it stands: Projects exist' in brief and 'cache warm' not in brief
            assert brief.index('Where did my projects go?')<brief.index('Did the other fix work?')<brief.index('Try again')
            assert '(no finished reply)' in brief and 'check the current state yourself' in brief
            resolved=workspace_context.resolve(app,bid,[{'kind':'handoff','id':source['id']}])
            assert resolved['references'][0]['label']=='Continued from Find missing projects' and 'Only partly' in resolved['text']
            rejects(lambda:workspace_context.references([{'kind':'terminal','id':'x'}]),'context reference')

            # Options: OMP can take the full conversation from Codex; other apps get a handoff.
            codex_home=base/'codex-home'/'sessions'/'2026'/'11'/'10';codex_home.mkdir(parents=True)
            (codex_home/f'rollout-x-{source["native_id"]}.jsonl').write_text('x'*40000,encoding='utf-8')
            os.environ['CODEX_HOME']=str(base/'codex-home')
            options=app.continue_options(bid,source['id'])
            by={a['id']:a for a in options['apps']}
            assert set(by)=={'omp','claude'} and by['omp']['method']=='import' and by['claude']['method']=='handoff'
            assert 'About 10,000 tokens' in by['omp']['cost'] and 'Private reasoning stays with Codex' in by['omp']['carries'] and by['claude']['cost']=='Nothing extra.'
            assert options['apps'][0]['id']=='omp' and 'copied into the other app' in options['privacy'] and not options['busy']

            # Handoff: a new chat with the carried context, the original folder, and links both ways. Same app and busy chats are refused.
            captured={}
            def fake_start(bid_,text,history,**kw):
                captured.update(kw,text=text);chat={'id':'chat-new','business_id':bid,'agent':kw['connection']['kind'],'title':'New','workspace':str(root.resolve())}
                app.preferences['chats'].append(chat);return {'chat_id':'chat-new'}
            with patch.object(app,'start_chat',side_effect=fake_start):
                rejects(lambda:app.continue_elsewhere(bid,source['id'],'Go','codex'),'already in that app')
                source['status']='working';rejects(lambda:app.continue_elsewhere(bid,source['id'],'Go','claude'),'still working');source['status']='complete'
                started=app.continue_elsewhere(bid,source['id'],'Continue this work.','claude')
            assert started['chat_id']=='chat-new' and captured['references']==[{'kind':'handoff','id':source['id']}] and captured['native_workspace']==str(project)
            new=next(c for c in app.preferences['chats'] if c['id']=='chat-new')
            assert source['continued_to']['chat_id']=='chat-new' and source['continued_to']['method']=='handoff'
            assert new['continued_from']=={**new['continued_from'],'chat_id':source['id'],'agent':'codex','title':'Find missing projects'}

            # Full conversation: the importer runs in a real terminal, AURA types the exact ID, verifies the copy and links it.
            linked={}
            def fake_add(bid_,kind,ident=None,add=False):
                assert add and kind=='omp';linked['ident']=ident
                chat={'id':'chat-omp','business_id':bid,'agent':'omp','native_id':ident,'title':'Imported','workspace':str(root.resolve())}
                app.preferences['chats'].append(chat);return {'id':'chat-omp'}
            with patch.object(app,'native_chats',side_effect=fake_add):
                job=app.import_continue(bid,source['id'],'omp')
                assert job['status']=='working' and terminals.TERMINALS.get(job['terminal_id']).cwd==str(project)
                end=time.monotonic()+60
                while workspace_ui.CONTINUE_JOBS[job['id']]['status']=='working' and time.monotonic()<end:time.sleep(.3)
                done=workspace_ui.CONTINUE_JOBS[job['id']]
            assert done['status']=='done' and done['new_chat_id']=='chat-omp',done
            assert linked['ident']=='omp-copy-01a1c14d' and source['continued_to']['chat_id']=='chat-omp' and source['continued_to']['method']=='import'
            assert not terminals.TERMINALS.get(job['terminal_id']).alive,'the importer must be closed before AURA continues the chat'
            # The copy is recognized only by the source ID the importer recorded.
            assert workspace_ui.imported_session('omp',dict(os.environ),source['native_id'],time.time()-60)=='omp-copy-01a1c14d'
            assert workspace_ui.imported_session('omp',dict(os.environ),'some-other-chat',time.time()-60) is None
            rejects(lambda:app.import_continue(bid,'chat-new','omp'),'cannot import')

            # Terminal output reaches the AI only when the person adds it to a chat, as plain text.
            shared=terminals.TERMINALS.start([sys.executable,'-c','print("\x1b[32mbuild failed: missing module\x1b[0m",flush=True)'],str(project))
            assert terminals.wait_for(shared,r'build failed',20)
            given=workspace_context.resolve(app,bid,[{'kind':'terminal','id':shared.id}])
            assert given['references'][0]['label']=='Terminal output' and 'build failed: missing module' in given['text'] and '' not in given['text'] and str(project) in given['text']
            terminals.TERMINALS.remove(shared.id)
            rejects(lambda:workspace_context.resolve(app,bid,[{'kind':'terminal','id':shared.id}]),'no longer available')

            # Catch-up: the linked chat gets what happened since, as an update to a conversation it already has; no new copy.
            options=app.continue_options(bid,'chat-omp')
            assert [l['chat_id'] for l in options['linked']]==[source['id']] and options['linked'][0]['method']=='catch_up'
            sent={}
            def fake_send(bid_,text,history,**kw):sent.update(kw,text=text);return {'chat_id':kw['chat_id']}
            with patch.object(app,'start_chat',side_effect=fake_send):
                rejects(lambda:app.catch_up(bid,'chat-omp','chat-unlinked','x'),'Choose a chat')
                display2=app.chat_display_path('chat-omp');display2.write_text(json.dumps([{'role':'user','text':'Move the catalog'},{'role':'assistant','text':'Moved; six projects show.'}]),encoding='utf-8')
                app.catch_up(bid,'chat-omp',source['id'],'Catch up.')
            assert sent['chat_id']==source['id'] and sent['references']==[{'kind':'handoff','id':'chat-omp','variant':'catch_up'}]
            assert source['caught_up_from']['chat_id']=='chat-omp' and 'continued_to' not in source
            omp_chat=next(c for c in app.preferences['chats'] if c['id']=='chat-omp')
            assert omp_chat['continued_to']=={**omp_chat['continued_to'],'chat_id':source['id'],'method':'catch_up'}
            caught=workspace_context.resolve(app,bid,[{'kind':'handoff','id':'chat-omp','variant':'catch_up'}])
            assert caught['references'][0]['label'].startswith('Caught up from') and 'it is new to you' in caught['text'] and 'Moved; six projects show.' in caught['text']
            assert app.terminal_command('claude-login')[0][-2:]==['auth','login'] and app.terminal_command('codex-login')[0][-1]=='login'

            # Plain terminals never receive AURA's saved keys; only named app commands run with that app's environment.
            assert app.terminal_command('shell')==(None,None)
            argv,env=app.terminal_command('omp-login');assert argv[-1]=='login' and env['BUSINESSOS_WORKSPACE']
            rejects(lambda:app.terminal_command('rm -rf /'),'offers')
        terminals.TERMINALS.stop_all()
    print('Continue and terminal passed: real terminals, handoff brief, options, links both ways, verified import through a real importer, safe environments.')


if __name__=='__main__':main()
