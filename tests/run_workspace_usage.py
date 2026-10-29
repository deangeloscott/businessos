"""Usage accounting: missing data, duplicate events, cumulative costs and isolation."""
from pathlib import Path
import json
import os
import sys
import tempfile
import threading
import time
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import workspace_usage as usage


def main():
    # Usage chooses a display automatically without switching native context or crossing businesses.
    views_prefs={'active_chats':{'a':'older'},'chats':[
        {'id':'older','business_id':'a','updated':1}, {'id':'newer','business_id':'a','updated':2},
        {'id':'private','business_id':'b','updated':999}], 'usage_chats':{'newer':{'input_tokens':5}}}
    assert usage.chat_views(views_prefs,'a')[0]['info']['id']=='older'
    assert usage.chat_views(views_prefs,'a','newer')[0]['position']=='Running'
    views_prefs['active_chats'].clear()
    assert [v['info']['id'] for v in usage.chat_views(views_prefs,'a')]==['newer','older']
    assert views_prefs['active_chats']=={}
    many={'active_chats':{'a':'c0'},'chats':[{'id':f'c{i}','business_id':'a','updated':i} for i in range(12)]}
    bounded=usage.chat_views(many,'a','c1')
    assert len(bounded)==5 and [v['info']['id'] for v in bounded]==['c1','c0','c11','c10','c9']
    assert many['active_chats']['a']=='c0'
    policy={'cache':{'expires_at':1300,'refresh_seconds':300,'source':'Observed cache write'}}
    chat={'id':'c','native_id':'native-c','agent':'claude','model':'claude-example','effort':'low','status':'complete'}
    connection={'model':'claude-example','effort':'low'}
    assert usage.can_keep_warm(chat,policy,connection,'claude',now=1100)
    for altered in ({**chat,'agent':'pi'},{**chat,'status':'working'},{**chat,'native_id':None}):
        assert not usage.can_keep_warm(altered,policy,connection,'claude',now=1100)
    assert not usage.can_keep_warm(chat,policy,{**connection,'model':'another'},'claude',now=1100)
    assert not usage.can_keep_warm(chat,policy,connection,'claude',now=1400)
    assert not usage.can_keep_warm(chat,{'cache':{'expires_at':1300}},connection,'claude',now=1100)
    observed={'last':{'input_tokens':100,'cached_input_tokens':80,'at':1000},'cache_hit':{'at':1000}}
    for kind,model in [('codex','gpt-6.1-sol'),('pi','google/gemini-3.8-flash')]:
        candidate={**chat,'agent':kind,'model':model}
        before=json.dumps(observed,sort_keys=True)
        estimate=usage.cache_window(candidate,observed)
        assert estimate['modeled'] and estimate['expires_at']==1300 and estimate['basis']
        assert usage.can_keep_warm(candidate,observed,{'model':model,'effort':'low'},kind,now=1100)
        assert not usage.can_keep_warm(candidate,observed,{'model':model,'effort':'low'},kind,now=1400)
        assert json.dumps(observed,sort_keys=True)==before,'A reference estimate became a provider fact'
        miss={**observed,'last':{'cached_input_tokens':0}}
        assert usage.cache_window(candidate,miss) is None
    assert usage.cache_window({'model':'unidentified'},observed) is None
    assert not usage.can_keep_warm({**chat,'agent':'pi','model':'google:gemini-4-argon'},observed,{'model':'google:gemini-4-argon','effort':'low'},'pi',now=1100)
    assert usage.cache_window({'agent':'codex'},policy)==policy['cache'],'Native policy lost priority'
    assert usage.measure({'prompt_tokens':100,'total_cached_tokens':50},'google')['cached_input_tokens']==50
    # A completed ping alone isn't a cache hit; only confirmed reuse extends observed retention.
    for read,expected in [(80,1400),(0,None)]:
        warm_prefs={'usage_chats':{'c':policy}}
        usage.record(warm_prefs,{'id':'ping','business_id':'a','keep_warm':True,'created':1100,'updated':1101,
                     'usage':{'last':{'input_tokens':100,'cached_input_tokens':read}}},chat,'Claude Code')
        assert warm_prefs['usage_chats']['c'].get('cache',{}).get('expires_at')==expected
    history=[{'role':'user','timestamp':1000}, {'role':'assistant','id':'write','model':'same','timestamp':1001,
        'usage':{'input_tokens':5,'cache_creation':{'ephemeral_5m_input_tokens':50}}},
        {'role':'user','timestamp':1100},{'role':'assistant','id':'hit','model':'same','timestamp':1101,
        'usage':{'input_tokens':5,'cache_read_input_tokens':50}}]
    assert usage.messages_usage(history,'claude')['cache']['expires_at']==1400
    history[-1]['model']='different'
    assert 'cache' not in usage.messages_usage(history,'claude')
    assert usage.measure({})=={}
    missing_usage=usage.omp_accounts({'accountsWithoutUsage':[{'provider':'openrouter'},{'provider':'openai-codex'}]})
    assert [a['mode'] for a in missing_usage]==['api','subscription'], 'API credentials without quota reports became subscriptions'
    assert usage.number(False) is None and usage.number(float('nan')) is None
    assert usage.measure({'input_tokens':0,'output_tokens':0},'codex')['input_tokens']==0
    raw={'input':10,'output':5,'cacheRead':80,'cacheWrite':20,'cost':{'total':.25}}
    pi=usage.measure(raw,'pi',1000)
    assert pi['input_tokens']==110 and pi['cost_kind']=='est'
    assert usage.measure({'input_tokens':110,'cached_input_tokens':80},'codex')['input_tokens']==110
    assert usage.measure({'input_tokens':10,'cache_read_input_tokens':80},'claude')['input_tokens']==90
    assert usage.measure({'prompt_tokens':110,'cost':.12},'openrouter')['cost_kind']=='reported'
    assert 'cost_usd' not in usage.measure({'input_tokens':1})
    messages=[{'id':'m','role':'assistant','usage':raw,'timestamp':1000000}]*2
    assert usage.messages_usage(messages,'pi')['input_tokens']==110
    latest=[{'id':'m','role':'assistant','usage':{'input':10,'output':1}},
            {'id':'m','role':'assistant','usage':{'input':10,'output':5}}]
    assert usage.messages_usage(latest,'pi')['output_tokens']==5
    replay={'role':'assistant','timestamp':1000,'content':[{'type':'text','text':'Hello'}],'usage':raw}
    assert usage.messages_usage([replay,replay],'pi')['input_tokens']==110
    assert usage.messages_usage([replay,{**replay,'timestamp':1001}],'pi')['input_tokens']==220
    prefs={}
    chat={'id':'chat','model':'example'}
    job={'id':'request','business_id':'a','updated':time.time(),'usage':pi}
    usage.record(prefs,job,chat,'Pi');usage.record(prefs,job,chat,'Pi')
    assert len(prefs['usage_receipts'])==1
    assert usage.summary(prefs,'a','chat')['totals']['cost_usd']==.25
    assert usage.summary(prefs,'b','chat')['requests']==0
    assert usage.summary(prefs,'a','chat','today')['budget_costs']=={},'Unknown subscription-equivalent cost entered the API budget'
    # Native history can update a chat total without reassigning past spend to today.
    usage.remember(prefs,'chat',{'input_tokens':1000,'last':{'cached_input_tokens':500}},'session')
    assert usage.summary(prefs,'a','chat','chat')['totals']['input_tokens']==1000
    assert usage.summary(prefs,'a','chat','today')['totals']['input_tokens']==110
    session={}
    cj={'id':'c','model':'claude'}
    def cost_job(ident,amount,new=False):
        return {'id':ident,'business_id':'a','updated':time.time(),'new_native_chat':new,
                'usage':{'session_cost_usd':amount,'cost_kind':'est'}}
    usage.record(session,cost_job('1',2,True),cj,'Claude')
    usage.record(session,cost_job('2',3),cj,'Claude')
    assert usage.summary(session,'a','c','today')['totals']['cost_usd']==3
    usage.remember(session,'c',{'input_tokens':500},'session')
    usage.record(session,cost_job('3',4),cj,'Claude')
    assert usage.summary(session,'a','c','today')['totals']['cost_usd']==4
    # A resumed session with an unknown baseline must not bill its entire past again.
    unknown={}
    usage.record(unknown,cost_job('old',10),cj,'Claude')
    assert 'cost_usd' not in usage.summary(unknown,'a','c','today')['totals']
    assert usage.summary(unknown,'a','c','chat')['totals']['cost_usd']==10
    assert usage.summary(unknown,'a','c','today')['missing_costs']==1
    # The preferred bucket map suppresses the legacy duplicate. Unknown quota != 0%.
    quota={'primary':{'usedPercent':25,'windowDurationMins':300,'resetsAt':2000}}
    assert len(usage.codex_limits({'rateLimits':quota,'rateLimitsByLimitId':{'codex':quota}}))==1
    assert usage.codex_limits({'rateLimits':{'primary':{'usedPercent':None}}})==[]
    assert usage.claude_limits({'status':'allowed','resetsAt':2000})[0].get('used_percent') is None
    assert usage.claude_limits({'status':'allowed_warning','utilization':.95})[0]['used_percent']==95
    # Key/account totals are provider snapshots, not another set of request receipts.
    from io import BytesIO
    with patch.object(usage,'build_opener') as opener:
        opener.return_value.open.side_effect=[BytesIO(json.dumps({'data':{'limit_remaining':0,'usage_monthly':2.5,'usage_daily':0}}).encode()),
            BytesIO(json.dumps({'data':{'total_credits':20,'total_usage':12}}).encode())]
        account=usage.openrouter_limits('test-only-key')
        assert account['key_limit_remaining_usd']==0 and account['spend_month_usd']==2.5
        assert account['balance_usd']==8 and account['account_spend_total_usd']==12
        assert account['spend_today_usd']==0
        request=opener.return_value.open.call_args_list[0].args[0]
        assert request.full_url=='https://openrouter.ai/api/v1/key'
        assert 'test-only-key' not in json.dumps(account)
    try:usage.NoRedirect().redirect_request(None,None,302,'',{},'https://other.invalid');raise AssertionError()
    except ValueError:pass
    # Two different accounts never merge because the email or plan matches.
    one=usage.account('openai','personal','same@example.com','plus','Codex')
    one.update(windows=[{'name':'5h','used_percent':20,'resets_at':time.time()+1800}],checked_at=1000,lifetime_tokens=999)
    shared={**one,'via':['OMP'],'checked_at':1001}
    two=usage.account('openai-codex','work','same@example.com','plus','OMP')
    merged=usage.merge_accounts([one,shared,two])
    assert len(merged)==2 and next(a for a in merged if a['id']==one['id'])['via']==['Codex','OMP']
    unknown=usage.account('openai',via='Hermes')
    assert len(usage.merge_accounts([one,unknown]))==2
    unknown.update(linkable=True)
    mapped={}
    usage.link_account(mapped,[one,unknown],unknown['id'],one['id'])
    assert len(usage.merge_accounts(usage.linked_accounts(mapped,[one,unknown])))==1
    replacement={**unknown,'id':'another-native-credential'}
    assert len(usage.merge_accounts(usage.linked_accounts(mapped,[one,replacement])))==2,'Account link followed a different native credential'
    usage.link_account(mapped,[one,unknown],unknown['id'],'')
    assert len(usage.merge_accounts(usage.linked_accounts(mapped,[one,unknown])))==2
    try:usage.link_account({},[one,{**unknown,'provider':'google'}],unknown['id'],one['id']);raise AssertionError()
    except ValueError:pass
    with patch.object(usage,'build_opener') as opener:
        opener.return_value.open.return_value=BytesIO(json.dumps({'code':200,'data':12.5}).encode())
        service=usage.service_account('kie','Kie AI','test-key')
        assert service['credits_remaining']==12.5 and 'balance_usd' not in service
        assert opener.return_value.open.call_args.args[0].full_url=='https://api.kie.ai/api/v1/chat/credit'
    with patch.object(usage,'build_opener') as opener:
        opener.return_value.open.return_value=BytesIO(json.dumps({'character_count':250,'character_limit':1000,'tier':'starter'}).encode())
        service=usage.service_account('elevenlabs','ElevenLabs','test-key')
        assert service['units_remaining']==750 and service['windows'][0]['used_percent']==25
        assert 'balance_usd' not in service
    history={}
    usage.remember_accounts(history,[one])
    switched=usage.remember_accounts(history,[two])
    previous=next(a for a in switched if a['id']==one['id'])
    assert previous['available'] is False and previous['windows'][0]['resets_at']==one['windows'][0]['resets_at']
    assert next(a for a in usage.remember_accounts(history,[{**one,'checked_at':2000}]) if a['id']==one['id'])['available'] is True
    assert 'same@example.com' not in json.dumps(history)
    report={'provider':'openai-codex','fetchedAt':1000000,'metadata':{'accountId':'personal','email':'same@example.com'},
            'limits':[{'window':{'label':'5h','resetsAt':1793228448000},'amount':{'unit':'percent','used':0}}]}
    assert usage.omp_accounts({'reports':[report]})[0]['id']==one['id']
    assert usage.omp_accounts({'reports':[report]})[0]['windows'][0]['used_percent']==0
    cache=usage.measure({'input_tokens':100,'cache_creation':{'ephemeral_5m_input_tokens':80}},'claude',1000)['cache']
    assert cache['est'] and cache['expires_at']==1300
    assert usage.cache_observation({'prompt_cache':{'expires_at':2000}},1000)['expires_at']==2000
    assert usage.cache_observation({'cached_input_tokens':80},1000) is None
    # A missing native usage command must never fall through to a model prompt.
    with patch.object(usage.subprocess,'run') as run:
        run.return_value=type('Reply',(),{'returncode':0,'stdout':'Options: --help\n'})()
        assert usage.native_accounts(['omp','--print'],'omp',ROOT,{})==[]
        assert run.call_count==1 and run.call_args.args[0]==['omp','--help']
    # Client period boundaries account for DST instead of assuming server local time.
    assert usage.summary(prefs,'a','chat','month',since=time.time()-10)['requests']==1
    try:usage.summary(prefs,'a','chat','month',since=time.time()+10000);raise AssertionError()
    except ValueError:pass
    with tempfile.TemporaryDirectory(prefix='aura-usage-') as td,patch.dict(os.environ):
        # Exercise the real stream parser with repeated events; no provider is invoked.
        import workspace_agents
        stream=Path(td)/'native_fixture.py'
        events=[{'type':'session','id':'fixture'},
                {'type':'assistant','message':{'id':'m','role':'assistant','content':[{'type':'text','text':'Done'}],
                 'usage':{'input_tokens':10,'output_tokens':5,'cache_read_input_tokens':80}}}]
        events+=[events[-1],{'type':'rate_limit_event','rate_limit_info':{'status':'allowed_warning','utilization':.95}},
                 {'type':'result','session_id':'fixture','total_cost_usd':2,'usage':{'input_tokens':900}}]
        stream.write_text('import json,sys\nsys.stdin.read()\nfor event in '+repr(events)+':print(json.dumps(event),flush=True)\n')
        updates=[]
        native=workspace_agents.run([sys.executable,str(stream),'-p'],'claude',Path(td),dict(os.environ),'Fixture only',None,'','',lambda **values:updates.append(values))
        assert native['usage']['input_tokens']==90 and native['usage']['output_tokens']==5
        assert native['usage']['session_cost_usd']==2
        assert any(v.get('quota_windows',[{}])[0].get('used_percent')==95 for v in updates if v.get('quota_windows'))
        os.environ['BUSINESSOS_WORKSPACE']=str(Path(td)/'workspace')
        os.environ['BUSINESSOS_WORKSPACE_CONFIG']=str(Path(td)/'pointer.json')
        from workspace_ui import Workspace,handler_for
        from setup import setup
        bid=setup(organization='Usage example')['business_id']
        app=Workspace(settings_file=Path(td)/'prefs.json')
        app.preferences['connected_apps']={'codex':{'kind':'codex'},'antigravity':{'kind':'antigravity'}}
        app.preferences['chats']=[{'id':'known','business_id':bid,'agent':'codex','native_id':'known-native','status':'complete'},
                                  {'id':'foreign','business_id':'another','agent':'codex','native_id':'foreign-native','status':'complete'}]
        calls=[]
        def rpc(command,requests,cwd,env):
            calls.extend(m for m,p in requests)
            if requests[0][0]=='account/read':return [{'account':{'type':'chatgpt','email':'user@example.com','planType':'pro'},'workspaceRouting':{'chatgptAccountId':'native-account'}}]
            if requests[0][0]=='account/usage/read':return [{'summary':{'lifetimeTokens':999},'dailyUsageBuckets':[{'startDate':'2026-10-27','tokens':123}]}]
            return [{'rateLimits':{'primary':{'usedPercent':95,'windowDurationMins':300,'resetsAt':time.time()+3600}}}]
        with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Codex','argv':['codex','exec']}]),patch('workspace_codex.rpc',rpc),patch.object(app,'agent_environment',return_value={}),patch('workspace_codex.history',return_value={'usage':{'input_tokens':42,'last':{'input_tokens':42}}}) as native_history:
            result=app.usage(bid,refresh=True)
            assert set(result['periods'])=={'chat','today','month'}
            assert calls==['account/read','account/rateLimits/read','account/usage/read']
            assert result['accounts'][0]['windows'][0]['used_percent']==95
            assert 'user@example.com' not in json.dumps(result)
            assert result['chat_info']['id']=='known' and result['chat']['input_tokens']==42
            assert app.preferences['active_chats']=={} and native_history.call_count==1
            assert native_history.call_args.args[2]=='known-native'
            app.usage(bid,refresh=True)
            assert result['accounts'][0]['lifetime_tokens']==999
            assert len(calls)==3,'Refresh spam queried the provider repeatedly'
            assert native_history.call_count==1,'Refresh spam reread native histories'
            saved=json.loads(app.settings_file.read_text(encoding='utf-8'))
            assert len(saved['usage_account_history'])==1 and 'native-account' not in json.dumps(saved)
            app.preferences['usage_settings']={bid:{'alerts':True,'budget_usd':None}}
            app.usage(bid);app.usage(bid)
            assert len(app.preferences['notification_items'])==1,'Quota alert was duplicated'
            app.preferences['usage_settings'][bid]['budget_usd']=10
            app.preferences['usage_receipts']=[{'id':'spent','business_id':bid,'chat_id':'c','at':time.time(),'cost_usd':8,'cost_kind':'est','billing':'api'}]
            app.usage(bid);app.usage(bid)
            assert len(app.preferences['notification_items'])==2,'Budget threshold alert was duplicated'
            app.preferences['usage_receipts'][0]['cost_usd']=10
            app.usage(bid);app.usage(bid)
            assert len(app.preferences['notification_items'])==3
            app.preferences['usage_receipts']=[]
            app.save_preferences(portable=True)
            portable=Path(os.environ['BUSINESSOS_WORKSPACE'])/'.businessos/view.json'
            assert not any(k.startswith('usage_') for k in json.loads(portable.read_text()))
        app.preferences['chats']=[]
        app.preferences['usage_chats']={}
        warm_app=Workspace(settings_file=Path(td)/'warm-prefs.json')
        warm_chat={'id':'c','native_id':'native-c','agent':'claude','model':'claude-example','effort':'low',
                   'status':'complete','business_id':bid,'workspace':os.environ['BUSINESSOS_WORKSPACE']}
        warm_app.agent={'name':'Claude Code','argv':['fixture-only']}
        warm_app.connection_kind='claude'
        warm_app.preferences.update(chats=[warm_chat],active_chats={bid:'c'},connection=connection,
                                    usage_chats={'c':{'cache':{**policy['cache'],'expires_at':time.time()+300}}})
        with patch('workspace_agents.run',return_value={'reply':'OK','usage':{'last':{'input_tokens':100,'cached_input_tokens':80}}}) as run,patch.object(warm_app,'agent_environment',return_value={}):
            try:warm_app.start_chat(bid,None,None,keep_warm_id='another');raise AssertionError('Wrong chat accepted')
            except ValueError:pass
            assert not run.called
            warm_job=warm_app.start_chat(bid,None,None,keep_warm_id='c')
            deadline=time.time()+3
            while not warm_app.preferences.get('usage_receipts') and time.time()<deadline:time.sleep(.01)
            assert warm_app.job['status']=='complete' and warm_app.job['keep_warm']
            assert run.call_count==1 and run.call_args.args[5]=='native-c'
            assert run.call_args.args[6:8]==('claude-example','low')
            assert 'Reply with OK only' in run.call_args.args[4]
            assert warm_app.preferences['usage_receipts'][0]['id']==warm_job['id']
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app))
        worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        base='http://127.0.0.1:'+str(server.server_port)
        try:
            def get(path,token=True):
                request=Request(base+path,headers={'X-Aura-Token':app.token} if token else {})
                with urlopen(request) as response:return json.load(response)
            assert get('/api/usage?business='+bid)['requests']==0
            payload={'business':bid,'alerts':False,'budget_usd':'12.50'}
            request=Request(base+'/api/usage/settings',data=json.dumps(payload).encode(),headers={'X-Aura-Token':app.token,'Content-Type':'application/json'})
            with urlopen(request) as response:assert json.load(response)['saved']
            assert get('/api/usage?business='+bid)['settings']=={'alerts':False,'budget_usd':12.5}
            # The real endpoint refuses stale/wrong chat targets without starting any model.
            with patch.object(app,'request_text',side_effect=AssertionError('Unexpected model request')):
                request=Request(base+'/api/usage/keep-warm',data=json.dumps({'business':bid,'chat_id':'missing'}).encode(),headers={'X-Aura-Token':app.token,'Content-Type':'application/json'})
                try:urlopen(request);raise AssertionError('Unexpected cache refresh')
                except HTTPError as exc:assert exc.code==400
            for path,code in [('/api/usage?business='+bid,403),('/api/usage?business=not-this-business',400)]:
                try:get(path,token=code!=403);raise AssertionError('Unexpected access')
                except HTTPError as exc:assert exc.code==code
        finally:server.shutdown();server.server_close();worker.join()
    print('Usage accounting, no-double-counting, quota metadata, quiet alerts and HTTP isolation passed.')


if __name__=='__main__':main()
