"""Accounts and continuing at reset: the parts where a mistake would cost a working sign-in or repeat work."""
import base64
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
from subprocess import CompletedProcess

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def sign_in(account, email, refresh):
    claims = base64.urlsafe_b64encode(json.dumps({'email': email, 'https://api.openai.com/auth': {'chatgpt_plan_type': 'plus'}}).encode()).decode().rstrip('=')
    return json.dumps({'auth_mode': 'chatgpt', 'tokens': {'id_token': 'x.' + claims + '.y', 'access_token': 'a', 'refresh_token': refresh, 'account_id': account}})


def main():
    with tempfile.TemporaryDirectory() as td:
        os.environ['AURA_STATE_DIR'] = str(Path(td) / 'state')
        os.environ['CODEX_HOME'] = str(Path(td) / 'codex')
        home = Path(os.environ['CODEX_HOME']); home.mkdir()
        import workspace_accounts as accounts
        if os.name != 'nt':  # The OS keyring is not available in every CI; exercise the logic with a memory vault.
            store = {}
            accounts.Vault.read = lambda self: dict(store)
            accounts.Vault.write = lambda self, rows: (store.clear(), store.update(rows))
        auth = home / 'auth.json'

        auth.write_text(sign_in('acct-1', 'one@example.com', 'r1'), encoding='utf-8')
        first = accounts.codex_capture('Personal')
        assert first['email'] == 'one@example.com' and first['plan'] == 'plus'
        auth.write_text(sign_in('acct-2', 'two@example.com', 'r2'), encoding='utf-8')
        second = accounts.codex_capture('Work')
        assert {a['nickname'] for a in accounts.public('codex')['accounts']} == {'Personal', 'Work'}

        # Codex refreshes its sign-in in place; switching away must keep that newer sign-in.
        auth.write_text(sign_in('acct-2', 'two@example.com', 'r2-refreshed'), encoding='utf-8')
        accounts.codex_switch(first['id'])
        assert json.loads(auth.read_text(encoding='utf-8'))['tokens']['account_id'] == 'acct-1'
        accounts.codex_switch(second['id'])
        assert json.loads(auth.read_text(encoding='utf-8'))['tokens']['refresh_token'] == 'r2-refreshed', 'refreshed sign-in was lost'
        assert [a['nickname'] for a in accounts.public('codex')['accounts'] if a['active']] == ['Work']
        try:
            accounts.remove(second['id']); raise AssertionError('removed the account Codex is using')
        except ValueError:
            pass

        (home / 'config.toml').write_text('cli_auth_credentials_store = "keyring"\n', encoding='utf-8')
        assert accounts.codex_supported()[0] is False
        (home / 'config.toml').unlink()

        for bad in ({'mode': 'sometimes'}, {'resume': 'always'}, {'unknown': 'x'}):
            try:
                accounts.set_policy(bad); raise AssertionError(f'accepted {bad}')
            except ValueError:
                pass
        accounts.set_policy({'mode': 'auto', 'goals': 'ask'})
        assert accounts.mode_for('chats') == 'auto' and accounts.mode_for('goals') == 'ask'

        import workspace_resume as resume
        resume.add('biz', td, 'chat-1', time.time() - 120)
        resume.add('biz', td, 'chat-2', time.time() + 3600)
        assert [r['chat_id'] for r in resume.take_due(td)] == ['chat-1']
        assert resume.take_due(td) == [], 'a continue ran twice'
        assert resume.for_chat('chat-1')['status']=='needs_review', 'an uncertain launch must remain recoverable'
        resume.settle(resume.for_chat('chat-1')['id'])
        assert resume.for_chat('chat-2') and not resume.for_chat('chat-1')
        resume.cancel('chat-2',td,'biz')
        for result in (CompletedProcess([],1,stdout='',stderr='Sign-in failed'),
                       CompletedProcess([],0,stdout='{}'),CompletedProcess([],0,stdout='[]')):
            with patch.object(accounts.subprocess,'run',return_value=result),patch.object(accounts.Vault,'write') as saved:
                try:accounts.add_claude(['fixture'],'fixture-token-12345678901234567890')
                except ValueError:pass
                else:raise AssertionError('A failed or unrecognized token check was accepted')
                saved.assert_not_called()
        with patch.object(accounts.subprocess,'run',return_value=CompletedProcess([],0,stdout=json.dumps(
                {'type':'result','subtype':'success','is_error':False,'result':'OK'}))):
            assert accounts.add_claude(['fixture'],'fixture-token-12345678901234567890')['accounts']
        recovery_checks(Path(td))
    print('Accounts passed: Codex sign-in swap keeps refreshed sign-ins, keyring refusal, settings validation, and continue-at-reset runs once.')


def recovery_checks(root):
    """Recovery keeps its owner and current intent, and never becomes a retry loop."""
    from setup import setup
    from _common import workspace_scope,workspace_root
    from workspace_ui import Workspace,SETUP_ERRORS
    import workspace_resume as resume,workspace_goals as goals,workspace_schedules as schedules
    a=root/'workspace-a';b=root/'workspace-b'
    with patch.dict(os.environ,{'BUSINESSOS_WORKSPACE_CONFIG':str(root/'pointer.json')}),patch.object(Workspace,'glance',return_value={'limits':None}):
        bid_a=setup(workspace=a,organization='Workspace A',run_doctor=False,write_link=False,allow_state_switch=True)['business_id']
        app_a=Workspace(agent={'name':'Fixture','argv':[sys.executable,'-c',"print('Done')"]})
        bid_b=setup(workspace=b,organization='Workspace B',run_doctor=False,write_link=False,allow_state_switch=True)['business_id']
        app_b=Workspace(agent={'name':'Fixture','argv':[sys.executable,'-c',"print('Done')"]})
        app_b.workspace_views[str(a.resolve())]=app_a.__dict__
        app_a.jobs=app_b.jobs;app_a.executions=app_b.executions
        app_a.preferences['connected_apps']['configured']={'kind':'configured','model':'','effort':''}
        task={'id':'task-a','name':'Work for A','app':'Fixture','owner':'configured','workspace':str(a),'description':'Produce A output'}
        calls=[]
        def start(owner,bid,text,history,**kw):
            calls.append((bid,str(workspace_root()),text,kw));return {'id':'request-new','chat_id':'new-chat'}
        with patch.object(schedules,'inventory',return_value={'items':[task]}),patch.object(Workspace,'start_chat',start):
            result=app_b.task_recover(bid_b,'task-a','run')
            assert calls[-1][0:2]==(bid_a,str(a.resolve())) and result['workspace']==str(a.resolve())
            assert app_b.workspace_path==str(b.resolve()), 'background recovery moved the visible workspace'
            task.update(last_status='error',last_error=SETUP_ERRORS['limit'],last_run='fixture-run')
            app_b.check_task_limits();app_a.check_task_limits()
            notices=[n for n in app_a.preferences['notification_items'] if n.get('kind')=='task_limit']
            assert len(notices)==1 and notices[0]['business_id']==bid_a and notices[0]['task_id']=='task-a'
            assert not any(n.get('kind')=='task_limit' for n in app_b.preferences['notification_items'])
            task['workspace']=''
            try:app_b.task_recover(bid_b,'task-a','run')
            except ValueError as error:assert 'workspace' in str(error)
            else:raise AssertionError('Unknown task ownership guessed the visible workspace')
            app_b.task_recover(bid_b,'task-a','run',confirmed=True)
            assert calls[-1][0:2]==(bid_b,str(b.resolve()))
            task.update(owner='codex',workspace=str(a))
            app_a.preferences['connected_apps']['codex']={'model':'fixture','effort':'high'}
            app_a.preferences['chats'].append({'id':'busy-codex','business_id':bid_a,'agent':'codex','workspace':str(a)})
            app_a.jobs['busy']={'id':'busy','chat_id':'busy-codex','status':'working','workspace':str(a)}
            with patch('workspace_accounts.codex_switch') as swapped:
                try:app_b.task_recover(bid_b,'task-a','account','fixture-account')
                except ValueError as error:assert 'finish' in str(error)
                else:raise AssertionError('Task recovery switched an active Codex account')
                swapped.assert_not_called()
            app_a.jobs.clear()
        task.update(owner='configured',workspace=str(a))
        with patch.object(schedules,'inventory',return_value={'items':[task]}):
            started=app_b.task_recover(bid_b,'task-a','run')
            deadline=time.monotonic()+10
            while app_b.jobs[started['id']]['status']=='working' and time.monotonic()<deadline:time.sleep(.02)
            job=app_b.jobs[started['id']]
            assert job['status']=='complete' and job['business_id']==bid_a and job['workspace']==str(a.resolve()),job
            assert app_b.workspace_path==str(b.resolve())
        with workspace_scope(a):
            goal=goals.save(bid_a,{'name':'Finish this work','scope':'chat','chat_id':'resume-chat','status':'active'})
            chat={'id':'resume-chat','business_id':bid_a,'workspace':str(a.resolve()),'agent':'configured','title':'Work','status':'error',
                  'goal_id':goal['id'],'native_id':'native-fixture','updated':time.time(),'recovery':{'request_id':'failed-request','status':'error'}}
            app_a.preferences['chats'].append(chat)
            basis=app_a.resume_basis(bid_a,chat['id'])
            resume.add(bid_a,a,chat['id'],time.time()-120,basis=basis)
            app_a.jobs['busy']={'id':'busy','chat_id':chat['id'],'workspace':str(a),'status':'working'}
            with patch.object(Workspace,'start_chat',start):app_a.resume_due()
            assert resume.for_chat(chat['id'])['status']=='pending', 'busy continuation was lost'
            app_a.jobs.clear()
            goals.save(bid_a,{'id':goal['id'],'status':'completed'})
            # Make the deferred item due again; use the public queue write, not a second scheduler.
            resume.add(bid_a,a,chat['id'],time.time()-120,basis=basis)
            before=len(calls)
            with patch.object(Workspace,'start_chat',start):app_a.resume_due()
            assert len(calls)==before and resume.for_chat(chat['id'])['status']=='needs_review'
            resume.cancel(chat['id'],b,bid_b)
            assert resume.for_chat(chat['id']), 'another workspace cancelled this continuation'
            resume.cancel(chat['id'],a,bid_a)
            goals.save(bid_a,{'id':goal['id'],'status':'active'})
            basis=app_a.resume_basis(bid_a,chat['id'])
            resume.add(bid_a,a,chat['id'],time.time()-120,basis=basis)
            with patch.object(Workspace,'start_chat',start):app_b.resume_due()
            assert not resume.for_chat(chat['id']) and calls[-1][0:2]==(bid_a,str(a.resolve()))
            options={'app':'claude','accounts':[{'id':'other','nickname':'Other','used':None}],'backup_app':'','resume':'off'}
            before=len(calls)
            with patch('workspace_accounts.mode_for',return_value='auto'),patch.object(Workspace,'limit_options',return_value=options),\
                    patch.object(Workspace,'accounts_action'),patch.object(Workspace,'start_chat',start):
                app_a.after_limit(bid_a,chat['id'],'Perform an external action',request_id='failed-request')
                app_a.after_limit(bid_a,chat['id'],'Perform an external action',request_id='failed-request')
                app_a.after_limit(bid_a,chat['id'],'Perform an external action',request_id='failed-request',recovered=True)
                app_a.after_limit(bid_a,chat['id'],'Old request',request_id='obsolete-request')
            assert len(calls)==before+1 and calls[-1][3]['limit_recovery'] is True
            assert 'Perform an external action' not in calls[-1][2], 'fallback replayed the original action'
            resume.add(bid_a,a,'',time.time()+3600,app='configured',task_id='task-a')
            resume.add(bid_a,a,'',time.time()+7200,app='configured',task_id='task-a')
            tasks=[r for r in resume.pending() if r.get('task_id')=='task-a']
            assert len(tasks)==1,'Scheduling the same recovery twice duplicated the task'
            resume.settle(tasks[0]['id'])
        app_a.native_sessions.close();app_b.native_sessions.close()


if __name__ == '__main__':
    main()
