"""Hermes messages: your phone chats with Hermes appear in AURA once, in the business you chose; chats from anyone
else stay for you to add; an open phone chat updates from Hermes's records; one message at a time while Hermes is
answering the phone; notices go to your phone only while you're away, through Hermes's own send command. Also the
small helpers that came with it: screen-control tools, where each app keeps its conversations, and the other apps."""
import json,os,sqlite3,sys,tempfile,textwrap,time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import workspace_scope

FAKE=textwrap.dedent('''
    import json,os,sqlite3,sys
    args=sys.argv[1:]
    if args[:1]==['send']:
        open(os.environ['FAKE_SENT'],'a',encoding='utf-8').write(json.dumps(args)+'\\n')
    elif args[:2]==['sessions','export']:
        ident=args[args.index('--session-id')+1]
        db=sqlite3.connect(os.path.join(os.environ['HERMES_HOME'],'state.db'))
        rows=db.execute('select role,content from messages where session_id=? order by id',(ident,)).fetchall()
        title=(db.execute('select title from sessions where id=?',(ident,)).fetchone() or [''])[0]
        print(json.dumps({'id':ident,'title':title,'messages':[{'role':r,'content':c} for r,c in rows]}))
''')


def database(home):
    db=sqlite3.connect(home/'state.db')
    db.executescript('''create table sessions(id text primary key,source text,user_id text,chat_id text,chat_type text,display_name text,title text,
        started_at real,last_activity_at real,thread_id text,parent_session_id text,end_reason text,hidden integer,archived integer);
        create table messages(id integer primary key autoincrement,session_id text,role text,content text,timestamp real);''')
    return db


def main():
    import workspace_hermes_messages as hm,workspace_chats
    assert workspace_chats.uses_screen('mcp__computer-use__left_click') and workspace_chats.uses_screen('computer')
    assert not workspace_chats.uses_screen('browser_take_screenshot') and not workspace_chats.uses_screen('Bash'),'a browser the tool runs itself is not your screen'
    with tempfile.TemporaryDirectory(prefix='aura-hermes-messages-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace';home=base/'hermes';home.mkdir();fake=base/'fake_hermes.py';fake.write_text(FAKE,encoding='utf-8');sent=base/'sent.jsonl'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'),HERMES_HOME=str(home),FAKE_SENT=str(sent))
        (home/'config.yaml').write_text("platforms:\n  telegram:\n    enabled: true\n    home_channel: {platform: telegram, chat_id: '42', user_id: '42'}\n",encoding='utf-8')
        (home/'gateway_state.json').write_text(json.dumps({'pid':os.getpid(),'gateway_state':'running','platforms':{'telegram':{'state':'connected'}}}),encoding='utf-8')
        db=database(home);now=time.time()
        try:run(base,root,home,fake,sent,db,now,hm)
        finally:db.close()
    print('Hermes messages passed: your phone chats come in once, live updates, one sender at a time, notices only while away.')


def run(base,root,home,fake,sent,db,now,hm):
    db.executemany('insert into sessions values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[
        ('mine','telegram','42','42','dm','Dee','Weekly numbers',now-60,now-50,None,None,None,0,0),
        ('other','telegram','77','77','dm','Sam','Hello bot',now-60,now-40,None,None,None,0,0),
        ('desk','tui',None,None,None,None,'At the computer',now-60,now-30,None,None,None,0,0),
        ('mine2','telegram','42','42','dm','Dee','',now-30,now-20,None,'mine',None,0,0)])
    db.execute("update sessions set end_reason='compression' where id='mine'")
    db.executemany('insert into messages(session_id,role,content,timestamp) values (?,?,?,?)',[
        ('mine','user','How did last week go?',now-60),('mine','assistant','Sales were up 4%.',now-55),('other','user','hi',now-40)])
    db.commit()

    found={c['id']:c for c in hm.conversations(since=0)}
    assert set(found)=={'mine','other'},'phone conversations only; a compressed continuation is the same conversation'
    assert found['mine']['yours'] and not found['other']['yours'] and found['other']['sender']=='Sam' and found['mine']['from']=='Telegram'
    assert hm.gateway()=={'set_up':True,'running':True,'platforms':[{'id':'telegram','name':'Telegram','state':'connected','problem':False}],'home':'telegram'}
    assert hm.marker(None,'mine')[0]=='mine2','the change mark follows the conversation to where Hermes continued it'

    from setup import setup
    import workspace_ui
    bid=setup(organization='Phone studio')['business_id']
    agents=[{'id':'hermes','name':'Hermes','argv':[sys.executable,str(fake)]},{'id':'codex','name':'Codex','argv':[sys.executable,'-c','']}]
    with workspace_scope(root),patch('workspace_ui.installed_agents',return_value=agents):
        app=workspace_ui.Workspace()
        assert app.hermes_messages_status()['chats']=={}
        app.hermes_messages_settings({'chats':bid})  # starts a check straight away
        with app.hermes_check_lock:pass
        app.check_hermes_messages();app.check_hermes_messages()
        phone=[c for c in app.preferences['chats'] if c.get('gateway')]
        assert len(phone)==1 and phone[0]['native_id']=='mine' and phone[0]['gateway']=='Telegram' and phone[0]['business_id']==bid,'your chat, once, in the chosen business'
        notes=[n for n in app.preferences['notification_items'] if n['kind']=='phone_chat']
        assert len(notes)==1 and notes[0]['title']=='New chat from Telegram: Weekly numbers' and notes[0]['chat_id']==phone[0]['id']
        assert not any(c.get('native_id')=='other' for c in app.preferences['chats']),"someone else's chat waits in Add existing"

        # A new phone message shows up in the open chat; nothing is re-read until Hermes's records change.
        assert app.conversation_changes(bid,phone[0]['id'])['changed'] is False
        db.execute("insert into messages(session_id,role,content,timestamp) values ('mine2','user','And this week?',?)",(time.time(),));db.commit()
        assert app.conversation_changes(bid,phone[0]['id'])['changed'] is True
        assert app.conversation_changes(bid,phone[0]['id'])['changed'] is False
        # While Hermes answers that phone message, AURA's send waits for it.
        try:app.start_chat(bid,'Also add costs',[],chat_id=phone[0]['id']);raise AssertionError('expected a wait')
        except ValueError as error:assert str(error)=="Hermes is still answering your Telegram message. Send again when it's done."
        db.execute("insert into messages(session_id,role,content,timestamp) values ('mine2','assistant','Up 6%.',?)",(time.time(),));db.commit()
        assert not app.hermes_answering(phone[0])

        # Notices: only while you're away, only the three kinds, once each, through Hermes's own send.
        app.hermes_messages_settings({'phone':True})
        stamp=time.time()-60
        app.preferences['notification_items']+=[{'id':'j1','business_id':bid,'chat_id':phone[0]['id'],'agent':'Hermes','status':'complete','at':stamp,'read':False,'delivered':False},
            {'id':'s1','business_id':bid,'chat_id':None,'kind':'saved','title':'Saved a file','status':'complete','at':stamp,'read':False,'delivered':False}]
        app.preferences['phone_notices']['since']=stamp-1
        app.ui_active_at=time.time();app.send_phone_notices()
        assert not sent.exists(),'nothing while you are at AURA'
        app.ui_active_at=0;app.send_phone_notices();app.send_phone_notices()
        lines=[json.loads(x) for x in sent.read_text(encoding='utf-8').splitlines()]
        assert lines==[['send','-t','telegram','-q','AURA · Phone studio: Finished · Weekly numbers']],lines
        # Many at once: a few, then the rest as one line; none silently dropped. Work from before you left stays here.
        app.ui_active_at=time.time()-900;app.preferences['phone_notices']['since']=0
        app.preferences['notification_items']+=[{'id':f'm{i}','business_id':bid,'chat_id':phone[0]['id'],'agent':'Hermes','status':'complete','at':time.time()-(1000 if i==5 else 300),'read':False,'delivered':False} for i in range(6)]
        sent.unlink();app.send_phone_notices()
        lines=[json.loads(x)[-1] for x in sent.read_text(encoding='utf-8').splitlines()]
        assert len(lines)==3 and lines[-1]=='AURA: 3 more updates. Open AURA to see them.',lines
        assert [n['id'] for n in app.preferences['notification_items'] if n['id'].startswith('m') and not n.get('phone')]==['m5']
        # How long away is your choice (10 minutes unless you change it), and a plan limit reaches you too.
        try:app.hermes_messages_settings({'phone_after':7});raise AssertionError('expected a choice')
        except ValueError:pass
        app.preferences['notification_items'].append({'id':'l1','business_id':bid,'chat_id':phone[0]['id'],'kind':'limit','title':'Codex plan limit reached. Open the chat to choose how to continue.','status':'complete','at':time.time()-200,'read':False,'delivered':False})
        sent.unlink();app.ui_active_at=time.time()-400;app.send_phone_notices()
        assert not sent.exists(),'not yet: 10 minutes is the default'
        app.hermes_messages_settings({'phone_after':5});app.send_phone_notices()
        assert json.loads(sent.read_text(encoding='utf-8'))[-1]=='AURA · Phone studio: Plan limit · Codex plan limit reached. Open the chat to choose how to continue.'

        assert app.other_apps_line()=='Other AI apps on this computer: Hermes, Codex. The user can continue this chat in one of them. '
        assert {'app':'Hermes','folder':str(home)} in app.app_histories()
        app.hermes_messages_settings({'chats':'','phone':False})
        assert 'hermes_messages' not in app.preferences and 'phone_notices' not in app.preferences


if __name__=='__main__':main()
